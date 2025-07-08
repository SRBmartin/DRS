import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SurveyService } from '../../../../../../../shared/services/survey.service';
import { CommonDialogsService } from '../../../../../../../shared/services/commondialog.service';
import { ToastService } from '../../../../../../../shared/services/toast.service';
import { LoaderService } from '../../../../../../../shared/services/loader.service';
import { SurveyDetailsRequest } from '../../../../../../../shared/dto/requests/survey/survey-details-request';
import { SurveyDetailsResponse } from '../../../../../../../shared/dto/responses/survey/survey-details-response';
import { AnswerSurveyWebsiteRequest } from '../../../../../../../shared/dto/requests/survey/answer-survey-website-request';
import { RouteNames } from '../../../../../../../shared/consts/routes';
import { AnswerSurveyWebsiteResponse } from '../../../../../../../shared/dto/responses/survey/answer-survey-website-response';

@Component({
  selector: 'app-answer-survey-website',
  templateUrl: './answer-survey-website.component.html',
  styleUrl: './answer-survey-website.component.scss'
})
export class AnswerSurveyWebsiteComponent implements OnInit{
  surveyId!: string;
  surveyTitle!: string;
  surveyQuestion!: string;
  selectedAnswer!: string | null;
  isAnonymous!: boolean;
  endDate!: string;
  endDateTime: Date | null = null;
  isClosed!: boolean;
  isUsersClosed!: boolean;
  isDialogOpen = false;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly surveyService: SurveyService,
    private readonly dialogService: CommonDialogsService,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.surveyId = this.route.snapshot.paramMap.get('survey_id')!;
    this.fetchSurveyDetails();
  }

  private fetchSurveyDetails(): void {
    const request: SurveyDetailsRequest = { survey_id: this.surveyId };
    this.loaderService.startLoading();
    
    this.surveyService.getSurveyDetails(request).subscribe({
      next: (response: SurveyDetailsResponse) => {
        this.surveyTitle = response.data?.title ?? '';
        this.surveyQuestion = response.data?.question ?? '';
        this.isAnonymous = response.data?.is_anonymous ?? false;

        if (response.data?.ending_time) {
          this.endDateTime = new Date(response.data.ending_time + 'Z'); 
          this.endDate = this.endDateTime.toLocaleString();
        } else {
          this.endDate = 'No end date specified';
        }
      
        this.isUsersClosed = response.data?.user_ended ?? false;
        this.updateIsClosed();
        this.loaderService.stopLoading();
      },
      error: () => {
        this.toastService.showError('Failed to load survey details.', 'Error');
        this.loaderService.stopLoading();
      }
    });
  }

  private updateIsClosed(): void{
    if ((this.endDateTime && this.endDateTime < new Date()) || this.isUsersClosed) {
      this.isClosed = true;
    }
  }

  selectAnswer(option: string): void {
    this.updateIsClosed();
    if (this.isClosed) {
      this.toastService.showError('This survey is closed.', 'Error');
      return;
    }

    this.isDialogOpen = true;
    this.dialogService
      .openConfirmationDialog('Confirm Your Answer', `Are you sure you want to select "${option}"?`)
      .afterClosed()
      .subscribe((confirmed: boolean) => {
        this.isDialogOpen = false;
        if (confirmed) {
          this.submitAnswer(option);
        } else {
          this.selectedAnswer = null;
        }
      });
  }

  private submitAnswer(option: string): void {
    this.updateIsClosed();
    if (this.isClosed) {
      this.toastService.showError('This survey is closed.', 'Error');
      return;
    }
    const request: AnswerSurveyWebsiteRequest = {
      survey_id: this.surveyId,
      response: option
    };

    this.loaderService.startLoading();
    this.surveyService.answerSurveyByWebsite(request).subscribe({
      next: (response: AnswerSurveyWebsiteResponse) => {
        this.selectedAnswer = option;
        this.toastService.showSuccess(response.message || 'Response submitted successfully!', 'Success');
        this.loaderService.stopLoading();
        this.router.navigate([RouteNames.DashboardRoute]);
      },
      error: (error) => {
        const errorMessage = error.message || 'Failed to submit response.';
        this.toastService.showError(errorMessage, 'Error');
        this.loaderService.stopLoading();
      }
    });
  }
}
import { Component } from '@angular/core';
import { AnswerSurveyEmailRequest } from '../../../../../../../shared/dto/requests/survey/answer-survey-email-request';
import { SurveyDetailsRequest } from '../../../../../../../shared/dto/requests/survey/survey-details-request';
import { SurveyDetailsResponse } from '../../../../../../../shared/dto/responses/survey/survey-details-response';
import { ActivatedRoute, Router } from '@angular/router';
import { SurveyService } from '../../../../../../../shared/services/survey.service';
import { CommonDialogsService } from '../../../../../../../shared/services/commondialog.service';
import { ToastService } from '../../../../../../../shared/services/toast.service';
import { LoaderService } from '../../../../../../../shared/services/loader.service';
import { AnswerSurveyEmailResponse } from '../../../../../../../shared/dto/responses/survey/answer-survey-email-response';

@Component({
  selector: 'app-answer-survey-email',
  templateUrl: './answer-survey-email.component.html',
  styleUrl: './answer-survey-email.component.scss'
})
export class AnswerSurveyEmailComponent {
  surveyTitle!: string;
  surveyQuestion!: string;
  emailId!: string;
  surveyId!: string;
  responseId!: string;
  selectedAnswer!: string | null;
  isAnswerConfirmed: boolean = false;
  isDialogOpen: boolean = false;
  isAnonymous!: boolean;
  endDate!: string;
  endDateTime: Date | null = null;
  isClosed!: boolean;
  isUserClosed!: boolean;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly surveyService: SurveyService,
    private readonly dialogService: CommonDialogsService,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService
  ) {}

  ngOnInit(): void {
    this.emailId = this.route.snapshot.paramMap.get('email_id')!;
    this.emailId = this.emailId?.replace(/[<>]/g, '').split(' ')[1] ?? this.emailId;

    this.surveyId = this.route.snapshot.paramMap.get('survey_id')!;
    this.responseId = this.route.snapshot.paramMap.get('response_id')!;
    const initialAnswer = this.route.snapshot.paramMap.get('option');

    if (initialAnswer){
      this.selectAnswer(initialAnswer);
    }

    this.fetchSurveyDetails();
  }

  private fetchSurveyDetails(): void {
    const request: SurveyDetailsRequest = {
      survey_id: this.surveyId
    };
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
        this.isUserClosed = response.data?.user_ended ?? false;
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
    if ((this.endDateTime && this.endDateTime < new Date()) || this.isUserClosed) {
      this.isClosed = true;
    }
  }

  submitAnswer(option: string): void {
    this.updateIsClosed();
    if (this.isClosed) {
      this.toastService.showError('The survey deadline has passed. You can no longer submit an answer.', 'Survey Expired');
      return;
    }

    const request: AnswerSurveyEmailRequest = {
      email_id: this.emailId,
      survey_id: this.surveyId,
      response_id: this.responseId,
      option: option
    };
    this.loaderService.startLoading();
    this.surveyService.answerSurveyByEmail(request).subscribe({
      next: (response: AnswerSurveyEmailResponse) => {
        this.selectedAnswer = option;
        this.toastService.showSuccess(response.message || 'Your response has been submitted.', 'Success');
        this.loaderService.stopLoading();
      },
      error: (error) => {
        const errorMessage = error.message || 'Failed to submit response.';
        this.toastService.showError(errorMessage, 'Error');
        this.loaderService.stopLoading();
      }
    });
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
}

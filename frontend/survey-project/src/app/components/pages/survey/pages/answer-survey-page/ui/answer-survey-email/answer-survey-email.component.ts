import { Component } from '@angular/core';
import { AnswerSurveyEmailRequest } from '../../../../../../../shared/dto/requests/survey/answer-survey-email-request';
import { SurveyDetailsRequest } from '../../../../../../../shared/dto/requests/survey/survey-details-request';
import { SurveyDetailsResponse } from '../../../../../../../shared/dto/responses/survey/survey-details-response';
import { ActivatedRoute, Router } from '@angular/router';
import { SurveyService } from '../../../../../../../shared/services/survey.service';
import { CommonDialogsService } from '../../../../../../../shared/services/commondialog.service';
import { ToastService } from '../../../../../../../shared/services/toast.service';

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

  constructor(
    private readonly route: ActivatedRoute,
    private readonly surveyService: SurveyService,
    private readonly dialogService: CommonDialogsService,
    private readonly toastService: ToastService
  ) {}

  ngOnInit(): void {
    this.emailId = this.route.snapshot.paramMap.get('email_id')!;
    this.emailId = this.emailId?.replace(/[<>]/g, '').split(' ')[1] ?? this.emailId;

    this.surveyId = this.route.snapshot.paramMap.get('survey_id')!;
    this.responseId = this.route.snapshot.paramMap.get('response_id')!;
    const initialAnswer = this.route.snapshot.paramMap.get('option');

    if (initialAnswer) {
      this.confirmAnswer(initialAnswer);
    }

    this.fetchSurveyDetails();
  }

  private fetchSurveyDetails(): void {
    const request: SurveyDetailsRequest = {
      survey_id: this.surveyId
    };

    this.surveyService.getSurveyDetails(request).subscribe({
      next: (response: SurveyDetailsResponse) => {
        this.surveyTitle = response.data?.title ?? '';
        this.surveyQuestion = response.data?.question ?? '';
      },
      error: () => {
        this.toastService.showError('Failed to load survey details.', 'Error');
      }
    });
  }

  confirmAnswer(option: string): void {
    this.dialogService
      .openConfirmationDialog('Confirm Your Answer', `Are you sure you want to select "${option}"?`)
      .afterClosed()
      .subscribe((confirmed: boolean) => {
        if (confirmed) {
          this.isAnswerConfirmed = true;
          this.submitAnswer(option);
        } else {
          this.isAnswerConfirmed = false;
          this.selectedAnswer = null;
        }
      });
  }
  

  submitAnswer(option: string): void {
    const request: AnswerSurveyEmailRequest = {
      email_id: this.emailId,
      survey_id: this.surveyId,
      response_id: this.responseId,
      option: option
    };
    console.log(request);
    this.surveyService.answerSurveyByEmail(request).subscribe({
      next: () => {
        this.selectedAnswer = option;
        this.toastService.showSuccess('Your response has been submitted.', 'Success');
      },
      error: () => {
        this.toastService.showError('Failed to submit your response.', 'Error');
      }
    });
  }

  selectAnswer(option: string): void {
    this.selectedAnswer = option;
    this.confirmAnswer(option);
  }
}

import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { ToastService } from '../../../../../shared/services/toast.service';
import { SurveyService } from '../../../../../shared/services/survey.service';
import { CreateSurveyRequest } from '../../../../../shared/dto/requests/survey/create-survey-request';
import { LoaderService } from '../../../../../shared/services/loader.service';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../../shared/consts/routes';
import { CreateSurveyResponse } from '../../../../../shared/dto/responses/survey/create-survey-response';

@Component({
  selector: 'app-create-survey-page',
  templateUrl: './create-survey-page.component.html',
  styleUrls: ['./create-survey-page.component.scss']
})
export class CreateSurveyPageComponent implements OnInit {
  surveyForm!: FormGroup;

  constructor(
    private readonly fb: FormBuilder,
    private readonly toastService: ToastService,
    private readonly surveyService: SurveyService,
    private readonly loaderService: LoaderService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.surveyForm = this.fb.group({
      surveyTitle: ['', [Validators.required, Validators.maxLength(200)]],
      surveyQuestion: ['', [Validators.required, Validators.maxLength(1000)]],
      surveyDate: [null, [Validators.required, this.futureDateValidator.bind(this)]],
      anonymous: [false],
      emails: [[]]
    });
  }

  onEmailsChanged(emails: string[]): void {
    this.surveyForm?.get('emails')?.setValue(emails);
  }

  onSubmit(): void {
    
    if (this.surveyForm.valid && this.surveyForm?.get('emails')?.value.length > 0) {
      const request = this.createSurveyRequest();
      this.handleCreateSurveyRequest(request);
    } else if(this.surveyForm.valid && this.surveyForm?.get('emails')?.value.length === 0) {
      this.toastService.showError('Add at least one email.');
    }else {
      this.toastService.showError('Check input errors and try again.');
      this.surveyForm.markAllAsTouched();
    }
  }

  createSurveyRequest(): CreateSurveyRequest {
    const rawDateValue = this.surveyForm.get('surveyDate')?.value;
    const formattedDate = this.formatDateTime(new Date(rawDateValue));
    const request: CreateSurveyRequest = {
      title: this.surveyForm.get('surveyTitle')?.value,
      question: this.surveyForm.get('surveyQuestion')?.value,
      ending_time: formattedDate,
      is_anonymous: this.surveyForm.get('anonymous')?.value,
      emails: this.surveyForm.get('emails')?.value
    };
    return request;
  }

  handleCreateSurveyRequest(request: CreateSurveyRequest): void {
    this.loaderService.startLoading();
    this.surveyService
        .createSurvey(request)
        .subscribe({
          next: (response: CreateSurveyResponse) => {
            if(response.survey) {
              this.toastService.showSuccess('Survey created successfully.');
              this.navigateToSurveyDetails(response.survey.id);
            } else {
              this.toastService.showError(response.message ?? 'An error occurred while creating survey.');
            }
            this.loaderService.stopLoading();
          },
          error: (e: any) => {
            this.toastService.showError(e.message ?? 'An error occurred while creating survey.');
            this.loaderService.stopLoading();
          }
        });
  }

  private futureDateValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) {
      return null;
    }
    const inputDate = new Date(control.value);
    const now = new Date();
    return inputDate <= now ? { pastDate: true } : null;
  }
  
  private formatDateTime(date: Date): string {
    const pad = (n: number) => n < 10 ? '0' + n : n;
    const year = date.getUTCFullYear();
    const month = pad(date.getUTCMonth() + 1);
    const day = pad(date.getUTCDate());
    const hours = pad(date.getUTCHours());
    const minutes = pad(date.getUTCMinutes());
    const seconds = pad(date.getUTCSeconds());
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  }
  

  private navigateToSurveyDetails(survey_id: string) {
    const route = `${RouteNames.SurveyRoute}/${RouteNames.SurveyDetailsRoute.replace(':survey_id', survey_id)}`;
    this.router.navigate([route]);
  }

}

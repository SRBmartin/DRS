import { Component, OnInit } from '@angular/core';
import { SurveyService } from '../../../../../shared/services/survey.service';
import { ActivatedRoute } from '@angular/router';
import { ToastService } from '../../../../../shared/services/toast.service';
import { LoaderService } from '../../../../../shared/services/loader.service';
import { SurveyResultsRequest } from '../../../../../shared/dto/requests/survey/survey-results-request';
import { SurveyResultsResponse } from '../../../../../shared/dto/responses/survey/survey-results-response';
import { DEFAULT_CHART_LEGEND, DEFAULT_CHART_OPTIONS, DEFAULT_CHART_TYPE, INITIAL_CHART_DATA } from './const/chart.config';
import { UserEndedRequest } from '../../../../../shared/dto/requests/survey/user_ended_request';
import { UserEndedResponse } from '../../../../../shared/dto/responses/survey/user_ended_response';
@Component({
  selector: 'app-survey-details',
  templateUrl: './survey-details.component.html',
  styleUrl: './survey-details.component.scss'
})
export class SurveyDetailsComponent implements OnInit {
  public chartType = DEFAULT_CHART_TYPE;
  public chartLegend = DEFAULT_CHART_LEGEND;

  constructor(
    private readonly surveyService: SurveyService,
    private readonly route: ActivatedRoute,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService
  ) {}

  public chartOptions = DEFAULT_CHART_OPTIONS;

  public chartData = INITIAL_CHART_DATA;

  public totalResponses = 0;
  public isAnonymous = true;
  public respondents: { name: string; email: string; answer: string }[] = [];
  public title = '';
  public question = '';
  public isClosed = false;
  private surveyId: string | null = null;
  ngOnInit(): void {
    const survey_id = this.route.snapshot.paramMap.get('survey_id');
    if (survey_id) {
      this.surveyId = survey_id;
      this.fetchSurveyResults(survey_id);
    }
  }

  private fetchSurveyResults(surveyId: string): void {
    this.loaderService.startLoading();
    const request: SurveyResultsRequest = { survey_id: surveyId };

    this.surveyService.getSurveyResults(request).subscribe({
      next: (response: SurveyResultsResponse) => {
        const yes = response.responses.yes;
        const no = response.responses.no;
        const maybe = response.responses.maybe;
        this.totalResponses = yes + no + maybe;

        const yesPercent = (yes / this.totalResponses) * 100;
        const noPercent = (no / this.totalResponses) * 100;
        const maybePercent = (maybe / this.totalResponses) * 100;

        this.chartData = {
          labels: ['Yes', 'No', 'Maybe'],
          datasets: [{
            data: [yesPercent, noPercent, maybePercent],
            backgroundColor: ['#4CAF50', '#F44336', '#9E9E9E']
          }]
        };

        this.title = response.title;
        this.question = response.question;
        this.isClosed = response.user_ended || new Date(response.ending_time) < new Date();
        this.isAnonymous = response.is_anonymous;
        this.respondents = response.user_responses.map(u => ({
          name: '',
          email: u.email,
          answer: u.response
        }));

        this.loaderService.stopLoading();
      },
      error: (err) => {
        this.toastService.showError(err.message || 'Unexpected error occurred.', 'Error');
        this.loaderService.stopLoading();
      }
    });
  }

  getPercentage(index: number): number {
    const val = this.chartData.datasets[0].data[index];
    return typeof val === 'number' ? val : 0;
  }

  getCount(index: number): number {
    return Math.round((this.getPercentage(index) / 100) * this.totalResponses);
  }
  public closeSurvey(): void {
    if (!this.surveyId) {
      this.toastService.showError('Invalid survey.', 'Error');
      return;
    }
  
    const request: UserEndedRequest = { survey_id: this.surveyId };
  
    this.loaderService.startLoading();
    this.surveyService.endSurvey(request).subscribe({
      next: (response: UserEndedResponse) => {
        this.toastService.showSuccess(response.message || 'Survey successfully closed.', 'Success');
        this.isClosed = true;
        this.loaderService.stopLoading();
      },
      error: (err) => {
        this.toastService.showError(err.message || 'Failed to close survey.', 'Error');
        this.loaderService.stopLoading();
      }
    });
  }
}
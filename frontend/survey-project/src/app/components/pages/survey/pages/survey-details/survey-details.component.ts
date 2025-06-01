import { Component, OnInit } from '@angular/core';
import { ChartData, ChartOptions, ChartType } from 'chart.js';
import { SurveyService } from '../../../../../shared/services/survey.service';
import { ActivatedRoute } from '@angular/router';
import { ToastService } from '../../../../../shared/services/toast.service';
import { LoaderService } from '../../../../../shared/services/loader.service';
import { SurveyResultsRequest } from '../../../../../shared/dto/requests/survey/survey-results-request';
import { SurveyResultsResponse } from '../../../../../shared/dto/responses/survey/survey-results-response';

@Component({
  selector: 'app-survey-details',
  templateUrl: './survey-details.component.html',
  styleUrl: './survey-details.component.scss'
})
export class SurveyDetailsComponent implements OnInit {
  public chartType: ChartType = 'bar';
  public chartLegend = false;

  constructor(
    private readonly surveyService: SurveyService,
    private readonly route: ActivatedRoute,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService
  ) {}

  public chartOptions: ChartOptions = {
    responsive: true,
    indexAxis: 'y',
    scales: {
      x: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value: number | string) => `${value}%`
        }
      }
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.x}%`
        }
      }
    }
  };

  public chartData: ChartData<'bar', number[], string | string[]> = {
    labels: ['Yes', 'No', 'No Response'],
    datasets: [{
      data: [0, 0, 0],
      backgroundColor: ['#4CAF50', '#F44336', '#9E9E9E']
    }]
  };

  public totalResponses = 0;
  public isAnonymous = true;
  public respondents: { name: string; email: string; answer: string }[] = [];
  public title = '';
  public question = '';
  public isClosed = false;


  ngOnInit(): void {
    const survey_id = this.route.snapshot.paramMap.get('survey_id');
    if (survey_id) {
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
        const noResponse = response.responses['no response'];
        this.totalResponses = yes + no + noResponse;

        const yesPercent = (yes / this.totalResponses) * 100;
        const noPercent = (no / this.totalResponses) * 100;
        const noResponsePercent = (noResponse / this.totalResponses) * 100;

        this.chartData = {
          labels: ['Yes', 'No', 'No Response'],
          datasets: [{
            data: [yesPercent, noPercent, noResponsePercent],
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
}

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { GetMySurveysResponse, SurveyDto } from '../../../../../shared/dto/responses/survey/get-my-surveys-response';
import { GetSurveysForMeResponse } from '../../../../../shared/dto/responses/survey/get-surveys-for-me-response';
import { SurveyService } from '../../../../../shared/services/survey.service';
import { LoaderService } from '../../../../../shared/services/loader.service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { error } from 'jquery';

@Component({
  selector: 'app-survey-list',
  templateUrl: './survey-list.component.html',
  styleUrl: './survey-list.component.scss'
})
export class SurveyListComponent implements OnChanges {
  @Input() mode: 'createdByMe' | 'forMe' = 'createdByMe';
  @Input() order: string = 'From newest to oldest';
  @Input() searchQuery: string = '';

  surveys: SurveyDto[] = [];

  originalSurveys: SurveyDto[] = []


  ngOnChanges(changes: SimpleChanges): void {
    if (changes['mode']) {
      this.fetchSurveys(); 
    }

    if (changes['order'] || changes['searchQuery']) {
      this.applyFilters();
    }
  }

  constructor(
    private surveyService: SurveyService,
    private readonly loaderService: LoaderService,
    private readonly toastService: ToastService
  ) {}

  private applyFilters(): void {
    let filtered = [...this.originalSurveys];

    if (this.searchQuery.trim()) {
      const lowerQuery = this.searchQuery.toLowerCase();
      filtered = filtered.filter(survey =>
        survey.title.toLowerCase().includes(lowerQuery) ||
        survey.question.toLowerCase().includes(lowerQuery)
      );
    }

    this.surveys = this.sortSurveys(filtered, this.order);
  }


  fetchSurveys(): void {
    this.loaderService.startLoading();

    const observable =
      this.mode === 'createdByMe'
        ? this.surveyService.getMySurveys()
        : this.surveyService.getSurveysForMe();

    observable.subscribe({
      next: (res: GetMySurveysResponse | GetSurveysForMeResponse) => {
        this.originalSurveys = res.surveys ?? [];
        this.applyFilters();
        this.loaderService.stopLoading();
      },
      error: (e: any) => {
        this.originalSurveys = [];
        this.surveys = [];
        this.loaderService.stopLoading();
        this.toastService.showError(e.message ?? '', "Error fetching surveys");
      }
    });
  }

  isExpired(endingTime: string): boolean {
    return new Date(endingTime).getTime() < new Date().getTime();
  }

  private sortSurveys(surveys: SurveyDto[], order: string): SurveyDto[] {
    switch (order) {
      case 'From newest to oldest':
        return surveys.sort((a, b) => new Date(b.ending_time).getTime() - new Date(a.ending_time).getTime());
      case 'From oldest to newest':
        return surveys.sort((a, b) => new Date(a.ending_time).getTime() - new Date(b.ending_time).getTime());
      case 'First open then closed':
        return surveys.sort((a, b) => {
          const aClosed = this.isExpired(a.ending_time) || a.user_ended;
          const bClosed = this.isExpired(b.ending_time) || b.user_ended;
          return Number(aClosed) - Number(bClosed);
        });
      case 'First closed then open':
        return surveys.sort((a, b) => {
          const aClosed = this.isExpired(a.ending_time) || a.user_ended;
          const bClosed = this.isExpired(b.ending_time) || b.user_ended;
          return Number(bClosed) - Number(aClosed);
        });
      default:
        return surveys;
    }
  }

  onSearchChanged(query: string): void {
    this.searchQuery = query;
  }
}

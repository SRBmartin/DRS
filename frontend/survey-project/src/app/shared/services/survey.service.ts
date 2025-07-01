import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../environment/environment";
import { CreateSurveyRequest } from "../dto/requests/survey/create-survey-request";
import { catchError, Observable, throwError } from "rxjs";
import { CreateSurveyResponse } from "../dto/responses/survey/create-survey-response";
import { SurveyResultsResponse } from "../dto/responses/survey/survey-results-response";
import { SurveyResultsRequest } from "../dto/requests/survey/survey-results-request";
import { AnswerSurveyEmailRequest } from "../dto/requests/survey/answer-survey-email-request";
import { AnswerSurveyEmailResponse } from "../dto/responses/survey/answer-survey-email-response";
import { AnswerSurveyWebsiteRequest } from "../dto/requests/survey/answer-survey-website-request";
import { AnswerSurveyWebsiteResponse } from "../dto/responses/survey/answer-survey-website-response";
import { SurveyDetailsRequest } from "../dto/requests/survey/survey-details-request";
import { SurveyDetailsResponse } from "../dto/responses/survey/survey-details-response";
import { DeleteSurveyResponse } from "../dto/responses/survey/delete-survey-response";

@Injectable({
    providedIn: 'root'
})
export class SurveyService {
    private readonly baseUrl!: string;

    constructor(
        private readonly httpClient: HttpClient,
    ){
        this.baseUrl = `${environment.api}/survey`;
    }
    
    createSurvey(request: CreateSurveyRequest): Observable<CreateSurveyResponse> {
        const url = `${this.baseUrl}`;
        return this.httpClient.post<CreateSurveyResponse>(url, request)
                    .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                    );
    }

    getSurveyResults(request: SurveyResultsRequest): Observable<SurveyResultsResponse> {
        const url = `${this.baseUrl}/details/${request.survey_id}`;
        return this.httpClient.get<SurveyResultsResponse>(url)
            .pipe(
                catchError((e: HttpErrorResponse) => {
                    return throwError(e.error);
                })
            );
    }
    answerSurveyByEmail(request: AnswerSurveyEmailRequest): Observable<AnswerSurveyEmailResponse> {
        const url = `${this.baseUrl}/answer/mail/${request.email_id}/${request.survey_id}/${request.response_id}/${request.option}`;
        return this.httpClient.post<AnswerSurveyEmailResponse>(url, null)
                    .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                    );
    }

    answerSurveyByWebsite(request: AnswerSurveyWebsiteRequest): Observable<AnswerSurveyWebsiteResponse> {
        const url = `${this.baseUrl}/answer/website`;
        return this.httpClient.post<AnswerSurveyWebsiteResponse>(url, request)
                    .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                    );
    }

    getSurveyDetails(request: SurveyDetailsRequest): Observable<SurveyDetailsResponse> {
        const url = `${this.baseUrl}/details`;
        return this.httpClient.post<SurveyDetailsResponse>(url, request)
                    .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                    );
    }

    deleteSurvey(surveyId: string): Observable<DeleteSurveyResponse> {
        const url = `${this.baseUrl}/${surveyId}`;
        return this.httpClient.delete<DeleteSurveyResponse>(url).pipe(
            catchError((e: HttpErrorResponse) => {
                return throwError(() => e.error);
            })
        );
    }
}
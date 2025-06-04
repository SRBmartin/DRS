import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../environment/environment";
import { CreateSurveyRequest } from "../dto/requests/survey/create-survey-request";
import { catchError, Observable, throwError } from "rxjs";
import { CreateSurveyResponse } from "../dto/responses/survey/create-survey-response";
import { SurveyResultsResponse } from "../dto/responses/survey/survey-results-response";
import { SurveyResultsRequest } from "../dto/requests/survey/survey-results-request";
import { UserEndedRequest } from "../dto/requests/survey/user_ended_request";
import { UserEndedResponse } from "../dto/responses/survey/user_ended_response";

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
    endSurvey(request: UserEndedRequest): Observable<UserEndedResponse> {
        const url = `${this.baseUrl}/end_survey`;

        return this.httpClient.patch<UserEndedResponse>(url, request)
            .pipe(
                catchError((e: HttpErrorResponse) => throwError(e.error))
        );
    }
}
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../environment/environment";
import { CreateSurveyRequest } from "../dto/requests/survey/create-survey-request";
import { catchError, Observable, throwError } from "rxjs";
import { CreateSurveyResponse } from "../dto/responses/survey/create-survey-response";

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

}
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { CheckSSIDRequest } from "../dto/requests/user/check-ssid-request";
import { catchError, Observable, throwError } from "rxjs";
import { RegisterRequest } from "../dto/requests/user/register-request";
import { RegisterResponse } from "../dto/responses/user/register-response";
import { environment } from "../environment/environment";
import { LoginRequest } from "../dto/requests/user/login-request";
import { LoginResponse } from "../dto/responses/user/login-response";
import { DeleteRequest } from "../dto/requests/user/delete-request";
import { DeleteResponse } from "../dto/responses/user/delete-response";
import { LogoutRequest } from "../dto/requests/user/logout-request";
import { LogoutResponse } from "../dto/responses/user/logout-response";
import { ChangePasswordRequest } from "../dto/requests/user/change-password-request";
import { ChangePasswordResponse } from "../dto/responses/user/change-password-response";
import { GeneralInfoResponse } from "../dto/responses/user/general-info-response";
import { ChangeGeneralInformationRequest } from "../dto/requests/user/change-general-info-request";
import { ChangeGeneralInformationResponse } from "../dto/responses/user/change-general-info-response";

@Injectable({
    providedIn: 'root'
})
export class UserService {
    private readonly baseUrl!: string;

    constructor(
        private readonly httpClient: HttpClient,
    ){
        this.baseUrl = `${environment.api}/users`;
    }

    verifySSID(request: CheckSSIDRequest): Observable<any> {
        const url = `${this.baseUrl}/verify`;
        return this.httpClient.post(url, request);
    }

    registerUser(request: RegisterRequest): Observable<RegisterResponse> {
        const url = `${this.baseUrl}`;
        return this.httpClient.post<RegisterResponse>(url, request)
                   .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                   );
    }

    loginUser(request: LoginRequest): Observable<LoginResponse> {
        const url = `${this.baseUrl}/login`;
        return this.httpClient.post<LoginResponse>(url, request)
                   .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                   );
    }

    logoutUser(request: LogoutRequest): Observable<any> {
        const url = `${this.baseUrl}/logout`; 
        return this.httpClient.post<LogoutResponse>(url, request)
                   .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                   );
    }

    deleteUserAccount(request: DeleteRequest): Observable<DeleteResponse> {
        const url = `${this.baseUrl}/delete-account`;  
        return this.httpClient.post<DeleteResponse>(url, request)   
            .pipe(
                catchError((e: HttpErrorResponse) => {
                    return throwError(e.error);
                })
            );
    }

    changePassword(request: ChangePasswordRequest): Observable<ChangePasswordResponse> {
        const url = `${this.baseUrl}/change-password`;

        return this.httpClient.patch<ChangePasswordResponse>(url, request).pipe(
            catchError((e: HttpErrorResponse) => throwError(e.error))
        );
    }
    
    getGeneralInfo(): Observable<GeneralInfoResponse> {
        const url = `${this.baseUrl}/general-information`;
        return this.httpClient.get(url).pipe(
            catchError((e: HttpErrorResponse) => throwError(e.error))
        );
    }
      
    updateGeneralInfo(
        updatedData: ChangeGeneralInformationRequest
    ): Observable<ChangeGeneralInformationResponse> {
        const url = `${this.baseUrl}/save-general-information`;
        return this.httpClient.put<ChangeGeneralInformationResponse>(url, updatedData).pipe(
            catchError((e: HttpErrorResponse) => throwError(e.error))
        );
    }
}
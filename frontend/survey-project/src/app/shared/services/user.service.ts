import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { CheckSSIDRequest } from "../dto/requests/user/check-ssid-request";
import { catchError, Observable, throwError } from "rxjs";
import { RegisterRequest } from "../dto/requests/user/register-request";
import { RegisterResponse } from "../dto/responses/user/register-response";
import { environment } from "../environment/environment";
import { LoginRequest } from "../dto/requests/user/login-request";
import { LoginResponse } from "../dto/responses/user/login-response";

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

    logoutUser(ssid: string): Observable<any> {
        const url = `${this.baseUrl}/logout`; 
        return this.httpClient.post(url, { ssid })  
                   .pipe(
                        catchError((e: HttpErrorResponse) => {
                            return throwError(e.error);
                        })
                   );
    }

    deleteUserAccount(password: string, ssid: string): Observable<any> {
        const url = `${this.baseUrl}/delete-account`;  
        return this.httpClient.post(url, { password, ssid })   
            .pipe(
                catchError((e: HttpErrorResponse) => {
                    return throwError(e.error);
                })
            );
    }

}
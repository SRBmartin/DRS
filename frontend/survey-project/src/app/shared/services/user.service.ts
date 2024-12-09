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

    // changePassword(request: { oldPassword: string, newPassword: string }): Observable<any> {
    //     const url = `${this.baseUrl}/profile-page/change-password`;
    //     return this.httpClient.post(url, request)
    //       .pipe(
    //         catchError((e: HttpErrorResponse) => throwError(e.error))
    //       );
    //   }
    changePassword(request: { oldPassword: string, newPassword: string }, ssid: string): Observable<any> {
        const url = `${this.baseUrl}/profile-page/change-password`;
        const payload = {
            old_password: request.oldPassword, // Map to match backend's expected field names
            new_password: request.newPassword,
        };
    
        return this.httpClient.post(url, payload, {
            headers: {
                Authorization: `Bearer ${ssid}`, // Add the required Authorization header
                'Content-Type': 'application/json' // Ensure Content-Type is JSON
            }
        }).pipe(
            catchError((e: HttpErrorResponse) => throwError(e.error)) // Handle errors
        );
    }
    

}
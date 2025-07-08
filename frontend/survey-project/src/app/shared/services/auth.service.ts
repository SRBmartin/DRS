import { Injectable } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { Session } from "../model/user/session";
import { Router } from "@angular/router";
import { UserService } from "./user.service";
import { Observable } from "rxjs";
import { DeleteRequest } from "../dto/requests/user/delete-request";
import { DeleteResponse } from "../dto/responses/user/delete-response";
import { RouteNames } from "../consts/routes";
import { ToastService } from "./toast.service";


@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(
        private readonly cookieService: CookieService,
        private readonly router: Router,
        private readonly userService: UserService,
        private readonly toastService: ToastService

    ) {}

    loginUser(session: Session): void {
        this.cookieService.set('ssid', session.id, {
            expires: new Date(session.ending_time),
            sameSite: 'Lax',
            secure: true,
            path: '/'
        });
    }

    logoutUser(): void {
        this.userService
        .logoutUser()
        .subscribe(() => {
            this.cookieService.delete('ssid');
            this.router.navigate([RouteNames.LandingRoute]);
        });
    }

    onDeleteUserAccount(): void {
        this.userService
        .logoutUser()
        .subscribe({
            next: () => {
                this.cookieService.delete('ssid'); 
                this.router.navigate([RouteNames.LandingRoute]); 
            },
            error: (err) => {
                this.toastService.showError(err.error.message);
            }
        });
    }

    deleteUserAccount(password: string): Observable<DeleteResponse> {
        const request: DeleteRequest = { password }; 
        return this.userService.deleteUserAccount(request); 
    }
}
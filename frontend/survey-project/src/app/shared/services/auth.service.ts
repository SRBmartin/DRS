import { Injectable } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { Session } from "../model/user/session";
import { Router } from "@angular/router";
import { UserService } from "./user.service";
import { Observable } from "rxjs";
import { DeleteRequest } from "../dto/requests/user/delete-request";
import { DeleteResponse } from "../dto/responses/user/delete-response";


@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(
        private readonly cookieService: CookieService,
        private readonly router: Router,
        private readonly userService: UserService

    ) {}

    loginUser(session: Session): void {
        this.cookieService.set('ssid', session.id, new Date(session.ending_time));
    }

    logoutUser(): void {
    
        this.userService.logoutUser().subscribe({
            next: () => {
                this.cookieService.delete('ssid'); 
                this.router.navigate(['/login']); 

            },
            error: (err) => {
                console.error('Error during logout:', err);
            }
        });
    }
    
    

    goToRegister(): void {
    
        this.userService.logoutUser().subscribe({
            next: () => {
                this.cookieService.delete('ssid'); 
                this.router.navigate(['/register']); 

            },
            error: (err) => {
                console.error('Error during logout:', err);
            }
        });
    }

    deleteUserAccount(password: string): Observable<DeleteResponse> {
        const request: DeleteRequest = { password }; 
        return this.userService.deleteUserAccount(request); 
    }
}
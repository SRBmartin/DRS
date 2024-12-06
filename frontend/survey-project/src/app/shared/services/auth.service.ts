import { Injectable } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { Session } from "../model/user/session";
import { Router } from "@angular/router";
import { UserService } from "./user.service";
import { Observable } from "rxjs";

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
        const ssid = this.cookieService.get('ssid');  
        if (!ssid) {
            this.router.navigate(['/login']);  
            return;
        }

        this.userService.logoutUser(ssid).subscribe({
            next: (response) => {
                console.log('Logout successful', response);  
                this.cookieService.delete('ssid');  
                this.router.navigate(['/login']);  
            },
            error: (err) => {
                console.error('Error during logout:', err);  
            }
        });
    }
    goToRegister(): void {
        const ssid = this.cookieService.get('ssid');  
        if (!ssid) {
            this.router.navigate(['/register']);  
            return;
        }

        this.userService.logoutUser(ssid).subscribe({
            next: (response) => {
                console.log('Logout successful', response);  
                this.cookieService.delete('ssid');  
                this.router.navigate(['/register']);  
            },
            error: (err) => {
                console.error('Error during logout:', err);  
            }
        });
    }

    deleteUserAccount(password: string): Observable<any> {
        const ssid = this.cookieService.get('ssid');  
        if (!ssid) {
          return new Observable();  
        }
    
        return this.userService.deleteUserAccount(password, ssid);
      }
}
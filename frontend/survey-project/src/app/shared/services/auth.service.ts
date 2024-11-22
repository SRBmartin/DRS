import { Injectable } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { Session } from "../model/user/session";
import { Router } from "@angular/router";

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(
        private readonly cookieService: CookieService,
    ) {}

    loginUser(session: Session): void {
        this.cookieService.set('ssid', session.id, new Date(session.ending_time));
    }
}
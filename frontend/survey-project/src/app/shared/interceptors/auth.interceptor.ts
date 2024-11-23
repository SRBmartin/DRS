import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class AuthInterceptor implements HttpInterceptor {
    constructor(
        private readonly cookieService: CookieService
    ) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const ssid = this.cookieService.get('ssid');

        if(ssid){
            const cloned = req.clone({
                setHeaders: {
                    Authorization: `Bearer ${ssid}`,
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': 'application/json'
                }
            })
            return next.handle(cloned);
        }else{
            const cloned = req.clone({
                setHeaders: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': 'application/json'
                }
            })
            return next.handle(cloned);
        }
    }
}
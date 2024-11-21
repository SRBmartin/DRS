import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { RouteNames } from '../consts/routes';
import { UserService } from '../services/user.service';
import { CheckSSIDRequest } from '../dto/requests/user/check-ssid-request';
import { catchError, map, of } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const cookieService = inject(CookieService);
  const userService = inject(UserService);

  const ssid = cookieService.get('ssid');

  if(!ssid){
    router.navigate([RouteNames.LoginRoute]);
    return false;
  }

  const request: CheckSSIDRequest = {
    ssid: ssid
  };

  return userService.
         verifySSID(request).
         pipe(
            map(() => {
              return true;
            }),
            catchError(() => {
              router.navigate([RouteNames.LoginRoute]);
              return of(false);
            })
         );

};

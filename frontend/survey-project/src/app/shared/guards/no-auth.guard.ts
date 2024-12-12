import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { RouteNames } from '../consts/routes';

export const noAuthGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const cookieService = inject(CookieService);

  const ssid = cookieService.get('ssid');

  if(ssid){
    router.navigate([RouteNames.DashboardRoute]);
    return false;
  }else{
    return true;
  }

};

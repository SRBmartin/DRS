import { Component, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  RouteNames = RouteNames;
  hideNavbar: boolean = false;

  constructor(private router: Router, private cookieService: CookieService) {
    this.router.events.subscribe(() => {
      this.hideNavbar = this.router.url === `/${RouteNames.RegisterRoute}`;
    });
  }

  isLoggedIn(): boolean {
    return this.cookieService.check('ssid');
  }
}

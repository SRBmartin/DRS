import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes'
import { CookieService } from 'ngx-cookie-service';
import { BasicButtonComponent } from '../button/basic-button.component';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss'
})
export class FooterComponent {
  RouteNames = RouteNames;
  hideFooter: boolean = false;

  constructor(private router: Router, private cookieService: CookieService) {
    this.router.events.subscribe(() => {
      this.hideFooter = this.router.url === `/${RouteNames.RegisterRoute}`;
    });
  }

  isLoggedIn(): boolean {
    return this.cookieService.check('ssid');
  }
}

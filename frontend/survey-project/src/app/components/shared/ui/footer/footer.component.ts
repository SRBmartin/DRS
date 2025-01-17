import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes';
import { CookieService } from 'ngx-cookie-service';
import { BasicButtonComponent } from '../button/basic-button.component';
import { BehaviorSubject } from 'rxjs';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss',
})
export class FooterComponent implements OnInit {
  currentYear: number = new Date().getFullYear();
  RouteNames = RouteNames;

  hideEntireFooter: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(
    false
  );
  hideUserSections: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(
    true
  );

  constructor(private router: Router, private cookieService: CookieService) {}

  ngOnInit(): void {
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe(() => {
        this.updateFooterVisibility();
      });

    this.updateFooterVisibility();
  }

  isLoggedIn(): boolean {
    const loggedIn = this.cookieService.check('ssid');
    return loggedIn;
  }

  updateFooterVisibility(): void {
    const currentUrl = this.router.url;

    const shouldHideFooter = currentUrl === `/${RouteNames.LoginRoute}` || currentUrl === `/`;
    this.hideEntireFooter.next(shouldHideFooter);

    const shouldHideUserSections = !this.isLoggedIn();
    this.hideUserSections.next(shouldHideUserSections);
  }
}

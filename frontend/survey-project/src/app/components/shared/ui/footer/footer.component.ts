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
    
    // Add check for email answer route
    const isEmailAnswerRoute = currentUrl.startsWith(`/${RouteNames.SurveyRoute}/${RouteNames.AnswerSurveyRoute}/mail`);
    const shouldHideFooter = 
      currentUrl === `/${RouteNames.LoginRoute}` || 
      currentUrl === `/` ||
      isEmailAnswerRoute;
    
    this.hideEntireFooter.next(shouldHideFooter);
  
    // Update user sections visibility
    const shouldHideUserSections = !this.isLoggedIn() || isEmailAnswerRoute;
    this.hideUserSections.next(shouldHideUserSections);
  }
}

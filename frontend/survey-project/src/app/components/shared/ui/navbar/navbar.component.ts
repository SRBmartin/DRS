import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes';
import { CookieService } from 'ngx-cookie-service';
import { BehaviorSubject } from 'rxjs';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../../../shared/services/auth.service';
import { CommonDialogsService } from '../../../../shared/services/commondialog.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  RouteNames = RouteNames;
  currentUrl: string = '';

  hideEntireNavbar: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  hideUserSections: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);

  constructor(
    private readonly router: Router,
    private readonly cookieService: CookieService,
    private readonly authService: AuthService,
    private readonly commonDialogs: CommonDialogsService 
  ) {}

  ngOnInit(): void {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.updateNavbarVisibility();
      });

    this.updateNavbarVisibility();
  }

  isLoggedIn(): boolean {
    const loggedIn = this.cookieService.check('ssid');
    return loggedIn;
  }

  updateNavbarVisibility(): void {
    const currentUrl = this.router.url;
    this.currentUrl = currentUrl;
    
    // Add check for email answer route
    const isEmailAnswerRoute = currentUrl.startsWith(`/${RouteNames.SurveyRoute}/${RouteNames.AnswerSurveyRoute}/mail`);
    const shouldHideNavbar = 
      currentUrl === `/${RouteNames.LoginRoute}` || 
      currentUrl === `/` ||
      isEmailAnswerRoute;
    
    this.hideEntireNavbar.next(shouldHideNavbar);
  
    // Update user sections visibility
    const shouldHideUserSections = !this.isLoggedIn() || isEmailAnswerRoute;
    this.hideUserSections.next(shouldHideUserSections);
  }

  onLogout(): void {
    const currentRoute = this.router.url; 

    this.commonDialogs
      .openConfirmationDialog(
        'Logout',
        'Are you sure you want to logout?'
      )
      .afterClosed()
      .subscribe((confirmed: boolean) => {
        if (confirmed) {
          this.executeLogout();  
          this.router.navigate([currentRoute]);  
        }
      });
  }

  private executeLogout(): void {
    this.authService.logoutUser();  
    
  }
}

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
    private router: Router,
    private cookieService: CookieService,
    private authService: AuthService,
    private commonDialogs: CommonDialogsService 
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
    const shouldHideNavbar =
      currentUrl === `/${RouteNames.LoginRoute}`;
    this.hideEntireNavbar.next(shouldHideNavbar);

    const shouldHideUserSections = !this.isLoggedIn();
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
        } else {
          this.router.navigate([currentRoute]);
        }
      });
  }

  private executeLogout(): void {
    this.authService.logoutUser();  
    
  }
}

import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes';
import { CookieService } from 'ngx-cookie-service';
import { BehaviorSubject } from 'rxjs';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../../../shared/services/auth.service';
import { ModalOpenerService } from '../../../../shared/services/modal-opener.service';
import { GenericConfirmDialogComponent } from '../../generic-confirm-dialog/generic-confirm-dialog.component';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  RouteNames = RouteNames;

  hideEntireNavbar: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  hideUserSections: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);

  constructor(
    private router: Router,
    private cookieService: CookieService,
    private authService: AuthService,
    private modalService: ModalOpenerService 

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

    const shouldHideNavbar =
      currentUrl === `/${RouteNames.LoginRoute}`;
    this.hideEntireNavbar.next(shouldHideNavbar);

    const shouldHideUserSections = !this.isLoggedIn();
    this.hideUserSections.next(shouldHideUserSections);
  }

  onLogout(): void {
    this.modalService
      .openModal(GenericConfirmDialogComponent, {
        title: 'LOGOUT',
        message: 'Are you sure you want to log out?'
      })
      .then((result) => {
        console.log('Modal closed with result:', result);
        if (result) {
          this.authService.logoutUser();
        }
      })
      .catch((error) => {
        console.error('Error in modal:', error);
      });
  }

  
}

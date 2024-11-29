import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes';
import { CookieService } from 'ngx-cookie-service';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent implements OnInit{
  RouteNames = RouteNames;
  hideNavbar: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(
    private router: Router,
    private cookieService: CookieService
  ) { }

  ngOnInit(): void {
    this.router.events.subscribe(() => {
      this.hideNavbar.next(this.router.url === `/${RouteNames.RegisterRoute}`);
    });
  }

  isLoggedIn(): boolean {
    return this.cookieService.check('ssid');
  }

}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../shared/consts/routes'
import { CookieService } from 'ngx-cookie-service';
import { BasicButtonComponent } from '../button/basic-button.component';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss'
})
export class FooterComponent implements OnInit{
  RouteNames = RouteNames;
  hideFooter: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

constructor(
  private router: Router,
  private cookieService: CookieService
) { }

ngOnInit(): void {
  this.router.events.subscribe(() => {
    this.hideFooter.next(this.router.url === `/${RouteNames.RegisterRoute}`);
  });
}

  isLoggedIn(): boolean {
    return this.cookieService.check('ssid');
  }
}

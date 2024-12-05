import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../shared/consts/routes';
import $ from 'jquery';
import 'slick-carousel';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss'
})
export class LandingPageComponent implements OnInit {
  constructor(
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    ($('.text-slider') as any).slick({
      infinite: true,
      autoplay: true,
      autoplaySpeed: 4000,
      arrows: false,
      dots: true,
      speed: 500,
      fade: true,
      cssEase: 'linear',
    });
  }

  onSignInClick(): void {
    this.router.navigate([RouteNames.LoginRoute]);
  }
}

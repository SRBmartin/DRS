import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { noAuthGuard } from './shared/guards/no-auth.guard';
import { authGuard } from './shared/guards/auth.guard';
import { RouteNames } from './shared/consts/routes';

const routes: Routes = [
  {
    path: RouteNames.LandingRoute,
    loadChildren: () => import('./components/pages/landing-page/landing-page.module').then(m => m.LandingPageModule),
    canActivate: [noAuthGuard]
  },
  {
    path: RouteNames.LoginRoute,
    loadChildren: () => import('./components/pages/login-page/login-page.module').then(m => m.LoginPageModule),
    canActivate: [noAuthGuard]
  },
  {
    path: RouteNames.RegisterRoute,
    loadChildren: () => import('./components/pages/register-page/register-page.module').then(m => m.RegisterPageModule),
    canActivate: [noAuthGuard]
  },
  {
    path: RouteNames.DashboardRoute,
    loadChildren: () => import('./components/pages/dashboard-page/dashboard-page.module').then(m => m.DashboardPageModule),
    canActivate: [authGuard]
  },
  {
    path: RouteNames.ProfileRoute,
    loadChildren: () => import('./components/pages/profile-page/profile-page.module').then(m => m.ProfilePageModule),
    canActivate: [authGuard] 
  },
  {
    path: RouteNames.SurveyRoute,
    loadChildren: () => import('./components/pages/survey/survey.module').then(m => m.SurveyModule),
    canActivate: [authGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

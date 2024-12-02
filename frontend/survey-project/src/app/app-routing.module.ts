import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { noAuthGuard } from './shared/guards/no-auth.guard';
import { authGuard } from './shared/guards/auth.guard';
import { RouteNames } from './shared/consts/routes';

const routes: Routes = [
  {
    path: RouteNames.RegisterRoute,
    loadChildren: () => import('./components/pages/register-page/register-page.module').then(m => m.RegisterPageModule),
    canActivate: [noAuthGuard]
  },
  {
    path: RouteNames.LoginRoute,
    loadChildren: () => import('./components/pages/login-page/login-page.module').then(m => m.LoginPageModule),
    canActivate: [noAuthGuard]
  },
  {
    path: RouteNames.ProfileRoute,
    loadChildren: () => import('./components/pages/profile-page/profile-page.module').then(m => m.ProfilePageModule),
    canActivate: [authGuard] 
  },
  {
    path: RouteNames.CreateSurveyRoute,
    loadChildren: () => import('./components/pages/create-survey-page/create-survey-page.module').then(m => m.CreateSurveyPageModule),
    canActivate: [authGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

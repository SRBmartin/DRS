import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RouteNames } from '../../../shared/consts/routes';
import { SurveyComponent } from './survey.component';
import { authGuard } from '../../../shared/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: SurveyComponent,
    children: [
      {
        path: '',
        redirectTo: RouteNames.CreateSurveyRoute,
        pathMatch: 'full'
      },
      {
        path: RouteNames.CreateSurveyRoute,
        loadChildren: () => import('./pages/create-survey-page/create-survey-page.module').then(m => m.CreateSurveyPageModule),
        canActivate: [authGuard]
      },
      {
        path: RouteNames.SurveyDetailsRoute,
        loadChildren: () => import('./pages/survey-details/survey-details.module').then(m => m.SurveyDetailsModule),
        canActivate: [authGuard]
      },
      {
        path: RouteNames.AnswerSurveyRoute,
        loadChildren: () => import('./pages/answer-survey-page/answer-survey-page.module').then(m => m.AnswerSurveyPageModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SurveyRoutingModule { }
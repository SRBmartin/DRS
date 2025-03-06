import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnswerSurveyPageComponent } from './answer-survey-page.component';
import { RouteNames } from '../../../../../shared/consts/routes';
import { AnswerSurveyEmailComponent } from './ui/answer-survey-email/answer-survey-email.component';
import { AnswerSurveyWebsiteComponent } from './ui/answer-survey-website/answer-survey-website.component';
import { authGuard } from '../../../../../shared/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: AnswerSurveyPageComponent,
    children: [
      {
        path: RouteNames.AnswerSurveyEmailRoute,
        component: AnswerSurveyEmailComponent
      },
      {
        path: RouteNames.AnswerSurveyWebsiteRoute,
        component: AnswerSurveyWebsiteComponent,
        canActivate: [authGuard]
      },
      {
        path: '**',
        redirectTo: RouteNames.AnswerSurveyWebsiteRoute
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AnswerSurveyPageRoutingModule { }

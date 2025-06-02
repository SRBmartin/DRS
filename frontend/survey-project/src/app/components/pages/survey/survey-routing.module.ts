import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RouteNames } from '../../../shared/consts/routes';
import { SurveyComponent } from './survey.component';

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
        loadChildren: () => import('./pages/create-survey-page/create-survey-page.module').then(m => m.CreateSurveyPageModule)
      },
      {
        path: RouteNames.SurveyDetailsRoute,
        loadChildren: () => import('./pages/survey-details/survey-details.module').then(m => m.SurveyDetailsModule)
      }
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SurveyRoutingModule { }

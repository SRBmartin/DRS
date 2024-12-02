import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateSurveyPageComponent } from './create-survey-page.component';

const routes: Routes = [
  {
    path: '',
    component: CreateSurveyPageComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CreateSurveyPageRoutingModule { }
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SurveyRoutingModule } from './survey-routing.module';
import { SurveyComponent } from './survey.component';
//import { EmailAnswerPageComponent } from './pages/answer-survey-page/email-answer-page/email-answer-page/email-answer-page.component';


@NgModule({
  declarations: [
    SurveyComponent
  ],
  imports: [
    CommonModule,
    SurveyRoutingModule,
  ]
})
export class SurveyModule { }

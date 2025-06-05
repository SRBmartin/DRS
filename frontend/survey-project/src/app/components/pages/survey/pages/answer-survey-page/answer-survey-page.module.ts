import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AnswerSurveyPageRoutingModule } from './answer-survey-page-routing.module';
import { AnswerSurveyPageComponent } from './answer-survey-page.component';
import { AnswerSurveyEmailComponent } from './ui/answer-survey-email/answer-survey-email.component';
import { AnswerSurveyWebsiteComponent } from './ui/answer-survey-website/answer-survey-website.component';
import { SharedModule } from '../../../../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    AnswerSurveyPageComponent,
    AnswerSurveyEmailComponent,
    AnswerSurveyWebsiteComponent
  ],
  imports: [
    CommonModule,
    AnswerSurveyPageRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class AnswerSurveyPageModule { }

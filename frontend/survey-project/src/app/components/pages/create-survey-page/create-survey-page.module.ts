import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateSurveyPageComponent } from './create-survey-page.component';
import { CreateSurveyPageRoutingModule } from './create-survey-page-routing.module';

@NgModule({
  declarations: [
    CreateSurveyPageComponent
  ],
  imports: [
    CommonModule,
    CreateSurveyPageRoutingModule
  ]
})
export class CreateSurveyPageModule { }

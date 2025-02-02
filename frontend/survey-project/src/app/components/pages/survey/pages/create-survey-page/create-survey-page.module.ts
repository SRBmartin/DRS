import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateSurveyPageComponent } from './create-survey-page.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../../../../shared/shared.module';
import { CreateSurveyPageRoutingModule } from './create-survey-page-routing.module';

@NgModule({
  declarations: [
    CreateSurveyPageComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    SharedModule,
    CreateSurveyPageRoutingModule
  ]
})
export class CreateSurveyPageModule { }

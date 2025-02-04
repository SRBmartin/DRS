import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SurveyDetailsRoutingModule } from './survey-details-routing.module';
import { SurveyDetailsComponent } from './survey-details.component';


@NgModule({
  declarations: [
    SurveyDetailsComponent
  ],
  imports: [
    CommonModule,
    SurveyDetailsRoutingModule
  ]
})
export class SurveyDetailsModule { }

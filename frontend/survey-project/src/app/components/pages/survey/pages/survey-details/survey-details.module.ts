import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SurveyDetailsRoutingModule } from './survey-details-routing.module';
import { SurveyDetailsComponent } from './survey-details.component';
import { NgChartsModule } from 'ng2-charts';


@NgModule({
  declarations: [
    SurveyDetailsComponent
  ],
  imports: [
    CommonModule,
    SurveyDetailsRoutingModule,
    NgChartsModule
  ]
})
export class SurveyDetailsModule { }

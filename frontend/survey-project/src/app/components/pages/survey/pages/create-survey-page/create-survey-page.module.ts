import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateSurveyPageComponent } from './create-survey-page.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../../../../shared/shared.module';
import { CreateSurveyPageRoutingModule } from './create-survey-page-routing.module';
import { EmailDatagridComponent } from './ui/email-datagrid/email-datagrid.component';

@NgModule({
  declarations: [
    CreateSurveyPageComponent,
    EmailDatagridComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule,
    CreateSurveyPageRoutingModule
  ]
})
export class CreateSurveyPageModule { }

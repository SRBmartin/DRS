import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardPageRoutingModule } from './dashboard-page-routing.module';
import { DashboardPageComponent } from './dashboard-page.component';
import { SharedModule } from '../../shared/shared.module';
import { HeaderComponent } from './ui/header/header.component';
import { SurveyListComponent } from './ui/survey-list/survey-list.component';


@NgModule({
  declarations: [
    DashboardPageComponent,
    HeaderComponent,
    SurveyListComponent
  ],
  imports: [
    CommonModule,
    DashboardPageRoutingModule,
    SharedModule,
  ]
})
export class DashboardPageModule { }

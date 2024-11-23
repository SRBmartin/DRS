import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RegisterPageRoutingModule } from './register-page-routing.module';
import { RegisterPageComponent } from './register-page.component';
import { SharedModule } from '../../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    RegisterPageComponent
  ],
  imports: [
    CommonModule,
    RegisterPageRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class RegisterPageModule { }

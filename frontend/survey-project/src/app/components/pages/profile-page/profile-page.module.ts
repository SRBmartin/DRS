import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProfilePageRoutingModule } from './profile-page-routing.module';
import { ProfilePageComponent } from './profile-page.component';
import { ChangePasswordComponent } from './ui/change-password/change-password.component';
import { DeleteMyAccountComponent } from './ui/delete-my-account/delete-my-account.component';
import { GeneralInformationsComponent } from './ui/general-informations/general-informations.component';
import { SharedModule } from '../../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    ProfilePageComponent,
    ChangePasswordComponent,
    DeleteMyAccountComponent,
    GeneralInformationsComponent
  ],
  imports: [
    CommonModule,
    ProfilePageRoutingModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class ProfilePageModule { }

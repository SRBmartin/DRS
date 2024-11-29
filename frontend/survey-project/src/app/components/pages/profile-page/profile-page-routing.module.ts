import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProfilePageComponent } from './profile-page.component';
import { GeneralInformationsComponent } from './ui/general-informations/general-informations.component';
import { ChangePasswordComponent } from './ui/change-password/change-password.component';
import { DeleteMyAccountComponent } from './ui/delete-my-account/delete-my-account.component';

//const routes: Routes = [];

const routes: Routes = [
  {
    path: '',
    component: ProfilePageComponent,
    children: [
      {path: 'general-information', component: GeneralInformationsComponent},
      {path: 'change-password', component: ChangePasswordComponent},
      {path: 'delete-my-account', component: DeleteMyAccountComponent},
      {path: '', redirectTo: 'general-information', pathMatch: 'full'}
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfilePageRoutingModule { }

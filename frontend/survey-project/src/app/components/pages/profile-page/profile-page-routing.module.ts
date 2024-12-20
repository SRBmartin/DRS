import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProfilePageComponent } from './profile-page.component';
import { GeneralInformationsComponent } from './ui/general-informations/general-informations.component';
import { ChangePasswordComponent } from './ui/change-password/change-password.component';
import { DeleteMyAccountComponent } from './ui/delete-my-account/delete-my-account.component';
import { RouteNames } from '../../../shared/consts/routes';

const routes: Routes = [
  {
    path: '',
    component: ProfilePageComponent,
    children: [
      {path: RouteNames.GeneralInformationRoute, component: GeneralInformationsComponent},
      {path: RouteNames.ChangePasswordRoute, component: ChangePasswordComponent},
      {path: RouteNames.DeleteMyAccountRoute, component: DeleteMyAccountComponent},
      {path: '', redirectTo: RouteNames.GeneralInformationRoute, pathMatch: 'full'}
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfilePageRoutingModule { }

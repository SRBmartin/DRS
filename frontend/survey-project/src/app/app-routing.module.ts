import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { noAuthGuard } from './shared/guards/no-auth.guard';
import { authGuard } from './shared/guards/auth.guard';
import { RouteNames } from './shared/consts/routes';

const routes: Routes = [
  {
    path: RouteNames.RegisterRoute,
    loadChildren: () => import('./components/pages/register-page/register-page.module').then(m => m.RegisterPageModule),
    canActivate: [noAuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './ui/navbar/navbar.component';
import { FooterComponent } from './ui/footer/footer.component';



@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    NavbarComponent,
    FooterComponent
  ]
})
export class SharedModule { }

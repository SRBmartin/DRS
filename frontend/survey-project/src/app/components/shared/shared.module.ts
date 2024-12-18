import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';  
import { NavbarComponent } from './ui/navbar/navbar.component';
import { FooterComponent } from './ui/footer/footer.component';
import { BasicInputComponent } from './ui/input/basic-input.component';
import { ReactiveFormsModule } from '@angular/forms';
import { LoaderComponent } from './loader/loader.component';
import { BasicButtonComponent } from './ui/button/basic-button.component';



@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    BasicInputComponent,
    LoaderComponent,
    BasicButtonComponent
    
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule
  ],
  exports: [
    NavbarComponent,
    FooterComponent,
    BasicInputComponent,
    LoaderComponent,
    BasicButtonComponent
  ]
})
export class SharedModule { }

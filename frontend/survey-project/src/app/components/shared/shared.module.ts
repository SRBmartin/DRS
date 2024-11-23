import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './ui/navbar/navbar.component';
import { FooterComponent } from './ui/footer/footer.component';
import { BasicInputComponent } from './ui/input/basic-input.component';
import { ReactiveFormsModule } from '@angular/forms';
import { LoaderComponent } from './loader/loader.component';



@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    BasicInputComponent,
    LoaderComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [
    NavbarComponent,
    FooterComponent,
    BasicInputComponent,
    LoaderComponent
  ]
})
export class SharedModule { }

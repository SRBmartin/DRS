import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';  
import { NavbarComponent } from './ui/navbar/navbar.component';
import { FooterComponent } from './ui/footer/footer.component';
import { BasicInputComponent } from './ui/input/basic-input.component';
import { ReactiveFormsModule } from '@angular/forms';
import { LoaderComponent } from './loader/loader.component';
import { BasicButtonComponent } from './ui/button/basic-button.component';
import { ConfirmationDialogComponent } from './confirmation-dialog/confirmation-dialog.component';
import { SearchInputComponent } from './ui/search-input/search-input.component';
import { SwitchViewComponent } from './ui/switch-view/switch-view.component';
import { BasicDropdownComponent } from './ui/basic-dropdown/basic-dropdown.component';
import { DateTimePickerComponent } from './ui/date-picker/date-time-picker.component';
import { TextareaComponent } from './ui/textarea/textarea.component';



@NgModule({
  declarations: [
    NavbarComponent,
    FooterComponent,
    BasicInputComponent,
    LoaderComponent,
    BasicButtonComponent,
    ConfirmationDialogComponent,
    SearchInputComponent,
    SwitchViewComponent,
    BasicDropdownComponent,
    DateTimePickerComponent,
    TextareaComponent
    
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
    BasicButtonComponent,
    SearchInputComponent,
    SwitchViewComponent,
    BasicDropdownComponent,
    DateTimePickerComponent,
    TextareaComponent
  ]
})
export class SharedModule { }

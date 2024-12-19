import { Injectable } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ModalOpenerService } from './modal-opener.service';
import { ConfirmationDialogComponent } from '../../components/shared/confirmation-dialog/confirmation-dialog.component';

@Injectable({
  providedIn: 'root',
})
export class CommonDialogsService {
  constructor(
    private readonly modalOpener: ModalOpenerService
  ) {}

  openConfirmationDialog(
    title: string,
    question: string
  ): MatDialogRef<ConfirmationDialogComponent> {
    return this.modalOpener.openResponsive(
      ConfirmationDialogComponent,
      { width: '500px', height: '300px' }, 
      { width: '300px', height: '200px' }, 
      { width: '90vw', height: '200px' }, 
      {
        title, 
        question, 
      }
    );
  }
}

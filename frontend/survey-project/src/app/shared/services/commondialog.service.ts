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
      { width: '50dvw', height: '40dvh' }, 
      { width: '50dvw', height: '40dvh' }, 
      { width: '50dvw', height: '40dvh' }, 
      {
        title, 
        question, 
      }
    );
  }
}

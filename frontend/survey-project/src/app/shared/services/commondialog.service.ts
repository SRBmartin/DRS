import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '../../components/shared/confirmation-dialog/confirmation-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class CommonDialogsService {
  constructor(private dialog: MatDialog) {}

  openConfirmationDialog(title: string, question: string) {
    document.body.classList.add('modal-open');
    document.documentElement.style.overflow = 'hidden';  

    
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: { title, question },
      width: '400px',
    });
  
    dialogRef.afterOpened().subscribe(() => {
      setTimeout(() => {
        window.scrollTo(0, 0);  
      }, 0);      
      const modal = document.querySelector('.modal');
      if (modal) {
        modal.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  
    dialogRef.afterClosed().subscribe(() => {
      document.body.classList.remove('modal-open');
      document.documentElement.style.overflow = '';  
    });
  
    return dialogRef;
  }
  
}

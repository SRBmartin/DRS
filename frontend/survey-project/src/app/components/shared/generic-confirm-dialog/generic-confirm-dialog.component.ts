import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-generic-confirm-dialog',
  templateUrl: './generic-confirm-dialog.component.html',
  styleUrls: ['./generic-confirm-dialog.component.scss'],
})
export class GenericConfirmDialogComponent {
  @Input() title: string = '';
  @Input() message: string = '';
  close!: (result: boolean) => void;

  ngOnInit(): void {
    console.log('Dialog initialized with:', { title: this.title, message: this.message });
  }
  
  onConfirm() {
    this.close(true);
  }

  onCancel() {
    this.close(false);
  }
}

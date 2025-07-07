import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-email-datagrid',
  templateUrl: './email-datagrid.component.html',
  styleUrls: ['./email-datagrid.component.scss']
})
export class EmailDatagridComponent {
  emails: string[] = [];
  newEmail: string = '';
  maxEmails: number = 50;
  emailInputError: boolean = false;
  @Output() emailsChanged = new EventEmitter<string[]>();

  addEmail(): void {
    if (!this.newEmail.trim() || this.emails.length >= this.maxEmails) return;
    if (this.isValidEmail(this.newEmail.trim())) {
      this.emails.push(this.newEmail.trim());
      this.emailsChanged.emit(this.emails);
      this.newEmail = '';
      this.emailInputError = false;
    } else {
      this.emailInputError = true;
    }
  }

  removeEmail(index: number): void {
    this.emails.splice(index, 1);
    this.emailsChanged.emit(this.emails);
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.addEmail();
    }
  }

  isValidEmail(email: string): boolean {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
}

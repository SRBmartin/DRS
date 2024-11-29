import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './basic-button.component.html',
  styleUrls: ['./basic-button.component.scss'],
})
export class BasicButtonComponent {
  @Input() label: string = 'Click Me';
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() class: string = '';
  @Input() disabled: boolean = false;
  @Input() size: 'sm' | 'md' | 'lg' = 'md';

  @Output() clickEvent: EventEmitter<void> = new EventEmitter<void>();

  onClick(): void {
    if (!this.disabled) {
      this.clickEvent.emit();
    }
  }

  getClass(): string {
    let baseClass = 'btn';
    if (this.size === 'sm') baseClass += ' btn-sm';
    if (this.size === 'md') baseClass += ' btn-md';
    if (this.size === 'lg') baseClass += ' btn-lg';
  
    return `${baseClass} ${this.class}`;
  }
  
}

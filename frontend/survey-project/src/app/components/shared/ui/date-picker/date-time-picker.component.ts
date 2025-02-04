import { Component, Input, Output, EventEmitter, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-date-time-picker',
  templateUrl: './date-time-picker.component.html',
  styleUrls: ['./date-time-picker.component.scss'],
  providers: [{
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef(() => DateTimePickerComponent),
    multi: true
  }]
})
export class DateTimePickerComponent implements ControlValueAccessor {
  @Input() label: string = '';
  @Input() type: string = 'datetime-local';
  @Input() placeholder: string = '';
  @Input() required: boolean = false;
  @Input() name: string = '';
  @Input() size: 'sm' | 'lg' | '' = '';
  @Input() class: string = '';
  @Input() hasError: boolean = false;
  @Output() dateChanged = new EventEmitter<Date>();

  value: string = '';
  isDisabled: boolean = false;
  onChange = (_: any) => {};
  onTouched = () => {};

  writeValue(value: any): void {
    if (value instanceof Date) {
      const pad = (n: number) => n < 10 ? '0' + n : n;
      const year = value.getFullYear();
      const month = pad(value.getMonth() + 1);
      const day = pad(value.getDate());
      const hours = pad(value.getHours());
      const minutes = pad(value.getMinutes());
      this.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    } else if (typeof value === 'string') {
      this.value = value;
    } else {
      this.value = '';
    }
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }
  
  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }
  
  setDisabledState(isDisabled: boolean): void {
    this.isDisabled = isDisabled;
  }

  onInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.value = target.value;
    const dateValue = this.value ? new Date(this.value) : null;
    this.onChange(dateValue);
    if (dateValue) {
      this.dateChanged.emit(dateValue);
    }
  }

  onBlurEvent(event: Event): void {
    this.onTouched();
  }
}

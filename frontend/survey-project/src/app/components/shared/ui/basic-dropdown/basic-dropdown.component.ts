import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-basic-dropdown',
  templateUrl: './basic-dropdown.component.html',
  styleUrls: ['./basic-dropdown.component.scss']
})
export class BasicDropdownComponent implements OnInit{
  @Input() items: string[] = [];
  @Output() orderChanged = new EventEmitter<string>();
  selected: string = '';
  dropdownOpen: boolean = false;

  ngOnInit(): void {
    if (this.items.length) {
      this.selected = this.items[0];
      this.orderChanged.emit(this.selected);
    }
  }

  toggleDropdown(): void {
    this.dropdownOpen = !this.dropdownOpen;
  }

  selectItem(item: string): void {
    this.selected = item;
    this.orderChanged.emit(this.selected);
    this.dropdownOpen = false;
  }
}

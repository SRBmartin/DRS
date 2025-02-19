import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-switch-view',
  templateUrl: './switch-view.component.html',
  styleUrls: ['./switch-view.component.scss']
})
export class SwitchViewComponent {
  selectedView: 'grid' | 'row' = 'grid';
  @Output() viewChanged = new EventEmitter<'grid' | 'row'>();

  selectView(view: 'grid' | 'row'): void {
    if (this.selectedView !== view) {
      this.selectedView = view;
      this.viewChanged.emit(this.selectedView);
    }
  }
}
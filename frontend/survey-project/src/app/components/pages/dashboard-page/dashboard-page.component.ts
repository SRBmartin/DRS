import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})
export class DashboardPageComponent {
  selectedMode: 'createdByMe' | 'forMe' = 'createdByMe';
  selectedOrder: string = 'From newest to oldest';
  searchQuery: string = '';
  selectedViewMode: 'grid' | 'row' = 'grid';

  orderDropdownItems: string[] = [
    'From newest to oldest',
    'From oldest to newest',
    'First open then closed',
    'First closed then open'
  ];

  onOrderChanged(order: string): void {
    this.selectedOrder = order; 
  }

  onSwitchMode(mode: 'createdByMe' | 'forMe') {
    this.selectedMode = mode;
  }

  onSearchChanged(query: string): void {
    this.searchQuery = query;
  }
}

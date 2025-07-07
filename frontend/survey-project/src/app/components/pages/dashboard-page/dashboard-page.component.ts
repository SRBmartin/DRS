import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})
export class DashboardPageComponent {
  orderDropdownItems: string[] = [
    'From newest to oldest',
    'From oldest to newest',
    'First open then closed',
    'First closed then open'
  ]
}

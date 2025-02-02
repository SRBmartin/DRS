import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../../shared/consts/routes';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Input() orderDropdownItems: string[] = [];

  constructor(
    private readonly router: Router
  ) {}

  onViewChanged(view: 'grid' | 'row'): void {
    
  }

  onSearchChanged(query: string): void {
    
  }

  onOrderChanged(order: string): void {
    
  }

  onNewSurvey(): void {
    this.router.navigate([RouteNames.CreateSurveyRoute]);
  }
}

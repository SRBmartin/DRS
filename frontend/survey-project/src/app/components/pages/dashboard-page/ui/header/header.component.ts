import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import { RouteNames } from '../../../../../shared/consts/routes';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Input() orderDropdownItems: string[] = [];
  @Output() viewChanged = new EventEmitter<'grid' | 'row'>();
  @Output() searchChanged = new EventEmitter<string>();
  @Output() orderChanged = new EventEmitter<string>();

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
    this.router.navigate([`${RouteNames.SurveyRoute}/${RouteNames.CreateSurveyRoute}`]);
  }
}

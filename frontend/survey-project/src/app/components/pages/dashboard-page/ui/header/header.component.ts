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
  @Output() searchChanged = new EventEmitter<string>();
  @Output() orderChanged = new EventEmitter<string>();

  constructor(
    private readonly router: Router
  ) {}

  onSearchChanged(query: string): void {
    this.searchChanged.emit(query);
  }

  onOrderChanged(order: string): void {
    this.orderChanged.emit(order);
  }

  onNewSurvey(): void {
    this.router.navigate([`${RouteNames.SurveyRoute}/${RouteNames.CreateSurveyRoute}`]);
  }
}

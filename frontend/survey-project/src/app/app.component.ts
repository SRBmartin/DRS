import { Component, OnInit } from '@angular/core';
import { LoaderService } from './shared/services/loader.service';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  isLoading: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(
    private readonly loaderService: LoaderService
  ) {}

  ngOnInit(): void {
    this.trackLoaderChanges();
  }

  trackLoaderChanges(): void {
    this.loaderService.isLoading.subscribe((isLoading) => {
      this.isLoading.next(isLoading);
      document.body.style.overflow = isLoading ? 'hidden' : 'inherit';
    });
  }

}

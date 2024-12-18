import { Injectable } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import {BehaviorSubject, combineLatest, map, Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ScreenObserverService {
  breakPointSmallScreen: string = '(max-width: 599px)'
  breakPointMediumScreen: string = '(min-width: 600px) and (max-width:1300px)'
  breakPointLargeScreen: string = '(min-width: 1301px)'
  private readonly isSmallScreenSubject = new BehaviorSubject<boolean>(false);
  private readonly isMediumScreenSubject = new BehaviorSubject<boolean>(false);
  private readonly isLargeScreenSubject = new BehaviorSubject<boolean>(false);

  public isSmallScreen$: Observable<boolean> =
    this.isSmallScreenSubject.asObservable();
  public isMediumScreen$: Observable<boolean> =
    this.isMediumScreenSubject.asObservable();
  public isLargeScreen$: Observable<boolean> =
    this.isLargeScreenSubject.asObservable();
  public screenSizeChanges$: Observable<[boolean, boolean, boolean]> = combineLatest([
    this.isSmallScreen$,
    this.isMediumScreen$,
    this.isLargeScreen$
  ]);
  public screenChanged$ = this.screenSizeChanges$.pipe(map(() => true))
  constructor(private readonly breakpointObserver: BreakpointObserver) {
    this.breakpointObserver
      .observe(this.breakPointSmallScreen)
      .pipe(map((result) => result.matches))
      .subscribe((result) => {
        this.isSmallScreenSubject.next(result);
      });

    this.breakpointObserver
      .observe([this.breakPointMediumScreen])
      .pipe(map((result) => result.matches))
      .subscribe((result) => {
        this.isMediumScreenSubject.next(result);
      });

    this.breakpointObserver
      .observe([this.breakPointLargeScreen])
      .pipe(map((result) => result.matches))
      .subscribe((result) => {
        this.isLargeScreenSubject.next(result);
      });
  }
  get isSmallScreen(): boolean {
    return this.isSmallScreenSubject.value;
  }
  get isMediumScreen(): boolean {
    return this.isMediumScreenSubject.value;
  }

  get isLargeScreen(): boolean {
    return this.isLargeScreenSubject.value;
  }
}

import { Injectable } from '@angular/core';
import {
  MatDialog,
  MatDialogConfig,
  MatDialogRef,
} from '@angular/material/dialog';
import { WidthHeightModal } from '../model/common/width-height.model';
import { ScreenObserverService } from './screen-observer.service';

const DEFAULT_WIDTH = '60dvw';
const DEFAULT_HEIGHT = '60dvh';

@Injectable({
  providedIn: 'root',
})
export class ModalOpenerService {

  constructor(
    private readonly dialog: MatDialog,
    private readonly screenObserver: ScreenObserverService,
  ) {}

  open<T>(
    component: new (...args: any[]) => T,
    width: string,
    height: string,
    data?: any,
    additionalConfig?: MatDialogConfig,
  ): MatDialogRef<T> {
    return this.dialog.open(component, {
      width: width,
      height: height,
      data: data,
      ...additionalConfig,
    });
  }

  openResponsive<T>(
    component: new (...args: any[]) => T,
    large: WidthHeightModal,
    medium: WidthHeightModal,
    small: WidthHeightModal,
    data?: any,
    additionalConfig?: MatDialogConfig,
  ): MatDialogRef<T> {
    const config: MatDialogConfig = {
      width: DEFAULT_WIDTH,
      height: DEFAULT_HEIGHT,
      data: data,
      autoFocus: false,
      ...additionalConfig,
    };
    if (this.screenObserver.isLargeScreen) {
      config.width = large.width;
      config.height = large.height;
      return this.dialog.open(component, config);
    }
    if (this.screenObserver.isMediumScreen) {
      config.width = medium.width;
      config.height = medium.height;
      return this.dialog.open(component, config);
    }
    if (this.screenObserver.isSmallScreen) {
      config.width = small.width;
      config.height = small.height;
      return this.dialog.open(component, config);
    }
    return this.dialog.open(component, config);
  }
}

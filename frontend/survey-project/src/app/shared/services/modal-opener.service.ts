import { Injectable, ComponentFactoryResolver, ApplicationRef, Injector } from '@angular/core';
import { ComponentRef, Type } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ModalOpenerService {
  private modalRef!: ComponentRef<any>;

  constructor(
    private resolver: ComponentFactoryResolver,
    private appRef: ApplicationRef,
    private injector: Injector
  ) {}

  openModal<T>(component: Type<T>, data?: any): Promise<any> {
    return new Promise((resolve) => {
      try {

        const factory = this.resolver.resolveComponentFactory(component);
        this.modalRef = factory.create(this.injector);

        // Пренос прослеђених података у компоненту
        if (data) {
          Object.assign(this.modalRef.instance, data);
        }

        this.modalRef.instance['close'] = (result: any) => {
          this.closeModal();
          resolve(result);
        };

        this.appRef.attachView(this.modalRef.hostView);
        const domElem = (this.modalRef.hostView as any).rootNodes[0] as HTMLElement;
        document.body.appendChild(domElem);

      } catch (error) {
        console.error('Error while opening modal:', error);
        resolve(null); 
      }
    });
  }

  closeModal() {
    try {
      if (this.modalRef) {
        this.appRef.detachView(this.modalRef.hostView);
        this.modalRef.destroy();
      }
    } catch (error) {
      console.error('Error while closing modal:', error);
    }
  }
}

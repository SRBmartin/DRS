import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { UserService } from '../../../../../shared/services/user.service';
import { CookieService } from 'ngx-cookie-service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-general-informations',
  templateUrl: './general-informations.component.html',
  styleUrl: './general-informations.component.scss'
})
export class GeneralInformationsComponent implements OnInit {
  userInfo: any = null;
  generalInfoForm!: FormGroup;

  constructor(
    private readonly userService: UserService,
    private readonly cookieService: CookieService,
    private readonly toastService: ToastService,
    private readonly fb: FormBuilder,
    private readonly cdr: ChangeDetectorRef
  ) {
    this.generalInfoForm = this.fb.group({
      name: [''],
      lastname: [''],
      address: [''],
      city: [''],
      country: [''],
      phone_number: [''],
      email: ['']
    });
  }

  ngOnInit(): void {
    this.fetchUserInfo();
  }

  private fetchUserInfo(): void {
    const ssid = this.cookieService.get('ssid');
    if (!ssid) {
      this.toastService.showError('You are not logged in.', 'Error');
      return;
    }

    this.userService.getGeneralInfo(ssid).subscribe({
      next: (response) => {
        this.userInfo = response.data;
        this.initializeForm();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.toastService.showError(err.message || 'Failed to fetch user information.', 'Error');
      }
    });
  }

  private initializeForm(): void {
    if (this.userInfo) {
      this.generalInfoForm = this.fb.group({
        name: [this.userInfo.name || ''],
        lastname: [this.userInfo.lastname || ''],
        address: [this.userInfo.address || ''],
        city: [this.userInfo.city || ''],
        country: [this.userInfo.country || ''],
        phone_number: [this.userInfo.phone_number || ''],
        email: [this.userInfo.email || '']
      });
    }
  }

  onSave(): void {
    const ssid = this.cookieService.get('ssid');
    if (!ssid) {
      this.toastService.showError('You are not logged in.', 'Error');
      return;
    }

    if (this.generalInfoForm.invalid) {
      this.toastService.showError('Please fill in all fields correctly.', 'Error');
      return;
    }

    const updatedData = this.generalInfoForm.value;
    this.userService.updateGeneralInfo(updatedData, ssid).subscribe({
      next: (response) => {
        this.toastService.showSuccess('Your information has been updated successfully.', 'Success');
        this.fetchUserInfo();
      },
      error: (err) => {
        this.toastService.showError(err.message || 'Failed to update user information.', 'Error');
      }
    });
}

}

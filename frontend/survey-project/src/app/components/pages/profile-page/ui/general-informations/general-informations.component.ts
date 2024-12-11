import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { UserService } from '../../../../../shared/services/user.service';
import { CookieService } from 'ngx-cookie-service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { GeneralInfoResponse } from '../../../../../shared/dto/responses/user/general-info-response';
import { ChangeGeneralInformationRequest } from '../../../../../shared/dto/requests/user/change-general-info-request';
import { ChangeGeneralInformationResponse } from '../../../../../shared/dto/responses/user/change-general-info-response';

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
      next: (response: GeneralInfoResponse) => {
        if (response.data) {
          this.userInfo = response.data;
          this.initializeForm();
          this.cdr.detectChanges();
        } else {
          this.toastService.showError(response.message || 'Failed to fetch user information.', 'Error');
        }
      },
      error: (err) => {
        this.toastService.showError(err.message || 'An unexpected error occurred.', 'Error');
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

  private createChangeGeneralInfoRequest(): ChangeGeneralInformationRequest {
    return {
      name: this.generalInfoForm.value.name,
      lastname: this.generalInfoForm.value.lastname,
      email: this.generalInfoForm.value.email,
      phone_number: this.generalInfoForm.value.phone_number,
      address: this.generalInfoForm.value.address,
      city: this.generalInfoForm.value.city,
      country: this.generalInfoForm.value.country
    };
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

    const updatedData = this.createChangeGeneralInfoRequest();

    this.userService.updateGeneralInfo(updatedData, ssid).subscribe({
      next: (response: ChangeGeneralInformationResponse) => {
        if (response.status) {
          this.toastService.showSuccess('Your information has been updated successfully.', 'Success');
          this.fetchUserInfo();
        } else {
          this.toastService.showError(response.message || 'Failed to update user information.', 'Error');
        }
      },
      error: (err) => {
        this.toastService.showError(err.message || 'An unexpected error occurred.', 'Error');
      }
    });
  }
}

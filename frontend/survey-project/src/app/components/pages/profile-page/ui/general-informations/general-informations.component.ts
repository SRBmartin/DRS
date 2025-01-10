import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { UserService } from '../../../../../shared/services/user.service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { GeneralInfoResponse } from '../../../../../shared/dto/responses/user/general-info-response';
import { ChangeGeneralInformationRequest } from '../../../../../shared/dto/requests/user/change-general-info-request';
import { ChangeGeneralInformationResponse } from '../../../../../shared/dto/responses/user/change-general-info-response';
import { CommonDialogsService } from '../../../../../shared/services/commondialog.service';

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
    private readonly toastService: ToastService,
    private readonly fb: FormBuilder,
    private readonly cdr: ChangeDetectorRef,
    private readonly commonDialogs: CommonDialogsService
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
    this.userService
        .getGeneralInfo()
        .subscribe({
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
        name: [this.userInfo.name || '', Validators.required],
        lastname: [this.userInfo.lastname || '', Validators.required],
        address: [this.userInfo.address || '', Validators.required],
        city: [this.userInfo.city || '', Validators.required],
        country: [this.userInfo.country || '', Validators.required],
        phone_number: [this.userInfo.phone_number || '', Validators.required],
        email: [this.userInfo.email || '', Validators.required]
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
    if (!this.generalInfoForm.invalid) {
      this.commonDialogs
        .openConfirmationDialog('Save changes',
          'Are you sure you want to save changes?'
        )
        .afterClosed()
        .subscribe((confirmed: boolean) => {
          if (!this.generalInfoForm.invalid) { }
          if (confirmed) {


            const updatedData = this.createChangeGeneralInfoRequest();

            this.userService
              .updateGeneralInfo(updatedData)
              .subscribe({
                next: (response: ChangeGeneralInformationResponse) => {
                  if (response.status == "204") {
                    this.toastService.showWarning(response.message || 'No changes detected.', 'Warning');
                  } else if (response.status == "200") {
                    this.toastService.showSuccess(response.message || 'Your information has been updated successfully.', 'Success');
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
        })
    } 
  }
}

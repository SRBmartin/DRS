import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../../../../shared/services/user.service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { CookieService } from 'ngx-cookie-service';
import { ChangePasswordResponse } from '../../../../../shared/dto/responses/user/change-password-response';
import { ChangePasswordRequest } from '../../../../../shared/dto/requests/user/change-password-request';
import { LoaderService } from '../../../../../shared/services/loader.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrl: './change-password.component.scss'
})
export class ChangePasswordComponent implements OnInit{
  changePasswordForm!: FormGroup;

  constructor(
    private readonly fb: FormBuilder,
    private readonly userService: UserService,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
  }

  private initializeForm(): void {
    this.changePasswordForm = this.fb.group(
      {
        oldPassword: ['', [Validators.required]],
        newPassword: [
          '',
          [
            Validators.required,
            Validators.minLength(6)
          ],
        ],
        confirmPassword: ['', [Validators.required]],
      },
      {
        validators: this.passwordsMatchValidator,
      }
    );
  }

  private passwordsMatchValidator(form: FormGroup) {
    const newPassword = form.get('newPassword')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return newPassword === confirmPassword
      ? null
      : { mismatch: true };
  }

  private createChangePasswordRequest(): ChangePasswordRequest{
    return {
      old_password: this.changePasswordForm.value.oldPassword,
      new_password: this.changePasswordForm.value.newPassword,
    };
  }

  onChangePassword(): void {
    if (this.changePasswordForm.valid) {
      const request = this.createChangePasswordRequest();
      this.loaderService.startLoading();
      this.userService
          .changePassword(request)
          .subscribe({
            next: (response: ChangePasswordResponse) => {
              this.toastService.showSuccess(response.message || 'Password changed successfully!', 'Success');
              this.changePasswordForm.reset();
              this.loaderService.stopLoading();
            },
            error: (err: any) => {
              this.toastService.showError(err.message || 'Failed to change password.', 'Error');
              this.loaderService.stopLoading();
            },
          });
    } else {
      this.changePasswordForm.markAllAsTouched();
    }
  }
}

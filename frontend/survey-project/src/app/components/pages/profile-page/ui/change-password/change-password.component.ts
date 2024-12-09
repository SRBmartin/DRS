import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../../../../shared/services/user.service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { CookieService } from 'ngx-cookie-service';

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
    private readonly cookieService: CookieService
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
            Validators.minLength(6),
            this.newPasswordNotSameAsOldPasswordValidator.bind(this),
          ],
        ],
        confirmPassword: ['', [Validators.required]],
      },
      {
        validators: this.passwordsMatchValidator,
      }
    );
  }

  // private passwordsMatchValidator(form: FormGroup) {
  //   const newPassword = form.get('newPassword')?.value;
  //   const confirmPassword = form.get('confirmPassword')?.value;
  //   return newPassword === confirmPassword ? null : { mismatch: true };
  // }

  private passwordsMatchValidator(form: FormGroup) {
    const newPassword = form.get('newPassword')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return newPassword === confirmPassword
      ? null
      : { mismatch: true };
  }

  private newPasswordNotSameAsOldPasswordValidator(control: any) {
    const oldPassword = this.changePasswordForm?.get('oldPassword')?.value;
    const newPassword = control.value;

    return newPassword === oldPassword
      ? { sameAsOldPassword: true }
      : null;
  }

  onChangePassword(): void {
    if (this.changePasswordForm.valid) {
      const { oldPassword, newPassword } = this.changePasswordForm.value;
      const ssid = this.cookieService.get('ssid');
      if (!ssid) {
        throw new Error('SSID not found in cookies. User might not be logged in.');
      }
      this.userService.changePassword({ oldPassword, newPassword }, ssid).subscribe({
        next: () => {
          this.toastService.showSuccess('Password changed successfully!', 'Success');
          this.changePasswordForm.reset();
        },
        error: (err: any) => {
          this.toastService.showError(err.message || 'Failed to change password.', 'Error');
        }
      });
    } else {
      this.changePasswordForm.markAllAsTouched();
    }
  }
}

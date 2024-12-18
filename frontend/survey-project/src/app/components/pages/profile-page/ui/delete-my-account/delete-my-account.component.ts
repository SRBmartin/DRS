import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../../../shared/services/auth.service';
import { ToastService } from '../../../../../shared/services/toast.service';
import { LoaderService } from '../../../../../shared/services/loader.service';
import { CookieService } from 'ngx-cookie-service';
import { DeleteResponse } from '../../../../../shared/dto/responses/user/delete-response';


@Component({
  selector: 'app-delete-my-account',
  templateUrl: './delete-my-account.component.html',
  styleUrls: ['./delete-my-account.component.scss']
})
export class DeleteMyAccountComponent implements OnInit {
  deleteForm!: FormGroup;

  constructor(
    private readonly fb: FormBuilder,
    private readonly authService: AuthService,
    private readonly toastService: ToastService,
    private readonly loaderService: LoaderService,
    private readonly cookieService: CookieService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
  }

  private initializeForm(): void {
    this.deleteForm = this.fb.group({
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onDeleteAccount(): void {
    if (this.deleteForm.valid) {
      const password = this.deleteForm.get('password')?.value;
      const ssid = this.cookieService.get('ssid');  

      this.loaderService.startLoading();

      this.authService.deleteUserAccount(password).subscribe({
        next: (response : DeleteResponse) => {
          this.toastService.showSuccess("Your account has been deleted successfully.", 'Account Deleted');
          this.authService.goToRegister()
          this.loaderService.stopLoading();
        }, 
        error: (e) => {
          this.toastService.showError(e.message ?? '', 'Delete Account Error');
          this.loaderService.stopLoading();
        }
      });
    } else {
      this.deleteForm.markAllAsTouched();
    }
  }
}

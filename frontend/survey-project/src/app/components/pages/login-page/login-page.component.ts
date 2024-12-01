import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginRequest } from '../../../shared/dto/requests/user/login-request';
import { UserService } from '../../../shared/services/user.service';
import { LoginResponse } from '../../../shared/dto/responses/user/login-response';
import { AuthService } from '../../../shared/services/auth.service';
import { ToastService } from '../../../shared/services/toast.service';
import { Router } from '@angular/router';
import { RouteNames } from '../../../shared/consts/routes';
import { LoaderService } from '../../../shared/services/loader.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class LoginPageComponent implements OnInit {
  loginForm!: FormGroup;
  homeRoute: string = RouteNames.HomeRoute;

  constructor(
    private readonly fb: FormBuilder,
    private readonly userService: UserService,
    private readonly authService: AuthService,
    private readonly toastService: ToastService,
    private readonly router: Router,
    private readonly loaderService: LoaderService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
  }

  private initializeForm(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  createLoginRequest(): LoginRequest {
    const request: LoginRequest = {
      email: this.loginForm.get('email')?.value,
      password: this.loginForm.get('password')?.value,
    };
    return request;
  }

  onLogin(): void {
    if (this.loginForm.valid) {
      const request = this.createLoginRequest();
      this.loaderService.startLoading();
      this.userService.loginUser(request).subscribe({
        next: (response: LoginResponse) => {
          if (response.session) {
            this.authService.loginUser(response.session);
            this.router.navigate([RouteNames.HomeRoute]);
            setTimeout(() => {
              this.toastService.showSuccess("You've successfully logged in.", 'Login success');
            }, 500);
          } else {
            this.toastService.showError(response.message ?? '', 'Login error');
            this.loginForm.get('password')?.setValue('');
            this.loginForm.get('password')?.markAsUntouched();
          }
          this.loaderService.stopLoading();
        },
        error: (e: any) => {
          this.toastService.showError(e.message ?? '', 'Login error');
          this.loginForm.get('password')?.setValue('');
          this.loginForm.get('password')?.markAsUntouched();
          this.loaderService.stopLoading();
        },
      });
    } else {
      this.loginForm.markAllAsTouched();
    }
  }

  onSignUpClick(): void {
    this.router.navigate([RouteNames.RegisterRoute]);
  }
}

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RegisterRequest } from '../../../shared/dto/requests/user/register-request';
import { UserService } from '../../../shared/services/user.service';
import { RegisterResponse } from '../../../shared/dto/responses/user/register-response';
import { AuthService } from '../../../shared/services/auth.service';
import { ToastService } from '../../../shared/services/toast.service';
import { Router } from '@angular/router';
import { RouteNames } from '../../../shared/consts/routes';
import { LoaderService } from '../../../shared/services/loader.service';

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.scss'],
})
export class RegisterPageComponent implements OnInit {
  registerForm!: FormGroup;

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
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      name: ['', [Validators.required, Validators.maxLength(100)]],
      lastname: ['', [Validators.required, Validators.maxLength(100)]],
      phoneNumber: ['', [Validators.required, Validators.pattern(/^\+?[0-9]{6,15}$/),]],
      address: ['', [Validators.required, Validators.maxLength(100)]],
      city: ['', [Validators.required, Validators.maxLength(100)]],
      country: ['', [Validators.required, Validators.maxLength(100)]],
    });
  }

  createRegisterRequest(): RegisterRequest {
    const request: RegisterRequest = {
      name: this.registerForm.get('name')?.value,
      lastname: this.registerForm.get('lastname')?.value,
      address: this.registerForm.get('address')?.value,
      city: this.registerForm.get('city')?.value,
      country: this.registerForm.get('country')?.value,
      phone_number: this.registerForm.get('phoneNumber')?.value,
      email: this.registerForm.get('email')?.value,
      password: this.registerForm.get('password')?.value
    };
    return request;
  }

  onRegister(): void {
    if (this.registerForm.valid) {
      const request = this.createRegisterRequest();
      this.loaderService.startLoading();
      this.userService
          .registerUser(request)
          .subscribe({
            next: (response: RegisterResponse) => {
              if(response.session){
                this.authService.loginUser(response.session);
                this.router.navigate([RouteNames.DashboardRoute]);
                setTimeout(() => {
                  this.toastService.showSuccess("You've successfuly created an account.", "Registration success");
                }, 500)
              }else{
                this.toastService.showError(response.message ?? '', "Registration error");
              }
              this.loaderService.stopLoading();
            },
            error: (e: any) => {
              this.toastService.showError(e.message ?? '', "Registration error");
              this.loaderService.stopLoading();
            }
          });
    }
  }

  onSignInClick(): void {
    this.router.navigate([RouteNames.LoginRoute]);
  }

}

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface LoginData {
  email: string;
  password: string;
}

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class LoginComponent {
  loginData: LoginData = {
    email: '',
    password: ''
  };

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }

  navigateToRegistro() {
    this.router.navigate(['/registro']);
  }

  onLogin() {
    if (this.loginData.email && this.loginData.password) {
      // TODO: Implementar lógica de autenticación
      console.log('Iniciando sesión:', this.loginData);
      // Simular login exitoso y redirigir al menú principal
      this.router.navigate(['/']);
    }
  }
}
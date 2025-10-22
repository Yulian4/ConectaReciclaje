import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface LoginData {
  email: string;
  password: string;
  userType: 'ciudadano' | 'reciclador' | 'admin';
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
    password: '',
    userType: 'ciudadano'
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
      
      // Redirigir según el tipo de usuario
      switch (this.loginData.userType) {
        case 'ciudadano':
          this.router.navigate(['/perfil']);
          break;
        case 'reciclador':
          this.router.navigate(['/gestion-reportes']);
          break;
        case 'admin':
          this.router.navigate(['/administracion']);
          break;
        default:
          this.router.navigate(['/']);
      }
    }
  }

  selectUserType(type: 'ciudadano' | 'reciclador' | 'admin') {
    this.loginData.userType = type;
  }
}
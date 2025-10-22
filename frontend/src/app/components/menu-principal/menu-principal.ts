import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-menu-principal',
  imports: [FormsModule],
  templateUrl: './menu-principal.html',
  styleUrl: './menu-principal.scss'
})
export class MenuPrincipalComponent {
  comando: string = '';
  isDarkMode: boolean = false;

  constructor(private router: Router) {}

  navigateAsCiudadano() {
    this.router.navigate(['/reporte-ciudadano']);
  }

  navigateAsReciclador() {
    this.router.navigate(['/gestion-reportes']);
  }

  navigateAsAdmin() {
    this.router.navigate(['/login']);
  }

  navigateToReportar() {
    this.router.navigate(['/reporte-ciudadano']);
  }

  navigateToReportes() {
    this.router.navigate(['/gestion-reportes']);
  }

  navigateToPanel() {
    this.router.navigate(['/administracion']);
  }

  navigateToEstadisticas() {
    // TODO: Implementar vista de estadísticas
  }

  navigateToLogin() {
    this.router.navigate(['/login']);
  }

  navigateToSignup() {
    this.router.navigate(['/registro']);
  }

  navigateToPerfil() {
    this.router.navigate(['/perfil']);
  }

  procesarComando() {
    if (this.comando.trim()) {
      // TODO: Implementar procesamiento de comandos
      console.log('Comando procesado:', this.comando);
      this.comando = '';
    }
  }

  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    const body = document.body;
    if (this.isDarkMode) {
      body.setAttribute('data-bs-theme', 'dark');
    } else {
      body.removeAttribute('data-bs-theme');
    }
  }
}

import { Component } from '@angular/core';
import { Router } from '@angular/router';

interface UserStats {
  totalReportes: number;
  co2Evitado: number;
  materialMasFrecuente: string;
  reportesActivos: number;
}

@Component({
  selector: 'app-perfil-usuario',
  imports: [],
  templateUrl: './perfil-usuario.html',
  styleUrl: './perfil-usuario.scss'
})
export class PerfilUsuarioComponent {
  userInfo = {
    nombre: 'Ana Rodriguez',
    email: 'ana.rodriguez@email.com',
    telefono: '+52 55 1234 5678',
    direccion: 'Av. Libertador 1234, Buenos Aires',
    tipoUsuario: 'ciudadano' as 'ciudadano' | 'reciclador' | 'admin'
  };

  userStats: UserStats = {
    totalReportes: 12,
    co2Evitado: 45.6,
    materialMasFrecuente: 'Plástico',
    reportesActivos: 3
  };

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }

  navigateToEditar() {
    this.router.navigate(['/editar-perfil']);
  }

  navigateToMisReportes() {
    this.router.navigate(['/seguimiento']);
  }

  navigateToNuevoReporte() {
    this.router.navigate(['/reporte-ciudadano']);
  }

  navigateToGestionReportes() {
    this.router.navigate(['/gestion-reportes']);
  }
}

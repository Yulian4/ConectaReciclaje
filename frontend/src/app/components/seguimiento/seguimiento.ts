import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface ReporteStatus {
  id: string;
  estado: 'pendiente' | 'asignado' | 'en_camino' | 'recolectado';
  fechaCreacion: string;
  reciclador?: string;
  fechaAsignacion?: string;
  fechaRecoleccion?: string;
  pesoEstimado: number;
  co2Evitado: number;
  tipoMaterial: string;
}

@Component({
  selector: 'app-seguimiento',
  imports: [CommonModule],
  templateUrl: './seguimiento.html',
  styleUrl: './seguimiento.scss'
})
export class SeguimientoComponent {
  reporte: ReporteStatus = {
    id: 'AB-123',
    estado: 'recolectado',
    fechaCreacion: 'Junio 1, 10:00 AM',
    reciclador: 'Juan Pérez',
    fechaAsignacion: 'Junio 1, 11:30 AM',
    fechaRecoleccion: 'Junio 2, 9:00 AM',
    pesoEstimado: 8,
    co2Evitado: 5.2,
    tipoMaterial: 'Plástico'
  };

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }

  cerrar() {
    this.router.navigate(['/']);
  }

  navigateToNuevoReporte() {
    this.router.navigate(['/reporte-ciudadano']);
  }

  getProgressPercentage(): number {
    switch (this.reporte.estado) {
      case 'pendiente': return 25;
      case 'asignado': return 50;
      case 'en_camino': return 75;
      case 'recolectado': return 100;
      default: return 0;
    }
  }

  getUrbanIAMessage(): string {
    switch (this.reporte.estado) {
      case 'pendiente':
        return '¡Hola! Tu reporte está siendo procesado. Pronto asignaremos un reciclador 🌱';
      case 'asignado':
        return `¡Genial! ${this.reporte.reciclador} ha aceptado tu reporte. Pronto estará en camino 🚴‍♂️`;
      case 'en_camino':
        return `${this.reporte.reciclador} está en camino hacia tu ubicación. ¡Prepara el material! 📦`;
      case 'recolectado':
        return `¡Excelente! Tu material fue recolectado. Has ayudado a evitar ${this.reporte.co2Evitado} kg de CO₂ 🌍`;
      default:
        return '¡Hola! Estoy aquí para ayudarte con el seguimiento de tu reporte 🤖';
    }
  }

  getStatusText(): string {
    switch (this.reporte.estado) {
      case 'pendiente': return 'PENDIENTE DE ASIGNACIÓN';
      case 'asignado': return 'RECICLADOR ASIGNADO';
      case 'en_camino': return 'EN CAMINO HACIA TU UBICACIÓN';
      case 'recolectado': return '¡RECOLECCIÓN COMPLETADA!';
      default: return 'ESTADO DESCONOCIDO';
    }
  }
}

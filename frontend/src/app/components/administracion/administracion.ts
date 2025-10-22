import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface DashboardMetrics {
  totalRecolectado: number;
  reportesCompletados: number;
  usuariosActivos: number;
  co2Evitado: number;
  recicladores: number;
  zonaTop: string;
}

interface ReporteAdmin {
  id: string;
  tipo: string;
  estado: 'pendiente' | 'asignado' | 'completado';
  ciudadano: string;
  reciclador?: string;
  fecha: string;
  peso: number;
  zona: string;
}

@Component({
  selector: 'app-administracion',
  imports: [CommonModule],
  templateUrl: './administracion.html',
  styleUrl: './administracion.scss'
})
export class AdministracionComponent {
  viewMode: 'mapa' | 'lista' = 'mapa';
  
  metrics: DashboardMetrics = {
    totalRecolectado: 1234,
    reportesCompletados: 567,
    usuariosActivos: 89,
    co2Evitado: 892.5,
    recicladores: 23,
    zonaTop: 'Centro'
  };

  reportes: ReporteAdmin[] = [
    {
      id: 'R001',
      tipo: 'Plástico',
      estado: 'completado',
      ciudadano: 'Ana García',
      reciclador: 'Juan Pérez',
      fecha: '2024-01-15',
      peso: 8.5,
      zona: 'Centro'
    },
    {
      id: 'R002',
      tipo: 'Cartón',
      estado: 'asignado',
      ciudadano: 'Carlos López',
      reciclador: 'María Rodríguez',
      fecha: '2024-01-15',
      peso: 12.0,
      zona: 'Norte'
    },
    {
      id: 'R003',
      tipo: 'Vidrio',
      estado: 'pendiente',
      ciudadano: 'Luis Martín',
      fecha: '2024-01-15',
      peso: 6.2,
      zona: 'Sur'
    }
  ];

  materialStats = [
    { tipo: 'Plástico', cantidad: 456, porcentaje: 37 },
    { tipo: 'Cartón', cantidad: 389, porcentaje: 31 },
    { tipo: 'Vidrio', cantidad: 234, porcentaje: 19 },
    { tipo: 'Metal', cantidad: 155, porcentaje: 13 }
  ];

  constructor(private router: Router) {}

  toggleView(mode: 'mapa' | 'lista') {
    this.viewMode = mode;
  }

  navigateBack() {
    this.router.navigate(['/']);
  }

  exportData() {
    // TODO: Implementar exportación de datos
    console.log('Exportando datos...');
  }

  getEstadoClass(estado: string): string {
    switch (estado) {
      case 'completado': return 'text-success';
      case 'asignado': return 'text-primary';
      case 'pendiente': return 'text-warning';
      default: return 'text-muted';
    }
  }

  getEstadoText(estado: string): string {
    switch (estado) {
      case 'completado': return 'Completado';
      case 'asignado': return 'Asignado';
      case 'pendiente': return 'Pendiente';
      default: return 'Desconocido';
    }
  }
}

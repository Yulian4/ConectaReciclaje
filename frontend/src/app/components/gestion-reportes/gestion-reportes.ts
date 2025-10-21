import { Component } from '@angular/core';

interface Reporte {
  tipo: string;
  icono: string;
  color: string;
  titulo: string;
  direccion: string;
  distancia: string;
  peso: string;
}

@Component({
  selector: 'app-gestion-reportes',
  imports: [],
  templateUrl: './gestion-reportes.html',
  styleUrl: './gestion-reportes.scss'
})
export class GestionReportesComponent {
  reportes: Reporte[] = [
    {
      tipo: 'plastico',
      icono: 'inventory_2',
      color: 'blue',
      titulo: 'Plástico y Cartón',
      direccion: 'Av. Siempreviva 742, a 2 cuadras',
      distancia: '1.2 km',
      peso: 'Aprox. 15 kg'
    },
    {
      tipo: 'vidrio',
      icono: 'liquor',
      color: 'green',
      titulo: 'Vidrio',
      direccion: 'Calle Falsa 123, cerca del parque',
      distancia: '2.5 km',
      peso: 'Aprox. 8 kg'
    },
    {
      tipo: 'papel',
      icono: 'article',
      color: 'yellow',
      titulo: 'Papel',
      direccion: 'Blvd. de los Sueños Rotos 45',
      distancia: '3.1 km',
      peso: 'Aprox. 22 kg'
    }
  ];

  filtroSeleccionado: string = 'todo';

  seleccionarFiltro(filtro: string) {
    this.filtroSeleccionado = filtro;
  }

  aceptarRuta() {
    // TODO: Implementar lógica de aceptación de ruta
    console.log('Ruta aceptada');
  }
}

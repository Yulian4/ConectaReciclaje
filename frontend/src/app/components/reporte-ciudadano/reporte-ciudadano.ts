import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Reporte {
  tipo: string;
  direccion: string;
  contacto: string;
}

@Component({
  selector: 'app-reporte-ciudadano',
  imports: [FormsModule],
  templateUrl: './reporte-ciudadano.html',
  styleUrl: './reporte-ciudadano.scss'
})
export class ReporteCiudadanoComponent {
  reporte: Reporte = {
    tipo: '',
    direccion: '',
    contacto: ''
  };

  showSuccessModal: boolean = false;

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }

  seleccionarTipo(tipo: string) {
    this.reporte.tipo = tipo;
  }

  seleccionarContacto(contacto: string) {
    this.reporte.contacto = contacto;
  }

  enviarReporte() {
    if (this.reporte.tipo && this.reporte.direccion && this.reporte.contacto) {
      // TODO: Implementar envío del reporte
      console.log('Enviando reporte:', this.reporte);
      this.showSuccessModal = true;
      setTimeout(() => {
        this.showSuccessModal = false;
        this.router.navigate(['/seguimiento']);
      }, 2000);
    }
  }
}

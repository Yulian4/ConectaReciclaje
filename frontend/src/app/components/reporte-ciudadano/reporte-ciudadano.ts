import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface Reporte {
  tipo: string;
  direccion: string;
  contacto: string;
  pesoAproximado: string;
  descripcion: string;
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
    contacto: '',
    pesoAproximado: '',
    descripcion: ''
  };

  pesoOpciones = [
    { valor: 'menos-5', texto: 'Menos de 5 kg' },
    { valor: '5-15', texto: '5 - 15 kg' },
    { valor: '15-30', texto: '15 - 30 kg' },
    { valor: 'mas-30', texto: 'Más de 30 kg' }
  ];

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

  seleccionarPeso(peso: string) {
    this.reporte.pesoAproximado = peso;
  }

  enviarReporte() {
    if (this.reporte.tipo && this.reporte.direccion && this.reporte.contacto && this.reporte.pesoAproximado) {
      // TODO: Implementar envío del reporte
      console.log('Enviando reporte:', this.reporte);
      this.showSuccessModal = true;
      setTimeout(() => {
        this.showSuccessModal = false;
        this.router.navigate(['/seguimiento']);
      }, 2000);
    } else {
      alert('Por favor completa todos los campos obligatorios');
    }
  }

  isFormValid(): boolean {
    return !!(this.reporte.tipo && this.reporte.direccion && this.reporte.contacto && this.reporte.pesoAproximado);
  }
}

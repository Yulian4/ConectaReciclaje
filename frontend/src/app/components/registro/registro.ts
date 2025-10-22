import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface RegistroData {
  nombre: string;
  email: string;
  password: string;
  confirmPassword: string;
  telefono: string;
  tipoUsuario: 'ciudadano' | 'reciclador';
  aceptaTerminos: boolean;
}

@Component({
  selector: 'app-registro',
  imports: [FormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.scss'
})
export class RegistroComponent {
  registroData: RegistroData = {
    nombre: '',
    email: '',
    password: '',
    confirmPassword: '',
    telefono: '',
    tipoUsuario: 'ciudadano',
    aceptaTerminos: false
  };

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/login']);
  }

  seleccionarTipoUsuario(tipo: 'ciudadano' | 'reciclador') {
    this.registroData.tipoUsuario = tipo;
  }

  onRegistro() {
    if (this.registroData.nombre && this.registroData.email &&
        this.registroData.password && this.registroData.confirmPassword &&
        this.registroData.password === this.registroData.confirmPassword &&
        this.registroData.aceptaTerminos) {
      // TODO: Implementar lógica de registro
      console.log('Registrando usuario:', this.registroData);
      // Simular registro exitoso y redirigir al login
      this.router.navigate(['/login']);
    }
  }
}
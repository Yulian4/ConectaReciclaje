import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

interface User {
  nombre: string;
  direccion: string;
  telefono: string;
  notificacionesPush: boolean;
  alertasSMS: boolean;
  recordatoriosCorreo: boolean;
}

@Component({
  selector: 'app-editar-usuario',
  imports: [FormsModule],
  templateUrl: './editar-usuario.html',
  styleUrl: './editar-usuario.scss'
})
export class EditarUsuarioComponent {
  user: User = {
    nombre: 'Juan Pérez',
    direccion: 'Calle Falsa 123, Springfield',
    telefono: '+52 55 8765 4321',
    notificacionesPush: true,
    alertasSMS: false,
    recordatoriosCorreo: true
  };

  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/perfil']);
  }

  guardarCambios() {
    // TODO: Implementar guardado de cambios
    console.log('Guardando cambios:', this.user);
    this.router.navigate(['/perfil']);
  }

  cancelar() {
    this.router.navigate(['/perfil']);
  }
}

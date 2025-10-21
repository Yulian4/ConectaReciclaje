import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-perfil-usuario',
  imports: [],
  templateUrl: './perfil-usuario.html',
  styleUrl: './perfil-usuario.scss'
})
export class PerfilUsuarioComponent {
  constructor(private router: Router) {}

  navigateToEditar() {
    this.router.navigate(['/editar-perfil']);
  }
}

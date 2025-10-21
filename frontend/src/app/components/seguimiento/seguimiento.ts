import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-seguimiento',
  imports: [],
  templateUrl: './seguimiento.html',
  styleUrl: './seguimiento.scss'
})
export class SeguimientoComponent {
  constructor(private router: Router) {}

  navigateBack() {
    this.router.navigate(['/']);
  }

  cerrar() {
    this.router.navigate(['/']);
  }
}

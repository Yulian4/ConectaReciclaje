import { Component } from '@angular/core';

@Component({
  selector: 'app-administracion',
  imports: [],
  templateUrl: './administracion.html',
  styleUrl: './administracion.scss'
})
export class AdministracionComponent {
  viewMode: 'mapa' | 'lista' = 'mapa';

  toggleView(mode: 'mapa' | 'lista') {
    this.viewMode = mode;
  }
}

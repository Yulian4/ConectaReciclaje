import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UrbaniaComponent } from './components/urbania/urbania';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UrbaniaComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('recicla-ya-frontend');
}

import { Routes } from '@angular/router';
import { MenuPrincipalComponent } from './components/menu-principal/menu-principal';
import { LoginComponent } from './components/login/login';
import { RegistroComponent } from './components/registro/registro';
import { PerfilUsuarioComponent } from './components/perfil-usuario/perfil-usuario';
import { EditarUsuarioComponent } from './components/editar-usuario/editar-usuario';
import { AdministracionComponent } from './components/administracion/administracion';
import { GestionReportesComponent } from './components/gestion-reportes/gestion-reportes';
import { ReporteCiudadanoComponent } from './components/reporte-ciudadano/reporte-ciudadano';
import { SeguimientoComponent } from './components/seguimiento/seguimiento';

export const routes: Routes = [
  { path: '', component: MenuPrincipalComponent },
  { path: 'login', component: LoginComponent },
  { path: 'registro', component: RegistroComponent },
  { path: 'perfil', component: PerfilUsuarioComponent },
  { path: 'editar-perfil', component: EditarUsuarioComponent },
  { path: 'administracion', component: AdministracionComponent },
  { path: 'gestion-reportes', component: GestionReportesComponent },
  { path: 'reporte-ciudadano', component: ReporteCiudadanoComponent },
  { path: 'seguimiento', component: SeguimientoComponent },
  { path: '**', redirectTo: '' }
];

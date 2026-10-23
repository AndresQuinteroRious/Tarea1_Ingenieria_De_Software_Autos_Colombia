import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'control-acceso',
    title: 'Control de acceso | Autos Colombia',
    loadComponent: () => import('./control-acceso/control-acceso').then((m) => m.ControlAcceso),
  },
  {
    path: 'gestion/operadores',
    title: 'Operadores | Autos Colombia',
    loadComponent: () => import('./operadores/operadores').then((m) => m.Operadores),
  },
  {
    path: 'gestion/celdas',
    title: 'Celdas | Autos Colombia',
    loadComponent: () => import('./celdas/celdas').then((m) => m.Celdas),
  },
  { path: '', pathMatch: 'full', loadComponent: () => import('./home/home').then((m) => m.Home) },
  {
    path: 'gestion/vehiculos',
    title: 'Vehículos | Autos Colombia',
    loadComponent: () => import('./vehiculos/vehiculos').then((m) => m.Vehiculos),
  },
  {
    path: 'gestion/usuarios',
    title: 'Usuarios | Autos Colombia',
    loadComponent: () => import('./usuarios/usuarios').then((m) => m.Usuarios),
  },
  {
    path: 'gestion/novedades',
    title: 'Novedades | Autos Colombia',
    loadComponent: () => import('./novedades/novedades').then((m) => m.Novedades),
  },
  {
    path: 'gestion/pagos',
    title: 'Pagos | Autos Colombia',
    loadComponent: () => import('./pagos/pagos').then((m) => m.Pagos),
  },
  { path: '**', redirectTo: '' },
];

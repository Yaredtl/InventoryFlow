import { Routes } from '@angular/router';
import { AppShell } from './shared/layout/app-shell';

export const routes: Routes = [
  {
    path: '',
    component: AppShell,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard',    loadComponent: () => import('./features/dashboard/dashboard').then(m => m.Dashboard) },
      { path: 'products',     loadComponent: () => import('./features/products/products').then(m => m.Products) },
      { path: 'categories',   loadComponent: () => import('./features/categories/categories').then(m => m.Categories) },
      { path: 'transactions', loadComponent: () => import('./features/transactions/transactions').then(m => m.Transactions) }
    ]
  }
];

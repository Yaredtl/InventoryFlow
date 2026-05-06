import { Component, inject, signal, OnInit } from '@angular/core';
import { ProductsService, Product } from './products.service';
import { CategoriesService, Category } from '../categories/categories.service';
import { ToastService } from '../../core/services/toast.service';
import { ProductForm } from './product-form/product-form';
import { ConfirmModal } from '../../shared/components/confirm-modal/confirm-modal';

@Component({
  selector: 'app-products',
  imports: [ProductForm, ConfirmModal],
  templateUrl: './products.html'
})
export class Products implements OnInit {
  private svc    = inject(ProductsService);
  private catSvc = inject(CategoriesService);
  private toast  = inject(ToastService);

  products     = signal<Product[]>([]);
  categories   = signal<Category[]>([]);
  showForm     = signal(false);
  editTarget   = signal<Product | null>(null);
  deleteTarget = signal<Product | null>(null);
  search       = signal('');

  ngOnInit(): void { this.load(); }

  load(): void {
    this.svc.getAll().subscribe(p => this.products.set(p));
    this.catSvc.getAll().subscribe(c => this.categories.set(c));
  }

  filtered(): Product[] {
    const q = this.search().toLowerCase();
    if (!q) return this.products();
    return this.products().filter(p =>
      p.name.toLowerCase().includes(q) || p.sku.toLowerCase().includes(q)
    );
  }

  stockStatus(p: Product): 'normal' | 'low' | 'empty' {
    if (p.current_stock === 0) return 'empty';
    if (p.current_stock <= p.min_stock_threshold) return 'low';
    return 'normal';
  }

  openCreate(): void {
    this.editTarget.set(null);
    this.showForm.set(true);
  }

  openEdit(p: Product): void {
    this.editTarget.set(p);
    this.showForm.set(true);
  }

  onSaved(): void {
    this.showForm.set(false);
    this.editTarget.set(null);
    this.load();
  }

  confirmDelete(p: Product): void { this.deleteTarget.set(p); }

  onDelete(): void {
    const p = this.deleteTarget();
    if (!p) return;
    this.svc.remove(p.id).subscribe({
      next: () => {
        this.toast.success('Eliminado', `${p.name} eliminado correctamente.`);
        this.deleteTarget.set(null);
        this.load();
      },
      error: () => this.deleteTarget.set(null)
    });
  }
}

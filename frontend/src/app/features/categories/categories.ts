import { Component, inject, signal, OnInit } from '@angular/core';
import { CategoriesService, Category } from './categories.service';
import { ToastService } from '../../core/services/toast.service';
import { CategoryForm } from './category-form/category-form';
import { ConfirmModal } from '../../shared/components/confirm-modal/confirm-modal';

@Component({
  selector: 'app-categories',
  imports: [CategoryForm, ConfirmModal],
  templateUrl: './categories.html'
})
export class Categories implements OnInit {
  private svc   = inject(CategoriesService);
  private toast = inject(ToastService);

  categories   = signal<Category[]>([]);
  showForm     = signal(false);
  editTarget   = signal<Category | null>(null);
  deleteTarget = signal<Category | null>(null);

  ngOnInit(): void { this.load(); }

  load(): void {
    this.svc.getAll().subscribe(c => this.categories.set(c));
  }

  openCreate(): void {
    this.editTarget.set(null);
    this.showForm.set(true);
  }

  openEdit(c: Category): void {
    this.editTarget.set(c);
    this.showForm.set(true);
  }

  onSaved(): void {
    this.showForm.set(false);
    this.editTarget.set(null);
    this.load();
  }

  confirmDelete(c: Category): void { this.deleteTarget.set(c); }

  onDelete(): void {
    const c = this.deleteTarget();
    if (!c) return;
    this.svc.remove(c.id).subscribe({
      next: () => {
        this.toast.success('Eliminado', `${c.name} eliminada correctamente.`);
        this.deleteTarget.set(null);
        this.load();
      },
      error: () => this.deleteTarget.set(null)
    });
  }
}

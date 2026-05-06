import { Component, OnInit, inject, input, output } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { CategoriesService, Category, CategoryPayload } from '../categories.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-category-form',
  imports: [ReactiveFormsModule],
  templateUrl: './category-form.html'
})
export class CategoryForm implements OnInit {
  category  = input<Category | null>(null);
  saved     = output<void>();
  cancelled = output<void>();

  private fb    = inject(FormBuilder);
  private svc   = inject(CategoriesService);
  private toast = inject(ToastService);

  loading = false;

  form = this.fb.group({
    name:        ['', [Validators.required, Validators.maxLength(100)]],
    description: ['', [Validators.maxLength(500)]]
  });

  get isEdit(): boolean { return !!this.category(); }

  fieldError(field: string): string | null {
    const c = this.form.get(field);
    if (!c?.touched || c.valid) return null;
    if (c.hasError('required'))  return 'Este campo es obligatorio.';
    if (c.hasError('maxlength')) return `Maximo ${c.errors?.['maxlength'].requiredLength} caracteres.`;
    return 'Valor invalido.';
  }

  ngOnInit(): void {
    const c = this.category();
    if (c) {
      this.form.patchValue({ name: c.name, description: c.description ?? '' });
    }
  }

  submit(): void {
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    const v = this.form.value;
    const payload: CategoryPayload = {
      name:        v.name!,
      description: v.description || null
    };
    this.loading = true;
    const req = this.isEdit
      ? this.svc.update(this.category()!.id, payload)
      : this.svc.create(payload);

    req.subscribe({
      next: () => {
        this.toast.success(this.isEdit ? 'Categoria actualizada' : 'Categoria creada');
        this.loading = false;
        this.saved.emit();
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 409) {
          this.toast.error('Nombre duplicado', err.error?.error ?? 'Ya existe esa categoria.');
        }
      }
    });
  }
}

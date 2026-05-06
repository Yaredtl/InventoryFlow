import { Component, OnInit, inject, input, output } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ProductsService, Product, ProductPayload } from '../products.service';
import { Category } from '../../categories/categories.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-product-form',
  imports: [ReactiveFormsModule],
  templateUrl: './product-form.html'
})
export class ProductForm implements OnInit {
  product    = input<Product | null>(null);
  categories = input<Category[]>([]);
  saved      = output<void>();
  cancelled  = output<void>();

  private fb    = inject(FormBuilder);
  private svc   = inject(ProductsService);
  private toast = inject(ToastService);

  loading = false;

  form = this.fb.group({
    name:                ['', [Validators.required, Validators.maxLength(150)]],
    sku:                 ['', [Validators.required, Validators.maxLength(50)]],
    price:               [null as number | null, [Validators.required, Validators.min(0.01)]],
    current_stock:       [0,  [Validators.required, Validators.min(0)]],
    min_stock_threshold: [0,  [Validators.required, Validators.min(0)]],
    category_id:         [null as number | null]
  });

  get isEdit(): boolean { return !!this.product(); }

  fieldError(field: string): string | null {
    const c = this.form.get(field);
    if (!c?.touched || c.valid) return null;
    if (c.hasError('required'))  return 'Este campo es obligatorio.';
    if (c.hasError('maxlength')) return `Maximo ${c.errors?.['maxlength'].requiredLength} caracteres.`;
    if (c.hasError('min'))       return `Valor minimo: ${c.errors?.['min'].min}.`;
    return 'Valor invalido.';
  }

  ngOnInit(): void {
    const p = this.product();
    if (p) {
      this.form.patchValue({
        name: p.name,
        sku:  p.sku,
        price: p.price,
        current_stock: p.current_stock,
        min_stock_threshold: p.min_stock_threshold,
        category_id: p.category_id
      });
    }
  }

  submit(): void {
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    const v = this.form.value;
    const payload: ProductPayload = {
      name:                v.name!,
      sku:                 v.sku!.toUpperCase().replace(/\s/g, ''),
      price:               v.price!,
      current_stock:       v.current_stock ?? 0,
      min_stock_threshold: v.min_stock_threshold ?? 0,
      category_id:         v.category_id ?? null
    };
    this.loading = true;
    const req = this.isEdit
      ? this.svc.update(this.product()!.id, payload)
      : this.svc.create(payload);

    req.subscribe({
      next: () => {
        this.toast.success(this.isEdit ? 'Producto actualizado' : 'Producto creado');
        this.loading = false;
        this.saved.emit();
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 409) {
          this.toast.error('SKU duplicado', err.error?.error ?? 'Ya existe ese SKU.');
        } else if (err.status === 422) {
          this.toast.error('Datos invalidos', err.error?.error ?? 'Revisa los campos.');
        }
      }
    });
  }
}

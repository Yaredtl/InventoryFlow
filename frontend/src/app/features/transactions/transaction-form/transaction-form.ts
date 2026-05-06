import { Component, inject, input, output, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { TransactionsService, StockConflict, TransactionCreate } from '../transactions.service';
import { Product } from '../../products/products.service';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-transaction-form',
  imports: [ReactiveFormsModule],
  templateUrl: './transaction-form.html'
})
export class TransactionForm {
  products  = input<Product[]>([]);
  saved     = output<void>();
  cancelled = output<void>();

  private fb    = inject(FormBuilder);
  private svc   = inject(TransactionsService);
  private toast = inject(ToastService);

  loading  = false;
  conflict = signal<StockConflict | null>(null);

  form = this.fb.group({
    product_id: [null as number | null, Validators.required],
    quantity:   [1, [Validators.required, Validators.min(1)]],
    type:       ['OUT', Validators.required]
  });

  fieldError(field: string): string | null {
    const c = this.form.get(field);
    if (!c?.touched || c.valid) return null;
    if (c.hasError('required')) return 'Este campo es obligatorio.';
    if (c.hasError('min'))      return 'Debe ser al menos 1.';
    return 'Valor invalido.';
  }

  submit(force = false): void {
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    const v = this.form.value;
    const payload: TransactionCreate = {
      product_id: v.product_id!,
      quantity:   v.quantity!,
      type:       v.type as 'IN' | 'OUT',
      force
    };
    this.loading = true;
    this.svc.create(payload).subscribe({
      next: (tx) => {
        this.loading = false;
        this.conflict.set(null);
        if (tx.warning) {
          this.toast.warning('Despacho parcial', tx.warning);
        } else {
          this.toast.success('Transaccion registrada');
        }
        this.saved.emit();
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 409) {
          this.conflict.set(err.error);
        } else if (err.status === 422) {
          this.toast.error('Datos invalidos', err.error?.error ?? 'Revisa los campos.');
        }
      }
    });
  }

  confirmForce(): void {
    this.conflict.set(null);
    this.submit(true);
  }
}

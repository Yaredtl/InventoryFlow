import { Component, inject, signal, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { forkJoin } from 'rxjs';
import { TransactionsService, Transaction } from './transactions.service';
import { ProductsService, Product } from '../products/products.service';
import { TransactionForm } from './transaction-form/transaction-form';

@Component({
  selector: 'app-transactions',
  imports: [TransactionForm, DatePipe],
  templateUrl: './transactions.html'
})
export class Transactions implements OnInit {
  private svc     = inject(TransactionsService);
  private prodSvc = inject(ProductsService);

  transactions = signal<Transaction[]>([]);
  products     = signal<Product[]>([]);
  showForm     = signal(false);
  loading      = signal(false);

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    forkJoin({ transactions: this.svc.getAll(), products: this.prodSvc.getAll() }).subscribe({
      next: ({ transactions, products }) => {
        this.transactions.set(transactions);
        this.products.set(products);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  productName(productId: number): string {
    return this.products().find(p => p.id === productId)?.name ?? `#${productId}`;
  }

  onSaved(): void {
    this.showForm.set(false);
    this.load();
  }
}

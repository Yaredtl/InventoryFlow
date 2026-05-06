import { Component, inject, signal, OnInit } from '@angular/core';
import { TransactionsService, Transaction } from './transactions.service';
import { ProductsService, Product } from '../products/products.service';
import { TransactionForm } from './transaction-form/transaction-form';

@Component({
  selector: 'app-transactions',
  imports: [TransactionForm],
  templateUrl: './transactions.html'
})
export class Transactions implements OnInit {
  private svc     = inject(TransactionsService);
  private prodSvc = inject(ProductsService);

  transactions = signal<Transaction[]>([]);
  products     = signal<Product[]>([]);
  showForm     = signal(false);

  ngOnInit(): void { this.load(); }

  load(): void {
    this.svc.getAll().subscribe(t => this.transactions.set(t));
    this.prodSvc.getAll().subscribe(p => this.products.set(p));
  }

  productName(productId: number): string {
    return this.products().find(p => p.id === productId)?.name ?? `#${productId}`;
  }

  onSaved(): void {
    this.showForm.set(false);
    this.load();
  }
}

import { Component, inject, signal, OnInit } from '@angular/core';
import { ProductsService } from '../products/products.service';
import { CategoriesService } from '../categories/categories.service';
import { TransactionsService } from '../transactions/transactions.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html'
})
export class Dashboard implements OnInit {
  private productsSvc     = inject(ProductsService);
  private categoriesSvc   = inject(CategoriesService);
  private transactionsSvc = inject(TransactionsService);

  totalProducts   = signal(0);
  totalCategories = signal(0);
  lowStockCount   = signal(0);
  todayTx         = signal(0);

  ngOnInit(): void {
    this.productsSvc.getAll().subscribe(p => this.totalProducts.set(p.length));
    this.productsSvc.getLowStock().subscribe(p => this.lowStockCount.set(p.length));
    this.categoriesSvc.getAll().subscribe(c => this.totalCategories.set(c.length));
    this.transactionsSvc.getAll(0, 1000).subscribe(t => {
      const today = new Date().toDateString();
      this.todayTx.set(
        t.filter(tx => new Date(tx.created_at).toDateString() === today).length
      );
    });
  }
}

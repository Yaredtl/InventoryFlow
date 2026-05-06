import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  current_stock: number;
  min_stock_threshold: number;
  category_id: number | null;
}

export interface ProductPayload {
  name: string;
  sku: string;
  price: number;
  current_stock?: number;
  min_stock_threshold?: number;
  category_id?: number | null;
}

const BASE = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class ProductsService {
  private http = inject(HttpClient);

  getAll(skip = 0, limit = 100): Observable<Product[]> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<Product[]>(`${BASE}/products`, { params });
  }

  getLowStock(): Observable<Product[]> {
    return this.http.get<Product[]>(`${BASE}/products/low-stock`);
  }

  create(data: ProductPayload): Observable<Product> {
    return this.http.post<Product>(`${BASE}/products`, data);
  }

  update(id: number, data: Partial<ProductPayload>): Observable<Product> {
    return this.http.patch<Product>(`${BASE}/products/${id}`, data);
  }

  remove(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${BASE}/products/${id}`);
  }
}

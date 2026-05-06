import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export type TransactionType = 'IN' | 'OUT';

export interface TransactionCreate {
  product_id: number;
  quantity: number;
  type: TransactionType;
  force?: boolean;
}

export interface Transaction {
  id: number;
  product_id: number;
  quantity: number;
  type: TransactionType;
  created_at: string;
  warning?: string | null;
  quantity_requested?: number | null;
}

export interface StockConflict {
  error: string;
  available_stock: number;
  requires_confirmation: boolean;
}

const BASE = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class TransactionsService {
  private http = inject(HttpClient);

  getAll(skip = 0, limit = 100): Observable<Transaction[]> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<Transaction[]>(`${BASE}/transactions`, { params });
  }

  create(data: TransactionCreate): Observable<Transaction> {
    return this.http.post<Transaction>(`${BASE}/transactions`, data);
  }
}

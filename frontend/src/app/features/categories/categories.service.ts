import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Category {
  id: number;
  name: string;
  description: string | null;
}

export interface CategoryPayload {
  name: string;
  description?: string | null;
}

const BASE = 'http://localhost:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class CategoriesService {
  private http = inject(HttpClient);

  getAll(): Observable<Category[]> {
    return this.http.get<Category[]>(`${BASE}/categories`);
  }

  create(data: CategoryPayload): Observable<Category> {
    return this.http.post<Category>(`${BASE}/categories`, data);
  }

  update(id: number, data: Partial<CategoryPayload>): Observable<Category> {
    return this.http.patch<Category>(`${BASE}/categories/${id}`, data);
  }

  remove(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${BASE}/categories/${id}`);
  }
}

import { Injectable, signal } from '@angular/core';

export type ToastType = 'success' | 'error' | 'warning';

export interface Toast {
  id: number;
  type: ToastType;
  message: string;
  description?: string;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  private nextId = 0;
  readonly toasts = signal<Toast[]>([]);

  show(type: ToastType, message: string, description?: string, duration = 4000): void {
    const id = ++this.nextId;
    this.toasts.update(list => [...list, { id, type, message, description }]);
    setTimeout(() => this.remove(id), duration);
  }

  success(message: string, description?: string): void { this.show('success', message, description); }
  error(message: string, description?: string): void   { this.show('error',   message, description); }
  warning(message: string, description?: string): void { this.show('warning', message, description); }

  remove(id: number): void {
    this.toasts.update(list => list.filter(t => t.id !== id));
  }
}

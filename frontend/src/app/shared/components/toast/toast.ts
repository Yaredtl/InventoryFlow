import { Component, inject } from '@angular/core';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.html'
})
export class ToastComponent {
  protected svc = inject(ToastService);
}

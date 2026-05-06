import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-confirm-modal',
  templateUrl: './confirm-modal.html'
})
export class ConfirmModal {
  title        = input('Confirmar accion');
  description  = input('');
  confirmLabel = input('Confirmar');
  visible      = input(false);

  confirmed = output<void>();
  cancelled = output<void>();
}

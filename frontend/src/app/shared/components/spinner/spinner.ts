import { Component, inject } from '@angular/core';
import { SpinnerService } from '../../../core/services/spinner.service';

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.html'
})
export class Spinner {
  protected spinner = inject(SpinnerService);
}

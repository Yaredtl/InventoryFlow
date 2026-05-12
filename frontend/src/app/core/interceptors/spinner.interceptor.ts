import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs';
import { SpinnerService } from '../services/spinner.service';

const MUTATION_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

export const spinnerInterceptor: HttpInterceptorFn = (_req, next) => {
  if (!MUTATION_METHODS.has(_req.method)) return next(_req);
  const spinner = inject(SpinnerService);
  spinner.show();
  return next(_req).pipe(finalize(() => spinner.hide()));
};

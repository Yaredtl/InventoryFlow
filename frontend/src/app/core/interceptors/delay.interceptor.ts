import { HttpInterceptorFn } from '@angular/common/http';
import { delay } from 'rxjs';

export const delayInterceptor: HttpInterceptorFn = (_req, next) => {
  return next(_req).pipe(delay(1000));
};

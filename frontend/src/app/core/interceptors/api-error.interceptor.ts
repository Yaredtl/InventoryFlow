import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { ToastService } from '../services/toast.service';

export const apiErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);

  return next(req).pipe(
    catchError(err => {
      if (err.status === 0) {
        toast.error('Sin conexion', 'No se pudo contactar con el servidor.');
      } else if (err.status >= 500) {
        toast.error('Error del servidor', 'Intenta de nuevo mas tarde.');
      }
      return throwError(() => err);
    })
  );
};

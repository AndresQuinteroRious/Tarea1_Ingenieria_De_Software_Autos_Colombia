import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { timeout } from 'rxjs';
import { Novedad, NovedadActualizar, NovedadCrear, NovedadesPagina } from '../models/novedad';

import { API_BASE_URL } from './api.service';

@Injectable({ providedIn: 'root' })
export class NovedadesService {
  private readonly http = inject(HttpClient);
  private readonly base = inject(API_BASE_URL);
  private readonly news = `${this.base}/novedades`;

  list(offset: number, limit: number) {
    return this.http
      .get<NovedadesPagina>(this.news, { params: { offset, limit } })
      .pipe(timeout(15000));
  }
  get(id: number) {
    return this.http.get<Novedad>(`${this.news}/${id}`).pipe(timeout(15000));
  }
  create(data: NovedadCrear) {
    return this.http.post<Novedad>(this.news, data).pipe(timeout(15000));
  }
  update(id: number, data: NovedadActualizar) {
    return this.http.patch<Novedad>(`${this.news}/${id}`, data).pipe(timeout(15000));
  }
  delete(id: number) {
    return this.http.delete<void>(`${this.news}/${id}`).pipe(timeout(15000));
  }
}

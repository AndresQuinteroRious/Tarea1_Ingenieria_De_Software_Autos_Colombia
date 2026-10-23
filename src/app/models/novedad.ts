export interface NovedadCrear {
  descripcion: string;
}
export type NovedadActualizar = Partial<NovedadCrear>;
export interface Novedad extends NovedadCrear {
  id: number;
  fecha: string;
}
export interface NovedadesPagina {
  items: Novedad[];
  total: number;
  offset: number;
  limit: number;
}

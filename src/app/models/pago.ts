export interface PagoCrear {
  valor: number;
  periodo: string;
}
export type PagoActualizar = Partial<PagoCrear>;
export interface Pago extends PagoCrear {
  id: number;
  fecha: string;
}
export interface PagosPagina {
  items: Pago[];
  total: number;
  offset: number;
  limit: number;
}

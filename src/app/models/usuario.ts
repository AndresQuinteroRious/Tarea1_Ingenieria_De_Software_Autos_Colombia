export interface UsuarioCrear {
  nombre: string;
  documento: string;
  telefono: string;
  fecha_vencimiento: string;
}
export type UsuarioActualizar = Partial<UsuarioCrear>;
export interface Usuario extends UsuarioCrear {
  id: number;
}
export interface UsuariosPagina {
  items: Usuario[];
  total: number;
  offset: number;
  limit: number;
}

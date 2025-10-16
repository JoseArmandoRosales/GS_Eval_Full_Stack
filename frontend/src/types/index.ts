/**
 * Tipos TypeScript para la aplicación
 */

export interface Sucursal {
  id: number;
  nombre: string;
  ciudad: string;
  direccion: string;
  telefono?: string;
  created_at: string;
}

export interface SolicitudCreate {
  // Datos del cliente
  nombre: string;
  apellido: string;
  email: string;
  telefono?: string;
  fecha_nacimiento: string;
  // Datos de la solicitud
  monto_solicitado: number;
  ingreso_mensual: number;
  score_crediticio: number;
  tiene_tarjeta_credito: boolean;
  tiene_credito_automotriz: boolean;
  plazo_meses: number;
  sucursal_id: number;
}

export interface SolicitudResponse {
  id: number;
  cliente_id: number;
  sucursal_id: number;
  monto_solicitado: number;
  ingreso_mensual: number;
  score_crediticio: number;
  tiene_tarjeta_credito: boolean;
  tiene_credito_automotriz: boolean;
  plazo_meses: number;
  estado: 'aprobado' | 'rechazado';
  motivo_rechazo?: string;
  fecha_solicitud: string;
  cliente_nombre?: string;
  cliente_email?: string;
  sucursal_nombre?: string;
  // Información financiera calculada
  cuota_mensual?: number;
  tasa_interes_anual?: number;
  total_a_pagar?: number;
  total_intereses?: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UsuarioAdmin {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface IndicadoresPorSucursal {
  sucursal_id: number;
  sucursal_nombre: string;
  ciudad: string;
  total_solicitudes: number;
  aprobadas: number;
  rechazadas: number;
  monto_promedio: number;
  monto_aprobado_total: number;
}

export interface IndicadoresGenerales {
  total_solicitudes: number;
  total_aprobadas: number;
  total_rechazadas: number;
  tasa_aprobacion: number;
  monto_total_solicitado: number;
  monto_total_aprobado: number;
  score_promedio: number;
  por_sucursal: IndicadoresPorSucursal[];
}

export interface SimulacionRequest {
  cantidad: number;
}

export interface SimulacionResponse {
  total_generadas: number;
  aprobadas: number;
  rechazadas: number;
  solicitudes: SolicitudResponse[];
}


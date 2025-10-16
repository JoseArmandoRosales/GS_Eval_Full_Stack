/**
 * Cliente API para comunicación con el backend
 */
import axios from 'axios';
import type {
  LoginRequest,
  TokenResponse,
  UsuarioAdmin,
  Sucursal,
  SolicitudCreate,
  SolicitudResponse,
  IndicadoresGenerales,
  SimulacionRequest,
  SimulacionResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Crear instancia de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token');
      window.location.href = '/admin';
    }
    return Promise.reject(error);
  }
);

// ==================== Autenticación ====================

export const login = async (credentials: LoginRequest): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>('/api/auth/login', credentials);
  return response.data;
};

export const getCurrentUser = async (): Promise<UsuarioAdmin> => {
  const response = await api.get<UsuarioAdmin>('/api/auth/me');
  return response.data;
};

// ==================== Sucursales ====================

export const getSucursales = async (): Promise<Sucursal[]> => {
  const response = await api.get<Sucursal[]>('/api/sucursales');
  return response.data;
};

// ==================== Solicitudes ====================

export const crearSolicitud = async (
  solicitud: SolicitudCreate
): Promise<SolicitudResponse> => {
  const response = await api.post<SolicitudResponse>('/api/solicitudes', solicitud);
  return response.data;
};

export const simularSolicitudes = async (
  datos: SimulacionRequest
): Promise<SimulacionResponse> => {
  const response = await api.post<SimulacionResponse>('/api/solicitudes/simular', datos);
  return response.data;
};

// ==================== Indicadores ====================

export const getIndicadores = async (): Promise<IndicadoresGenerales> => {
  const response = await api.get<IndicadoresGenerales>('/api/indicadores');
  return response.data;
};

export default api;


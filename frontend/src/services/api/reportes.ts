import { apiClient } from './client';
import { ReporteCreatePayload, ReporteResponse } from '../../types/reporte';

export async function crearReporte(payload: ReporteCreatePayload): Promise<ReporteResponse> {
  return apiClient<ReporteResponse>('/api/v1/reportes', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function obtenerHistorialUsuario(usuarioId: string): Promise<ReporteResponse[]> {
  return apiClient<ReporteResponse[]>(`/api/v1/reportes/usuario/${usuarioId}`);
}

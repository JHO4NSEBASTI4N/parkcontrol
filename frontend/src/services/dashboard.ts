import api from "./api";

export interface DashboardResumen {
  vehiculos_estacionados: number;
  ingresos_hoy: number | string;
  clientes_registrados: number;
  movimientos_hoy: number;
}

export async function obtenerResumenDashboard(): Promise<DashboardResumen> {
  const respuesta = await api.get<DashboardResumen>(
    "/api/dashboard/resumen"
  );

  return respuesta.data;
}
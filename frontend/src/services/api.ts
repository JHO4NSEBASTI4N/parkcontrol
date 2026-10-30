import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/",
  timeout: 10000,
  headers: {
    Accept: "application/json",
  },
});

api.interceptors.request.use((configuracion) => {
  const token = sessionStorage.getItem("parkcontrol_token");

  if (token) {
    configuracion.headers.Authorization = `Bearer ${token}`;
  }

  return configuracion;
});

api.interceptors.response.use(
  (respuesta) => respuesta,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      console.error("Error de comunicación con ParkControl:", {
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        estadoHTTP: error.response?.status,
        respuesta: error.response?.data,
        mensaje: error.message,
      });
    } else {
      console.error("Error inesperado:", error);
    }

    return Promise.reject(error);
  }
);

export default api;
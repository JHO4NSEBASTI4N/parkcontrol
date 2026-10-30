import api from "./api";

export interface RespuestaLogin {
  access_token: string;
  token_type: string;
}

export async function iniciarSesion(
  correo: string,
  contrasena: string
): Promise<RespuestaLogin> {
  const formulario = new URLSearchParams();

  formulario.append("username", correo);
  formulario.append("password", contrasena);

  const respuesta = await api.post<RespuestaLogin>(
    "/api/auth/login",
    formulario,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  sessionStorage.setItem(
    "parkcontrol_token",
    respuesta.data.access_token
  );

  return respuesta.data;
}
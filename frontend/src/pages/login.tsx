import { useState, type FormEvent } from "react";
import {
  CarFront,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
} from "lucide-react";
import { iniciarSesion } from "../services/autenticacion";

export default function Login() {
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [mostrarContrasena, setMostrarContrasena] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  async function manejarIngreso(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setError("");

    if (!correo.trim() || !contrasena) {
      setError("Ingresa tu correo y contraseña.");
      return;
    }

    setCargando(true);

    try {
      await iniciarSesion(correo.trim(), contrasena);
      window.location.href = "/dashboard";
    } catch (errorApi: unknown) {
      const mensaje =
        typeof errorApi === "object" &&
        errorApi !== null &&
        "response" in errorApi
          ? "Correo o contraseña incorrectos, o cuenta desactivada."
          : "No fue posible conectar con el servidor. Verifica que FastAPI esté funcionando.";

      setError(mensaje);
    } finally {
      setCargando(false);
    }
  }

  return (
    <main className="login-pagina">
      {/* Sección de Presentación / Branding */}
      <section className="login-presentacion">
        <div className="marca">
          <span className="marca-icono">
            <CarFront size={30} />
          </span>
          <span>
            Park<span className="marca-azul">Control</span>
          </span>
        </div>

        <div className="presentacion-contenido">
          <span className="etiqueta">GESTIÓN INTELIGENTE</span>
          <h1>
            Tu parqueadero,
            <br />
            bajo control.
          </h1>
          <p>
            Administra vehículos, clientes, tarifas y pagos desde una sola
            plataforma.
          </p>
        </div>

        <div className="presentacion-figura" aria-hidden="true">
          <div className="figura-circulo circulo-uno" />
          <div className="figura-circulo circulo-dos" />
          <CarFront className="figura-carro" size={150} strokeWidth={1} />
          <div className="figura-linea" />
        </div>

        <p className="presentacion-pie">Control eficiente. Operación segura.</p>
      </section>

      {/* Sección del Formulario */}
      <section className="login-formulario-contenedor">
        <div className="login-formulario">
          <div className="login-icono-movil">
            <CarFront size={32} />
          </div>

          <span className="bienvenida">BIENVENIDO DE NUEVO</span>
          <h2>Iniciar sesión</h2>
          <p className="subtitulo">
            Ingresa tus credenciales para acceder al sistema.
          </p>

          <form onSubmit={manejarIngreso}>
            {/* Campo Correo */}
            <label htmlFor="correo">Correo electrónico</label>
            <div className="campo">
              <Mail size={19} />
              <input
                id="correo"
                type="email"
                placeholder="usuario@ejemplo.com"
                autoComplete="username"
                value={correo}
                onChange={(evento) => setCorreo(evento.target.value)}
                required
              />
            </div>

            {/* Campo Contraseña */}
            <label htmlFor="contrasena">Contraseña</label>
            <div className="campo">
              <LockKeyhole size={19} />
              <input
                id="contrasena"
                type={mostrarContrasena ? "text" : "password"}
                placeholder="Ingresa tu contraseña"
                autoComplete="current-password"
                value={contrasena}
                onChange={(evento) => setContrasena(evento.target.value)}
                required
              />
              <button
                className="boton-ver"
                type="button"
                aria-label={
                  mostrarContrasena
                    ? "Ocultar contraseña"
                    : "Mostrar contraseña"
                }
                onClick={() => setMostrarContrasena(!mostrarContrasena)}
              >
                {mostrarContrasena ? <EyeOff size={19} /> : <Eye size={19} />}
              </button>
            </div>

            {/* Mensaje de Error */}
            {error && (
              <div className="mensaje-error" role="alert">
                {error}
              </div>
            )}

            {/* Botón de Enviar */}
            <button
              className="boton-ingresar"
              type="submit"
              disabled={cargando}
            >
              {cargando ? "Validando acceso..." : "Ingresar al sistema"}
            </button>
          </form>

          <p className="login-seguridad">
            <ShieldCheck size={17} />
            Acceso protegido para usuarios autorizados
          </p>
        </div>
      </section>
    </main>
  );
}
import { useCallback, useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  NavLink,
  useNavigate,
  Outlet,
} from "react-router-dom";
 
import {
  LayoutDashboard,
  CarFront,
  Users,
  ClipboardList,
  CreditCard,
  Tags,
  ShieldCheck,
  LogOut,
  Wallet,
  Clock3,
  RefreshCw,
  Menu,
  X,
  ParkingCircle,
} from "lucide-react";
 
import Login from "./pages/login";
// import Vehiculos from "./pages/Vehiculos";
import Clientes from "./pages/Clientes";
// import Movimientos from "./pages/Movimientos";
// import Tarifas from "./pages/Tarifas";
// import Pagos from "./pages/Pagos";
// import Usuarios from "./pages/Usuarios";
import { obtenerResumenDashboard } from "./services/dashboard";
import type { DashboardResumen } from "./services/dashboard";
import "./index.css";
 
const opcionesMenu = [
  { nombre: "Dashboard", ruta: "/dashboard", Icono: LayoutDashboard },
  { nombre: "Vehículos", ruta: "/vehiculos", Icono: CarFront },
  { nombre: "Clientes", ruta: "/clientes", Icono: Users },
  { nombre: "Movimientos", ruta: "/movimientos", Icono: ClipboardList },
  { nombre: "Pagos", ruta: "/pagos", Icono: CreditCard },
  { nombre: "Tarifas", ruta: "/tarifas", Icono: Tags },
  { nombre: "Usuarios", ruta: "/usuarios", Icono: ShieldCheck },
];
 
function formatoMoneda(valor: number | string) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(Number(valor) || 0);
}
 
/* =========================================================
   DASHBOARD Y MENÚ PRINCIPAL
========================================================= */
 
function Dashboard() {
  const navegar = useNavigate();
  const [menuMovil, setMenuMovil] = useState(false);
 
  function cerrarSesion() {
    sessionStorage.removeItem("parkcontrol_token");
    navegar("/", { replace: true });
  }
 
  return (
    <div className="pc-layout">
      {menuMovil && (
        <button
          className="pc-fondo-movil"
          aria-label="Cerrar menú"
          onClick={() => setMenuMovil(false)}
        />
      )}
 
      <aside
        className={`pc-sidebar ${
          menuMovil ? "pc-sidebar-abierto" : ""
        }`}
      >
        <div className="pc-marca">
          <span className="pc-marca-icono">
            <ParkingCircle size={29} />
          </span>
 
          <span>
            Park<span>Control</span>
          </span>
 
          <button
            className="pc-cerrar-menu"
            onClick={() => setMenuMovil(false)}
            aria-label="Cerrar menú"
          >
            <X size={22} />
          </button>
        </div>
 
        <p className="pc-menu-titulo">MENÚ PRINCIPAL</p>
 
        <nav className="pc-nav">
          {opcionesMenu.map(({ nombre, ruta, Icono }) => (
            <NavLink
              key={ruta}
              to={ruta}
              end
              className={({ isActive }) =>
                `pc-nav-enlace ${
                  isActive ? "pc-nav-activo" : ""
                }`
              }
              onClick={() => setMenuMovil(false)}
            >
              <Icono size={19} />
              <span>{nombre}</span>
 
              {ruta === "/dashboard" && (
                <span className="pc-indicador-activo" />
              )}
            </NavLink>
          ))}
        </nav>
 
        <div className="pc-sidebar-pie">
          <div className="pc-seguridad">
            <ShieldCheck size={20} />
 
            <div>
              <strong>Acceso seguro</strong>
              <span>Sesión autenticada</span>
            </div>
          </div>
 
          <button
            className="pc-boton-salir"
            onClick={cerrarSesion}
          >
            <LogOut size={19} />
            Cerrar sesión
          </button>
        </div>
      </aside>
 
      <main className="pc-contenido">
        <button
          className="pc-menu-movil"
          onClick={() => setMenuMovil(true)}
          aria-label="Abrir menú"
        >
          <Menu size={23} />
        </button>
 
        <Outlet />
      </main>
    </div>
  );
}
 
/* =========================================================
   PANTALLA PRINCIPAL DEL DASHBOARD
========================================================= */
 
function PaginaDashboard() {
  const [resumen, setResumen] =
    useState<DashboardResumen | null>(null);
 
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
 
  const cargarResumen = useCallback(async () => {
    setCargando(true);
    setError("");
 
    try {
      const datos = await obtenerResumenDashboard();
      setResumen(datos);
    } catch {
      setError(
        "No fue posible cargar los indicadores. Comprueba tu sesión y la conexión con el servidor."
      );
    } finally {
      setCargando(false);
    }
  }, []);
 
  useEffect(() => {
    void cargarResumen();
  }, [cargarResumen]);
 
  const tarjetas = [
    {
      titulo: "Vehículos estacionados",
      valor: resumen?.vehiculos_estacionados ?? "—",
      detalle: "Ingresos que continúan activos",
      Icono: CarFront,
      color: "#2563eb",
      fondo: "#eff6ff",
    },
    {
      titulo: "Ingresos del día",
      valor: resumen
        ? formatoMoneda(resumen.ingresos_hoy)
        : "—",
      detalle: "Pagos registrados hoy",
      Icono: Wallet,
      color: "#059669",
      fondo: "#ecfdf5",
    },
    {
      titulo: "Clientes registrados",
      valor: resumen?.clientes_registrados ?? "—",
      detalle: "Clientes activos",
      Icono: Users,
      color: "#7c3aed",
      fondo: "#f5f3ff",
    },
    {
      titulo: "Movimientos del día",
      valor: resumen?.movimientos_hoy ?? "—",
      detalle: "Entradas registradas hoy",
      Icono: Clock3,
      color: "#d97706",
      fondo: "#fffbeb",
    },
  ];
 
  return (
    <>
      <header className="pc-header">
        <div className="pc-header-izquierda">
          <div>
            <span className="pc-migas">
              PARKCONTROL / GENERAL
            </span>
 
            <h1>Dashboard</h1>
 
            <p>
              Resumen de la operación de tu parqueadero.
            </p>
          </div>
        </div>
 
        <button
          className="pc-actualizar"
          onClick={() => void cargarResumen()}
          disabled={cargando}
        >
          <RefreshCw
            size={17}
            className={cargando ? "pc-girando" : ""}
          />
          Actualizar
        </button>
      </header>
 
      <section className="pc-bienvenida">
        <div>
          <span className="pc-etiqueta">
            PANEL DE CONTROL
          </span>
 
          <h2>¡Bienvenido a ParkControl!</h2>
 
          <p>
            Consulta los indicadores y supervisa la actividad
            de tu parqueadero desde un solo lugar.
          </p>
        </div>
 
        <div className="pc-ilustracion" aria-hidden="true">
          <ParkingCircle size={72} strokeWidth={1.2} />
        </div>
      </section>
 
      {error && (
        <div className="pc-error" role="alert">
          <span>{error}</span>
 
          <button onClick={() => void cargarResumen()}>
            Reintentar
          </button>
        </div>
      )}
 
      <section className="pc-seccion">
        <div className="pc-seccion-encabezado">
          <div>
            <h2>Indicadores generales</h2>
            <p>Información consultada desde el servidor.</p>
          </div>
 
          <span className="pc-estado">
            <span />
            {cargando
              ? "Actualizando..."
              : error
                ? "Sin conexión"
                : "Datos consultados"}
          </span>
        </div>
 
        <div className="pc-tarjetas">
          {tarjetas.map(
            ({
              titulo,
              valor,
              detalle,
              Icono,
              color,
              fondo,
            }) => (
              <article
                className="pc-tarjeta"
                key={titulo}
              >
                <div className="pc-tarjeta-superior">
                  <span
                    className="pc-tarjeta-icono"
                    style={{ color, background: fondo }}
                  >
                    <Icono size={23} />
                  </span>
 
                  <span className="pc-tarjeta-punto" />
                </div>
 
                <p className="pc-tarjeta-titulo">
                  {titulo}
                </p>
 
                <div className="pc-tarjeta-valor">
                  {cargando && !resumen ? "..." : valor}
                </div>
 
                <p className="pc-tarjeta-detalle">
                  {detalle}
                </p>
              </article>
            )
          )}
        </div>
      </section>
 
      <section className="pc-informacion">
        <div className="pc-informacion-icono">
          <ShieldCheck size={25} />
        </div>
 
        <div>
          <h3>Panel conectado con ParkControl API</h3>
 
          <p>
            Los indicadores y módulos de gestión se conectan
            con FastAPI para administrar la operación del parqueadero.
          </p>
        </div>
      </section>
 
      <footer className="pc-footer">
        <span>
          ParkControl · Gestión inteligente de parqueaderos
        </span>
 
        <span>Panel administrativo</span>
      </footer>
    </>
  );
}
 
/* =========================================================
   PROTECCIÓN DE RUTAS
========================================================= */
 
function RutaProtegida() {
  const token = sessionStorage.getItem(
    "parkcontrol_token"
  );
 
  return token ? (
    <Outlet />
  ) : (
    <Navigate to="/" replace />
  );
}
 
/* =========================================================
   APLICACIÓN Y NAVEGACIÓN
========================================================= */
 
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
 
        <Route element={<RutaProtegida />}>
          <Route element={<Dashboard />}>
            <Route
              path="/dashboard"
              element={<PaginaDashboard />}
            />
 
            {/*  
            <Route
              path="/vehiculos"
              element={<Vehiculos />}
            />
 
            {/* MÓDULO CLIENTES INTEGRADO */}
            <Route
              path="/clientes"
              element={<Clientes />}
            />
 
 {/*
            <Route
              path="/movimientos"
              element={<Movimientos />}
            />
 
            <Route
              path="/pagos"
              element={<Pagos />}
            />
 
            <Route
              path="/tarifas"
              element={<Tarifas />}
            />
 
            <Route
              path="/usuarios"
              element={<Usuarios />}
            /> */}
          </Route>
        </Route>
 
        <Route
          path="*"
          element={<Navigate to="/dashboard" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}
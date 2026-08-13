# 🚨 Sistema de Reporte de Emergencias de Cartagena con IA y Trazabilidad

Sistema de respuesta rápida para emergencias en Cartagena (Accidentes, Inseguridad/Robos, Emergencias Médicas, Incidentes de Tránsito) con captura automática de GPS, fotos de evidencia, clasificación de severidad con IA (visión y orquestación local vía Ollama) y trazabilidad legal de identidad.

---

## 🏗️ Arquitectura General

El proyecto se divide en dos componentes principales:

```
emergencias-cartagena/
├── backend/            # FastAPI + SQLAlchemy + PostgreSQL + Agents IA (Ollama)
├── frontend/           # Mobile App en React Native + Expo (bun)
├── docker-compose.yml  # Levanta Postgres + Backend containerizados
└── README.md           # Guía técnica y de desarrollo
```

---

## ⚡ 1. Guía de Ejecución Rápida

### Backend + Base de Datos (Docker)
En la raíz del proyecto, ejecuta:

```bash
docker-compose up --build
```

- **API Backend**: `http://localhost:8000`
- **Documentación Swagger / OpenAPI**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **PostgreSQL**: Puerto `5432` (`emergencias_db`, usuario: `postgres`, clave: `postgres`)

### Frontend Mobile (Expo Go)
Desde la carpeta `frontend/`:

```bash
cd frontend
bun install
bunx expo start
```
Abre la aplicación **Expo Go** en tu celular y escanea el código QR que aparecerá en la consola.

---

## 📡 2. Contratos de Comunicación Frontend ↔ Backend

El frontend se comunica centralizadamente mediante `src/services/api/client.ts` pasando los endpoints descritos a continuación:

### **A. Crear Reporte de Emergencia**
- **Endpoint:** `POST /api/v1/reportes`
- **Payload (`ReporteCreate`):**
```json
{
  "tipo_emergencia": "accidente",
  "ubicacion_lat": 10.399722,
  "ubicacion_lng": -75.514444,
  "foto_url": "data:image/jpeg;base64,...",
  "organismo": "transito",
  "usuario_nombre": "Carlos Pérez",
  "usuario_telefono": "3001234567"
}
```
- **Respuesta (`ReportePublic`):**
```json
{
  "id": "c1f7b8d4-5a9e-4c7b-b3f2-1a4e5d6c7b8a",
  "tipo_emergencia": "accidente",
  "ubicacion_lat": 10.399722,
  "ubicacion_lng": -75.514444,
  "foto_url": "data:image/jpeg;base64,...",
  "organismo": "transito",
  "usuario_id": "8e7f6a5b-4c3d-2e1f-0a9b-8c7d6e5f4a3b",
  "severidad": "grave",
  "estado": "pendiente",
  "resumen_ia": "Reporte de Accidente con severidad GRAVE en zona de Cartagena.",
  "grupo_incidente_id": null,
  "created_at": "2026-08-13T10:30:00Z"
}
```

### **B. Consultar Historial del Usuario**
- **Endpoint:** `GET /api/v1/reportes/usuario/{usuario_id}`
- **Respuesta:** Lista de objetos `ReportePublic`.

### **C. Cola del Operador (Reordenamiento dinámico por severidad y tiempo)**
- **Endpoint:** `GET /api/v1/operador/cola`
- **Respuesta:** Lista de reportes ordenados según `score_prioridad` (combina severidad + minutos de espera).

### **D. Actualizar Estado de Reporte (Operador)**
- **Endpoint:** `PATCH /api/v1/operador/reportes/{id}/estado?nuevo_estado=en_atencion`
- **Estados válidos:** `pendiente`, `en_atencion`, `resuelto`, `descartado`.

---

## 🛠️ 3. Guía de Desarrollo para Agentes / Desarrolladores Frontend

Si un compañero o agente de IA va a extender la aplicación móvil, debe seguir las siguientes **reglas estrictas**:

1. **Estructura de Pantallas (`src/screens/`)**:
   - `SeleccionarTipoEmergencia/index.tsx`: Muestra las tarjetas con los 4 tipos de emergencia (`accidente`, `robo_inseguridad`, `emergencia_medica`, `incidente_transito`).
   - `CapturarUbicacionYFoto/index.tsx`: Gestiona el GPS nativo con `useUbicacion` y la cámara con `useCamara`. Pide el teléfono para la trazabilidad legal.
   - `ConfirmarReporte/index.tsx`: Muestra el resumen del reporte y el **Aviso Legal de Trazabilidad e Identidad** antes de realizar la petición HTTP.
   - `HistorialReportes/index.tsx`: Lista las emergencias reportadas anteriormente.

2. **Servicios HTTP (`src/services/api/`)**:
   - **NUNCA** hacer llamadas `fetch` o `axios` directas dentro de componentes o screens.
   - Toda llamada a la API debe agregarse en `src/services/api/reportes.ts` consumiendo `client.ts`.

3. **Tipado TypeScript (`src/types/`)**:
   - Mantener las interfaces en `src/types/reporte.ts` sincronizadas con los esquemas Pydantic del backend.

4. **Variables de Entorno**:
   - En celulares reales, define `EXPO_PUBLIC_API_URL=http://<TU_IP_LOCAL>:8000` para que el celular alcance el servidor backend corriendo en tu laptop/Docker.

---

## 👥 4. Roles y Flujo para la Demo del Pitch
1. **Flujo Ciudadano (Celular / Expo Go)**: Reporta con 1 toque → Captura GPS + Foto → Revisa Aviso Legal → Envía.
2. **Flujo Operador (Backend / Dashboard)**: Clasificación instantánea por IA de severidad + resumen automático → Asignación a Ambulancia / Policía / Tránsito.

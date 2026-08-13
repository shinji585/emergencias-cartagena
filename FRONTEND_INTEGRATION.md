# 📱 GUÍA DE INTEGRACIÓN FRONTEND - API DE REPORTES

## ✅ El Backend YA HACE el análisis de modelos automáticamente

Cuando tu frontend hace `POST /api/v1/reportes`, el backend **instantáneamente**:

1. 📸 Analiza la imagen (si existe) con Gemma3 - **VisionAgent**
2. 🧠 Orquesta el reporte con LLaMA - **OrchestratorAgent**  
3. 🎯 Detecta: HAZMAT, desastres, zona insular, Plan Candado
4. 📋 Enruta a organismos correspondientes - **RoutingAgent**
5. 💾 Persiste TODO en PostgreSQL

**No necesitas hacer nada más. El análisis ya está incluido.**

---

## 🔌 Conexión del Frontend

### 1️⃣ Endpoint para Crear Reporte (y hacer análisis)

```typescript
// src/services/api/reportes.ts
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// CREAR REPORTE - Automáticamente dispara análisis de modelos
export const crearReporte = async (datos: ReporteCreate) => {
  const response = await API.post('/reportes', {
    tipo_emergencia: datos.tipo_emergencia,
    ubicacion_lat: datos.ubicacion_lat,
    ubicacion_lng: datos.ubicacion_lng,
    descripcion: datos.descripcion, // ⭐ Esto es CLAVE para los modelos
    foto_url: datos.foto_url,       // ⭐ URL o base64 de imagen
    organismo: datos.organismo,
    usuario_nombre: datos.usuario_nombre,
    usuario_telefono: datos.usuario_telefono
  });
  
  // Respuesta incluye: id, severidad, resumen_ia, etc
  return response.data;
};
```

### Response del POST (Reporte creado + análisis ejecutado)

```json
{
  "id": "dafca6fc-657d-4032-b2db-6ab8057cb0de",
  "tipo_emergencia": "emergencia_industrial",
  "severidad": "grave",
  "resumen_ia": "Reporte de Emergencia Industrial... HAZMAT DETECTADO",
  "ubicacion_lat": 10.25,
  "ubicacion_lng": -75.65,
  "descripcion": "Fuga de gases tóxicos en Mamonal",
  "foto_url": null,
  "organismo": "policia",
  "usuario_id": "2082c27c-55b9-46eb-a811-962862acfe77",
  "estado": "pendiente",
  "grupo_incidente_id": null,
  "created_at": "2026-08-13T19:39:11.927101Z"
}
```

**⚠️ En este punto, los modelos YA ejecutaron análisis**

---

### 2️⃣ Endpoint para Obtener Despacho (ver organismos a despachar)

```typescript
// En tu pantalla de confirmación
export const obtenerDespacho = async (reporteId: string) => {
  const response = await API.get(`/reportes/${reporteId}/despacho`);
  
  // Contiene: organismos_notificados[], plan_candado (si es robo), etc
  return response.data;
};
```

### Response del GET despacho

```json
{
  "reporte_id": "dafca6fc-657d-4032-b2db-6ab8057cb0de",
  "tipo_emergencia": "emergencia_industrial",
  "severidad": "grave",
  "resumen_ia": "Reporte de Emergencia Industrial... HAZMAT DETECTADO",
  "cai_cercano": "CAI Zona Periférica",
  "organismos_notificados": [
    {
      "nombre": "Guardia Costera - Armada Nacional",
      "tipo": "rescate_maritimo",
      "telefono": "(+57 5) 6656 800",
      "accion": "Despachar unidad a coordenadas (10.25, -75.65)",
      "api_endpoint": "https://api.guardiacostera.mil.co/emergencias"
    },
    {
      "nombre": "CRUE - Coordinación en tierra",
      "tipo": "coordinacion_medica",
      "telefono": "(+57 5) 6600 123",
      "accion": "Despachar unidad a coordenadas (10.25, -75.65)",
      "api_endpoint": null
    }
  ],
  "plan_candado": null,
  "estado_despacho": "calculado",
  "mensaje": "Alerta generada y canalizada a 2 organismos"
}
```

---

### 3️⃣ Obtener Detalles del Reporte

```typescript
export const obtenerReporte = async (reporteId: string) => {
  const response = await API.get(`/reportes/${reporteId}`);
  return response.data;
};
```

### 4️⃣ Obtener Historial del Usuario

```typescript
export const obtenerHistorial = async (usuarioId: string) => {
  const response = await API.get(`/reportes/usuario/${usuarioId}`);
  return response.data; // array de reportes
};
```

---

## 🎯 Flujo Completo en tu App

### Pantalla: ConfirmarReporte

```typescript
// ConfirmarReporte/index.tsx
import React, { useState } from 'react';
import { crearReporte, obtenerDespacho } from '../services/api/reportes';

export const ConfirmarReporte: React.FC<Props> = ({ ubicacion, descripcion, foto }) => {
  const [cargando, setCargando] = useState(false);
  const [despacho, setDespacho] = useState(null);
  
  const handleConfirmar = async () => {
    setCargando(true);
    try {
      // PASO 1: Crear reporte → Backend automáticamente ejecuta modelos
      const reporte = await crearReporte({
        tipo_emergencia: "emergencia_industrial", // Del selector anterior
        ubicacion_lat: ubicacion.latitude,
        ubicacion_lng: ubicacion.longitude,
        descripcion: descripcion,  // ⭐ IMPORTANTE para análisis
        foto_url: foto,             // ⭐ IMPORTANTE para visión
        organismo: "policia",
        usuario_nombre: "Usuario",
        usuario_telefono: "3001234567"
      });
      
      console.log('✅ Reporte creado:', reporte.id);
      console.log('📊 Análisis IA completado:', reporte.resumen_ia);
      
      // PASO 2: Obtener despacho (lista de organismos a contactar)
      const despachoData = await obtenerDespacho(reporte.id);
      setDespacho(despachoData);
      
      console.log('🚨 Organismos a despachar:', despachoData.organismos_notificados);
      
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setCargando(false);
    }
  };
  
  return (
    <View>
      <Text>Descripción: {descripcion}</Text>
      <Text>Ubicación: {ubicacion.latitude}, {ubicacion.longitude}</Text>
      
      <Button 
        onPress={handleConfirmar}
        loading={cargando}
        title="Confirmar Reporte"
      />
      
      {despacho && (
        <View>
          <Text style={{fontSize: 18, fontWeight: 'bold'}}>
            🎯 Análisis Completado
          </Text>
          
          <Text>Severidad: {despacho.severidad}</Text>
          <Text>Resumen IA: {despacho.resumen_ia}</Text>
          
          <Text style={{marginTop: 10, fontWeight: 'bold'}}>
            📢 Organismos a despachar ({despacho.organismos_notificados.length}):
          </Text>
          {despacho.organismos_notificados.map(org => (
            <View key={org.nombre} style={{marginVertical: 5, paddingLeft: 10}}>
              <Text>• {org.nombre}</Text>
              <Text>  📞 {org.telefono}</Text>
              <Text>  ✈️ {org.accion}</Text>
            </View>
          ))}
          
          {despacho.plan_candado && (
            <View style={{marginTop: 10, backgroundColor: '#ffeeee'}}>
              <Text style={{fontWeight: 'bold', color: 'red'}}>
                🚔 PLAN CANDADO ACTIVADO
              </Text>
              <Text>Radio: {despacho.plan_candado.radio_huida_km} km</Text>
              <Text>Recomendación: {despacho.plan_candado.recomendacion_tactica}</Text>
            </View>
          )}
        </View>
      )}
    </View>
  );
};
```

---

## 🔄 Campos Importantísimos para que los Modelos Funcionen Bien

| Campo | Requerido | Uso | Ejemplo |
|-------|----------|-----|---------|
| `tipo_emergencia` | ✅ | Enrutamiento inicial | `emergencia_industrial` |
| `descripcion` | ✅ | **Análisis IA (HAZMAT, desastres, Plan Candado)** | `"Fuga de gases tóxicos"` |
| `foto_url` | ⚠️ | Análisis de visión (si existe) | URL o base64 |
| `ubicacion_lat/lng` | ✅ | Zona insular, CAI cercano | `10.25, -75.65` |
| `organismo` | ✅ | Asignación inicial | `policia` |
| `usuario_telefono` | ⚠️ | Seguimiento | `3001234567` |

---

## 🧪 Test en Terminal

```bash
# Crear reporte con HAZMAT
curl -X POST http://localhost:8000/api/v1/reportes \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_emergencia": "emergencia_industrial",
    "ubicacion_lat": 10.25,
    "ubicacion_lng": -75.65,
    "descripcion": "Fuga de gases tóxicos en Mamonal",
    "foto_url": null,
    "organismo": "policia",
    "usuario_nombre": "Test",
    "usuario_telefono": "3001234567"
  }'

# Obtener despacho (reemplazar ID)
curl http://localhost:8000/api/v1/reportes/{REPORT_ID}/despacho
```

---

## 📊 Casos Validados

✅ **HAZMAT**: "fuga de gases", "químicos", "explosión", "tóxicos" → Guardia Costera + Bomberos
✅ **Desastres**: "inundación", "lluvia", "desbordamiento" → Bomberos + Defensa Civil
✅ **Plan Candado**: Tipo=robo_inseguridad → Radio huida calculado
✅ **Insular**: Lat 10.0-10.28, Lng -76.5 a -75.55 → Guardia Costera
✅ **Tránsito**: Tipo=accidente → CRUE + DATT + Ambulancia

---

## ✅ RESUMEN FINAL

**El análisis de modelos ESTÁ INCLUIDO en el POST**

No necesitas hacer:
- ❌ POST a un endpoint de análisis
- ❌ Llamar manualmente a visión
- ❌ Esperar a otro endpoint

Solo necesitas:
1. ✅ POST /api/v1/reportes (backend hace TODO)
2. ✅ GET /api/v1/reportes/{id}/despacho (ver resultados)

**Listo para hacer push cuando quieras ✨**

# 🚀 Guía de Ejecución Local con Modelos IA

## Requisitos
- **WSL2 con Ubuntu 22.04**
- **Docker y Docker Compose** 
- **Ollama instalado** en WSL (localhost:11434)
- **RAM disponible:** 16 GB mínimo para Q4 cuantización

## Paso 1: Verificar que Ollama está corriendo

```bash
# Ver modelos instalados
ollama list

# Debería mostrar:
# gemma3:4b      3.3 GB
# llama3.2:3b    2.0 GB

# Si falta alguno, instalar:
ollama pull gemma3:4b
ollama pull llama3.2:3b

# Ver que esté escuchando en puerto 11434
netstat -an | grep 11434
```

## Paso 2: Iniciar los servicios Docker

```bash
cd /home/toji/projects/emergencias-cartagena

# Construir imagen backend
docker-compose build

# Iniciar servicios (DB + Backend)
docker-compose up

# En otra terminal, verificar salud
docker-compose ps
docker logs emergencias_cartagena_backend
```

## Paso 3: Probar la API

```bash
# Health check
curl http://localhost:8000/health

# Ver documentación interactiva
# Abrir en navegador: http://localhost:8000/docs

# Test: Crear un reporte
curl -X POST http://localhost:8000/api/v1/reportes \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_emergencia": "ACCIDENTE",
    "ubicacion_lat": 10.3915,
    "ubicacion_lng": -75.5093,
    "descripcion": "Accidente de tránsito con heridos en Centro Histórico",
    "organismo": "CRUE",
    "usuario_nombre": "Juan Pérez",
    "usuario_telefono": "3005551234"
  }'
```

## Paso 4: Verificar que los modelos están siendo usados

```bash
# Ver logs del backend
docker logs -f emergencias_cartagena_backend

# Debería mostrar:
# 📸 Analizando imagen para emergencia: ACCIDENTE
# 🧠 Orquestando reporte - Buscando duplicados...
# 🚨 Enrutando emergencia a organismos...
```

## Arquitectura Local

```
┌─ WSL2 Ubuntu 22.04 ────────────────────────────────────────────┐
│                                                                 │
│  ┌─ Ollama (localhost:11434) ──────────────────────────────┐  │
│  │  ├─ llama3.2:3b (2.0 GB) - Texto/Orquestación         │  │
│  │  └─ gemma3:4b   (3.3 GB) - Visión/Análisis            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ▲                                   │
│  ┌─ Docker Compose ────────┼───────────────────────────────┐  │
│  │  ┌──────────────────────┼────────────────────────────┐  │  │
│  │  │ Backend (8000)       │                            │  │  │
│  │  │  ├─ FastAPI app      └─► Llamadas a Ollama       │  │  │
│  │  │  ├─ OrchestratorAgent                            │  │  │
│  │  │  ├─ VisionAgent                                  │  │  │
│  │  │  └─ RoutingAgent                                 │  │  │
│  │  └───────────────────┬─────────────────────────────┘  │  │
│  │                      │                                  │  │
│  │  ┌──────────────────┘                                  │  │
│  │  │ PostgreSQL (5432)                                   │  │
│  │  │  ├─ usuarios                                        │  │
│  │  │  ├─ reportes                                        │  │
│  │  │  └─ clasificaciones_ia                              │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Casos de Uso Implementados

### 1️⃣ Accidentes de Tránsito
- Detección automática de tránsito
- Notificación a CRUE y hospitales cercanos
- Generación de desvíos dinámicos

### 2️⃣ Desastres Naturales/Inundaciones
- Deduplicación inteligente por zona
- Detección de palabras clave de riesgo
- Agrupación de reportes en incidente sectorial

### 3️⃣ Emergencias Industriales (HAZMAT)
- Detección de términos: químicos, gas, incendio, tóxicos
- Elevación automática a SEVERIDAD CRÍTICA
- Notificación a Brigadas HAZMAT especiales

### 4️⃣ Emergencias Turísticas Insulares
- Detección de ubicación insular
- Traducción multilingüe (en/fr/de → es)
- Notificación a Guardia Costera

### 5️⃣ Robos e Inseguridad
- Mapeo automático a CAI más cercano
- Cálculo de radio de huida (Plan Candado)
- Coordenadas de cierre de vías

## Troubleshooting

### ❌ Error: Ollama connection refused
```bash
# Verificar que Ollama está corriendo
ollama serve

# O verificar puerto en uso
netstat -an | grep 11434
```

### ❌ Error: Model not found
```bash
# Descargar modelos manualmente
ollama pull llama3.2:3b
ollama pull gemma3:4b

# Verificar tamaño disponible
df -h
```

### ❌ Error: Out of memory
```bash
# Si tienes menos de 16 GB RAM, usar Q5_K_M o Q6_K_M
# Editar docker-compose.yml con variable OLLAMA_MODEL_QUANTIZATION
# Nota: Afectará velocidad de inferencia
```

### ❌ Base de datos no inicializa
```bash
# Resetear BD
docker-compose down -v
docker-compose up --build

# Verificar esquema
docker exec -it emergencias_cartagena_db psql -U postgres -d emergencias_db -c "\dt"
```

## Monitoreo en Producción Local

```bash
# Ver recursos en tiempo real
docker stats

# Logs del backend
docker logs -f --tail=50 emergencias_cartagena_backend

# Conectar a BD
docker exec -it emergencias_cartagena_db psql -U postgres -d emergencias_db
SELECT id, tipo_emergencia, severidad, estado FROM reportes ORDER BY created_at DESC LIMIT 10;
```

## Variables de Entorno

Ver `.env.local` para configuración completa. Opciones principales:

- `OLLAMA_URL`: Dirección del servidor Ollama
- `OLLAMA_TEXT_MODEL`: Modelo para análisis de texto (default: llama3.2:3b)
- `OLLAMA_VISION_MODEL`: Modelo para análisis de imágenes (default: gemma3:4b)
- `DATABASE_URL`: Cadena de conexión PostgreSQL
- `LOG_LEVEL`: Nivel de logs (DEBUG, INFO, WARNING, ERROR)

---

**Última actualización:** 13 de Agosto de 2026  
**Status:** ✅ Totalmente local - Sin servidor remoto

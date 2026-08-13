import urllib.request
import json
import time
import sys

base = "http://localhost:8000"

def req(method, endpoint, data=None):
    url = base + endpoint
    body = json.dumps(data).encode("utf-8") if data else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            elapsed = round((time.time() - start) * 1000, 2)
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}, elapsed
    except urllib.error.HTTPError as e:
        elapsed = round((time.time() - start) * 1000, 2)
        content = e.read().decode("utf-8")
        try:
            return e.code, json.loads(content), elapsed
        except Exception:
            return e.code, content, elapsed
    except Exception as e:
        return 0, str(e), 0

print("================================================================================")
print("🚀 EJECUTANDO SUITE COMPLETA DE PRUEBAS E2E (API FASTAPI + DOCKER)")
print("================================================================================")

results = []

# 1. Health Check
s, d, el = req("GET", "/health")
results.append(("1. Health Check", s, el, "PASS" if s == 200 else "FAIL", str(d)))

# 2. Registrar Usuario
u_payload = {"nombre": "Samuel Vargas", "telefono": "3009876543"}
s, d, el = req("POST", "/api/v1/usuarios", u_payload)
user_id = d.get("id") if isinstance(d, dict) else None
results.append(("2. Crear Usuario", s, el, "PASS" if s == 201 else "FAIL", f"ID: {user_id}"))

# 3. Obtener Usuario por ID
s, d, el = req("GET", f"/api/v1/usuarios/{user_id}")
results.append(("3. Obtener Usuario por ID", s, el, "PASS" if s == 200 else "FAIL", d.get("nombre") if isinstance(d, dict) else ""))

# 4. Caso 1: Accidente de Tránsito
c1 = {
    "tipo_emergencia": "accidente",
    "ubicacion_lat": 10.4236,
    "ubicacion_lng": -75.5350,
    "descripcion": "Colisión múltiple entre dos autos y una moto en Av. Santander frente a Marbella",
    "organismo": "transito",
    "usuario_id": user_id
}
s, d, el = req("POST", "/api/v1/reportes", c1)
r1_id = d.get("id") if isinstance(d, dict) else None
sev1 = d.get("severidad", "") if isinstance(d, dict) else ""
results.append(("4. Caso 1: Accidente Tránsito", s, el, "PASS" if s == 201 else "FAIL", f"ID: {r1_id} | Severidad: {sev1}"))

# 5. Caso 2: Inundación / Desastre Natural
c2 = {
    "tipo_emergencia": "accidente",
    "ubicacion_lat": 10.3950,
    "ubicacion_lng": -75.4950,
    "descripcion": "Desbordamiento grave de caño por lluvia torrencial, vía totalmente anegada e inundada en Olaya",
    "organismo": "transito",
    "usuario_id": user_id
}
s, d, el = req("POST", "/api/v1/reportes", c2)
r2_id = d.get("id") if isinstance(d, dict) else None
res2 = d.get("resumen_ia", "") if isinstance(d, dict) else ""
results.append(("5. Caso 2: Inundación / Desastre", s, el, "PASS" if s == 201 else "FAIL", f"ID: {r2_id} | Resumen: {res2[:45]}..."))

# 6. Caso 3: HAZMAT Químicos Mamonal
c3 = {
    "tipo_emergencia": "emergencia_industrial",
    "ubicacion_lat": 10.3150,
    "ubicacion_lng": -75.5050,
    "descripcion": "Fuga masiva de químicos tóxicos y escape de gas en sector petroquímico de Mamonal",
    "organismo": "policia",
    "usuario_id": user_id
}
s, d, el = req("POST", "/api/v1/reportes", c3)
r3_id = d.get("id") if isinstance(d, dict) else None
sev3 = d.get("severidad", "") if isinstance(d, dict) else ""
results.append(("6. Caso 3: HAZMAT Industrial", s, el, "PASS" if s == 201 else "FAIL", f"ID: {r3_id} | Severidad: {sev3}"))

# 7. Caso 4: Turístico Insular (Islas del Rosario / Barú)
c4 = {
    "tipo_emergencia": "emergencia_medica",
    "ubicacion_lat": 10.1500,
    "ubicacion_lng": -75.7800,
    "descripcion": "Medical emergency on boat near Rosario Islands, tourist injured, need immediate ambulance",
    "organismo": "ambulancia",
    "usuario_id": user_id
}
s, d, el = req("POST", "/api/v1/reportes", c4)
r4_id = d.get("id") if isinstance(d, dict) else None
res4 = d.get("resumen_ia", "") if isinstance(d, dict) else ""
results.append(("7. Caso 4: Turístico Insular", s, el, "PASS" if s == 201 else "FAIL", f"ID: {r4_id} | Resumen: {res4[:45]}..."))

# 8. Caso 5: Robo e Inseguridad (Plan Candado)
c5 = {
    "tipo_emergencia": "robo_inseguridad",
    "ubicacion_lat": 10.4220,
    "ubicacion_lng": -75.5480,
    "descripcion": "Atraco con arma de fuego a transeúnte en Calle Don Sancho Centro Histórico",
    "organismo": "policia",
    "usuario_id": user_id
}
s, d, el = req("POST", "/api/v1/reportes", c5)
r5_id = d.get("id") if isinstance(d, dict) else None
results.append(("8. Caso 5: Robo / Plan Candado", s, el, "PASS" if s == 201 else "FAIL", f"ID: {r5_id}"))

# 9. Cola Priorizada del Operador
s, d, el = req("GET", "/api/v1/operador/cola")
cola_len = len(d) if isinstance(d, list) else 0
results.append(("9. Cola Despacho Operador", s, el, "PASS" if s == 200 else "FAIL", f"Total en cola activa: {cola_len}"))

# 10. Métricas del Operador
s, d, el = req("GET", "/api/v1/operador/metricas")
results.append(("10. Métricas del Operador", s, el, "PASS" if s == 200 else "FAIL", f"Metricas: {d}"))

# 11. Actualizar Estado de Reporte
s, d, el = req("PATCH", f"/api/v1/operador/reportes/{r1_id}/estado?nuevo_estado=en_atencion")
est11 = d.get("estado", "") if isinstance(d, dict) else ""
results.append(("11. Actualizar Estado (Operador)", s, el, "PASS" if s == 200 else "FAIL", f"Nuevo estado: {est11}"))

# 12. Historial de Reportes por Usuario
s, d, el = req("GET", f"/api/v1/reportes/usuario/{user_id}")
uhist = len(d) if isinstance(d, list) else 0
results.append(("12. Historial de Usuario", s, el, "PASS" if s == 200 else "FAIL", f"Total reportes creados: {uhist}"))

all_passed = True
for name, status, lat, verdict, detail in results:
    if verdict != "PASS":
        all_passed = False
    print(f"[{verdict:4}] {name:32} | HTTP {status} | {lat:7.2f}ms | {detail}")

print("================================================================================")
if all_passed:
    print("✅ TODAS LAS PRUEBAS E2E PASARON EXITOSAMENTE (12/12 - 100%)")
else:
    print("❌ ALGUNAS PRUEBAS FALLARON")
    sys.exit(1)

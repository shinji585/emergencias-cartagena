"""
Test rápido para validar la orquestación de modelos Ollama.
Ejecutar: python tests/test_rapid_ollama.py
"""
import asyncio

from app.agents.orchestrator import OrchestratorAgent
from app.agents.vision import VisionAgent
from app.schemas.enums import Severidad, TipoEmergencia


async def test_caso_1_accidente_transito():
    """CASO 1: Accidente de tránsito - Modelo de texto"""
    print("\n" + "="*60)
    print("TEST CASO 1: ACCIDENTE DE TRÁNSITO")
    print("="*60)
    
    orchestrator = OrchestratorAgent()
    
    resultado = await orchestrator.generate_summary_and_grouping(
        tipo=TipoEmergencia.INCIDENTE_TRANSITO,
        severidad=Severidad.GRAVE,
        lat=10.3915,
        lng=-75.5093,
        existentes=[],
        descripcion="Choque entre dos vehículos en Av. Santander con 3 heridos"
    )
    
    print(f"✅ Resumen IA: {resultado['resumen_ia']}")
    print(f"   Severidad: {resultado.get('severidad_ajustada', 'grave')}")
    print(f"   Grupo ID: {resultado.get('grupo_incidente_id', 'Nuevo incidente')}")
    print(f"   Organismos: {resultado.get('organismos_primarios', [])}")
    return True


async def test_caso_2_inundacion():
    """CASO 2: Desastre natural - Deduplicación"""
    print("\n" + "="*60)
    print("TEST CASO 2: INUNDACIÓN - DEDUPLICACIÓN")
    print("="*60)
    
    orchestrator = OrchestratorAgent()
    
    # Simular reportes previos en la misma zona
    existentes = [
        {
            "id": "rep-001",
            "ubicacion_lat": 10.38,
            "ubicacion_lng": -75.51,
            "tipo_emergencia": TipoEmergencia.ACCIDENTE.value,
            "grupo_incidente_id": "grupo-inundacion-01",
        }
    ]
    
    resultado = await orchestrator.generate_summary_and_grouping(
        tipo=TipoEmergencia.ACCIDENTE,
        severidad=Severidad.GRAVE,
        lat=10.381,  # ~100m de distancia
        lng=-75.511,
        existentes=existentes,
        descripcion="Inundación en barrio vulnerable - múltiples reportes"
    )
    
    print(f"✅ Resumen IA: {resultado['resumen_ia']}")
    print(f"   Grupo ID: {resultado.get('grupo_incidente_id', 'Nuevo')}")
    print(f"   Detectó duplicado: {resultado.get('grupo_incidente_id') is not None}")
    return True


async def test_caso_3_hazmat():
    """CASO 3: HAZMAT - Detección y elevación automática"""
    print("\n" + "="*60)
    print("TEST CASO 3: HAZMAT - DETECCIÓN AUTOMÁTICA")
    print("="*60)
    
    orchestrator = OrchestratorAgent()
    
    # Test múltiples palabras clave HAZMAT
    hazmat_descriptions = [
        "Fuga de gases tóxicos en Mamonal",
        "Incendio industrial en planta química",
        "Derrame de químicos peligrosos",
        "Explosión en fábrica de reactivos"
    ]
    
    for desc in hazmat_descriptions:
        is_hazmat = orchestrator._detect_hazmat_risk(desc)
        print(f"  '{desc}' → HAZMAT detectado: {is_hazmat}")
        assert is_hazmat, f"No detectó HAZMAT en: {desc}"
    
    # Generar despacho con HAZMAT
    resultado = await orchestrator.generate_summary_and_grouping(
        tipo=TipoEmergencia.EMERGENCIA_INDUSTRIAL,
        severidad=Severidad.GRAVE,
        lat=10.25,
        lng=-75.65,
        existentes=[],
        descripcion="Fuga de gases tóxicos en planta"
    )
    
    print(f"\n✅ Resumen IA: {resultado['resumen_ia']}")
    print(f"   HAZMAT detectado: {'HAZMAT' in resultado['resumen_ia']}")
    print(f"   Severidad: {resultado.get('severidad_ajustada', 'grave')}")
    return True


async def test_caso_4_insular():
    """CASO 4: Emergencia Insular - Zona y Guardia Costera"""
    print("\n" + "="*60)
    print("TEST CASO 4: EMERGENCIA INSULAR")
    print("="*60)
    
    orchestrator = OrchestratorAgent()
    
    # Probar ubicaciones insulares
    ubicaciones = [
        (10.15, -76.15, "Islas del Rosario"),
        (10.17, -75.78, "Barú"),
        (10.18, -75.85, "Tierra Bomba"),
        (10.3815, -75.5097, "Centro Histórico - NO insular"),
    ]
    
    for lat, lng, nombre in ubicaciones:
        is_insular = orchestrator._is_location_insular(lat, lng)
        print(f"  {nombre} ({lat}, {lng}) → Insular: {is_insular}")
    
    # Generar despacho insular
    resultado = await orchestrator.generate_summary_and_grouping(
        tipo=TipoEmergencia.EMERGENCIA_MEDICA,
        severidad=Severidad.GRAVE,
        lat=10.15,
        lng=-76.15,
        existentes=[],
        descripcion="Turista con emergencia médica en isla"
    )
    
    print(f"\n✅ Resumen IA: {resultado['resumen_ia']}")
    print(f"   Zona Insular detectada: {'INSULAR' in resultado['resumen_ia']}")
    return True


async def test_caso_5_plan_candado():
    """CASO 5: Robo - Plan Candado"""
    print("\n" + "="*60)
    print("TEST CASO 5: PLAN CANDADO - ROBO/INSEGURIDAD")
    print("="*60)
    
    orchestrator = OrchestratorAgent()
    
    # Test cálculo de radio de huida
    tiempos = [1, 3, 5, 10]
    print("  Radio de huida según tiempo transcurrido:")
    for minutos in tiempos:
        radio = orchestrator._calculate_escape_radius_km(minutos)
        print(f"    {minutos} min → {radio:.2f} km")
    
    # Generar análisis de Plan Candado
    plan = await orchestrator.analyze_robo_plan_candado(
        lat=10.3915,
        lng=-75.5093,
        minutes_elapsed=3
    )
    
    print("\n✅ Plan Candado:")
    print(f"   Punto: ({plan['punto_incidente']['lat']}, {plan['punto_incidente']['lng']})")
    print(f"   Radio de huida: {plan['radio_huida_km']:.2f} km")
    print(f"   Tiempo transcurrido: {plan['tiempo_transcurrido_min']} min")
    print(f"   Acción: {plan['accion']}")
    return True


async def test_vision_agent():
    """Test VisionAgent sin imagen (fallback)"""
    print("\n" + "="*60)
    print("TEST VISION AGENT (SIN IMAGEN)")
    print("="*60)
    
    vision = VisionAgent()
    
    # Test sin imagen
    resultado = await vision.analyze_image(
        tipo=TipoEmergencia.ACCIDENTE,
        foto_url=None,
        descripcion="Accidente grave con múltiples heridos"
    )
    
    print("✅ Análisis sin imagen:")
    print(f"   Severidad: {resultado['severidad']}")
    print(f"   Confianza: {resultado['confianza']:.2f}")
    print(f"   Justificación: {resultado['justificacion']}")
    print(f"   Coincide tipo: {resultado['coincide_tipo']}")
    return True


async def main():
    """Ejecutar todos los tests"""
    print("\n" + "🚀 INICIANDO TESTS DE ORQUESTACIÓN DE MODELOS OLLAMA")
    print("="*60)
    
    try:
        # Verificar que Ollama está disponible
        print("Verificando Ollama en localhost:11434...")
        import httpx
        async with httpx.AsyncClient(timeout=2.0) as client:
            res = await client.get("http://localhost:11434/api/tags")
            if res.status_code == 200:
                print("✅ Ollama disponible")
                models = res.json().get("models", [])
                print(f"   Modelos: {[m['name'] for m in models]}")
            else:
                print("❌ Ollama no responde correctamente")
                return False
    except Exception as e:
        print(f"❌ Error conectando a Ollama: {e}")
        print("   Asegurate de ejecutar: ollama serve")
        return False
    
    # Ejecutar tests
    tests = [
        test_caso_1_accidente_transito,
        test_caso_2_inundacion,
        test_caso_3_hazmat,
        test_caso_4_insular,
        test_caso_5_plan_candado,
        test_vision_agent,
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"\n❌ Error en {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test.__name__, False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"✅ Pasados: {passed}/{total}")
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
    
    return all(r for _, r in results)


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

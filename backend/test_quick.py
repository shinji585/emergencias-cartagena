#!/usr/bin/env python3
"""
Test ultra-rápido de conectividad a Ollama.
No requiere dependencias del proyecto, solo urllib.
"""
import json
import urllib.error
import urllib.request


def test_ollama_health():
    """Verifica que Ollama está respondiendo"""
    print("\n" + "="*60)
    print("TEST 1: OLLAMA HEALTH")
    print("="*60)
    
    try:
        url = "http://localhost:11434/api/tags"
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = data.get("models", [])
            print("✅ Ollama respondiendo en localhost:11434")
            print(f"   Modelos encontrados: {len(models)}")
            for m in models:
                print(f"     - {m['name']} ({m['size']} bytes)")
            return True
    except Exception as e:
        print(f"❌ Error conectando a Ollama: {e}")
        return False


def test_ollama_generate_text():
    """Prueba generación de texto con llama3.2"""
    print("\n" + "="*60)
    print("TEST 2: GENERACIÓN DE TEXTO (llama3.2:3b)")
    print("="*60)
    
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",
            "prompt": "Di una frase breve sobre emergencias en Cartagena",
            "stream": False,
            "num_predict": 50,
            "temperature": 0.3
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            text = data.get("response", "").strip()
            print("✅ Modelo llama3.2:3b respondiendo")
            print(f"   Respuesta: {text[:100]}...")
            return True
    except Exception as e:
        print(f"❌ Error en generación de texto: {e}")
        return False


def test_ollama_vision():
    """Prueba si gemma3:4b está disponible"""
    print("\n" + "="*60)
    print("TEST 3: DISPONIBILIDAD GEMMA3:4b (VISIÓN)")
    print("="*60)
    
    try:
        url = "http://localhost:11434/api/tags"
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = data.get("models", [])
            model_names = [m['name'] for m in models]
            
            if "gemma3:4b" in model_names:
                print("✅ Gemma3:4b disponible para análisis de imágenes")
                return True
            else:
                print("❌ Gemma3:4b NO encontrado")
                print(f"   Modelos disponibles: {model_names}")
                return False
    except Exception as e:
        print(f"❌ Error verificando modelos: {e}")
        return False


def test_hazmat_detection():
    """Prueba detección de HAZMAT (lógica sin IA)"""
    print("\n" + "="*60)
    print("TEST 4: DETECCIÓN HAZMAT (LÓGICA DETERMINÍSTICA)")
    print("="*60)
    
    HAZMAT_KEYWORDS = {
        "químicos", "fuga de gas", "incendio industrial", "tóxicos", "reactivos",
        "explosión", "derrame", "contaminación", "vapor tóxico", "sustancia peligrosa"
    }
    
    test_cases = [
        ("Fuga de gases tóxicos en Mamonal", True),
        ("Incendio industrial", True),
        ("Derrame de químicos", True),
        ("Accidente de tránsito", False),
        ("Robo en casa", False),
    ]
    
    all_pass = True
    for desc, expected in test_cases:
        lower_desc = desc.lower()
        detected = any(kw in lower_desc for kw in HAZMAT_KEYWORDS)
        status = "✅" if detected == expected else "❌"
        print(f"  {status} '{desc}' → HAZMAT={detected} (expected={expected})")
        all_pass = all_pass and (detected == expected)
    
    return all_pass


def test_location_detection():
    """Prueba detección de zona insular"""
    print("\n" + "="*60)
    print("TEST 5: DETECCIÓN ZONA INSULAR")
    print("="*60)
    
    def is_location_insular(lat: float, lng: float) -> bool:
        # Rango correcto del código del proyecto
        return (10.0 <= lat <= 10.28) and (-76.5 <= lng <= -75.55)
    
    test_cases = [
        (10.15, -76.15, "Islas del Rosario", True),
        (10.17, -75.78, "Barú", True),
        (10.18, -75.85, "Tierra Bomba", True),
        (10.3815, -75.5097, "Centro Histórico", False),
        (10.3750, -75.5500, "Getsemaní", False),
    ]
    
    all_pass = True
    for lat, lng, nombre, expected in test_cases:
        detected = is_location_insular(lat, lng)
        status = "✅" if detected == expected else "❌"
        print(f"  {status} {nombre} ({lat}, {lng}) → Insular={detected}")
        all_pass = all_pass and (detected == expected)
    
    return all_pass


def test_plan_candado():
    """Prueba cálculo de Plan Candado"""
    print("\n" + "="*60)
    print("TEST 6: PLAN CANDADO - RADIO DE HUIDA")
    print("="*60)
    
    def calculate_escape_radius_km(minutes_elapsed: int) -> float:
        # 30 km/h en zonas urbanas
        return (minutes_elapsed * 30.0) / 60.0
    
    test_cases = [
        (1, 0.5),
        (3, 1.5),
        (5, 2.5),
        (10, 5.0),
    ]
    
    all_pass = True
    for minutes, expected_km in test_cases:
        radius = calculate_escape_radius_km(minutes)
        tolerance = 0.01
        match = abs(radius - expected_km) < tolerance
        status = "✅" if match else "❌"
        print(f"  {status} {minutes} min → {radius:.2f} km (expected ~{expected_km} km)")
        all_pass = all_pass and match
    
    return all_pass


def main():
    """Ejecutar todos los tests"""
    print("\n" + "🚀 INICIANDO TESTS DE ORQUESTACIÓN - VERSIÓN ULTRA-RÁPIDA")
    print("="*60)
    
    tests = [
        ("Ollama Health", test_ollama_health),
        ("Generación de Texto", test_ollama_generate_text),
        ("Disponibilidad Gemma3", test_ollama_vision),
        ("Detección HAZMAT", test_hazmat_detection),
        ("Detección Insular", test_location_detection),
        ("Plan Candado", test_plan_candado),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"✅ PASADOS: {passed}/{total}\n")
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
    
    print("\n" + "="*60)
    if passed == total:
        print("🎉 TODOS LOS TESTS PASARON - ORQUESTACIÓN LISTA")
        print("="*60)
        print("\nProximos pasos:")
        print("  1. cd /home/toji/projects/emergencias-cartagena")
        print("  2. docker-compose up")
        print("  3. curl http://localhost:8000/docs")
        return True
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - REVISAR LOGS")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

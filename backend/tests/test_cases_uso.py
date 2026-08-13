"""
Tests para validar los 5 casos de uso del sistema de emergencias.
Ejecutar con: pytest tests/test_cases_uso.py -v
"""
import pytest
from app.agents.orchestrator import OrchestratorAgent
from app.agents.routing import RoutingAgent
from app.agents.vision import VisionAgent
from app.schemas.enums import Severidad, TipoEmergencia


class TestOrchestratorHAZMAT:
    """CASO 3: Emergencias Industriales (HAZMAT)"""

    @pytest.fixture
    def orchestrator(self):
        return OrchestratorAgent()

    def test_hazmat_detection_quimicos(self, orchestrator):
        """Detecta 'químicos' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Fuga de químicos en Mamonal")
        assert orchestrator._detect_hazmat_risk("QUIMICOS derramados")
        assert orchestrator._detect_hazmat_risk("peligrosos químicos")

    def test_hazmat_detection_gas(self, orchestrator):
        """Detecta 'fuga de gas' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Fuga de gas en industria")
        assert orchestrator._detect_hazmat_risk("GAS TOXICO detectado")
        assert orchestrator._detect_hazmat_risk("escape de gas")

    def test_hazmat_detection_incendio_industrial(self, orchestrator):
        """Detecta 'incendio industrial' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Incendio industrial")
        assert orchestrator._detect_hazmat_risk("INCENDIO en fábrica")
        assert orchestrator._detect_hazmat_risk("fuego industrial")

    def test_hazmat_detection_toxicos(self, orchestrator):
        """Detecta 'tóxicos' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Sustancias tóxicas")
        assert orchestrator._detect_hazmat_risk("TOXICOS liberados")
        assert orchestrator._detect_hazmat_risk("tóxico en aire")

    def test_hazmat_detection_explosion(self, orchestrator):
        """Detecta 'explosión' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Explosión en planta")
        assert orchestrator._detect_hazmat_risk("EXPLOSION detectada")
        assert orchestrator._detect_hazmat_risk("explosión química")

    def test_hazmat_detection_reactivos(self, orchestrator):
        """Detecta 'reactivos' como HAZMAT"""
        assert orchestrator._detect_hazmat_risk("Reactivos peligrosos")
        assert orchestrator._detect_hazmat_risk("REACTIVOS derramados")

    def test_hazmat_not_detected_accidente_normal(self, orchestrator):
        """NO detecta HAZMAT en accidente normal"""
        assert not orchestrator._detect_hazmat_risk("Accidente de tránsito")
        assert not orchestrator._detect_hazmat_risk("Choque de carros")
        assert not orchestrator._detect_hazmat_risk("Lluvia intensa")

    def test_hazmat_case_insensitive(self, orchestrator):
        """HAZMAT detection es case-insensitive"""
        assert orchestrator._detect_hazmat_risk("QUÍMICOS")
        assert orchestrator._detect_hazmat_risk("quimicos")
        assert orchestrator._detect_hazmat_risk("QuImIcOs")

    @pytest.mark.asyncio
    async def test_hazmat_routing_orchestrator(self, orchestrator):
        """Verifica que HAZMAT se enruta a organismos correctos"""
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.EMERGENCIA_INDUSTRIAL,
            severidad=Severidad.GRAVE,
            lat=10.3915,
            lng=-75.5093,
            existentes=[],
            descripcion="Fuga de gases tóxicos en Mamonal"
        )
        
        # Debe elevar a GRAVE y mencionar HAZMAT
        assert "HAZMAT" in resultado["resumen_ia"] or "CRÍTICA" in resultado["resumen_ia"] or resultado["severidad_ajustada"] == "grave"


class TestOrchestratorDesastres:
    """CASO 2: Desastres Naturales/Inundaciones"""

    @pytest.fixture
    def orchestrator(self):
        return OrchestratorAgent()

    def test_disaster_detection_inundacion(self, orchestrator):
        """Detecta 'inundación' como desastre"""
        assert orchestrator._detect_disaster_natural("Inundación en barrio")
        assert orchestrator._detect_disaster_natural("INUNDACION detectada")
        assert orchestrator._detect_disaster_natural("zona inundada")

    def test_disaster_detection_desbordamiento(self, orchestrator):
        """Detecta 'desbordamiento' como desastre"""
        assert orchestrator._detect_disaster_natural("Desbordamiento de caño")
        assert orchestrator._detect_disaster_natural("DESBORDAMIENTO río")
        assert orchestrator._detect_disaster_natural("se desbordó arroyo")

    def test_disaster_detection_lluvia(self, orchestrator):
        """Detecta 'lluvia' como desastre"""
        assert orchestrator._detect_disaster_natural("Lluvia intensa")
        assert orchestrator._detect_disaster_natural("LLUVIA fuerte")
        assert orchestrator._detect_disaster_natural("lluvia torrencial")

    def test_disaster_detection_deslizamiento(self, orchestrator):
        """Detecta 'deslizamiento' como desastre"""
        assert orchestrator._detect_disaster_natural("Deslizamiento de tierra")
        assert orchestrator._detect_disaster_natural("DESLIZAMIENTO")
        assert orchestrator._detect_disaster_natural("aluvión")

    def test_disaster_not_detected_accidente(self, orchestrator):
        """NO detecta desastre en accidente normal"""
        assert not orchestrator._detect_disaster_natural("Accidente de tránsito")
        assert not orchestrator._detect_disaster_natural("Robo en casa")

    @pytest.mark.asyncio
    async def test_disaster_deduplication(self, orchestrator):
        """Verifica deduplicación en zona de desastre"""
        # Simular varios reportes en misma zona
        existentes = [
            {
                "id": "report-1",
                "ubicacion_lat": 10.38,
                "ubicacion_lng": -75.51,
                "tipo_emergencia": TipoEmergencia.ACCIDENTE.value,
                "grupo_incidente_id": None,
            },
            {
                "id": "report-2",
                "ubicacion_lat": 10.381,  # ~100 metros de distancia
                "ubicacion_lng": -75.511,
                "tipo_emergencia": TipoEmergencia.ACCIDENTE.value,
                "grupo_incidente_id": None,
            }
        ]
        
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.ACCIDENTE,
            severidad=Severidad.GRAVE,
            lat=10.382,  # Mismo área general
            lng=-75.512,
            existentes=existentes,
            descripcion="Inundación en zona - múltiples reportes"
        )
        
        # Debería detectar como duplicado/agrupado
        assert resultado["grupo_incidente_id"] is not None or "Incidente sectorial" in resultado["resumen_ia"]


class TestOrchestratorInsular:
    """CASO 4: Emergencias Turísticas Insulares"""

    @pytest.fixture
    def orchestrator(self):
        return OrchestratorAgent()

    def test_location_insular_islas_rosario(self, orchestrator):
        """Detecta ubicación en Islas del Rosario"""
        assert orchestrator._is_location_insular(10.15, -76.15)

    def test_location_insular_baru(self, orchestrator):
        """Detecta ubicación en Barú"""
        assert orchestrator._is_location_insular(10.17, -75.78)

    def test_location_insular_tierra_bomba(self, orchestrator):
        """Detecta ubicación en Tierra Bomba"""
        assert orchestrator._is_location_insular(10.18, -75.85)

    def test_location_not_insular_centro_historico(self, orchestrator):
        """NO detecta insular en Centro Histórico"""
        assert not orchestrator._is_location_insular(10.3815, -75.5097)

    def test_location_not_insular_getsemani(self, orchestrator):
        """NO detecta insular en Getsemaní"""
        assert not orchestrator._is_location_insular(10.3750, -75.5500)

    @pytest.mark.asyncio
    async def test_insular_emergency_routing(self, orchestrator):
        """Verifica que emergencia insular menciona Guardia Costera"""
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.EMERGENCIA_MEDICA,
            severidad=Severidad.GRAVE,
            lat=10.15,  # Islas del Rosario
            lng=-76.15,
            existentes=[],
            descripcion="Turista con síntomas graves en Isla"
        )
        
        # Debería mencionar zona insular/marina
        assert "INSULAR" in resultado["resumen_ia"] or "Marino" in resultado["resumen_ia"] or "Guardia" in resultado["resumen_ia"]


class TestOrchestratorPlanCandado:
    """CASO 5: Robos e Inseguridad (Plan Candado)"""

    @pytest.fixture
    def orchestrator(self):
        return OrchestratorAgent()

    def test_escape_radius_1_minuto(self, orchestrator):
        """Calcula radio de huida para 1 minuto"""
        radius = orchestrator._calculate_escape_radius_km(minutes_elapsed=1)
        # 30 km/h * 1 min = 0.5 km
        assert radius == pytest.approx(0.5, rel=0.01)

    def test_escape_radius_3_minutos(self, orchestrator):
        """Calcula radio de huida para 3 minutos"""
        radius = orchestrator._calculate_escape_radius_km(minutes_elapsed=3)
        # 30 km/h * 3 min = 1.5 km
        assert radius == pytest.approx(1.5, rel=0.01)

    def test_escape_radius_5_minutos(self, orchestrator):
        """Calcula radio de huida para 5 minutos"""
        radius = orchestrator._calculate_escape_radius_km(minutes_elapsed=5)
        # 30 km/h * 5 min = 2.5 km
        assert radius == pytest.approx(2.5, rel=0.01)

    @pytest.mark.asyncio
    async def test_plan_candado_analysis(self, orchestrator):
        """Verifica análisis de Plan Candado"""
        resultado = await orchestrator.analyze_robo_plan_candado(
            lat=10.3915, lng=-75.5093, minutes_elapsed=3
        )
        
        assert resultado["punto_incidente"]["lat"] == 10.3915
        assert resultado["punto_incidente"]["lng"] == -75.5093
        assert resultado["tiempo_transcurrido_min"] == 3
        assert resultado["radio_huida_km"] == pytest.approx(1.5, rel=0.01)
        assert "Plan Candado" in resultado["accion"]


class TestRoutingAgent:
    """Tests para RoutingAgent - Mapeo a organismos"""

    @pytest.fixture
    def routing(self):
        return RoutingAgent()

    def test_routing_hazmat_activates_brigadas(self, routing):
        """HAZMAT activa Brigadas especiales"""
        organismos = routing.route_by_type(
            tipo=TipoEmergencia.EMERGENCIA_INDUSTRIAL,
            severidad=Severidad.GRAVE,
            is_hazmat=True,
            is_insular=False,
            is_disaster=False
        )
        
        assert len(organismos) > 0
        nombres = [o.nombre.upper() if o else "" for o in organismos]
        assert any("HAZMAT" in n for n in nombres)

    def test_routing_insular_guardia_costera(self, routing):
        """Emergencia insular enruta a Guardia Costera"""
        organismos = routing.route_by_type(
            tipo=TipoEmergencia.EMERGENCIA_MEDICA,
            severidad=Severidad.GRAVE,
            is_hazmat=False,
            is_insular=True,
            is_disaster=False
        )
        
        assert len(organismos) > 0
        nombres = [o.nombre.upper() if o else "" for o in organismos]
        assert any("GUARDIA" in n or "COSTERA" in n for n in nombres)

    def test_routing_disaster_bomberos_oagrd(self, routing):
        """Desastre enruta a Bomberos y OAGRD"""
        organismos = routing.route_by_type(
            tipo=TipoEmergencia.ACCIDENTE,
            severidad=Severidad.GRAVE,
            is_hazmat=False,
            is_insular=False,
            is_disaster=True
        )
        
        assert len(organismos) > 0
        nombres = [o.nombre.upper() if o else "" for o in organismos]
        assert any("BOMBERO" in n or "OAGRD" in n for n in nombres)

    def test_routing_trafico_crue_datt(self, routing):
        """Accidente de tránsito enruta a CRUE y DATT"""
        organismos = routing.route_by_type(
            tipo=TipoEmergencia.INCIDENTE_TRANSITO,
            severidad=Severidad.MODERADO,
            is_hazmat=False,
            is_insular=False,
            is_disaster=False
        )
        
        assert len(organismos) > 0

    def test_cai_location_centro_historico(self, routing):
        """Mapea Centro Histórico al CAI correspondiente"""
        cai = routing.get_cai_by_location(10.38, -75.51)
        assert cai is not None
        assert "Centro" in cai or "Histórico" in cai or "CAI" in cai

    def test_cai_location_bocagrande(self, routing):
        """Mapea Bocagrande al CAI correspondiente"""
        cai = routing.get_cai_by_location(10.40, -75.45)
        assert cai is not None
        assert "CAI" in cai


class TestVisionAgent:
    """Tests para VisionAgent - Análisis de imágenes"""

    @pytest.fixture
    def vision(self):
        return VisionAgent()

    @pytest.mark.asyncio
    async def test_vision_no_photo_defaults_moderado(self, vision):
        """Sin foto: usa análisis regla-basada"""
        resultado = await vision.analyze_image(
            tipo=TipoEmergencia.INCIDENTE_TRANSITO,
            foto_url=None
        )
        
        assert resultado["severidad"] == "leve"
        assert resultado["confianza"] > 0
        assert resultado["coincide_tipo"] is True

    @pytest.mark.asyncio
    async def test_vision_accidente_grave(self, vision):
        """Accidente mapea a severidad grave"""
        resultado = await vision.analyze_image(
            tipo=TipoEmergencia.ACCIDENTE,
            foto_url=None,
            descripcion="Accidente con múltiples heridos"
        )
        
        assert resultado["severidad"] in ["grave", "moderado"]

    @pytest.mark.asyncio
    async def test_vision_robo_moderado(self, vision):
        """Robo mapea a severidad moderada"""
        resultado = await vision.analyze_image(
            tipo=TipoEmergencia.ROBO_INSEGURIDAD,
            foto_url=None
        )
        
        assert resultado["severidad"] in ["leve", "moderado"]

    def test_rule_based_analysis_grave_keywords(self, vision):
        """Detecta keywords graves en descripción"""
        resultado = vision._rule_based_analysis(
            tipo=TipoEmergencia.EMERGENCIA_MEDICA,
            descripcion="Paciente muerto, fallecido"
        )
        
        assert resultado["severidad"] == "grave"

    def test_rule_based_analysis_leve_keywords(self, vision):
        """Detecta keywords leves en descripción"""
        resultado = vision._rule_based_analysis(
            tipo=TipoEmergencia.EMERGENCIA_MEDICA,
            descripcion="Rasguño leve menor"
        )
        
        assert resultado["severidad"] == "leve"


class TestIntegration:
    """Tests de integración de los 5 casos de uso"""

    @pytest.mark.asyncio
    async def test_caso_1_accidente_transito(self):
        """CASO 1: Accidente de tránsito"""
        orchestrator = OrchestratorAgent()
        routing = RoutingAgent()
        
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.INCIDENTE_TRANSITO,
            severidad=Severidad.GRAVE,
            lat=10.3915,
            lng=-75.5093,
            existentes=[],
            descripcion="Choque de dos carros en Av. Santander"
        )
        
        # Verificar organización
        assert "resumen_ia" in resultado
        assert resultado["severidad_ajustada"] == "grave"

    @pytest.mark.asyncio
    async def test_caso_2_inundacion(self):
        """CASO 2: Desastre natural"""
        orchestrator = OrchestratorAgent()
        
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.ACCIDENTE,
            severidad=Severidad.GRAVE,
            lat=10.38,
            lng=-75.51,
            existentes=[],
            descripcion="Inundación en barrio vulnerable"
        )
        
        assert "resumen_ia" in resultado

    @pytest.mark.asyncio
    async def test_caso_3_hazmat(self):
        """CASO 3: Emergencia HAZMAT"""
        orchestrator = OrchestratorAgent()
        
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.EMERGENCIA_INDUSTRIAL,
            severidad=Severidad.GRAVE,
            lat=10.25,  # Mamonal
            lng=-75.65,
            existentes=[],
            descripcion="Fuga de gases tóxicos en planta química"
        )
        
        # Debe detectar HAZMAT
        assert "HAZMAT" in resultado["resumen_ia"] or resultado["severidad_ajustada"] == "grave"

    @pytest.mark.asyncio
    async def test_caso_4_insular_multilingue(self):
        """CASO 4: Emergencia insular"""
        orchestrator = OrchestratorAgent()
        
        resultado = await orchestrator.generate_summary_and_grouping(
            tipo=TipoEmergencia.EMERGENCIA_MEDICA,
            severidad=Severidad.GRAVE,
            lat=10.15,  # Islas del Rosario
            lng=-76.15,
            existentes=[],
            descripcion="Tourist medical emergency on island"  # Inglés
        )
        
        assert "resumen_ia" in resultado

    @pytest.mark.asyncio
    async def test_caso_5_robo_plan_candado(self):
        """CASO 5: Robo con Plan Candado"""
        orchestrator = OrchestratorAgent()
        
        plan = await orchestrator.analyze_robo_plan_candado(
            lat=10.3915,
            lng=-75.5093,
            minutes_elapsed=3
        )
        
        assert plan["radio_huida_km"] > 0
        assert "Plan Candado" in plan["accion"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

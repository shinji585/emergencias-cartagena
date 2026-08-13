# 🚨 Análisis de Casos de Uso y Especificación del Agente IA

**Proyecto:** Sistema de Reporte de Emergencias de Cartagena con IA y Trazabilidad  
**Ubicación:** `emergencias-cartagena/`  
**Fecha:** 13 de Agosto de 2026  

---

## 📌 1. Visión General del Sistema y Objetivos del Agente IA

El sistema integra inteligencia artificial multimodal (visión por computador, procesamiento de lenguaje natural multilingüe, georreferenciación espacial y deduplicación de incidentes) para optimizar la atención de emergencias en Cartagena de Indias y sus zonas insulares. 

El agente actúa como un orquestador inteligente que clasifica, deduplica, traduce y despacha automáticamente las alertas a las centrales de riesgo y organismos de socorro competentes.

---

## 🚑 2. Punto 1: Accidentes de Tránsito, Intervención Médica y Gestión de Tráfico

### A. Notificación Automática a Centrales Médicas
* **Geolocalización e Intervención:** El agente analiza el accidente de tránsito y determina las coordenadas exactas de la escena.
* **Despacho a Red Hospitalaria:** Notifica de inmediato al **CRUE (Centro Regulador de Urgencias y Emergencias)** y a las clínicas/hospitales con servicio de urgencias más cercanos (ej. Hospital Universitario del Caribe, Clínica Madre Bernarda, Hospital Bocagrande).
* **Gestión de Ambulancias:** Envía la ficha de triage preliminar para el envío priorizado de ambulancias medicalizadas o básicas.

### B. Gestión Dinámica de Tráfico y Corredores de Emergencia
* **Detección de Ciudadanos en la Zona:** El agente identifica a conductores y personas navegando en un radio cercano al punto del accidente.
* **Generación de Rutas de Desvío:** Notifica desvíos y rutas alternativas en tiempo real para evitar la congestión en las avenidas principales (ej. Av. Pedro de Heredia, Av. Santander, Transversal 54).
* **Corredor de Emergencia Eficaz:** Al desviar el tráfico particular de manera anticipada, se garantiza que las ambulancias y vehículos de socorro lleguen a la escena sin bloqueos viales.

---

## 🌊 3. Punto 2: Desastres Naturales, Inundaciones y Emergencias Industriales

### A. Agente Multimodal en Desastres e Inundaciones
* **Procesamiento de Evidencia:** El agente analiza imágenes, videos y descripciones de zonas afectadas por inundaciones, desbordamiento de caños o arroyos en barrios vulnerables.
* **Notificación a Organismos de Socorro:** Envía las coordenadas exactas y el nivel de afectación al **Cuerpo Oficial de Bomberos** y a la **Oficina Asesora para la Gestión del Riesgo de Desastres (OAGRD)**.

### B. Agrupación Inteligente y Deduplicación de Alarmas
* **Fusión de Reportes Múltiples:** Cuando ocurren inundaciones o desastres de gran magnitud, decenas de ciudadanos envían reportes del mismo sector. El agente agrupa estos reportes por ventana espacio-temporal.
* **Prevención de Saturación:** Consolida múltiples alertas en una única **Ficha de Incidente Sectorial**, evitando duplicidad de alarmas y permitiendo a las autoridades movilizar maquinaria pesada de socorro (dragas, motobombas, retroexcavadoras) de forma ágil y coordinada.

### C. Emergencias Industriales y Materiales Peligrosos (HAZMAT)
* **Reconocimiento de Palabras Clave Críticas:** El agente escanea los reportes en busca de términos como *"químicos"*, *"fuga de gas"*, *"incendio industrial"*, *"tóxicos"*, *"reactivos"* o *"explosión"*.
* **Priorización HAZMAT:** Ante la presencia de estas palabras o evidencia visual en zonas como el Parque Industrial de Mamonal, el agente eleva la severidad a **CRÍTICA** e informa a las brigadas industriales y Bomberos especialistas en HAZMAT para una intervención inmediata antes de que afecte maquinarias de alto riesgo o poblados aledaños.

---

## 🏝️ 4. Punto 3: Emergencias Médicas Turísticas en Zona Insular (Multilingüe & Guardia Costera)

### A. Recepción y Traducción Multilingüe
* **Atención a Turistas Internacionales:** Procesamiento de solicitudes de auxilio en **inglés, francés, alemán** u otros idiomas en zonas insulares y turísticas de Cartagena (**Barú / Playa Blanca, Islas del Rosario, Tierra Bomba, Centro Histórico, Bocagrande**).
* **Traducción Automática de Sintomatología:** El agente interpreta los síntomas reportados por el visitante y los traduce al español en una ficha médica estandarizada para el personal asistencial local.

### B. Geolocalización Marítima y Enrutamiento Dual
* **Transmisión a la Guardia Costera:** En emergencias insulares o marítimas, transmite la posición GPS exacta a la **Guardia Costera de la Armada Nacional** para despliegue de lanchas de rescate rápido o evacuación médica marítima.
* **Coordinación con el CRUE:** Sincroniza la recepción de la víctima en el muelle en tierra firme con el **CRUE** para la espera de una ambulancia medicalizada.

---

## 👮 5. Punto 4: Robos e Inseguridad (Geolocalización, CAI y Cuadrante)

### A. Geolocalización e Identificación Espacial
* **Captura de Coordenadas:** Registro preciso del lugar donde ocurre o se presenciante un evento de hurto o inseguridad.

### B. Mapeo a CAI y Cuadrante Policial
* **Enrutamiento por Jurisdicción:** El agente ubica el **CAI (Centro de Atención Inmediata)** y el **Cuadrante de la Policía Nacional** correspondiente a la zona.
* **Plan Candado y Radio de Huida:** Calcula un radio proyectado de huida de los sospechosos en función del tiempo transcurrido (ej. 1 min = 500m; 3 min = 1.5 km en avenidas de escape), notificando a patrullas adyacentes para la ejecución del Plan Candado.

---

## 📋 6. Matriz Concreta de Casos de Uso del Agente IA

| # | Caso de Uso Concreto | Organismos / Entidades Receptores | Lógica e Inteligencia del Agente IA | Impacto Esperado |
|---|---|---|---|---|
| **1** | **Accidente Vial con Heridos** | CRUE, Hospitales Cercanos, DATT, Ciudadanos Cercanos | Enrutamiento a la red hospitalaria más cercana + Generación de desvíos de tráfico en tiempo real para conductores del sector | Liberación de un corredor de emergencia para la llegada rápida de ambulancias |
| **2** | **Inundación / Desastre Natural** | Bomberos, OAGRD, Maquinaria de Socorro | Geolocalización exacta + Agrupación y deduplicación automática de múltiples reportes en la misma zona | Elimina alarmas duplicadas y acelera el despliegue de maquinaria pesada de rescate |
| **3** | **Emergencia Industrial (HAZMAT)** | Bomberos HAZMAT, Brigadas Mamonal | NLP para detección de keywords (*químicos, incendio industrial, gas*) + Alerta de máxima prioridad | Reducción del tiempo de respuesta ante riesgos químicos e industriales de gran escala |
| **4** | **Emergencia Turística Insular** | Guardia Costera (Armada Nacional), CRUE | Traducción multilingüe (Inglés -> Español) + Diagnóstico preliminar + Geolocalización insular | Evacuación marítima y médica oportuna en Barú y las Islas del Rosario |
| **5** | **Robo / Inseguridad Ciudadana** | CAI más cercano, Cuadrante de Policía | Mapeo automático de cuadrante + Proyección de radio de huida (Plan Candado) | Reacción policial inmediata y cierre estratégico de vías de escape |

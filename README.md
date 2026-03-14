# CloudArquitecto — Strands Agent

Agente conversacional de AWS construido con [Strands Agents](https://strandsagents.com). Responde preguntas sobre costos, arquitecturas y servicios de AWS en español.

## Instalación y uso

1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales
   ```

4. Ejecutar el agente:
   ```bash
   python agent.py
   ```

## Herramientas disponibles

### `estimar_costo_lambda`
Calcula el costo mensual estimado de AWS Lambda usando los precios estándar (invocaciones + cómputo en GB-segundos), descontando el free tier.

**Ejemplos de preguntas:**
- "¿Cuánto me costaría una Lambda con 5 millones de invocaciones, 200ms de duración y 512MB de memoria?"
- "Estima el costo mensual de una función Lambda que se ejecuta 10 millones de veces con 100ms y 128MB."
- "¿Cuál sería el costo de Lambda con 500k invocaciones al mes, 1 segundo de duración y 1024MB?"

---

### `recomendar_arquitectura`
Devuelve una arquitectura AWS recomendada según el caso de uso: `api_rest`, `streaming`, `ml_inference`, `static_web` o `batch`.

**Ejemplos de preguntas:**
- "¿Qué arquitectura AWS me recomiendas para construir una API REST?"
- "Necesito procesar datos en tiempo real, ¿qué servicios AWS uso?"
- "¿Cómo despliego un sitio web estático en AWS?"

---

### `buscar_servicio_aws`
Lista los principales servicios de AWS agrupados por categoría: `compute`, `storage`, `database`, `ai` o `networking`.

**Ejemplos de preguntas:**
- "¿Qué servicios de cómputo tiene AWS?"
- "Muéstrame los servicios de base de datos disponibles en AWS."
- "¿Qué opciones de inteligencia artificial ofrece AWS?"

---

### `comparar_instancias_ec2`
Compara dos tipos de instancia EC2 mostrando vCPUs, RAM y precio aproximado por hora (región us-east-1, Linux, On-Demand). Soporta familias t3, t3a, m5, m6i, c5, c6i, r5 y r6i.

**Ejemplos de preguntas:**
- "¿Cuál es la diferencia entre una t3.micro y una t3.small?"
- "Compara las instancias m5.xlarge y c5.xlarge."
- "¿Qué me conviene más, una r5.large o una m6i.large?"

---

### `calculator`
Realiza operaciones matemáticas y cálculos numéricos.

**Ejemplos de preguntas:**
- "¿Cuánto es 15% de $3,200?"
- "Calcula 1024 multiplicado por 730."
- "¿Cuántos GB-segundos son 2 millones de invocaciones de 300ms con 256MB?"

---

### `current_time`
Obtiene la fecha y hora actual.

**Ejemplos de preguntas:**
- "¿Qué hora es ahora?"
- "¿Cuál es la fecha de hoy?"
- "Dime la hora actual."

## Estructura del proyecto

```
.
├── agent.py          # Definición del agente y punto de entrada
├── tools.py          # Herramientas personalizadas de AWS
├── requirements.txt  # Dependencias Python
├── .env.example      # Plantilla de variables de entorno
└── README.md
```

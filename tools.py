from strands import tool


@tool
def estimar_costo_lambda(
    invocaciones: int,
    duracion_ms: float,
    memoria_mb: int
) -> str:
    """
    Calcula el costo mensual estimado de AWS Lambda.

    Usa los precios estándar de AWS Lambda:
    - Primeros 1M de invocaciones gratis, luego $0.20 por millón.
    - Cómputo: $0.0000166667 por GB-segundo (después del free tier de 400,000 GB-s).

    Args:
        invocaciones: Número total de invocaciones al mes.
        duracion_ms: Duración promedio de cada invocación en milisegundos.
        memoria_mb: Memoria asignada a la función en MB.

    Returns:
        Resumen del costo mensual estimado en USD.
    """
    PRECIO_POR_MILLON_INVOCACIONES = 0.20
    PRECIO_POR_GB_SEGUNDO = 0.0000166667
    FREE_TIER_INVOCACIONES = 1_000_000
    FREE_TIER_GB_SEGUNDOS = 400_000

    # Costo por invocaciones
    invocaciones_facturables = max(0, invocaciones - FREE_TIER_INVOCACIONES)
    costo_invocaciones = (invocaciones_facturables / 1_000_000) * PRECIO_POR_MILLON_INVOCACIONES

    # Costo por cómputo (GB-segundos)
    duracion_s = duracion_ms / 1000
    memoria_gb = memoria_mb / 1024
    gb_segundos_total = invocaciones * duracion_s * memoria_gb
    gb_segundos_facturables = max(0, gb_segundos_total - FREE_TIER_GB_SEGUNDOS)
    costo_computo = gb_segundos_facturables * PRECIO_POR_GB_SEGUNDO

    costo_total = costo_invocaciones + costo_computo

    return (
        f"Estimación mensual para AWS Lambda:\n"
        f"  - Invocaciones: {invocaciones:,}\n"
        f"  - Duración promedio: {duracion_ms} ms\n"
        f"  - Memoria: {memoria_mb} MB\n"
        f"  - GB-segundos consumidos: {gb_segundos_total:,.2f}\n"
        f"  - Costo por invocaciones: ${costo_invocaciones:.4f}\n"
        f"  - Costo por cómputo: ${costo_computo:.4f}\n"
        f"  - COSTO TOTAL ESTIMADO: ${costo_total:.4f} USD/mes"
    )


@tool
def recomendar_arquitectura(caso_de_uso: str) -> str:
    """
    Devuelve una arquitectura AWS recomendada según el caso de uso indicado.

    Casos de uso soportados:
    - api_rest: APIs RESTful con baja latencia.
    - streaming: Procesamiento de datos en tiempo real.
    - ml_inference: Inferencia de modelos de machine learning.
    - static_web: Sitios web estáticos o SPAs.
    - batch: Procesamiento por lotes de grandes volúmenes de datos.

    Args:
        caso_de_uso: Tipo de carga de trabajo. Valores válidos:
                     'api_rest', 'streaming', 'ml_inference', 'static_web', 'batch'.

    Returns:
        Descripción de la arquitectura recomendada con los servicios AWS sugeridos.
    """
    arquitecturas = {
        "api_rest": (
            "Arquitectura recomendada para API REST:\n"
            "  - Amazon API Gateway (gestión de endpoints y throttling)\n"
            "  - AWS Lambda (lógica de negocio serverless)\n"
            "  - Amazon DynamoDB (base de datos NoSQL de baja latencia)\n"
            "  - Amazon Cognito (autenticación y autorización)\n"
            "  - AWS WAF (protección contra ataques web)\n"
            "  Patrón: API Gateway → Lambda → DynamoDB"
        ),
        "streaming": (
            "Arquitectura recomendada para Streaming:\n"
            "  - Amazon Kinesis Data Streams (ingesta de eventos en tiempo real)\n"
            "  - AWS Lambda o Amazon Kinesis Data Analytics (procesamiento)\n"
            "  - Amazon S3 (almacenamiento de datos procesados)\n"
            "  - Amazon OpenSearch Service (búsqueda y visualización)\n"
            "  - Amazon CloudWatch (monitoreo de pipelines)\n"
            "  Patrón: Kinesis Streams → Lambda/KDA → S3 + OpenSearch"
        ),
        "ml_inference": (
            "Arquitectura recomendada para ML Inference:\n"
            "  - Amazon SageMaker Endpoints (despliegue de modelos)\n"
            "  - AWS Lambda (preprocesamiento y orquestación)\n"
            "  - Amazon API Gateway (exposición del endpoint de inferencia)\n"
            "  - Amazon S3 (almacenamiento de modelos y artefactos)\n"
            "  - Amazon CloudWatch (métricas de latencia y errores)\n"
            "  Patrón: API Gateway → Lambda → SageMaker Endpoint"
        ),
        "static_web": (
            "Arquitectura recomendada para Sitio Web Estático:\n"
            "  - Amazon S3 (almacenamiento de archivos estáticos)\n"
            "  - Amazon CloudFront (CDN global con baja latencia)\n"
            "  - AWS Certificate Manager (certificado SSL/TLS gratuito)\n"
            "  - Amazon Route 53 (DNS y dominio personalizado)\n"
            "  - AWS WAF (protección opcional contra bots)\n"
            "  Patrón: Route 53 → CloudFront → S3"
        ),
        "batch": (
            "Arquitectura recomendada para Procesamiento Batch:\n"
            "  - AWS Batch (orquestación de trabajos por lotes)\n"
            "  - Amazon S3 (entrada y salida de datos)\n"
            "  - AWS Step Functions (coordinación de flujos de trabajo)\n"
            "  - Amazon ECR (imágenes Docker de los jobs)\n"
            "  - Amazon CloudWatch Events (programación de ejecuciones)\n"
            "  Patrón: EventBridge → Step Functions → AWS Batch → S3"
        ),
    }

    caso = caso_de_uso.lower().strip()
    if caso not in arquitecturas:
        casos_validos = ", ".join(arquitecturas.keys())
        return f"Caso de uso '{caso_de_uso}' no reconocido. Opciones válidas: {casos_validos}."

    return arquitecturas[caso]


@tool
def buscar_servicio_aws(categoria: str) -> str:
    """
    Lista los principales servicios de AWS agrupados por categoría.

    Categorías disponibles:
    - compute: Servicios de cómputo (servidores, contenedores, serverless).
    - storage: Servicios de almacenamiento de objetos, bloques y archivos.
    - database: Bases de datos relacionales, NoSQL, caché y más.
    - ai: Servicios de inteligencia artificial y machine learning.
    - networking: Servicios de red, DNS, CDN y conectividad.

    Args:
        categoria: Categoría de servicios a consultar. Valores válidos:
                   'compute', 'storage', 'database', 'ai', 'networking'.

    Returns:
        Lista de servicios AWS de la categoría solicitada con una breve descripción.
    """
    servicios = {
        "compute": [
            ("Amazon EC2", "Máquinas virtuales escalables en la nube"),
            ("AWS Lambda", "Funciones serverless sin gestión de servidores"),
            ("Amazon ECS", "Orquestación de contenedores Docker"),
            ("Amazon EKS", "Kubernetes gestionado en AWS"),
            ("AWS Fargate", "Cómputo serverless para contenedores"),
            ("AWS Elastic Beanstalk", "Despliegue y escalado automático de aplicaciones"),
            ("Amazon Lightsail", "Servidores virtuales simples y económicos"),
        ],
        "storage": [
            ("Amazon S3", "Almacenamiento de objetos altamente duradero"),
            ("Amazon EBS", "Volúmenes de bloques para instancias EC2"),
            ("Amazon EFS", "Sistema de archivos NFS gestionado y elástico"),
            ("AWS Storage Gateway", "Integración de almacenamiento on-premises con la nube"),
            ("Amazon S3 Glacier", "Archivado de datos de bajo costo a largo plazo"),
            ("AWS Backup", "Servicio centralizado de copias de seguridad"),
        ],
        "database": [
            ("Amazon RDS", "Bases de datos relacionales gestionadas (MySQL, PostgreSQL, etc.)"),
            ("Amazon Aurora", "Base de datos relacional compatible con MySQL/PostgreSQL de alto rendimiento"),
            ("Amazon DynamoDB", "Base de datos NoSQL clave-valor de latencia en milisegundos"),
            ("Amazon ElastiCache", "Caché en memoria con Redis o Memcached"),
            ("Amazon Redshift", "Data warehouse para análisis a escala de petabytes"),
            ("Amazon DocumentDB", "Base de datos de documentos compatible con MongoDB"),
            ("Amazon Neptune", "Base de datos de grafos gestionada"),
        ],
        "ai": [
            ("Amazon Bedrock", "Modelos fundacionales de IA generativa como API"),
            ("Amazon SageMaker", "Plataforma completa para entrenar y desplegar modelos ML"),
            ("Amazon Rekognition", "Análisis de imágenes y videos con visión artificial"),
            ("Amazon Comprehend", "Procesamiento de lenguaje natural (NLP)"),
            ("Amazon Polly", "Conversión de texto a voz realista"),
            ("Amazon Transcribe", "Transcripción automática de audio a texto"),
            ("Amazon Translate", "Traducción automática de idiomas"),
            ("Amazon Lex", "Creación de chatbots conversacionales"),
        ],
        "networking": [
            ("Amazon VPC", "Red privada virtual aislada en la nube"),
            ("Amazon CloudFront", "CDN global para entrega de contenido con baja latencia"),
            ("Amazon Route 53", "DNS escalable y registro de dominios"),
            ("AWS Direct Connect", "Conexión dedicada entre on-premises y AWS"),
            ("AWS Transit Gateway", "Hub central para conectar múltiples VPCs"),
            ("Elastic Load Balancing", "Distribución de tráfico entre instancias"),
            ("AWS PrivateLink", "Acceso privado a servicios sin exponer tráfico a internet"),
        ],
    }

    cat = categoria.lower().strip()
    if cat not in servicios:
        categorias_validas = ", ".join(servicios.keys())
        return f"Categoría '{categoria}' no reconocida. Opciones válidas: {categorias_validas}."

    lista = servicios[cat]
    resultado = f"Servicios AWS en la categoría '{cat}':\n"
    for nombre, descripcion in lista:
        resultado += f"  - {nombre}: {descripcion}\n"
    return resultado.strip()


@tool
def comparar_instancias_ec2(instancia_1: str, instancia_2: str) -> str:
    """
    Compara dos tipos de instancia EC2 mostrando vCPUs, RAM y precio aproximado por hora.

    Incluye instancias de las familias t3, t3a, m5, m6i, c5, c6i, r5 y r6i.
    Los precios son aproximados para la región us-east-1 (Linux, On-Demand).

    Args:
        instancia_1: Primer tipo de instancia EC2 (ej: 't3.micro').
        instancia_2: Segundo tipo de instancia EC2 (ej: 't3.small').

    Returns:
        Tabla comparativa con vCPUs, RAM y precio por hora de ambas instancias.
    """
    # vcpus, ram_gb, precio_usd_hora
    INSTANCIAS: dict[str, tuple[int, float, float]] = {
        "t3.nano":     (2,   0.5,   0.0052),
        "t3.micro":    (2,   1.0,   0.0104),
        "t3.small":    (2,   2.0,   0.0208),
        "t3.medium":   (2,   4.0,   0.0416),
        "t3.large":    (2,   8.0,   0.0832),
        "t3.xlarge":   (4,  16.0,   0.1664),
        "t3.2xlarge":  (8,  32.0,   0.3328),
        "t3a.nano":    (2,   0.5,   0.0047),
        "t3a.micro":   (2,   1.0,   0.0094),
        "t3a.small":   (2,   2.0,   0.0188),
        "t3a.medium":  (2,   4.0,   0.0376),
        "t3a.large":   (2,   8.0,   0.0752),
        "t3a.xlarge":  (4,  16.0,   0.1504),
        "t3a.2xlarge": (8,  32.0,   0.3008),
        "m5.large":    (2,   8.0,   0.0960),
        "m5.xlarge":   (4,  16.0,   0.1920),
        "m5.2xlarge":  (8,  32.0,   0.3840),
        "m5.4xlarge":  (16, 64.0,   0.7680),
        "m6i.large":   (2,   8.0,   0.0960),
        "m6i.xlarge":  (4,  16.0,   0.1920),
        "m6i.2xlarge": (8,  32.0,   0.3840),
        "m6i.4xlarge": (16, 64.0,   0.7680),
        "c5.large":    (2,   4.0,   0.0850),
        "c5.xlarge":   (4,   8.0,   0.1700),
        "c5.2xlarge":  (8,  16.0,   0.3400),
        "c5.4xlarge":  (16, 32.0,   0.6800),
        "c6i.large":   (2,   4.0,   0.0850),
        "c6i.xlarge":  (4,   8.0,   0.1700),
        "c6i.2xlarge": (8,  16.0,   0.3400),
        "c6i.4xlarge": (16, 32.0,   0.6800),
        "r5.large":    (2,  16.0,   0.1260),
        "r5.xlarge":   (4,  32.0,   0.2520),
        "r5.2xlarge":  (8,  64.0,   0.5040),
        "r5.4xlarge":  (16, 128.0,  1.0080),
        "r6i.large":   (2,  16.0,   0.1260),
        "r6i.xlarge":  (4,  32.0,   0.2520),
        "r6i.2xlarge": (8,  64.0,   0.5040),
        "r6i.4xlarge": (16, 128.0,  1.0080),
    }

    i1 = instancia_1.lower().strip()
    i2 = instancia_2.lower().strip()

    errores = []
    if i1 not in INSTANCIAS:
        errores.append(f"'{instancia_1}' no reconocida.")
    if i2 not in INSTANCIAS:
        errores.append(f"'{instancia_2}' no reconocida.")
    if errores:
        tipos_validos = ", ".join(sorted(INSTANCIAS.keys()))
        return (
            f"Instancia(s) no reconocida(s): {' '.join(errores)}\n"
            f"Tipos disponibles: {tipos_validos}"
        )

    vcpus1, ram1, precio1 = INSTANCIAS[i1]
    vcpus2, ram2, precio2 = INSTANCIAS[i2]

    def diferencia(v1: float, v2: float) -> str:
        if v1 == v2:
            return "igual"
        pct = abs(v1 - v2) / min(v1, v2) * 100
        mayor = i1 if v1 > v2 else i2
        return f"{mayor} es {pct:.0f}% mayor"

    return (
        f"Comparación EC2: {i1} vs {i2}\n"
        f"{'Característica':<20} {'':>2} {i1:<15} {i2:<15}\n"
        f"{'-'*55}\n"
        f"{'vCPUs':<20} {'':>2} {vcpus1:<15} {vcpus2:<15}  ({diferencia(vcpus1, vcpus2)})\n"
        f"{'RAM (GB)':<20} {'':>2} {ram1:<15} {ram2:<15}  ({diferencia(ram1, ram2)})\n"
        f"{'Precio/hora (USD)':<20} {'':>2} ${precio1:<14.4f} ${precio2:<14.4f}  ({diferencia(precio1, precio2)})\n"
        f"\n"
        f"Costo mensual estimado (730 h):\n"
        f"  {i1}: ${precio1 * 730:.2f} USD\n"
        f"  {i2}: ${precio2 * 730:.2f} USD"
    )

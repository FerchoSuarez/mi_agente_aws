from strands import Agent
from strands_tools import calculator, current_time
# Importamos las 4 herramientas de tu archivo tools.py
from tools import (
    estimar_costo_lambda, 
    recomendar_arquitectura, 
    buscar_servicio_aws, 
    comparar_instancias_ec2
)

SYSTEM_PROMPT = """
Eres CloudArquitecto, un experto senior en AWS.
Tu objetivo es ayudar a los usuarios con:
1. Estimación de costos de Lambda.
2. Recomendación de arquitecturas probadas.
3. Información detallada de servicios por categoría.
4. Comparación técnica y económica de instancias EC2.

Responde siempre en español, de forma profesional y usa las herramientas disponibles.
"""

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[
        estimar_costo_lambda, 
        recomendar_arquitectura, 
        buscar_servicio_aws, 
        comparar_instancias_ec2, # Nueva herramienta agregada
        calculator, 
        current_time
    ]
)

print("=== CloudArquitecto: Agente AWS Listo ===")
while True:
    user_input = input("Tu: ").strip()
    if user_input.lower() == "salir": break
    print("\nRespuesta:")
    agent(user_input)
    print()
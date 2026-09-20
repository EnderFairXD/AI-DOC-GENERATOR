import os
import json
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

load_dotenv()

def generate_readme(raw_code: str, structured_data: dict) -> str:
    """Pide a Llama 3.1 que genere un README profesional con diagramas Mermaid."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    llm = Ollama(
        base_url=base_url,
        model="llama3.1",
        temperature=0.2, # Al nivel de temperatura bajo, es más estructurado y técnico
        num_ctx=8192
    )
    
    template = """
    Eres un Ingeniero de Software Principal y experto en Arquitectura Técnica. Tu tarea es generar un archivo README.md técnico e impecable en español basado en el análisis de este código fuente.

    Estructura analizada del código (en formato JSON):
    {datos_estructurados}

    Código fuente original:
    ```python
    {codigo_original}
    ```

    Debes generar un documento Markdown con las siguientes secciones obligatorias:
    1. 🚀 **Descripción General**: Explicación clara y concisa de qué resuelve este código y su propósito arquitectónico.
    2. 📊 **Diagrama de Flujo / Arquitectura**: Genera un diagrama de bloques o de flujo utilizando la sintaxis nativa de **Mermaid.js** (encapsulado ÚNICAMENTE dentro de un bloque ```mermaid ... ```). El diagrama debe explicar visualmente cómo interactúan las funciones o cómo fluyen los datos.
    3. 🛠️ **Explicación Detallada de Componentes**: Desglosa las funciones y clases basándote en los datos estructurados proporcionados. Explica qué hace cada parámetro.
    4. 💡 **Ejemplo de Integración**: Escribe un bloque de código de ejemplo que demuestre cómo otro desarrollador debería importar y usar este archivo en el mundo real.

    Escribe la documentación de forma profesional, clara y directa.
    """
    
    prompt = PromptTemplate(
        input_variables=["datos_estructurados", "codigo_original"],
        template=template
    )
    
    chain = prompt | llm
    
    # Convertimos el diccionario de AST a string JSON bonito para que el LLM lo entienda mejor
    json_data = json.dumps(structured_data, indent=2)
    
    return chain.invoke({
        "datos_estructurados": json_data,
        "codigo_original": raw_code
    })
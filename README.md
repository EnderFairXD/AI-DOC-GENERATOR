# Generador Técnico de Documentación AI

Una aplicación web que utiliza parsing AST (Abstract Syntax Tree) para realizar ingeniería inversa en código Python y genera automáticamente archivos `README.md` técnicos con diagramas de flujo integrados (Mermaid.js). Todo procesado de forma local y privada usando Ollama (Llama 3.1).

## Requisitos Previos
1. Instalar [Python 3.9+](https://www.python.org/)
2. Instalar y ejecutar [Ollama](https://ollama.com/) localmente.
3. Descargar el modelo ejecutando en terminal: `ollama run llama3.1`

## Instalación
1. Clona el repositorio: `git clone <tu-enlace-github>`
2. Crea y activa el entorno virtual:
   * `python -m venv .venv`
   * Mac/Linux: `source .venv/bin/activate` 
   * Windows: `.venv\Scripts\activate`
3. Instala dependencias: `pip install -r requirements.txt`
4. Copia las variables de entorno: `cp .env.example .env`
5. Arranca el servidor: `streamlit run src/main.py`
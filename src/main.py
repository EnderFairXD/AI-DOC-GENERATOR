import streamlit as st
from utils.code_parser import analyze_python_code
from services.doc_service import generate_readme

st.set_page_config(page_title="AI Doc Generator", page_icon="📝", layout="wide")

st.title("📝 Generador Técnico de Documentación (AI)")
st.markdown("Analiza la arquitectura de tu código local mediante AST y genera READMEs con diagramas integrados de forma privada.")

# Ofrecer dos opciones: Subir archivo o pegar texto
modo = st.radio("Selecciona método de entrada:", ["Pegar código en texto", "Subir archivo .py"])
codigo_fuente = ""

if modo == "Pegar código en texto":
    codigo_fuente = st.text_area("Pega tu código Python aquí:", height=250, placeholder="def mi_funcion()...")
else:
    uploaded_file = st.file_uploader("Sube tu archivo de Python (.py)", type="py")
    if uploaded_file is not None:
        codigo_fuente = uploaded_file.read().decode("utf-8")
        st.success("Archivo cargado correctamente.")

if codigo_fuente:
    if st.button("🚀 Generar Documentación Técnica"):
        with st.status("Procesando ingeniería inversa del código...", expanded=True) as status:
            try:
                # Paso 1: Realizar el Parsing con AST
                status.write("Ejecutando Parser AST (Analizando funciones, clases y firmas)...")
                datos_arquitectura = analyze_python_code(codigo_fuente)
                
                if "error" in datos_arquitectura:
                    status.update(label="Error de sintaxis", state="error")
                    st.error(datos_arquitectura["error"])
                else:
                    # Paso 2: Enviar al Servidor Local
                    status.write("Estructura extraída con éxito. Enviando mapa sintáctico a Llama 3.1 en CasaOS...")
                    readme_final = generate_readme(codigo_fuente, datos_arquitectura)
                    
                    status.update(label="¡README.md e ingeniería de diagramas completada!", state="complete")
                    
                    st.markdown("---")
                    st.subheader("📋 Archivo README.md Generado")
                    
                    # Botón para descargar el archivo resultante listo para Git
                    st.download_button(
                        label="💾 Descargar README.md",
                        data=readme_final,
                        file_name="README.md",
                        mime="text/markdown"
                    )
                    
                    # Mostrar la documentación renderizada en pantalla
                    st.markdown(readme_final)
                    
            except Exception as e:
                status.update(label="Error en el proceso", state="error")
                st.error(f"Error del sistema: {str(e)}")
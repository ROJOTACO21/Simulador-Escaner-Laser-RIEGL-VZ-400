import streamlit as st
import math

# Configuración de la página
st.set_page_config(page_title="Simulador Escáner Láser RIEGL VZ-400", layout="wide")

# Función para formatear números según especificaciones
def formato_numero(valor, decimales=2):
    """
    Formatea números con comas para decimales y puntos para miles
    Ejemplo: 8250.25 -> 8.250,25
    """
    if valor == 0:
        return "0"
    
    # Separar parte entera y decimal
    parte_entera = int(valor)
    parte_decimal = round(valor - parte_entera, decimales)
    
    # Formatear parte entera con separadores de miles
    parte_entera_str = f"{parte_entera:,}".replace(",", ".")
    
    # Formatear parte decimal si existe
    if parte_decimal > 0:
        parte_decimal_str = f"{parte_decimal:.{decimales}f}".split('.')[1]
        return f"{parte_entera_str},{parte_decimal_str}"
    else:
        return parte_entera_str

# Título principal
st.title("Simulador Escáner Láser RIEGL VZ-400 - Preparación de Levantamiento")
st.write("Este simulador te guiará paso a paso para definir los parámetros de un levantamiento con el patrón de levantamiento Rectangular Field of View (FOV).")

# Crear layout de 3 columnas
col1, col2, col3 = st.columns([1, 1, 1])

# Columna 1: Introducción y Paso 2 (PHI SOCS)
with col1:
    # ---------------------------
    # Paso 1 - Bienvenida
    # ---------------------------
    st.header("Paso 1: Introducción")
    st.write("""
    En este asistente podrás definir los siguientes parámetros:
    1. **PHI SOCS (ángulo horizontal)**
    2. **THETA SOCS (ángulo vertical)**
    3. **Frecuencia del láser**
    """)
    st.image("IMA/gif_intro.gif", caption="Vista general del escaneo", use_container_width=True)
    
    # ---------------------------
    # Paso 2 - PHI SOCS
    # ---------------------------
    st.header("Paso 2: Parámetros PHI SOCS (Ángulo de línea - φ)")
    
    # Modificado: solo números enteros para start y stop angles
    phi_start = st.number_input("Start angle (°)", min_value=0, max_value=360, value=0, step=1, key="phi_start", format="%d")
    phi_stop = st.number_input("Stop angle (°)", min_value=0, max_value=360, value=180, step=1, key="phi_stop", format="%d")
    phi_inc = st.number_input("Increment Δφ (°)", min_value=0.0024, max_value=0.5, value=0.05, step=0.001, format="%.4f", key="phi_inc")
    
    st.image("IMA/vista planta.gif", caption="Movimiento horizontal del escaneo", use_container_width=True)
    
    if phi_start >= phi_stop:
        st.error("⚠️ El Start angle debe ser menor que el Stop angle.")

# Columna 2: Paso 3 y Paso 4
with col2:
    # ---------------------------
    # Paso 3 - THETA SOCS
    # ---------------------------
    st.header("Paso 3: Parámetros THETA SOCS (Ángulo de marco - θ)")
    
    # Modificado: solo números enteros para start y stop angles
    theta_start = st.number_input("Start angle (°)", min_value=30, max_value=130, value=30, step=1, key="theta_start", format="%d")
    theta_stop = st.number_input("Stop angle (°)", min_value=30, max_value=130, value=100, step=1, key="theta_stop", format="%d")
    theta_inc = st.number_input("Increment Δθ (°)", min_value=0.0024, max_value=0.288, value=0.05, step=0.001, format="%.4f", key="theta_inc")
    
    if theta_start >= theta_stop:
        st.error("⚠️ El Start angle debe ser menor que el Stop angle.")
    
    # Verificar si los incrementos son iguales
    incrementos_iguales = abs(phi_inc - theta_inc) < 0.0001  # Tolerancia para comparación de floats
    
    if not incrementos_iguales:
        st.error("⚠️ El Increment de THETA y PHI deben ser iguales para una nube de puntos uniforme.")
    
    # ---------------------------
    # Paso 4 - Frecuencia del láser
    # ---------------------------
    st.header("Paso 4: Frecuencia del escáner")
    st.markdown("Seleccione la frecuencia del pulso láser permitida para el Riegl VZ-400.")
    
    # Selector de frecuencia (solo dos opciones)
    frecuencia = st.radio(
        "Frecuencia del pulso láser:",
        options=[100_000, 300_000],
        format_func=lambda x: f"{x/1000:.0f} kHz",
        key="frecuencia"
    )
    
    # Mostrar imagen con pie de figura
    st.image(
        "IMA/ESP.png",
        caption="Figura 1. Especificaciones técnicas del Riegl VZ-400 – Frecuencia del pulso láser",
        use_container_width=True
    )
    
    st.write(f"**Frecuencia seleccionada:** {frecuencia/1000:.0f} kHz")

# Columna 3: Fórmulas y Resultados
with col3:
    # ---------------------------
    # Paso 5 - Cálculo de parámetros de rendimiento
    # ---------------------------
    st.header("Paso 5: Cálculo de parámetros de rendimiento")
    
    # Sección de parámetros de entrada (resumen)
    st.subheader("📋 Parámetros de Entrada")
    
    # Mejorar la estética con columnas y formato mejorado
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        st.markdown("**PHI SOCS**")
        st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
                   f"<b>Start:</b> {formato_numero(phi_start, 0)}°<br>"
                   f"<b>Stop:</b> {formato_numero(phi_stop, 0)}°<br>"
                   f"<b>Δφ:</b> {formato_numero(phi_inc, 4)}°</div>", 
                   unsafe_allow_html=True)
        
    with input_col2:
        st.markdown("**THETA SOCS**")
        st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
                   f"<b>Start:</b> {formato_numero(theta_start, 0)}°<br>"
                   f"<b>Stop:</b> {formato_numero(theta_stop, 0)}°<br>"
                   f"<b>Δθ:</b> {formato_numero(theta_inc, 4)}°</div>", 
                   unsafe_allow_html=True)
        
        st.markdown("**Frecuencia**")
        st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px;'>"
                   f"<b>Valor:</b> {frecuencia/1000:.0f} kHz</div>", 
                   unsafe_allow_html=True)
    
    # Verificar si se pueden realizar los cálculos
    if phi_start >= phi_stop or theta_start >= theta_stop or not incrementos_iguales:
        st.error("No se pueden calcular los resultados debido a errores en los parámetros de entrada.")
    else:
        # Cálculos (se ejecutan automáticamente cuando cambia cualquier variable)
        theta_total = theta_stop - theta_start  # [°]
        
        # Ajuste de N según la frecuencia seleccionada
        if frecuencia == 100_000:
            N = 34  # líneas/s para 100 kHz
        else:
            N = 100  # líneas/s para 300 kHz
            
        M = theta_total / theta_inc  # puntos/línea
        P = M * N  # puntos/s
        Vb = phi_inc * N  # °/s
        phi_total = phi_stop - phi_start  # rango horizontal en °
        T = phi_total / Vb  # s
        PT = P * T  # puntos totales
        
        # Aproximar T al entero mayor más cercano
        T_redondeado = math.ceil(T)
        
        # Mostrar fórmulas
        st.subheader("🧮 Fórmulas utilizadas")
        st.latex(r"N = \text{líneas/s (depende de la frecuencia)}")
        st.latex(r"M = \frac{\theta_{\text{total}}}{\Delta\theta} \ \text{[puntos/línea]}")
        st.latex(r"P = M \times N \ \text{[puntos/s]}")
        st.latex(r"V_b = \Delta\phi \times N \ \text{[°/s]}")
        st.latex(r"T = \frac{\phi_{\text{total}}}{V_b} \ \text{[s]}")
        st.latex(r"PT = P \times T \ \text{[puntos]}")
        
        # Resultados
        st.subheader("📊 Resultados")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="N (líneas/s)", value=formato_numero(N, 0))
            st.metric(label="M (puntos/línea)", value=formato_numero(M, 0))
        with col_res2:
            st.metric(label="P (puntos/s)", value=formato_numero(P, 0))
            st.metric(label="Vb (°/s)", value=formato_numero(Vb, 2))
        with col_res3:
            st.metric(label="T (segundos)", value=formato_numero(T_redondeado, 0))
            st.metric(label="PT (puntos)", value=formato_numero(PT, 0))
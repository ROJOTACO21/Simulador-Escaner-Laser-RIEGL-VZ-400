import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Simulador Escáner Láser RIEGL VZ-400", layout="centered")

# Título principal
st.title("Simulador Escáner Láser RIEGL VZ-400 - Preparación de Levantamiento")
st.write("Este simulador te guiará paso a paso para definir los parámetros de un levantamiento con el patrón de levantamiento Rectangular Field of View (FOV).")

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
# Ejemplo de GIF (cambia por la ruta real)
st.image("IMA/gif_intro.gif", caption="Vista general del escaneo", use_container_width=True)

# ---------------------------
# Paso 2 - PHI SOCS
# ---------------------------

st.header("Paso 2: Parámetros PHI SOCS (Ángulo de línea - φ)")

phi_start = st.number_input("Start angle (°)", min_value=0.0, max_value=360.0, value=0.0, step=0.1)
phi_stop = st.number_input("Stop angle (°)", min_value=0.0, max_value=360.0, value=180.0, step=0.1)
phi_inc = st.number_input("Increment Δφ (°)", min_value=0.0024, max_value=0.5, value=0.01, step=0.001, format="%.4f")

st.image("IMA/vista planta.gif", caption="Movimiento horizontal del escaneo", use_container_width=True)

if phi_start >= phi_stop:
    st.error("⚠️ El Start angle debe ser menor que el Stop angle.")

# ---------------------------
# Paso 3 - THETA SOCS
# ---------------------------

st.header("Paso 3: Parámetros THETA SOCS (Ángulo de marco - θ)")

theta_start = st.number_input("Start angle (°)", min_value=30.0, max_value=130.0, value=30.0, step=0.1)
theta_stop = st.number_input("Stop angle (°)", min_value=30.0, max_value=130.0, value=100.0, step=0.1)
theta_inc = st.number_input("Increment Δθ (°)", min_value=0.0024, max_value=0.288, value=0.01, step=0.001, format="%.4f")

#st.image("theta.gif", caption="Movimiento vertical del escaneo", use_column_width=True)

if theta_start >= theta_stop:
    st.error("⚠️ El Start angle debe ser menor que el Stop angle.")
if theta_inc != phi_inc:
    st.warning("⚠️ El Increment de THETA y PHI deben ser iguales para una nube de puntos uniforme.")

# ---------------------------
# Paso 4 - Frecuencia del láser
# ---------------------------

st.header("Paso 4: Frecuencia del escáner")
st.markdown("Seleccione la frecuencia del pulso láser permitida para el Riegl VZ-400.")

# Selector de frecuencia (solo dos opciones)
frecuencia = st.radio(
    "Frecuencia del pulso láser:",
    options=[100_000, 300_000],
    format_func=lambda x: f"{x/1000:.0f} kHz"
)

# Mostrar imagen con pie de figura
st.image(
    "IMA/ESP.png",  # Cambia si la ruta es distinta
    caption="Figura 1. Especificaciones técnicas del Riegl VZ-400 – Frecuencia del pulso láser",
    use_container_width=True
)

st.write(f"**Frecuencia seleccionada:** {frecuencia/1000:.0f} kHz")


# ---------------------------
# Paso 5 - Cálculo de parámetros de rendimiento
# ---------------------------


st.header("Paso 5: Cálculo de parámetros de rendimiento")
st.markdown("A partir de los valores ingresados, se calculan los parámetros de rendimiento del escáner.")

# Variables
theta_total = theta_stop - theta_start  # [°]
N = 100  # líneas/s
M = theta_total / theta_inc  # puntos/línea
P = M * N  # puntos/s
Vb = phi_inc * N  # °/s
phi_total = phi_stop - phi_start  # rango horizontal en °
T = phi_total / Vb  # s
PT = P * T  # puntos totales

# Mostrar fórmulas y resultados

st.subheader("Fórmulas utilizadas")
st.latex(r"N = 100 \ \text{[líneas/s]}")
st.latex(r"M = \frac{\theta_{\text{total}}}{\Delta\theta} \ \text{[puntos/línea]}")
st.latex(r"P = M \times N \ \text{[puntos/s]}")
st.latex(r"V_b = \Delta\phi \times N \ \text{[°/s]}")
st.latex(r"T = \frac{\phi_{\text{total}}}{V_b} \ \text{[s]}")
st.latex(r"PT = P \times T \ \text{[puntos]}")

# Resultados
st.subheader("Resultados")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="N (líneas/s)", value=f"{N:.0f}")
    st.metric(label="M (puntos/línea)", value=f"{M:.0f}")
with col2:
   st.metric(label="P (puntos/s)", value=f"{P:,.0f}")
   st.metric(label="Vb (°/s)", value=f"{Vb:.2f}")
with col3:
   st.metric(label="T (segundos)", value=f"{T:.2f}")
   st.metric(label="PT (puntos)", value=f"{PT:,.0f}")


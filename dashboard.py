# dashboard.py
# Ejecutar con: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Mi Dashboard", layout="wide")

# Título principal
st.title("🚀 Dashboard de Ventas - Demo")
st.markdown("---")

# Generar datos de ejemplo
@st.cache_data  # Cachea los datos para mejor rendimiento
def cargar_datos():
    np.random.seed(42)
    fechas = pd.date_range("2024-01-01", periods=100, freq="D")
    datos = {
        "Fecha": fechas,
        "Ventas": np.random.randint(100, 1000, 100),
        "Región": np.random.choice(["Norte", "Sur", "Este", "Oeste"], 100),
        "Producto": np.random.choice(["A", "B", "C"], 100)
    }
    return pd.DataFrame(datos)

df = cargar_datos()

# Sidebar con filtros
st.sidebar.header("Filtros")
regiones = st.sidebar.multiselect(
    "Selecciona región(es):",
    options=df["Región"].unique(),
    default=df["Región"].unique()
)
productos = st.sidebar.multiselect(
    "Selecciona producto(s):",
    options=df["Producto"].unique(),
    default=df["Producto"].unique()
)

# Filtrar datos
df_filtrado = df[
    (df["Región"].isin(regiones)) & 
    (df["Producto"].isin(productos))
]

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total Ventas", f"${df_filtrado['Ventas'].sum():,}")
col2.metric("Promedio Diario", f"${df_filtrado['Ventas'].mean():,.0f}")
col3.metric("Registros", len(df_filtrado))

st.markdown("---")

# Gráficos en dos columnas
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("📈 Ventas por Fecha")
    fig_linea = px.line(
        df_filtrado, x="Fecha", y="Ventas", 
        color="Región", title=""
    )
    st.plotly_chart(fig_linea, use_container_width=True)

with col_der:
    st.subheader("📊 Ventas por Producto")
    ventas_producto = df_filtrado.groupby("Producto")["Ventas"].sum().reset_index()
    fig_barras = px.bar(
        ventas_producto, x="Producto", y="Ventas",
        color="Producto", title=""
    )
    st.plotly_chart(fig_barras, use_container_width=True)

# Tabla de datos
st.subheader("📋 Datos Detallados")
st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

# Botón para descargar datos
st.download_button(
    label="⬇️ Descargar CSV",
    data=df_filtrado.to_csv(index=False),
    file_name="datos_filtrados.csv",
    mime="text/csv"
)
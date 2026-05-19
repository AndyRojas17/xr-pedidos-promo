import streamlit as st
from utils import render_header, render_footer

st.set_page_config(
    page_title="XR Panel — XR Moto Store",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("Herramientas de gestión — XR Moto Store")

st.markdown("## Bienvenido al panel de herramientas")
st.markdown('<p style="color:#666;margin-top:-12px">Selecciona una herramienta para comenzar</p>',
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style="background:#FAFAFA;border:1.5px solid #E0E0E0;border-top:4px solid #CC0000;
                border-radius:12px;padding:28px 24px;min-height:180px">
        <div style="font-size:2rem;margin-bottom:8px">🛒</div>
        <div style="font-size:1.2rem;font-weight:800;color:#1A1A1A">Pedidos Promo</div>
        <div style="color:#666;font-size:0.9rem;margin-top:8px;line-height:1.5">
            Analiza historial de ventas, stock actual y lista promocional Honda
            para generar el TOP 60 de productos recomendados a pedir.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.page_link("pages/1_Pedidos_Promo.py", label="Ir a Pedidos Promo →", use_container_width=True)

with col2:
    st.markdown("""
    <div style="background:#FAFAFA;border:1.5px solid #E0E0E0;border-top:4px solid #005BAC;
                border-radius:12px;padding:28px 24px;min-height:180px">
        <div style="font-size:2rem;margin-bottom:8px">🔍</div>
        <div style="font-size:1.2rem;font-weight:800;color:#1A1A1A">Compatibilidades</div>
        <div style="color:#666;font-size:0.9rem;margin-top:8px;line-height:1.5">
            Busca códigos de repuestos y modelos compatibles. Escribe el modelo
            o nombre del repuesto y encuentra todo lo que le aplica.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.page_link("pages/2_Compatibilidades.py", label="Ir a Compatibilidades →", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr style="border-top:1px solid #EEE">', unsafe_allow_html=True)
st.markdown("""
<p style="color:#AAAAAA;font-size:0.8rem;text-align:center">
    Base de datos actual: <b>302 repuestos</b> cargados desde Lista Promo Mayo 2026.
    Se irá ampliando con cada nueva lista y repuestos agregados manualmente.
</p>
""", unsafe_allow_html=True)

render_footer()

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

st.markdown("""
<style>
.xr-card {
    display: block;
    text-decoration: none;
    background: #FAFAFA;
    border: 1.5px solid #E0E0E0;
    border-radius: 12px;
    padding: 28px 24px;
    min-height: 180px;
    transition: all 0.18s ease;
    cursor: pointer;
}
.xr-card:hover {
    background: #FFFFFF;
    box-shadow: 0 6px 24px rgba(0,0,0,0.10);
    transform: translateY(-3px);
    border-color: #BBBBBB;
    text-decoration: none;
}
.xr-card.red  { border-top: 4px solid #CC0000; }
.xr-card.blue { border-top: 4px solid #005BAC; }
/* Quitar subrayado de todo el contenido interno */
.xr-card * { text-decoration: none !important; }
.xr-card-icon  { font-size: 2.2rem; margin-bottom: 10px; }
.xr-card-title { font-size: 1.2rem; font-weight: 800; color: #1A1A1A; }
.xr-card-desc  { color: #666; font-size: 0.9rem; margin-top: 8px; line-height: 1.5; }
.xr-card-arrow { display: inline-block; margin-top: 16px; font-size: 0.9rem;
                  font-weight: 700; color: #CC0000; }
.xr-card.blue .xr-card-arrow { color: #005BAC; }
/* Responsive: en móvil apilar las tarjetas verticalmente */
.xr-cards-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 640px) {
    .xr-cards-grid { grid-template-columns: 1fr; gap: 16px; }
    .xr-card { padding: 20px 18px; }
}
</style>

<div class="xr-cards-grid">

  <a href="/Pedidos_Promo" class="xr-card red">
    <div class="xr-card-icon">🛒</div>
    <div class="xr-card-title">Pedidos Promo</div>
    <div class="xr-card-desc">
      Analiza historial de ventas, stock actual y lista promocional Honda
      para generar el TOP 60 de productos recomendados a pedir.
    </div>
    <div class="xr-card-arrow">Ir a Pedidos Promo →</div>
  </a>

  <a href="/Compatibilidades" class="xr-card blue">
    <div class="xr-card-icon">🔍</div>
    <div class="xr-card-title">Compatibilidades</div>
    <div class="xr-card-desc">
      Busca códigos de repuestos y modelos compatibles. Escribe el modelo
      o nombre del repuesto y encuentra todo lo que le aplica.
    </div>
    <div class="xr-card-arrow">Ir a Compatibilidades →</div>
  </a>

</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr style="border-top:1px solid #EEE">', unsafe_allow_html=True)
st.markdown("""
<p style="color:#AAAAAA;font-size:0.8rem;text-align:center">
    Base de datos actual: <b>302 repuestos</b> cargados desde Lista Promo Mayo 2026.
    Se irá ampliando con cada nueva lista y repuestos agregados manualmente.
</p>
""", unsafe_allow_html=True)

render_footer()

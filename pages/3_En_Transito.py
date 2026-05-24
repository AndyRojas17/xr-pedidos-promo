import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import render_header, render_footer

st.set_page_config(
    page_title="En Tránsito — XR Panel",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("En Tránsito — Pedidos realizados recientemente")

# ── CARGA DE DATOS ────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "en_transito.csv")

@st.cache_data
def cargar_datos():
    df = pd.read_csv(DATA_PATH, dtype=str).fillna('')
    df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(0).astype(int)
    df['Precio']   = pd.to_numeric(df['Precio'],   errors='coerce')
    df['Total']    = pd.to_numeric(df['Total'],     errors='coerce')
    return df

df = cargar_datos()

# ── MÉTRICAS ─────────────────────────────────────────────────────────────────
total_items    = len(df)
total_unidades = int(df['Cantidad'].sum())
total_inversion = df['Total'].sum()
ambos_count    = len(df[df['Fuente'] == 'Ambos'])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card blue">
        <div class="metric-value">{total_items}</div>
        <div class="metric-label">Ítems en tránsito</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{total_unidades:,}</div>
        <div class="metric-label">Unidades pedidas</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card red">
        <div class="metric-value">S/. {total_inversion:,.0f}</div>
        <div class="metric-label">Inversión total</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card green">
        <div class="metric-value">{ambos_count}</div>
        <div class="metric-label">Ítems en ambas listas</div></div>""", unsafe_allow_html=True)

st.markdown('<div style="margin-top:24px"></div>', unsafe_allow_html=True)

# ── FILTROS ───────────────────────────────────────────────────────────────────
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    buscar = st.text_input("", placeholder="Buscar por código, descripción o modelo…",
                           label_visibility="collapsed")
with col_f2:
    fuentes = ['Todas'] + sorted(df['Fuente'].unique().tolist())
    filtro_fuente = st.selectbox("", fuentes, label_visibility="collapsed")

df_filtrado = df.copy()
if buscar.strip():
    q = buscar.lower()
    df_filtrado = df_filtrado[
        df_filtrado['Codigo'].str.lower().str.contains(q) |
        df_filtrado['Descripcion'].str.lower().str.contains(q) |
        df_filtrado['Modelo'].str.lower().str.contains(q)
    ]
if filtro_fuente != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Fuente'] == filtro_fuente]

st.markdown(f"<p style='color:#888;font-size:0.82rem;margin-bottom:8px'>{len(df_filtrado)} ítem(s) mostrados</p>",
            unsafe_allow_html=True)

# ── TABLA ─────────────────────────────────────────────────────────────────────
FUENTE_COLOR = {
    'Ambos':               ('#E8F5E9', '#2E7D32'),
    'Lista Promo Mayo 2026': ('#E8F0FE', '#1A4FAE'),
    'Sugeridos Paty':      ('#FFF3E0', '#E65100'),
}

for _, row in df_filtrado.iterrows():
    bg, fg = FUENTE_COLOR.get(row['Fuente'], ('#F5F5F5', '#333'))
    precio_str = f"S/. {row['Precio']:.2f}" if pd.notna(row['Precio']) else '—'
    total_str  = f"S/. {row['Total']:,.2f}" if pd.notna(row['Total']) else '—'

    st.markdown(f"""
    <div style="background:#FAFAFA;border:1px solid #E5E5E5;border-left:4px solid #CC0000;
                border-radius:8px;padding:14px 20px;margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
            <div style="flex:1;min-width:220px">
                <span style="font-family:monospace;background:#F0F0F0;color:#333;
                             padding:2px 8px;border-radius:4px;font-size:0.85rem;
                             font-weight:700">{row['Codigo']}</span>
                <span style="font-size:0.95rem;font-weight:700;color:#1A1A1A;
                             margin-left:10px">{row['Descripcion']}</span>
            </div>
            <span style="background:{bg};color:{fg};padding:2px 10px;border-radius:10px;
                         font-size:0.75rem;font-weight:700;white-space:nowrap">{row['Fuente']}</span>
        </div>
        <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:16px;align-items:center">
            <span style="font-size:0.8rem;color:#666">
                🏍️ <b>{row['Modelo'] if row['Modelo'] else '—'}</b>
            </span>
            <span style="font-size:0.8rem;color:#666">
                📦 <b style="color:#1A1A1A">{row['Cantidad']} uds</b>
            </span>
            <span style="font-size:0.8rem;color:#666">
                💲 Precio: <b>{precio_str}</b>
            </span>
            <span style="font-size:0.8rem;color:#666">
                💰 Total: <b style="color:#CC0000">{total_str}</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if df_filtrado.empty:
    st.info("No se encontraron ítems con ese criterio.")

# ── DESCARGA ──────────────────────────────────────────────────────────────────
st.markdown('<div style="margin-top:32px"></div>', unsafe_allow_html=True)
st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin-bottom:20px">', unsafe_allow_html=True)

def generar_excel_transito(df_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'En Tránsito'

    ws.merge_cells('A1:G1')
    c = ws['A1']
    c.value = 'XR MOTO STORE — PEDIDOS EN TRÁNSITO'
    c.font = Font(name='Arial', bold=True, size=12, color='FFFFFF')
    c.fill = PatternFill('solid', start_color='CC0000')
    c.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 24

    headers = ['Código', 'Descripción', 'Modelo', 'Precio (S/.)', 'Cantidad', 'Total (S/.)', 'Fuente']
    widths  = [18, 40, 30, 14, 12, 14, 24]
    thin = Side(style='thin', color='D9D9D9')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for ci, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=2, column=ci, value=h)
        cell.font = Font(name='Arial', bold=True, size=10, color='FFFFFF')
        cell.fill = PatternFill('solid', start_color='404040')
        cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[2].height = 20

    fill_ambos  = PatternFill('solid', start_color='E8F5E9')
    fill_promo  = PatternFill('solid', start_color='E8F0FE')
    fill_paty   = PatternFill('solid', start_color='FFF3E0')
    fill_alt    = PatternFill('solid', start_color='F5F5F5')

    for ri, (_, row) in enumerate(df_data.iterrows()):
        er = ri + 3
        precio = row['Precio'] if pd.notna(row['Precio']) else ''
        total  = row['Total']  if pd.notna(row['Total'])  else ''
        vals = [row['Codigo'], row['Descripcion'], row['Modelo'],
                precio, row['Cantidad'], total, row['Fuente']]

        if row['Fuente'] == 'Ambos':
            fill = fill_ambos
        elif 'Promo' in str(row['Fuente']):
            fill = fill_promo
        elif 'Paty' in str(row['Fuente']):
            fill = fill_paty
        else:
            fill = fill_alt if ri % 2 == 0 else PatternFill()

        for ci, val in enumerate(vals, 1):
            cell = ws.cell(row=er, column=ci, value=val)
            cell.border = border
            cell.font = Font(name='Arial', size=9)
            cell.alignment = Alignment(vertical='center')
            cell.fill = fill
            if ci == 1:
                cell.font = Font(name='Arial', bold=True, size=9)
            if ci in (4, 6) and val != '':
                cell.number_format = '#,##0.00'
        ws.row_dimensions[er].height = 16

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf

col_dl, col_info = st.columns([1, 2])
with col_dl:
    clave = st.text_input("🔒 Clave de administrador", type="password",
                          placeholder="Ingresa la clave para descargar")
    if clave == "xr3010":
        excel_data = generar_excel_transito(df)
        st.download_button(
            label="⬇️  Descargar pedidos en tránsito (Excel)",
            data=excel_data,
            file_name="XR_En_Transito.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    elif clave:
        st.markdown('<p style="color:#CC0000;font-size:0.82rem;margin-top:4px">Clave incorrecta.</p>',
                    unsafe_allow_html=True)
with col_info:
    st.markdown(f"""
    <p style="color:#888;font-size:0.85rem;margin-top:8px">
        Lista de <b>{len(df)} ítems</b> pedidos recientemente —
        <b>{total_unidades:,} unidades</b> por un total de
        <b>S/. {total_inversion:,.0f}</b>. Solo disponible para administradores.
    </p>
    """, unsafe_allow_html=True)

st.markdown('<div style="margin-top:16px"></div>', unsafe_allow_html=True)
with st.expander("ℹ️  ¿Cómo se actualiza esta lista?"):
    st.markdown("""
    Para actualizar los pedidos en tránsito:
    1. Corre el script `update_transito.py` con la nueva Lista Promo y/o Sugeridos Paty.
    2. El script genera un nuevo `data/en_transito.csv`.
    3. Haz commit y push a GitHub — la app se actualiza automáticamente.
    """)

render_footer()

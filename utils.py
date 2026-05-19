import streamlit as st
import os

STYLES = """
<style>
.stApp { background-color: #FFFFFF; }
.xr-divider { border: none; border-top: 1px solid #EEEEEE; margin: 20px 0; }
.metric-card {
    background: #FAFAFA; border-radius: 10px; padding: 18px 22px;
    border: 1px solid #EEEEEE; border-left: 4px solid #CC0000;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-card.blue   { border-left-color: #005BAC; }
.metric-card.green  { border-left-color: #00A651; }
.metric-card.orange { border-left-color: #FF8C00; }
.metric-value { font-size: 2rem; font-weight: 800; color: #1A1A1A; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #888888; text-transform: uppercase;
                letter-spacing: 0.8px; margin-top: 6px; }
.stButton > button {
    background: linear-gradient(135deg, #CC0000, #990000) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    font-size: 1.1rem !important; font-weight: 700 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #FF0000, #CC0000) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(204,0,0,0.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #005BAC, #003D7A) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    font-size: 1rem !important; font-weight: 700 !important;
    padding: 12px 32px !important; width: 100% !important;
}
.upload-card {
    background: #FAFAFA; border: 1.5px solid #E0E0E0; border-radius: 10px;
    padding: 20px; margin-bottom: 12px;
}
.upload-card h4 {
    color: #CC0000; font-size: 0.85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 4px 0;
}
.upload-card p { color: #888888; font-size: 0.78rem; margin: 0 0 12px 0; }
.xr-footer {
    text-align: center; color: #AAAAAA; font-size: 0.75rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #EEEEEE;
}
</style>
"""

def render_header(subtitle=""):
    st.markdown(STYLES, unsafe_allow_html=True)
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=110)
    with col_title:
        st.markdown(f"""
        <div style="padding-top:8px">
            <div style="font-size:1.9rem;font-weight:900;color:#CC0000;line-height:1">
                XR Panel
            </div>
            <div style="font-size:0.9rem;color:#555555;margin-top:4px">
                {subtitle if subtitle else 'Herramientas de gestión — XR Moto Store'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div style="border-top:2px solid #CC0000;margin:16px 0 24px 0"></div>',
                unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="xr-footer">
        XR Moto Store S.A.C. — Repuestos Honda
    </div>
    """, unsafe_allow_html=True)

"""
Streamlit Frontend - Webes felület
"""
import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import os

# Konfiguráció
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Rubik Speedcube Timer",
    page_icon="🎲",
    layout="wide"
)

# Címsor
st.title("🎲 Rubik Speedcube Timer")
st.markdown("---")


def call_api(endpoint: str, method: str = "GET", data: dict = None):
    """API hívás helper függvény."""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API hiba: {e}")
        return None


# Két oszlop layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("⏱️ Timer")
    
    # Scramble generálás
    if st.button("🔄 Új Scramble", use_container_width=True):
        scramble_data = call_api("/scramble")
        if scramble_data:
            st.session_state.scramble = scramble_data["scramble"]
    
    # Daily scramble
    if st.button("📅 Napi Scramble", use_container_width=True):
        scramble_data = call_api("/scramble/daily")
        if scramble_data:
            st.session_state.scramble = scramble_data["scramble"]
    
    # Scramble megjelenítése
    if "scramble" in st.session_state:
        st.info(f"**Scramble:** {st.session_state.scramble}")
    
    st.markdown("---")
    
    # Idő bevitele
    st.subheader("Idő mentése")
    time_input = st.number_input(
        "Idő (másodperc)",
        min_value=0.01,
        max_value=3600.0,
        value=15.0,
        step=0.01
    )
    
    if st.button("💾 Mentés", type="primary", use_container_width=True):
        if "scramble" not in st.session_state:
            st.warning("Először generálj scramble-t!")
        else:
            data = {
                "time": time_input,
                "scramble": st.session_state.scramble
            }
            result = call_api("/times", method="POST", data=data)
            if result:
                st.success(f"✅ Idő mentve: {time_input}s")
                st.rerun()

with col2:
    st.header("📊 Statisztikák")
    
    # Statisztikák lekérése
    stats = call_api("/stats")
    
    if stats:
        # Metrikák
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("🏆 Legjobb", f"{stats['best_time']:.2f}s" if stats['best_time'] else "N/A")
        
        with metrics_col2:
            st.metric("📈 Átlag", f"{stats['average']:.2f}s" if stats['average'] else "N/A")
        
        with metrics_col3:
            st.metric("📋 Kirakások", stats['total_solves'])
        
        if stats['last_5_avg']:
            st.info(f"**AO5 (utolsó 5):** {stats['last_5_avg']:.2f}s")

# Legutóbbi idők
st.markdown("---")
st.header("🕐 Legutóbbi Kirakások")

times = call_api("/times")

if times:
    # Táblázat
    st.dataframe(
        [
            {
                "Idő": f"{t['time']:.2f}s",
                "Scramble": t['scramble'][:50] + "...",
                "Dátum": datetime.fromisoformat(t['date'].replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
            }
            for t in times[:10]
        ],
        use_container_width=True
    )
    
    # VIZUALIZÁCIÓ - Időfejlődés grafikon
    if len(times) > 1:
        st.subheader("📉 Időfejlődés")
        
        time_values = [t['time'] for t in reversed(times[:20])]
        indices = list(range(1, len(time_values) + 1))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=indices,
            y=time_values,
            mode='lines+markers',
            name='Idő',
            line=dict(color='#FF6B6B', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Utolsó 20 kirakás",
            xaxis_title="Kirakás sorszám",
            yaxis_title="Idő (másodperc)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Még nincsenek mentett idők. Kezdj el gyakorolni! 🎲")

# Footer
st.markdown("---")
st.caption("Rubik Speedcube Timer v1.0 | FastAPI + Streamlit")

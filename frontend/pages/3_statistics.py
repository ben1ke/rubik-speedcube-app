"""
Statisztikák Oldal - Részletes elemzések és grafikonok.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Path beállítása
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.utils.api_client import APIClient

# Oldal konfiguráció
st.set_page_config(
    page_title="Statisztikák - Rubik Speedcube",
    page_icon="📊",
    layout="wide"
)

# API Client
api = APIClient()


def format_time(seconds: float) -> str:
    """Idő formázása."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}:{secs:05.2f}"


def main():
    """Statisztikák oldal megjelenítése."""
    
    st.title("📊 Statisztikák")
    st.markdown("Elemezd a fejlődésed és nézd meg a teljesítményedet!")
    st.markdown("---")
    
    # Backend ellenőrzés
    if not api.health_check():
        st.error("❌ Backend nem érhető el!")
        return
    
    # Statisztikák betöltése
    with st.spinner("Statisztikák betöltése..."):
        stats = api.get_stats_summary()
    
    if stats.get("total_solves", 0) == 0:
        st.warning("⚠️ Még nincs mentett idő. Kezdj el gyakorolni a Timer oldalon!")
        return
    
    # ============= METRIKÁK =============
    st.subheader("🏆 Főbb Mutatók")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        best = stats.get("best")
        if best:
            st.metric("🥇 Best", f"{best:.2f}s")
        else:
            st.metric("🥇 Best", "N/A")
    
    with col2:
        ao5 = stats.get("ao5")
        if ao5:
            st.metric("📈 AO5", f"{ao5:.2f}s")
        else:
            st.metric("📈 AO5", "< 5 idő")
    
    with col3:
        ao12 = stats.get("ao12")
        if ao12:
            st.metric("📈 AO12", f"{ao12:.2f}s")
        else:
            st.metric("📈 AO12", "< 12 idő")
    
    with col4:
        ao100 = stats.get("ao100")
        if ao100:
            st.metric("📈 AO100", f"{ao100:.2f}s")
        else:
            st.metric("📈 AO100", "< 100 idő")
    
    with col5:
        total = stats.get("total_solves", 0)
        st.metric("🎯 Összesen", total)
    
    st.markdown("---")
    
    # ============= GRAFIKONOK =============
    
    # Tabs a különböző grafikonokhoz
    tab1, tab2, tab3 = st.tabs(["📈 Időfejlődés", "📊 Eloszlás", "📋 Összes Idő"])
    
    with tab1:
        st.subheader("📈 Időfejlődés Grafikon")
        st.markdown("Nézd meg, hogyan változtak az időid az egyes kirakások során.")
        
        with st.spinner("Grafikon adatok betöltése..."):
            chart_data = api.get_chart_data()
        
        if chart_data:
            # DataFrame készítése
            df = pd.DataFrame(chart_data)
            df['date'] = pd.to_datetime(df['date'])
            
            # Plotly vonaldiagram
            fig = px.line(
                df,
                x='solve_number',
                y='time',
                title='Kirakási Idők Fejlődése',
                labels={
                    'solve_number': 'Kirakás Sorszáma',
                    'time': 'Idő (másodperc)'
                },
                markers=True,
                hover_data={'date': '|%Y-%m-%d %H:%M'}
            )
            
            fig.update_layout(
                xaxis_title="Kirakás Sorszáma",
                yaxis_title="Idő (másodperc)",
                hovermode='x unified',
                height=500
            )
            
            # Best time vonal hozzáadása
            if stats.get("best"):
                fig.add_hline(
                    y=stats["best"],
                    line_dash="dash",
                    line_color="green",
                    annotation_text=f"Best: {stats['best']:.2f}s",
                    annotation_position="right"
                )
            
            # AO5 vonal (ha van)
            if stats.get("ao5"):
                fig.add_hline(
                    y=stats["ao5"],
                    line_dash="dash",
                    line_color="blue",
                    annotation_text=f"AO5: {stats['ao5']:.2f}s",
                    annotation_position="right"
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Fejlődési trendek
            st.markdown("### 📊 Fejlődési Trendek")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Első 10 átlaga
                if len(df) >= 10:
                    first_10 = df.head(10)['time'].mean()
                    st.metric("Első 10 átlag", f"{first_10:.2f}s")
            
            with col2:
                # Utolsó 10 átlaga
                if len(df) >= 10:
                    last_10 = df.tail(10)['time'].mean()
                    st.metric("Utolsó 10 átlag", f"{last_10:.2f}s")
            
            with col3:
                # Változás %
                if len(df) >= 20:
                    first_10 = df.head(10)['time'].mean()
                    last_10 = df.tail(10)['time'].mean()
                    change = ((last_10 - first_10) / first_10) * 100
                    st.metric("Változás", f"{change:+.1f}%")
        else:
            st.info("Nincs elég adat a grafikonhoz.")
    
    with tab2:
        st.subheader("📊 Idő Eloszlás")
        st.markdown("Az időid eloszlása különböző tartományokban.")
        
        with st.spinner("Eloszlás számítása..."):
            distribution = api.get_distribution(bucket_size=2.0)
        
        if distribution:
            # DataFrame készítése
            df_dist = pd.DataFrame(distribution)
            
            # Plotly oszlopdiagram
            fig = px.bar(
                df_dist,
                x='range',
                y='count',
                title='Kirakási Idők Eloszlása',
                labels={
                    'range': 'Idő Tartomány',
                    'count': 'Kirakások Száma'
                },
                color='count',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                xaxis_title="Idő Tartomány",
                yaxis_title="Kirakások Száma",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statisztikák az eloszlásról
            st.markdown("### 📈 Eloszlási Statisztikák")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                most_common = df_dist.loc[df_dist['count'].idxmax()]
                st.metric("Leggyakoribb tartomány", most_common['range'])
            
            with col2:
                total_in_dist = df_dist['count'].sum()
                st.metric("Kategorizált idők", int(total_in_dist))
            
            with col3:
                st.metric("Különböző tartományok", len(df_dist))
        else:
            st.info("Nincs elég adat az eloszláshoz.")
    
    with tab3:
        st.subheader("📋 Összes Kirakási Idő")
        st.markdown("Összes mentett időd táblázatos formában.")
        
        # Szűrők
        col1, col2 = st.columns([1, 3])
        
        with col1:
            show_dnf = st.checkbox("DNF-ek megjelenítése", value=True)
        
        with col2:
            limit = st.slider("Megjelenített idők száma", 10, 200, 50, 10)
        
        with st.spinner("Idők betöltése..."):
            all_times = api.get_times(limit=limit)
        
        if all_times:
            # DataFrame készítése
            df_data = []
            for i, time_entry in enumerate(all_times, 1):
                dnf = time_entry.get("dnf", 0)
                
                # DNF szűrés
                if not show_dnf and dnf:
                    continue
                
                time_value = time_entry.get("time", 0)
                
                if dnf:
                    display_time = "DNF"
                    numeric_time = None
                else:
                    display_time = format_time(time_value)
                    numeric_time = time_value
                
                df_data.append({
                    "#": i,
                    "Idő": display_time,
                    "Másodperc": numeric_time,
                    "Scramble": time_entry.get("scramble", "")[:60] + "...",
                    "Dátum": datetime.fromisoformat(time_entry.get("date", "")).strftime("%Y-%m-%d %H:%M:%S")
                })
            
            df = pd.DataFrame(df_data)
            
            # Táblázat megjelenítése
            st.dataframe(
                df[["#", "Idő", "Scramble", "Dátum"]],
                use_container_width=True,
                hide_index=True,
                height=600
            )
            
            # Gyors statisztikák a táblázatról
            st.markdown("### 📊 Táblázat Statisztikák")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Megjelenített sorok", len(df))
            
            with col2:
                valid_times = [t for t in df['Másodperc'] if t is not None]
                if valid_times:
                    st.metric("Átlag", f"{sum(valid_times) / len(valid_times):.2f}s")
                else:
                    st.metric("Átlag", "N/A")
            
            with col3:
                if valid_times:
                    st.metric("Min", f"{min(valid_times):.2f}s")
                else:
                    st.metric("Min", "N/A")
            
            with col4:
                if valid_times:
                    st.metric("Max", f"{max(valid_times):.2f}s")
                else:
                    st.metric("Max", "N/A")
        else:
            st.info("Nincs mentett idő.")
    
    # ============= SESSION STATS =============
    st.markdown("---")
    st.subheader("🔥 Session Statisztikák")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Utolsó 24 óra**")
        session_24h = api.get_session_stats(hours=24)
        
        if session_24h.get("total_solves", 0) > 0:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Összes", session_24h.get("total_solves", 0))
                best = session_24h.get("best")
                if best:
                    st.metric("Best", f"{best:.2f}s")
            
            with col_b:
                st.metric("Érvényes", session_24h.get("valid_solves", 0))
                avg = session_24h.get("average")
                if avg:
                    st.metric("Átlag", f"{avg:.2f}s")
        else:
            st.info("Nincs adat az elmúlt 24 órából.")
    
    with col2:
        st.markdown("**📅 Utolsó 7 nap**")
        session_7d = api.get_session_stats(hours=168)
        
        if session_7d.get("total_solves", 0) > 0:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Összes", session_7d.get("total_solves", 0))
                best = session_7d.get("best")
                if best:
                    st.metric("Best", f"{best:.2f}s")
            
            with col_b:
                st.metric("Érvényes", session_7d.get("valid_solves", 0))
                avg = session_7d.get("average")
                if avg:
                    st.metric("Átlag", f"{avg:.2f}s")
        else:
            st.info("Nincs adat az elmúlt 7 napból.")
    
    # Footer
    st.markdown("---")
    st.caption("Statisztikák oldal | Elemezd a teljesítményedet és javíts! 📈")


if __name__ == "__main__":
    main()

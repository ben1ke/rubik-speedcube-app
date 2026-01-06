"""
Timer Oldal - Időmérés, scramble és idők mentése.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Path beállítása az importokhoz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.utils.api_client import APIClient

# Oldal konfiguráció
st.set_page_config(
    page_title="Timer - Rubik Speedcube",
    page_icon="⏱️",
    layout="wide"
)

# API Client
api = APIClient()


def format_time(seconds: float) -> str:
    """
    Idő formázása olvasható formátumra.
    
    Args:
        seconds: Másodpercek
    
    Returns:
        str: Formázott idő
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}:{secs:05.2f}"


def main():
    """Timer oldal megjelenítése."""
    
    st.title("⏱️ Timer")
    st.markdown("Mérj időt, gyakorolj és mentsd el az eredményeidet!")
    st.markdown("---")
    
    # Backend ellenőrzés
    if not api.health_check():
        st.error("❌ Backend nem érhető el!")
        return
    
    # Két oszlop layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔀 Scramble")
        
        # Scramble generálás
        if "current_scramble" not in st.session_state:
            st.session_state.current_scramble = api.get_scramble()
        
        # Scramble megjelenítése
        scramble_text = st.session_state.current_scramble.get("scramble", "")
        st.code(scramble_text, language=None)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔄 Új Scramble", use_container_width=True):
                st.session_state.current_scramble = api.get_scramble()
                st.rerun()
        
        with col_btn2:
            if st.button("📅 Napi Scramble", use_container_width=True):
                st.session_state.current_scramble = api.get_daily_scramble()
                st.rerun()
        
        st.markdown("---")
        
        # Idő beviteli form
        st.subheader("⏱️ Idő Mentése")
        
        with st.form("time_form"):
            col_time1, col_time2 = st.columns([3, 1])
            
            with col_time1:
                time_input = st.number_input(
                    "Idő (másodperc)",
                    min_value=0.01,
                    max_value=3600.0,
                    value=10.0,
                    step=0.01,
                    format="%.2f"
                )
            
            with col_time2:
                dnf_checkbox = st.checkbox("DNF")
            
            submit_button = st.form_submit_button("💾 Mentés", use_container_width=True)
            
            if submit_button:
                dnf_value = 1 if dnf_checkbox else 0
                
                with st.spinner("Mentés..."):
                    result = api.save_time(
                        time=time_input,
                        scramble=scramble_text,
                        dnf=dnf_value
                    )
                
                if result:
                    if dnf_value:
                        st.success("✅ DNF mentve!")
                    else:
                        st.success(f"✅ Idő mentve: {format_time(time_input)}")
                    
                    # Új scramble automatikusan
                    st.session_state.current_scramble = api.get_scramble()
                    st.rerun()
                else:
                    st.error("❌ Hiba történt a mentés során!")
        
        st.markdown("---")
        
        # Utolsó 10 idő megjelenítése táblázatban
        st.subheader("📋 Utolsó 10 Idő")
        
        with st.spinner("Idők betöltése..."):
            recent_times = api.get_recent_times(limit=10)
        
        if recent_times:
            # DataFrame készítése
            df_data = []
            for i, time_entry in enumerate(recent_times, 1):
                dnf = time_entry.get("dnf", 0)
                time_value = time_entry.get("time", 0)
                
                if dnf:
                    display_time = "DNF"
                else:
                    display_time = format_time(time_value)
                
                df_data.append({
                    "#": i,
                    "Idő": display_time,
                    "Scramble": time_entry.get("scramble", "")[:50] + "...",
                    "Dátum": datetime.fromisoformat(time_entry.get("date", "")).strftime("%Y-%m-%d %H:%M")
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Még nincs mentett idő. Kezdj el gyakorolni! 🚀")
    
    with col2:
        st.subheader("📊 Gyors Statisztikák")
        
        with st.spinner("Statisztikák betöltése..."):
            stats = api.get_stats_summary()
        
        if stats and stats.get("total_solves", 0) > 0:
            # Best
            best = stats.get("best")
            if best:
                st.metric("🏆 Best", f"{best:.2f}s")
            else:
                st.metric("🏆 Best", "N/A")
            
            # AO5
            ao5 = stats.get("ao5")
            if ao5:
                st.metric("📈 AO5", f"{ao5:.2f}s")
            else:
                st.metric("📈 AO5", "< 5 idő")
            
            # AO12
            ao12 = stats.get("ao12")
            if ao12:
                st.metric("📈 AO12", f"{ao12:.2f}s")
            else:
                st.metric("📈 AO12", "< 12 idő")
            
            # AO100
            ao100 = stats.get("ao100")
            if ao100:
                st.metric("📈 AO100", f"{ao100:.2f}s")
            else:
                st.metric("📈 AO100", "< 100 idő")
            
            # Total
            total = stats.get("total_solves", 0)
            st.metric("🎯 Összesen", total)
            
            st.markdown("---")
            
            # Tippek
            st.info("""
            💡 **Tippek:**
            - Gyakorolj minden nap
            - Ismerj meg új algoritmusokat
            - Elemezd a statisztikáidat
            - Tartsd nyitva a scramble-t kirakás közben
            """)
        else:
            st.info("Még nincs adat. Kezdj el mérni időket! ⏱️")
    
    # Footer
    st.markdown("---")
    st.caption("Timer oldal | Gyakorolj rendszeresen a jobb időkért! 💪")


if __name__ == "__main__":
    main()

"""
Streamlit Főoldal - Rubik Speedcube App.
Üdvözlő oldal napi scramble-lel és gyors statisztikákkal.
"""
import streamlit as st
from frontend.utils.api_client import APIClient

# Oldal konfiguráció
st.set_page_config(
    page_title="Rubik Speedcube App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Client inicializálása
api = APIClient()


def main():
    """Főoldal megjelenítése."""
    
    # Fejléc
    st.title("🧊 Rubik Speedcube App")
    st.markdown("---")
    
    # Üdvözlő szöveg
    st.markdown("""
    ### Üdvözöllek a Rubik Speedcube Alkalmazásban! 🎯
    
    Ez az alkalmazás segít neked a Rubik kocka kirakási időid nyomon követésében,
    algoritmusok tanulásában és fejlődésed elemzésében.
    
    **Funkciók:**
    - ⏱️ **Timer**: Időmérés és mentés
    - 🧩 **Algoritmusok**: PLL, OLL, F2L algoritmusok gyűjteménye
    - 📊 **Statisztikák**: Részletes elemzések és grafikonok
    """)
    
    st.markdown("---")
    
    # Backend kapcsolat ellenőrzése
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if api.health_check():
            st.success("✅ Backend kapcsolat rendben")
        else:
            st.error("❌ Backend nem érhető el! Indítsd el: `uvicorn backend.main:app --reload`")
            return
    
    st.markdown("---")
    
    # Két oszlop: Napi scramble + Gyors statisztikák
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Mai Napi Scramble")
        
        with st.spinner("Scramble betöltése..."):
            daily_scramble = api.get_daily_scramble()
        
        if daily_scramble:
            # Scramble megjelenítése nagy betűkkel
            st.code(daily_scramble.get("scramble", ""), language=None)
            st.caption(f"Lépések száma: {daily_scramble.get('length', 0)}")
            
            # Új scramble gomb
            if st.button("🔄 Új Random Scramble"):
                with st.spinner("Generálás..."):
                    new_scramble = api.get_scramble()
                    if new_scramble:
                        st.code(new_scramble.get("scramble", ""), language=None)
                        st.caption(f"Lépések száma: {new_scramble.get('length', 0)}")
    
    with col2:
        st.subheader("📊 Gyors Statisztikák")
        
        with st.spinner("Statisztikák betöltése..."):
            stats = api.get_stats_summary()
        
        if stats:
            # Metrikák megjelenítése
            metric_col1, metric_col2 = st.columns(2)
            
            with metric_col1:
                best = stats.get("best")
                if best:
                    st.metric("🏆 Legjobb idő", f"{best:.2f}s")
                else:
                    st.metric("🏆 Legjobb idő", "Nincs adat")
                
                ao5 = stats.get("ao5")
                if ao5:
                    st.metric("📈 Average of 5", f"{ao5:.2f}s")
                else:
                    st.metric("📈 Average of 5", "Nincs elég adat")
            
            with metric_col2:
                ao12 = stats.get("ao12")
                if ao12:
                    st.metric("📈 Average of 12", f"{ao12:.2f}s")
                else:
                    st.metric("📈 Average of 12", "Nincs elég adat")
                
                total = stats.get("total_solves", 0)
                st.metric("🎯 Összes kirakás", total)
        else:
            st.info("Még nincs mentett idő. Kezdj el gyakorolni a Timer oldalon! ⏱️")
    
    st.markdown("---")
    
    # Session statisztikák
    st.subheader("🔥 Mai Session")
    
    with st.spinner("Session statisztikák betöltése..."):
        session_stats = api.get_session_stats(hours=24)
    
    if session_stats and session_stats.get("total_solves", 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Összes", session_stats.get("total_solves", 0))
        
        with col2:
            st.metric("Érvényes", session_stats.get("valid_solves", 0))
        
        with col3:
            best = session_stats.get("best")
            if best:
                st.metric("Legjobb", f"{best:.2f}s")
            else:
                st.metric("Legjobb", "N/A")
        
        with col4:
            avg = session_stats.get("average")
            if avg:
                st.metric("Átlag", f"{avg:.2f}s")
            else:
                st.metric("Átlag", "N/A")
    else:
        st.info("Ma még nem volt kirakás. Kezdj el gyakorolni! 💪")
    
    st.markdown("---")
    
    # Navigációs linkek
    st.markdown("""
    ### 🚀 Kezdj el használni!
    
    Használd a bal oldali menüt a navigációhoz:
    - **Timer** - Időmérés és kirakások mentése
    - **Algoritmusok** - Tanulj új algoritmusokat
    - **Statisztikák** - Elemezd a fejlődésed
    """)
    
    # Footer
    st.markdown("---")
    st.caption("Rubik Speedcube App v1.0.0 | FastAPI + Streamlit + SQLAlchemy")


if __name__ == "__main__":
    main()

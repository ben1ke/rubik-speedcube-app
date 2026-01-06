"""
Algoritmusok Oldal - Rubik kocka algoritmusok böngészése és kezelése.
"""
import streamlit as st
import sys
import os

# Path beállítása
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.utils.api_client import APIClient

# Oldal konfiguráció
st.set_page_config(
    page_title="Algoritmusok - Rubik Speedcube",
    page_icon="🧩",
    layout="wide"
)

# API Client
api = APIClient()

# Elérhető kategóriák és nehézségek
CATEGORIES = ["PLL", "OLL", "F2L", "CMLL", "COLL", "Basic", "Advanced"]
DIFFICULTIES = ["Kezdő", "Haladó", "Expert"]


def main():
    """Algoritmusok oldal megjelenítése."""
    
    st.title("🧩 Algoritmusok")
    st.markdown("Tanulj új algoritmusokat és böngéssz a gyűjteményben!")
    st.markdown("---")
    
    # Backend ellenőrzés
    if not api.health_check():
        st.error("❌ Backend nem érhető el!")
        return
    
    # Tabs: Böngészés és Új hozzáadása
    tab1, tab2 = st.tabs(["📚 Böngészés", "➕ Új Algoritmus"])
    
    with tab1:
        # Szűrők
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Kategória szűrő
            category_filter = st.selectbox(
                "Kategória szűrő",
                ["Összes"] + CATEGORIES,
                index=0
            )
        
        with col2:
            # Keresés
            search_query = st.text_input("🔍 Keresés név alapján", "")
        
        st.markdown("---")
        
        # Algoritmusok betöltése
        with st.spinner("Algoritmusok betöltése..."):
            if search_query:
                # Keresés
                algorithms = api.search_algorithms(search_query)
            else:
                # Szűrés kategória szerint
                selected_category = None if category_filter == "Összes" else category_filter
                algorithms = api.get_algorithms(category=selected_category)
        
        if algorithms:
            st.success(f"✅ {len(algorithms)} algoritmus találva")
            
            # Algoritmusok megjelenítése expander-ekben
            for alg in algorithms:
                with st.expander(f"**{alg['name']}** - {alg['category']} ({alg['difficulty']})"):
                    col_info, col_action = st.columns([4, 1])
                    
                    with col_info:
                        st.markdown(f"**Kategória:** {alg['category']}")
                        st.markdown(f"**Nehézség:** {alg['difficulty']}")
                        st.markdown("**Lépések:**")
                        st.code(alg['notation'], language=None)
                        st.caption(f"ID: {alg['id']} | Létrehozva: {alg['created_at'][:10]}")
                    
                    with col_action:
                        if st.button("🗑️ Törlés", key=f"delete_{alg['id']}"):
                            with st.spinner("Törlés..."):
                                success = api.delete_algorithm(alg['id'])
                            
                            if success:
                                st.success("✅ Törölve!")
                                st.rerun()
                            else:
                                st.error("❌ Hiba történt!")
        else:
            st.info("Nincs találat. Adj hozzá új algoritmusokat! ➕")
    
    with tab2:
        st.subheader("➕ Új Algoritmus Hozzáadása")
        
        with st.form("algorithm_form"):
            # Név
            name = st.text_input(
                "Algoritmus neve *",
                placeholder="pl. T-Perm, Sexy Move, stb."
            )
            
            # Kategória
            category = st.selectbox(
                "Kategória *",
                CATEGORIES
            )
            
            # Nehézség
            difficulty = st.selectbox(
                "Nehézség *",
                DIFFICULTIES
            )
            
            # Notáció
            notation = st.text_area(
                "Lépéssorozat (notáció) *",
                placeholder="R U R' U' R' F R2 U' R' U' R U R' F'",
                height=100
            )
            
            # Submit gomb
            submit = st.form_submit_button("💾 Mentés", use_container_width=True)
            
            if submit:
                # Validáció
                if not name or not notation:
                    st.error("❌ A név és a notáció mezők kötelezőek!")
                elif len(name) < 2:
                    st.error("❌ A név túl rövid!")
                elif len(notation) < 2:
                    st.error("❌ A notáció túl rövid!")
                else:
                    # Mentés
                    with st.spinner("Mentés..."):
                        result = api.create_algorithm(
                            name=name,
                            notation=notation,
                            category=category,
                            difficulty=difficulty
                        )
                    
                    if result:
                        st.success(f"✅ Algoritmus mentve: {name}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Hiba történt! Lehet, hogy már létezik ilyen nevű algoritmus.")
        
        st.markdown("---")
        
        # Tippek
        st.info("""
        💡 **Tippek algoritmus hozzáadásához:**
        - Adj egyedi nevet (pl. "T-Perm", "Sune", "Sexy Move")
        - Használj standard notációt (R, U, F, L, D, B, ', 2)
        - Válaszd ki a megfelelő kategóriát
        - A nehézségi szintet a lépések száma alapján állítsd be
        
        **Notáció példák:**
        - PLL: `R U R' U' R' F R2 U' R' U' R U R' F'`
        - OLL: `R U2 R' U' R U' R'`
        - F2L: `R U' R' U R U R'`
        """)
    
    # Statisztikák az algoritmusokról
    st.markdown("---")
    st.subheader("📊 Algoritmus Statisztikák")
    
    with st.spinner("Statisztikák számítása..."):
        all_algorithms = api.get_algorithms()
    
    if all_algorithms:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Összes algoritmus", len(all_algorithms))
        
        with col2:
            # Kategóriák száma
            categories = set(alg['category'] for alg in all_algorithms)
            st.metric("🗂️ Kategóriák", len(categories))
        
        with col3:
            # Legnépszerűbb kategória
            from collections import Counter
            category_counts = Counter(alg['category'] for alg in all_algorithms)
            most_common = category_counts.most_common(1)
            if most_common:
                st.metric("🏆 Legnépszerűbb", f"{most_common[0][0]} ({most_common[0][1]})")
    else:
        st.info("Még nincsenek algoritmusok az adatbázisban.")
    
    # Footer
    st.markdown("---")
    st.caption("Algoritmusok oldal | Folyamatosan tanulj újakat! 📚")


if __name__ == "__main__":
    main()

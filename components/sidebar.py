import streamlit as st
from pathlib import Path


def render_sidebar():

    # ==========================================
    # Logo (Optional)
    # ==========================================

    logo = Path("assets/logo.png")

    if logo.exists():

        st.sidebar.image(
            str(logo),
            use_container_width=True,
        )


    # ==========================================
    # Branding
    # ==========================================

    st.sidebar.title(
        "🩺 RenalTwin AI"
    )

    st.sidebar.caption(
        "Clinical Decision Support System"
    )


    st.sidebar.markdown("---")


    # ==========================================
    # System Information
    # ==========================================

    st.sidebar.info(
        """
### System Information

**Version:** 2.5

**AI Model:** Random Forest

**Explainability:** SHAP

**Simulation:** Digital Twin

**Dataset:** NHANES 2017–2020
"""
    )


    st.sidebar.markdown("---")


    # ==========================================
    # Status
    # ==========================================

    st.sidebar.success(
        """
System Status

🟢 AI Engine Active

🟢 Database Connected

🟢 Patient Monitoring Enabled
"""
    )


    st.sidebar.markdown("---")


    # ==========================================
    # Footer
    # ==========================================

    st.sidebar.caption(
        "© 2026 RenalTwin AI"
    )
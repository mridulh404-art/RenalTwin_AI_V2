import streamlit as st


def patient_actions():

    st.subheader("⚡ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "🩺 New Visit",
            use_container_width=True,
        ):
            st.switch_page(
                "pages/3_New_Visit.py"
            )

    with c2:

        if st.button(
            "📈 Progress",
            use_container_width=True,
        ):
            st.switch_page(
                "pages/5_Progress_Analysis.py"
            )

    with c3:

        if st.button(
            "📝 Clinical Notes",
            use_container_width=True,
        ):
            st.switch_page(
                "pages/8_Clinical_Notes.py"
            )

    with c4:

        if st.button(
            "📄 Reports",
            use_container_width=True,
        ):
            st.switch_page(
                "pages/6_Reports.py"
            )
import streamlit as st


def patient_banner(patient, latest_visit=None):

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            "### 👤 Patient"
        )

        st.write(
            patient.get(
                "Full_Name",
                "-"
            )
        )

        st.caption(
            patient.get(
                "Patient_ID",
                "-"
            )
        )


    with c2:

        st.markdown(
            "### 📋 Demographics"
        )

        st.write(
            f"{patient.get('Sex','-')} • {patient.get('Age','-')} Years"
        )

        st.caption(
            f"Physician: {patient.get('Physician','-')}"
        )


    with c3:

        st.markdown(
            "### 🩺 Latest Risk"
        )

        if latest_visit is not None:

            risk = latest_visit["Risk"]

            probability = latest_visit["Probability"]

            st.metric(
                "Risk",
                risk
            )

            st.caption(
                f"{probability:.1%}"
            )

        else:

            st.metric(
                "Risk",
                "-"
            )


    with c4:

        st.markdown(
            "### 📅 Last Visit"
        )

        if latest_visit is not None:

            st.write(
                latest_visit["Visit_Date"]
            )

            st.caption(
                latest_visit.get(
                    "Model",
                    "-"
                )
            )

        else:

            st.write("-")


    st.markdown("---")
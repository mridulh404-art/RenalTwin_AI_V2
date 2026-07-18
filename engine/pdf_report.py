from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ==========================================================
# RenalTwin AI V2
# Clinical PDF Report Generator
# ==========================================================


def generate_report(
        patient: dict,
        prediction: dict,
        output_path
):

    """
    Generate RenalTwin AI Clinical PDF Report
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    styles = getSampleStyleSheet()


    title_style = styles["Heading1"]

    title_style.alignment = TA_CENTER


    heading = styles["Heading2"]

    normal = styles["BodyText"]


    doc = SimpleDocTemplate(
        str(output_path)
    )


    story = []


    # ======================================================
    # Title
    # ======================================================

    story.append(

        Paragraph(
            "RenalTwin AI V2",
            title_style,
        )

    )


    story.append(

        Paragraph(
            "Clinical Decision Support Report",
            heading,
        )

    )


    story.append(
        Spacer(1, 20)
    )


    # ======================================================
    # Patient Information
    # ======================================================


    story.append(

        Paragraph(
            "<b>Patient Information</b>",
            heading,
        )

    )


    patient_table = [

        [
            "Patient ID",
            patient.get(
                "Patient ID",
                "-"
            )
        ],

        [
            "Name",
            patient.get(
                "Name",
                "-"
            )
        ],

        [
            "Age",
            patient.get(
                "Age",
                "-"
            )
        ],

        [
            "Sex",
            patient.get(
                "Sex",
                "-"
            )
        ],

        [
            "BMI",
            patient.get(
                "BMI",
                "-"
            )
        ],

        [
            "Systolic BP",
            patient.get(
                "SBP",
                "-"
            )
        ],

        [
            "Diastolic BP",
            patient.get(
                "DBP",
                "-"
            )
        ],

        [
            "Physician",
            patient.get(
                "Physician",
                "-"
            )
        ],

    ]


    table = Table(
        patient_table
    )


    table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0,0),
                (0,-1),
                colors.lightgrey
            ),

            (
                "BOTTOMPADDING",
                (0,0),
                (-1,-1),
                8
            ),

        ])

    )


    story.append(table)


    story.append(
        Spacer(1,20)
    )



    # ======================================================
    # AI Prediction
    # ======================================================


    story.append(

        Paragraph(
            "<b>AI Prediction</b>",
            heading,
        )

    )


    probability = prediction.get(
        "Probability",
        0
    )


    if isinstance(probability, str):

        probability_text = probability

    else:

        probability_text = f"{probability:.1%}"



    prediction_table = [

        [
            "Model",
            prediction.get(
                "Model",
                "-"
            )
        ],

        [
            "CKD Probability",
            probability_text
        ],

        [
            "Threshold",
            prediction.get(
                "Threshold",
                "-"
            )
        ],

        [
            "Risk Level",
            prediction.get(
                "Risk",
                "-"
            )
        ],

        [
            "Priority",
            prediction.get(
                "Priority",
                "-"
            )
        ],

        [
            "Follow Up",
            prediction.get(
                "Follow_Up",
                "-"
            )
        ],

    ]


    table = Table(
        prediction_table
    )


    table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0,0),
                (0,-1),
                colors.lightgrey
            ),

            (
                "BOTTOMPADDING",
                (0,0),
                (-1,-1),
                8
            ),

        ])

    )


    story.append(table)


    story.append(
        Spacer(1,20)
    )



    # ======================================================
    # Recommendations
    # ======================================================


    story.append(

        Paragraph(
            "<b>Clinical Recommendation</b>",
            heading,
        )

    )


    recommendation = prediction.get(
        "Recommendation",
        prediction.get(
            "Recommendations",
            "-"
        )
    )


    if isinstance(
        recommendation,
        list
    ):

        recommendation = "<br/>".join(
            [
                f"• {item}"
                for item in recommendation
            ]
        )


    story.append(

        Paragraph(
            str(recommendation),
            normal,
        )

    )


    story.append(
        Spacer(1,25)
    )



    # ======================================================
    # Disclaimer
    # ======================================================


    story.append(

        Paragraph(
            "<b>Disclaimer</b>",
            heading,
        )

    )


    story.append(

        Paragraph(

            "This report was generated automatically by "
            "RenalTwin AI V2. The prediction is intended "
            "to support clinical decision-making and "
            "should not replace professional medical "
            "judgment or established clinical guidelines.",

            normal,

        )

    )


    story.append(
        Spacer(1,15)
    )



    # ======================================================
    # Footer
    # ======================================================


    story.append(

        Paragraph(

            "<font size='9' color='grey'>"
            "Generated by RenalTwin AI V2 | "
            "AI-powered Clinical Decision Support System"
            "</font>",

            normal,

        )

    )


    doc.build(
        story
    )


    print(
        f"PDF saved to: {output_path}"
    )
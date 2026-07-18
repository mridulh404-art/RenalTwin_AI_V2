import pandas as pd

# ==========================================================
# Visit Comparison
# ==========================================================

def compare_visits(visits, visit1, visit2):

    first = visits[
        visits["Visit_ID"] == visit1
    ].iloc[0]

    second = visits[
        visits["Visit_ID"] == visit2
    ].iloc[0]

    metrics = [

        "Probability",

        "Mean_SBP",

        "Mean_DBP",

        "LBXSCR",

        "LBDSALSI",

        "eGFR",

        "LBXHGB",

        "SII",

    ]

    comparison = []

    for metric in metrics:

        if metric in visits.columns:

            comparison.append(

                {

                    "Metric": metric,

                    "Visit 1": first[metric],

                    "Visit 2": second[metric],

                    "Difference":
                        second[metric] - first[metric],

                }

            )

    return pd.DataFrame(comparison)

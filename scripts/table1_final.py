import pandas as pd


df = pd.read_csv(
    "data/processed/renal_twin_engineered.csv"
)


print("="*60)
print("TABLE 1: BASELINE CHARACTERISTICS")
print("="*60)


print("\nDataset size:")
print(df.shape)


# ----------------------------
# CKD Distribution
# ----------------------------

print("\nCKD Distribution")

print(
    df["CKD"]
    .value_counts()
)

print(
    df["CKD"]
    .value_counts(normalize=True)
    *100
)



# ----------------------------
# Continuous Variables
# ----------------------------

continuous = {

    "Age":
    "RIDAGEYR",

    "BMI":
    "BMXBMI",

    "Systolic BP":
    "Mean_SBP",

    "Diastolic BP":
    "Mean_DBP",

    "Creatinine":
    "LBXSCR",

    "eGFR":
    "eGFR",

}


print("\nContinuous Variables")

for name, col in continuous.items():

    print("\n",name)

    print(
        df.groupby("CKD")[col]
        .agg(
            [
                "mean",
                "std",
                "median"
            ]
        )
    )



# ----------------------------
# Categorical Variables
# ----------------------------

categorical = {


    "Sex":
    "RIAGENDR",


    "Diabetes":
    "DIQ010",


    "Smoking":
    "SMQ020",


    "Albuminuria":
    "Albuminuria",


    "CKD Stage":
    "CKD_Stage"

}



print("\nCategorical Variables")


for name,col in categorical.items():

    print("\n",name)

    print(

        pd.crosstab(

            df[col],

            df["CKD"],

            margins=True

        )

    )
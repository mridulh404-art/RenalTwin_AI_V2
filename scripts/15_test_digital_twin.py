from engine.digital_twin import simulate

patient = {

    "RIDAGEYR":65,
    "Female":1,
    "RIDRETH3":3,

    "BMXBMI":31,
    "BMXWAIST":102,

    "Mean_SBP":165,
    "Mean_DBP":95,

    "Diabetes":1,
    "Smoker":1,

    "LBXPLTSI":260,
    "LBDNENO":4.8,
    "LBDLYMNO":1.8,

    "LBXHGB":12.4,

    "SII":690,

    "LBXSCR":2.2,
    "LBDSALSI":38,

    "eGFR":40,
    "URDACT":320,
}

result = simulate(

    patient,

    {

        "Mean_SBP":125,

    },

    "Model B",

)

print(result)
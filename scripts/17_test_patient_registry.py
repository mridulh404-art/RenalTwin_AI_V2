from engine.patient_registry import register_patient

patient = {

    "Full_Name": "John Smith",

    "Date_of_Birth": "1965-02-14",

    "Age": 60,

    "Sex": "Male",

    "Phone": "0123456789",

    "Email": "john@example.com",

    "Address": "Dhaka",

    "Physician": "Dr. Ahmed",

}

patient_id = register_patient(patient)

print(patient_id)
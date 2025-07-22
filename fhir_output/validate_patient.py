import re

def validate_patient(patient_json):
    errors = []
    
    # Validate presence of 'id'
    if "id" not in patient_json or not patient_json["id"]:
        errors.append("Missing or empty 'id' field.")
    
    # Validate 'gender' if present
    valid_genders = {"male", "female", "other", "unknown"}
    gender = patient_json.get("gender")
    if gender and gender.lower() not in valid_genders:
        errors.append(f"Invalid gender value: '{gender}'. Valid values are {valid_genders}.")
    
    # Validate 'birthDate' format if present
    birthdate = patient_json.get("birthDate")
    if birthdate:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", birthdate):
            errors.append(f"Invalid birthDate format: '{birthdate}'. Expected YYYY-MM-DD.")
    
    # Validate 'name' - family and given must exist
    if "name" not in patient_json or not patient_json["name"]:
        errors.append("Missing 'name' field.")
    else:
        name_entry = patient_json["name"][0]
        if not name_entry.get("family"):
            errors.append("Missing 'family' name in 'name'.")
        given = name_entry.get("given")
        if not given or not any(given):
            errors.append("Missing 'given' name in 'name'.")
    
    # Validate 'identifier' if present
    if "identifier" in patient_json:
        for ident in patient_json["identifier"]:
            if not ident.get("value"):
                errors.append("An 'identifier' entry has empty or missing 'value'.")
    
    return errors


# Example usage
if __name__ == "__main__":
    import json

    # Load a sample patient json file
    with open("c:/Users/Quen Lynn/FHIR_SME_portfolio/fhir_output/patient.json") as f:
        patient_data = json.load(f)

    validation_errors = validate_patient(patient_data)

    if validation_errors:
        print("Validation errors found:")
        for err in validation_errors:
            print(f" - {err}")
    else:
        print("Patient resource passed all validation checks.")

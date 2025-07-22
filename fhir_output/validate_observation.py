import json
import re

def validate_observation(obs_json):
    errors = []

    # Validate 'resourceType'
    if obs_json.get("resourceType") != "Observation":
        errors.append("Invalid or missing 'resourceType'.")

    # Validate 'id'
    if "id" not in obs_json or not obs_json["id"]:
        errors.append("Missing or empty 'id' field.")

    # Validate 'status'
    if obs_json.get("status") not in ["registered", "preliminary", "final", "amended"]:
        errors.append(f"Invalid or missing 'status': {obs_json.get('status')}.")

    # Validate 'code.coding'
    if "code" not in obs_json or "coding" not in obs_json["code"]:
        errors.append("Missing 'code.coding'.")
    else:
        codings = obs_json["code"]["coding"]
        if not isinstance(codings, list) or len(codings) == 0:
            errors.append("'code.coding' must be a non-empty list.")
        else:
            for c in codings:
                if not c.get("code") or not c.get("system"):
                    errors.append("Each 'coding' entry must include 'code' and 'system'.")

    # Validate 'subject.reference'
    subject_ref = obs_json.get("subject", {}).get("reference")
    if not subject_ref or not subject_ref.startswith("Patient/"):
        errors.append("Missing or invalid 'subject.reference' (must start with 'Patient/').")

    # Validate 'valueQuantity'
    if "valueQuantity" in obs_json:
        val = obs_json["valueQuantity"].get("value")
        if val is None or not isinstance(val, (int, float)):
            errors.append("'valueQuantity.value' must be numeric.")
        if "unit" not in obs_json["valueQuantity"]:
            errors.append("Missing 'valueQuantity.unit'.")

    # Validate 'effectiveDateTime' (if present)
    effective = obs_json.get("effectiveDateTime")
    if effective:
        pattern = r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|(\+\d{2}:\d{2})))?$"
        if not re.match(pattern, effective):
            errors.append(f"Invalid 'effectiveDateTime' format: '{effective}'.")

    return errors

if __name__ == "__main__":
    # Load file
    with open("c:/Users/Quen Lynn/FHIR_SME_Portfolio/fhir_output/observation.json") as f:
        observation = json.load(f)

    # Validate
    validation_errors = validate_observation(observation)
    if validation_errors:
        print("Validation errors found in Observation resource:")
        for err in validation_errors:
            print(" -", err)
    else:
        print("Observation passed validation.")

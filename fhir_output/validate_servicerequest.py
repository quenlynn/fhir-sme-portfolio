import re

def validate_servicerequest(sr_json):
    errors = []

    # Validate 'id'
    if "id" not in sr_json or not sr_json["id"]:
        errors.append("Missing or empty 'id' field.")

    # Validate 'status' field
    if "status" not in sr_json or not sr_json["status"]:
        errors.append("Missing or empty 'status' field.")

    # Validate 'intent' field
    if "intent" not in sr_json or not sr_json["intent"]:
        errors.append("Missing or empty 'intent' field.")

    # Validate 'code.coding'
    if "code" not in sr_json or "coding" not in sr_json["code"]:
        errors.append("Missing 'code.coding' field.")
    else:
        codings = sr_json["code"]["coding"]
        if not codings or not isinstance(codings, list):
            errors.append("'code.coding' must be a non-empty list.")
        else:
            for c in codings:
                if not c.get("code"):
                    errors.append("One 'coding' entry missing 'code' field.")

    # Validate 'subject.reference'
    subject_ref = sr_json.get("subject", {}).get("reference")
    if not subject_ref:
        errors.append("Missing 'subject.reference' field.")

    # Validate 'authoredOn' date format if present
    authored_on = sr_json.get("authoredOn")
    if authored_on:
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, authored_on):
            errors.append(f"Invalid 'authoredOn' date format: '{authored_on}'. Expected YYYY-MM-DD.")

    # Validate 'requester.reference'
    requester_ref = sr_json.get("requester", {}).get("reference")
    if not requester_ref:
        errors.append("Missing 'requester.reference' field.")

    return errors

# Example usage
if __name__ == "__main__":
    import json

    with open("c:/Users/Quen Lynn/FHIR_SME_Portfolio/fhir_output/servicerequest.json") as f:
        sr_data = json.load(f)

    errs = validate_servicerequest(sr_data)

    if errs:
        print("Validation errors in ServiceRequest:")
        for e in errs:
            print(" -", e)
    else:
        print("ServiceRequest passed validation.")

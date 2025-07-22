import json
import psycopg2
from datetime import datetime

def load_single_resource(filename, expected_type):
    with open(filename, 'r') as f:
        data = json.load(f)
    if isinstance(data, dict) and data.get("resourceType") == expected_type:
        return [data]
    else:
        raise ValueError(f"Unexpected JSON structure in {filename}")

# STEP 3: Update these DB connection details with your info
conn = psycopg2.connect(
    dbname="fhir_portfolio",
    user="postgres",
    password="@1234Jaber",
    host="localhost",  
    port="5433"        
)
cur = conn.cursor()

# STEP 4: Load JSON resources
service_requests = load_single_resource("servicerequest.json", "ServiceRequest")
observations = load_single_resource("observation.json", "Observation")

# STEP 5: Insert ServiceRequest data into your servicerequest table
for sr in service_requests:
    patient_ref = sr.get("subject", {}).get("reference", "")
    patient_id = patient_ref.split("/")[-1] if "/" in patient_ref else patient_ref

    cur.execute("""
        INSERT INTO servicerequest (
            fhir_id, patient_id, code, display, status, intent,
            authored_on, requester_ref
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (fhir_id) DO NOTHING
    """, (
        sr.get("id"),
        patient_id,
        sr.get("code", {}).get("coding", [{}])[0].get("code"),
        sr.get("code", {}).get("coding", [{}])[0].get("display"),
        sr.get("status"),
        sr.get("intent"),
        datetime.fromisoformat(sr.get("authoredOn")) if sr.get("authoredOn") else None,
        sr.get("requester", {}).get("reference"),
    ))

# STEP 6: Insert Observation data into your observation table
for obs in observations:
    patient_ref = obs.get("subject", {}).get("reference", "")
    patient_id = patient_ref.split("/")[-1] if "/" in patient_ref else patient_ref

    code_coding = obs.get("code", {}).get("coding", [{}])[0]
    value_quantity = obs.get("valueQuantity", {})

    cur.execute("""
        INSERT INTO observation (
            fhir_id, patient_id, code, system, display, value, unit, effective_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (fhir_id) DO NOTHING
    """, (
        obs.get("id"),
        patient_id,
        code_coding.get("code"),
        code_coding.get("system"),
        code_coding.get("display"),
        value_quantity.get("value"),
        value_quantity.get("unit"),
        datetime.fromisoformat(obs.get("effectiveDateTime")) if obs.get("effectiveDateTime") else None,
    ))

# STEP 7: Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")

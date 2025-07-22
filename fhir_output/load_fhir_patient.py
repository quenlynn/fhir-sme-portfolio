import os
import json
import psycopg2

# PostgreSQL connection parameters
db_params = {
    "dbname": "fhir_portfolio",
    "user": "postgres",
    "password": "@1234Jaber",  # Replace with your actual password
    "host": "localhost",
    "port": "5433"
}

# File paths
observation_file = "fhir_output/observation.json"
servicerequest_file = "fhir_output/servicerequest.json"

def load_observations(cursor):
    if not os.path.exists(observation_file):
        print(f"Observation file not found: {observation_file}")
        return

    with open(observation_file) as f:
        data = json.load(f)

    for obs in data if isinstance(data, list) else [data]:
        fhir_id = obs.get("id")
        subject_ref = obs.get("subject", {}).get("reference", "").split("/")[-1]
        code = obs.get("code", {}).get("coding", [{}])[0].get("code")
        system = obs.get("code", {}).get("coding", [{}])[0].get("system")
        display = obs.get("code", {}).get("coding", [{}])[0].get("display")
        value = obs.get("valueQuantity", {}).get("value")
        unit = obs.get("valueQuantity", {}).get("unit")
        effective_datetime = obs.get("effectiveDateTime")

        cursor.execute("""
            INSERT INTO observation (
                fhir_id, subject_ref, code, system, display, value, unit, effective_datetime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (fhir_id, subject_ref, code, system, display, value, unit, effective_datetime))

def load_servicerequests(cursor):
    if not os.path.exists(servicerequest_file):
        print(f"ServiceRequest file not found: {servicerequest_file}")
        return

    with open(servicerequest_file) as f:
        data = json.load(f)

    for sr in data if isinstance(data, list) else [data]:
        fhir_id = sr.get("id")
        status = sr.get("status")
        intent = sr.get("intent")
        code = sr.get("code", {}).get("coding", [{}])[0].get("code")
        display = sr.get("code", {}).get("coding", [{}])[0].get("display")
        subject_ref = sr.get("subject", {}).get("reference", "").split("/")[-1]
        authored_on = sr.get("authoredOn")
        requester_ref = sr.get("requester", {}).get("reference", "").split("/")[-1]

        cursor.execute("""
            INSERT INTO servicerequest (
                fhir_id, status, intent, code, display, subject_ref, authored_on, requester_ref
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (fhir_id, status, intent, code, display, subject_ref, authored_on, requester_ref))


# Run both loaders
try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    load_observations(cursor)
    load_servicerequests(cursor)
    conn.commit()
    print("✅ Observation and ServiceRequest data loaded successfully.")
except Exception as e:
    print("❌ Error:", e)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

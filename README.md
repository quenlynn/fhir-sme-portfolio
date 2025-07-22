# FHIR SME Portfolio (HL7-FHIR-PostgreSQL)
This portfolio demonstrates a manual HL7-to-FHIR transformation pipeline using Python and PostgreSQL. It reflects real-world healthcare data interoperability skills without the use of an interface engine like Mirth.

# Objective
Transform HL7v2 messages (ADT, ORU, ORM) into FHIR-compliant JSON resources.
Load FHIR resources into a structured PostgreSQL database.
Query and analyze clinical data with SQL.

# Technology
Python (json, psycopg2)
PostgreSQL
Postman (for testing FHIR API endpoints)
Synthea (for generating synthetic HL7 data)


# Folder Overview
Folder                      	| Description 
hl7_messages		 	| Raw HL7v2 messages (ADT, ORU, ORM) 
fhir_output			| Converted FHIR JSON resources (Patient, Observation, ServiceRequest) 
python_loaders			| Python scripts to insert FHIR JSON into the database 
db_scripts			| SQL scripts to create schema and run queries 
postman			        | Postman collection for testing resource posting (optional) 

#Database Schema
patient (fhir_id, name, birthDate, gender)
observation (id, patient_id → patient.fhir_id, code, value, date)
servicerequest (id, patient_id → patient.fhir_id, code, status, date)

Relationships are enforced using foreign key constraints on `patient_id`.


# Workflow
1. HL7 messages were created using Synthea.
2. Messages were converted to FHIR JSON format following US Core standards.
3. Python scripts(`load_patient.py`, etc.) parsed and inserted JSON data into PostgreSQL.
4. SQL queries were used for basic reporting and validation.

# SQL Analysis Examples
Count of patients by gender
Number of service requests per patient
Observation value ranges (e.g., height, blood pressure)

# Data Quality Practices
Primary and foreign key validation
Field-level integrity (date formats, value types)
FHIR resource verification for conformance

Built by Quen 
FHIR Integration | HL7 v2 | Data Analysis | Python | PostgreSQL

def parse_ack_message(message):
    lines = message.strip().split('\n')
    msa_line = next((line for line in lines if line.startswith('MSA')), None)
    
    if not msa_line:
        return "Invalid ACK format – MSA segment missing."

    fields = msa_line.split('|')
    ack_code = fields[1]
    control_id = fields[2]
    error_msg = fields[3] if len(fields) > 3 else ""

    if ack_code == "AA":
        return f"✅ ACK received for message control ID {control_id}."
    elif ack_code == "AE":
        return f"❌ Application Error (AE) for ID {control_id}: {error_msg}"
    elif ack_code == "AR":
        return f"❌ Application Reject (AR) for ID {control_id}: {error_msg}"
    else:
        return f"⚠️ Unknown ACK code '{ack_code}' for message ID {control_id}."

# Example usage
if __name__ == "__main__":
    with open("ack_sample.hl7", "r") as f:
        ack_message = f.read()
    result = parse_ack_message(ack_message)
    print(result)

    with open("nack_sample.hl7", "r") as f:
        nack_message = f.read()
    result = parse_ack_message(nack_message)
    print(result)

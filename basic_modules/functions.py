import requests
import json
import base64
from cryptography.fernet import Fernet

def create_ticket(company, public_key, private_key, domain, clientid, board_id, company_id, ticket_summary, ticket_content, encryption_key):
    # Define the API endpoint
    endpoint = f"https://{domain}/v4_6_release/apis/3.0/service/tickets/"

    # Define the ticket details
    ticket = {
        "summary": ticket_summary,
        "initialDescription": ticket_content,
        "board": {
            "id": board_id  # Replace with your board ID
        },
        "company": {
            "id": company_id,
        }
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(ticket)

    # Construct the Basic authentication header
    auth_string = f"{company}+{public_key}:{private_key}"
    auth_header = f"Basic {base64.b64encode(auth_string.encode()).decode()}"

    # Send the request to create the ticket
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header,
        "clientid": clientid
    }
    response = requests.post(endpoint, data=json_data, headers=headers)

    # Check the response status code
    if response.status_code == 201:
        print("Ticket created successfully!")
        return "Ticket created successfully! Check your board to ensure it's there, then hit save to save these settings."
    else:
        print(f"Error creating ticket: {response.content}")
        return f"Error creating ticket: {response.content}"

def send_monitor_notification(ntfy_monitor, message, cw_ticket):
    requests.post(ntfy_monitor, data=message.encode(encoding='utf-8'))

    if cw_ticket:  # If cw_ticket is not empty
        create_ticket(**cw_ticket)
    
def send_alert_notification(ntfy_alert, message):
    requests.post(ntfy_alert, data=message.encode(encoding='utf-8'))

if __name__ == "__main__":
    pass


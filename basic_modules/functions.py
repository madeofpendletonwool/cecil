import requests
import json
import base64

def create_ticket(company, public_key, private_key, domain, clientid, board_id, company_id):
    # Define the API endpoint
    endpoint = f"https://{domain}/v4_6_release/apis/3.0/service/tickets/"

    # Define the ticket details
    ticket = {
        "summary": "This is a test ticket created by CECIL!",
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

if __name__ == "__main__":
    pass
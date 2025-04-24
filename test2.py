import msal
import requests

# Azure app credentials (from your app.py)
CLIENT_ID = "e660f5df-830b-4197-b538-f89129763062"
CLIENT_SECRET = "lPJ8Q~MJCu_0ghkGZcrJBDLbHRXKh61uVh5cybJ3"
TENANT_ID = "46d6a910-c309-42a3-8144-6fa061daf05f"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Teams app details (from your app.py)
TEAMS_APP_ID = "e660f5df-830b-4197-b538-f89129763062"
ENTITY_ID = "ticketingTab"

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Could not obtain access token: {result.get('error_description')}")

def send_teams_notification(ticket_id, user_id):
    access_token = get_access_token()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/teamwork/sendActivityNotification"
    payload = {
        "topic": {
            "source": "text",
            "value": "Test Notification",
            "webUrl": f"https://teams.microsoft.com/l/entity/{TEAMS_APP_ID}/{ENTITY_ID}"
        },
        "activityType": "testNotification",
        "previewText": {
            "content": f"This is a test notification for ticket ID: {ticket_id}"
        },
        "recipient": {
            "@odata.type": "microsoft.graph.aadUserNotificationRecipient",
            "userId": user_id
        }
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    # if response.status_code != 202:
    #     raise Exception(f"Failed to send notification: {response.text}")
    # print("Notification sent successfully!")

if __name__ == "__main__":
    TEST_USER_ID = "3a971bab-cb9c-4f1c-a36a-051f5ddbd339"
    TEST_TICKET_ID = 16

    try:
        send_teams_notification(TEST_TICKET_ID, TEST_USER_ID)
    except Exception as e:
        print(f"Error: {e}")
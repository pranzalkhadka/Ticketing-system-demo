import msal
import os
import requests

# Azure app credentials (from your app.py)
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
TEAMS_APP_ID = os.getenv("TEAMS_APP_ID")

# Teams app details (from your app.py)
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
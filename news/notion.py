import requests
import json

# Your Notion integration's secret key
notion_key = 'secret_YOUR_NOTION_KEY'

# The ID of the database you want to add a row to
database_id = 'YOUR_DATABASE_ID'

# The data for the new row
new_row_data = {
    'parent': {'database_id': database_id},
    'properties': {
        'Name': {
            'title': [
                {
                    'text': {
                        'content': 'New row',
                    },
                },
            ],
        },
        'Description': {
            'rich_text': [
                {
                    'text': {
                        'content': 'This is a new row',
                    },
                },
            ],
        },
    },
}

# The headers for the API request
headers = {
    'Authorization': f'Bearer {notion_key}',
    'Content-Type': 'application/json',
    'Notion-Version': '2021-08-16',
}

# Send the API request
response = requests.post(
    'https://api.notion.com/v1/pages',
    headers=headers,
    data=json.dumps(new_row_data),
)

# Check if the request was successful
if response.status_code == 200:
    print('Row added successfully')
else:
    print(f'Failed to add row: {response.text}')
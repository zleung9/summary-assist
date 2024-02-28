import os
from notion_client import Client
import json

# The ID of the database is the first UUID after the slash.
# for example: https://www.notion.so/zleung/4af538f372fa4ac39ec69aeb04be2020?v=6423a31d633248bfb456a5ead527f23c&pvs=4
# database ID is 4af538f372fa4ac39ec69aeb04be2020
# For production the workspace is Oliver's and the database address is: 
# https://www.notion.so/5f120796c787424b8c768cc179c94093?v=86bca37702c0489c904a1d5bf04aa940&pvs=4
NOTION_KEY = os.getenv("NOTION_SECRET")
DATABASE_ID = "5f120796c787424b8c768cc179c94093"
NOTION_KEY_TEST = os.getenv("NOTION_SECRET_TEST")
DATABASE_ID_TEST = '4af538f372fa4ac39ec69aeb04be2020'


def safe_get(data, dot_chained_keys):
    '''
        data = {'a': {'b': [{'c': 1}]}};  safe_get(data, 'a.b.0.c') -> 1
        Ref: https://www.youtube.com/watch?v=rQeG6DeUPNs&list=PLS_o2ayVCKvDwzhB-wdzBTvpQwgArrHlY&index=4
    '''
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


def write_content_to_file(content, file_name):
    json_content = json.dumps(content)
    with open(file_name, 'w') as f:
        f.write(json_content)


def write_row(
        client, 
        database_id,
        entry: int,
        episode: int = None,
    ):
    '''
        Write a new row to the database.
    '''
    client.pages.create(
        parent={"database_id": database_id},
        properties={
            "episode":{
                "number": episode,
            },
            "title": {
                "title": [
                    {
                        "text": {
                            "content": entry["title"]
                        }
                    }
                ]
            },
            "body": {
                "rich_text": [
                    {
                        "text": {
                            "content": entry["body"]
                        }
                    }
                ]
            },
            "category": {
                "select": {
                    "name": " " if not entry["category"] else entry["category"]
                }
            },
            "source": {
                "url": entry["source"]
            },
            "date": {
                "date": {
                    "start": "2024-01-01" if not entry["date"] else entry["date"]
                }
            },
            "topics": {
                "multi_select": [
                    {"name": topic} for topic in entry["topics"]
                ]
            }
        }
    )
    

def simple_rows(db_rows):
    """Convert the notion database rows to a simple format."""
    simple_rows = []
    for row in db_rows["results"]:
        simpe_row = {
            "episode": safe_get(row, "properties.episode.number"),
            "title": safe_get(row, "properties.title.title.0.plain_text"),
            "body": safe_get(row, "properties.body.rich_text.0.plain_text"),
            "category": safe_get(row, "properties.category.select.name"),
            "source": safe_get(row, "properties.source.url"),
            "date": safe_get(row, "properties.date.date.start"),
            "topics": ",".join([safe_get(topic, f"name") for topic in safe_get(row, "properties.topics.multi_select")])
        }
        simple_rows.append(simpe_row)
    return simple_rows
    

def main():
    # Initialize the client
    client = Client(auth=NOTION_KEY)
    db_rows = client.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "episode",
            "number": {
                "equals": 37
            }
        }
    )
    
    write_content_to_file(db_rows, 'notion.json')
    write_content_to_file(simple_rows(db_rows), 'notion_simple.json')

    # row = {
    #     "title": "CEO Romi Mahajan Advises Private Fusion Industry",
    #     "body": "Romi Mahajan, CEO of ExoFusion, provides insights on four key factors shaping the future of private fusion energy industry. He emphasizes the essential role of scientific understanding, the need for realistic timelines, the importance of governmental support, and the value of a collaborative ecosystem.",
    #     "category": "Industry",
    #     "source": "https://fusionenergyinsights.com/blog/post/opinion-four-admonitions-for-private-sector-fusion-companies#:~:text=Opinion%3A",
    #     "date": "2024-01-11",
    #     "topics": [
    #         "Topic B",
    #         "Topic C"
    #     ],
    #     "episode": 1
    # }

    # rows = json.load(open('notion_simple.json', 'r'))
    # for row in rows:
    #     write_row(client, DATABASE_ID, row)

if __name__ == '__main__': 
    main()
from notion_client import Client
import json

# Your Notion integration's secret key
NOTION_KEY = 'secret_ObTGTqjP17h0N9RDhd4YPbIxj6abqVvZVcaHJj8KTh0'

# The ID of the database is the first UUID after the slash.
# for example: https://www.notion.so/zleung/4af538f372fa4ac39ec69aeb04be2020?v=6423a31d633248bfb456a5ead527f23c&pvs=4
# database ID is 4af538f372fa4ac39ec69aeb04be2020
DATABASE_ID = '4af538f372fa4ac39ec69aeb04be2020'


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
        episode: int=None,
        title: str=None,
        body: str=None,
        category: str=None,
        source: str=None,
        date: str=None,
        topics: list=None 
    ):
    '''
        Write a new row to the database.
    '''
    client.pages.create(
        parent={"database_id": database_id},
        properties={
            "episode":{
                "number": episode
            },
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "body": {
                "rich_text": [
                    {
                        "text": {
                            "content": body
                        }
                    }
                ]
            },
            "category": {
                "select": {
                    "name": category
                }
            },
            "source": {
                "url": source
            },
            "date": {
                "date": {
                    "start": date
                }
            },
            "topics": {
                "multi_select": [
                    {"name": topic} for topic in topics
                ]
            }
        }
    )



def main():
    # Initialize the client
    client = Client(auth=NOTION_KEY)

    db_info = client.databases.retrieve(database_id=DATABASE_ID)
    db_rows = client.databases.query(
        database_id=DATABASE_ID, 
        filter={
            "property": "body",
            "rich_text": {
                "is_empty": True
            }
        }
    )
    
    write_content_to_file(db_rows, 'notion.json')

    simple_rows = []
    for row in db_rows["results"]:
        simpe_row = {
            "episode": safe_get(row, "properties.episode.number"),
            "title": safe_get(row, "properties.title.title.0.plain_text"),
            "body": safe_get(row, "properties.body.rich_text.0.plain_text"),
            "category": safe_get(row, "properties.category.select.name"),
            "source": safe_get(row, "properties.source.url"),
            "date": safe_get(row, "properties.date.date.start"),
            "topics": [safe_get(topic, f"name") for topic in safe_get(row, "properties.topics.multi_select")]
        }
        simple_rows.append(simpe_row)

    write_content_to_file(simple_rows, 'notion_simple.json')

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
    #     write_row(client, DATABASE_ID, **row)

if __name__ == '__main__': 
    main()
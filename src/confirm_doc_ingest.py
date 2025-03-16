import weaviate
import os

# Initialize Weaviate client
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Ensure your API key is set
    }
)

try:
    collection = client.collections.get("PolicyDocument")
    for item in collection.iterator():
        print(item.uuid, item.properties["title"])

finally:
    client.close()

import weaviate
import os

# # Initialize Weaviate client
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Ensure your API key is set
    }
)

try:
    collection = client.collections.get("PolicyDocument")
    response = collection.generate.near_text(
        query="colorado",
        limit=2,
        grouped_task="Write a two sentence summary on the management of the Colorado River. Include which states are impacted.",
    )
    print(response.generated)
finally:
    client.close()

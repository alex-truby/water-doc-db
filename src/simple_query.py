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
        query="LBT",
        limit=2,
        grouped_task="How many acre feet of water does Littlefoot get access to on the Stegosaurus River?"
    )
    print(response.generated) 
    response = collection.generate.near_text(
        query="LBT",
        limit=2,
        grouped_task="Who is impacted by the Stegosaurus River Water Rights Agreement?"
    )
    print(response.generated) 
finally:
    client.close()




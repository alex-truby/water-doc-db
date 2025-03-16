import weaviate
import weaviate.classes as wvc
import os
import json

# # Initialize Weaviate client
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Ensure your API key is set
    }
)

try:
    collection = client.collections.get("PolicyDocument")

    # Simple query - find document titles related to 'Colorado'
    simple_query_response = collection.query.near_text(
        query="colorado",
        distance=0.25,
        return_metadata=wvc.query.MetadataQuery(distance=True)
    )

    print(f"There are {len(simple_query_response.objects)} related to your search.")

    print('Related documents: ')

    for o in simple_query_response.objects:  # View by object
        # print(o.metadata) # TODO: currently, only distance is calculated
        print('    * ', o.properties['title'], f" ({o.properties['policyType']})")

    print('-' * 80)

    # Test gen response 1 - can it reference a made up water rights document not on the WWW?
    task_1_text = "How many acre feet of water does Littlefoot get access to on the Stegosaurus River?"
    response = collection.generate.near_text(
        query="LBT",
        distance = 0.3,
        # return_metadata=wvc.query.MetadataQuery(distance=True), # TODO: Implement methodology to improve distance metrics and filtering
        grouped_task=task_1_text
    )

    print("Task: ", task_1_text)
    print("The following documents were used to generate this response: ")
    for obj in response.objects:
        print('    * ', obj.properties['title'])
    print(response.generated) 
    print('-' * 80)

    # Test gen response 2 - can it correctly identify who is impacted by the made up agreement?
    task_2_text = "Who is part of the Stegosaurus River Water Rights Agreement?"
    response = collection.generate.near_text(
        query="Stegosaurus River",
        distance = 0.2,
        grouped_task=task_2_text
    )
    print("Task: ", task_2_text)
    print("The following documents were used to generate this response: ")
    for obj in response.objects:
        print('    * ', obj.properties['title'])
    print(response.generated) 
finally:
    client.close()


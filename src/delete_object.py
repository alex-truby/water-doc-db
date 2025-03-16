import weaviate

# Initialize Weaviate client
client = weaviate.connect_to_local()

uuid_to_delete = input("Enter uuid of the object you want to delete: ").strip()

try:
    collection = client.collections.get("PolicyDocument")
    collection.data.delete_by_id(uuid_to_delete)
    print("Successfully delete object with uuid: {uuid_to_delete}")
finally:
    client.close()

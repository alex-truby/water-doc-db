import weaviate

client = weaviate.connect_to_local()

print(client.is_ready())  # Should print: `True`

client.close()  # Free up resources
import weaviate
import weaviate.classes as wvc
import os

client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.environ[
            "OPENAI_APIKEY"
        ]  # Your OpenAI API key must be set in the environment
    }
)


try:
    policy_documents = client.collections.create(
        name="PolicyDocument",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            wvc.config.Property(
                name="title",
                data_type=wvc.config.DataType.TEXT,
            ),
            wvc.config.Property(
                name="content",
                data_type=wvc.config.DataType.TEXT,
            ),
            wvc.config.Property(
                name="country",
                data_type=wvc.config.DataType.TEXT_ARRAY,
                # input_type=list,   # Allow multiple countries
            ),
            wvc.config.Property(
                name="state",
                data_type=wvc.config.DataType.TEXT_ARRAY,
                # is_array=True,   # Allow multiple states
            ),
            wvc.config.Property(
                name="policyType",
                data_type=wvc.config.DataType.TEXT_ARRAY,
                # is_array=True,   # Allow multiple policy types
            ),
        ],
        generative_config=wvc.config.Configure.Generative.openai(),
    )

    # Print out the full configuration for verification
    print(policy_documents.config.get(simple=False))

finally:
    client.close()

# # to delete a class
# client.collections.delete("PolicyDocument")
# client.close()

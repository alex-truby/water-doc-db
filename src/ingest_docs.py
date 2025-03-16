import os
import weaviate
import PyPDF2

# Initialize Weaviate client
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.environ[
            "OPENAI_APIKEY"
        ]  # Your OpenAI API key must be set in the environment
    }
)


def extract_text_from_pdf(pdf_path):
    text = ""
    title = None
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # Attempt to extract title from PDF metadata
            if reader.metadata and "/Title" in reader.metadata:
                title = reader.metadata["/Title"]
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return title, text


def ingest_pdf(pdf_path):
    print(f"\nProcessing file: {pdf_path}")
    file_name = os.path.basename(pdf_path)
    title, content = extract_text_from_pdf(pdf_path)
    if not title:
        title = os.path.splitext(file_name)[0]
        print("No title metadata found, using file name as title.")
    else:
        print(f"Extracted title: {title}")

    # Prompt user for metadata
    country = input("Enter country for this document: ").strip()
    state = input("Enter state for this document: ").strip()
    policyType = input("Enter policy type for this document: ").strip()

    data_object = {
        "title": title,
        "content": content,
        "country": country,
        "state": state,
        "policyType": policyType,
    }

    try:
        client.data_object.create(data_object, class_name="PolicyDocument")
        print(f"Successfully ingested {file_name}")
    except Exception as e:
        print(f"Error ingesting {file_name}: {e}")


def main():
    # Path to the directory containing PDF policy documents
    pdf_directory = os.path.join(os.path.dirname(__file__), "..", "data", "policies")
    if not os.path.exists(pdf_directory):
        print(
            f"Directory {pdf_directory} does not exist. Please create it and add PDF files."
        )
        return

    # Iterate through PDF files in the directory
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            ingest_pdf(pdf_path)


if __name__ == "__main__":
    main()

import os
import weaviate
import PyPDF2
import re
import click


def extract_text_from_pdf(pdf_path):
    text = ""
    title = None
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if reader.metadata and "/Title" in reader.metadata:
                # title = reader.metadata['/Title']
                title = reader.metadata["/Title"]
                # Clean up the title
                title = title.strip()
                # Remove trailing .pdf or .PDF using regex
                title = re.sub(r"\.pdf$", "", title, flags=re.IGNORECASE)
                title = title.replace(".PDF", "")
                # Replace hyphens and underscores with spaces
                title = title.replace("-", " ").replace("_", " ")
                # Collapse multiple spaces into a single space
                title = " ".join(title.split())
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return title, text


def ingest_pdf(client, pdf_path, collection):  # Pass the client as an argument
    print(f"\nProcessing file: {pdf_path}")
    file_name = os.path.basename(pdf_path)
    title, content = extract_text_from_pdf(pdf_path)
    if not title:
        print("No title metadata found, please manually input a title.")
        title = input("Enter title for this document: ").strip()
    else:
        print(f"Extracted title: {title}")

    country_input = input(
        "Enter country/countries for this document (comma-separated): "
    ).strip()
    state_input = input("Enter state(s) for this document (comma-separated): ").strip()
    policyType_input = input(
        "Enter policy type(s) for this document (comma-separated): "
    ).strip()

    countries = [x.strip() for x in country_input.split(",") if x.strip()]
    states = [x.strip() for x in state_input.split(",") if x.strip()]
    policyTypes = [x.strip() for x in policyType_input.split(",") if x.strip()]

    data_object = {
        "title": title,
        "content": content,
        "country": countries,
        "state": states,
        "policyType": policyTypes,
    }

    try:
        with collection.batch.dynamic() as batch:
            batch.add_object(data_object)
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                exit
        print(f"Successfully ingested {file_name}")
    except Exception as e:
        print(f"Error ingesting {file_name}: {e}")


@click.command()
@click.option(
    "--ingest_mode",
    "-i",
    type=str,
    help="'single' or 'all' files in policy docs folder.",
)
def cli(ingest_mode):
    client = weaviate.connect_to_local(
        headers={"X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]}
    )

    collection = client.collections.get("PolicyDocument")

    pdf_directory = os.path.join(os.path.dirname(__file__), "..", "data", "policy_docs")
    if not os.path.exists(pdf_directory):
        print(
            f"Directory {pdf_directory} does not exist. Please create it and add PDF files."
        )
        return
    if ingest_mode == "single":
        filename = input("Enter filename of document to upload: ").strip()
        try:
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(pdf_directory, filename)
                ingest_pdf(
                    client, pdf_path, collection
                )  # Pass the client to ingest_pdf
        except:
            print(
                "Filepath does not exist. Please ensure the file to upload is in PDF format in data/policy_docs."
            )
    else:
        for filename in os.listdir(pdf_directory):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(pdf_directory, filename)
                ingest_pdf(
                    client, pdf_path, collection
                )  # Pass the client to ingest_pdf
    client.close()


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        print(f"An error occurred: {e}")

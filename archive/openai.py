from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Create client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Send request
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello world :)"
)

print(response.output_text)
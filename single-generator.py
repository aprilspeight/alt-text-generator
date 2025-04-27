import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load env variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image_to_data_url(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }.get(ext, "image/jpeg")
    return f"data:{mime_type};base64,{base64_image}"

def generate_single_alt_text(image_path):
    try:
        data_url = encode_image_to_data_url(image_path)
        message_content = [
            {"role": "system", "content": "You are a helpful assistant specialized in creating accessible alt text for images."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": (
                        "Generate concise alt text under 300 characters for this image. "
                        "If it's a UI screenshot, mention the key interface parts and important actions."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": data_url}
                }
            ]}
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=message_content,
            max_tokens=80
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    image_path = "./sample-image.jpeg"  # Change this path to your test image
    alt_text = generate_single_alt_text(image_path)
    if alt_text:
        print(f"\nGenerated Alt Text:\n{alt_text}\n")

import os
import argparse
import base64
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def encode_image_to_data_url(image_path):
    """Encode an image file to a base64 data URL."""
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

def generate_alt_text(model_name, image_path):
    """Generate alt text for an image using OpenAI API."""
    try:
        data_url = encode_image_to_data_url(image_path)

        message_content = [
            {"role": "system", "content": "You are a helpful assistant specialized in creating accessible alt text for images."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": (
                        "Generate a concise and descriptive alt text for this image. "
                        "If the image is a screenshot of a digital interface (such as a website, app, or software tool), "
                        "describe the main area, key visible options or buttons, and any highlighted elements. "
                        "Focus on what a user would need to understand without seeing it. "
                        "Keep the description under 300 characters."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": data_url}
                }
            ]}
        ]

        # Try to call OpenAI API with retry on rate limit
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=message_content,
                    max_tokens=80
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < 2:
                    print("Rate limited, retrying...")
                    time.sleep(5 * (attempt + 1))
                else:
                    raise e

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def create_markdown_header(output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Image Alt Text Results\n\n")
        f.write("Generated on: " + time.strftime("%Y-%m-%d at %H:%M:%S") + "\n\n")
        f.write("| Image File | Alt Text |\n")
        f.write("|------------|----------|\n")

def append_to_markdown(output_file, image_path, alt_text):
    with open(output_file, 'a', encoding='utf-8') as f:
        rel_path = os.path.basename(image_path)
        safe_alt_text = alt_text.replace('|', '\\|')
        f.write(f"| {rel_path} | {safe_alt_text} |\n")

def process_folder(folder_path, model_name, output_file, extensions=['.jpg', '.jpeg', '.png', '.gif', '.webp']):
    results = {}
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist")
        return
    
    image_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                image_files.append(os.path.join(root, file))
    
    print(f"Found {len(image_files)} images to process")
    create_markdown_header(output_file)
    
    for i, image_path in enumerate(image_files):
        print(f"Processing {i+1}/{len(image_files)}: {image_path}")
        alt_text = generate_alt_text(model_name, image_path)
        
        if alt_text:
            results[image_path] = alt_text
            print(f"Generated alt text: {alt_text}")
            append_to_markdown(output_file, image_path, alt_text)
        
        time.sleep(2)  # Delay to avoid rate limits
    
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\n\n## Summary\n\n")
        f.write(f"- Total images processed: {len(image_files)}\n")
        f.write(f"- Successfully generated alt text: {len(results)}\n")
        f.write(f"- Failed: {len(image_files) - len(results)}\n")

def main():
    parser = argparse.ArgumentParser(description='Generate alt text for images in a folder using OpenAI API')
    parser.add_argument('folder', help='Path to the folder containing images')
    parser.add_argument('--output', default='alt_text_results.md', help='Output markdown file name')
    parser.add_argument('--extensions', default='.jpg,.jpeg,.png,.gif,.webp', help='Comma-separated list of image extensions')
    args = parser.parse_args()

    model_name = "gpt-4o"
    extensions = args.extensions.split(',')

    process_folder(args.folder, model_name, args.output, extensions)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()

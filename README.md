# <p align="center">Alt-Text Generator</p>

![Illustration of a Gen AI Alt-Text Generator. The left side describes its function: generating alt text for image sets using Python and OpenAI. An arrow points from an image icon to a document icon, indicating the process of converting images to text and organizing them in a markdown file.](alt-text-generator.png)

Need to generate alt-text for a bulk set of images? This sample provides a basic alt-text generator that iterates over images in a specified folder, converts each image to base64 data URL, generates alt-text for each converted image, and then organizes everything into a markdown file - providing both the file name and alt-text!

*Note: If you only need to generate alt-text for a single image, check out the [Single Generator](https://github.com/aprilspeight/alt-text-generator/blob/main/single-generator.py).*

## ✅ Requirements

- [OpenAI API](https://platform.openai.com/signup) access
- Code editor ([Visual Studio Code](https://code.visualstudio.com/) is always a fabulous choice!)

## Run the Script
1. Make sure your .env file is set up with your `OPENAI_API_KEY`.
1. Open a terminal in the project directory.
1. Run `pip install -r requirements.txt` to install dependencies.
1. Run the script by providing the path to the folder with your images:
`python alt-text-v2.py ./images`
(You can replace ./images with any folder path you want.)

## 📦 Resources

- [OpenAI Developer Docs](https://platform.openai.com/docs/overview)

## 🚨 Contact

Have a question or issue trying the sample? Submit an issue to the repo!



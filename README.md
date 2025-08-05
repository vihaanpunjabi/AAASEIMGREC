# Image Recognition

Analyze images using Google's Gemini API.

## Setup

1. Clone repo
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your Google API key

## Usage

```python
from sample import analyze_image

# Basic usage
result = analyze_image("image.jpg", "Describe this image")
print(result)

# With structured output
from pydantic import BaseModel

class ImageAnalysis(BaseModel):
    label: str

result = analyze_image("image.jpg", "What is this?", ImageAnalysis)
print(result)
```

## Files

- `sample.py` - Main function
- `prompts/prompt.md` - Default prompt
- `requirements.txt` - Dependencies
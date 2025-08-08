
#!/usr/bin/env python3
"""
================================================================================
E-WASTE IMAGE ANALYZER - Simple Version
================================================================================
This program looks at pictures of electronic waste and tells you if it's safe
to shred them or not. It's like having an expert look at your old electronics!

How it works:
1. You give it a folder with pictures
2. It looks at each picture using Google's AI
3. It tells you if each item is safe to shred
4. It shows you all results in a nice table
================================================================================
"""

# Import the tools we need
import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Google's AI library for analyzing images
try:
    import google.generativeai as genai
except ImportError:
    print("Error: Please install the required library:")
    print("   pip install google-generativeai")
    sys.exit(1)

# Load settings from .env file (this is where your API key lives)
load_dotenv()

# ============================================================================
# CONFIGURATION - These are settings you can change
# ============================================================================

# Get your Google API key from the .env file
API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if we have an API key
if not API_KEY:
    print("\nERROR: No Google API key found!")
    print("\nHow to fix this:")
    print("1. Create a file called '.env' in this folder")
    print("2. Add this line to it: GOOGLE_API_KEY=your_actual_key_here")
    print("3. Get a free key from: https://makersuite.google.com/app/apikey")
    sys.exit(1)

# Set up Google's AI with our key
genai.configure(api_key=API_KEY)

# What types of image files we can analyze
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']



class SimpleEWasteAnalyzer:
    """
    This is our main analyzer. Think of it like a smart assistant that
    looks at pictures and tells you about the electronic waste in them.
    """
    
    def __init__(self):
        """Set up the analyzer when we create it"""
        
        # This is Google's AI model - like choosing which expert to consult
        self.ai_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Instructions we give to the AI about what to look for
        with open("prompt.md", 'r') as f:
            self.instructions = f.read()
        
        # This tells the AI exactly what format we want the answer in
        self.response_format = {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "What is this item?"
                },
                "safety_level": {
                    "type": "string",
                    "enum": ["Safe to Shred", "Requires Preprocessing", "Do Not Shred", "Discard"],
                    "description": "Can we shred it?"
                },
                "hazards": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of dangerous parts"
                },
                "notes": {
                    "type": "string", 
                    "description": "Any warnings or special instructions"
                }
            },
            "required": ["item_name", "safety_level", "hazards", "notes"]
        }
    
    def analyze_one_image(self, image_path: Path, item_num: int, total: int) -> Dict:
        """
        Analyze a single image and return the results
        
        Args:
            image_path: The location of the image file
            item_num: The item number for display
            total: Total number of images
            
        Returns:
            A dictionary with the analysis results
        """
        
        result = {
            "filename": image_path.name,
            "item_num": item_num,
            "item_name": "Unknown",
            "safety_level": "Do Not Shred",  # Default to safe option
            "hazards": [],
            "notes": "",
            "error": None
        }
        
        try:
            # Step 1: Upload the image to Google
            uploaded_image = genai.upload_file(str(image_path))
            
            # Step 2: Ask the AI to analyze it
            response = self.ai_model.generate_content(
                [self.instructions, uploaded_image],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=self.response_format,
                    temperature=0.1  # Makes answers more consistent
                )
            )
            
            # Step 3: Get the answer and save it
            ai_answer = json.loads(response.text)
            result.update(ai_answer)
            
        except Exception as error:
            # If something goes wrong, save the error
            result["error"] = str(error)
            print(f"\nFailed to process {image_path.name}: {error}\n")
        
        return result

# ============================================================================
# HELPER FUNCTIONS - These make the output look nice
# ============================================================================

def print_single_result(result: Dict):
    """
    Print the result for one image in the original format
    
    Args:
        result: The analysis results for one image
    """
    
    print(f"""
    ====================================================================

        ITEM {result['item_num']}: ({result['filename']})

        Item: {result['item_name']}
        Shred Safety: {result['safety_level']}""")
    
    # Only show hazards if item is not safe to shred directly
    if result['safety_level'] in ["Do Not Shred", "Requires Preprocessing"]:
        if result['hazards']:
            print(f"        Hazards Present: {', '.join(result['hazards'])}")
    
    if result['notes'] and result['item_name'] != "Unknown":
        print(f"        Notes: {result['notes']}")
    
    print("\n    ====================================================================")

def print_summary(all_results: List[Dict], processing_time: float):
    """
    Print a summary of all results
    
    Args:
        all_results: List of all analysis results
        processing_time: Total time taken
    """
    
    print("\n" + "="*70)
    print("\nPROCESSING SUMMARY:\n")
    
    # Count different safety levels
    total = len(all_results)
    safe = sum(1 for r in all_results if r['safety_level'] == 'Safe to Shred')
    needs_work = sum(1 for r in all_results if r['safety_level'] == 'Requires Preprocessing')
    dangerous = sum(1 for r in all_results if r['safety_level'] == 'Do Not Shred')
    not_ewaste = sum(1 for r in all_results if r['safety_level'] == 'Discard')
    errors = sum(1 for r in all_results if r['error'])
    
    print(f"  Total Images: {total}")
    print(f"  Successfully Processed: {total - errors}")
    print(f"  Failed: {errors}")
    print(f"  Processing Time: {processing_time:.1f} seconds")
    print(f"  Average Time per Image: {processing_time/total:.1f} seconds")
    
    print("\n  Safety Breakdown:")
    print(f"    - Safe to Shred: {safe}")
    print(f"    - Requires Preprocessing: {needs_work}")
    print(f"    - Do Not Shred: {dangerous}")
    print(f"    - Non E-waste (Discard): {not_ewaste}")
    
    # List failed files if any
    failed_results = [r for r in all_results if r['error']]
    if failed_results:
        print("\n  Failed Files:")
        for r in failed_results:
            print(f"    - {r['filename']}")
    
    print("\n" + "="*70)

# ============================================================================
# MAIN FUNCTION - This runs everything
# ============================================================================

def analyze_folder(folder_path: str = "images/"):
    """
    Main function that analyzes all images in a folder
    
    Args:
        folder_path: Where to look for images (default: "images/")
    """
    
    # Check if the folder exists
    folder = Path(folder_path)
    if not folder.exists():
        print(f"\nError: The folder '{folder_path}' doesn't exist!")
        return
    
    # Find all image files in the folder
    image_files = []
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in ALLOWED_IMAGE_TYPES:
            image_files.append(file)
    
    # Check if we found any images
    if not image_files:
        print(f"No images found in '{folder_path}'")
        return
    
    total_images = len(image_files)
    print(f"\nProcessing {total_images} images from '{folder_path}'\n")
    
    # Create the analyzer
    analyzer = SimpleEWasteAnalyzer()
    
    # Track time
    start_time = time.time()
    
    # Analyze each image
    all_results = []
    for index, image_file in enumerate(image_files, 1):
        # Analyze this image
        result = analyzer.analyze_one_image(image_file, index, total_images)
        all_results.append(result)
        
        # Print the result right away
        print_single_result(result)
        
        # Small pause to avoid hitting API limits
        if index < len(image_files):
            time.sleep(0.5)
    
    # Calculate total time
    processing_time = time.time() - start_time
    
    # Print summary
    print_summary(all_results, processing_time)

# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    """This runs when you execute the script"""
    
    # Always analyze the images folder
    analyze_folder("images/")

import google.generativeai as genai
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ============= ENUMS FOR CATEGORIES =============
class ObjectCategory(str, Enum):
    # Consumer Electronics
    SMARTPHONE = "Smartphone"
    TABLET = "Tablet"
    LAPTOP = "Laptop"
    DESKTOP_COMPUTER = "Desktop Computer"
    MONITOR = "Monitor"
    TELEVISION = "Television"
    GAMING_CONSOLE = "Gaming Console"
    SMARTWATCH = "Smartwatch"
    EARBUDS = "Earbuds/Headphones"
    CAMERA = "Digital Camera"
    
    # Computer Components
    CIRCUIT_BOARD = "Circuit Board"
    HARD_DRIVE = "Hard Drive"
    RAM = "RAM Module"
    PROCESSOR = "CPU/Processor"
    GRAPHICS_CARD = "Graphics Card"
    POWER_SUPPLY = "Power Supply Unit"
    SSD = "Solid State Drive"
    MOTHERBOARD = "Motherboard"
    
    # Batteries
    LITHIUM_BATTERY = "Lithium-ion Battery"
    ALKALINE_BATTERY = "Alkaline Battery"
    LEAD_ACID_BATTERY = "Lead-acid Battery"
    BUTTON_BATTERY = "Button Cell Battery"
    LAPTOP_BATTERY = "Laptop Battery Pack"
    PHONE_BATTERY = "Phone Battery"
    
    # Cables and Accessories
    CABLES = "Cables/Wires"
    CHARGER = "Charger/Adapter"
    KEYBOARD = "Keyboard"
    MOUSE = "Mouse"
    USB_DEVICE = "USB Device/Flash Drive"
    
    # Large Appliances
    PRINTER = "Printer"
    SCANNER = "Scanner"
    ROUTER = "Router/Modem"
    SPEAKER = "Speaker System"
    MICROWAVE = "Microwave"
    
    # Other
    CRT = "Cathode-Ray Tube"
    MIXED_EWASTE = "Mixed E-waste"
    UNKNOWN = "Unknown Device"

class ShredSafety(str, Enum):
    SAFE_TO_SHRED = "Safe to Shred"
    DO_NOT_SHRED = "Do Not Shred"
    REQUIRES_PREPROCESSING = "Requires Preprocessing Before Shredding"
    DISCARD = "Discard"

# ============= PYDANTIC MODELS =============
class HazardousComponents(BaseModel):
    has_battery: bool = Field(description="Contains battery that could explode/leak")
    has_mercury: bool = Field(description="Contains mercury (LCD screens, old monitors)")
    has_lead: bool = Field(description="Contains lead (CRT monitors, solder)")
    has_capacitors: bool = Field(description="Contains capacitors that may hold charge")
    has_toner: bool = Field(description="Contains toner/ink (printers)")
    has_refrigerant: bool = Field(description="Contains refrigerant gases")
    has_cadmium: bool = Field(description="Contains cadmium")
    has_nickel: bool = Field(description="Contains nickel")

class EWasteAnalysis(BaseModel):
    # Basic Classification
    object_type: ObjectCategory
    
    # Safety Assessment
    shred_safety: ShredSafety
    
    # Component Analysis
    hazardous_components: HazardousComponents

    #observations just in case the object is not ewaste
    observations: str = Field(description="Any additional relevant observations")


# ============= ANALYSIS FUNCTIONS =============
def create_analysis_schema():
    """Create the JSON schema for Gemini API"""
    return {
        "type": "object",
        "properties": {
            "object_type": {
                "type": "string",
                "enum": [e.value for e in ObjectCategory],
                "description": "Type of electronic waste"
            },
            "shred_safety": {
                "type": "string",
                "enum": [e.value for e in ShredSafety],
                "description": "Whether item is safe to shred"
            },
            "hazardous_components": {
                "type": "object",
                "properties": {
                    "has_battery": {"type": "boolean"},
                    "has_mercury": {"type": "boolean"},
                    "has_lead": {"type": "boolean"},
                    "has_capacitors": {"type": "boolean"},
                    "has_toner": {"type": "boolean"},
                    "has_refrigerant": {"type": "boolean"},
                    "has_cadmium": {"type": "boolean"},
                    "has_nickel": {"type": "boolean"}
                },
                "required": ["has_battery", "has_mercury", "has_lead", "has_capacitors", 
                           "has_toner", "has_refrigerant", "has_cadmium", "has_nickel"]
            },
            "observations": {
                "type": "string",
                "description": "Additional observations"
            },
        },
        "required": ["object_type", "shred_safety", "hazardous_components", "observations"]
    }

def analyze_ewaste(image_file, additional_context=""):
    """
    Analyze e-waste image and return comprehensive processing instructions
    
    Args:
        image_file: Path to the image file
        additional_context: Any additional context about the item
    
    Returns:
        EWasteAnalysis object with complete analysis
    """
    # Create the comprehensive prompt
    with open("prompt.md", 'r') as f:
        prompt = f.read()

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        image = genai.upload_file(image_file)
        
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=create_analysis_schema()
            )
        )
        
        # Parse and validate response
        result_dict = json.loads(response.text)
        analysis = EWasteAnalysis(**result_dict)
        return analysis
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise

def generate_processing_report(image_path, analysis: EWasteAnalysis) -> str:
    """Generate a human-readable processing report"""
    report = f"""
    ====================================================================

        ITEM """ + str(num) + f""": (""" + str(image_path) + f""")

        Item: {analysis.object_type} """
    if analysis.object_type == ObjectCategory.UNKNOWN:
        report += "\n        " + analysis.observations
    report += f"""
        Shred Safety: {analysis.shred_safety}
    """
    if analysis.shred_safety == ShredSafety.DO_NOT_SHRED or analysis.shred_safety == ShredSafety.REQUIRES_PREPROCESSING:
        report += f"""
        Hazards:

        Battery: {'YES' if analysis.hazardous_components.has_battery else 'NO'}
        Mercury: {'YES' if analysis.hazardous_components.has_mercury else 'NO'}
        Lead: {'YES' if analysis.hazardous_components.has_lead else 'NO'}
        Capacitors: {'YES' if analysis.hazardous_components.has_capacitors else 'NO'}
        Toner: {'YES' if analysis.hazardous_components.has_toner else 'NO'}
        Refrigerant: {'YES' if analysis.hazardous_components.has_refrigerant else 'NO'}
        Cadmium: {'YES' if analysis.hazardous_components.has_cadmium else 'NO'}
        Nickel: {'YES' if analysis.hazardous_components.has_nickel else 'NO'}"""
    report += "\n\n    ===================================================================="
    
    return report

# ============= MAIN EXECUTION =============

folder_path = "/Users/williambeesley/Desktop/AAASEIMGREC/images"
images = os.listdir(folder_path)
num = 0
for image_path in images:
    num += 1
    if __name__ == "__main__":
        try:
            analysis = analyze_ewaste(str("images/" + image_path))
            
            # Generate and print report
            report = generate_processing_report(image_path, analysis)
            print(report)

        except Exception as e:
            print(f"❌ Error: {e}")

# 🔧 E-Waste Analyzer - Easy Guide

## What Does This Do?

This program looks at pictures of old electronics and tells you if they're safe to shred for recycling. It's like having an expert check your e-waste!

## Quick Start (3 Steps)

### Step 1: Get Your Google API Key (Free!)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (looks like: `AIzaSyB...`)

### Step 2: Set Up Your Key
1. Create a new file called `.env` in this folder
2. Add this line: `GOOGLE_API_KEY=paste_your_key_here`
3. Save the file

### Step 3: Run It!
```bash
python3 simple_analyzer.py
```

## Adding Your Images

Put your e-waste photos in the `images/` folder:
```
images/
  ├── old_phone.jpg
  ├── broken_laptop.png
  └── circuit_board.jpg
```

## Understanding Results

The program will tell you one of four things:

### ✅ **Safe** - OK to shred!
- Examples: Empty circuit boards, cables, keyboards
- Action: Can go straight to the shredder

### ⚠️ **Needs Work** - Remove dangerous parts first
- Examples: Printers (remove toner), hard drives (remove magnets)
- Action: Take out the dangerous parts, then shred

### 🚫 **Dangerous** - DO NOT SHRED!
- Examples: Batteries, LCD screens, CRT monitors
- Action: These need special recycling - don't shred them

### ❓ **Not E-Waste** - This isn't electronic
- Examples: Food, clothes, regular trash
- Action: This doesn't belong in e-waste recycling

## Example Output

```
================================================================================
🔧 E-WASTE ANALYZER - Let's check if your e-waste is safe to shred!
================================================================================

📦 ITEM #1: old_keyboard.jpg
--------------------------------------------------
📋 Item: Mechanical Keyboard
✅ Safety: Safe - OK to shred!

📦 ITEM #2: phone_battery.jpg
--------------------------------------------------
📋 Item: Lithium Battery
🚫 Safety: Dangerous - DO NOT SHRED!
⚡ Dangerous Parts: Lithium, Electrolyte
📝 Notes: Can explode if shredded. Needs special battery recycling.

================================================================================
📊 SUMMARY REPORT
================================================================================

📈 Total items analyzed: 2
   ✅ Safe to shred: 1
   🚫 Dangerous (don't shred): 1
```

## Troubleshooting

### "No Google API key found!"
- Make sure your `.env` file exists
- Check that the key is on the right line: `GOOGLE_API_KEY=your_key`

### "No images found"
- Put images in the `images/` folder
- Supported formats: .jpg, .jpeg, .png, .gif, .bmp, .webp

### "Module not found"
- Install requirements: `pip install -r requirements.txt`

## Safety Tips

🔋 **Batteries** = Always dangerous (except tiny CMOS batteries)  
📺 **Screens** = LCD, Plasma, CRT all contain toxins  
⚡ **Capacitors** = Can hold dangerous charge  
☠️ **Mercury/Lead** = Found in old monitors and some components  

## Need Help?

- The program saves results to `analysis_results.txt`
- Each image takes about 2-3 seconds to analyze
- You can analyze different folders: `python3 simple_analyzer.py my_folder/`

---

**Remember:** When in doubt, mark it as dangerous! Better safe than sorry with e-waste. ♻️
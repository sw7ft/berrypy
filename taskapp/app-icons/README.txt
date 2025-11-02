BerryPy App Icons Directory
===========================

This directory stores app icons for the BerryPy Task Manager.

Icon Specifications:
- Size: 48x48 pixels (PNG format recommended)
- Format: PNG, JPG, or GIF
- Naming: Use the exact filename specified in catalog.json

To add an icon:
1. Create a 48x48 pixel icon
2. Save it in this directory with a descriptive name (e.g., "aichat.png")
3. Update the corresponding app entry in catalog.json to include:
   "icon": "filename.png"

Example catalog.json entry:
{
  "AI-Chat": {
    "name": "AI Chat Assistant",
    "description": "...",
    "icon": "aichat.png"
  }
}

If an icon is not found, the app will display the first letter of the app name as a fallback.


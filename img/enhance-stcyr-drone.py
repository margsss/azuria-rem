#!/usr/bin/env python3
"""Generate a true drone/aerial masterplan view of Saint Cyr from the architect render"""

import os
import base64
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]
client = genai.Client(api_key=API_KEY)
MODEL = "nano-banana-pro-preview"

IMG_DIR = Path(__file__).parent
OUT_DIR = IMG_DIR / "enhanced"

# Use the original architect render as reference
filepath = IMG_DIR / "saint-cyr-2.webp"
img_b64 = base64.b64encode(filepath.read_bytes()).decode()

prompt = """You are a world-class architectural photographer operating a professional drone (DJI Inspire 3).

Take this 3D render of a commercial development and create a PHOTOREALISTIC DRONE PHOTOGRAPH shot from DIRECTLY ABOVE — a bird's eye / top-down aerial view at approximately 80-100 meters altitude, looking STRAIGHT DOWN at the masterplan.

ABSOLUTE REQUIREMENTS:
1. CAMERA MUST BE HIGH ABOVE, looking DOWN — this is a DRONE shot, NOT a ground-level photo
2. KEEP the EXACT same buildings — same shapes, same brick/wood facades, same roof designs, same layout
3. KEEP the EXACT same roads, parking areas, landscaping, and overall masterplan layout
4. ALL vehicles must be pickup trucks and artisan work vans — NO sedans, NO bicycles
5. The image must show the FULL site layout from above — all buildings, roads, parking, green areas visible

PHOTOREALISM REQUIREMENTS:
- INDISTINGUISHABLE from a real drone photograph
- Beautiful Californian golden hour light casting long shadows from buildings (shadows visible from above)
- Real rooftop textures — HVAC units, skylights, roof membrane materials
- Real asphalt, real landscaping with individual trees casting circular shadows
- Painted parking lines, road markings visible from above
- Natural depth — slight atmospheric haze at edges
- Shot on Hasselblad medium format drone camera, 4K"""

print("Generating drone view...")
response = client.models.generate_content(
    model=MODEL,
    contents=[{"parts": [
        {"inline_data": {"mime_type": "image/webp", "data": img_b64}},
        {"text": prompt}
    ]}],
    config={"response_modalities": ["image", "text"]}
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        out_path = OUT_DIR / "saint-cyr-drone.png"
        out_path.write_bytes(part.inline_data.data)
        print(f"SAVED: {out_path} ({len(part.inline_data.data)//1024}KB)")
        break
else:
    print("WARN: No image in response")
    if response.text:
        print(response.text[:300])

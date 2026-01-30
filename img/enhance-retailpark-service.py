#!/usr/bin/env python3
"""Generate retail park view from inside building through glass window"""

import os
import base64
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]
client = genai.Client(api_key=API_KEY)
MODEL = "nano-banana-pro-preview"

IMG_DIR = Path(__file__).parent
OUT_DIR = IMG_DIR / "enhanced"

# Use existing retail-park as reference
filepath = IMG_DIR / "retail-park.webp"
img_b64 = base64.b64encode(filepath.read_bytes()).decode()

prompt = """You are a world-class architectural photographer. Take this retail park render and reimagine it as seen FROM INSIDE one of the buildings, looking OUT through a large floor-to-ceiling glass window.

REQUIREMENTS:
- The camera is INSIDE a modern commercial space, looking OUT through a large glass window/storefront
- Through the glass, we see the retail park buildings, parking, landscaping — the same development shown in the reference image
- The glass creates beautiful reflections and light effects
- Warm French golden hour sunset light streaming through the window, creating long light beams on the interior floor
- The interior is a clean, modern commercial space — polished concrete floor, exposed ceiling
- Shallow depth of field — interior elements slightly soft, exterior sharp through glass
- The mood is warm, inviting, the feeling of being inside your own commercial space looking at a beautiful development at sunset
- Photorealistic, shot on Leica M11, 28mm Summilux, f/2, 4K
- French countryside / suburban setting visible through the window"""

print("Generating retail park interior view...")
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
        out_path = OUT_DIR / "service-retail.png"
        out_path.write_bytes(part.inline_data.data)
        print(f"SAVED: {out_path} ({len(part.inline_data.data)//1024}KB)")
        break
else:
    print("WARN: No image")
    if response.text:
        print(response.text[:300])

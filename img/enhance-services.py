#!/usr/bin/env python3
"""Generate unique service images — warm, human, not buildings"""

import os
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]
client = genai.Client(api_key=API_KEY)
MODEL = "nano-banana-pro-preview"
OUT_DIR = Path(__file__).parent / "enhanced"

SERVICES = {
    "service-village.png": "Photorealistic photograph of an artisan's hands working in a well-lit modern workshop — welding sparks, woodworking, or metal fabrication. Warm amber tungsten interior light mixed with natural daylight coming through large industrial windows. Shallow depth of field, bokeh background showing a clean modern workshop space. The feeling of skilled craftsmanship and pride. Intimate, warm, golden tones. Shot on Leica M11 with 50mm Summilux, f/1.4, 4K.",

    "service-cle.png": "Photorealistic photograph of a handshake between two professionals in front of a brand new modern building — one wearing a hard hat and high-vis vest, the other in a smart business suit. Golden sunset light behind them creating a warm backlit silhouette effect with lens flare. The new building is slightly out of focus in the background — clean architecture, fresh materials. The feeling of a successful handover, trust, partnership. Warm golden tones throughout. Shot on Sony A7R V with 85mm f/1.4 GM, shallow depth of field, 4K.",
}

for name, prompt in SERVICES.items():
    print(f"Generating {name}...")
    response = client.models.generate_content(
        model=MODEL, contents=prompt,
        config={"response_modalities": ["image", "text"]}
    )
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            out = OUT_DIR / name
            out.write_bytes(part.inline_data.data)
            print(f"  SAVED: {out} ({len(part.inline_data.data)//1024}KB)")
            break
    else:
        print(f"  WARN: No image")
        if response.text:
            print(f"  {response.text[:200]}")

print("\nDone.")

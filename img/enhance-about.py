#!/usr/bin/env python3
"""Generate atmospheric about page images"""

import os
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]
client = genai.Client(api_key=API_KEY)
MODEL = "nano-banana-pro-preview"
OUT_DIR = Path(__file__).parent / "enhanced"

IMAGES = {
    "about-hero.png": "Photorealistic overhead photograph of a dark walnut desk with architectural blueprints and masterplans spread out, a few pencils, a ruler, a white hard hat at the edge, a black ceramic coffee cup, warm amber desk lamp casting intimate golden light. The blueprints show artisan workshop villages and industrial buildings. Moody, cinematic, shallow depth of field. Dark background, warm tones. The feeling of late-night dedication and craftsmanship. Shot on Leica M11, 35mm Summilux, f/1.4, 4K.",

    "about-team.png": "Photorealistic photograph shot from behind — three professionals in dark business attire standing together looking at a construction site at golden hour sunset. They are silhouettes against a beautiful orange-pink sky. In front of them, a modern artisan workshop village is under construction — steel frames, cranes, scaffolding. The feeling of vision, partnership, ambition. No faces visible. Cinematic wide angle. Shot on Hasselblad X2D, 45mm, f/2.8, 4K.",
}

for name, prompt in IMAGES.items():
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

#!/usr/bin/env python3
"""Batch 2: Fix village-artisans, add saint-cyr-2 drone, generate corbeil data center"""

import os
import base64
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]
client = genai.Client(api_key=API_KEY)
MODEL = "nano-banana-pro-preview"

IMG_DIR = Path(__file__).parent
OUT_DIR = IMG_DIR / "enhanced"
OUT_DIR.mkdir(exist_ok=True)

STYLE_BASE = """You are a world-class architectural photographer. Take this 3D render and create a PHOTOREALISTIC photograph that looks 100% real — like taken with a Hasselblad H6D on location.

ABSOLUTE REQUIREMENTS — NEVER VIOLATE:
1. KEEP the EXACT same buildings — same shapes, same facade patterns, same colors, same rooflines, same window positions. Do NOT redesign anything.
2. KEEP the EXACT same layout — roads, parking spots, trees, fences, paths must be in the EXACT same positions.
3. KEEP the EXACT same camera angle and perspective. Do NOT change the viewpoint.
4. ALL vehicles must be pickup trucks (Ford F-150, Toyota Hilux) and artisan work vans (Ford Transit, Renault Master, Mercedes Sprinter) — NO sedans, NO SUVs, NO bicycles.

PHOTOREALISM REQUIREMENTS:
- This must be INDISTINGUISHABLE from a real photograph. No CG feel whatsoever.
- Beautiful Californian golden hour light — warm sun low in sky, long dramatic shadows, rich warm tones
- Sky: gorgeous deep blue with golden-pink wispy clouds, NOT flat or overexposed
- Materials must look REAL: brushed metal with actual reflections, weathered concrete with texture, glass reflecting the sky and surroundings, real asphalt with slight imperfections
- Trees must look like real mature trees with individual leaves catching sunlight, NOT CG blobs
- Add subtle lens effects: very slight vignette, natural depth of field, micro lens flare from sun
- Ground: real asphalt texture, real concrete curbs, real painted road markings slightly worn
- People if present: photorealistic, wearing work clothes, natural poses"""


def enhance(filename, prompt):
    filepath = IMG_DIR / filename
    if not filepath.exists():
        print(f"  SKIP: {filename} not found")
        return False
    print(f"  Reading {filename}...")
    img_bytes = filepath.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode()
    ext = filepath.suffix.lower()
    mime = "image/webp" if ext == ".webp" else f"image/{ext.lstrip('.')}"
    print(f"  Sending to Gemini...")
    response = client.models.generate_content(
        model=MODEL,
        contents=[{"parts": [
            {"inline_data": {"mime_type": mime, "data": img_b64}},
            {"text": prompt}
        ]}],
        config={"response_modalities": ["image", "text"]}
    )
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            out_name = Path(filename).stem + ".png"
            out_path = OUT_DIR / out_name
            out_path.write_bytes(part.inline_data.data)
            print(f"  SAVED: {out_path} ({len(part.inline_data.data)//1024}KB)")
            return True
    print(f"  WARN: No image in response")
    if response.text:
        print(f"  Response: {response.text[:200]}")
    return False


def generate(name, prompt):
    print(f"  Generating {name}...")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"response_modalities": ["image", "text"]}
    )
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            out_path = OUT_DIR / name
            out_path.write_bytes(part.inline_data.data)
            print(f"  SAVED: {out_path} ({len(part.inline_data.data)//1024}KB)")
            return True
    print(f"  WARN: No image in response")
    if response.text:
        print(f"  Response: {response.text[:200]}")
    return False


if __name__ == "__main__":
    # 1. Re-enhance village-artisans from CORRECT original
    print("\n═══ 1. VILLAGE-ARTISANS (correct original) ═══")
    enhance("village-artisans-original.png", STYLE_BASE + "\nThis is an artisan village in Saint Genis Pouilly, France — 38 workshop cells with metal cladding in burgundy, grey and beige vertical panels, large roller doors, trees planted between parking bays. Keep ALL building proportions, facade panel colors and patterns, and tree positions exactly as shown.")

    # 2. Saint-Cyr-2 drone/aerial view
    print("\n═══ 2. SAINT-CYR-2 (drone view) ═══")
    enhance("saint-cyr-2.webp", STYLE_BASE.replace("KEEP the EXACT same camera angle", "KEEP the EXACT same aerial/drone camera angle from above") + "\nThis is a commercial development in Saint Cyr L'École, France — aerial drone view from above showing brick and wood facade buildings, parking area with landscaping. This MUST remain a DRONE/AERIAL photograph taken from above, looking down at the buildings. Keep ALL building shapes, roof angles, roads, landscaping and facade details exactly as shown.")

    # 3. Generate Corbeil-Essonnes data center
    print("\n═══ 3. CORBEIL-ESSONNES DATA CENTER (generate) ═══")
    generate("corbeil.png", "Photorealistic photograph of a modern premium data center facility — sleek contemporary architecture with clean lines, dark metal and glass facade, cooling units visible on the roof, secure perimeter fencing, manicured landscaping. A few pickup trucks and work vans parked in front. Beautiful Californian golden hour light, dramatic sky with golden-pink clouds. The building should look substantial, high-tech and secure — a serious infrastructure investment. Shot on Hasselblad H6D medium format, shallow depth of field, 4K cinematic quality.")

    print("\n✓ Done.")

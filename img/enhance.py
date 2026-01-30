#!/usr/bin/env python3
"""Azuria REM — Image enhancement via Gemini Nano Banana Pro"""

import os
import sys
import base64
from pathlib import Path
from google import genai

# Load key
API_KEY = os.environ.get("GEMINI_API_KEY") or open(os.path.expanduser("~/our-brain/secrets/gemini.env")).read().strip().split("=",1)[1]

client = genai.Client(api_key=API_KEY)
MODEL_ENHANCE = "nano-banana-pro-preview"  # best for photorealism
MODEL_GENERATE = "nano-banana-pro-preview"

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

# ── Real project renders: enhance to photorealistic ──
PROJECT_IMAGES = {
    "saint-ouen.webp": STYLE_BASE + "\nThis is an artisan village in Saint Ouen l'Aumône, France — industrial workshop units with roller doors, metal cladding in burgundy and grey tones, central parking area with trees. Keep ALL building proportions and facade patterns exactly as shown.",
    "saint-cyr-1.webp": STYLE_BASE + "\nThis is a commercial development in Saint Cyr L'École, France. Keep ALL building shapes, roof angles, and facade details exactly as shown.",
    "feyzin.webp": STYLE_BASE + "\nThis is an artisan village in Feyzin, France — 25 workshop cells. Keep ALL building layouts, access roads, and vegetation placement exactly as shown.",
    "village-artisans.webp": STYLE_BASE + "\nThis is an artisan village in Saint Genis Pouilly, France — 38 workshop cells. Keep ALL buildings, roads, fences, and tree positions exactly as shown.",
    "retail-park.webp": STYLE_BASE + "\nThis is a retail park village with brick/wood facade buildings, parking with landscaping. Keep ALL building designs, parking layout, bicycle paths, and planting beds exactly as shown.",
    "hero.webp": STYLE_BASE + "\nThis is used as the hero/banner image. Make it extra cinematic — dramatic golden hour light, beautiful sky. Keep ALL buildings and layout exactly as shown.",
}

# ── Stock replacements: generate new images ──
GENERATE_IMAGES = {
    "cle-en-main.webp": "Photorealistic photograph of a brand new modern artisan workshop complex just completed and ready for handover — clean contemporary architecture with metal cladding, large glass roller doors, premium materials (steel, wood, concrete). Warm Californian golden hour light. A few pickup trucks and artisan work vans parked in front. Lush landscaping, fresh asphalt, everything pristine and new. The feeling of a premium turnkey delivery. Shot on Hasselblad medium format, shallow depth of field, 4K.",
    "montage.webp": "Photorealistic photograph of a modern office with floor-to-ceiling windows showing Paris skyline (Eiffel Tower visible in background). A large wall-mounted screen displays architectural plans and 3D renders of artisan workshop villages. On the desk: blueprints, architectural scale models of small industrial buildings, hard hat. No people visible. Warm golden afternoon light streaming through windows. Clean minimalist Parisian office. Shot on Hasselblad, shallow depth of field, 4K.",
}


def enhance_image(filename, prompt):
    """Send image + prompt to Gemini for enhancement."""
    filepath = IMG_DIR / filename
    if not filepath.exists():
        print(f"  SKIP: {filename} not found")
        return False

    print(f"  Reading {filename}...")
    img_bytes = filepath.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode()

    # Determine mime type
    ext = filepath.suffix.lower()
    mime = "image/webp" if ext == ".webp" else f"image/{ext.lstrip('.')}"

    print(f"  Sending to Gemini...")
    response = client.models.generate_content(
        model=MODEL_ENHANCE,
        contents=[
            {
                "parts": [
                    {"inline_data": {"mime_type": mime, "data": img_b64}},
                    {"text": prompt}
                ]
            }
        ],
        config={"response_modalities": ["image", "text"]}
    )

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            out_path = OUT_DIR / filename.replace('.webp', '.png')
            img_data = part.inline_data.data  # already bytes
            out_path.write_bytes(img_data)
            print(f"  SAVED: {out_path} ({len(img_data)//1024}KB)")
            return True

    print(f"  WARN: No image in response for {filename}")
    if response.text:
        print(f"  Response: {response.text[:200]}")
    return False


def generate_image(filename, prompt):
    """Generate a new image from text prompt."""
    print(f"  Generating {filename}...")
    response = client.models.generate_content(
        model=MODEL_GENERATE,
        contents=prompt,
        config={"response_modalities": ["image", "text"]}
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            out_path = OUT_DIR / filename.replace('.webp', '.png')
            img_data = part.inline_data.data  # already bytes
            out_path.write_bytes(img_data)
            print(f"  SAVED: {out_path} ({len(img_data)//1024}KB)")
            return True

    print(f"  WARN: No image in response for {filename}")
    if response.text:
        print(f"  Response: {response.text[:200]}")
    return False


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "enhance"):
        print("\n═══ ENHANCING PROJECT RENDERS ═══")
        for fname, prompt in PROJECT_IMAGES.items():
            print(f"\n→ {fname}")
            try:
                enhance_image(fname, prompt)
            except Exception as e:
                print(f"  ERROR: {e}")

    if mode in ("all", "generate"):
        print("\n═══ GENERATING REPLACEMENTS ═══")
        for fname, prompt in GENERATE_IMAGES.items():
            print(f"\n→ {fname}")
            try:
                generate_image(fname, prompt)
            except Exception as e:
                print(f"  ERROR: {e}")

    print("\n✓ Done. Check site/img/enhanced/")

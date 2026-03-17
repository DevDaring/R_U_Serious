"""
Generate story character and avatar images using Bria FIBO API,
then populate the CSV files.
"""

import os
import sys
import csv
import httpx
import time
from datetime import datetime

BRIA_API_KEY = os.getenv("BRIA_API_KEY", "bf487553c99f461fb418f846e1fa5e9d")
BASE_URL = "https://engine.prod.bria-api.com/v2"
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "data", "media")
CSV_DIR = os.path.join(os.path.dirname(__file__), "data", "csv")

CHARACTERS = [
    {
        "id": "CHR001",
        "name": "Luna the Fairy",
        "prompt": "A cute magical fairy girl character with sparkling wings, wearing a purple dress with stars, holding a magic wand, full body illustration",
        "description": "A magical fairy who loves science",
        "aspect": "3:4",
        "filename": "chr001.png",
    },
    {
        "id": "CHR002",
        "name": "Professor Oak",
        "prompt": "A wise elderly owl professor character wearing round glasses and a graduation cap, holding a book, friendly expression, full body illustration",
        "description": "A wise old owl who teaches",
        "aspect": "3:4",
        "filename": "chr002.png",
    },
    {
        "id": "CHR003",
        "name": "Ganesha Guide",
        "prompt": "A cute friendly baby elephant character wearing a colorful vest, smiling and waving, cartoon style, standing upright, full body illustration",
        "description": "A friendly elephant companion",
        "aspect": "3:4",
        "filename": "chr003.png",
    },
    {
        "id": "CHR_ROBO",
        "name": "Robo Explorer",
        "prompt": "A small friendly robot character for kids, with big round glowing blue eyes, silver metallic body, antenna on head, waving hand, full body cartoon illustration",
        "description": "A curious robot who explores space and technology",
        "aspect": "3:4",
        "filename": "chr_robo.png",
    },
    {
        "id": "CHR_PIRATE",
        "name": "Captain Codebeard",
        "prompt": "A friendly cartoon pirate captain character for children, eye patch, tricorn hat with skull and crossbones, red coat, holding a treasure map, full body illustration",
        "description": "A swashbuckling pirate who teaches geography",
        "aspect": "3:4",
        "filename": "chr_pirate.png",
    },
    {
        "id": "CHR_DINO",
        "name": "Dino the Scholar",
        "prompt": "A cute baby green dinosaur character wearing a backpack and holding a pencil, standing upright, smiling, cartoon style educational illustration, full body",
        "description": "A dinosaur who loves learning about history",
        "aspect": "3:4",
        "filename": "chr_dino.png",
    },
    {
        "id": "CHR_ASTRO",
        "name": "Stella Stargazer",
        "prompt": "A young girl astronaut character in a colorful spacesuit, helmet with star stickers, floating in space with planets behind, cartoon illustration, full body",
        "description": "An astronaut who teaches about the cosmos",
        "aspect": "3:4",
        "filename": "chr_astro.png",
    },
    {
        "id": "CHR_WIZARD",
        "name": "Merlin Jr.",
        "prompt": "A young boy wizard character in a blue robe covered in math symbols and stars, holding a glowing staff, pointy hat, friendly face, cartoon illustration, full body",
        "description": "A young wizard who makes math magical",
        "aspect": "3:4",
        "filename": "chr_wizard.png",
    },
]

AVATARS = [
    {
        "id": "AVT_SPACE",
        "name": "Space Explorer",
        "prompt": "A cool cartoon avatar portrait of a kid astronaut with a round helmet, stars reflected in visor, friendly smile, vibrant colors, portrait style",
        "style": "cartoon",
        "filename": "avt_space.png",
    },
    {
        "id": "AVT_NINJA",
        "name": "Code Ninja",
        "prompt": "A cute cartoon ninja avatar portrait with a dark mask, bright determined eyes, headband with a code symbol, portrait style illustration",
        "style": "cartoon",
        "filename": "avt_ninja.png",
    },
    {
        "id": "AVT_DRAGON",
        "name": "Friendly Dragon",
        "prompt": "A cute friendly baby dragon avatar portrait, green scales, big round orange eyes, small wings, smiling, cartoon portrait illustration",
        "style": "cartoon",
        "filename": "avt_dragon.png",
    },
    {
        "id": "AVT_SCIENTIST",
        "name": "Mad Scientist",
        "prompt": "A fun cartoon mad scientist avatar portrait, wild spiky white hair, safety goggles on forehead, lab coat, holding a bubbling test tube, portrait illustration",
        "style": "cartoon",
        "filename": "avt_scientist.png",
    },
    {
        "id": "AVT_SUPERHERO",
        "name": "Super Learner",
        "prompt": "A cartoon kid superhero avatar portrait wearing a cape and mask, with a book symbol on chest, confident smile, vibrant colors, portrait illustration",
        "style": "cartoon",
        "filename": "avt_superhero.png",
    },
    {
        "id": "AVT_ARTIST",
        "name": "Creative Artist",
        "prompt": "A cheerful cartoon artist avatar portrait, beret hat, paint brush behind ear, colorful paint splashes on cheeks, big smile, portrait illustration",
        "style": "cartoon",
        "filename": "avt_artist.png",
    },
    {
        "id": "AVT_DETECTIVE",
        "name": "Detective Quiz",
        "prompt": "A cartoon kid detective avatar portrait, magnifying glass, deerstalker hat, curious expression, vintage style, portrait illustration",
        "style": "cartoon",
        "filename": "avt_detective.png",
    },
    {
        "id": "AVT_MUSIC",
        "name": "Music Maestro",
        "prompt": "A cheerful cartoon musician avatar portrait, headphones around neck, musical notes floating around, colorful hair, portrait illustration",
        "style": "cartoon",
        "filename": "avt_music.png",
    },
]


def generate_image(prompt: str, aspect_ratio: str = "1:1") -> bytes:
    """Call Bria FIBO API to generate an image."""
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_KEY,
    }
    payload = {
        "prompt": f"cartoon style, vibrant colors, child-friendly illustration, {prompt}",
        "sync": True,
        "aspect_ratio": aspect_ratio,
        "model_version": "FIBO",
    }

    with httpx.Client(timeout=120.0) as client:
        resp = client.post(f"{BASE_URL}/image/generate", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        image_url = data.get("result", {}).get("image_url")
        if not image_url:
            raise ValueError(f"No image_url in response: {data}")
        print(f"  Downloading from: {image_url[:80]}...")
        img_resp = client.get(image_url, timeout=60.0)
        img_resp.raise_for_status()
        return img_resp.content


def main():
    os.makedirs(os.path.join(MEDIA_DIR, "characters"), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_DIR, "avatars"), exist_ok=True)

    # --- Generate Characters ---
    print("=" * 60)
    print("GENERATING STORY CHARACTERS")
    print("=" * 60)
    char_rows = []
    for ch in CHARACTERS:
        filepath = os.path.join(MEDIA_DIR, "characters", ch["filename"])
        print(f"\n[Character] {ch['name']} ({ch['id']})")
        try:
            img_bytes = generate_image(ch["prompt"], ch["aspect"])
            with open(filepath, "wb") as f:
                f.write(img_bytes)
            print(f"  Saved: {filepath} ({len(img_bytes)} bytes)")
            char_rows.append({
                "character_id": ch["id"],
                "user_id": "USR002",
                "name": ch["name"],
                "image_path": f"characters/{ch['filename']}",
                "creation_method": "ai_generated",
                "description": ch["description"],
                "created_at": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(2)  # rate limit

    # --- Generate Avatars ---
    print("\n" + "=" * 60)
    print("GENERATING AVATARS")
    print("=" * 60)
    avt_rows = []
    for av in AVATARS:
        filepath = os.path.join(MEDIA_DIR, "avatars", av["filename"])
        print(f"\n[Avatar] {av['name']} ({av['id']})")
        try:
            img_bytes = generate_image(av["prompt"], "1:1")
            with open(filepath, "wb") as f:
                f.write(img_bytes)
            print(f"  Saved: {filepath} ({len(img_bytes)} bytes)")
            avt_rows.append({
                "avatar_id": av["id"],
                "user_id": "USR002",
                "name": av["name"],
                "image_path": f"avatars/{av['filename']}",
                "creation_method": "ai_generated",
                "style": av["style"],
                "created_at": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(2)

    # --- Update characters.csv ---
    char_csv = os.path.join(CSV_DIR, "characters.csv")
    print(f"\nUpdating {char_csv} ...")
    # Read existing, overwrite matching IDs
    existing_chars = []
    existing_ids = set()
    with open(char_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_chars.append(row)
            existing_ids.add(row["character_id"])
    for cr in char_rows:
        if cr["character_id"] in existing_ids:
            existing_chars = [r if r["character_id"] != cr["character_id"] else cr for r in existing_chars]
        else:
            existing_chars.append(cr)
    with open(char_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["character_id", "user_id", "name", "image_path", "creation_method", "description", "created_at"])
        writer.writeheader()
        writer.writerows(existing_chars)
    print(f"  Characters CSV updated: {len(existing_chars)} total rows")

    # --- Update avatars.csv ---
    avt_csv = os.path.join(CSV_DIR, "avatars.csv")
    print(f"\nUpdating {avt_csv} ...")
    existing_avts = []
    existing_avt_ids = set()
    with open(avt_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_avts.append(row)
            existing_avt_ids.add(row["avatar_id"])
    for ar in avt_rows:
        if ar["avatar_id"] in existing_avt_ids:
            existing_avts = [r if r["avatar_id"] != ar["avatar_id"] else ar for r in existing_avts]
        else:
            existing_avts.append(ar)
    with open(avt_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["avatar_id", "user_id", "name", "image_path", "creation_method", "style", "created_at"])
        writer.writeheader()
        writer.writerows(existing_avts)
    print(f"  Avatars CSV updated: {len(existing_avts)} total rows")

    print("\n" + "=" * 60)
    print(f"DONE! Generated {len(char_rows)} characters and {len(avt_rows)} avatars")
    print("=" * 60)


if __name__ == "__main__":
    main()

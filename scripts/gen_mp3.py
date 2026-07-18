"""Generate MP3 files for phrases that Youdao TTS cannot pronounce."""
import asyncio, hashlib, json, os, re, sys

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "audio")
AUDIO_MAP_JS = os.path.join(os.path.dirname(__file__), "..", "audio_map.js")

PHRASES = [
    # Mrs. Brice's Mice (2026-07-18): phrases Youdao TTS returns HTTP 500 for
    "dried them behind their ears",
    "loved to sing",
    "danced around",
    "on top of her hand",
    "on one side of",
    "It is time for our walk.",
    "So he could see where they were going.",
    "ran this way and that",
    "get tired of doing sth.",
    "went back to",
    "sat in front",
    "went up one aisle",
    "went down another",
    "leading the way",
    "went home to eat it",
    "After they ate",
    "kept right on doing",
]

def slugify(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s.strip("_")

async def gen_one(phrase, out_path):
    """Use edge-tts Python API to generate MP3."""
    import edge_tts
    # Clean the text for TTS (remove parens content)
    tts_text = re.sub(r"\(.*?\)", "", phrase)  # remove (was) etc
    tts_text = tts_text.strip(" .!?,;:\"'")
    
    try:
        communicate = edge_tts.Communicate(tts_text, "en-US-AriaNeural")
        await communicate.save(out_path)
        size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        print(f"  OK: {phrase!r} → {os.path.basename(out_path)} ({size} bytes)")
        return True
    except Exception as e:
        print(f"  FAIL: {phrase!r} → {e}")
        return False

async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # Read existing audio_map
    with open(AUDIO_MAP_JS, "r", encoding="utf-8") as f:
        content = f.read()
    map_data = json.loads(content.replace("window.AUDIO_MAP = ", "").rstrip(";"))
    
    results = {}
    for phrase in PHRASES:
        slug = slugify(phrase)
        h = hashlib.md5(phrase.encode()).hexdigest()[:6]
        fname = f"{slug}_{h}.mp3"
        out_path = os.path.join(AUDIO_DIR, fname)
        
        if os.path.exists(out_path):
            print(f"  SKIP (exists): {phrase!r} → {fname}")
        else:
            ok = await gen_one(phrase, out_path)
            if not ok:
                continue
        
        results[phrase] = fname
    
    # Update audio_map.js
    for phrase, fname in results.items():
        if phrase not in map_data:
            map_data[phrase] = fname
            print(f"  ADDED to audio_map: {phrase!r} → {fname}")
    
    # Write updated audio_map.js
    js_content = "window.AUDIO_MAP = " + json.dumps(map_data, ensure_ascii=False, indent=None)
    with open(AUDIO_MAP_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"\nDone! Added {len(results)} entries to audio_map.js")
    print(f"Total entries in audio_map.js: {len(map_data)}")

asyncio.run(main())

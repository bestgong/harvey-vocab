"""Generate MP3 files for phrases that Youdao TTS cannot pronounce."""
import asyncio, hashlib, json, os, re, sys

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "audio")
AUDIO_MAP_JS = os.path.join(os.path.dirname(__file__), "..", "audio_map.js")

PHRASES = [
    "get one's food",
    "it is(was) time for",
    "to be fed",
    "jump in the water",
    "That is all there is.",
    "He looked sad.",
    "He did not know what to look at first.",
    "from out of town",
    "lovely fur coat",
    "born with it",
    "no room for you",
    "Here is a place.",
    "make words with blocks",
    "the sounds fine",
    "Is it you?",
    "sat at his desk",
    "He learned how to read.",
    "threw the ball over the net",
    "The ball must not hit the ground.",
    "It is even.",
    "School was over.",
    "I just wanted to know what it is like outside.",
    "welcome you home",
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

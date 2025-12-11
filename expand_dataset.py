"""
Script to help expand the Quran verses dataset.
This script can be used to add more verses or validate the dataset.
"""

import json

def load_verses(json_path='quran_verses.json'):
    """Load existing verses"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_verses(verses, json_path='quran_verses.json'):
    """Save verses to JSON file"""
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    verses = load_verses()
    print(f"Current dataset has {len(verses)} verses")
    print(f"Unique surahs: {len(set(v['surah'] for v in verses))}")


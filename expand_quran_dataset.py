"""
Script to expand the Quran verses dataset by fetching from public API
and merging with existing data.
"""

import json
import requests

def fetch_quran_from_api():
    """
    Fetch Quran verses from alquran.cloud API
    Returns a list of verses with Arabic text and English translations
    """
    try:
        print("Fetching Arabic text from API...")
        # Fetch Arabic text
        arabic_url = "https://api.alquran.cloud/v1/quran/quran-uthmani"
        arabic_response = requests.get(arabic_url, timeout=30)
        
        print("Fetching English translation from API...")
        # Fetch English translation
        english_url = "https://api.alquran.cloud/v1/quran/en.sahih"
        english_response = requests.get(english_url, timeout=30)
        
        if arabic_response.status_code == 200 and english_response.status_code == 200:
            arabic_data = arabic_response.json()
            english_data = english_response.json()
            verses_list = []
            
            # Process both responses
            if 'data' in arabic_data and 'surahs' in arabic_data['data']:
                # Create a mapping of (surah, ayah) -> translation
                translation_map = {}
                if 'data' in english_data and 'surahs' in english_data['data']:
                    for surah in english_data['data']['surahs']:
                        surah_num = surah['number']
                        for ayah in surah['ayahs']:
                            key = (surah_num, ayah['numberInSurah'])
                            translation_map[key] = ayah['text']
                
                # Process Arabic verses
                for surah in arabic_data['data']['surahs']:
                    surah_num = surah['number']
                    for ayah in surah['ayahs']:
                        ayah_num = ayah['numberInSurah']
                        translation = translation_map.get((surah_num, ayah_num), "")
                        
                        verse = {
                            "surah": surah_num,
                            "ayah": ayah_num,
                            "arabic": ayah['text'],
                            "transliteration": "",  # API doesn't provide this
                            "translation": translation,
                            "text": translation if translation else ayah['text']  # Use translation for search, fallback to Arabic
                        }
                        verses_list.append(verse)
                
                print(f"Fetched {len(verses_list)} verses from API")
                return verses_list
        else:
            print(f"API request failed. Arabic: {arabic_response.status_code}, English: {english_response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching from API: {e}")
        print("You can manually expand quran_verses.json instead")
        return None

def load_existing_verses():
    """Load existing verses from JSON file"""
    try:
        with open('quran_verses.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_verses(verses, filename='quran_verses.json'):
    """Save verses to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(verses)} verses to {filename}")

def merge_verses(existing, new):
    """Merge existing and new verses, avoiding duplicates"""
    # Create a set of (surah, ayah) tuples for existing verses
    existing_keys = {(v['surah'], v['ayah']) for v in existing}
    
    # Add new verses that don't already exist
    merged = existing.copy()
    added_count = 0
    for verse in new:
        key = (verse['surah'], verse['ayah'])
        if key not in existing_keys:
            merged.append(verse)
            existing_keys.add(key)
            added_count += 1
    
    print(f"Added {added_count} new verses")
    return merged

def deduplicate_verses(verses):
    """Remove duplicate verses based on (surah, ayah)"""
    seen = set()
    unique_verses = []
    for verse in verses:
        key = (verse['surah'], verse['ayah'])
        if key not in seen:
            seen.add(key)
            unique_verses.append(verse)
    return unique_verses

if __name__ == "__main__":
    print("=" * 50)
    print("Quran Dataset Expander")
    print("=" * 50)
    
    # Load existing verses
    existing_verses = load_existing_verses()
    print(f"Current dataset: {len(existing_verses)} verses")
    
    # Try to fetch from API
    new_verses = fetch_quran_from_api()
    
    if new_verses:
        # Merge verses
        merged_verses = merge_verses(existing_verses, new_verses)
        
        # Remove any duplicates
        merged_verses = deduplicate_verses(merged_verses)
        
        # Sort by surah and ayah
        merged_verses.sort(key=lambda x: (x['surah'], x['ayah']))
        
        # Save merged dataset
        save_verses(merged_verses)
        print(f"\nTotal verses in dataset: {len(merged_verses)}")
        print(f"Unique verses: {len(set((v['surah'], v['ayah']) for v in merged_verses))}")
    else:
        print("\nCould not fetch from API. Current dataset unchanged.")
        print("To expand manually, add more verses to quran_verses.json")


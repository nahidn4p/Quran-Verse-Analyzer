import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import gradio as gr
import torch

# Force CPU usage
device = 'cpu'
torch.set_num_threads(4)  # Use multiple CPU threads

# Surah names mapping (1-114)
SURAH_NAMES = {
    1: "Al-Fatihah", 2: "Al-Baqarah", 3: "Ali 'Imran", 4: "An-Nisa", 5: "Al-Ma'idah",
    6: "Al-An'am", 7: "Al-A'raf", 8: "Al-Anfal", 9: "At-Tawbah", 10: "Yunus",
    11: "Hud", 12: "Yusuf", 13: "Ar-Ra'd", 14: "Ibrahim", 15: "Al-Hijr",
    16: "An-Nahl", 17: "Al-Isra", 18: "Al-Kahf", 19: "Maryam", 20: "Ta-Ha",
    21: "Al-Anbiya", 22: "Al-Hajj", 23: "Al-Mu'minun", 24: "An-Nur", 25: "Al-Furqan",
    26: "Ash-Shu'ara", 27: "An-Naml", 28: "Al-Qasas", 29: "Al-Ankabut", 30: "Ar-Rum",
    31: "Luqman", 32: "As-Sajdah", 33: "Al-Ahzab", 34: "Saba", 35: "Fatir",
    36: "Ya-Sin", 37: "As-Saffat", 38: "Sad", 39: "Az-Zumar", 40: "Ghafir",
    41: "Fussilat", 42: "Ash-Shura", 43: "Az-Zukhruf", 44: "Ad-Dukhan", 45: "Al-Jathiyah",
    46: "Al-Ahqaf", 47: "Muhammad", 48: "Al-Fath", 49: "Al-Hujurat", 50: "Qaf",
    51: "Adh-Dhariyat", 52: "At-Tur", 53: "An-Najm", 54: "Al-Qamar", 55: "Ar-Rahman",
    56: "Al-Waqi'ah", 57: "Al-Hadid", 58: "Al-Mujadila", 59: "Al-Hashr", 60: "Al-Mumtahanah",
    61: "As-Saff", 62: "Al-Jumu'ah", 63: "Al-Munafiqun", 64: "At-Taghabun", 65: "At-Talaq",
    66: "At-Tahrim", 67: "Al-Mulk", 68: "Al-Qalam", 69: "Al-Haqqah", 70: "Al-Ma'arij",
    71: "Nuh", 72: "Al-Jinn", 73: "Al-Muzzammil", 74: "Al-Muddaththir", 75: "Al-Qiyamah",
    76: "Al-Insan", 77: "Al-Mursalat", 78: "An-Naba", 79: "An-Nazi'at", 80: "Abasa",
    81: "At-Takwir", 82: "Al-Infitar", 83: "Al-Mutaffifin", 84: "Al-Inshiqaq", 85: "Al-Buruj",
    86: "At-Tariq", 87: "Al-A'la", 88: "Al-Ghashiyah", 89: "Al-Fajr", 90: "Al-Balad",
    91: "Ash-Shams", 92: "Al-Layl", 93: "Ad-Duha", 94: "Ash-Sharh", 95: "At-Tin",
    96: "Al-Alaq", 97: "Al-Qadr", 98: "Al-Bayyinah", 99: "Az-Zalzalah", 100: "Al-Adiyat",
    101: "Al-Qari'ah", 102: "At-Takathur", 103: "Al-Asr", 104: "Al-Humazah", 105: "Al-Fil",
    106: "Quraysh", 107: "Al-Ma'un", 108: "Al-Kawthar", 109: "Al-Kafirun", 110: "An-Nasr",
    111: "Al-Masad", 112: "Al-Ikhlas", 113: "Al-Falaq", 114: "An-Nas"
}

# Load Quran verses
def load_verses(json_path='quran_verses.json'):
    """Load Quran verses from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        verses = json.load(f)
    return verses

# Initialize the model and create embeddings
print("Loading sentence transformer model (CPU only)...")
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)  # Lightweight and fast model

print("Loading Quran verses...")
verses = load_verses()

# Create embeddings for all verses
print("Creating embeddings for verses (CPU only)...")
verse_texts = [verse['text'] for verse in verses]
verse_embeddings = model.encode(verse_texts, show_progress_bar=True, device=device)
verse_embeddings = np.array(verse_embeddings)

print(f"Loaded {len(verses)} verses and created embeddings.")

def search_verses(query, top_k=5):
    """
    Search for relevant Quran verses using semantic similarity
    
    Args:
        query: Search query string
        top_k: Number of top results to return
    
    Returns:
        List of relevant verses with their details
    """
    if not query.strip():
        return []
    
    # Encode the query (CPU only)
    query_embedding = model.encode([query], device=device)
    
    # Calculate cosine similarity
    similarities = cosine_similarity(query_embedding, verse_embeddings)[0]
    
    # Get top k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Prepare results
    results = []
    for idx in top_indices:
        verse = verses[idx]
        similarity_score = similarities[idx]
        surah_num = verse['surah']
        results.append({
            'surah': surah_num,
            'surah_name': SURAH_NAMES.get(surah_num, f"Surah {surah_num}"),
            'ayah': verse['ayah'],
            'arabic': verse['arabic'],
            'translation': verse['translation'],
            'transliteration': verse['transliteration'],
            'similarity': float(similarity_score)
        })
    
    return results

def format_results(results):
    """Format search results for display"""
    if not results:
        return "No results found. Please try a different search query."
    
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(f"""
**Result {i}** (Similarity: {result['similarity']:.2%})
**{result['surah_name']} ({result['surah']}:{result['ayah']})**

**Arabic:**
{result['arabic']}

**Transliteration:**
{result['transliteration'] if result['transliteration'] else 'N/A'}

**Translation:**
{result['translation']}

---
""")
    
    return "\n".join(formatted)

def search_interface(query, num_results):
    """Gradio interface function"""
    if not query:
        return "Please enter a search query."
    
    results = search_verses(query, top_k=num_results)
    return format_results(results)

# Create Gradio interface
with gr.Blocks(title="AI-Powered Quran Verse Finder", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📖 AI-Powered Quran Verse Finder
    
    Search any topic and find relevant Quran verses using AI-powered semantic search.
    
    **How it works:** Enter a topic or question, and the system will find verses that are semantically similar to your query using advanced embeddings.
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Search Query",
                placeholder="e.g., mercy, prayer, patience, forgiveness, guidance...",
                lines=2
            )
            num_results = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Number of Results"
            )
            search_btn = gr.Button("🔍 Search Verses", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 💡 Example Queries:
            - "mercy and forgiveness"
            - "patience in hardship"
            - "prayer and worship"
            - "guidance and wisdom"
            - "gratitude and thankfulness"
            """)
    
    output = gr.Markdown(label="Search Results")
    
    # Set up event handlers
    search_btn.click(
        fn=search_interface,
        inputs=[query_input, num_results],
        outputs=output
    )
    
    query_input.submit(
        fn=search_interface,
        inputs=[query_input, num_results],
        outputs=output
    )
    
    gr.Markdown("""
    ---
    ### 📝 Note
    This tool uses semantic search powered by sentence transformers to find verses that are conceptually related to your query, even if they don't contain the exact keywords.
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)


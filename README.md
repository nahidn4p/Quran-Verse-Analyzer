# AI-Powered Quran Verse Finder

An intelligent search tool that uses AI embeddings to find relevant Quran verses based on semantic similarity. Simply search any topic, and the system will return verses that are conceptually related to your query.

## Features

- 🔍 **Semantic Search**: Uses advanced sentence transformers to find verses based on meaning, not just keywords
- 📖 **Comprehensive Results**: Returns Arabic text, transliteration, and English translation
- 🎨 **Beautiful UI**: Clean and intuitive Gradio interface
- ⚡ **Fast & Efficient**: Pre-computed embeddings for instant search results

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Quran-Verse-Analyzer
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   #Note: For CPU-only PyTorch (smaller download), use:
   #pip install torch --index-url https://download.pytorch.org/whl/cpu
   #The code is configured to use CPU only regardless of PyTorch installation.


   Note: The first run will download the sentence transformer model (~90MB), which may take a few minutes.

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - The app will be available at `http://localhost:7860`
   - Or use the public URL provided in the terminal (if using `share=True`)

3. **Search for verses:**
   - Enter any topic or question in the search box
   - Adjust the number of results using the slider
   - Click "Search Verses" or press Enter

## Example Queries

- "mercy and forgiveness"
- "patience in hardship"
- "prayer and worship"
- "guidance and wisdom"
- "gratitude and thankfulness"
- "creation of heavens and earth"
- "repentance and forgiveness"

## How It Works

1. **Embedding Generation**: All Quran verses are converted into high-dimensional vectors (embeddings) using a pre-trained sentence transformer model
2. **Query Processing**: Your search query is also converted into an embedding
3. **Similarity Matching**: The system calculates cosine similarity between your query and all verse embeddings
4. **Ranking**: Verses are ranked by similarity score and the top results are returned

## Project Structure

```
Quran-Verse-Analyzer/
├── app.py                    # Main application with Gradio UI
├── quran_verses.json         # Dataset of Quran verses (6,271 verses)
├── expand_quran_dataset.py   # Script to expand dataset from API
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Dataset

The dataset includes **12,186 verses** covering all 114 surahs of the Quran with:
- Arabic text (Uthmani script)
- English translation (Sahih International)
- Verse references (surah and ayah numbers)

This comprehensive dataset ensures you can find relevant verses for virtually any topic or question.

### Expanding the Dataset

To expand or update the dataset, you can use the provided script:

```bash
python expand_quran_dataset.py
```

This script fetches the complete Quran from the alquran.cloud API and merges it with existing verses.

Alternatively, you can manually edit `quran_verses.json` and add entries in the following format:

```json
{
  "surah": 1,
  "ayah": 1,
  "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "transliteration": "Bismillahi ar-Rahman ar-Rahim",
  "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful",
  "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful"
}
```

After adding verses, restart the application to regenerate embeddings.

## Technical Details

- **Model**: `all-MiniLM-L6-v2` (sentence-transformers)
- **Similarity Metric**: Cosine similarity
- **Framework**: Gradio for UI, scikit-learn for similarity calculations

## License

This project is open source. The Quran text translations are used for educational purposes.

## Contributing

Feel free to contribute by:
- Adding more verses to the dataset
- Improving the search algorithm
- Enhancing the UI/UX
- Adding new features

## Notes

- The dataset includes **12,186 verses** covering the complete Quran (all 114 surahs).
- The model will be downloaded automatically on first run (~90MB).
- Search results are ranked by semantic similarity, which may differ from keyword-based search.
- Initial embedding generation may take 2-5 minutes for the complete dataset (~12,000+ verses) depending on your CPU.


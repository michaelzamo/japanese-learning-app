from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Import de Sudachi pour le test immédiat (nous le déplacerons plus tard)
from sudachipy import tokenizer, dictionary

# Initialisation des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Japanese Reader API",
    description="Backend pour l'application d'étude du japonais (Clone LingQ)",
    version="0.1.0"
)

# Configuration CORS (Cross-Origin Resource Sharing)
# Indispensable pour que votre futur Frontend (React/Vue) puisse parler à ce Backend
origins = [
    "http://localhost:3000",  # Frontend local React standard
    "http://localhost:5173",  # Frontend local Vite/Vue standard
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialisation du Tokenizer Japonais (Sudachi) ---
# Mode A : Découpage court (ex: 食べたくなかった -> 食べ / たく / なかっ / た)
# Mode C : Découpage long (ex: 食べたくなかった -> 食べたくなかった)
# Pour l'apprentissage, le Mode A est souvent plus précis pour la grammaire.
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A

# --- Modèles de données (Pydantic) ---
class TextRequest(BaseModel):
    text: str

# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Japanese Reader. Le serveur tourne."}

@app.post("/api/test-nlp")
def test_japanese_analysis(request: TextRequest):
    """
    Endpoint temporaire pour tester le découpage de phrase.
    Envoie un texte japonais, reçoit les tokens.
    """
    try:
        text = request.text
        tokens = tokenizer_obj.tokenize(text, mode)
        
        results = []
        for t in tokens:
            results.append({
                "surface": t.surface(),             # Le mot tel qu'il apparaît
                "dictionary_form": t.dictionary_form(), # La forme dictionnaire (lemme)
                "part_of_speech": t.part_of_speech(),   # Nature grammaticale
                "reading": t.reading_form()             # Lecture (Katakana)
            })
            
        return {"original_text": text, "tokens": results}

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse : {e}")
        raise HTTPException(status_code=500, detail=str(e))

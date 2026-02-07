from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import logging

# Imports de nos modules locaux
from .db.base import SessionLocal, engine
from .db.init_db import init_models
from .models.card import UserCard, CardContext
from .models.dictionary import DictionaryEntry
from .services.srs_algorithm import calculate_next_review
from sudachipy import tokenizer, dictionary

# Initialisation
init_models()
app = FastAPI(title="Japanese Reader API")

# Configuration du Tokenizer Japonais
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèles Pydantic (Validation) ---
class TextRequest(BaseModel):
    text: str

class CardCreate(BaseModel):
    word_text: str
    reading: str
    lemma: str
    definition: str
    sentence_context: str

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/")
def read_root():
    return {"status": "online"}

@app.post("/api/test-nlp")
def test_japanese_analysis(request: TextRequest, db: Session = Depends(get_db)):
    try:
        tokens = tokenizer_obj.tokenize(request.text, mode)
        results = []
        for t in tokens:
            lemma = t.dictionary_form()
            # Recherche de la définition
            dict_entry = db.query(DictionaryEntry).filter(
                (DictionaryEntry.kanji == lemma) | (DictionaryEntry.reading == lemma)
            ).first()
            
            results.append({
                "surface": t.surface(),
                "dictionary_form": lemma,
                "reading": t.reading_form(),
                "part_of_speech": t.part_of_speech(),
                "definition": dict_entry.definitions if dict_entry else "No definition found"
            })
        return {"tokens": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cards")
def create_card(card_data: CardCreate, db: Session = Depends(get_db)):
    new_card = UserCard(
        word_text=card_data.word_text,
        reading=card_data.reading,
        lemma=card_data.lemma,
        definition=card_data.definition,
        next_review_date=datetime.now()
    )
    db.add(new_card)
    db.flush()
    new_context = CardContext(card_id=new_card.id, sentence_text=card_data.sentence_context)
    db.add(new_context)
    db.commit()
    return {"id": new_card.id}

@app.get("/api/reviews")
def get_reviews(db: Session = Depends(get_db)):
    now = datetime.now()
    reviews = db.query(UserCard).filter(UserCard.next_review_date <= now).all()
    results = []
    for card in reviews:
        context = db.query(CardContext).filter(CardContext.card_id == card.id).first()
        results.append({
            "id": card.id,
            "word_text": card.word_text,
            "reading": card.reading,
            "definition": card.definition,
            "context_sentence": context.sentence_text if context else ""
        })
    return results

@app.post("/api/reviews/{card_id}")
def update_card_srs(card_id: int, quality: str, db: Session = Depends(get_db)):
    card = db.query(UserCard).filter(UserCard.id == card_id).first()
    if not card: raise HTTPException(status_code=404)
    # Note: Assurez-vous que calculate_next_review est bien importé
    new_interval, new_ease, next_date = calculate_next_review(card.interval, card.ease_factor, quality)
    card.interval = new_interval
    card.ease_factor = new_ease
    card.next_review_date = next_date
    db.commit()
    return {"next_review": next_date}




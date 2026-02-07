from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Sera lié à l'User plus tard
    
    # Informations sur le mot
    word_text = Column(String, index=True)      # ex: 会う
    reading = Column(String)                    # ex: あう
    lemma = Column(String)                      # Forme dico pour le lien dictionnaire
    definition = Column(Text)                   # Définition sauvegardée
    pitch_accent = Column(Integer, nullable=True) # ex: 0
    
    # Logique SRS (Spaced Repetition System)
    status = Column(String, default="learning") # learning, mastered, ignored
    interval = Column(Integer, default=1)       # En jours
    ease_factor = Column(Float, default=2.5)    # Facteur multiplicateur (SM-2)
    next_review_date = Column(DateTime(timezone=True), server_default=func.now())
    last_review_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relation : Une carte possède une ou plusieurs phrases de contexte
    contexts = relationship("CardContext", back_populates="card", cascade="all, delete-orphan")

class CardContext(Base):
    __tablename__ = "card_contexts"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("user_cards.id"))
    
    # La phrase complète
    sentence_text = Column(Text, nullable=False)
    # Optionnel : ID du texte d'origine pour y revenir si besoin
    source_text_id = Column(Integer, nullable=True) 

    card = relationship("UserCard", back_populates="contexts")

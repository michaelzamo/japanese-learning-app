from .base import Base, engine
# IMPORT IMPORTANT :
from ..models.card import UserCard, CardContext
from ..models.dictionary import DictionaryEntry 

def init_models():
    Base.metadata.create_all(bind=engine)
    print("Tables créées : user_cards, card_contexts, dictionary")

if __name__ == "__main__":
    init_models()

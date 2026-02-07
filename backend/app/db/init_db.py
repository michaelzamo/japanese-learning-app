from .base import Base, engine
from ..models.card import UserCard, CardContext

def init_models():
    # Cette commande crée toutes les tables définies dans nos modèles
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès (Tables user_cards et card_contexts créées).")

if __name__ == "__main__":
    init_models()

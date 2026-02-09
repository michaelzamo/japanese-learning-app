import json
import os
from sqlalchemy.orm import Session
from app.db.base import SessionLocal, engine
from app.models.dictionary import DictionaryEntry

def import_yomitan_json():
    # Chemin vers le dossier où vous avez décompressé le ZIP
    data_dir = "data/" 
    db = SessionLocal()
    
    # Trouver tous les fichiers term_bank
    files = [f for f in os.listdir(data_dir) if f.startswith('term_bank')]
    
    if not files:
        print("Aucun fichier term_bank_*.json trouvé dans le dossier data/")
        return

    print(f"Début de l'importation de {len(files)} fichiers JSON...")

    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            entries = json.load(f)
            
            entries_to_add = []
            for entry in entries:
                kanji = entry[0]
                reading = entry[1]
                definitions_list = entry[5]
                
                # --- NOUVELLE LOGIQUE DE NETTOYAGE ---
                clean_defs = []
                if isinstance(definitions_list, list):
                    for d in definitions_list:
                        if isinstance(d, str):
                            clean_defs.append(d)
                        elif isinstance(d, dict):
                            # Pour le format "Structured Content" de Yomitan
                            # On récupère récursivement le texte si présent
                            content = d.get('content') or d.get('text') or ""
                            if isinstance(content, str):
                                clean_defs.append(content)
                            elif isinstance(content, list):
                                # Parfois content est lui-même une liste
                                clean_defs.append(" ".join([str(i) for i in content if isinstance(i, str)]))
                
                definitions_str = " / ".join(clean_defs) if clean_defs else "No definition"
                # -------------------------------------

                db_entry = DictionaryEntry(
                    kanji=kanji,
                    reading=reading,
                    definitions=definitions_str
                )
                entries_to_add.append(db_entry)

            # Insertion par lot pour la rapidité
            db.bulk_save_objects(entries_to_add)
            db.commit()
            print(f"Importé : {file_name}")

    db.close()
    print("Importation terminée avec succès !")

def extract_text(data):
    """Extrait récursivement tout le texte d'une structure Yomitan complexe."""
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return " ".join([extract_text(i) for i in data if i is not None])
    if isinstance(data, dict):
        # On cherche les clés classiques de contenu dans Yomitan
        content = data.get('content') or data.get('text') or ""
        return extract_text(content)
    return ""

def import_yomitan_json():
    data_dir = "data/" 
    db = SessionLocal()
    
    files = [f for f in os.listdir(data_dir) if f.startswith('term_bank')]
    if not files:
        print("Aucun fichier trouvé.")
        return

    print(f"Début de l'importation de {len(files)} fichiers...")

    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                entries = json.load(f)
                entries_to_add = []
                for entry in entries:
                    # Index 0: Kanji, Index 1: Reading, Index 5: Definitions
                    kanji = str(entry[0])
                    reading = str(entry[1])
                    raw_definitions = entry[5]
                    
                    # On utilise notre nouvelle fonction d'extraction
                    clean_defs = []
                    if isinstance(raw_definitions, list):
                        for item in raw_definitions:
                            text = extract_text(item).strip()
                            if text:
                                clean_defs.append(text)
                    
                    definitions_str = " / ".join(clean_defs) if clean_defs else "No definition"

                    entries_to_add.append(DictionaryEntry(
                        kanji=kanji,
                        reading=reading,
                        definitions=definitions_str
                    ))

                db.bulk_save_objects(entries_to_add)
                db.commit()
                print(f"Importé avec succès : {file_name}")
            except Exception as e:
                print(f"Erreur sur le fichier {file_name}: {e}")
                db.rollback()

    db.close()
    print("Importation terminée !")


if __name__ == "__main__":
    import_yomitan_json()

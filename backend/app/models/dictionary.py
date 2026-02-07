from sqlalchemy import Column, Integer, String, Text
from ..db.base import Base

class DictionaryEntry(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(String, index=True)    # ex: 食べる
    reading = Column(String, index=True)  # ex: たべる
    definitions = Column(Text)            # JSON ou texte long (manger, to eat)

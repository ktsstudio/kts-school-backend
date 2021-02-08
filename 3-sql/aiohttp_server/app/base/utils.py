from typing import Tuple
from textblob import TextBlob


def analyze_text(text: str) -> Tuple[float, float]:
    blob_text = TextBlob(text)
    return blob_text.polarity, blob_text.subjectivity

from keybert import KeyBERT  # type: ignore

from nespresso.recsys.preprocessing.model import model

keyword_model = KeyBERT(model=model)


def ExtractKeywords(text: str, top_n: int = 10) -> str:
    keywords = keyword_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        use_maxsum=True,
        nr_candidates=50,
        top_n=top_n,
    )

    return ", ".join([kw for kw, _ in keywords])

#!/usr/bin/env python3

#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from datetime import datetime
from os import getenv
import spacy
from fastapi import FastAPI
from fastapi import HTTPException
from models import SentencesRequest, WordsRequest, HealthResponse, TokenizerResponse, Language, ParagraphsRequest

# Load SpaCy language model
nlps = {
    Language.en: spacy.load("en_core_web_md"),
    Language.fr: spacy.load("fr_core_news_md"),
}

app = FastAPI()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": getenv("VERSION", "0.0.0"),
        "build_id": getenv("BUILD_ID", "0")
    }


@app.post("/tokenize/sentences", response_model=TokenizerResponse)
async def tokenize_sentences(request: SentencesRequest):
    """Tokenize text into sentences."""
    try:
        doc = nlps[request.lang](request.text)

        return {"tokens": [sent.text for sent in doc.sents]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tokenize/words", response_model=TokenizerResponse)
async def tokenize_words(request: WordsRequest):
    """Tokenize text into words."""
    try:
        doc = nlps[request.lang](request.text)

        # Extract tokens excluding punctuations
        if request.exclude_punct:
            tokens = [token.text for token in doc if not token.is_punct]

        # Extract all tokens, including punctuations
        else:
            tokens = [token.text for token in doc]

        # Lowercase tokens if requested
        if request.lowercase:
            tokens = [token.lower() for token in tokens]

        return {"tokens": tokens}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tokenize/paragraphs", response_model=TokenizerResponse)
async def tokenize_words(request: ParagraphsRequest):
    """Tokenize text into paragraphs."""
    try:
        doc = nlps[request.lang](request.text)

        # Extract paragraphs
        start = 0
        paragraphs = []
        for token in doc:
            if token.is_space and token.text.count("\n") > 1:
                paragraphs.append(doc[start:token.i].text.strip())
                start = token.i
        paragraphs.append(doc[start:].text.strip())

        return {"tokens": paragraphs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#!/usr/bin/env python3

#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import SentencesRequest, WordsRequest, HealthResponse, TokenizerResponse, Language, VectorizerResponse
from fastapi import UploadFile, File, HTTPException
import spacy
from spacy_layout import spaCyLayout
from os import getenv

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
        # Use SpaCy to tokenize into sentences
        doc = nlps[request.lang](request.text)
        tokens = [sent.text for sent in doc.sents]

        return {"tokens": tokens}
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


# @todo
@app.post("/tokenize/pdf")
async def vectorize_pdf(file: UploadFile = File(...), lang: Language = Language.en):
    """Extract text from a PDF file and tokenize it."""
    try:
        nlp = spacy.blank(lang.name)
        layout = spaCyLayout(nlp)

        # Process a document and create a spaCy Doc object
        doc = layout(await file.read())

        return doc._.layout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the PDF: {str(e)}")
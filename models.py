#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from enum import Enum
from pydantic import BaseModel
from typing import List

class Language(Enum):
    fr = "fr"
    en = "en"

class BaseRequest(BaseModel):
    lang: Language = "en"
    text: str

class SentencesRequest(BaseRequest):
    pass

class ParagraphsRequest(BaseRequest):
    pass

class WordsRequest(BaseRequest):
    exclude_punct: bool = True
    lowercase: bool = False

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    build_id: str

class TokenizerResponse(BaseModel):
    tokens: list[str]

class VectorizerResponse(BaseModel):
    vectors: List[List[float]]  # List of vectors for blocks

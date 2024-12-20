# NLP Tokenizer

[![Code Inc.](https://img.shields.io/badge/Powered%20by-Code%20Inc.-blue)](https://www.codeinc.co)
[![Docker Image CI](https://github.com/codeinchq/nlp-tokenizer/actions/workflows/docker-image.yml/badge.svg)](https://github.com/codeinchq/nlp-tokenizer/actions/workflows/docker-image.yml)
[![Docker Image Version](https://img.shields.io/docker/v/codeinchq/nlp-tokenizer?sort=semver&label=Docker%20Hub&color=red)](https://hub.docker.com/r/codeinchq/nlp-tokenizer/tags)

This repository contains a simple containerized API to tokenize text using the [spaCy](https://spacy.io/) library. The API is built using [FastAPI](https://fastapi.tiangolo.com/).

The image is available on [Docker Hub](https://hub.docker.com/r/codeinchq/nlp-tokenizer) under the name `codeinchq/nlp-tokenizer`.

## Configuration

By default, the container listens on port 3000. The port is configurable using the `PORT` environment variable.

## Usage

To run locally the container, execute the following command:

```shell
docker run -p "8000:8000" codeinchq/nlp-tokenizer
```

### Sentence Tokenization

```shell
curl -X POST "http://127.0.0.1:8000/tokenize/sentences" \
-H "Content-Type: application/json" \
-d '{"text": "This is a sample sentence for the documentation. It is used for illustrative purposes."}'
```

#### In French
```shell
curl -X POST "http://127.0.0.1:8000/tokenize/sentences" \
-H "Content-Type: application/json" \
-d '{"lang": "fr", "text": "Ceci est une phrase d’exemple pour la documentation. Elle est utilisée à des fins illustratives."}'
```

### Word Tokenization

```shell
curl -X POST "http://127.0.0.1:8000/tokenize/words" \
-H "Content-Type: application/json" \
-d '{"text": "This is a sample sentence for the documentation. It is used for illustrative purposes."}'
```

#### In French
```shell
curl -X POST "http://127.0.0.1:8000/tokenize/words" \
-H "Content-Type: application/json" \
-d '{"lang": "fr", "text": "Ceci est une phrase d’exemple pour la documentation. Elle est utilisée à des fins illustratives."}'
```

### Health check

A health check is available at the `/health` endpoint. The server returns a status code of `200` if the service is healthy, along with a JSON object:
```json
{ "status": "up", "timestamp": "0001-01-01T00:00:00Z" }
```

## Client

A PHP 8 client is available at on [GitHub](https://github.com/codeinchq/document-cloud-php-client) and [Packagist](https://packagist.org/packages/codeinc/document-cloud-client).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/codeinchq/nlp-tokenizer?tab=MIT-1-ov-file) file for details.

# Remarks
This project is just an experiment with using AI with datasets
You should modify it with different datasets for increased usability 
Not for practical use

# Project Title

This project demonstrates the integration of AstraDB with OpenAI's GPT-3 to store and retrieve text embeddings and perform similarity searches.

## Description

This application uses AstraDB's Cassandra database to store text embeddings generated by OpenAI's GPT-3 model. 
It allows users to input a question and retrieve similar headlines from a dataset sourced from Hugging Face's `datasets` library.

## Getting Started

### Dependencies

- Python 3.x
- `cassandra-driver`
- `langchain` library
- `datasets` from Hugging Face

### Installing

- Install the required packages using `pip install [Package]` 

### Setting up AstraDB

- Sign up for AstraDB and create a database.
- Obtain your secure bundle path, application token, client ID, and client secret from AstraDB.

### Setting up OpenAI API

- Sign up for OpenAI and obtain an API key for GPT-3.

### Configuration

Update the following environment variables with your AstraDB and OpenAI API details:

```plaintext
ASTRA_DB_SECURE_BUNDLE_PATH="your secure bundle path here"
ASTRA_DB_APPLICATION_TOKEN="Your token here"
ASTRA_DB_CLIENT_ID="Your client id here"
ASTRA_DB_CLIENT_SECRET ="Your client secret here"
ASTRA_DB_KEYSPACE="search"
OPENAI_API_KEY="Your openai api key here"
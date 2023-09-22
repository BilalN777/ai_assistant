ASTRA_DB_SECURE_BUNDLE_PATH="/Users/Bilal/personal_proj/ai_assistant/secure-connect-vector-db.zip"
ASTRA_DB_APPLICATION_TOKEN="AstraCS:kzpbZKaNnTCoJWwBXvaTezHK:ca4b83b9f3f00ef79dd42fc46dc63ee0c07d642a1d65aea50b8840d86d9ed779"
ASTRA_DB_CLIENT_ID="kzpbZKaNnTCoJWwBXvaTezHK"
ASTRA_DB_CLIENT_SECRET ="+X6IS1b2iNMLq.8l9YEUcpy2wJ,+JgK4FsqZlT8RN0e9whm58_P-BsQ_4nvJZWEHvRJMrcXSo5NM5,,ZHf02O.BpMEYFJbkEcY0BoN,76TPlcT6Rv2MdP+j57y6dKo62"
ASTRA_DB_KEYSPACE="search"
OPENAI_API_KEY="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"

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from datasets import load_dataset

cloud_config= {
        'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="qa_mini_demo",
)

print("Loading data from huggingface")
dataset = load_dataset("Biddls/Onion_News", split="train")
headlines = dataset["text"][:50]

print("\nGenerating embedding and storing in AstraDB")
myCassandraVStore.add_texts(headlines)

print("Inserted %i headlines.\n" % len(headlines))

vectorIdx = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)

first_question = True
while True:
    if first_question:
        query_text = input("Ask me a question: (or type 'quit to exit): ")
        first_question = False
    else:
        query_text = input("Ask me another question: (or type 'quit to exit): ")

    if query_text == "quit":
        break

    print("QUESTION: \%s\"" % query_text)
    answer = vectorIdx.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    print("DOCUMENTS BY RELEVANCE:")
    for doc, score in myCassandraVStore.similarity_search_with_score(query_text, k=4):
        print("  %0.4f \"%s...\"" % (score, doc.page_content[:60]))
        
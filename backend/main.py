from text_extractor import TextExtraction
from text_chunker import ChunkText
from sentence_encoder import SentenceEncoder
from faiss_indexer import FaissIndexer

import os
import uuid
import sys
import spacy
import json
import uvicorn
import faiss 
from fastapi import FastAPI, Request, status
from db import Chunk, init_db, engine, get_session
from spacy.cli import download
import logging as log
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
download("en_core_web_sm")
sys.path.append(os.path.abspath("C:/Users/emada/Documents/partial-solutions-1/partial-solutions-1"))
faiss_indexer = FaissIndexer(None, 'hnsw')

directory = 'files'

from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel import Session


app = FastAPI()
session = Session(engine)


@app.get("/")
async def read_root():
    result = session.query(Chunk).all()
    return [Chunk(text=chunk.text, embedding=chunk.embedding, id=chunk.id) for chunk in result]


@app.on_event("startup")
def startup():
    init_db()
    process_files()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	log.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

base_index = faiss.IndexFlatL2(512) #TODO extract this from embedding
index = faiss.IndexIDMap(base_index)
def process_files():
    vectors = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # Step 1: Extract Text from file
        text_extractor = TextExtraction.to_text(f)
        # Step 2: Create chunks from text
        chunks = ChunkText().create_chunks(text_extractor)
        # Step 3: Encode chunks into vectors
        vectors = SentenceEncoder().encode(chunks)
        id_list = []
        for idx, chunk in enumerate(chunks):
            chunk = chunk.replace("\x00", "\uFFFD")
            embedding_vector = vectors[idx]
            embedding_vector_array = embedding_vector.tolist()
            vector = json.dumps({'embedding': embedding_vector_array})
            chunk = Chunk(text=chunk, embedding=vector)
            session.add(chunk)
            session.commit()
            session.refresh(chunk)
            id_list.append(chunk.id)
        index.add_with_ids(vectors, id_list)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/chunks", response_model=list[Chunk])
def get_chunks(session: Session = Depends(get_session)):
    result = session.execute(select(Chunk))
    chunks = result.scalars().all()
    return [Chunk(text=chunk.text, id=chunk.id) for chunk in chunks]

@app.post("/addChunk")
def add_chunk(chunk, session: Session = Depends(get_session)):
    chunk = Chunk(text=chunk.text, embeddings=chunk.embeddings)
    session.add(chunk)
    session.commit()
    session.refresh(chunk)
    return chunk

@app.post("/search/")
async def search(data: dict):
    search = data['search']
    log.info(f'Seach query: {search}')
    search_query_encoded = SentenceEncoder().encode([search])
    #log.info(f'search encoced {search_query_encoded}')
    D, I = index.search(search_query_encoded, 4)
    indices = I[0]
    results = []
    log.info(f'index {indices}')
    for i in indices:
        id = i.item()
        log.info(f'index searches {id}')
        chunk = session.get(Chunk, id)
        if not chunk:
            log.error(f'Chunk with index {i} not found')
        chunk_text = chunk.text
        results.append(chunk_text)
    log.info(f'search index {I}')
    log.info(f'results {results}')
    return { "results": results}

if __name__ == '__main__':
    # input
    '''
                for vector, idx in vectors:
            # insert into sql -> get chunk_id
        # id = uuid.uuid4() # REMOVE
        print(len(vector))
        vector_entries.append(vector)
    '''
    # Step 4: Store vectors in vector index
    #faiss_indexer.add(vectors)
    #app.run(host="0.0.0.0", debug=True)
    #uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

    # Step 5 - take in input from user and return 3 nearest search document - include sentences, not just the vectors as numbers
            
    # step 6 - find the chunk from index_result
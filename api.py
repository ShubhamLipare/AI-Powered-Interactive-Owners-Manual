from fastapi import FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.ingestion import DataIngestion
from src.retriever import ConversationRAG
from src.database_layer import *
from Models.schema import ChatRequest
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException

app = FastAPI(title="Owners Manual API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
async def ingest_documents(files: list[UploadFile]):
    try:
        log.info(f"Received {len(files)} files for ingestion.")
        log.info(f"files: {[file.filename for file in files]}")
        ingestion = DataIngestion()
        ingestion.build_retriever(files,2000,200,5)
        return {"status_code": 200, "message": "Documents ingested successfully."}
    except CustomException as e:
        log.error(f"Error during ingestion: {e}")
        raise e

@app.post("/chat")
async def chat_with_manual(payload:ChatRequest):
    try:
        session_id=payload.session_id
        query = payload.query
        history = get_messages(session_id)
        log.info(f"Received query: {query}")
        rag = ConversationRAG(session_id=session_id)
        rag.load_retriever_from_faiss(index_dir="faiss_index",index_name="index",search_type="similarity",search_kwargs={"k":5})
        response = rag.invoke(user_query=query, conversation_history=history)
        save_message(session_id, "user", query)
        save_message(session_id, "assistant", response)
        log.info(f"Generated response")
        return {"status_code": 200, "response": response}
    except CustomException as e:
        log.error(f"Error during chat: {e}")
        raise e
    
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from prompt.prompt_library import final_answer_prompt,query_enhancement_prompt
from src.ingestion import DataIngestion
from utils.model_loader import ModelLoader
from utils.document_ops import generate_session_id
import os
from typing import Optional
from operator import itemgetter

class ConversationRAG:
    def __init__(self,session_id:Optional[str],retriever=None):
        self.llm=self._load_llm()
        self.embedding_model=ModelLoader().load_embedding_model()
        self.session_id=session_id or generate_session_id()
        self.qa_prompt=final_answer_prompt
        self.query_enhancement_prompt=query_enhancement_prompt

        self.chain=None
        self.retriever=retriever

    def _load_llm(self):
        try:
            llm=ModelLoader().load_llm()
            if not llm:
                raise CustomException("LLM model could not be loaded.")
            log.info("LLM model loaded successfully.")
            return llm
        except Exception as e:
            log.error(f"Error loading LLM model: {e}")
            raise CustomException(f"Error loading LLM model: {e}")
    @staticmethod
    def _format_docs(docs) -> str:
        return "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)
    
    def load_retriever_from_faiss(self,index_dir,index_name,search_type,search_kwargs,k=5):
        try:
            log.info(f"Loading FAISS index from directory: {index_dir}")
            if not os.path.exists(index_dir):
                raise CustomException(f"FAISS index directory '{index_dir}' does not exist.")
            self.vectorestore=FAISS.load_local(index_dir, self.embedding_model,index_name,allow_dangerous_deserialization=True)
            log.info("FAISS index loaded into vector store.")
            if search_kwargs is None:
                search_kwargs={"k":k}
            self.retriever=self.vectorestore.as_retriever(search_type=search_type,search_kwargs=search_kwargs)
            log.info("Retriever loaded successfully, building RAG chain.")
            self._build_chain()
            return self.retriever
        except Exception as e:
            log.error(f"Error loading FAISS index: {e}")
            raise CustomException(f"Error loading FAISS index: {e}")
        
    def invoke(self,user_query,conversation_history=None):
        try:
            log.info(f"Invoking RAG chain for user query: {user_query}")
            if self.chain is None:
                raise CustomException("RAG chain is not built.")
            response=self.chain.invoke({"user_query":user_query,
                                        "conversation_history":conversation_history or []})
            if not response:
                raise CustomException("No response generated from RAG chain.")
            log.info("RAG chain invoked successfully. Returning response.")
            return response
        except Exception as e:
            log.error(f"Error invoking RAG chain: {e}")
            raise CustomException(f"Error invoking RAG chain: {e}")
    
    def _build_chain(self):
        try:
            if self.retriever is None:
                raise CustomException("Retriever is not initialized.")
            question_rewritter= ({"user_query":itemgetter("user_query"),"conversation_history":itemgetter("conversation_history")} |self.query_enhancement_prompt | self.llm | StrOutputParser())
            log.info(f"question rewritter:{question_rewritter}")
            retrieve_docs= question_rewritter | self.retriever | self._format_docs
            log.info(f"retrieve_docs:{retrieve_docs}")
            self.chain= ({"user_query":itemgetter("user_query"),
                          "conversation_history":itemgetter("conversation_history"),
                          "retrieved_context":retrieve_docs}
                         | self.qa_prompt
                         | self.llm
                         | StrOutputParser())
            log.info("QA chain built successfully.")
        except Exception as e:
            log.error(f"Error building QA chain: {e}")
            raise CustomException(f"Error building QA chain: {e}")

if __name__ == "__main__":
    session_id="test_session"
    rag = ConversationRAG(session_id=session_id)
    rag.load_retriever_from_faiss(index_dir="faiss_index",index_name="index",search_type="similarity",search_kwargs={"k":5})
    user_query = "How does attention head works?"
    conversation_history = []
    response = rag.invoke(user_query=user_query, conversation_history=conversation_history)
    print("Response:", response)
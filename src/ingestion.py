from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from utils.document_ops import save_uploaded_file,load_document,get_project_root, generate_session_id
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DataIngestion:
    def __init__(self):
        self.session_id = generate_session_id()
        self.session_path = get_project_root() / "data" / self.session_id

    def chunk_and_store(self,uploaded_files,chunk_size,chunk_overlap):
        try:
            uploads_path = self.session_path / "uploads"
            loaded_docs_path = self.session_path / "loaded_docs"
            chunked_docs_path = self.session_path / "chunked_docs"
            saved_files = save_uploaded_file(uploaded_files, uploads_path)
            documents = load_document(saved_files, loaded_docs_path)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            chunks = text_splitter.split_documents(documents)
            #saving chunked docs in local
            os.makedirs(chunked_docs_path, exist_ok=True)
            with open(chunked_docs_path / "chunked_docs.txt", "w", encoding="utf-8") as f:
                for i, doc in enumerate(chunks):
                    f.write(f"{'*'*40} chunk {i+1} {'*'*40}\n")
                    f.write(doc.page_content + "\n")
            log.info(f"Successfully chuncked data into {len(chunks)} chunks in session {self.session_id}.")
            return chunks
        except CustomException as ce:
            log.error(f"Data ingestion failed: {ce}")
            raise CustomException("Data ingestion process failed.", ce) from ce
        
class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()
if __name__ == "__main__":
    ingestion = DataIngestion()
    file_path=Path(r"C:\Users\Shubham\Downloads\Attention Is All You Need.pdf")
    dummy_file=DummyFile(file_path)
    chunks = ingestion.chunk_and_store([dummy_file], 1000, 200)
    print(f"Processed in session: {ingestion.session_id}")
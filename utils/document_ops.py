import uuid
from datetime import datetime, timezone, timedelta
import re
import os
from pathlib import Path
from typing import List,Iterable
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from langchain_community.document_loaders import PyMuPDFLoader 

SUPPORTED_EXTENSIONS = {".pdf"}

def get_project_root():
    """Get the root path of the project."""
    return Path(__file__).resolve().parent.parent

def generate_session_id(prefix: str = "session") -> str:
    # IST is UTC+5:30
    ist = timezone(timedelta(hours=5, minutes=30))
    return f"{prefix}_{datetime.now(ist).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def save_uploaded_file(uploaded_file, target_path: str) -> str:
    try:
        log.info(f"Saving uploaded files to {target_path}")
        target_path.mkdir(parents=True, exist_ok=True)
        saved:List[Path] = []
        for uf in uploaded_file:
            log.info(f"Processing uploaded file: {uf}")
            #Handle FastAPI UploadFile
            if hasattr(uf, "filename"):
                name = uf.filename
                file_bytes = uf.file.read()
            # Handle Streamlit UploadedFile / DummyFile
            elif hasattr(uf, "name"):
                name = uf.name
                file_bytes = uf.getbuffer()
            else:
                raise CustomException("Unsupported uploaded file type")

            ext = Path(name).suffix.lower()
            log.info(f"File name : {name} , File extension: {ext}")
            if ext not in SUPPORTED_EXTENSIONS:
                raise CustomException(f"Unsupported file extension: {ext}. Supported extensions are: {SUPPORTED_EXTENSIONS}")
            # Clean file name (only alphanum, dash, underscore)
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', Path(name).stem).lower()
            fname = f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"
            out = target_path / fname
            with open(out, "wb") as f:
                f.write(file_bytes)
            # with open(out, "wb") as f:
            #     if hasattr(uf, "read"):
            #         f.write(uf.read())
            #     else:
            #         f.write(uf.getbuffer())
            saved.append(out)
        log.info(f"Saved uploaded files: {saved}")
        return saved

    except Exception as e:
        log.error(f"Error in save_uploaded_file: {e}")
        raise CustomException(e)

def load_document(folder_paths: List[Path], save_path: Path = None):
    try:
        log.info(f"Loading documents from: {folder_paths}")
        docs = []
        for p in folder_paths:
            if p.is_file() and p.suffix.lower() == ".pdf":
                loader=PyMuPDFLoader(str(p))
                docs.extend(loader.load())
        if save_path:
            #saving doc file in local
            os.makedirs(save_path, exist_ok=True)
            with open(save_path / "loaded_docs.txt", "w",encoding="utf-8") as f:
                for i, doc in enumerate(docs):
                    f.write(f"{'*'*40} Document {i+1} {'*'*40}\n")
                    f.write(doc.page_content + "\n")
        log.info(f"Loaded {len(docs)} documents from {folder_paths}")
        return docs
    except Exception as e:
        log.error(f"Error in load_document: {e}")
        raise CustomException(e)

#created DummyFile function for testing purpose
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()
    
# if __name__=="__main__":
#     file_path=Path(r"C:\Users\Shubham\Downloads\Attention Is All You Need.pdf")
#     dummy_file=DummyFile(file_path)
#     saved_files=save_uploaded_file([dummy_file],Path("uploads"))
#     loaded_docs=load_document(saved_files)
#     print(loaded_docs[0].page_content[:500])
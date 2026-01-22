import uuid
from zoneinfo import ZoneInfo
from datetime import datetime
import re
from pathlib import Path
from typing import List,Iterable
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from langchain_community.document_loaders import PyMuPDFLoader 

SUPPORTED_EXTENSIONS = {".pdf"}

def generate_session_id(prefix: str = "session") -> str:
    ist = ZoneInfo("Asia/Kolkata")
    return f"{prefix}_{datetime.now(ist).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def save_uploaded_file(uploaded_file, target_path: str) -> str:
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        saved:List[Path] = []
        for uf in uploaded_file:
            name=getattr(uf,"name","file")
            ext=Path(name).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                raise CustomException(f"Unsupported file extension: {ext}. Supported extensions are: {SUPPORTED_EXTENSIONS}")
            # Clean file name (only alphanum, dash, underscore)
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', Path(name).stem).lower()
            fname = f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"
            out = target_path / fname
            with open(out, "wb") as f:
                if hasattr(uf, "read"):
                    f.write(uf.read())
                else:
                    f.write(uf.getbuffer())
            saved.append(out)
        log.info(f"Saved uploaded files: {saved}")
        return saved

    except Exception as e:
        log.error(f"Error in save_uploaded_file: {e}")
        raise CustomException(e)

def load_document(folder_paths: List[Path]):
    try:
        docs = []
        for p in folder_paths:
            ext=p.suffix.lower()
            if ext == ".pdf":
                loader=PyMuPDFLoader(str(p))
            docs.extend(loader.load())
        log.info(f"Loaded {len(docs)} documents from {folder_paths}")
        return docs
    except Exception as e:
        log.error(f"Error in load_document: {e}")
        raise CustomException(e)
    
class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()
    
# if __name__=="__main__":
#     file_path=Path(r"C:\Users\Shubham\Downloads\Attention Is All You Need.pdf")
#     dummy_file=DummyFile(file_path)
#     saved_files=save_uploaded_file([dummy_file],Path("uploads"))
#     loaded_docs=load_document(saved_files)
#     print(loaded_docs[0].page_content[:500])
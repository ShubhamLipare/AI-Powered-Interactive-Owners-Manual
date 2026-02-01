import importlib.metadata
packages = [
    "python-dotenv",
    "ipykernel",
    "langchain",
    "langchain-core",
    "langchain-community",
    "langchain-huggingface",
    "langchain-groq",
    "langchain-google-genai",
    "transformers",
    "sentence-transformers",
    "pymupdf",
    "fastembed",
    "faiss-cpu",
    "fastapi",
    "streamlit",
    "uvicorn",
    "python-multipart",
    "ragas"
]
for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")

# # serve static & templates
# app.mount("/static", StaticFiles(directory="../static"), name="static")
# templates = Jinja2Templates(directory="../templates")
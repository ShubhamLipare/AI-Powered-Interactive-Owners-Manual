from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

from utils.config_loder import load_config
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException

class ModelLoader:
    def __init__(self):
        self.config = load_config('config/config.yaml')
        log.info("Configuration loaded successfully.")
        self.api_key=os.getenv("LLM_API_KEY")
        self.embedding_key=os.getenv("EMBEDDING_API_KEY")

    def load_llm(self):
        try:
            llm_block=self.config.get('llm', {})
            provider_key=os.getenv("LLM_PROVIDER","groq")

            llm_config=llm_block[provider_key]
            provider=llm_config.get("provider")
            model_name=llm_config.get("model_name")
            temperature=llm_config.get("temperature",0)
            max_tokens=llm_config.get("max_tokens",1024)

            if provider=="groq":
                log.info("Loading Groq LLM model.")
                return ChatGroq(
                    model=model_name,
                    api_key=self.api_key,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif provider=="google":
                log.info("Loading Google Generative AI LLM model.")
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_key,
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
        except Exception as e:
            log.error(f"Error loading LLM model: {e}")
            raise CustomException(e)


    def load_embedding_model(self):
        try:
            embedding_block=self.config.get('embedding_model', {})
            model_name=embedding_block.get('model_name')
            log.info(f"loading embedding model: {model_name}")
            return  FastEmbedEmbeddings(model_name=model_name)
        except Exception as e:
            log.error(f"Error loading embedding model: {e}")
            raise CustomException(e)
    
if __name__ == "__main__":
    loader=ModelLoader()
    llm=loader.load_llm()
    tokenizer=loader.load_embedding_model()
    print(llm.invoke("Hello, how are you?"))
    sentences = ['This is an example sentence', 'Each sentence is converted']
    encoded_input = tokenizer(sentences, padding=True, truncation=True)
    print(encoded_input)
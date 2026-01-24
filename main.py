from utils.model_loader import ModelLoader


def main():
    model_loader = ModelLoader()
    llm = model_loader.load_llm()
    print(llm.invoke("write a code for fibonacci in python"))

if __name__ == "__main__":
    main()

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text):
        spiltter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        chunks = spiltter.split_text(text)
        return chunks
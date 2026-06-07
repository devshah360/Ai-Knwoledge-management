import os
from sqlalchemy.orm import Session
from app.models.document_model import Document
from app.services.pdf_service import extract_text_from_pdf
from app.services.elastic_service import index_document
from app.services.embedding_service import generate_embedding
from app.services.chunk_service import chunk_text
from app.services.vectorstore_service import add_document_chunks
from tasks import process_document_tasks

UPLOADED_FOLDER = "app/uploads"

def save_uploaded_file(
                file,
                current_user,
                db:Session
):
        
        file_location = f"{UPLOADED_FOLDER}/{file.filename}"

        with open(file_location,"wb") as buffer:
                buffer.write(file.file.read())

        extracted_text = ""

        if file.content_type == "application/pdf":
                extracted_text = extract_text_from_pdf(file_location)
        elif file.content_type == "text/plain":
                with open( file_location , "r" , encoding="utf-8") as txt_file:
                        extracted_text = txt_file.read()
        
        if not extracted_text:
                extracted_text = "No Readable Found"

        embedding = []
        if extracted_text :
                embedding = generate_embedding(extracted_text[:1000])

        chunks = []
        if extracted_text:
                chunks = chunk_text(extracted_text)
                
        new_document = Document(
                filename = file.filename,
                filepath = file_location,
                filetype = file.content_type,
                content = extracted_text,
                embedding=embedding,
                chunks = chunks,
                owner_id = current_user.id
        ) 

        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        if extracted_text:
                process_document_tasks.delay(new_document.id,extracted_text)

        print("Chunks Genereated:", len(chunks))

        if chunks:
                add_document_chunks(new_document.id,chunks)
                
        
        #index_document(new_document)
        return new_document

        
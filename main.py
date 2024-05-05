from fastapi import FastAPI, HTTPException
from app.models import Book
from app.validation import BookCreate, BookUpdate
from database import session

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/api/v1/book")
async def create_book(book: BookCreate):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return {"status": True, "message": "Book Created successfully", "data": db_book.__dict__}


@app.get("/api/v1/book")
async def get_all_books():
    db_book = session.query(Book)
    data = db_book.all()
    return {"status": True, "message": "Book Created successfully", "data": data}


@app.get("/api/v1/book/{id}")
async def get_single_book(book_id: int):
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": True, "message": "Book found", "data": db_book}


@app.put("/api/v1/book/{id}")
async def update_single_book(book_id: int, book: BookUpdate):
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    session.commit()
    session.refresh(db_book)
    return {"status": True, "message": "Book Updated successfully", "data": db_book.__dict__}


@app.delete("/api/v1/book/{id}")
async def delete_single_book(book_id: int):
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"stauts": True, "message": "Book deleted successfully"}

from sqlalchemy.orm import Session
from .models import Term
from .schemas import TermCreate

def get_all_terms(db: Session):
    return db.query(Term).all()

def get_term_by_name(db: Session, name: str):
    return db.query(Term).filter(Term.name == name).first()

def create_term(db: Session, term: TermCreate):
    db_term = Term(name=term.name, description=term.description)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def update_term(db: Session, current_name: str, term: TermCreate):
    db_term = db.query(Term).filter(Term.name == current_name).first()
    if db_term:
        db_term.name = term.name
        db_term.description = term.description
        db.commit()
        db.refresh(db_term)
    return db_term

def delete_term(db: Session, name: str):
    db_term = db.query(Term).filter(Term.name == name).first()
    if db_term:
        db.delete(db_term)
        db.commit()
    return db_term

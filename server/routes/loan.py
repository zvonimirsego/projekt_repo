from fastapi import APIRouter, HTTPException
from database.py_classes import Loan

router = APIRouter(prefix="/loan", tags=["Loan"])


# GET ruta, dohvaćanje svih posudbi
@router.get("/all_loans")
def all_loans():
    loans = Loan.fetch_all()
    return loans


# GET ruta, dohvaćanje posudbe po korisniku
@router.get("/user/{email}")
def get_loans_by_user(email: str):
    loans = Loan.fetch_by_user(email)
    if not loans:
        raise HTTPException(status_code=404, detail="Nema posudbi za ovog korisnika")
    return loans


# GET ruta, pretraživanje prema id-u posudbe
@router.get("/{id_loan}")
def get_loan(id_loan: int):
    loan = Loan.fetch(id_loan)
    if not loan:
        raise HTTPException(status_code=404, detail="Zapis posudbe ne postoji")
    return loan

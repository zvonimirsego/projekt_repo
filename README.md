# Projekt_repo

Repozitorij za projekt iz softverskog inženjerstva.


## Tema

Tema ovog projekta je razvoj web aplikacije za posudbu opreme. Aplikacija omogućuje upravljanje sustavom za posudbu opreme, uključujući korisnike, opremu, posudbe i administratorske funkcionalnosti.

---

## 🚀 Ključne Funkcionalnosti
* **Upravljanje Korisnicima**: dodavanje, dohvat, uređivanje i brisanje korisnika.
* **Upravljanje Opremom**: pregled sve opreme, pregled dostupne opreme i dohvat opreme prema ID-u.
* **Administracija Opreme**: dodavanje, uređivanje i brisanje opreme.
* **Upravljanje Posudbama**: izrada posudbe, pregled svih posudbi, pregled posudbi korisnika i brisanje rezervacije.

---
## 🛠️ Tehnologije
* Python 3.12
* FastAPI
* Uvicorn
* SQLModel / SQLAlchemy
* Pytest
* Docker
* Docker Compose


---

## 💻 Pokretanje Projekta Lokalno

Da biste projekt pokrenuli lokalno slijedite sljedeće korake:
Otvorite novi terminal i pokrenite:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt
uvicorn server.main:app --host 0.0.0.0 --port 8000
```
### Nakon toga, aplikacija će biti dostupna na adresi: http://localhost:8000/docs#/
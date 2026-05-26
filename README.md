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

---

## 🐳 Pokretanje s Dockerom

Preporučeni način pokretanja — ne zahtijeva instalaciju Pythona ili ovisnosti na vašem računalu.

### Preduvjeti
* Docker Desktop (Windows/Mac) ili Docker Engine + Compose plugin (Linux)
* Git (za kloniranje repozitorija)

### Brzi start
Iz root direktorija projekta:
```bash
docker compose up
```

Aplikacija će biti dostupna na: http://localhost:8000/docs#/

Za zaustavljanje pritisnite `Ctrl+C`. Za potpuno čišćenje kontejnera:
```bash
docker compose down
```

### Ponovna izgradnja nakon promjena u kodu
```bash
docker compose up --build
```

### Mogući problemi
* **`port is already allocated`** — neki drugi proces koristi port 8000. Promijenite port u `docker-compose.yml` iz `"8000:8000"` u npr. `"9000:8000"` i koristite http://localhost:9000.
* **`Cannot connect to the Docker daemon`** — Docker Desktop nije pokrenut. Pokrenite ga iz Start izbornika i pričekajte da se ikona kita ustabili.

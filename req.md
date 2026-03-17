# Projekt: Posudba opreme
## Članovi tima
- Marin Pontoni
- Tibor Milković
- Zvonimir Šego
- Marko Kovačić
- Krunoslav Lešić
## GitHub repozitorij
- Link: https://github.com/zvonimirsego/projekt_repo
- Svi članovi dodani: DA
## User storyji
US-01 Kao korisnik sustava, želim imati mogućnost registracije i prijave u sustav kako bih mu mogao pristupiti

## Funkcijski zahtjevi
FZ-01 Sustav mora imati mjesto za unos potrebnih podataka za registraciju novih korisnika. <br>
FZ-02 Sustav mora imati mjesto za unos potrebnih podataka za prijavu već postojećeg korisnika. <b4>
FZ-03 Sustav mora sprijeciti ponovnu registraciju vec postojeceg korisnika. <br>
FZ-04 Sustav mora omoguciti korisniku povijest svih svojih dosadasnjih posudbi opreme.

## Nefunkcijski zahtjevi
NZ-01 Sustav mora obraditi prijavu korisnika u vremenskom roku od 2 sekunde. <br>
NZ-02  Sustav mora bilježiti greške pri neuspjeloj rezervaciji.

## Taskovi
TASK-01 Napraviti model baze podataka za pohranu registriranih korisnika <br>
TASK-02 Napraviti obrazac za unos podataka potrebnih za registraciju <br>
TASK-03 Povezati bazu podataka sa sučeljem <br>
TASK-04 Napraviti obrazac za prijavu već postojećeg korisnika <br>
TASK-05 Napisati testni pokušaj prijave korisnika <br>
TASK-06 Implementirati provjeru postojanja korisnika u bazi podataka prema e-mail adresi. <br>
TASK-07 Dizajnirati i programirati prikaz poruke o pogresci na sucelju za registraciju. <br>
TASK-08 Napisati unit test koji provjerava odbija li sustav unos vec postojeceg e-maila. <br>
TASK-09 Konfigurirati servis za zapisivanje (logging) gresaka u bazu ili datoteku. <br>

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
US-01 Kao korisnik sustava, želim imati mogućnost registracije i prijave u sustav kako bih mu mogao pristupiti. <br>
US-02 Kao administrator, želim moći vidjeti popis sve dostupne opreme, sve posuđene opreme kao i tko je tu opremu posudio, te vrijeme posudbe kako bih mogao efikasnije upravljati svojim sustavom za posudbu opreme.

## Funkcijski zahtjevi
FZ-01 Sustav mora imati mjesto za unos potrebnih podataka za registraciju novih korisnika. <br>
FZ-02 Sustav mora imati mjesto za unos potrebnih podataka za prijavu već postojećeg korisnika. <br>
FZ-03 Sustav mora sprijeciti ponovnu registraciju vec postojeceg korisnika. <br>
FZ-04 Sustav mora omoguciti korisniku povijest svih svojih dosadasnjih posudbi opreme. <br>
FZ-05 Sustav mora prikazati popis slobodne opreme za posudbu. <br>
FZ-06 Sustav mora prikazati popis posuđene opreme te kraj roka posudbe. <br>
FZ-07 Administrator mora moći na popis dodati novokupljenu opremu.<br>
FZ-08 Administrator mora moći obrisati pokvarenuu opremu s popisa. <br>
FZ-09 Sustav mora omogućiti produženje rezervacije posuđene opreme. <br>
FZ-10 Sustav mora spriječiti posudbu već posuđene opreme.           <br>

## Nefunkcijski zahtjevi
NZ-01 Sustav mora obraditi prijavu korisnika u vremenskom roku od 2 sekunde. <br>
NZ-02 Sustav mora bilježiti greške pri neuspjeloj rezervaciji. <br>
NZ-03 Sustav mora moći prebaciti novoposuđenu opremu s popisa slobodne na popis posuđene opreme u manje od 3 sekunde za 90% zahtjeva. <br>
NZ-04 Korsnik može otkazati posudbu maksimalno 12 h prije posudbe. <br> 
NZ-05 Sustav mora biti dizajniran tako bi se nova oprema ili funkcionalnosti mogle dodati bez promjene postojećeg koda.

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
TASK-10 Napraviti bazu podataka koja prikazuje popis sve opreme. <br>
TASK-11 Napraviti prikaze posuđene i dostupne opreme. <br>
TASK-12 Napraviti obrasce za dodavanje opreme i mogućnost brisanja opreme. <br>
TASK-13 Održavanje baze podataka. <br>
TASK-14 Mogućnost produljenja roka posudbe. <br>

## Raspodjela taskova
- Marin Pontoni : FZ-01, FZ-02, NZ-01, TASK-01 - TASK-05
- Tibor Milković : FZ-03, FZ-04, NZ-02, TASK-06 - TASK-09
- Zvonimir Šego : FZ-05, FZ-06, NZ-03, TASK-10, TASK-11
- Marko Kovačić : FZ-07, FZ-08, NZ-04, TASK-12
- Krunoslav Lešić: FZ-09, FZ-10, NZ-05, TASK-13, TASK-14
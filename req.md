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
US-02 Kao korisnik sustava, želim imati mogućnost pravljenja posudbe dostupne opreme za posudbu te moguće otkazivanje ukoliko mi više nije potrebno. Također, želio bih moći vidjeti svoju vlastitu povijest posudbi. <br>
US-03 Kao administrator, želim moći vidjeti popis sve posuđene opreme, sve dostupne opreme i svih posudbi kako bih mogao upravljati svojim sustavom za posudbu opreme. Dodatno, želim imati mogućnost uređenja inventara i posudbi kako bih mogao što ažurnije imati popis dostupne opreme. Po mogućnosti bih želio da sustav javi meni (a ako je moguće i korisniku) ukoliko dođe do prekoračenja roka posudbe.

## Funkcijski zahtjevi
FZ-01 Sustav mora imati mjesto za unos potrebnih podataka za registraciju novih korisnika. <br>
FZ-02 Sustav mora imati mjesto za unos potrebnih podataka za prijavu već postojećeg korisnika. <br>
FZ-03 Sustav mora prikazati popis slobodne opreme za posudbu. <br>
FZ-04 Sustav mora prikazati popis posuđene opreme te kraj roka posudbe (administratoru za sve, korisniku samo za njegovu posuđenu opremu). <br>
FZ-05 Sustav mora omogućiti korisniku mogućnost posudbe opreme. <br>
FZ-06 Sustav mora omoguciti korisniku povijest svih svojih dosadasnjih posudbi opreme. <br>
FZ-07 Sustav mora omogućiti administratoru da na popis doda novonabavljenu opremu. <br>
FZ-08 Sustav mora omogućiti administratoru brisanje pokvarene opreme s popisa sve opreme. <br>
FZ-09 Sustav mora omogućiti korisniku produženje rezervacije posuđene opreme. <br>
FZ-10 Sustav mora spriječiti posudbu već posuđene opreme. <br>
FZ-11 Sustav mora obavijestiti administratora (po mogućnosti i korisnika) ukoliko kasni s vraćanjem opreme. <br>
FZ-12 Sustav mora omogućiti administratoru uređenje posudbe (ovo uključuje i bilježenje vraćanja posuđene opreme).

## Nefunkcijski zahtjevi
NZ-01 Sustav mora obraditi prijavu korisnika u vremenskom roku od 2 sekunde. <br>
NZ-02 Sustav mora bilježiti greške pri neuspjeloj rezervaciji. <br>
NZ-03 Sustav mora moći prebaciti novoposuđenu opremu s popisa slobodne na popis posuđene opreme u manje od 3 sekunde za 90% zahtjeva. <br>
NZ-04 Korsnik može otkazati posudbu maksimalno 4 h prije posudbe. <br> 
NZ-05 Sustav mora biti dizajniran tako bi se nova oprema ili funkcionalnosti mogle dodati bez promjene postojećeg koda. <br>
NZ-06 Sustav mora administratoru (po mogućnosti i korisniku) javiti pri prvoj idućoj prijavi u sustav o prekoračenju roka (podrazumjeva podatke o posuđenoj opremi i korisniku). <br> 
NZ-07 Sustav mora biti microserviced i containerized; u Dockeru. <br>

## Taskovi
TASK-01 Napraviti obrazac za registraciju korisnika. <br>
TASK-02 Napraviti obrazac za prijavu korisnika. <br>
TASK-03 U bazu podataka dodati novog korisnika (registracija) te provjeriti postojećeg (prijava). <br>
TASK-04 [ADMIN] Napraviti obrazac za dodavanje nove opreme. <br>
TASK-05 [ADMIN] Omogućiti administratoru brisanje opreme iz inventara. <br>
TASK-06 U bazu podataka dodati novu opremu i po potrebi obrisati. <br>
TASK-07 Na glavnoj stranici postaviti popis sve dostupne opreme (fetchanje iz baze podataka). <br>
TASK-08 Napraviti stranicu za pregled dosadašnjih posudbi jednog korisnika (fetchanje iz baze podataka po id). <br>
TASK-09 [ADMIN] Napraviti stranicu za pregled svih posudbi (mogućnost povezivanja s TASK-07). <br>
TASK-10 Napraviti obrazac korisniku za posudbu opreme. Uključuje i unos trajanja posudbe. <br>
TASK-11 Omogućiti korisniku produljavanje roka posudbe. <br>
TASK-12 [ADMIN] Omogućiti uređenje posudbe. Uključuje i zapis o vraćanju opreme. <br>
TASK-13 Slanje notifikacije (i korisniku koji je posudio kao i adminu) pri idućoj prijavi ukoliko je prekoračen rok posudbe. <br>
TASK-14 [ADMIN] Omogućiti administratoru slanje e-maila u slučaju prekoračenja roka posudbe.

## Raspodjela taskova (TREBA PROMIJENITI NA IDUĆEM SASTANKU)
- Marin Pontoni : FZ-01, FZ-02, NZ-01, TASK-01 - TASK-05
- Tibor Milković : FZ-03, FZ-04, NZ-02, TASK-06 - TASK-09
- Zvonimir Šego : FZ-05, FZ-06, NZ-03, TASK-10, TASK-11
- Marko Kovačić : FZ-07, FZ-08, NZ-04, NZ-06, TASK-12
- Krunoslav Lešić: FZ-09, FZ-10, NZ-05, TASK-13, TASK-14
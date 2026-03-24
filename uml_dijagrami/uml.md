# UML dijagrami
## Use case dijagram
Dijagram prikazuje sustav za posudbu opreme s jednim glavnim akterom, korisnikom. <br>
Korisnik može obaviti prijavu/registraciju, pregledati dostupnu opremu, pregledati povijest posudbi i pokrenuti posudbu. <br>
Use case Povijest posudbi ima relaciju `<<include>>` prema Trenutne posudbe, što znači da taj prikaz obavezno uključuje i aktivne posudbe. <br>
Use case Notifikacija za kašnjenje je povezan relacijom `<<extend>>` s Posudba, pa se izvršava samo u posebnoj situaciji kašnjenja. <br>
Time dijagram jasno odvaja osnovne korisničke funkcionalnosti od dodatnih, uvjetnih ponašanja sustava. <br>
## Sequence dijagram
- akter Korisnik predstavlja vanjskog učesnika koji pokreće proces rezervacije. <br>
- participant UI, API servis i database (Baza) predstavljaju unutrašnje dijelove sistema koji međusobno komuniciraju. <br>
- poruka Korisnik → UI : make_reservation() pokreće scenarij rezervacije. <br>
- activate/deactivate označavaju period kada su UI i API servis aktivni tokom obrade zahtjeva. <br>
- UI šalje zahtjev API servisu putem check_data(), a API zatim dohvaća podatke iz baze preko findEquipment(). <br>
- Baza → API : equipmentData je povratna poruka koja sadrži tražene podatke o opremi. <br>
- alt / else / end prikazuje dvije moguće grane: <br>
- uspješna rezervacija (reservationSuccess) <br>
- neuspješna rezervacija (reservationError) <br>
- UI → Korisnik : odgovor vraća konačan rezultat korisniku. <br>
## Class dijagram
Class dijagram modelira tri glavne klase sustava: Korisnik, Admin i Oprema. <br>
Klasa Korisnik sadrži osnovne korisničke podatke (username, email, password) te operacije za kreiranje i otkazivanje rezervacije. <br>
Klasa Oprema opisuje entitet opreme kroz atribute (id, name, condition, availability) i metodu checkAvailability() za provjeru dostupnosti. <br>
Između Korisnik i Oprema je veza kardinalnosti 0..* prema 0..*, što znači da jedan korisnik može imati više rezervacija opreme, a jedna oprema može biti povezana s više korisnika kroz vrijeme. <br>
Admin nasljeđuje Korisnik i proširuje ga administratorskim CRUD funkcijama za upravljanje opremom i slanje upozorenja. <br>
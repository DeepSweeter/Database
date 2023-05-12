insert into categorie(denumire_cat, descriere) values('metal','Sectiunea utilaje prelucrare metal contine strunguri mari si mici pentru metal, masini de gaurit, masini de rectificat, fierastraie metal.');
insert into categorie(denumire_cat, descriere) values('lemn','Masinile unelte disponibile, pot fi folosite in scopuri diferite, utilizarea depinzand de cantitatea de putere necesara pentru fiecare operatiune.');
insert into categorie(denumire_cat, descriere) values('accesorii','Cautati accesoriile necesare pentru utilajele din atelierul dumneavoastra care sa va aduca la viata viziunea creativa de prelucrare a lemnului sau a metalelor?');
insert into categorie(denumire_cat, descriere) values('generatoare curent','Sa fie casa ta singura din cartier cu luminile inca aprinse atunci cand se intrerupe curentul.');

insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (1,'strunguri metal','Strungul universal este o masina-unealta de uz general care permite strunjirea pieselor cilindrice si/sau prismatice.');
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (1,'masini de gaurit','Aceasta categorie este formata din masini de gaurit si produse conexe.');
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (2,'exhaustore rumegus','Iti doresti un mediu de lucru curat? Alege unul din sistemele de exhaustare din gama noastra!');
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (2,'fierastraie circulare','Ai nevoie de un fierastrau circular ce poate acoperi toate cerintele?');
insert into subcategorie(id_cat, denumire_sub) values (3,'metal');
insert into subcategorie(id_cat, denumire_sub) values (3,'lemn');
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (4,'generatoare','Pregatestete pentru o pana de curent prelungita si protejeaza tot ceea ce conteaza pentru tine si familia ta.');

insert into producator(denumire_producator, tara_producator, descriere) values('Optimum','Germania','OPTIMUM pentru calitate, rentabilitate si servicii.');
insert into producator(denumire_producator,tara_producator, descriere) values('Holzstar','Germania','Do It Yourself la cel mai ridicat standard.');
insert into producator(denumire_producator,tara_producator, descriere) values('Morse','SUA','Morse are un singur obiectiv de peste 50 de ani, sa produca cele mai bune panze pentru fierastraie si accesorii.');
insert into producator(denumire_producator,tara_producator, descriere) values('Metallkraft','Germania','METALLKRAFT pentru utilizare versatila.');
insert into producator(denumire_producator,tara_producator) values('Fixtec','China');
insert into producator(denumire_producator,tara_producator) values('Unicraft','Germania');


insert into detalii(descriere, poza) values('Utilizat preponderent in ateliere de reparatii auto sau ceasornicarii datorita preciziei.', 'www.poza1.com' );
insert into detalii(descriere, poza) values('Asigura gauri precise si continue cu un diametru de pana la 127 mm.', 'www.poza2.com' );
insert into detalii(descriere, poza) values('Acest exhaustor creste eficietna masinilor de tamplarie.', 'www.poza3.com' );
insert into detalii(descriere, poza) values('Masa de lucru generoasa din aluminiu.', 'www.poza4.com' );
insert into detalii(descriere, poza) values(' Turatie Maxima 5000 rpm.', 'www.poza5.com' );
insert into detalii(descriere, poza) values('Sac colector pentru exhaustor rumegus de calitate din PVC', 'www.poza6.com' );
insert into detalii(descriere, poza) values('Tehnologie inverter pentru o performanta constanta.', 'www.poza7.com' );


insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 1, 'Strung Metal OPTIturn 1503V' ,6239 ,1 ,1,79 );
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 2, 'Masina de gaurit tevi RB 127', 5851,4 , 2, 24);
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 3, 'Exhaustor rumegus SAA 902', 1207.02 , 2, 3, 15);
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 4, 'Fierastrau circular FTS18001',1146.6 , 5, 4, 40);
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 5, 'Varf de centrare rotativ MK 1', 216.34, 1, 5,24);
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 6, 'Sac colector exhaustor SAA 902', 9.27 , 2, 6, 456);
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 7, 'Generator PG I 12 SR', 2443.19, 6, 7, 14);


insert into proprietati(denumire_prop) values('debit aer'); --1
insert into proprietati(denumire_prop) values('tensiune alimentare'); --2
insert into proprietati(denumire_prop) values('presiune negativa maxima'); --3
insert into proprietati(denumire_prop) values('cursa pinola');--4
insert into proprietati(denumire_prop) values('turatii'); --5
insert into proprietati(denumire_prop) values ('greutate');  --6 
insert into proprietati(denumire_prop) values ('putere motor s1');  --7 
insert into proprietati(denumire_prop) values ('latime sac');  --8 
insert into proprietati(denumire_prop) values ('nivel zgomot');  --9 



insert into val_prop(valoare) values('1200 m3 per h'); --1
insert into val_prop(valoare) values('1100 Pa'); --2
insert into val_prop(valoare) values('230 V'); --3
insert into val_prop(valoare) values('2500 rpm'); --4
insert into val_prop(valoare) values('30 mm'); --5
insert into val_prop(valoare) values('23 Kg'); --6
insert into val_prop(valoare) values('14.5 Kg'); --7
insert into val_prop(valoare) values('1.1 KW'); --8
insert into val_prop(valoare) values('19 Kg'); --9
insert into val_prop(valoare) values('5000 rpm'); --10
insert into val_prop(valoare) values('1.8 KW'); --11
insert into val_prop(valoare) values('84 l'); --12
insert into val_prop(valoare) values('93 dB'); --13
insert into val_prop(valoare) values('12.1 Kg'); --14





insert into prod_prop(id_prod, id_prop, id_val_prop) values(1,2,3);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(1,4,5);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(1,5,4);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(1,6,6);

insert into prod_prop(id_prod, id_prop, id_val_prop) values(2,7,8);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(2,6,7);

insert into prod_prop(id_prod, id_prop, id_val_prop) values(3,6,9);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(3,1,1);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(3,3,2);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(3,2,3);

insert into prod_prop(id_prod, id_prop, id_val_prop) values(4,5,10);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(4,7,11);

insert into prod_prop(id_prod, id_prop, id_val_prop) values(6,8,12);

insert into prod_prop(id_prod, id_prop, id_val_prop) values(7,6,14);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(7,2,3);
insert into prod_prop(id_prod, id_prop, id_val_prop) values(7,9,13);



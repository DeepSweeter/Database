--Verificare Tabela categorie 

insert into categorie(denumire_cat, descriere) values('generatoare curent',
        'Sa fie casa ta singura din cartier cu luminile inca aprinse atunci cand se intrerupe curentul.');  -- Eroare element duplicat
insert into categorie(denumire_cat, descriere) values('generatoare curent12',
        'Sa fie casa ta singura din cartier cu luminile inca aprinse atunci cand se intrerupe curentul.'); -- Eroare nu respecta regular expression 
insert into categorie(denumire_cat, descriere) values('',
        'Sa fie casa ta singura din cartier cu luminile inca aprinse atunci cand se intrerupe curentul.'); -- eroare element null

--Verificare tabela subcategorie
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (1,'strunguri metal',
    'Strungul universal este o masina-unealta de uz general care permite strunjirea pieselor cilindrice si/sau prismatice.'); -- Eroare element duplicat
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (1,'strunguri metal12',
    'Strungul universal este o masina-unealta de uz general care permite strunjirea pieselor cilindrice si/sau prismatice.');-- Eroare nu respecta regular expression 
insert into subcategorie(id_cat, denumire_sub, subcategorie.descriere) values (1,'',
    'Strungul universal este o masina-unealta de uz general care permite strunjirea pieselor cilindrice si/sau prismatice.');-- eroare element null
    

--Verificare tabela producator 

insert into producator(denumire_producator, tara_producator, descriere) values('Optimum','Germania',
    'OPTIMUM pentru calitate, rentabilitate si servicii.'); -- Eroare element duplicat
insert into producator(denumire_producator, tara_producator, descriere) values('Optimus Prime1','Germania1',
    'OPTIMUM pentru calitate, rentabilitate si servicii.'); -- Eroare nu respecta regular expressionn
insert into producator(denumire_producator, tara_producator, descriere) values('','Germania',
    'OPTIMUM pentru calitate, rentabilitate si servicii.'); -- Eroare element null
    
--Verificare tabela detalii
insert into detalii(descriere, poza) values('Tehnologie inverter pentru o performanta constanta.', 'www.po##%^za7.co7m' ); -- eroare adresa invalida

--Verificare tabela produse
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 1,
    '1503V' ,6239 ,9 ,9, 12 ); -- inserare la producator, detaliu  invalid
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 1, 
    'Strung Metal OPTIturn 1503V' ,6239 ,1 ,1, 12 ); -- eroare duplicat
insert into produse(id_sub, denumire_prod, pret, id_producator, id_desc, stoc) values( 1,
    '' ,6239 ,1 ,1, 12 ); -- eroare null

--Verificare tabela val_prop
insert into val_prop(valoare) values('230### V'); --eroare nu respecta regular expression 
insert into val_prop(valoare) values('230 V'); --eroare nu respecta unique key


-- Verificare tabela prod_prop
insert into proprietati(denumire_prop) values ('greutate');  --duplicat
insert into proprietati(denumire_prop) values ('greutate## 123');  --nu respecta regular expression 


--Selectii, modificari, stergeri:
select p.denumire_prod , p.pret, pr.denumire_producator, pr.tara_producator, d.descriere, d.poza
from produse p, producator pr, detalii d
where p.id_producator = pr.id_producator and p.id_desc = d.id_desc and pr.denumire_producator = 'Optimum' order by p.pret;


select c.denumire_cat, s.denumire_sub, pd.denumire_producator,  p.denumire_prod,
p.pret, pd.tara_producator, pr.denumire_prop, val.valoare, d.descriere
from produse p, val_prop val, prod_prop pp, proprietati pr, categorie c, subcategorie s, producator pd, detalii d
where p.id_prod = pp.id_prod
and pp.id_prop = pr.id_prop
and val.id_val_prop = pp.id_val_prop
and s.id_cat = c.id_cat
and p.id_sub = s.id_sub
and p.id_producator = pd.id_producator
and d.id_desc = p.id_desc
and pd.tara_producator = 'Germania';


update produse
    set stoc = 5
    where denumire_prod like 'Generator%';
    
delete from produse
    where id_sub = 1;
	
drop sequence  detalii_id_desc_seq;
drop sequence  detalii_produse_id_desc_seq;
drop sequence prod_prop_id_prod_prop_seq;
drop sequence producator_id_producator_seq;
drop sequence produse_id_prod_seq;
drop sequence promotii_id_prom_seq;
drop sequence proprietati_id_prop_seq;
drop sequence subcategorie_id_sub_seq;
drop sequence val_prop_id_val_prop_seq;

drop table categorie cascade constraints;
drop table subcategorie cascade constraints;
drop table produse cascade constraints;
drop table detalii_produse cascade constraints;
drop table producator cascade constraints;
drop table prod_prop cascade constraints;
drop table val_prop cascade constraints;
drop table proprietati cascade constraints;




        

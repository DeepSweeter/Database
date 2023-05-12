import os
import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import cx_Oracle
currentfolder = os.getcwd()
cx_Oracle.init_oracle_client(lib_dir=currentfolder + '\instantclient_21_7')

class valuesPanel:
    def __init__(self, val, cursor) -> None:
        self.root = tk.Toplevel()
        self.root.geometry("360x600")
        self.root.title("Valori")
        
        #*Variables
        self.c = cursor
        self.prop = val
        #*Table
        self.table = self.create_table()
        
        #*Buttons
        
        self.button_close = tk.Button(self.root, text='Inchide', command=self.close_all)
        self.button_close.place(x=10, y=510, width=100)
        
        self.button_add = tk.Button(self.root, text = 'Adauga', command=self.add)
        self.button_add.place(x=10, y= 550, width=100)
        
        self.button_delete = tk.Button(self.root, text="Sterge", command=self.delete)
        self.button_delete.place(x=125, y= 510, width=100)
        
        #*Entry
        self.entry_add = tk.Entry(self.root)
        self.entry_add.place(x= 115, y= 550, width=200, height= 30)
        
        #*Functions
        self.complete_table()
        
        #*mainLoop
        self.root.mainloop()

    def create_table(self):
        columns = ('values')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.heading('values', text='Valori')
        tree.column('values', anchor='center')

        
        tree.grid(row=0, column=0, sticky='news')
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky='ns')
        
        tree.place(x=10, y=5, width=330, height=495)
        scrollbar.place(x=340,y=5,height=495)
        return tree
    
    
    def close_all(self):
        self.root.destroy()
        
    def add(self):
        #!Problema: cand adaug o valoare nu pot sa o leg de o proprietate fara sa o leg obligatoriu si de un produs
        #?Solutii:
            #? 1. Fie creez un produs dummy care sa tina toate proprietatile si valorile noi inserate
            #? 2. Fie modific structura tabelelor. 
        #* Pentru ca nu ma pot conecta la baza de date din sql developer o sa merg pe varianta 1.
        querry1 = 'insert into val_prop(valoare) values (:bind)'
        querry2 = 'insert into prod_prop(id_prop, id_val_prop, id_prod) values (:bind1, :bind2, :bind3)'
        querry3 = 'select id_prop from proprietati where denumire_prop= :bind'
        querry4 = 'select id_val_prop from val_prop where valoare= :bind'
        try:
            self.c.execute(querry1, bind= self.entry_add.get())
            self.table.insert(parent='', index='end', text='', values=((self.entry_add.get(),)))
        except Exception as e:
            messagebox.showerror(title='Eroare', message=e)
        
        
        self.c.execute(querry3, bind=self.prop)
        rows = self.c.fetchall()
        id_prop=None
        for row in rows:
            id_prop = row[0]
        
        self.c.execute(querry4, bind=self.entry_add.get())
        rows = self.c.fetchall()
        id_val_prop=None
        for row in rows:
            id_val_prop = row[0]

        querry5 ='select id_prod from produse where denumire_prod = \'Dummy\''
        self.c.execute(querry5)
        rows=self.c.fetchall()
        id_prod=None
        for row in rows:
            id_prod = row[0]
        try:
            self.c.execute(querry2, bind1=id_prop, bind2= id_val_prop, bind3=id_prod)
        except Exception as e:
            print(e)

    def delete(self):
        #TODO stergere valoare selectata
        selection = self.table.focus()
        v1= self.table.item(selection)
        val = v1['values']
        if val == '':
            messagebox.showerror(title='Eroare', message='Nicio proprietate selectat')
        else:
            m= messagebox.askyesnocancel(title='Warning', message='Esti sigur ca vrei sa stergi valoarea??')
            if m == True:
                querry = 'delete from val_prop where valoare = :bind'
                querry1 = 'delete from prod_prop where id_val_prop = :bind'
                querry2 = 'select id_val_prop from val_prop where valoare = :bind'
                
                self.c.execute(querry2, bind= val[0])
                rows = self.c.fetchall()
                id_prop=None
                for row in rows:
                    id_prop = row[0]
                self.c.execute(querry1, bind = id_prop)
                self.c.execute(querry, bind= val[0])
                self.table.delete(selection)
    
    def complete_table(self):
        querry ='select distinct v.valoare\
                    from val_prop v,proprietati p, prod_prop pp\
                    where p.id_prop = pp.id_prop\
                    and pp.id_val_prop = v.id_val_prop\
                    and p.denumire_prop = :bind'
        self.c.execute(querry, bind= self.prop)
        rows = self.c.fetchall()
        for row in rows:
            self.table.insert(parent='', index='end', text='', values=(row[0],))

class propertiesPanel:
    def __init__(self, cursor) -> None:
        self.root = tk.Toplevel()
        self.root.geometry('360x600')
        self.root.title("Proprietati")
        self.valori = None
        self.c = cursor
        
        #*Table
        self.tree = self.create_table()
        
        #*Button
        self.button_close = tk.Button(self.root, text='Inchide', command=self.close_all)
        self.button_close.place(x=10, y=510, width=100)
        
        self.button_select = tk.Button(self.root, text= 'Vizualizeaza', command=self.valori_prop)
        self.button_select.place(x=125, y= 510, width=100)
        
        self.button_add = tk.Button(self.root, text = 'Adauga', command=self.add)
        self.button_add.place(x=10, y= 550, width=100)
        
        self.button_delete = tk.Button(self.root, text="Sterge", command=self.delete)
        self.button_delete.place(x=235, y= 510, width=100)
        
        #*Entry
        self.entry_add = tk.Entry(self.root)
        self.entry_add.place(x= 115, y= 550, width=200, height= 30)
        
        self.complete_table()
        
        #*mainLoop
        self.root.mainloop()
        
    def create_table(self):
        columns = ('proprietati')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.heading('proprietati', text='Proprietati')
        tree.column('proprietati', anchor='center')
        
        tree.grid(row=0, column=0, sticky='news')
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky='ns')
        
        tree.place(x=10, y=5, width=330, height=495)
        scrollbar.place(x=340,y=5,height=495)
        return tree
        
    def close_all(self):
        if self.valori != None:
            self.valori.root.destroy()
        self.root.destroy()
       
    def valori_prop(self):
        #TODO se ia o valoare din tabela si se afiseaza toate valorile respective proprietati-done
        val = self.tree.focus()
        v1 = self.tree.item(val)
        v2 = ' '.join(v1['values'])
        self.valori = valuesPanel(v2, self.c) 

    def add(self):
        #TODO se preia text din self.entry_add si se adauga in tabela-done
        querry = 'insert into proprietati(denumire_prop) values (:bind)'
        try:
            self.c.execute(querry, bind=self.entry_add.get())
            self.tree.insert(parent='', index='end', text='', values=((self.entry_add.get(),)))
        except Exception as e:
            messagebox.showerror(title='Eroare', message=e)

    def delete(self):
        #TODO se sterge prorpietatea selectata curent
        selection = self.tree.focus()
        v1= self.tree.item(selection)
        val = v1['values']
        if val == '':
            messagebox.showerror(title='Eroare', message='Nicio proprietate selectat')
        else:
            m= messagebox.askyesnocancel(title='Warning', message='Esti sigur ca vrei sa stergi proprietatea?')
            if m == True:
                querry = 'delete from proprietati where denumire_prop = :bind'
                querry1 = 'delete from prod_prop where id_prop = :bind'
                querry2 = 'select id_prop from proprietati where denumire_prop = :bind'
                self.c.execute(querry2, bind= val[0])
                rows = self.c.fetchall()
                id_prop=None
                for row in rows:
                    id_prop = row[0]
                self.c.execute(querry1, bind = id_prop)
                self.c.execute(querry, bind= val[0])
                self.tree.delete(selection)
                

    
    def complete_table(self):
        self.c.execute('select denumire_prop from proprietati')
        rows = self.c.fetchall()
        for row in rows:
            self.tree.insert(parent='', index='end', text='', values=(row[0]))
        

class productPanel:
    def __init__(self, cursor, connection, val=None):
        self.root = tk.Toplevel()
        self.root.geometry('1400x800')
        self.root.title('Vizualizare Produs')
        
        #* Variables
        self.menuvar_prod = StringVar()
        self.menuvar_subcat = StringVar()
        self.menuvar_cat = StringVar()
        self.propdict = dict()
        self.c=cursor
        self.con = connection
        self.values = val
        self.i = 0
        self.listprod_old =[]
        self.listdet_old = []
        self.listprod = []
        self.listdet = []

        
        #*Labels
        self.label_denumireProd = tk.Label(self.root, text='Denumire Produs', font=('Arial', 16), justify='right')
        self.label_denumireProd.place(x = 30, y = 30, width= 210, height=30)
        
        self.label_producator = tk.Label(self.root, text='Producator', font=('Arial', 16), justify='right')
        self.label_producator.place(x=30, y = 80, width=210, height=30)
        
        self.label_descriere = tk.Label(self.root, text='Descriere', font=('Arial', 16))
        self.label_descriere.place(x=30, y =130, width=210, height=30)
        
        self.label_pret = tk.Label(self.root, text='Pret', font=('Arial', 16))
        self.label_pret.place(x= 700, y = 30, width=210, height=30)
        
        self.label_stoc = tk.Label(self.root, text='Stoc', font=('Arial', 16))
        self.label_stoc.place(x=700, y = 80, width=210, height=30)
        
        self.label_poza = tk.Label(self.root, text='Poza', font=('Arial', 16))
        self.label_poza.place(x = 700, y = 130, width=210, height=30)
        
        self.label_categorie = tk.Label(self.root, text='Categorie', font=('Arial', 16))
        self.label_categorie.place(x= 700, y= 180, width=210, height=30)
        
        self.label_subcategorie = tk.Label(self.root, text='Subcategorie', font=('Arial', 16))
        self.label_subcategorie.place(x= 700, y= 230, width=210, height=30)
        
        self.label_proprietati = tk.Label(self.root, text='Proprietati', font=('Arial', 16))
        self.label_proprietati.place(x=30, y=450, width=210, height=30)
        
        self.label_valori = tk.Label(self.root, text='Valori', font=('Arial', 14))
        self.label_valori.place(x=750, y= 420, width=100, height=30)
        
        #*Entries
        self.entry_denumireProd = tk.Entry(self.root, font=('Arial',15))
        self.entry_denumireProd.place(x=250, y = 30, width=350, height=30)
        
        self.entry_pret = tk.Entry(self.root, font=('Arial',15))
        self.entry_pret.place(x=920, y=30, width=350, height=30)

        self.entry_stoc = tk.Entry(self.root, font=('Arial',15))
        self.entry_stoc.place(x= 920, y= 80, width= 350, height=30)
        
        self.entry_poza = tk.Entry(self.root, font=('Arial',15))
        self.entry_poza.place(x= 920, y= 130, width= 350, height=30)
        
        
        #*Text
        self.text_descriere = tk.Text(self.root)
        self.text_descriere.place(x=250, y= 130, width=350, height=150)
        
        #*MenuButton
      
        mp = self.getList('producator')
        self.menu_producator = self.makeMenu(mp, self.menuvar_prod, self.root)
        self.menu_producator.place(x= 250, y= 80, width=350, height=30)
        
        
        mc = self.getList('categorie')
        self.menu_categorie = self.makeMenu(mc, self.menuvar_cat, self.root)
        self.menu_categorie.place(x=920, y = 180, width=350, height=30)
         
        ms = self.getList('subcategorie')
        self.menu_subcategorie = self.makeMenu(ms ,self.menuvar_subcat, self.root)
        self.menu_subcategorie.place(x= 920, y= 230, width=350, height=30 )
        
        #*Table
        
        self.table_props = self.create_table(['Proprietati'],550, 450, 300)
        self.table_props.place(x=250, y =450, width=300, height=300)
        
        
        
        
        #*Buttons
        self.button_addProp = tk.Button(self.root, text='Adauga Proprietate', command= self.add_prop)
        self.button_addProp.place(x=30, y=450, width=210, height=30)
       
        self.button_close = tk.Button(self.root, text='Inchide', command=self.close_all)
        self.button_close.place(x=30, y = 750, width=100, height= 30)
        
        self.button_save = tk.Button(self.root, text = 'Salveaza', command=self.save_all)
        self.button_save.place(x = 1000, y = 450, width=200, height=30)
        
        #*Proprietati-Valori
        self.frameProp = tk.Frame(self.root, background='white')
        self.frameProp.place(x=700, y=450, width=250, height=300)
        self.frameProp.columnconfigure(0, weight= 1)
        self.frameProp.columnconfigure(1, weight= 1)
        
        #*Calling functions
        self.complete_table()
        self.edit_tab()
        
        # *mainLoop
        self.root.mainloop()
        
    #!Functions
        
    #*Functie de creat un meniu button primeste ca 
    #* parametru o lista cu valorile ce o sa se afle in meniu
    #* si un flag care este o variabila in care se va stoca valoarea
    def makeMenu(self, val, flag, root):
        menu_button = ttk.Menubutton(root, textvariable=flag)
            
        menu = tk.Menu(menu_button, tearoff=0, bg='white', font=('Arial', 14))
            
        for i in val:
            menu.add_radiobutton(label=i, value=i, variable=flag)
                
        menu_button["menu"] = menu
            
        return menu_button
    
    def create_table(self, columns, x, y, h):
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column , anchor='center')
        
        tree.grid(row=0, column=0, sticky='news')
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky='ns')
        scrollbar.place(x=x, y=y, height=h)
        
        return tree
    
    def add_prop(self):
        focus = self.table_props.focus()
        entry = self.table_props.item(focus)['values']
        val = StringVar()
        
        #!entry[0] e prima valoare din lista
        l = self.getList(entry[0])
        menuBar = self.makeMenu(l, val, self.frameProp)
        self.propdict[entry[0]] = val
        newLabel = tk.Label(self.frameProp, text=entry[0])
        newLabel.grid(column=0, row=self.i, sticky='we')
        menuBar.grid(column=1, row=self.i,sticky='we')
        self.i+=1
        
    def close_all(self):
        a = messagebox.askyesno(title='Salvare', message='Doresti sa salvezi inainte de a iesi?')
        if a != True:
            self.c.execute('ROLLBACK a1')
        else:
            self.con.commit()
        self.root.destroy()
    
    def save_all(self):
        #TODO doua metode de save all: una pentru obiect nou, cealalta pentru obiect modificat
        self.c.execute('SAVEPOINT a1')
        self.listprod=[self.entry_denumireProd.get(), self.entry_pret.get(), self.entry_stoc.get()]
        self.listdet=[self.text_descriere.get('1.0', tk.END), self.entry_poza.get()]
        producator_id = self.getId('producator', self.menuvar_prod.get())
        sub_id = self.getId('subcategorie', self.menuvar_subcat.get())
        props= self.propdict.keys()
        values= self.propdict.values()
        props_id=[]
        values_id=[]
        

        for prop in props:
            props_id.append(self.getId('proprietati', prop))

        for value in values:
            values_id.append(self.getId('valori', value.get()))

        
        if self.values != None:
      
            querry4 = 'update produse set denumire_prod = :bind1, pret= :bind2, stoc= :bind3, id_sub= :bind4 where id_prod =:bind5'
            querry5 = 'update detalii set descriere= :bind1, poza= :bind2 where id_desc= :bind3'
            querry6 = 'select pp.id_prod_prop, pp.id_prop, pp.id_prod\
                 from prod_prop pp , produse p, proprietati pr\
                 where pp.id_prop = pr.id_prop and\
                 p.id_prod = pp.id_prod and\
                 p.denumire_prod = :bind1 and\
                 pr.denumire_prop = :bind2'
            querry7 = 'update prod_prop set id_val_prop = :bind1 where id_prod_prop = :bind2'
            querry8 = 'insert into prod_prop(id_prod, id_prop, id_val_prop) values (:bind1, :bind2, :bind3)'
            produs_id = self.getId('produse', self.listprod_old[0])
            desc_id = self.getId('detalii', self.listdet_old[1])
            self.c.execute(querry5, bind1 = self.listdet[0], bind2 = self.listdet[1], bind3= desc_id)
            self.c.execute(querry4, bind1 = self.listprod[0], bind2= self.listprod[1], bind3=self.listprod[2],bind4=sub_id, bind5= produs_id)
           

            for prop in props:
                print(prop)
                try:                
                    self.c.execute(querry6, bind1= self.listprod[0], bind2 = prop)
                    rows = self.c.fetchall()
                    if len(rows) !=0:
                        for row in rows:
                            print(row)
                            self.c.execute(querry7, bind1 = self.getId('valori', self.propdict[prop].get()), bind2=row[0])
                    else:
                        self.c.execute(querry8, bind1= produs_id, bind2= self.getId("proprietati", prop), bind3=self.getId('valori', self.propdict[prop].get()))  
                except Exception as e:
                    print(e)
      
                    
            

        else:
            querry1 = 'insert into detalii(descriere, poza) values (:bind1, :bind2)'
            querry2= 'insert into produse(denumire_prod, pret, stoc, id_sub, id_producator, id_desc) values\
                (:bind1, :bind2, :bind3, :bind4, :bind5, :bind6)'
            try:
                self.c.execute(querry1, bind1=self.listdet[0], bind2 = self.listdet[1])
            except:
                self.c.execute('ROLLBACK a1')
            desc_id = self.getId('detalii', self.listdet[1])
            try:
                self.c.execute(querry2,
                    bind1= self.listprod[0],
                    bind2= self.listprod[1],
                    bind3= self.listprod[2],
                    bind4= sub_id,
                    bind5= producator_id,
                    bind6 = desc_id)
            except:
                self.c.execute('Rollback a1')

            produs_id = self.getId('produse', self.listprod[0])
            querry3 = 'insert into prod_prop(id_prod, id_prop, id_val_prop) values (:bind1, :bind2, :bind3)'

            for p, v in zip(props_id, values_id):
                self.c.execute(querry3, bind1=produs_id, bind2=p, bind3=v)
        
        self.con.commit()
    
    def getList(self, tabel):
        if tabel == 'producator':
            querry = 'select denumire_producator from producator'
            self.c.execute(querry)
            rows = self.c.fetchall()
            l= []
            for row in rows:
                l.append(row[0],)
            return l
        elif tabel == 'categorie':
            querry = 'select denumire_cat from categorie'
            self.c.execute(querry)
            rows = self.c.fetchall()
            l= []
            for row in rows:
                l.append(row[0],)
            return l
        elif tabel == 'subcategorie':
            querry = 'select denumire_sub from subcategorie'
            self.c.execute(querry)
            rows = self.c.fetchall()
            l= []
            for row in rows:
                l.append(row[0],)
            return l
        else:
            querry ='select distinct v.valoare\
                from val_prop v,proprietati p, prod_prop pp\
                where p.id_prop = pp.id_prop\
                and pp.id_val_prop = v.id_val_prop\
                and p.denumire_prop = :bind'
            self.c.execute(querry, bind=tabel)
            rows = self.c.fetchall()
            l =[]
            for row in rows:
                l.append(row[0],)
            return l
    
    def complete_table(self):
        self.c.execute('select denumire_prop from proprietati')
        rows = self.c.fetchall()
        for row in rows:
            self.table_props.insert(parent='', index='end', text='', values=(row[0],))
    
    def edit_tab(self):
        if self.values != None:
            self.change_text(self.entry_denumireProd, self.values[1])
            self.change_text(self.entry_pret, self.values[4])
            self.change_text(self.entry_stoc, self.values[3])
            self.menuvar_cat.set(self.values[5])
            self.menuvar_subcat.set(self.values[6])
            self.menuvar_prod.set(self.values[2])
            self.listprod_old = [self.entry_denumireProd.get(), self.entry_pret.get(), self.entry_stoc.get()]
            
            
            querry = 'select d.descriere, d.poza from detalii d, produse p\
                where p.id_desc = d.id_desc\
                and p.id_prod = :bind'
            self.c.execute(querry, bind=self.values[0])
            rows = self.c.fetchall()
            for row in rows:
                self.text_descriere.insert(tk.END, row[0])
                self.change_text(self.entry_poza, row[1])
            
            self.listdet_old = [self.text_descriere.get('1.0', tk.END), self.entry_poza.get()]
            
            querry = 'select pr.denumire_prop, v.valoare\
                from proprietati pr, val_prop v, prod_prop pp, produse p\
                where pr.id_prop = pp.id_prop\
                and p.id_prod = pp.id_prod\
                and pp.id_val_prop = v.id_val_prop\
                and p.id_prod = :bind'
            self.c.execute(querry, bind = self.values[0])
            rows = self.c.fetchall()
            for row in rows:
                child = self.getTreeId(row[0])
                self.table_props.focus(child)
                self.table_props.selection_set(child)
                self.add_prop()
                self.propdict[row[0]].set(row[1])

    def change_text(self, entry, txt):
        entry.delete(0,tk.END)
        entry.insert(0,txt)
    
    def getTreeId(self, value):
        rows = self.table_props.get_children()
        for row in rows:
            a = self.table_props.item(row)
            if a['values'][0] == value:
                return row        

    def getId(self, type, value):
        if type == 'producator':
            querry = 'select id_producator from producator where denumire_producator = :bind1'
        if type == 'detalii':
            querry = 'select id_desc from detalii where poza = :bind1'
        if type == 'proprietati':
            querry = 'select id_prop from proprietati where denumire_prop = :bind1'
        if type == 'valori':
            querry = 'select id_val_prop from val_prop where valoare = :bind1'
        if type == 'produse':
            querry = 'select id_prod from produse where denumire_prod = :bind1'
        if type == 'subcategorie':
            querry = 'select id_sub from subcategorie where denumire_sub = :bind1'
        if type == 'categorie':
            querry = 'select id_cat from categorie where denumire_cat = :bind1'
        if type == 'prod_prop':
            querry = 'select id_prod_prop from prod_prop where id_prop = :bind1'


        self.c.execute(querry,bind1 = value)

        rows = self.c.fetchall()
        id= None
        for row in rows:
            id = row[0]
        return id          

class mainPanel:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry('1400x800')
        self.root.title('UtilajExpert.ro')
      
        #*Variables
        self.proprietati = None
        self.newProd = None
        self.currentProd = None
        self.con = None
        self.c = None
        
        #*Conexiune la baza de date
        try:    
         self.dsn_tns = cx_Oracle.makedsn('bd-dc.cs.tuiasi.ro', '1539', service_name='orcl')
         self.con = cx_Oracle.connect('bd094', 'csbditp', dsn=self.dsn_tns)
         self.c = self.con.cursor()
         
        except Exception as e:
            messagebox.showerror(title="Eroare la conexiune", message=e)
      
       
        #*Labels
        self.label_mainPage = tk.Label(self.root, text="Pagina Principala", font=('Arial', 12), justify='center')
        self.label_mainPage.place(x=610, y=10, width=180, height=25)
        
        #*Buttons
        self.button_proprietati= tk.Button(self.root, text='Proprietati', command=self.open_proprietati)
        self.button_proprietati.place(x=10 , y = 5, width=100, height=30 )
        
        self.button_close= tk.Button(self.root, text='Inchide', command=self.close_all)
        self.button_close.place(x=10 , y = 765, width=100, height=30 )
        
        self.button_edit = tk.Button(self.root, text = 'Vizualizeaza', command=self.edit)
        self.button_edit.place(x=1180, y=765, width=100, height=30)
        
        self.button_delete = tk.Button(self.root, text = 'Sterge', command=self.delete)
        self.button_delete.place(x=1290, y=765, width=100, height=30)
        
        self.button_add = tk.Button(self.root, text='Adauga Produs', command=self.add)
        self.button_add.place(x=1240, y=5, width=150, height=30)
        
        self.button_save = tk.Button(self.root, text= 'Salveaza', command= self.save)
        self.button_save.place(x=1070, y=765, width=100, height=30)
        #*Table
        self.tree = self.create_table()
        
        #*Completare date
        self.complete_mainTable()
        
        #*mainLoop
        self.root.mainloop()
        
    
    def edit(self):
        #TODO creeaza un window de tip product in care valorile sunt deja completate in widgets cu linia selectata anterior
        selection = self.tree.focus()
        v1= self.tree.item(selection)
        val = v1['values']
        if val == '':
            messagebox.showerror(title='Eroare', message='Eroare: Selecteaza un produs')
        else:
            self.currentProd = productPanel(self.c, self.con, val)
    
    def delete(self):
        #TODO sterge linia selectata-done
        selection = self.tree.focus()
        v1= self.tree.item(selection)
        val = v1['values']
        if val == '':
            messagebox.showerror(title='Eroare', message='Niciun produs selectat')
        else:
            m= messagebox.askyesnocancel(title='Warning', message='Esti sigur ca vrei sa stergi produsul?')
            if m == True:
                querry = 'delete from produse where denumire_prod = :bind'
                querry1 = 'delete from prod_prop where id_prod =:bind'
                querry2 = 'select id_prod from produse where denumire_prod = :bind'
                
                self.c.execute(querry2, bind = val[1])
                rows = self.c.fetchall()
                id_prod=None
                for row in rows:
                    id_prod = row[0]
                self.c.execute(querry1, bind = id_prod)
                self.c.execute(querry, bind= val[1])
                self.tree.delete(selection)
        

    def add(self):
        #TODO creeaza un window de tip product in care widget-urile se completat sunt goale
        self.newProd = productPanel(self.c, self.con)
    
    def create_table(self):
        columns = ('id','denumire','producator','stoc','pret','categorie','subcategorie')
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.heading('id', text='ID')
        tree.heading('denumire', text='Denumire Produs')
        tree.heading('producator', text='Producator')
        tree.heading('stoc', text='Stoc')
        tree.heading('pret', text='Pret')
        tree.heading('categorie', text='Categorie')
        tree.heading('subcategorie', text='Subcategorie')
        
        tree.column('id',width=30, stretch=False)
        tree.column('denumire', anchor='w')
        tree.column('producator', anchor='center')
        tree.column('stoc', anchor='center')
        tree.column('pret', anchor='center')
        tree.column('categorie', anchor='center')
        tree.column('subcategorie', anchor='center')
        
        
        tree.grid(row=0, column=0, sticky='news')
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky='ns')
        
        tree.place(x=10, y=40, width=1380, height=720)
        scrollbar.place(x=1380,y=40,height=720)
        
        return tree
        
    def open_proprietati(self):
        self.proprietati = propertiesPanel(self.c)
    
    def close_all(self):
        #TODO destroy all panels and disconnect from the data base - done
        m = messagebox.askyesnocancel(title="Exit", message='Esti sigur ca vrei sa inchizi programul?')
        if m:
            n = messagebox.askyesno(title='Salvare', message='Vrei sa salvezi modificarile?')
            if n:
                self.con.commit()
                
            if self.c != None:
                self.c.close()
                self.con.close()
            if self.proprietati != None:
                self.proprietati.close_all()
            if self.newProd != None:
                self.newProd.close_all()
            if self.currentProd != None:
                self.currentProd.close_all()
            self.root.destroy()

    def complete_mainTable(self):
        self.c.execute("select p.id_prod, p.denumire_prod, pd.denumire_producator, p.stoc, p.pret, cat.denumire_cat, subcat.denumire_sub\
                            from produse p, producator pd, categorie cat, subcategorie subcat\
                            where p.id_producator = pd.id_producator\
                            and p.id_sub = subcat.id_sub\
                            and subcat.id_cat = cat.id_cat")
        res = self.c.fetchall()
        for row in res:
            self.tree.insert(parent='', index='end', text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
     
    def save(self):
        m = messagebox.askyesno(title='Salvare', message='Doriti sa salvati?')
        if m:
            try:
                self.con.commit()
                messagebox.showinfo(title='Salvare', message='Salvare reusita')
            except Exception as e:
                messagebox.showerror(title='Eroare', message=e)
            for child in self.tree.get_children():
                self.tree.delete(child)
            self.complete_mainTable()
                
            
        

if __name__ == '__main__':
    panel = mainPanel()


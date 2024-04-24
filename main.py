
from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from PIL import Image
def utilisation():
    myig2 = Tk()
    myig2.title("utilisation")
    myig2.geometry("1500x600")
    myig2.resizable(False, False)
    myig2.config(bg='white')
    sidebar_frame = CTkFrame(master=myig2, fg_color="#b0b4ff", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(False)
    sidebar_frame.pack(fill="y", anchor="w", side="left")
    table1 = ttk.Treeview(myig2, columns=(1, 2, 3, 4, 5), height=5, show="headings")
    table1.place(x=380, y=100, height=400, width=900)
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("Treeview",
                    background="#fbf9f1",
                    fieldbackground="#F5F5F5",
                    foreground="black",
                    font=("Segoe UI", 12),
                    rowheight=40)
    style.map("Treeview",
              background=[('selected', 'green')])
    table1.heading(1, text="id", anchor=CENTER, )
    table1.heading(2, text="Désignation", anchor=CENTER)
    table1.heading(3, text="matricule", anchor=CENTER)
    table1.heading(4, text="quantite ", anchor=CENTER)
    table1.heading(5, text="time ", anchor=CENTER)
    table1.column(1, width=50, minwidth=50, anchor=CENTER)
    table1.column(2, width=200, minwidth=200, anchor=CENTER)
    table1.column(3, width=150, minwidth=150, anchor=CENTER)
    table1.column(4, width=100, minwidth=100, anchor=CENTER)
    table1.column(5, width=100, minwidth=100, anchor=CENTER)

    connexion = sqlite3.connect('base')
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM TABLE2")
    donnees = curseur.fetchall()
    for ligne in table1.get_children():
        table1.delete(ligne)
    for ligne in donnees:
        table1.insert('', 'end', values=ligne)
    connexion.close()
    def send():
        global reference
        reference= champ_reference1.get()
        afficher_donnees_par_reference()

    def afficher_donnees_par_reference():
        connexion = sqlite3.connect('base')
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM TABLE1 WHERE reference=?", (reference,))
        donnees = curseur.fetchall()
        for ligne in table1.get_children():
            table1.delete(ligne)
        for ligne in donnees:
            table1.insert('', 'end', values=ligne)
        connexion.close()
    def destroy1():
        myig2.destroy()
        ouvrire()
    def destroy2():
        myig2.destroy()
        new_window()
    personne_icone = Image.open("person_icon.png")
    personne = CTkImage(dark_image=personne_icone, light_image=personne_icone, size=(20, 20))
    lise_icone = Image.open("list_icon.png")
    liste = CTkImage(dark_image=lise_icone, light_image=lise_icone, size=(20, 20))
    ajoute_icone = Image.open("ajoute.png")
    ajoute = CTkImage(light_image=ajoute_icone, size=(20, 20))
    champ_reference1 = CTkEntry(master=myig2, width=305, placeholder_text="Recherche reference", border_color="#b0b4ff",
                               border_width=2)
    champ_reference1.place(x=230, y=40)
    en = CTkButton(master=myig2, text="Recherche", fg_color="#b0b4ff", font=("Arial Bold", 19), border_width=1,
                   hover_color="#d8b7e1", text_color="black", anchor=CENTER, command=send)
    en.place(x=550, y=40)
    bt1 = CTkButton(master=sidebar_frame, text="Gestion des Données", fg_color="black", font=("Arial Bold", 12),
                    hover_color="#d8b7e1", text_color="white", anchor="w", image=ajoute,command=destroy1)
    bt1.pack(anchor="center", ipady=8, pady=(100, 0))
    bt2 = CTkButton(master=sidebar_frame, text="Historique", fg_color="black", font=("Arial Bold", 17),
                    text_color="white", hover_color="#d8b7e1", anchor="w", image=personne)
    bt2.pack(anchor="center", ipady=8, pady=(16, 0))

    bt3 = CTkButton(master=sidebar_frame, text="stock", fg_color="black", font=("Arial Bold", 17),
                    hover_color="#d8b7e1", text_color="white", anchor="w", image=liste,command=destroy2)
    bt3.pack(anchor="center", ipady=12, pady=(16, 0))
    myig2.mainloop()
def ouvrire():
    myig1 = Tk()
    myig1.title("ajouter")
    myig1.geometry("1200x620+400+50")
    myig1.config(bg='white')
    myig1.resizable(False, False)
    frame1 = CTkFrame(master=myig1, fg_color="#b0b4ff", width=176, height=650, corner_radius=0)
    frame1.pack_propagate(False)
    frame1.pack(fill="y", anchor="w", side="left")
    def suprimer():
        # Connect to the database
        conn = sqlite3.connect('base')
        cursor = conn.cursor()
        mt = reference1.get()
        # Récupérer toutes les lignes avec la même référence
        cursor.execute("SELECT * FROM TABLE1 WHERE reference=?", (mt,))
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("DELETE FROM TABLE1 WHERE reference=?", (mt,))
        conn.commit()
        conn.close()
    def modifierdonner():
            mt = reference1.get()
            qn = quantite1.get()
            qnt = quantitemin1.get()
            if not mt or not qn or not qnt:
                messagebox.showerror("Error", "Les valeurs ne peuvent pas être vides.")
                return
            connexion = sqlite3.connect('base')
            curseur = connexion.cursor()
            try:
                curseur.execute(
                    "UPDATE TABLE1 SET  quantite=?, quantiteminimal=?  WHERE reference=?",
                    (   qn, qnt, mt))
                connexion.commit()
                connexion.close()
                messagebox.showinfo("Information", "Matériel MODIFIÉ avec succès")
            except Exception as e:
                print(e)
    def ajouterdonner():
        mt = reference1.get()
        ds = desination1.get()
        qn = quantite1.get()
        qnt = quantitemin1.get()
        ip = adres1.get()
        if not mt or not ds or not qn or not qnt or not ip:
            messagebox.showerror("Error", "Les valeurs ne peuvent pas être vides.")
            return
        connexion = sqlite3.connect('base')
        curseur = connexion.cursor()
        try:

            curseur.execute("SELECT MAX(id) FROM TABLE1")
            max_id = curseur.fetchone()[0]
            if max_id is None:
                max_id = 0

            new_id = max_id + 1

            curseur.execute(
                "INSERT INTO TABLE1 (id, Désignation, reference, quantite, quantiteminimal, position) VALUES (?, ?, ?, ?, ?, ?)",
                (new_id, ds, mt, qn, qnt, ip))

            connexion.commit()
            connexion.close()

            messagebox.showinfo("Information", "Matériel ajouté avec succès")

        except Exception as e:
            print(e)

    def destroy1():
        myig1.destroy()
        utilisation()
    def ajouter():
        myig1.destroy()

        new_window()

    personne_icone = Image.open("person_icon.png")
    personne = CTkImage(dark_image=personne_icone, light_image=personne_icone, size=(20, 20))
    lise_icone = Image.open("list_icon.png")
    liste = CTkImage(dark_image=lise_icone, light_image=lise_icone, size=(20, 20))
    ajoute_icone = Image.open("ajoute.png")
    ajoute = CTkImage(light_image=ajoute_icone, size=(20, 20))
    bt1 = CTkButton(master=frame1, text="Gestion des Données", fg_color="black", font=("Arial Bold", 12),
                    hover_color="#d8b7e1", text_color="white", anchor="w", image=ajoute)
    bt1.pack(anchor="center", ipady=8, pady=(100, 0))
    bt2 = CTkButton(master=frame1, text="Historique", fg_color="black", font=("Arial Bold", 17),
                    text_color="white", hover_color="#d8b7e1", anchor="w", image=personne,command=destroy1)
    bt2.pack(anchor="center", ipady=8, pady=(16, 0))
    bt3 = CTkButton(master=frame1, text="stock", fg_color="black", font=("Arial Bold", 17),
                    hover_color="#d8b7e1", text_color="white", anchor="w", image=liste, command=ajouter)
    bt3.pack(anchor="center", ipady=12, pady=(16, 0))

    message = CTkLabel(master=myig1, text="ajouter la nouvelle article", text_color="black", fg_color="#f5f5f8",
                        font=("Arial Black", 30))
    message.place(x=370, y=0)

    reference = Label(myig1, relief=RIDGE, text="reference", font=("Arial", 16), bg="#e1f7ff", fg="black")


    reference.place(x=306, y=129, width=200, height=33)
    reference1 = CTkEntry(master=myig1, width=220, placeholder_text="", border_color="#b0b4ff",
                           border_width=2)

    reference1.place(x=400, y=103)


    desination = Label(myig1, relief=RIDGE, text="desination", font=("Arial", 16), bg="#e1f7ff", fg="black",borderwidth=2)
    desination.place(x=303, y=189, width=200, height=33)


    desination1 = CTkEntry(master=myig1, width=220, placeholder_text="", border_color="#b0b4ff",
                          border_width=2)

    desination1.place(x=400, y=151)



    quantite = Label(myig1, relief=RIDGE, text="quantite", font=("Arial", 16), bg="#e1f7ff", fg="black")

    quantite.place(x=303, y=251, width=200, height=33)
    quantite1 = CTkEntry(master=myig1, width=220, placeholder_text="", border_color="#b0b4ff",
                          border_width=2)
    quantite1.place(x=400, y=201,)

    quantitemin = Label(myig1, relief=RIDGE, text="quantite minimal", font=("Arial", 16), bg="#e1f7ff", fg="black",borderwidth=2,border=1)

    quantitemin.place(x=303, y=314, width=200, height=33)
    quantitemin1 = CTkEntry(master=myig1, width=220, placeholder_text="", border_color="#b0b4ff",
                          border_width=2)
    quantitemin1.place(x=400, y=251)

    adres = Label(myig1, relief=RIDGE, text="position", font=("Arial Bold", 16), bg="#e1f7ff", fg="black",borderwidth=2,border=1)
    adres.place(x=306, y=376, width=200, height=33)
    adres1 = CTkEntry(master=myig1, width=220, placeholder_text="", border_color="#b0b4ff",
                          border_width=2)
    adres1.place(x=400, y=300)

    en = CTkButton(master=myig1, text="Enregistrer", fg_color="green", font=("Arial Bold", 19), border_width=1,border_color="black",
                   hover_color="#d8b7e1", text_color="black", anchor=CENTER, command=ajouterdonner)
    en.place(x=400, y=350)

    sup = CTkButton(master=myig1, text="Supprimer", fg_color="red", font=("Arial Bold", 19), border_width=1,
                   hover_color="#d8b7e1", text_color="black", anchor=CENTER, command=suprimer)
    sup.place(x=580, y=350)

    en = CTkButton(master=myig1, text="Modifier", fg_color="#b0b4ff", font=("Arial Bold", 19), border_width=1,
                   hover_color="#d8b7e1", text_color="black", anchor=CENTER, command=modifierdonner)
    en.place(x=740, y=350)

    myig1.mainloop()
def new_window():
    myig = CTk()
    myig.title("Gestion de stock")
    myig.geometry("1500x800+1+1")
    myig.config(bg='#efeff8')
    sidebar_frame = CTkFrame(master=myig, fg_color="#b0b4ff", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(False)
    sidebar_frame.pack(fill="y", anchor="w", side="left")
    def fonction1():
        destroy()
        utilisation()

    def fonction():
        destroy()
        ouvrire()
    def destroy():
        myig.destroy()
    def send():
        global reference
        reference = champ_reference.get()
        afficher_donnees_par_reference(reference)
    def afficher_donnees_par_reference(reference):
        connexion = sqlite3.connect('base')
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM TABLE1 WHERE reference=?", (reference,))
        donnees = curseur.fetchall()
        for ligne in table.get_children():
            table.delete(ligne)
        for ligne in donnees:
            table.insert('', 'end', values=ligne)
        connexion.close()
    def afficher_donnees():
        connexion = sqlite3.connect('base')
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM TABLE1")
        donnees = curseur.fetchall()
        for ligne in table.get_children():
            table.delete(ligne)
        for ligne in donnees:
            table.insert('', 'end', values=ligne)
        connexion.close()
    def send_matricule_quantite():
        while True:
            global matricule
            matricule = simpledialog.askstring("Matricule", "Entrez le matricule")
            if matricule is not None:
                    if matricule=="iyed" or matricule=="asma"or matricule=="fahed":
                        messagebox.showinfo("","Matricule validé.")
                        global quantite2
                        quantite2 = simpledialog.askstring("Quantité", "Entrez la quantité")
                        if quantite2 is not None and int(quantite2)  >  0 :
                                quantite2 = int(quantite2)
                                inserer_donnees()
                                break
                        else:
                            messagebox.showerror("Erreur", "Veuillez entrer une quantité valide.")
                    else:
                       messagebox.showerror("Erreur", "Veuillez entrer une matricule valide.")
            else:
                break
    def inserer_donnees():
        if table.selection():
            selected_items = table.selection()
            for item in selected_items:
                    reference4= table.item(item, 'values')[2]
                    conn = sqlite3.connect('base')
                    cursor = conn.cursor()
                    cursor.execute('SELECT quantite FROM TABLE1 WHERE reference = ?', (reference4,))
                    quantitegeneral = cursor.fetchone()[0]
                    cursor.execute('SELECT quantiteminimal FROM TABLE1 WHERE reference = ?', (reference4,))
                    quantitemin=cursor.fetchone()[0]
                    if quantitegeneral >= quantite2:
                        cursor.execute('INSERT INTO TABLE2 (matricule, quantite,reference) VALUES (?, ?, ?)',
                                    (matricule, quantite2, reference4))
                        conn.commit()
                        newquantity = quantitegeneral - quantite2
                        cursor.execute('UPDATE TABLE1 SET quantite=? WHERE reference=?', (newquantity, reference4))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("info","Félicitations, la matricule et la quantité ont été validées. L'armoire correspondant à la référence sélectionnée a été ouverte avec succès. Veuillez retirer la quantité saisie et fermer l'armoire après avoir terminé le processus de retrait. Merci.")
                        if newquantity<=quantitemin:
                            fon()
                    else:
                      messagebox.showerror("Erreur", "La quantité entrée est supérieure à la quantité disponible.")
        else:
            messagebox.showerror("Erreur", "Aucune colonne sélectionnée")
    def fon():
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'iyedgharbi479@gmail.com'
        smtp_password = 'jmzawyxjzihzinif'
        # Créer un objet SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = 'gharbiiyed10@example.com'
        msg['Subject'] = 'Sujet de l\'email'
        message = 'la quantite restant et inferieur a la quantite minimal '
        msg.attach(MIMEText(message, 'plain'))
        # Envoyer l'e-mail
        server.send_message(msg)
        # Fermer la connexion SMTP
        server.quit()
    def executer_deux_fonctions():
        send_matricule_quantite()
    Lbltitre =CTkLabel(master=myig, text="Gestion de stock", text_color="black",fg_color="#f5f5f8", font=("Arial Black", 40))
    Lbltitre.place(x=640, y=0)
    Lblmateriel = Label(myig, relief=RIDGE, text="Liste des articles", font=("Arial", 20), bg="#f5f5f8", fg="black")
    Lblmateriel.place(x=650,y=235, width=760)
    champ_reference = CTkEntry(master=myig, width=305, placeholder_text="Recherche reference", border_color="#b0b4ff", border_width=2)
    champ_reference.place(x=230, y=102)
    en = CTkButton(master=myig, text="Recherche", fg_color="#b0b4ff", font=("Arial Bold", 19),border_width=1, hover_color="#d8b7e1",text_color="black", anchor=CENTER,command=send)
    en.place(x=550,y=102)
    bouton_afficher = CTkButton(master=myig, text="  Afficher ", fg_color="#b0b4ff", font=("Arial Bold", 19), border_width=1 ,hover_color="#d8b7e1",text_color="black", anchor=CENTER,command=afficher_donnees)
    bouton_afficher.place(x=700,y=102)
    ov = CTkButton(master=myig, text="  Ouvrir ", fg_color="#b0b4ff", font=("Arial Bold", 30), hover_color="GREEN",text_color="black", anchor=CENTER,border_width=1,command=executer_deux_fonctions)
    ov.place(x=700,y=600)  # command=save_data)
    personne_icone = Image.open("person_icon.png")
    personne = CTkImage(dark_image=personne_icone, light_image=personne_icone, size=(20, 20))
    lise_icone = Image.open("list_icon.png")
    liste = CTkImage(dark_image=lise_icone, light_image=lise_icone, size=(20, 20))
    ajoute_icone = Image.open("ajoute.png")
    ajoute = CTkImage( light_image=ajoute_icone, size=(20, 20))
    bt1 =CTkButton(master=sidebar_frame, text="Gestion des Données", fg_color="black", font=("Arial Bold", 12),
             hover_color="#d8b7e1",text_color="white", anchor="w",image=ajoute,command=fonction)
    bt1.pack(anchor="center", ipady=8, pady=(160, 0))
    bt2 = CTkButton(master=sidebar_frame, text="Historique", fg_color="black", font=("Arial Bold", 17), text_color="white", hover_color="#d8b7e1", anchor="w",image=personne,command=fonction1)
    bt2.pack(anchor="center", ipady=8, pady=(16, 0))
    bt3 =CTkButton(master=sidebar_frame, text="stock", fg_color="black", font=("Arial Bold", 17), hover_color="#d8b7e1",text_color="white", anchor="w",image=liste)
    bt3.pack(anchor="center", ipady=8, pady=(16, 0))
    table = ttk.Treeview(myig, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
    table.place(x=430, y=270, height=450, width=1300)
    # Define a custom style for the table
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("Treeview",
                    background="#fbf9f1",
                    fieldbackground="#F5F5F5",
                    foreground="black",
                    font=("Segoe UI", 12),
                    rowheight=40)
    style.map("Treeview",
              background=[('selected', 'green')])
    # Set column headers
    table.heading(1, text="id", anchor=CENTER,)
    table.heading(2, text="Désignation", anchor=CENTER)
    table.heading(3, text="reference", anchor=CENTER)
    table.heading(4, text="quantite ", anchor=CENTER)
    table.heading(5, text="quantite minimal", anchor=CENTER)
    table.heading(6, text="Position", anchor=CENTER)

    # Set column widths
    table.column(1, width=50, minwidth=50, anchor=CENTER)
    table.column(2, width=150, minwidth=150, anchor=CENTER)
    table.column(3, width=150, minwidth=150, anchor=CENTER)
    table.column(4, width=100, minwidth=100, anchor=CENTER)
    table.column(5, width=150, minwidth=150, anchor=CENTER)
    table.column(6, width=250, minwidth=250, anchor=CENTER)

    # Pack the table

    myig.mainloop()
root =CTk()
def check_credentials():
    id_entry = entry_id.get()
    password_entry = entry_password.get()
    if \
            id_entry == '' and password_entry == '':
             # Vérifie si la fenêtre principale existe encore
            root.destroy()
            new_window()
    else:
        messagebox.showerror("erreur","user id or password est incorrect")
root.title("Login")
root.config(bg='#e5f1e9')
root.geometry("900x460")
root.resizable(False,False)
frame = CTkFrame(master=root, width=439, height=395, fg_color="#ffffff")
frame.place(x=40,y=20)
photo = PhotoImage(file='logiin.png')
im = Label(frame, image=photo)
im.place(x=0, y=0,)
im.config(bg='#e5f1e9')
photo45 = PhotoImage(file='pszphoto.png')
im1 = Label(root, image=photo45)
im1.place(x=880, y=450,)
im1.config(bg='#e5f1e9')

email_icon_data = Image.open("email.png")
photo1 = PhotoImage(file='passs.png')
password_icon_data = Image.open("passs.png")

password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20,20))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))

id_label =CTkLabel(master=root, text="  USER ", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 20), image=email_icon, compound="left")
id_label.place(x=640,y=80)
entry_id = CTkEntry(master=root,placeholder_text="start typing...",width=200,text_color="#242424")
entry_id.place(x=640,y=110)

password_label = CTkLabel(master=root, text="  Password", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 20), image=password_icon, compound="left")
password_label.place(x=640,y=185)
entry_password = CTkEntry(master=root,placeholder_text="start typing...",width=200,text_color="#242424",show='*')
entry_password.place(x=640,y=220)

submit_button=CTkButton(master=root, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=check_credentials)
submit_button.place(x=630,y=290)
root.mainloop()



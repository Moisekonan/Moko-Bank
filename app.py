import os
import requests
import io
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from database import Base, Comptes, Clients, Utilisateurs, Carnet_client, Transactions
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import xlwt
from fpdf import FPDF

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)

# Configurer la BaseDonnée
engine = create_engine('sqlite:///mokobank.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))

# charge donnees
nom_utilisateur = 'C00000001'
nom = 'Moise'
user_type = 'gestionnaire'
mdp = 'Moiseo@001'
mdp_hash = bcrypt.generate_password_hash(mdp).decode('utf-8')
db.execute(text("INSERT INTO utilisateurs (id,nom,user_type,mot_de_passe) VALUES (:u,:n,:t,:p)"),
            {"u": nom_utilisateur,"n":nom,"t":user_type ,"p": mdp_hash})
db.commit()
print("compte Terminé ............................................ ")
# user 2
nom_utilisateur = 'C00000002'
nom = 'Mental'
user_type = 'caissier'
mdp = 'Mental@002'
mdp_hash = bcrypt.generate_password_hash(mdp).decode('utf-8')
db.execute(text("INSERT INTO utilisateurs (id,nom,user_type,mot_de_passe) VALUES (:u,:n,:t,:p)"),
            {"u": nom_utilisateur,"n":nom,"t":user_type ,"p": mdp_hash})
db.commit()
print("compte Terminé ............................................ ")
# user 3
nom_utilisateur = 'C00000003'
nom = 'NaN'
user_type = 'caissier'
mdp = 'NaNDigit@003'
mdp_hash = bcrypt.generate_password_hash(mdp).decode('utf-8')
db.execute(text("INSERT INTO utilisateurs (id,nom,user_type,mot_de_passe) VALUES (:u,:n,:t,:p)"),
            {"u": nom_utilisateur,"n":nom,"t":user_type ,"p": mdp_hash})
db.commit()
print("compte Terminé ............................................ ")

# Code principal (Les Routes)
@app.route('/')
@app.route("/dashboard")
def dashboard():
    return render_template("accueil.html", home=True)


@app.route("/ajoutclient", methods=["GET", "POST"])
def ajoutclient():
    # recupere les pays api
    recup_pays = requests.get('https://restcountries.com/v3.1/all', [])
    liste_pays = recup_pays.json()
    pays_nom = []
    for i in liste_pays:
        pays_nom.append(i['name']['common'])

    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            client_ssn_id = int(request.form.get("client_ssn_id"))
            nom = str(request.form.get("nom"))
            email = str(request.form.get("email"))
            age = int(request.form.get("age"))
            pays = str(request.form.get("pays"))
            ville = str(request.form.get("ville"))
            
            # Utilisez text() pour définir la requête SQL
            query_check_existing = text("SELECT * FROM clients WHERE client_ssn_id = :c")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_existing, {"c": client_ssn_id}).fetchone()
            
            if result is None:
                result_count = db.query(Clients).count()
                if result_count == 0:
                    query_insert = text("INSERT INTO clients (id_client, client_ssn_id, nom, email, age, pays, ville, statut) VALUES (110110000, :c, :n, :add, :a, :s, :ville, 'activer')")
                else:
                    query_insert = text("INSERT INTO clients (client_ssn_id, nom, email, age, pays, ville, statut) VALUES (:c, :n, :add, :a, :s, :ville, 'activer')")
                
                # Exécutez la requête SQL d'insertion avec des paramètres
                db.execute(query_insert, {"c": client_ssn_id, "n": nom, "add": email, "a": age, "s": pays, "ville": ville})
                db.commit()
                
                # Obtenez l'ID du client inséré
                inserted_client = db.execute(text("SELECT id_client FROM clients WHERE client_ssn_id = :c"), {"c": client_ssn_id}).fetchone()
                
                if inserted_client is None:
                    flash("Les données ne sont pas insérées ! Vérifiez votre saisie.", "danger")
                else:
                    temp = Carnet_client(id_client=inserted_client.id_client, message_enregistrement="Client Créé")
                    db.add(temp)
                    db.commit()
                    flash(f"Client {nom} est créé avec l'identifiant du client : {inserted_client.id_client}.", "success")
                    return redirect(url_for('voirclient'))
            
            flash(f'SSN id : {client_ssn_id} est déjà présent dans la base de données.', 'warning')

    return render_template('ajoutclient.html', ajoutclient=True, pays=sorted(pays_nom))

@app.route("/voirclient/<id_client>")
@app.route("/voirclient", methods=["GET", "POST"])
def voirclient(id_client=None):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            client_ssn_id = request.form.get('client_ssn_id')
            id_client = request.form.get('id_client')
            
            # Utilisez text() pour définir la requête SQL
            query = text("SELECT * FROM clients WHERE id_client = :c OR client_ssn_id = :d")
            
            # Exécutez la requête SQL avec des paramètres
            data = db.execute(query, {"c": id_client, "d": client_ssn_id}).fetchone()
            
            if data is not None:
                return render_template('voirclient.html', voirclient=True, data=data)

            flash("Client n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
        elif id_client is not None:
            
            # Utilisez text() pour définir la requête SQL
            query = text("SELECT * FROM clients WHERE id_client = :c")
            
            # Exécutez la requête SQL avec des paramètres
            data = db.execute(query, {"c": id_client}).fetchone()
            
            if data is not None:
                return render_template('voirclient.html', voirclient=True, data=data)

            flash("Client n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
    else:
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))

    return render_template('voirclient.html', voirclient=True)

@app.route('/modifierclient')
@app.route('/modifierclient/<id_client>', methods=["GET", "POST"])
def modifierclient(id_client=None):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if id_client is not None:
            if request.method != "POST":
                id_client = int(id_client)
                
                # Utilisez text() pour définir la requête SQL
                query = text("SELECT * FROM clients WHERE id_client = :c AND statut != 'desactiver'")
                
                # Exécutez la requête SQL avec des paramètres
                data = db.execute(query, {"c": id_client}).fetchone()
                
                if data is not None:
                    return render_template('modifierclient.html', modifierclient=True, data=data)
                else:
                    flash('Le client est désactivé ou absent de la base de données.', 'warning')
            else:
                id_client = int(id_client)
                nom = str(request.form.get("nom"))
                email = str(request.form.get("email"))
                age = int(request.form.get("age"))
                
                # Utilisez text() pour définir la requête SQL
                query_check_existing = text("SELECT * FROM clients WHERE id_client = :c AND statut = 'activer'")
                
                # Exécutez la requête SQL avec des paramètres
                result = db.execute(query_check_existing, {"c": id_client}).fetchone()
                
                if result is not None:
                    query_update = text("UPDATE clients SET nom = :n, email = :add, age = :ag WHERE id_client = :a")
                    
                    # Exécutez la requête SQL d'update avec des paramètres
                    db.execute(query_update, {"n": nom, "add": email, "ag": age, "a": id_client})
                    db.commit()
                    
                    temp = Carnet_client(id_client=id_client, message_enregistrement="Mise à jour des données clients")
                    db.add(temp)
                    db.commit()
                    flash(f"Les données des clients ont été mises à jour avec succès.", "success")
                else:
                    flash("Identité du client invalide. Veuillez vérifier l'identité du client.", 'warning')

    return redirect(url_for('voirclient'))

@app.route('/supprimerclient')
@app.route('/supprimerclient/<id_client>')
def supprimerclient(id_client):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if id_client is not None:
            id_client = int(id_client)
            
            # Utilisez text() pour définir la requête SQL
            query_check_client = text("SELECT * from clients WHERE id_client = :a AND statut='activer'")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_client, {"a": id_client}).fetchone()
            
            if result is not None:
                # Utilisez text() pour définir la requête SQL d'update
                query_update_client = text("UPDATE clients SET statut='desactiver' WHERE id_client = :a")
                
                # Exécutez la requête SQL d'update avec des paramètres
                db.execute(query_update_client, {"a": id_client})
                db.commit()
                
                temp = Carnet_client(id_client=id_client, message_enregistrement="Client Désactivé")
                db.add(temp)
                db.commit()
                flash(f"Le Client est Désactivé.", "success")
                return redirect(url_for('dashboard'))
            
            else:
                flash(
                    f"Client avec identifiant: {id_client} est déjà désactivé ou n'est pas présent dans la base de données.", 'warning')
    
    return redirect(url_for('modifierclient'))

@app.route('/activerclient')
@app.route('/activerclient/<id_client>')
def activerclient(id_client):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if id_client is not None:
            id_client = int(id_client)
            
            # Utilisez text() pour définir la requête SQL
            query_check_client = text("SELECT * from clients WHERE id_client = :a AND statut='desactiver'")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_client, {"a": id_client}).fetchone()
            
            if result is not None:
                # Utilisez text() pour définir la requête SQL d'update
                query_update_client = text("UPDATE clients SET statut='activer' WHERE id_client = :a")
                
                # Exécutez la requête SQL d'update avec des paramètres
                db.execute(query_update_client, {"a": id_client})
                db.commit()
                
                temp = Carnet_client(id_client=id_client, message_enregistrement="Client Activé")
                db.add(temp)
                db.commit()
                flash(f"Le client est activé.", "success")
                return redirect(url_for('dashboard'))
            
            flash(
                f"Client avec identifiant: {id_client} est déjà activé ou n'est pas présent dans la base de données.", 'warning')
    
    return redirect(url_for('modifierclient'))

@app.route('/activercompte')
@app.route('/activercompte/<id_compte>')
def activercompte(id_compte=None):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if id_compte is not None:
            id_compte = int(id_compte)
            
            # Utilisez text() pour définir la requête SQL
            query_check_compte = text("SELECT * FROM comptes WHERE id_compte = :a AND statut='desactiver'")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_compte, {"a": id_compte}).fetchone()
            
            if result is not None:
                date = datetime.datetime.now()
                
                # Utilisez text() pour définir la requête SQL d'update
                query_update_compte = text("UPDATE comptes SET statut='activer', message='Le compte est réactivé', dernier_majour = :d WHERE id_compte = :a")
                
                # Exécutez la requête SQL d'update avec des paramètres
                db.execute(query_update_compte, {"d": date, "a": id_compte})
                db.commit()
                
                flash(f"Le compte est activé.", "success")
                return redirect(url_for('dashboard'))
            
            flash(
                f"Compte avec identifiant: {id_compte} est déjà activé ou n'est pas présent dans la base de données.", 'warning')
    
    return redirect(url_for('voircompte'))

@app.route('/statutclient')
def statutclient():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        
        # Utilisez text() pour définir la requête SQL
        query = text("SELECT clients.id_client as id, clients.client_ssn_id as ssn_id, clients.nom, clients.statut, carnet_client.message_enregistrement as message, carnet_client.heure_sortir as date "
                     "FROM (SELECT id_client, MAX(heure_sortir) as max_date "
                     "FROM carnet_client GROUP BY id_client) as latest_carnet "
                     "JOIN carnet_client ON latest_carnet.id_client = carnet_client.id_client "
                     "AND latest_carnet.max_date = carnet_client.heure_sortir "
                     "JOIN clients ON clients.id_client = latest_carnet.id_client "
                     "ORDER BY carnet_client.heure_sortir DESC")
        
        # Exécutez la requête SQL
        data = db.execute(query).fetchall()
        
        if data:
            return render_template('statutclient.html', statutclient=True, data=data)
        else:
            flash('Aucune donnée trouvée.', 'danger')
    
    return redirect(url_for('dashboard'))


@app.route("/ajoutcompte", methods=["GET", "POST"])
def ajoutcompte():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            id_client = int(request.form.get("id_client"))
            type_de_compte = request.form.get("type_de_compte")
            montant = float(request.form.get("montant"))
            message = "Compte créé avec succès"
            
            # Utilisez text() pour définir la requête SQL
            query_check_client = text("SELECT * FROM clients WHERE id_client = :c")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_client, {"c": id_client}).fetchone()
            
            if result is not None:
                
                # Utilisez text() pour définir la requête SQL
                query_check_compte = text("SELECT * FROM comptes WHERE id_client = :c AND type_de_compte = :at")
                
                # Exécutez la requête SQL avec des paramètres
                result = db.execute(query_check_compte, {"c": id_client, "at": type_de_compte}).fetchone()
                
                if result is None:
                    result_count = db.query(Comptes).count()
                    if result_count == 0:
                        query_insert = text("INSERT INTO comptes (id_compte, type_de_compte, balance, id_client, statut, message, dernier_majour) VALUES (360110000, :at, :m, :c, 'activer', :msg, :d)")
                    else:
                        query_insert = text("INSERT INTO comptes (type_de_compte, balance, id_client, statut, message, dernier_majour) VALUES (:at, :m, :c, 'activer', :msg, :d)")
                    
                    # Exécutez la requête SQL d'insertion avec des paramètres
                    db.execute(query_insert, {"at": type_de_compte, "m": montant, "c": id_client, "msg": message, "d": datetime.datetime.now()})
                    db.commit()
                    
                    flash(
                        f"Le compte {type_de_compte} est créé avec l'ID du client : {id_client}.", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash(
                        f'Client avec identifiant: {id_client} a déjà un compte {type_de_compte}.', 'warning')
            else:
                flash(
                    f"Client avec identifiant: {id_client} n'existe pas dans la base de données.", 'warning')
    
    return render_template('ajoutcompte.html', ajoutcompte=True)


@app.route("/supprimercompte", methods=["GET", "POST"])
def supprimercompte():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            id_compte = int(request.form.get("id_compte"))
            
            # Utilisez text() pour définir la requête SQL
            query_check_compte = text("SELECT * FROM comptes WHERE id_compte = :a AND statut='activer'")
            
            # Exécutez la requête SQL avec des paramètres
            result = db.execute(query_check_compte, {"a": id_compte}).fetchone()
            
            if result is not None:
                message = "Compte désactivé"
                date = datetime.datetime.now()
                
                # Utilisez text() pour définir la requête SQL d'update
                query_update_compte = text("UPDATE comptes SET statut='desactiver', message= :m, dernier_majour = :d WHERE id_compte = :a;")
                
                # Exécutez la requête SQL d'update avec des paramètres
                db.execute(query_update_compte, {"m": message, "d": date, "a": id_compte})
                db.commit()
                
                flash(f"Le compte client a été désactivé avec succès.", "success")
                return redirect(url_for('dashboard'))
            
            flash(
                f"Compte avec identifiant: {id_compte} est déjà désactivé ou le compte n'est pas trouvé.", 'warning')
    
    return render_template('supprimercompte.html', supprimercompte=True)

@app.route("/voircompte", methods=["GET", "POST"])
def voircompte():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == "gestionnaire" or session['user_type'] == "caissier":
        if request.method == "POST":
            id_compte = request.form.get("id_compte")
            id_client = request.form.get("id_client")
            
            # Utilisez text() pour définir la requête SQL
            query = text("SELECT * FROM comptes WHERE id_client = :c or id_compte = :d")
            
            # Exécutez la requête SQL avec des paramètres
            data = db.execute(query, {"c": id_client, "d": id_compte}).fetchone()
            
            if data:
                return render_template('voircompte.html', voircompte=True, data=data)

            flash(
                "Le compte n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
    else:
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    return render_template('voircompte.html', voircompte=True)

@app.route("/voircomptestatut", methods=["GET", "POST"])
def voircomptestatut():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        
        # Utilisez text() pour définir la requête SQL
        query = text("SELECT * FROM comptes")
        
        # Exécutez la requête SQL
        data = db.execute(query).fetchall()
        
        if data:
            return render_template('voircomptestatut.html', voircomptestatut=True, data=data)
        else:
            flash("Les comptes sont introuvables !", 'danger')
    
    return render_template('voircomptestatut.html', voircomptestatut=True)

@app.route('/depot', methods=['GET', 'POST'])
@app.route('/depot/<id_compte>', methods=['GET', 'POST'])
def depot(id_compte):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "caissier":
        if id_compte is None:
            return redirect(url_for('voircompte'))
        else:
            if request.method == "POST":
                montant = request.form.get("montant")
                
                # Utilisez text() pour définir la requête SQL
                query_check_compte = text("SELECT * FROM comptes WHERE id_compte = :a AND statut='activer'")
                
                # Exécutez la requête SQL avec des paramètres
                data = db.execute(query_check_compte, {"a": id_compte}).fetchone()
                
                if data is not None:
                    balance = int(montant) + int(data.balance)
                    
                    # Utilisez text() pour définir la requête SQL d'update
                    query_update_compte = text("UPDATE comptes SET balance= :b WHERE id_compte = :a")
                    
                    # Exécutez la requête SQL d'update avec des paramètres
                    db.execute(query_update_compte, {"b": balance, "a": data.id_compte})
                    db.commit()
                    
                    flash(
                        f"Montant {montant} F CFA déposé sur le compte: {data.id_compte} avec succès.", 'success')
                    
                    temp = Transactions(
                        id_compte=data.id_compte, trans_message="Montant du dépôt", montant=montant)
                    db.add(temp)
                    db.commit()
                else:
                    flash(f"Compte introuvable ou désactivé.", 'danger')
            else:
                query_get_compte = text("SELECT * FROM comptes WHERE id_compte = :a")
                
                # Exécutez la requête SQL avec des paramètres
                data = db.execute(query_get_compte, {"a": id_compte}).fetchone()
                
                if data is not None:
                    return render_template('depot.html', depot=True, data=data)
                else:
                    flash(f"Compte introuvable ou désactivé.", 'danger')

    return redirect(url_for('dashboard'))

# Code pour le montant de retrait

@app.route('/retrait', methods=['GET', 'POST'])
@app.route('/retrait/<id_compte>', methods=['GET', 'POST'])
def retrait(id_compte):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "caissier":
        if id_compte is None:
            return redirect(url_for('voircompte'))
        else:
            if request.method == "POST":
                montant = request.form.get("montant")
                
                # Utilisez text() pour définir la requête SQL
                query_check_compte = text("SELECT * FROM comptes WHERE id_compte = :a AND statut='activer'")
                
                # Exécutez la requête SQL avec des paramètres
                data = db.execute(query_check_compte, {"a": id_compte}).fetchone()
                
                if data is not None:
                    if int(data.balance) >= int(montant):
                        balance = int(data.balance) - int(montant)
                        
                        # Utilisez text() pour définir la requête SQL d'update
                        query_update_compte = text("UPDATE comptes SET balance= :b WHERE id_compte = :a")
                        
                        # Exécutez la requête SQL d'update avec des paramètres
                        db.execute(query_update_compte, {"b": balance, "a": data.id_compte})
                        db.commit()
                        
                        flash(
                            f"{montant} F CFA prélevé sur le compte: {data.id_compte} avec succès.", 'success')
                        
                        temp = Transactions(
                            id_compte=data.id_compte, trans_message="Montant prélevé", montant=montant)
                        db.add(temp)
                        db.commit()
                    else:
                        flash(f"Le solde du compte est insuffisant.", 'danger')
                        return redirect(url_for('voircompte'))
                else:
                    flash(f"Compte introuvable ou désactivé.", 'danger')
            else:
                query_get_compte = text("SELECT * FROM comptes WHERE id_compte = :a")
                
                # Exécutez la requête SQL avec des paramètres
                data = db.execute(query_get_compte, {"a": id_compte}).fetchone()
                
                if data is not None:
                    return render_template('retrait.html', depot=True, data=data)
                else:
                    flash(f"Compte introuvable ou désactivé.", 'danger')

    return redirect(url_for('dashboard'))

@app.route('/transfert', methods=['GET', 'POST'])
@app.route('/transfert/<id_client>', methods=['GET', 'POST'])
def transfert(id_client=None):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "caissier":
        if id_client is None:
            return redirect(url_for('voircompte'))
        else:
            if request.method == 'POST':
                src_type = request.form.get("src_type")
                trg_type = request.form.get("trg_type")
                montant = int(request.form.get("montant"))
                if src_type != trg_type:
                    query_check_src_compte = text("SELECT * FROM comptes WHERE id_client = :a AND type_de_compte = :t AND statut='activer'")
                    src_data = db.execute(query_check_src_compte, {"a": id_client, "t": src_type}).fetchone()

                    query_check_trg_compte = text("SELECT * FROM comptes WHERE id_client = :a AND type_de_compte = :t AND statut='activer'")
                    trg_data = db.execute(query_check_trg_compte, {"a": id_client, "t": trg_type}).fetchone()

                    if src_data is not None and trg_data is not None:
                        if src_data.balance > montant:
                            src_balance = src_data.balance - montant
                            trg_balance = trg_data.balance + montant

                            query_update_src_compte = text("UPDATE comptes SET balance = :b WHERE id_client = :a AND type_de_compte = :t")
                            db.execute(query_update_src_compte, {"b": src_balance, "a": id_client, "t": src_type})
                            db.commit()
                            temp = Transactions(
                                id_compte=src_data.id_compte, trans_message="Montant transféré à "+str(trg_data.id_compte), montant=montant)
                            db.add(temp)
                            db.commit()

                            query_update_trg_compte = text("UPDATE comptes SET balance = :b WHERE id_client = :a AND type_de_compte = :t")
                            db.execute(query_update_trg_compte, {"b": trg_balance, "a": id_client, "t": trg_type})
                            db.commit()
                            temp = Transactions(
                                id_compte=trg_data.id_compte, trans_message="Montant reçu de " + str(src_data.id_compte), montant=montant)
                            db.add(temp)
                            db.commit()

                            flash(
                                f"Montant {montant} F CFA transféré à {trg_data.id_compte} de {src_data.id_compte} avec succès", 'success')
                        else:
                            flash("Montant insuffisant pour transférer.", "danger")

                    else:
                        flash("Comptes introuvables", "danger")

                else:
                    flash(
                        "Impossible de transférer le montant sur le même compte.", 'warning')

            else:
                query_get_comptes = text("SELECT * FROM comptes WHERE id_client = :a")
                data = db.execute(query_get_comptes, {"a": id_client}).fetchall()
                if data:
                    return render_template('transfert.html', depot=True, id_client=id_client)
                else:
                    flash("Données introuvables ou ID client invalide", 'danger')
                    return redirect(url_for('voircompte'))

    return redirect(url_for('dashboard'))

@app.route("/declaration", methods=["GET", "POST"])
def declaration():
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "caissier":
        if request.method == "POST":
            id_compte = request.form.get("id_compte")
            number = request.form.get("number")
            flag = request.form.get("Radio")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            if flag == "red":
                # "SELECT * FROM (SELECT * FROM transactions where id_compte=:d ORDER BY trans_id DESC LIMIT :l)Var1 ORDER BY trans_id ASC;"
                query = text("SELECT * FROM transactions where id_compte=:d ORDER BY trans_id DESC LIMIT :l;")
                data = db.execute(query, {"d": id_compte, "l":number}).fetchall()
                # query = text("SELECT * FROM (SELECT * FROM transactions where id_compte=:id_compte ORDER BY trans_id DESC LIMIT :number)Var1 ORDER BY trans_id ASC;")
                # data = db.execute(query, id_compte=id_compte, number=number).fetchall()
            else:
                query = text("SELECT * FROM transactions WHERE id_compte=:a between DATE(heure_sortir) >= :s AND DATE(heure_sortir) <= :e;")
                data = db.execute(query, {
                                  "a": id_compte, "s": start_date, "e": end_date}).fetchall()
                # query = text("SELECT * FROM transactions WHERE id_compte=:id_compte AND DATE(heure_sortir) BETWEEN :start_date AND :end_date;")
                # data = db.execute(query, id_compte=id_compte, start_date=start_date, end_date=end_date).fetchall()
            if data:
                return render_template('declaration.html', declaration=True, data=data, id_compte=id_compte)
            else:
                flash("Aucune transaction", 'danger')
                return redirect(url_for('dashboard'))
    else:
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))
    return render_template('declaration.html', declaration=True)

import io
from flask import Response, jsonify, render_template
from fpdf import FPDF
import xlwt

@app.route('/declaration_pdf/<id_compte>')
@app.route('/declaration_pdf/<id_compte>/<ftype>')
def declaration_pdf(id_compte=None, ftype=None):
    if 'utilisateurs' not in session:
        return redirect(url_for('login'))

    if session['user_type'] == "gestionnaire":
        flash("Vous n'avez pas accès à cette page", "warning")
        return redirect(url_for('dashboard'))

    if session['user_type'] == "caissier":
        if id_compte is not None:
            query = text("SELECT * FROM transactions WHERE id_compte=:a ORDER BY heure_sortir LIMIT 20;")
            data = db.execute(query, {"a": id_compte}).fetchall()

            if data:
                if ftype is None or ftype == 'pdf':
                    pdf = FPDF()
                    pdf.add_page()
                    page_width = pdf.w - 2 * pdf.l_margin

                    pdf.set_font('Times', 'B', 16.0)
                    pdf.cell(page_width, 0.0, "MOKO-Bank", align='C')
                    pdf.ln(10)

                    msg = 'Relevé de compte : ' + str(id_compte)
                    pdf.set_font('Times', '', 12.0)
                    pdf.cell(page_width, 0.0, msg, align='C')
                    pdf.ln(10)

                    pdf.set_font('Times', 'B', 11)
                    pdf.ln(1)

                    th = pdf.font_size

                    pdf.cell(page_width/5, th, 'Transaction Id')
                    pdf.cell(page_width/3, th, 'Description')
                    pdf.cell(page_width/3, th, 'Date')
                    pdf.cell(page_width/7, th, 'Montant')
                    pdf.ln(th)

                    pdf.set_font('Times', '', 11)

                    for row in data:
                        pdf.cell(page_width/5, th, str(row.trans_id))
                        pdf.cell(page_width/3, th, row.trans_message)
                        pdf.cell(page_width/3, th, str(row.heure_sortir))
                        pdf.cell(page_width/7, th, str(row.montant))
                        pdf.ln(th)

                    pdf.ln(10)
                    query = text("SELECT balance FROM comptes WHERE id_compte=:a;")
                    bal = db.execute(query, {"a": id_compte}).fetchone()

                    pdf.set_font('Times', '', 10.0)
                    msg = 'Solde actuel : ' + str(bal.balance) + ' F CFA'
                    pdf.cell(page_width, 0.0, msg, align='C')
                    pdf.ln(5)

                    pdf.cell(page_width, 0.0,
                             '-- Fin de la déclaration --', align='C')

                    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'inline;filename=declaration.pdf'})

                elif ftype == 'xl':
                    output = io.BytesIO()
                    workbook = xlwt.Workbook()
                    sh = workbook.add_sheet('Extrait de compte')

                    sh.write(0, 0, 'Transaction ID')
                    sh.write(0, 1, 'Description')
                    sh.write(0, 2, 'Date')
                    sh.write(0, 3, 'Montant')

                    idx = 0
                    for row in data:
                        sh.write(idx+1, 0, str(row.trans_id))
                        sh.write(idx+1, 1, row.trans_message)
                        sh.write(idx+1, 2, str(row.heure_sortir))
                        sh.write(idx+1, 3, str(row.montant))
                        idx += 1

                    workbook.save(output)
                    output.seek(0)

                    response = Response(output, mimetype="application/ms-excel", headers={
                                        "Content-Disposition": "attachment;filename=declaration.xls"})
                    return response
            else:
                flash("ID de compte invalide", 'danger')
        else:
            flash("Veuillez indiquer l'ID du compte", 'warning')

    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('utilisateurs', None)
    return redirect(url_for('login'))

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'utilisateurs' in session:
        return redirect(url_for('dashboard'))

    # if request.method == "POST":
    #     usern = request.form.get("username").upper()
    #     passw = request.form.get("password").encode('utf-8')
    #     query = text("SELECT * FROM utilisateurs WHERE id = :u")
    #     result = db.execute(query, {"u": usern}).fetchone()
    #     print(result)
    #     if result is not None:
    #         if bcrypt.check_password_hash(result['mot_de_passe'], passw) is True:
    #             session['utilisateurs'] = usern
    #             session['nom'] = result.nom
    #             session['user_type'] = result.user_type
    #             flash(
    #                 f"{result.nom.capitalize()}, vous êtes connecté(e) avec succès !", "success")
    #             return redirect(url_for('dashboard'))
    #     flash(
    #         "Désolé, le nom d'utilisateur ou le mot de passe ne correspond pas.", "danger")
    if request.method == "POST":
        usern = request.form.get("username").upper()
        passw = request.form.get("password").encode('utf-8')
        query = text("SELECT mot_de_passe, nom, user_type FROM utilisateurs WHERE id = :u")
        result = db.execute(query, {"u": usern}).fetchone()
        print(result)
        if result is not None:
            stored_password_hash = result[0]  # Colonne 'mot_de_passe'
            if bcrypt.check_password_hash(stored_password_hash, passw):
                session['utilisateurs'] = usern
                session['nom'] = result[1]  # Colonne 'nom' 
                session['user_type'] = result[2]  # Colonne 'user_type'
                flash(
                    f"{session['nom'].capitalize()}, vous êtes connecté(e) avec succès !", "success")
                return redirect(url_for('dashboard'))
        flash(
            "Désolé, le nom d'utilisateur ou le mot de passe ne correspond pas.", "danger")
    return render_template("login.html", login=True)

# Api
@app.route('/api')
@app.route('/api/v1')
def api():
    return """
    <h2>Liste des Api</h2>
    <ol>
        <li>
            <a href="/api/v1/carnetclient">Carnet des clients</a>
        </li>
        <li>
            <a href="/api/v1/carnetcomptes">Carnet des comptes</a>
        </li>
    </ol>
    """
    
@app.route('/carnetclient', methods=["GET", "POST"])
@app.route('/api/v1/carnetclient', methods=["GET", "POST"])
def carnetclient():
    if 'utilisateurs' not in session:
        flash("Veuillez vous connecter", "warning")
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette api", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            id_client = request.json['id_client']
            query = text("SELECT message_enregistrement, heure_sortir FROM carnet_client WHERE id_client = :id_client ORDER BY heure_sortir DESC")
            data = db.execute(query, {'id_client': id_client}).fetchone()
            if data:
                response_data = {
                    "message": data.message_enregistrement,
                    "date": data.heure_sortir
                }
                return jsonify(response_data)
            else:
                return jsonify({"message": "Aucune donnée trouvée pour cet ID de client."}), 404
        else:
            dict_data = []
            query = text("SELECT clients.id_client as id, clients.client_ssn_id as ssn_id, clients.nom, clients.statut, carnet_client.message_enregistrement as message, carnet_client.heure_sortir as date FROM carnet_client JOIN clients ON clients.id_client = carnet_client.id_client ORDER BY carnet_client.heure_sortir DESC LIMIT 50")
            data = db.execute(query).fetchall()
            for row in data:
                t = {
                    "id": row.id,
                    "ssn_id": row.ssn_id,
                    "message": row.message,
                    "date": row.date
                }
                dict_data.append(t)
            return jsonify(dict_data)


@app.route('/carnetcomptes', methods=["GET", "POST"])
@app.route('/api/v1/carnetcomptes', methods=["GET", "POST"])
def carnetcomptes():
    if 'utilisateurs' not in session:
        flash("Veuillez vous connecter", "warning")
        return redirect(url_for('login'))
    if session['user_type'] != "gestionnaire":
        flash("Vous n'avez pas accès à cette api", "warning")
        return redirect(url_for('dashboard'))
    if session['user_type'] == "gestionnaire":
        if request.method == "POST":
            id_compte = request.json['id_compte']
            query = text("SELECT statut, message, dernier_majour as heure_sortir FROM comptes WHERE id_compte = :id_compte;")
            data = db.execute(query, {'id_compte': id_compte}).fetchone()
            if data:
                response_data = {
                    "statut": data.statut,
                    "message": data.message,
                    "date": data.heure_sortir
                }
                return jsonify(response_data)
            else:
                return jsonify({"message": "Aucune donnée trouvée pour cet ID de compte."}), 404
        else:
            dict_data = []
            query = text("SELECT id_client, id_compte, type_de_compte, statut, message, dernier_majour FROM comptes LIMIT 50;")
            data = db.execute(query).fetchall()
            for row in data:
                t = {
                    "id_client": row.id_client,
                    "id_compte": row.id_compte,
                    "type_de_compte": row.type_de_compte,
                    "statut": row.statut,
                    "message": row.message,
                    "date": row.dernier_majour
                }
                dict_data.append(t)
            return jsonify(dict_data)
# Main
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)

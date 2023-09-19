# @app.route("/ajoutclient", methods=["GET", "POST"])
# def ajoutclient():
#     # recupere les pays api
#     recup_pays = requests.get('https://restcountries.com/v3.1/all', [])
#     liste_pays = recup_pays.json()
#     pays_nom = []
#     for i in liste_pays:
#         pays_nom.append(i['name']['common'])

#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             client_ssn_id = int(request.form.get("client_ssn_id"))
#             nom = str(request.form.get("nom"))
#             email = str(request.form.get("email"))
#             age = int(request.form.get("age"))
#             pays = str(request.form.get("pays"))
#             ville = str(request.form.get("ville"))
#             result = db.execute(
#                 "SELECT * from clients WHERE client_ssn_id = :c", {"c": client_ssn_id}).fetchone()
#             if result is None:
#                 result = db.query(Clients).count()
#                 if result == 0:
#                     query = Clients(id_client=110110000, client_ssn_id=client_ssn_id, nom=nom,
#                                     email=email, age=age, pays=pays, ville=ville, statut='activer')
#                 else:
#                     query = Clients(client_ssn_id=client_ssn_id, nom=nom, email=email,
#                                     age=age, pays=pays, ville=ville, statut='activer')
#                 # result = db.execute("INSERT INTO clients (client_ssn_id,nom,email,age,pays,ville) VALUES (:c,:n,:add,:a,:s,:ville)", {"c": client_ssn_id,"n":nom,"add":email,"a": age,"s":pays,"ville":ville})
#                 db.add(query)
#                 db.commit()
#                 if query.id_client is None:
#                     flash(
#                         "Les données ne sont pas insérées ! Vérifiez votre saisie.", "danger")
#                 else:
#                     temp = Carnet_client(id_client=query.id_client,
#                                          message_enregistrement="Client Créé")
#                     db.add(temp)
#                     db.commit()
#                     flash(
#                         f"Client {query.nom} est créé avec l'identifiant du client : {query.id_client}.", "success")
#                     return redirect(url_for('voirclient'))
#             flash(
#                 f'SSN id : {client_ssn_id} est déjà présent dans la base de données.', 'warning')

#     return render_template('ajoutclient.html', ajoutclient=True, pays=sorted(pays_nom))


# @app.route("/voirclient/<id_client>")
# @app.route("/voirclient", methods=["GET", "POST"])
# def voirclient(id_client=None):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             client_ssn_id = request.form.get('client_ssn_id')
#             id_client = request.form.get('id_client')
#             data = db.execute("SELECT * from clients WHERE id_client = :c or client_ssn_id = :d", {
#                               "c": id_client, "d": client_ssn_id}).fetchone()
#             if data is not None:
#                 return render_template('voirclient.html', voirclient=True, data=data)

#             flash("Client n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
#         elif id_client is not None:
#             data = db.execute(
#                 "SELECT * from clients WHERE id_client = :c", {"c": id_client}).fetchone()
#             if data is not None:
#                 return render_template('voirclient.html', voirclient=True, data=data)

#             flash("Client n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
#     else:
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))

#     return render_template('voirclient.html', voirclient=True)


# @app.route('/modifierclient')
# @app.route('/modifierclient/<id_client>', methods=["GET", "POST"])
# def modifierclient(id_client=None):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if id_client is not None:
#             if request.method != "POST":
#                 id_client = int(id_client)
#                 data = db.execute(
#                     "SELECT * from clients WHERE id_client = :c", {"c": id_client}).fetchone()
#                 if data is not None and data.statut != 'desactiver':
#                     return render_template('modifierclient.html', modifierclient=True, data=data)
#                 else:
#                     flash(
#                         'Le client est désactivé ou absent de la base de données.', 'warning')
#             else:
#                 id_client = int(id_client)
#                 nom = str(request.form.get("nom"))
#                 email = str(request.form.get("email"))
#                 age = int(request.form.get("age"))
#                 result = db.execute(
#                     "SELECT * from clients WHERE id_client = :c and statut='activer'", {"c": id_client}).fetchone()
#                 if result is not None:
#                     result = db.execute("UPDATE clients SET nom = :n , email = :add , age = :ag WHERE id_client = :a", {
#                                         "n": nom, "add": email, "ag": age, "a": id_client})
#                     db.commit()
#                     temp = Carnet_client(
#                         id_client=id_client, message_enregistrement="Mise à jour des données clients")
#                     db.add(temp)
#                     db.commit()
#                     flash(
#                         f"Les données des clients ont été mises à jour avec succès.", "success")
#                 else:
#                     flash(
#                         "Identité du client invalide. Veuillez vérifier l'identité du client.", 'warning')

#     return redirect(url_for('voirclient'))


# @app.route('/supprimerclient')
# @app.route('/supprimerclient/<id_client>')
# def supprimerclient(id_client):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if id_client is not None:
#             id_client = int(id_client)
#             result = db.execute(
#                 "SELECT * from clients WHERE id_client = :a and statut='activer'", {"a": id_client}).fetchone()
#             if result is not None:
#                 # delete from comptes WHERE id_compte = :a and type_de_compte=:at", {"a": id_compte,"at":type_de_compte}
#                 query = db.execute(
#                     "UPDATE clients SET statut='desactiver' WHERE id_client = :a", {"a": id_client})
#                 db.commit()
#                 temp = Carnet_client(
#                     id_client=id_client,  message_enregistrement="Client Désactivé")
#                 db.add(temp)
#                 db.commit()
#                 flash(f"Le Client est Desactiver.", "success")
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash(
#                     f"Client avec identifiant: {id_client} est déjà désactivé ou n'est pas présent dans la base de données.", 'warning')
#     return redirect(url_for('modifierclient'))


# @app.route('/activerclient')
# @app.route('/activerclient/<id_client>')
# def activerclient(id_client):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if id_client is not None:
#             id_client = int(id_client)
#             result = db.execute(
#                 "SELECT * from clients WHERE id_client = :a and statut='desactiver'", {"a": id_client}).fetchone()
#             if result is not None:
#                 query = db.execute(
#                     "UPDATE clients SET statut='activer' WHERE id_client = :a", {"a": id_client})
#                 db.commit()
#                 temp = Carnet_client(
#                     id_client=id_client,  message_enregistrement="Client Activer")
#                 db.add(temp)
#                 db.commit()
#                 flash(f"Le client est activé.", "success")
#                 return redirect(url_for('dashboard'))
#             flash(
#                 f"Client avec identifiant: {id_client} est déjà activé ou n'est pas présent dans la base de données.", 'warning')
#     return redirect(url_for('modifierclient'))


# @app.route('/activercompte')
# @app.route('/activercompte/<id_compte>')
# def activercompte(id_compte=None):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if id_compte is not None:
#             id_compte = int(id_compte)
#             result = db.execute(
#                 "SELECT * from comptes WHERE id_compte = :a and statut='desactiver'", {"a": id_compte}).fetchone()
#             if result is not None:
#                 date = datetime.datetime.now()
#                 query = db.execute("UPDATE comptes SET statut='activer', message='Le compte est réactivé', dernier_majour = :d WHERE id_compte = :a", {
#                                    "d": date, "a": id_compte})
#                 db.commit()
#                 flash(f"Le compte est activé.", "success")
#                 return redirect(url_for('dashboard'))
#             flash(
#                 f"Compte avec identifiant: {id_compte} est déjà activé ou n'est pas présent dans la base de données.", 'warning')
#     return redirect(url_for('voircompte'))


# @app.route('/statutclient')
# def statutclient():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         # requête pour obtenir un message de journal par identifiant de client
#         data = db.execute("SELECT clients.id_client as id, clients.client_ssn_id as ssn_id, clients.nom, clients.statut, carnet_client.message_enregistrement as message, carnet_client.heure_sortir as date from (select id_client, message_enregistrement,heure_sortir from carnet_client group by id_client ORDER by heure_sortir desc) as carnet_client JOIN clients ON clients.id_client = carnet_client.id_client group by carnet_client.id_client order by carnet_client.heure_sortir desc").fetchall()
#         if data:
#             return render_template('statutclient.html', statutclient=True, data=data)
#         else:
#             flash('Aucune donnée trouvée.', 'danger')
#     return redirect(url_for('dashboard'))


# @app.route("/ajoutcompte", methods=["GET", "POST"])
# def ajoutcompte():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             id_client = int(request.form.get("id_client"))
#             type_de_compte = request.form.get("type_de_compte")
#             montant = float(request.form.get("montant"))
#             message = "Compte créé avec succès"
#             result = db.execute(
#                 "SELECT * from clients WHERE id_client = :c", {"c": id_client}).fetchone()
#             if result is not None:
#                 result = db.execute("SELECT * from comptes WHERE id_client = :c and type_de_compte = :at", {
#                                     "c": id_client, "at": type_de_compte}).fetchone()
#                 if result is None:
#                     result = db.query(Comptes).count()
#                     if result == 0:
#                         query = Comptes(id_compte=360110000, type_de_compte=type_de_compte, balance=montant, id_client=id_client,
#                                         statut='activer', message=message, dernier_majour=datetime.datetime.now())
#                     else:
#                         query = Comptes(type_de_compte=type_de_compte, balance=montant, id_client=id_client,
#                                         statut='activer', message=message, dernier_majour=datetime.datetime.now())
#                     db.add(query)
#                     db.commit()
#                     if query.id_compte is None:
#                         flash(
#                             "Les données ne sont pas insérées ! Vérifiez votre saisie.", "danger")
#                     else:
#                         flash(
#                             f"Le compte {query.type_de_compte} est créé avec l'ID du client : {query.id_compte}.", "success")
#                         return redirect(url_for('dashboard'))
#                 else:
#                     flash(
#                         f'Client avec identifiant: {id_client} a déjà un compte {type_de_compte}.', 'warning')
#             else:
#                 flash(
#                     f"Client avec identifiant: {id_client} n'existe pas dans la base de données.", 'warning')
#     return render_template('ajoutcompte.html', ajoutcompte=True)


# @app.route("/supprimercompte", methods=["GET", "POST"])
# def supprimercompte():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             id_compte = int(request.form.get("id_compte"))
#             result = db.execute(
#                 "SELECT * from comptes WHERE id_compte = :a and statut='activer'", {"a": id_compte}).fetchone()
#             if result is not None:
#                 # delete from comptes WHERE id_compte = :a and type_de_compte=:at", {"a": id_compte,"at":type_de_compte}
#                 message = "Compte désactivé"
#                 date = datetime.datetime.now()
#                 query = db.execute("UPDATE comptes SET statut='desactiver', message= :m, dernier_majour = :d WHERE id_compte = :a;", {
#                                    "m": message, "d": date, "a": id_compte})
#                 db.commit()
#                 flash(f"Le compte client a été désactivé avec succès.", "success")
#                 return redirect(url_for('dashboard'))
#             flash(
#                 f"Compte avec identifiant: {id_compte} est déjà désactivé ou le compte n'est pas trouvé.", 'warning')
#     return render_template('supprimercompte.html', supprimercompte=True)


# @app.route("/voircompte", methods=["GET", "POST"])
# def voircompte():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire" or session['user_type'] == "caissier":
#         if request.method == "POST":
#             id_compte = request.form.get("id_compte")
#             id_client = request.form.get("id_client")
#             data = db.execute("SELECT * from comptes WHERE id_client = :c or id_compte = :d", {
#                               "c": id_client, "d": id_compte}).fetchone()
#             if data:
#                 return render_template('voircompte.html', voircompte=True, data=data)

#             flash(
#                 "Le compte n'a pas été trouvé ! Veuillez vérifier votre saisie.", 'danger')
#     else:
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     return render_template('voircompte.html', voircompte=True)


# @app.route("/voircomptestatut", methods=["GET", "POST"])
# def voircomptestatut():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         data = db.execute("select * from comptes").fetchall()
#         if data:
#             return render_template('voircomptestatut.html', voircomptestatut=True, data=data)
#         else:
#             flash("Les comptes sont introuvables !", 'danger')
#     return render_template('voircomptestatut.html', voircomptestatut=True)

# # Code pour le montant du dépôt


# @app.route('/depot', methods=['GET', 'POST'])
# @app.route('/depot/<id_compte>', methods=['GET', 'POST'])
# def depot(id_compte):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "caissier":
#         if id_compte is None:
#             return redirect(url_for('voircompte'))
#         else:
#             if request.method == "POST":
#                 montant = request.form.get("montant")
#                 data = db.execute(
#                     "select * from comptes where id_compte = :a and statut='activer'", {"a": id_compte}).fetchone()
#                 if data is not None:
#                     balance = int(montant) + int(data.balance)
#                     query = db.execute("UPDATE comptes SET balance= :b WHERE id_compte = :a", {
#                                        "b": balance, "a": data.id_compte})
#                     db.commit()
#                     flash(
#                         f"Montant {montant} F CFA déposé sur le compte: {data.id_compte} avec succès.", 'success')
#                     temp = Transactions(
#                         id_compte=data.id_compte, trans_message="Montant du dépôt", montant=montant)
#                     db.add(temp)
#                     db.commit()
#                 else:
#                     flash(f"Compte introuvable ou désactivé.", 'danger')
#             else:
#                 data = db.execute(
#                     "select * from comptes where id_compte = :a", {"a": id_compte}).fetchone()
#                 if data is not None:
#                     return render_template('depot.html', depot=True, data=data)
#                 else:
#                     flash(f"Compte introuvable ou désactivé.", 'danger')

#     return redirect(url_for('dashboard'))

# # Code pour le montant de retrait


# @app.route('/retrait', methods=['GET', 'POST'])
# @app.route('/retrait/<id_compte>', methods=['GET', 'POST'])
# def retrait(id_compte):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "caissier":
#         if id_compte is None:
#             return redirect(url_for('voircompte'))
#         else:
#             if request.method == "POST":
#                 montant = request.form.get("montant")
#                 data = db.execute(
#                     "select * from comptes where id_compte = :a and statut='activer'", {"a": id_compte}).fetchone()
#                 if data is not None:
#                     if int(data.balance) >= int(montant):
#                         balance = int(data.balance)-int(montant)
#                         query = db.execute("UPDATE comptes SET balance= :b WHERE id_compte = :a",
#                                            {"b": balance, "a": data.id_compte})
#                         db.commit()
#                         flash(
#                             f"{montant} F CFA prélevé sur le compte: {data.id_compte} avec succès.", 'success')
#                         temp = Transactions(
#                             id_compte=data.id_compte, trans_message="Montant prélevé", montant=montant)
#                         db.add(temp)
#                         db.commit()
#                     else:
#                         flash(f"Le solde du compte est insuffisant.", 'success')
#                         return redirect(url_for('voircompte'))
#                 else:
#                     flash(f"Compte introuvable ou désactivé.", 'danger')
#             else:
#                 data = db.execute(
#                     "select * from comptes where id_compte = :a", {"a": id_compte}).fetchone()
#                 if data is not None:
#                     return render_template('retrait.html', depot=True, data=data)
#                 else:
#                     flash(f"Compte introuvable ou désactivé.", 'danger')

#     return redirect(url_for('dashboard'))

# # Code pour le montant du transfertt


# @app.route('/transfert', methods=['GET', 'POST'])
# @app.route('/transfert/<id_client>', methods=['GET', 'POST'])
# def transfert(id_client=None):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "caissier":
#         if id_client is None:
#             return redirect(url_for('voircompte'))
#         else:
#             if request.method == 'POST':
#                 src_type = request.form.get("src_type")
#                 trg_type = request.form.get("trg_type")
#                 montant = int(request.form.get("montant"))
#                 if src_type != trg_type:
#                     src_data = db.execute("select * from comptes where id_client = :a and type_de_compte = :t and statut='activer'", {
#                                           "a": id_client, "t": src_type}).fetchone()
#                     trg_data = db.execute("select * from comptes where id_client = :a and type_de_compte = :t and statut='activer'", {
#                                           "a": id_client, "t": trg_type}).fetchone()
#                     if src_data is not None and trg_data is not None:
#                         if src_data.balance > montant:
#                             src_balance = src_data.balance - montant
#                             trg_balance = trg_data.balance + montant

#                             test = db.execute("update comptes set balance = :b where id_client = :a and type_de_compte = :t", {
#                                               "b": src_balance, "a": id_client, "t": src_type})
#                             db.commit()
#                             temp = Transactions(
#                                 id_compte=src_data.id_compte, trans_message="Montant transféré à "+str(trg_data.id_compte), montant=montant)
#                             db.add(temp)
#                             db.commit()

#                             db.execute("update comptes set balance = :b where id_client = :a and type_de_compte = :t", {
#                                        "b": trg_balance, "a": id_client, "t": trg_type})
#                             db.commit()
#                             temp = Transactions(
#                                 id_compte=trg_data.id_compte, trans_message="Montant reçu de " + str(src_data.id_compte), montant=montant)
#                             db.add(temp)
#                             db.commit()

#                             flash(
#                                 f"Montant {montant} F CFA transféré à {trg_data.id_compte} de {src_data.id_compte} avec succèes", 'success')
#                         else:
#                             flash("Montant insuffisant pour transférer.", "danger")

#                     else:
#                         flash("Comptes introuvables", "danger")

#                 else:
#                     flash(
#                         "Impossible de transférer le montant sur le même compte.", 'warning')

#             else:
#                 data = db.execute(
#                     "select * from comptes where id_client = :a", {"a": id_client}).fetchall()
#                 if data:
#                     return render_template('transfert.html', depot=True, id_client=id_client)
#                 else:
#                     flash("Données introuvables ou ID client invalide", 'danger')
#                     return redirect(url_for('voircompte'))

#     return redirect(url_for('dashboard'))

# # code pour visualiser l'état du compte basé sur l'identifiant du compte
# # en utilisant le numéro de la dernière transaction
# # ou
# # Utilisation de la durée de la date spécifiée


# @app.route("/declaration", methods=["GET", "POST"])
# def declaration():
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "caissier":
#         if request.method == "POST":
#             id_compte = request.form.get("id_compte")
#             number = request.form.get("number")
#             flag = request.form.get("Radio")
#             start_date = request.form.get("start_date")
#             end_date = request.form.get("end_date")
#             if flag == "red":
#                 # data = db.execute("SELECT * FROM (SELECT * FROM transactions where id_compte=:d ORDER BY trans_id DESC LIMIT :l)Var1 ORDER BY trans_id ASC;", {
#                 #                   "d": id_compte, "l": number}).fetchall()
#                 query = text("SELECT * FROM (SELECT * FROM transactions where id_compte=:id_compte ORDER BY trans_id DESC LIMIT :number)Var1 ORDER BY trans_id ASC;")
#                 data = db.execute(query, id_compte=id_compte, number=number).fetchall()
#             else:
#                 # data = db.execute("SELECT * FROM transactions WHERE id_compte=:a between DATE(heure_sortir) >= :s AND DATE(heure_sortir) <= :e;", {
#                 #                   "a": id_compte, "s": start_date, "e": end_date}).fetchall()
#                 query = text("SELECT * FROM transactions WHERE id_compte=:id_compte AND DATE(heure_sortir) BETWEEN :start_date AND :end_date;")
#                 data = db.execute(query, id_compte=id_compte, start_date=start_date, end_date=end_date).fetchall()
#             if data:
#                 return render_template('declaration.html', declaration=True, data=data, id_compte=id_compte)
#             else:
#                 flash("Aucune transaction", 'danger')
#                 return redirect(url_for('dashboard'))
#     else:
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     return render_template('declaration.html', declaration=True)

# # code for generate declaration PDF or Excel file


# @app.route('/declaration_pdf/<id_compte>')
# @app.route('/declaration_pdf/<id_compte>/<ftype>')
# def declaration_pdf(id_compte=None, ftype=None):
#     if 'utilisateurs' not in session:
#         return redirect(url_for('login'))
#     if session['user_type'] == "gestionnaire":
#         flash("Vous n'avez pas accès à cette page", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "caissier":
#         if id_compte is not None:
#             data = db.execute(
#                 "SELECT * FROM transactions WHERE id_compte=:a order by heure_sortir limit 20;", {"a": id_compte}).fetchall()
#             column_names = ['TransactionId', 'Description', 'Date', 'Montant']
#             if data:
#                 if ftype is None:  # Check for provide pdf file as default
#                     pdf = FPDF()
#                     pdf.add_page()

#                     page_width = pdf.w - 2 * pdf.l_margin

#                     # code for setting header
#                     pdf.set_font('Times', 'B', 16.0)
#                     pdf.cell(page_width, 0.0, "Siémisika-Bank", align='C')
#                     pdf.ln(10)

#                     # code for Showing account id
#                     msg = 'Relevé de compte : ' + str(id_compte)
#                     pdf.set_font('Times', '', 12.0)
#                     pdf.cell(page_width, 0.0, msg, align='C')
#                     pdf.ln(10)

#                     # code for Showing account id
#                     pdf.set_font('Times', 'B', 11)
#                     pdf.ln(1)

#                     th = pdf.font_size

#                     # code for table header
#                     pdf.cell(page_width/5, th, 'Transaction Id')
#                     pdf.cell(page_width/3, th, 'Description')
#                     pdf.cell(page_width/3, th, 'Date')
#                     pdf.cell(page_width/7, th, 'Montant')
#                     pdf.ln(th)

#                     pdf.set_font('Times', '', 11)

#                     # code for table row data
#                     for row in data:
#                         pdf.cell(page_width/5, th, str(row.trans_id))
#                         pdf.cell(page_width/3, th, row.trans_message)
#                         pdf.cell(page_width/3, th, str(row.heure_sortir))
#                         pdf.cell(page_width/7, th, str(row.montant))
#                         pdf.ln(th)

#                     pdf.ln(10)

#                     bal = db.execute("SELECT balance FROM comptes WHERE id_compte=:a;", {
#                                      "a": id_compte}).fetchone()

#                     pdf.set_font('Times', '', 10.0)
#                     msg = 'Solde actuel : ' + str(bal.balance) + ' F CFA'
#                     pdf.cell(page_width, 0.0, msg, align='C')
#                     pdf.ln(5)

#                     pdf.cell(page_width, 0.0,
#                              '-- Fin de la déclaration --', align='C')

#                     return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'inline;filename=declaration.pdf'})

#                 elif ftype == 'xl':  # Check for bulid and send Excel file for download

#                     output = io.BytesIO()
#                     # create WorkBook object
#                     workbook = xlwt.Workbook()
#                     # add a sheet
#                     sh = workbook.add_sheet('Extrait de compte')

#                     # add headers
#                     sh.write(0, 0, 'Transaction ID')
#                     sh.write(0, 1, 'Description')
#                     sh.write(0, 2, 'Date')
#                     sh.write(0, 3, 'Montant')

#                     # add row data into Excel file
#                     idx = 0
#                     for row in data:
#                         sh.write(idx+1, 0, str(row.trans_id))
#                         sh.write(idx+1, 1, row.trans_message)
#                         sh.write(idx+1, 2, str(row.heure_sortir))
#                         sh.write(idx+1, 3, str(row.montant))
#                         idx += 1

#                     workbook.save(output)
#                     output.seek(0)

#                     response = Response(output, mimetype="application/ms-excel", headers={
#                                         "Content-Disposition": "attachment;filename=declaration.xls"})
#                     return response
#             else:
#                 flash("ID de compte invalide", 'danger')
#         else:
#             flash("Veuillez indiquer l'ID du compte", 'warning')
#     return redirect(url_for('dashboard'))

# # route for 404 error


# @app.errorhandler(404)
# def not_found(e):
#     return render_template("404.html")

# # Logout


# @app.route("/logout")
# def logout():
#     session.pop('utilisateurs', None)
#     return redirect(url_for('login'))

# # LOGIN


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if 'utilisateurs' in session:
#         return redirect(url_for('dashboard'))

#     if request.method == "POST":
#         usern = request.form.get("username").upper()
#         passw = request.form.get("password").encode('utf-8')
#         result = db.execute(
#             "SELECT * FROM utilisateurs WHERE id = :u", {"u": usern}).fetchone()
#         print(result)
#         if result is not None:
#             if bcrypt.check_password_hash(result['mot_de_passe'], passw) is True:
#                 session['utilisateurs'] = usern
#                 session['nom'] = result.nom
#                 session['user_type'] = result.user_type
#                 flash(
#                     f"{result.nom.capitalize()}, vous êtes connecté(e) avec succès !", "success")
#                 return redirect(url_for('dashboard'))
#         flash(
#             "Désolé, le nom d'utilisateurs ou le mot de passe ne correspond pas.", "danger")
#     return render_template("login.html", login=True)

# # Api


# @app.route('/api')
# @app.route('/api/v1')
# def api():
#     return """
#     <h2>Liste des Api</h2>
#     <ol>
#         <li>
#             <a href="/api/v1/carnetclient">Carnet des clients</a>
#         </li>
#         <li>
#             <a href="/api/v1/carnetcomptes">Carnet des comptes</a>
#         </li>
#     </ol>
#     """

# # Api pour mettre à jour le journal d'un client particulier dans la table html onClick of refresh


# @app.route('/carnetclient', methods=["GET", "POST"])
# @app.route('/api/v1/carnetclient', methods=["GET", "POST"])
# def carnetclient():
#     if 'utilisateurs' not in session:
#         flash("Veuillez vous connecter", "warning")
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette api", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             id_client = request.json['id_client']
#             data = db.execute("select  message_enregistrement,heure_sortir from carnet_client where id_client= :c ORDER by heure_sortir desc", {
#                               'c': id_client}).fetchone()
#             t = {
#                 "message": data.message_enregistrement,
#                 "date": data.heure_sortir
#             }
#             return jsonify(t)
#         else:
#             dict_data = []
#             data = db.execute("SELECT clients.id_client as id, clients.client_ssn_id as ssn_id,clients.nom, clients.statut, carnet_client. message_enregistrement as message, carnet_client.heure_sortir as date from carnet_client JOIN clients ON clients.id_client = carnet_client.id_client order by carnet_client.heure_sortir desc limit 50").fetchall()
#             for row in data:
#                 t = {
#                     "id": row.id,
#                     "ssn_id": row.ssn_id,
#                     "message": row.message,
#                     "date": row.date
#                 }
#                 dict_data.append(t)
#             return jsonify(dict_data)

# # Api pour la mise à jour d'un journal de compte particulier dans un tableau html lors d'un clic de rafraîchissement


# @app.route('/carnetcomptes', methods=["GET", "POST"])
# @app.route('/api/v1/carnetcomptes', methods=["GET", "POST"])
# def carnetcomptes():
#     if 'utilisateurs' not in session:
#         flash("Veuillez vous connecter", "warning")
#         return redirect(url_for('login'))
#     if session['user_type'] != "gestionnaire":
#         flash("Vous n'avez pas accès à cette api", "warning")
#         return redirect(url_for('dashboard'))
#     if session['user_type'] == "gestionnaire":
#         if request.method == "POST":
#             id_compte = request.json['id_compte']
#             data = db.execute("select statut,message,dernier_majour as heure_sortir from comptes where id_compte= :c;", {
#                               'c': id_compte}).fetchone()
#             t = {
#                 "statut": data.statut,
#                 "message": data.message,
#                 "date": data.heure_sortir
#             }
#             return jsonify(t)
#         else:
#             dict_data = []
#             data = db.execute(
#                 "SELECT id_client, id_compte, type_de_compte, statut, message, dernier_majour from comptes limit 50").fetchall()
#             for row in data:
#                 t = {
#                     "id_client": row.id_client,
#                     "id_compte": row.id_compte,
#                     "type_de_compte": row.type_de_compte,
#                     "statut": row.statut,
#                     "message": row.message,
#                     "date": row.dernier_majour
#                 }
#                 dict_data.append(t)
#             return jsonify(dict_data)

############################
###########################
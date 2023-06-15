from flask import Flask, request,render_template, jsonify,redirect,send_file, url_for,flash,make_response
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import sys
import mysql.connector
from fpdf import FPDF
import json
from http import client
import pdfkit


# Define the Stagiaire class
app = Flask(__name__, template_folder='templates')




app.secret_key = 'many random bytes'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data'

mysql = MySQL(app)

class Stagiaire:
        def __init__(self, id, CIN, nom, prenom, age,date_debut,date_fin,annee, email, tel,etablissement):
            self.CIN = CIN
            self.id = id
            self.nom = nom
            self.prenom = prenom
            self.age = age
            self.email = email
            self.tel = tel
            self.date_debut = date_debut
            self.date_fin = date_fin
            self.annee = annee
            self.etablissement=etablissement
class Stagiare_encours:
        def __init__(self, CIN,id, nom, prenom, age, email,date_debut,date_fin,annee, tel, encadrant,etablissement):
            self.CIN = CIN
            self.nom = nom
            self.prenom = prenom
            self.age = age
            self.email = email
            self.tel = tel
            self.encadrant=encadrant
            self.etablissement=etablissement
            self.date_debut = date_debut
            self.date_fin = date_fin
            self.annee = annee
           




@app.route('/')
def home():
    return render_template('main.html')

#multipule page handling
@app.route('/<page_name>')
def redirect_page(page_name):
    if page_name == 'index':
        return render_template('redirect.html')
    elif page_name=='acceuil':
        return render_template('main.html')
    elif page_name=='dea':
        return render_template('dea.html')
    elif page_name=='dr':
        return render_template('dr.html')
    elif page_name=='as':
        return render_template('as.html')
    elif page_name=='lds':
        return render_template('lds.html')
    elif page_name=='astage':
        return render_template('astage.html')
    elif page_name=='ch_stage':
        return render_template('ch_stage.html')
    elif page_name=='ch_stagaire':
        return render_template('suces.html')
    elif page_name=='stats':
        return render_template('stats.html')
    return render_template('redirect.html')
#it doesn't work 
@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stagiaire')
    data = cur.fetchall()
    return render_template('lds.html', stagiaire=data)
#for fetching data from the db
@app.route('/data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stagiaire')
    data = cur.fetchall()
    # Convert the data to a list of dictionaries
    result = []
    for row in data:
        result.append({ 'CIN': row[0], 'nom': row[2] , 'prenom':row[3],'age':row[4] , 'email':row[5],'tel':row[6], 'date_debut':row[7],'date_fin':row[8],'annee':row[9],'etablissement':row[10]})
    return jsonify({'stagiaire': result})





@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        # Get form data from the request object
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        email = request.form['email']
        tel = request.form['tel']
        CIN = request.form['cin']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        annee = request.form['annee']
        etablissement = request.form['etablissement']

        # Execute the SQL query
        query = "UPDATE stagiaire SET nom=%s, prenom=%s, age=%s, email=%s, tel=%s, date_debut=%s, date_fin=%s, annee=%s, etablissement=%s WHERE CIN=%s"
        values = (nom, prenom, age, email, tel, date_debut, date_fin, annee, etablissement, CIN)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        # Flash a success message and redirect to the updated page
        flash('Stagiaire updated successfully')
        return render_template('lds.html')

    
@app.route('/delete', methods=['POST'])
def delete_stagiaire():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        CIN = request.form['cin']
        cur.execute('DELETE FROM stagiaire WHERE CIN = %s', [CIN])
        mysql.connection.commit()
        cur.close()
        return render_template("lds.html")


@app.route('/add_stagiaire', methods=['GET', 'POST'])
def add_stagiaire():
    if request.method == 'POST':
        # Get form data from the request object
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        email = request.form['email']
        tel = request.form['tel']
        CIN = request.form[ 'cin']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        annee = request.form['annee']
        etablissement = request.form['etablissement']

        # Create a new Stagiaire object
        new_stagiaire = Stagiaire(id=None, nom=nom, prenom=prenom, age=age, email=email, tel=tel, CIN=CIN,
                                  date_debut=date_debut, date_fin=date_fin, annee=annee, etablissement=etablissement)

        # Insert the new Stagiaire into the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO `stagiaire` (nom, prenom, age, email, tel, CIN, date_debut, date_fin, annee, etablissement) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (new_stagiaire.nom, new_stagiaire.prenom, new_stagiaire.age, new_stagiaire.email, new_stagiaire.tel,
                  new_stagiaire.CIN, new_stagiaire.date_debut, new_stagiaire.date_fin, new_stagiaire.annee,
                  new_stagiaire.etablissement)
        cur.execute(query, values)
        mysql.connection.commit()

        # Close the connection
        cur.close()

    return render_template('lds.html')

@app.route('/add_stage', methods=['GET', 'POST'])
def add_stage():
    if request.method == 'POST':
        # Get form data from the request object
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        email = request.form['email']
        tel = request.form['tel']
        CIN = request.form[ 'cin']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        annee = request.form['annee']
        encadrant=request.form['encadrant']
        etablissement = request.form['etablissement']

        # Create a new Stagiaire object
        new_stage = Stagiare_encours(id=None, nom=nom, prenom=prenom, age=age, email=email, tel=tel, CIN=CIN,
                                  date_debut=date_debut, date_fin=date_fin, annee=annee, etablissement=etablissement,encadrant=encadrant)

        # Insert the new Stagiaire into the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO `stagiaire_encours` (nom, prenom, age, email, tel, CIN, date_debut, date_fin, annee,encadrant ,etablissement) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        values = (new_stage.nom, new_stage.prenom, new_stage.age, new_stage.email, new_stage.tel,
                  new_stage.CIN, new_stage.date_debut, new_stage.date_fin, new_stage.annee,
                  new_stage.etablissement,new_stage.encadrant)
        cur.execute(query, values)
        mysql.connection.commit()

        # Close the connection
        cur.close()

    return render_template('redirect.html')
#fetching 
@app.route('/', methods=['GET'])
def dex():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stagiaire_encours ')
    s7data = cur.fetchall()
    return render_template('redirect.html', stagiaire=s7data)
    
#fetching returns a json 
@app.route('/sdata', methods=['GET'])
def get_sdata():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stagiaire_encours')
    sdata = cur.fetchall()
    cur.close()

    # Convert the data to a list of dictionaries
    result = []
    for row in sdata:
        result.append({ 'CIN': row[0], 'nom': row[2] , 'prenom':row[3],'age':row[4] , 'email':row[5],'date_debut':row[6], 'date_fin':row[7],'annee':row[8],'tel':row[9],'encadrant':row[10],'etablissement':row[11]})
    return jsonify({'stagiaire': result})


   
@app.route('/supdate', methods=['POST'])
def supdate():
    if request.method == 'POST':
        # Get form data from the request object
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        email = request.form['email']
        tel = request.form['tel']
        CIN = request.form['cin']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        annee = request.form['annee']
        encadrant=request.form['encadrant']
        etablissement = request.form['etablissement']

        # Execute the SQL query
        query = "UPDATE stagiaire_encours SET nom=%s, prenom=%s, age=%s, email=%s, tel=%s, date_debut=%s, date_fin=%s, annee=%s, encadrant=%s, etablissement=%s WHERE CIN=%s"
        values = (nom, prenom, age, email, tel, date_debut, date_fin, annee,encadrant, etablissement, CIN)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        # Flash a success message and redirect to the updated page
        flash('Stagiaire updated successfully')
        return render_template('redirect.html')
@app.route('/sdelete', methods=['POST'])
def delete_stage():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        CIN = request.form['cin']
        cur.execute('DELETE FROM stagiaire_encours WHERE CIN = %s', [CIN])
        mysql.connection.commit()
        cur.close()
        return render_template("redirect.html")
    



@app.route('/chart', methods=['GET'])
def chart():
    cur = mysql.connection.cursor()
    
    # Count the number of 'stagiare_encours'
    cur.execute('SELECT COUNT(*) FROM stagiaire_encours')
    encours_count = cur.fetchone()[0]

    # Count the number of 'stagiare'
    cur.execute('SELECT COUNT(*) FROM stagiaire')
    stagiare_count = cur.fetchone()[0]

    cur.close()

    # Create a dictionary with the counts
    data = {
       'Stagiare': stagiare_count if stagiare_count is not None else 0,
        'Stagiare en cours': encours_count if encours_count is not None else 0,
    }

    # Return the counts as JSON response
    return jsonify(data)



@app.route('/evolution-data', methods=['GET'])
def get_evolution_data():
    cur = mysql.connection.cursor()

    # Retrieve the year and month from date_debut for stagiaires
    cur.execute("SELECT YEAR(date_debut), MONTH(date_debut), COUNT(*) FROM stagiaire_encours GROUP BY YEAR(date_debut), MONTH(date_debut)")
    stagiaires_data = cur.fetchall()

    # Retrieve the year and month from date_debut for stagiaires en cours
    cur.execute("SELECT YEAR(date_debut), MONTH(date_debut), COUNT(*) FROM stagiaire GROUP BY YEAR(date_debut), MONTH(date_debut)")
    en_cours_data = cur.fetchall()

    cur.close()

    # Format the data into separate lists of labels (months) and counts
    labels = []
    stagiaires_counts = []
    en_cours_counts = []

    for row in stagiaires_data:
        year = row[0]
        month = row[1]
        label = f"{month}/{year}"
        labels.append(label)
        stagiaires_counts.append(row[2])

    for row in en_cours_data:
        en_cours_counts.append(row[2])

    # Prepare the data to be sent as a JSON response
    data = {
        'labels': labels,
        'stagiaires': stagiaires_counts,
        'enCours': en_cours_counts
    }

    return jsonify(data)

@app.route('/etablissement-data', methods=['GET'])
def get_etablissement_data():
    cur = mysql.connection.cursor()

    # Retrieve the etablissements and their counts
    cur.execute('SELECT etablissement, COUNT(*) FROM stagiaire_encours GROUP BY etablissement')
    etablissement_data = cur.fetchall()

    cur.close()

    # Format the data into separate lists of etablissements and counts
    etablissements = []
    counts = []

    for row in etablissement_data:
        etablissements.append(row[0])
        counts.append(row[1])

    # Prepare the data to be sent as a JSON response
    data = {
        'etablissements': etablissements,
        'counts': counts
    }

    return jsonify(data)

@app.route('/generate-attestation', methods=['POST'])
def generate_attestation():
    CIN = request.json['searchText']  # Assuming the CIN is sent in the JSON request body
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM stagiaire_encours WHERE CIN = %s', [CIN])
    stagiaire = cur.fetchall()
    cur.close()

    if not stagiaire:
        return jsonify({'error': 'Stagiaire not found'})

    pdf_filename = 'attestation.pdf'  # Provide the desired filename for the generated PDF

    # Prepare the content based on stagiaire details
    content = []
    for row in stagiaire:
        content.append("                                                Attestation de stage en entreprise")
        content.append("")
        line = f" {row[2]}"
        linep = f" {row[3]}"
        ecole=f"{row[11]}"
        dated=f"{row[6]}"
        datef=f"{row[7]}"
        content.append(f"Je soussigné(e) Monsieur certifie par la présente que Monsieur {line} {linep},etudiant à ")
        content.append(f"{ecole} a effectué un stage au sein de notre entreprise du {dated} au {datef} ")
        content.append("Cette attestation est délivrée à l'intéressé(e) pour servir et valoir ce que de droit.")
        content.append("")
        content.append("Fait le :")
        content.append("")
        content.append("Signature :")
        content.append("")
        content.append("")

        content.append("Cachet de l'entreprise")

        # Include other stagiaire details as needed

    # Generate the PDF using the provided data
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    for line in content:
        pdf.cell(0, 14, txt=line.encode('latin-1', 'replace').decode('latin-1'), ln=True)  # Encode and decode using latin-1
    pdf.output(pdf_filename)

    # Send the PDF file as a response
    return send_file(pdf_filename, as_attachment=True)

@app.route('/affecter', methods=['GET', 'POST'])
def affecter():
    if request.method == 'POST':
        CIN = request.form['cin']
        encadrant = request.form['encadrant']

        # Retrieve stagiaire data from the database based on CIN
        cur = mysql.connection.cursor()
        query = "SELECT nom, prenom, age, email, tel, date_debut, date_fin, annee, etablissement FROM stagiaire WHERE CIN = %s"
        cur.execute(query, (CIN,))
        stagiaire_data = cur.fetchone()

        if stagiaire_data:
            # Create a new Stagiaire_encours object
            new_stage = Stagiare_encours(id=None, nom=stagiaire_data[0], prenom=stagiaire_data[1],
                                          age=stagiaire_data[2], email=stagiaire_data[3], tel=stagiaire_data[4],
                                          CIN=CIN, date_debut=stagiaire_data[5], date_fin=stagiaire_data[6],
                                          annee=stagiaire_data[7], encadrant=encadrant, etablissement=stagiaire_data[8])

            # Insert the new Stagiaire_encours into the database
            cur = mysql.connection.cursor()
            query_insert = "INSERT INTO `stagiaire_encours` (nom, prenom, age, email, tel, CIN, date_debut, date_fin, annee, encadrant, etablissement) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (new_stage.nom, new_stage.prenom, new_stage.age, new_stage.email, new_stage.tel,
                      new_stage.CIN, new_stage.date_debut, new_stage.date_fin, new_stage.annee,
                      new_stage.encadrant, new_stage.etablissement)
            cur.execute(query_insert, values)

            # Delete the stagiaire from the `stagiaire` table
            query_delete = "DELETE FROM stagiaire WHERE CIN = %s"
            cur.execute(query_delete, (CIN,))

            mysql.connection.commit()
            cur.close()

            return render_template('redirect.html')
        else:
            return "Stagiaire not found"









    

if __name__ == '__main__':
    app.run(debug=True)



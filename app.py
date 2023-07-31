from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt






# ================ les configurations app =============== #

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'lavieestainsi'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///La_Table.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# =========== les classes =========== #
# Modèle Utilisateur
class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(40), nullable=False)
    prenom = db.Column(db.String(60), nullable=False)
    Nom_utilisateur = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Utilisateur:{self.Nom} : {self.prenom} : {self.Nom_utilisateur} Email: {self.email} : {self.mot_de_passe}'
# Créer un modèle pour stocker les informations des réservations
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    heure = db.Column(db.String(50), nullable=False)
    personnes = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'Reservation:{self.nom} :  {self.email} : {self.telephone} : {self.date} : {self.heure} : {self.personnes} : {self.message}'
# Créer un modèle pour stocker les informations du formulaire
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
# =========== les routes =========== 

# Modèle Utilisateur
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('inscription'))

# Route Accueil
@app.route('/')
@app.route('/accueil')
def accueil():
    return render_template('Accueil.html', title='Accueil')

@app.route('/apropos')
def apropos():
    return render_template('Apropos.html',title='A_propos')


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Sauvegarder les informations du formulaire dans la base de données
    form_data = FormData(name=name, email=email, subject=subject, message=message)
    db.session.add(form_data)
    db.session.commit()

    return render_template('thank_you.html')


@app.route('/reservation', methods=['POST'])
def reservation():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form['telephone']
        date = request.form['date']
        heure = request.form['heure']
        personnes = int(request.form['personnes'])
        message = request.form['message']

        # Sauvegarder les informations de réservation dans la base de données
        reservation = Reservation(nom=nom, email=email, telephone=telephone, date=date, heure=heure, personnes=personnes, message=message)
        db.session.add(reservation)
        db.session.commit()

        # Variables SMTP
        smtp_server = 'smtp.gmail.com'  # Serveur SMTP de Gmail (changez-le si vous utilisez un autre fournisseur)
        smtp_port = 587  # Port du serveur SMTP (changez-le si nécessaire)
        smtp_username = os.environ.get('SMTP_USERNAME')  # Adresse e-mail pour l'authentification SMTP
        smtp_password = os.environ.get('SMTP_PASSWORD')  # Mot de passe pour l'authentification SMTP
    
        # Adresse e-mail de l'expéditeur et du destinataire
        sender_email = 'verlainejim98@gmail.com'
        receiver_email = email

        # Création du message au format HTML
        subject = 'Confirmation de réservation'
        body = f'''
        <p>Bonjour {nom},</p>
        <p>Merci pour votre réservation. Voici les détails :</p>
        <p>Date : {date}</p>
        <p>Heure : {heure}</p>
        <p>Nombre de personnes : {personnes}</p>
        <p>Message : {message}</p>
        <p>Nous vous attendons avec impatience !</p>
        <p>Cordialement,</p>
        <p>L'équipe de votre restaurant</p>
        '''

        # Création de l'objet du message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Ajout du corps du message au format HTML
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP et envoi de l'e-mail
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("E-mail envoyé avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")

        # Rediriger l'utilisateur vers une page de confirmation après la soumission du formulaire.
        return render_template('confirmation.html')

    # Si la méthode de requête n'est pas POST, redirigez l'utilisateur vers la page d'accueil avec le formulaire.
    return render_template('reservation.html', title='Reservation')


        # Envoyer l'e-mail réussi
            #  flash('Votre réservation a été effectuée avec succès!', 'success')
    # except Exception as e:
        # Erreur lors de l'envoi de l'e-mail
            #  flash('Désolé, une erreur s\'est produite lors de la réservation de la table. Veuillez réessayer plus tard.', 'error')

    return redirect(url_for('route_for_the_form_page'))


if __name__ == '__main__':
    app.run(debug=True)
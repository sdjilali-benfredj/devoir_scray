from redmail import EmailSender

email = EmailSender(host="0.0.0.0", port=5000)

def envoie():
    email.send(
        subject="Une connexion à MongoDB à été faite",
        sender="sharkserberus@gmail.com",
        receivers=['first.last@example.com'],
        text="Une connexion à MongoDB à été faite",
        html="<h1>Une connexion à MongoDB à été faite</h1>"
    )
    return True
#=========================================================================
    
import logging
import os
import socket
from datetime import datetime

# Configurez le niveau de journalisation
log_file_path = 'logs/app.log'

# Vérifiez si le dossier 'logs' existe, sinon, créez-le
log_folder = os.path.dirname(log_file_path)
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Vérifiez si le fichier journal existe, sinon, créez-le
if not os.path.isfile(log_file_path):
    with open(log_file_path, 'w'):
        pass  # Créez simplement le fichier vide

# Configurez le niveau de journalisation et le format des messages
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(hostname)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file_path, 'a'), logging.StreamHandler()])

# Ajoutez un filtre pour inclure l'adresse de l'hôte dans les messages
class HostnameFilter(logging.Filter):
    def filter(self, record):
        record.hostname = socket.gethostname()
        return True

# Ajoutez le filtre au logger
logger = logging.getLogger()
logger.addFilter(HostnameFilter())

#==============================================================================

from flask import Flask, render_template
from pymongo import MongoClient
import subprocess
from waitress import serve 


app = Flask(__name__)

# Connexion à MongoDB (remplacez les paramètres par les vôtres)
client = MongoClient('mongodb://localhost:27017')
db = client['quotes_database']
logging.info('===========================Connexion à MongoDB===========================')

envoie()





@app.route('/')
def index():
    # Récupérer une citation aléatoire depuis MongoDB
    random_quote = db.quotes.aggregate([{ '$sample': { 'size': 1 } }]).next()
    logging.info('===========================Récupération une citation aléatoire depuis MongoDB===========================')
    return render_template('index.html', quote=random_quote)

@app.route('/SurMaRoute')
def run_spider():
    try:
        # Exécuter la commande Scrapy
        subprocess.run(['scrapy', 'crawl', 'quotes'], check=True)
        logging.info('===========================Exécuter la commande Scrapy===========================')
        return "Spider exécuté avec succès."
    except subprocess.CalledProcessError:
        logging.error("===========================Erreur lors de l'exécution du Spider===========================")
        return "Erreur lors de l'exécution du Spider."

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)




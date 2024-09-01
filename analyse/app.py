import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import io
import base64
from flask import Flask, render_template, request
import matplotlib
import mplcursors

# Utilisation du backend non-interactif pour éviter les erreurs GUI
matplotlib.use('Agg')

app = Flask(__name__)

def load_data():
    file_path = 'C:/Users/MSI/Desktop/analyse/phosphate2.xlsx'
    data = pd.read_excel(file_path)
    
    # Mapping des noms de mois en français à l'anglais
    month_translation = {
        'janv.': 'Jan',
        'févr.': 'Feb',
        'mars': 'Mar',
        'avr.': 'Apr',
        'mai': 'May',
        'juin': 'Jun',
        'juil.': 'Jul',
        'août': 'Aug',
        'sept.': 'Sep',
        'oct.': 'Oct',
        'nov.': 'Nov',
        'déc.': 'Dec'
    }
    
    # Remplacer les noms des mois en français par anglais
    data['Mois'] = data['Mois'].replace(month_translation, regex=True)
    
    # Convertir la colonne 'Mois' en datetime
    data['Mois'] = pd.to_datetime(data['Mois'], format='%b %Y')
    
    # Traitement des autres colonnes
    data['Prix'] = data['Prix'].str.replace(',', '.').str.strip().astype(float)
    data['Variation en Pourcentage'] = data['Variation en Pourcentage'].replace('-', '0').str.replace('%', '').str.replace(',', '.').str.strip().astype(float)
    
    return data

def plot_graph(data, years):
    start_date = pd.to_datetime('today') - pd.DateOffset(years=years)
    filtered_data = data[data['Mois'] >= start_date]
    
    plt.figure(figsize=(10, 6))
    line, = plt.plot(filtered_data['Mois'], filtered_data['Prix'], marker='o', linestyle='-')
    plt.title(f'Prix des phosphates ({years} dernières années)')
    plt.xlabel('Date')
    plt.ylabel('Prix')
    plt.grid(True)

    # Ajouter des annotations avec mplcursors
    mplcursors.cursor(line, hover=True).connect("add", lambda sel: sel.annotation.set_text(f'Prix: {filtered_data["Prix"].iloc[sel.index]:.2f}'))

    # Formater l'axe x pour afficher les dates
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()
    
    # Sauvegarder le graphique dans un objet BytesIO et convertir en base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    plt.close()
    return plot_url

def plot_prediction_graph(data, prediction_type):
    plt.figure(figsize=(10, 6))
    
    if prediction_type == 'short':
        start_date = pd.to_datetime('today') - pd.DateOffset(months=6)
        recent_data = data[data['Mois'] >= start_date]
        plt.plot(recent_data['Mois'], recent_data['Prix'], marker='o', linestyle='-')
        plt.title('Prévision à court terme')
    
    elif prediction_type == 'long':
        start_date = pd.to_datetime('today') - pd.DateOffset(months=12)
        recent_data = data[data['Mois'] >= start_date]
        plt.plot(recent_data['Mois'], recent_data['Prix'], marker='o', linestyle='-')
        plt.title('Prévision à long terme')
    
    plt.xlabel('Date')
    plt.ylabel('Prix')
    plt.grid(True)
    
    # Formater l'axe x pour afficher les dates
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()
    
    # Sauvegarder le graphique dans un objet BytesIO et convertir en base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    plt.close()
    return plot_url

@app.route('/', methods=['GET'])
def index():
    data = load_data()
    years = int(request.args.get('years', 5))
    
    plot_url = plot_graph(data, years)
    short_term_prediction = predict_short_term(data)
    long_term_prediction = predict_long_term(data)
    
    return render_template('index.html', plot_url=plot_url, years=years,
                           short_term_prediction=short_term_prediction,
                           long_term_prediction=long_term_prediction)

@app.route('/prediction/<type>', methods=['GET'])
def prediction(type):
    data = load_data()
    plot_url = plot_prediction_graph(data, type)
    title = 'Prévision à court terme' if type == 'short' else 'Prévision à long terme'
    return {'plot_url': plot_url}

def predict_short_term(data):
    # Placeholder: Moyenne mobile simple pour les 6 derniers mois
    recent_data = data[data['Mois'] >= pd.to_datetime('today') - pd.DateOffset(months=6)]
    avg_price = recent_data['Prix'].mean()
    return avg_price

def predict_long_term(data):
    # Placeholder: Moyenne mobile simple pour les 12 derniers mois
    recent_data = data[data['Mois'] >= pd.to_datetime('today') - pd.DateOffset(months=12)]
    avg_price = recent_data['Prix'].mean()
    return avg_price

if __name__ == '__main__':
    app.run(debug=True)

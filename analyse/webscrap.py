from bs4 import BeautifulSoup
import pandas as pd

# Chemin vers le fichier HTML
file_path = 'C:/Users/MSI/Desktop/analyse/phosphate-360.xls'

# Lire le contenu du fichier HTML
with open(file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Trouver la table dans le HTML
table = soup.find('table', {'id': 'gvPrices'})

# Extraire les en-têtes
headers = [header.get_text(strip=True) for header in table.find_all('th')]

# Extraire les lignes de la table
rows = []
for row in table.find_all('tr')[1:]:  # Skip header row
    cols = [col.get_text(strip=True) for col in row.find_all('td')]
    rows.append(cols)

# Créer un DataFrame Pandas
df = pd.DataFrame(rows, columns=headers)

# Enregistrer le DataFrame en tant que fichier Excel
output_file =  'C:/Users/MSI/Desktop/analyse/phosphate2.xlsx'
df.to_excel(output_file, index=False)

print("Les données ont été extraites et enregistrées dans un fichier Excel.")

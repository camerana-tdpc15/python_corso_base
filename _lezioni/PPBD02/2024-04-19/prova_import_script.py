import os
from converti_nomi_nascita_univeral import converti_file

# Ottiene il percorso assoluto dello script corrente
script_path = os.path.abspath(__file__)

# Ottiene la directory in cui risiede lo script
script_dir = os.path.dirname(script_path)

# Costruisce un percorso assoluto al file di input
input_path = os.path.join(script_dir, 'input.txt')
output_path = os.path.join(script_dir, 'output.csv')

converti_file(input_path, output_path)

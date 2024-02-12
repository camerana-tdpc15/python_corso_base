import os
import sys
from pathlib import Path
try:
    from bs4 import BeautifulSoup
except ImportError:
    print('Questo script richiede la libreria BeautifulSoup.')
    print('Installala tramite il comando: pip install beautifulsoup4')
    sys.exit(1)
try:
    from nbconvert import SlidesExporter
except ImportError:
    print('Questo script richiede la libreria nbconvert.')
    print('Installala tramite il comando: pip install nbconvert')
    sys.exit(1)

# Lista dei notebook disponibili per la conversione in slide HTML.
NOTEBOOKS = [
    '00_prerequisiti.ipynb',
    '01_programmazione.ipynb',
    '02_python_intro.ipynb',
    '03_ide_setup.ipynb',
    '04_python_base.ipynb',
    '05_python_flow_control.ipynb',
    '06_python_environment.ipynb',
]

# Prima sistemiamo i percorsi per rendere più versatile e semplce l'uso dello script...

# Ottiene innanzitutto il percorso assoluto del file di questo script.
script_path = os.path.abspath(__file__)

# Dato che la struttura del repository è determinata, e dato che questo script
# è all'interno della stessa cartella in cui devono essere salvate le slide al
# termine del processo di conversione, ottiene il percorso assoluto della
# directory in cui si trova lo script e dunque anche le slide.
slides_dir = os.path.dirname(script_path)

# I notebook originali sono nella cartella superiore a quella delle slide.
notebooks_path = os.path.join(slides_dir, '../')


# Funzione per aggiornare i percorsi relativi nei file HTML perché per esempio
# le immagini sono nella cartella "imgs" che si trova al livello superiore.
# Quindi per esempio "./imgs/immagine.png" deve diventare "../imgs/immagine.png".
def update_html_paths(file_path):
    # Legge il contenuto del file HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Esegue il parsing del contenuto HTML e ottiene l'oggetto BeautifulSoup.
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Per ogni tag che ha l'attributo "src"
    for tag in soup.find_all(src=True):
        # Se il percorso inizia con "./"
        if tag['src'].startswith('./'):
            # Lo sostituisce con "../"
            tag['src'] = tag['src'].replace('./', '../')

    # Stessa cosa per gli attributi "href"
    for tag in soup.find_all(href=True):
        if tag['href'].startswith('./'):
            tag['href'] = tag['href'].replace('./', '../')

    # Sovrascrive il file HTML con i percorsi aggiornati.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

# Funzione per convertire i notebook in slide HTML e subito dopo aggiornarne i
# percorsi relativi.
def convert_notebooks(notebooks):
    # Crea l'oggetto per la conversione in slide HTML e ne imposta le opzioni...
    exporter = SlidesExporter()
    # Imposta la directory in cui si trovano i template per la conversione.
    # ATTENZIONE: Questa directory non è inclusa nel repository, ma non è altro
    #             che una cartella che contiene una copia del template di default
    #             "reveal_wide" con alcune modifiche per adattarlo al tema scuro
    #             e regolarne la larghezza.
    exporter.extra_template_basedirs = [os.path.join(notebooks_path, '../reveal_templates')]
    exporter.template_name = 'reveal_wide'
    # Imposta il tema scuro.
    exporter.reveal_theme = 'black'
    exporter.theme = 'dark'
    # Imposta il livello di log.
    exporter.log_level = 'DEBUG'

    # Converte in slide HTML e corregge ciascun notebook della lista...
    for nb in notebooks:
        # Esegue la conversione in slide HTML.
        output, resources = exporter.from_filename(os.path.join(notebooks_path, nb))
        # Genera il percorso del file HTML di output.
        output_file = Path(slides_dir, Path(nb).stem+'.html')
        # Scrive il file HTML di output.
        with open(output_file, 'w') as f:
            f.write(output)

        # Aggiorna i percorsi relativi nel file HTML.
        update_html_paths(output_file)
        # Stampa un messaggio che indica quale notebook è stato convertito.
        print(f'Conversione e correzione di: {nb}')


# Se viene eseguito come script, esegue la chiamata alla funzione principale,
# che esegue a sua volta la conversione in slide e la correzione dei percorsi
# dei notebook.
if __name__ == '__main__':
    # Se non sono stati passati parametri, esegue la conversione per tutti i
    # notebook presenti nella lista di default NOTEBOOKS.
    if len(sys.argv) == 1:
        # Chiama la funzione principale passando la lista di default.
        convert_notebooks(NOTEBOOKS)
        sys.exit(0)
    # Se viene passato un parametro, deve essere il nome di un notebook.
    # Quindi esegue la conversione solo di quel notebook.
    elif len(sys.argv) == 2:
        notebook_path = [sys.argv[1]]
        notebook_name = os.path.basename(notebook_path[0])
        # Controlla che il notebook passato come parametro sia presente nella
        # lista di default.
        if notebook_name not in NOTEBOOKS:
            print(f'Il notebook "{notebook_name}" non è valido.')
            sys.exit(1)
        # Chiama la funzione principale passando il nome del notebook indicato.
        convert_notebooks([notebook_name])
        sys.exit(0)
    else:
        # Se viene passato più di un parametro, per ora stampa un messaggio di
        # errore e termina lo script.
        print('Questo script accetta al massimo un parametro: il nome di un notebook.')
        sys.exit(1)

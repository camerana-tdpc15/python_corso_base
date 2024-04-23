import os
import matplotlib.font_manager as font_manager
from fontTools.ttLib import TTFont

EMOJI = [
    range(0x1F600, 0x1F64F + 1),  # Emoticons
    range(0x1F300, 0x1F5FF + 1),  # Miscellaneous Symbols and Pictographs
    range(0x1F900, 0x1F9FF + 1),  # Supplemental Symbols and Pictographs
    range(0x1FA70, 0x1FAFF + 1),  # Symbols and Pictographs Extended-A
    range(0x1F680, 0x1F6FF + 1),  # Transport and Map Symbols
]

def _get_font_path(font_name):
    # windows_fonts_folder = os.path.join(os.environ['WINDIR'], 'Fonts')
    # print(windows_fonts_folder)
    fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    # print(fonts)
    # Trova il font che corrisponde al nome richiesto
    for font in fonts:
        if font_name in font:
            return font
    raise FileNotFoundError('Il font non è stato trovato.')

def get_font_chars(font_name):
    font_path = _get_font_path(font_name)
    font = TTFont(font_path)
    cmap_table = font['cmap']  # Access the character mapping table
    characters = set()

    for cmap in cmap_table.tables:
        if cmap.isUnicode():  # Check if the table is Unicode
            characters.update(cmap.cmap.keys())  # Add all character codes from this table

    print(f'Trovati {len(characters)} caratteri.')
    res = []
    for code in characters:
        if not any(code in emoji_range for emoji_range in EMOJI):
            char = chr(code)
            if not char.isspace() and char.isprintable():
                res.append(char)

    return tuple(res)

ricetta_orig = "oliva\t, pepe,cappero ,\n detersivo,\t \n cappero, peperone, acciuga ,oliva , pepe\t,\t cappero , \noliva,pasta\n"
# ricetta_orig = "oliva\t, pepe,cappero ,\n dete\nrsivo,\t \n cappero, peperone, acciuga ,oliva , pepe\t,\t cappero , \noliva,pasta\n"
# ricetta_orig = "cappone , pepe,\noliva\n,\n\tpepe, acciuga "   #  1 oliva 2 pepe 0 cappero

ricetta_divisa = ricetta_orig.split(',')

ricetta = {}

for nome_orig in ricetta_divisa:
    nome_pulito = nome_orig.strip()
    if nome_pulito in ricetta:
        ricetta[nome_pulito] += 1
    else:
        ricetta[nome_pulito] = 1
print("Servono: ")

for key in ricetta:
    if ricetta[key] > 1:
        print('   ', ricetta[key], key)




import jinja2

# Creazione dell'ambiente
environment = jinja2.Environment()
# Creazione del template
template = environment.from_string("Hello, {{ name }}!")
# Rendering del template 
saluto = template.render(name="World")
print(saluto)


 
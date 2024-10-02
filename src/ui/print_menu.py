def print_with_color_and_format(text, color_code, bold=False, underline=False):
    start_code = "\033["
    if bold:
        start_code += "1;"
    if underline:
        start_code += "4;"
    start_code += f"{color_code}m"
    end_code = "\033[0m"
    print(f"{start_code}{text}{end_code}")
# rojo:31, verde:32, amarillo:33, azul:34


def print_menu_general():
    print_with_color_and_format('''
--------Registro de concentración - Buho------------------------------------------------------
Menú de opciones:
1) Iniciar sesión de concentración
2) Generar gráficos
3) Configurar tiempo
4) Salir
          ''', '33', bold = True)

def print_menu_concetracion():
    print_with_color_and_format('''
-------------------
Elegir tipo de concentración:
    1) Estudio
    2) Meditación
    3) Ejercicio Físico
    4) Trabajo
    5) Regresar 
                                
          ''', '32')
    
def print_menu_estudio():
    print_with_color_and_format('''
Elegir materia a estudiar:
          1) Idiomas
          2) Desarrollo de software          
          3) Matemáticas aplicadas
          4) Inteligencia Artificial y Aprendizaje Automático 
          5) Otros
          6) Regresar
          ''', '34')
    
def print_menu_meditacion():
    print_with_color_and_format('''
Elegir tipo de meditación:
          1) Vipassana
          2) Mindfulness
          3) Regresar 
           ''', '34')
def print_menu_ejercicio_fisico():
    print_with_color_and_format('''
Elegir tipo de ejercicio físico:
          1) Cardío
          2) Fuerza                
          3) Regresar 
           ''', '34')
    
def print_menu_trabajo():
    print_with_color_and_format('''
¿Para quién trabajas?
          1) Para mi
          2) Para otro
          3) Regresar
           ''', '34')
    
def print_despedida():
    print_with_color_and_format("Saliendo del programa...Hasta pronto!", '31', bold = True)
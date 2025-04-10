import json
import os
import random

# utils.py content (you can keep this in a separate file or put it here)
def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:  # Agregar encoding
        json.dump(data, f, indent=4, ensure_ascii=False) # Asegurar que se guarden bien caracteres especiales

def load_list(filename):
    with open(filename, "r", encoding="utf-8") as f:  # Agregar encoding
        return [line.strip() for line in f]

def run_cli(language):
    if language == "espanol":
        print("Bienvenido al Sock Spy de Kanarath!")
        gender_question = "¿Crear un hombre o una mujer? (hombre/mujer): "
        gender_options = "(hombre/mujer)"
        gender_error = "Respuesta inválida. ¿Hombre o mujer? (hombre/mujer): "
        nationality_question = "¿Qué nacionalidad? (spanish, chinese, ...): "
        nationality_options = "(spanish, chinese, ...)"
        nationality_error = "Nacionalidad inválida. Introduce una válida (spanish, chinese, ...): "
        choose_name = "Elige un nombre:"
        choose_last_name = "Elige un apellido:"
        select_number = "Introduce el número del {item} que quieres: "
        add_errors_question = "¿Añadir errores de ortografía a la biografía? (si/no): "
        add_errors_options = "(si/no)"
        profile_picture_question = "¿Añadir imagen de perfil? (si/no): "
        profile_picture_options = "(si/no)"
        common_phrases_question = "¿Añadir frases comunes? (si/no): "
        common_phrases_options = "(si/no)"
        profile_generated = "\nPerfil generado:\n"
        edit_question = "¿Deseas editar algún campo? (si/no): "
        edit_options = "(si/no)"
        edit_field_question = "¿Qué campo quieres editar? (ej. biography, interests): "
        new_value_question = "Introduce el nuevo valor para '{field}': "
        appendix_question = "¿Quieres añadir un apéndice al perfil? (si/no): "
        appendix_options = "(si/no)"
        username_question = "¿Qué nombre de usuario quieres usar? "
        username_confirmation = "Has introducido '{username}'. ¿Es correcto? (si/no): "
        password_question = "¿Qué contraseña quieres usar? (Visible): "
        password_confirmation = "Has introducido '{password}'. ¿Es correcto? (si/no): "
        platform_tracking_question = "¿En qué plataformas vas a crear un usuario con este Sock Spy? (Separadas por comas, ej: Twitter,Facebook,Instagram): "
        platform_tracking_options = "(Separadas por comas, ej: Twitter,Facebook,Instagram)"
        age_question = "¿Qué edad tiene el Sock Spy? "
        age_error = "Por favor, introduce una edad válida (un número): "

        filename_question = "Introduce el nombre del archivo para guardar el perfil (ej. sock_spy.json): "
        profile_saved = "Perfil guardado en {filename}"
    else:  # English
        print("Welcome to Kanarath's Sock Spy!")
        gender_question = "Create a male or a female? (male/female): "
        gender_options = "(male/female)"
        gender_error = "Invalid response. Male or female? (male/female): "
        nationality_question = "What nationality? (spanish, chinese, ...): "
        nationality_options = "(spanish, chinese, ...)"
        nationality_error = "Invalid nationality. Enter a valid one (spanish, chinese, ...): "
        choose_name = "Choose a name:"
        choose_last_name = "Choose a last name:"
        select_number = "Enter the number of the {item} you want: "
        add_errors_question = "Add spelling errors to the biography? (yes/no): "
        add_errors_options = "(yes/no)"
        profile_picture_question = "Add profile picture? (yes/no): "
        profile_picture_options = "(yes/no)"
        common_phrases_question = "Add common phrases? (yes/no): "
        common_phrases_options = "(yes/no)"
        profile_generated = "\nProfile generated:\n"
        edit_question = "Do you want to edit any field? (yes/no): "
        edit_options = "(yes/no)"
        edit_field_question = "What field do you want to edit? (e.g. biography, interests): "
        new_value_question = "Enter the new value for '{field}': "
        appendix_question = "Do you want to add an appendix to the profile? (yes/no): "
        appendix_options = "(yes/no)"
        username_question = "What username do you want to use? "
        username_confirmation = "You entered '{username}'. Is it correct? (yes/no): "
        password_question = "What password do you want to use? (Visible): "
        password_confirmation = "You entered '{password}'. Is it correct? (yes/no): "
        platform_tracking_question = "On what platforms will you create a user with this Sock Spy? (Comma-separated, e.g.: Twitter,Facebook,Instagram): "
        platform_tracking_options = "(Comma-separated, e.g.: Twitter,Facebook,Instagram)"
        age_question = "How old is the Sock Spy? "
        age_error = "Please enter a valid age (a number): "

        filename_question = "Enter the filename to save the profile (e.g. sock_spy.json): "
        profile_saved = "Profile saved to {filename}"

    gender = input(f"{gender_question} {gender_options}: ").lower()
    while gender not in ["hombre", "mujer", "male", "female"]:
        gender = input(gender_error).lower()
    gender = "male" if gender in ["hombre","male"] else "female"

    nationality = input(f"{nationality_question} {nationality_options}: ").lower()
    #Valida que exista la info
    name_file = f"data/names/{gender}/{nationality}.txt"
    while not os.path.exists(name_file):
      nationality = input(nationality_error).lower()
      name_file = f"data/names/{gender}/{nationality}.txt"

    #Selecciona Nombre
    names = load_list(name_file)
    print(choose_name)
    for i, name in enumerate(names[:5]):
        print(f"{i+1}. {name}")
    name_index = input(select_number.format(item="nombre" if language == "espanol" else "name"))
    selected_name = names[int(name_index)-1]

    #Selecciona Apellido
    last_names = load_list(f"data/last_names/{nationality}.txt")
    print(choose_last_name)
    for i, last_name in enumerate(last_names[:5]):
        print(f"{i+1}. {last_name}")
    last_name_index = input(select_number.format(item="apellido" if language == "espanol" else "lastname"))
    selected_last_name = last_names[int(last_name_index)-1]

    #Age selection
    age_valid = False
    while not age_valid:
        try:
            age = int(input(age_question))
            if 0 < age < 120:  # Basic sanity check
                age_valid = True
            else:
                print("Por favor, introduce una edad realista." if language == "espanol" else "Please, enter a realistic age.")
        except ValueError:
            print("Por favor, introduce una edad válida (un número)." if language == "espanol" else "Please enter a valid age (a number): ")

    # Generate Username Suggestions
    username_suggestions = generate_username_suggestions(selected_name, selected_last_name, age)
    print("Sugerencias de nombre de usuario:" if language == "espanol" else "Username suggestions:")
    for i, suggestion in enumerate(username_suggestions):
        print(f"{i+1}. {suggestion}")

    #location
    options = {}
    options["add_errors"] = input(f"{add_errors_question} {add_errors_options}: ").lower() == "si" or input(add_errors_question).lower() == "yes"
    options["profile_picture"] = input(f"{profile_picture_question} {profile_picture_options}: ").lower() == "si" or input(profile_picture_question).lower() == "yes"
    options["common_phrases"] = input(f"{common_phrases_question} {common_phrases_options}: ").lower() == "si" or input(common_phrases_question).lower() == "yes"

    # Username Loop
    username_correct = False
    while not username_correct:
        username = input(username_question)
        confirmation = input(username_confirmation.format(username=username)).lower()
        if confirmation in ["si", "yes"]:
            username_correct = True
        else:
            print("Por favor, introduce el nombre de usuario de nuevo." if language == "espanol" else "Please, enter the username again.")

    # Password Loop
    password_correct = False
    while not password_correct:
        password = input(password_question)
        confirmation = input(password_confirmation.format(password=password)).lower()
        if confirmation in ["si", "yes"]:
            password_correct = True
        else:
            print("Por favor, introduce la contraseña de nuevo." if language == "espanol" else "Please, enter the password again.")

    # Platforms Tracking
    platforms = input(f"{platform_tracking_question} {platform_tracking_options}: ").split(",")

    # Crear Diccionario
    sock_spy = {
        "first_name": selected_name,
        "last_name": selected_last_name,
        "age": age,
        "username": username,
        "password": password,
        "platforms": [p.strip() for p in platforms]  # Limpia los espacios
    }

    print(profile_generated, json.dumps(sock_spy, indent=4, ensure_ascii=False))

    # Edición final
    edit = input(f"{edit_question} {edit_options}: ").lower()
    while edit == "si" or edit == "yes":
        field = input(edit_field_question)
        new_value = input(new_value_question.format(field=field))
        sock_spy[field] = new_value
        edit = input(f"{edit_question} {edit_options}: ").lower()

    # Apéndice
    appendix = input(f"{appendix_question} {appendix_options}: ").lower()
    if appendix == "si" or appendix == "yes":
        appendix_text = input(appendix_text_question)
        sock_spy["appendix"] = appendix_text

    # Guardar el resultado
    filename = input(filename_question)
    save_data(sock_spy, filename)
    print(profile_saved.format(filename=filename))

def generate_username_suggestions(first_name, last_name, age):
    suggestions = []

    # Basic username
    suggestions.append(f"{first_name.lower()}{last_name.lower()}")
    suggestions.append(f"{first_name.lower()}.{last_name.lower()}")

    # Adding age
    suggestions.append(f"{first_name.lower()}{age}")
    suggestions.append(f"{first_name.lower()}{last_name.lower()}{age}")

    # Adding year of birth (more realistic)
    birth_year = 2024 - age
    suggestions.append(f"{first_name.lower()}{birth_year}")

    # Adding random numbers
    suggestions.append(f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}")

    # Truncated names
    suggestions.append(f"{first_name[:3].lower()}{last_name[:3].lower()}")

    # Initials
    suggestions.append(f"{first_name[0].lower()}{last_name[0].lower()}{random.randint(100, 999)}")

    return random.sample(suggestions, 5)  # Return only 5 suggestions

def get_random_logo():
    logos = [
        """
        # Logo 1: Replace this with your ASCII art.
        \033[32m
         _       _____  ____   ____        _____   ___   ____
        | |     / /  _||  _ \ /  _ \      |  ___| / _ \ |  _ \
        | | /| / /| |  | |_) )| |_) |     | |_   | | | || |_) )
        | |/ |/ / | |__|  _ ( |  _ <      |  _|  | | | ||  _ <
        |__/|__/  |____|_| \_\|_| \_|     |_|    |_| |_||_| \_|
                     Sock Spy
        \033[0m
        """,
        """
        # Logo 2: Replace this with your ASCII art.
        \033[33m
          /\\   /\\
         (  '---'  )
          (  > <  )
           ( vvv )
            `---'
        Sock Spy
        \033[0m
        """,
        """
        # Logo 3: Replace this with your ASCII art.
        \033[34m
         _.-""-._
        /   _    \\
        |  ( )   |
        \   `-'   /
         `-------'
        Sock Spy
        \033[0m
        """,
        """
        # Logo 4: Replace this with your ASCII art.
        \033[35m
        ((`--^--'))
         ) O o (
        /   (_)   \\
        Sock Spy
        \033[0m
        """,
        """
        # Logo 5: Replace this with your ASCII art.
        \033[36m
         _.-""-._
        /   _    \\
        |  ( )   |
        \   `-'   /
         `-------'
        Sock Spy
        \033[0m
        """
    ]
    return random.choice(logos)

if __name__ == "__main__":
    # Logo ASCII
    logo = get_random_logo()
    print(logo)

    language = input("¿En qué idioma quieres crear tu Sock Spy? (espanol/ingles): ").lower()
    while language not in ["espanol", "ingles"]:
        language = input("Idioma inválido. Elige 'espanol' o 'ingles': ").lower()

    run_cli(language)
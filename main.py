#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sock Spy: CLI Tool for Generating OSINT Sock Puppets
A tool to create realistic and customizable personas for OSINT investigations.
"""

import os
import sys
import json
import random
import datetime
from utils import (
    load_data_file,
    load_json_file,
    save_profile,
    export_profile_to_txt,
    display_ascii_art,
    clear_screen,
    get_input,
    get_numeric_choice,
    generate_username_suggestions,
    get_current_year,
    load_hierarchical_data
)

# Configuración de idioma
TEXTS = {
    "en": {
        "welcome": "Welcome to Sock Spy: OSINT Sock Puppet Generator",
        "language_select": "Select language:",
        "language_options": ["English", "Spanish"],
        "gender_select": "Select gender for the persona:",
        "gender_options": ["Male", "Female"],
        "nationality_select": "Select nationality:",
        "nationality_options": ["Spanish", "English", "Chinese", "European", "Asian", "American"],
        "name_select": "Select a first name:",
        "lastname_select": "Select a last name:",
        "age_prompt": "Enter the age of the persona (0-120):",
        "age_error": "Please enter a valid age between 0 and 120.",
        "username_suggestions": "Username suggestions:",
        "username_prompt": "Enter a username for the persona:",
        "username_confirm": "Confirm username '{}'? (y/n):",
        "password_prompt": "Enter a password for the persona:",
        "password_confirm": "Confirm password '{}'? (y/n):",
        "platforms_prompt": "Enter comma-separated list of platforms (e.g., Twitter, Facebook, Instagram):",
        "add_errors_prompt": "Add profile errors? (y/n):",
        "add_picture_prompt": "Add profile picture? (y/n):",
        "add_phrases_prompt": "Add common phrases? (y/n):",
        "profile_preview": "Generated Profile Preview:",
        "edit_profile_prompt": "Do you want to edit any fields? (y/n):",
        "edit_field_prompt": "Enter the field name to edit:",
        "edit_value_prompt": "Enter the new value:",
        "add_appendix_prompt": "Do you want to add an appendix to the profile? (y/n):",
        "appendix_prompt": "Enter appendix text:",
        "filename_prompt": "Enter filename to save the profile (without extension):",
        "save_success": "Profile saved to {}",
        "export_success": "Profile exported to {}",
        "continue_prompt": "Press Enter to continue...",
        "main_menu": "Main Menu:",
        "main_menu_options": [
            "Create new persona",
            "Load existing persona",
            "View program information",
            "Exit"
        ],
        "back_option": "Back",
        "exit_option": "Exit",
        "invalid_choice": "Invalid choice. Please try again.",
        "program_info": """
Sock Spy: CLI Tool for Generating OSINT Sock Puppets
Version: 1.1
Created for: Security researchers, OSINT investigators, and professionals
Purpose: Create realistic online personas for research and analysis purposes.
        """,
        "interests_select": "Select interests category:",
        "interests_subcategory": "Select interests subcategory:",
        "interests_specific": "Select specific interests (enter numbers separated by commas, max 5):",
        "profession_category": "Select profession category:",
        "profession_subcategory": "Select profession subcategory:",
        "profession_specific": "Select a specific profession:",
        "location_country": "Select a country:",
        "location_region": "Select a region:",
        "location_city": "Select a city:",
        "location_neighborhood": "Select a neighborhood:",
        "biography_prompt": "Enter a short biography (press Enter to generate automatically):",
        "no_personas_found": "No saved personas found.",
        "select_persona": "Select a persona to load:",
        "persona_loaded": "Persona loaded successfully.",
        "persona_options": "Persona Options:",
        "persona_options_list": [
            "View persona details",
            "Edit persona",
            "Export persona",
            "Export persona as TXT",
            "Delete persona",
            "Back to main menu"
        ],
        "confirm_delete": "Are you sure you want to delete this persona? (y/n):",
        "deleted_success": "Persona deleted successfully.",
        "common_phrases_select": "Select common phrases (enter numbers separated by commas, max 3):",
        "regenerate_options": "Would you like to see more options? (y/n):",
        "stop_navigation": "Stop here and use this selection? (y/n):",
        "skip_to_next": "Skip to next section? (y/n):"
    },
    "es": {
        "welcome": "Bienvenido a Sock Spy: Generador de Sock Puppets para OSINT",
        "language_select": "Seleccione idioma:",
        "language_options": ["Inglés", "Español"],
        "gender_select": "Seleccione género para la persona:",
        "gender_options": ["Masculino", "Femenino"],
        "nationality_select": "Seleccione nacionalidad:",
        "nationality_options": ["Española", "Inglesa", "China", "Europea", "Asiática", "Americana"],
        "name_select": "Seleccione un nombre:",
        "lastname_select": "Seleccione un apellido:",
        "age_prompt": "Ingrese la edad de la persona (0-120):",
        "age_error": "Por favor ingrese una edad válida entre 0 y 120.",
        "username_suggestions": "Sugerencias de nombre de usuario:",
        "username_prompt": "Ingrese un nombre de usuario para la persona:",
        "username_confirm": "¿Confirmar nombre de usuario '{}'? (s/n):",
        "password_prompt": "Ingrese una contraseña para la persona:",
        "password_confirm": "¿Confirmar contraseña '{}'? (s/n):",
        "platforms_prompt": "Ingrese lista de plataformas separadas por comas (ej., Twitter, Facebook, Instagram):",
        "add_errors_prompt": "¿Añadir errores de perfil? (s/n):",
        "add_picture_prompt": "¿Añadir foto de perfil? (s/n):",
        "add_phrases_prompt": "¿Añadir frases comunes? (s/n):",
        "profile_preview": "Vista previa del perfil generado:",
        "edit_profile_prompt": "¿Desea editar algún campo? (s/n):",
        "edit_field_prompt": "Ingrese el nombre del campo a editar:",
        "edit_value_prompt": "Ingrese el nuevo valor:",
        "add_appendix_prompt": "¿Desea añadir un apéndice al perfil? (s/n):",
        "appendix_prompt": "Ingrese texto del apéndice:",
        "filename_prompt": "Ingrese nombre de archivo para guardar el perfil (sin extensión):",
        "save_success": "Perfil guardado en {}",
        "export_success": "Perfil exportado a {}",
        "continue_prompt": "Presione Enter para continuar...",
        "main_menu": "Menú Principal:",
        "main_menu_options": [
            "Crear nueva persona",
            "Cargar persona existente",
            "Ver información del programa",
            "Salir"
        ],
        "back_option": "Volver",
        "exit_option": "Salir",
        "invalid_choice": "Opción inválida. Por favor intente de nuevo.",
        "program_info": """
Sock Spy: Herramienta CLI para Generar Sock Puppets para OSINT
Versión: 1.1
Creado para: Investigadores de seguridad, investigadores OSINT y profesionales
Propósito: Crear personas en línea realistas para fines de investigación y análisis.
        """,
        "interests_select": "Seleccione categoría de intereses:",
        "interests_subcategory": "Seleccione subcategoría de intereses:",
        "interests_specific": "Seleccione intereses específicos (ingrese números separados por comas, máx 5):",
        "profession_category": "Seleccione categoría de profesión:",
        "profession_subcategory": "Seleccione subcategoría de profesión:",
        "profession_specific": "Seleccione una profesión específica:",
        "location_country": "Seleccione un país:",
        "location_region": "Seleccione una región:",
        "location_city": "Seleccione una ciudad:",
        "location_neighborhood": "Seleccione un barrio:",
        "biography_prompt": "Ingrese una biografía corta (presione Enter para generar automáticamente):",
        "no_personas_found": "No se encontraron personas guardadas.",
        "select_persona": "Seleccione una persona para cargar:",
        "persona_loaded": "Persona cargada exitosamente.",
        "persona_options": "Opciones de Persona:",
        "persona_options_list": [
            "Ver detalles de la persona",
            "Editar persona",
            "Exportar persona",
            "Exportar persona como TXT",
            "Eliminar persona",
            "Volver al menú principal"
        ],
        "confirm_delete": "¿Está seguro que desea eliminar esta persona? (s/n):",
        "deleted_success": "Persona eliminada exitosamente.",
        "common_phrases_select": "Seleccione frases comunes (ingrese números separados por comas, máx 3):",
        "regenerate_options": "¿Desea ver más opciones? (s/n):",
        "stop_navigation": "¿Detener aquí y usar esta selección? (s/n):",
        "skip_to_next": "¿Saltar a la siguiente sección? (s/n):"
    }
}

class SockSpy:
    def __init__(self):
        self.language = "en"  # Default language
        self.texts = TEXTS[self.language]
        self.profile = {}
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
        self.exports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
        
        # Ensure directories exist
        for directory in [self.profiles_dir, self.exports_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def select_language(self):
        """Allow user to select language"""
        clear_screen()
        print(self.texts["welcome"])
        print("\n" + self.texts["language_select"])
        
        for i, lang in enumerate(self.texts["language_options"], 1):
            print(f"{i}. {lang}")
        
        choice = get_numeric_choice(1, len(self.texts["language_options"]))
        
        if choice == 1:
            self.language = "en"
        else:
            self.language = "es"
        
        self.texts = TEXTS[self.language]
    
    def display_welcome(self):
        """Display welcome screen with ASCII art"""
        clear_screen()
        display_ascii_art(self.data_dir)
        print(self.texts["welcome"])
        input(self.texts["continue_prompt"])
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            clear_screen()
            print(self.texts["main_menu"])
            
            for i, option in enumerate(self.texts["main_menu_options"], 1):
                print(f"{i}. {option}")
            
            choice = get_numeric_choice(1, len(self.texts["main_menu_options"]))
            
            if choice == 1:
                self.create_persona()
            elif choice == 2:
                self.load_persona()
            elif choice == 3:
                self.show_program_info()
            elif choice == 4:
                sys.exit(0)
    
    def create_persona(self):
        """Guide user through persona creation process"""
        self.profile = {}
        
        # Select gender
        clear_screen()
        print(self.texts["gender_select"])
        for i, gender in enumerate(self.texts["gender_options"], 1):
            print(f"{i}. {gender}")
        
        gender_choice = get_numeric_choice(1, len(self.texts["gender_options"]))
        gender = "male" if gender_choice == 1 else "female"
        self.profile["gender"] = gender
        
        # Select nationality
        clear_screen()
        print(self.texts["nationality_select"])
        for i, nationality in enumerate(self.texts["nationality_options"], 1):
            print(f"{i}. {nationality}")
        
        nationality_choice = get_numeric_choice(1, len(self.texts["nationality_options"]))
        nationality = self.texts["nationality_options"][nationality_choice - 1].lower()
        self.profile["nationality"] = nationality
        
        # Select first name
        self.select_name(gender, nationality)
        
        # Select last name
        self.select_lastname(nationality)
        
        # Get age
        clear_screen()
        while True:
            try:
                age = int(input(self.texts["age_prompt"] + " "))
                if 0 <= age <= 120:
                    self.profile["age"] = age
                    break
                else:
                    print(self.texts["age_error"])
            except ValueError:
                print(self.texts["age_error"])
        
        # Generate username suggestions
        self.select_username()
        
        # Get password
        clear_screen()
        while True:
            password = input(self.texts["password_prompt"] + " ")
            confirm = input(self.texts["password_confirm"].format(password) + " ")
            if confirm.lower() in ["y", "yes", "s", "si", "sí"]:
                self.profile["password"] = password
                break
        
        # Get platforms
        clear_screen()
        platforms_input = input(self.texts["platforms_prompt"] + " ")
        platforms = [p.strip() for p in platforms_input.split(",") if p.strip()]
        self.profile["platforms"] = platforms
        
        # Select interests hierarchically
        self.select_hierarchical_interests()
        
        # Select profession hierarchically
        self.select_hierarchical_profession()
        
        # Select location
        self.select_location()
        
        # Add common phrases if desired
        clear_screen()
        if input(self.texts["add_phrases_prompt"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.select_common_phrases()
        
        # Add profile picture if desired
        clear_screen()
        if input(self.texts["add_picture_prompt"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.select_profile_picture()
        
        # Add profile errors if desired
        clear_screen()
        if input(self.texts["add_errors_prompt"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.add_profile_errors()
        
        # Preview profile
        self.preview_profile()
        
        # Edit profile if desired
        if input(self.texts["edit_profile_prompt"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.edit_profile()
        
        # Add appendix if desired
        clear_screen()
        if input(self.texts["add_appendix_prompt"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            appendix = input(self.texts["appendix_prompt"] + " ")
            self.profile["appendix"] = appendix
        
        # Save profile
        clear_screen()
        filename = input(self.texts["filename_prompt"] + " ")
        if not filename:
            filename = f"{self.profile['first_name']}_{self.profile['last_name']}".lower()
        
        filepath = save_profile(self.profile, filename, self.profiles_dir)
        print(self.texts["save_success"].format(filepath))
        
        # Export to TXT
        txt_filepath = export_profile_to_txt(self.profile, filename, self.exports_dir)
        print(self.texts["export_success"].format(txt_filepath))
        
        input(self.texts["continue_prompt"])
    
    def select_name(self, gender, nationality):
        """Select a first name with option to regenerate list"""
        clear_screen()
        print(self.texts["name_select"])
        
        names_file = os.path.join(self.data_dir, "names", gender, f"{nationality.lower()}.txt")
        names = load_data_file(names_file)
        
        while True:
            random_names = random.sample(names, min(5, len(names)))
            
            for i, name in enumerate(random_names, 1):
                print(f"{i}. {name}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            name_choice = get_numeric_choice(1, len(random_names))
            self.profile["first_name"] = random_names[name_choice - 1]
            break
    
    def select_lastname(self, nationality):
        """Select a last name with option to regenerate list"""
        clear_screen()
        print(self.texts["lastname_select"])
        
        lastnames_file = os.path.join(self.data_dir, "last_names", f"{nationality.lower()}.txt")
        lastnames = load_data_file(lastnames_file)
        
        while True:
            random_lastnames = random.sample(lastnames, min(5, len(lastnames)))
            
            for i, lastname in enumerate(random_lastnames, 1):
                print(f"{i}. {lastname}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            lastname_choice = get_numeric_choice(1, len(random_lastnames))
            self.profile["last_name"] = random_lastnames[lastname_choice - 1]
            break
    
    def select_username(self):
        """Generate and select username with option to regenerate suggestions"""
        clear_screen()
        
        while True:
            print(self.texts["username_suggestions"])
            username_suggestions = generate_username_suggestions(
                self.profile["first_name"],
                self.profile["last_name"],
                self.profile["age"]
            )
            
            for i, username in enumerate(username_suggestions, 1):
                print(f"{i}. {username}")
            
            # Option to select from suggestions or enter custom
            print(f"{len(username_suggestions) + 1}. Enter custom username")
            
            choice = get_numeric_choice(1, len(username_suggestions) + 1)
            
            if choice <= len(username_suggestions):
                username = username_suggestions[choice - 1]
                confirm = input(self.texts["username_confirm"].format(username) + " ")
                if confirm.lower() in ["y", "yes", "s", "si", "sí"]:
                    self.profile["username"] = username
                    break
                # If not confirmed, regenerate
            else:
                # Custom username
                username = input(self.texts["username_prompt"] + " ")
                confirm = input(self.texts["username_confirm"].format(username) + " ")
                if confirm.lower() in ["y", "yes", "s", "si", "sí"]:
                    self.profile["username"] = username
                    break
    
    def select_hierarchical_interests(self):
        """Select interests using hierarchical structure"""
        clear_screen()
        interests_data = load_json_file(os.path.join(self.data_dir, "interests.json"))
        selected_interests = []
        
        # First level - Main categories
        print(self.texts["interests_select"])
        categories = list(interests_data.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        category_choice = get_numeric_choice(1, len(categories))
        selected_category = categories[category_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            # Select random interests from this category
            all_interests = []
            for subcategory in interests_data[selected_category].values():
                all_interests.extend(subcategory)
            
            random_interests = random.sample(all_interests, min(5, len(all_interests)))
            self.profile["interests"] = random_interests
            return
        
        # Second level - Subcategories
        clear_screen()
        print(self.texts["interests_subcategory"])
        subcategories = list(interests_data[selected_category].keys())
        for i, subcategory in enumerate(subcategories, 1):
            print(f"{i}. {subcategory}")
        
        # Option to skip to next section
        if input(self.texts["skip_to_next"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["interests"] = []
            return
        
        subcategory_choice = get_numeric_choice(1, len(subcategories))
        selected_subcategory = subcategories[subcategory_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            # Select random interests from this subcategory
            specific_interests = interests_data[selected_category][selected_subcategory]
            random_interests = random.sample(specific_interests, min(5, len(specific_interests)))
            self.profile["interests"] = random_interests
            return
        
        # Third level - Specific interests
        clear_screen()
        print(self.texts["interests_specific"])
        specific_interests = interests_data[selected_category][selected_subcategory]
        
        while True:
            # Show random selection of specific interests
            random_specific = random.sample(specific_interests, min(10, len(specific_interests)))
            
            for i, interest in enumerate(random_specific, 1):
                print(f"{i}. {interest}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            interests_input = input("> ")
            try:
                interest_choices = [int(x.strip()) for x in interests_input.split(",") if x.strip()]
                interest_choices = [i for i in interest_choices if 1 <= i <= len(random_specific)]
                interest_choices = interest_choices[:5]  # Limit to 5 interests
                selected_interests = [random_specific[i-1] for i in interest_choices]
                self.profile["interests"] = selected_interests
                break
            except ValueError:
                self.profile["interests"] = []
                break
    
    def select_hierarchical_profession(self):
        """Select profession using hierarchical structure"""
        clear_screen()
        professions_data = load_json_file(os.path.join(self.data_dir, "professions.json"))
        
        # First level - Main categories
        print(self.texts["profession_category"])
        categories = list(professions_data.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        category_choice = get_numeric_choice(1, len(categories))
        selected_category = categories[category_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            # Select random profession from this category
            all_professions = []
            for subcategory in professions_data[selected_category].values():
                all_professions.extend(subcategory)
            
            self.profile["profession"] = random.choice(all_professions)
            return
        
        # Second level - Subcategories
        clear_screen()
        print(self.texts["profession_subcategory"])
        subcategories = list(professions_data[selected_category].keys())
        for i, subcategory in enumerate(subcategories, 1):
            print(f"{i}. {subcategory}")
        
        # Option to skip to next section
        if input(self.texts["skip_to_next"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            # Select random profession from general category
            professions_file = os.path.join(self.data_dir, "professions", "general.txt")
            professions = load_data_file(professions_file)
            self.profile["profession"] = random.choice(professions)
            return
        
        subcategory_choice = get_numeric_choice(1, len(subcategories))
        selected_subcategory = subcategories[subcategory_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            # Select random profession from this subcategory
            specific_professions = professions_data[selected_category][selected_subcategory]
            self.profile["profession"] = random.choice(specific_professions)
            return
        
        # Third level - Specific profession
        clear_screen()
        print(self.texts["profession_specific"])
        specific_professions = professions_data[selected_category][selected_subcategory]
        
        while True:
            # Show random selection of specific professions
            random_specific = random.sample(specific_professions, min(5, len(specific_professions)))
            
            for i, profession in enumerate(random_specific, 1):
                print(f"{i}. {profession}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            profession_choice = get_numeric_choice(1, len(random_specific))
            self.profile["profession"] = random_specific[profession_choice - 1]
            break
    
    def select_location(self):
        """Select location with hierarchical structure"""
        clear_screen()
        locations = load_json_file(os.path.join(self.data_dir, "locations.json"))
        
        # Select country
        print(self.texts["location_country"])
        countries = list(locations.keys())
        for i, country in enumerate(countries, 1):
            print(f"{i}. {country}")
        
        country_choice = get_numeric_choice(1, len(countries))
        selected_country = countries[country_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = selected_country
            return
        
        # Select region
        clear_screen()
        print(self.texts["location_region"])
        regions = list(locations[selected_country].keys())
        for i, region in enumerate(regions, 1):
            print(f"{i}. {region}")
        
        # Option to skip to next section
        if input(self.texts["skip_to_next"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = selected_country
            return
        
        region_choice = get_numeric_choice(1, len(regions))
        selected_region = regions[region_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = f"{selected_country}, {selected_region}"
            return
        
        # Select city
        clear_screen()
        print(self.texts["location_city"])
        cities = list(locations[selected_country][selected_region].keys())
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city}")
        
        # Option to skip to next section
        if input(self.texts["skip_to_next"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = f"{selected_country}, {selected_region}"
            return
        
        city_choice = get_numeric_choice(1, len(cities))
        selected_city = cities[city_choice - 1]
        
        # Ask if user wants to stop here
        if input(self.texts["stop_navigation"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = f"{selected_city}, {selected_region}, {selected_country}"
            return
        
        # Select neighborhood
        clear_screen()
        print(self.texts["location_neighborhood"])
        neighborhoods = locations[selected_country][selected_region][selected_city]
        for i, neighborhood in enumerate(neighborhoods, 1):
            print(f"{i}. {neighborhood}")
        
        # Option to skip to next section
        if input(self.texts["skip_to_next"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
            self.profile["location"] = f"{selected_city}, {selected_region}, {selected_country}"
            return
        
        neighborhood_choice = get_numeric_choice(1, len(neighborhoods))
        selected_neighborhood = neighborhoods[neighborhood_choice - 1]
        
        self.profile["location"] = f"{selected_neighborhood}, {selected_city}, {selected_region}, {selected_country}"
    
    def select_common_phrases(self):
        """Select common phrases based on nationality"""
        clear_screen()
        print(self.texts["common_phrases_select"])
        
        # Determine language file based on nationality
        language_file = "english.txt"
        if self.profile["nationality"].lower() in ["spanish", "española"]:
            language_file = "spanish.txt"
        elif self.profile["nationality"].lower() in ["chinese", "china"]:
            language_file = "chinese.txt"
        
        phrases_file = os.path.join(self.data_dir, "common_phrases", language_file)
        phrases = load_data_file(phrases_file)
        
        while True:
            random_phrases = random.sample(phrases, min(10, len(phrases)))
            
            for i, phrase in enumerate(random_phrases, 1):
                print(f"{i}. {phrase}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            phrases_input = input("> ")
            try:
                phrase_choices = [int(x.strip()) for x in phrases_input.split(",") if x.strip()]
                phrase_choices = [i for i in phrase_choices if 1 <= i <= len(random_phrases)]
                phrase_choices = phrase_choices[:3]  # Limit to 3 phrases
                selected_phrases = [random_phrases[i-1] for i in phrase_choices]
                self.profile["common_phrases"] = selected_phrases
                break
            except ValueError:
                self.profile["common_phrases"] = []
                break
    
    def select_profile_picture(self):
        """Select a profile picture URL"""
        clear_screen()
        pictures_file = os.path.join(self.data_dir, "profile_pictures.txt")
        pictures = load_data_file(pictures_file)
        
        # Filter by gender
        gender = self.profile["gender"]
        gender_pictures = [pic for pic in pictures if f"/{gender}/" in pic]
        
        while True:
            random_pictures = random.sample(gender_pictures, min(5, len(gender_pictures)))
            
            for i, picture in enumerate(random_pictures, 1):
                print(f"{i}. {picture}")
            
            if input(self.texts["regenerate_options"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                continue
            
            picture_choice = get_numeric_choice(1, len(random_pictures))
            self.profile["profile_picture"] = random_pictures[picture_choice - 1]
            break
    
    def add_profile_errors(self):
        """Add intentional errors to the profile for realism"""
        # Randomly decide which fields to add errors to
        fields = ["first_name", "last_name", "location"]
        error_fields = random.sample(fields, random.randint(0, len(fields)))
        
        for field in error_fields:
            if field in self.profile and isinstance(self.profile[field], str):
                # Types of errors: typo, capitalization, extra/missing letter
                error_type = random.choice(["typo", "caps", "extra", "missing"])
                
                if error_type == "typo" and len(self.profile[field]) > 3:
                    # Replace a random letter with an adjacent one on keyboard
                    keyboard = {
                        'a': 'sq', 'b': 'vn', 'c': 'xv', 'd': 'sf', 'e': 'wr', 'f': 'dg',
                        'g': 'fh', 'h': 'gj', 'i': 'uo', 'j': 'hk', 'k': 'jl', 'l': 'k',
                        'm': 'n', 'n': 'bm', 'o': 'ip', 'p': 'o', 'q': 'wa', 'r': 'et',
                        's': 'ad', 't': 'ry', 'u': 'yi', 'v': 'cb', 'w': 'qe', 'x': 'zc',
                        'y': 'tu', 'z': 'x'
                    }
                    
                    pos = random.randint(0, len(self.profile[field]) - 1)
                    char = self.profile[field][pos].lower()
                    if char in keyboard:
                        replacement = random.choice(keyboard[char])
                        self.profile[field] = self.profile[field][:pos] + replacement + self.profile[field][pos+1:]
                
                elif error_type == "caps" and len(self.profile[field]) > 1:
                    # Randomly change capitalization
                    pos = random.randint(0, len(self.profile[field]) - 1)
                    char = self.profile[field][pos]
                    if char.islower():
                        self.profile[field] = self.profile[field][:pos] + char.upper() + self.profile[field][pos+1:]
                    else:
                        self.profile[field] = self.profile[field][:pos] + char.lower() + self.profile[field][pos+1:]
                
                elif error_type == "extra" and len(self.profile[field]) > 2:
                    # Add an extra letter
                    pos = random.randint(0, len(self.profile[field]) - 1)
                    char = self.profile[field][pos]
                    self.profile[field] = self.profile[field][:pos] + char + self.profile[field][pos:]
                
                elif error_type == "missing" and len(self.profile[field]) > 3:
                    # Remove a letter
                    pos = random.randint(0, len(self.profile[field]) - 1)
                    self.profile[field] = self.profile[field][:pos] + self.profile[field][pos+1:]
    
    def preview_profile(self):
        """Display a preview of the generated profile"""
        clear_screen()
        print(self.texts["profile_preview"])
        print("\n" + "=" * 40 + "\n")
        
        print(f"Name: {self.profile.get('first_name', 'N/A')} {self.profile.get('last_name', 'N/A')}")
        print(f"Gender: {self.profile.get('gender', 'N/A')}")
        print(f"Age: {self.profile.get('age', 'N/A')}")
        print(f"Nationality: {self.profile.get('nationality', 'N/A')}")
        print(f"Location: {self.profile.get('location', 'N/A')}")
        print(f"Username: {self.profile.get('username', 'N/A')}")
        print(f"Password: {self.profile.get('password', 'N/A')}")
        
        print("\nPlatforms:")
        for platform in self.profile.get("platforms", []):
            print(f"- {platform}")
        
        print("\nInterests:")
        for interest in self.profile.get("interests", []):
            print(f"- {interest}")
        
        print(f"\nProfession: {self.profile.get('profession', 'N/A')}")
        
        if "common_phrases" in self.profile:
            print("\nCommon Phrases:")
            for phrase in self.profile["common_phrases"]:
                print(f"- {phrase}")
        
        if "profile_picture" in self.profile:
            print(f"\nProfile Picture: {self.profile['profile_picture']}")
        
        if "appendix" in self.profile:
            print(f"\nAppendix: {self.profile['appendix']}")
        
        print("\n" + "=" * 40 + "\n")
        input(self.texts["continue_prompt"])
    
    def edit_profile(self):
        """Allow user to edit profile fields"""
        clear_screen()
        self.preview_profile()
        
        while True:
            field = input(self.texts["edit_field_prompt"] + " ")
            if not field:
                break
            
            if field in self.profile:
                new_value = input(self.texts["edit_value_prompt"] + " ")
                self.profile[field] = new_value
            else:
                print(f"Field '{field}' not found in profile.")
            
            if input(self.texts["edit_profile_prompt"] + " ").lower() not in ["y", "yes", "s", "si", "sí"]:
                break
        
        self.preview_profile()
    
    def load_persona(self):
        """Load an existing persona from file"""
        clear_screen()
        
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
        
        profiles = [f for f in os.listdir(self.profiles_dir) if f.endswith('.json')]
        
        if not profiles:
            print(self.texts["no_personas_found"])
            input(self.texts["continue_prompt"])
            return
        
        print(self.texts["select_persona"])
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile[:-5]}")  # Remove .json extension
        
        choice = get_numeric_choice(1, len(profiles))
        profile_path = os.path.join(self.profiles_dir, profiles[choice - 1])
        
        with open(profile_path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)
        
        print(self.texts["persona_loaded"])
        self.persona_options(profile_path)
    
    def persona_options(self, profile_path):
        """Display options for loaded persona"""
        while True:
            clear_screen()
            print(self.texts["persona_options"])
            
            for i, option in enumerate(self.texts["persona_options_list"], 1):
                print(f"{i}. {option}")
            
            choice = get_numeric_choice(1, len(self.texts["persona_options_list"]))
            
            if choice == 1:
                self.preview_profile()
            elif choice == 2:
                self.edit_profile()
                # Save changes
                with open(profile_path, "w", encoding="utf-8") as f:
                    json.dump(self.profile, f, indent=2, ensure_ascii=False)
            elif choice == 3:
                # Export persona as JSON
                export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
                if not os.path.exists(export_dir):
                    os.makedirs(export_dir)
                
                export_path = os.path.join(export_dir, os.path.basename(profile_path))
                with open(export_path, "w", encoding="utf-8") as f:
                    json.dump(self.profile, f, indent=2, ensure_ascii=False)
                
                print(self.texts["export_success"].format(export_path))
                input(self.texts["continue_prompt"])
            elif choice == 4:
                # Export persona as TXT
                export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
                if not os.path.exists(export_dir):
                    os.makedirs(export_dir)
                
                filename = os.path.basename(profile_path)[:-5]  # Remove .json extension
                txt_filepath = export_profile_to_txt(self.profile, filename, export_dir)
                
                print(self.texts["export_success"].format(txt_filepath))
                input(self.texts["continue_prompt"])
            elif choice == 5:
                # Delete persona
                if input(self.texts["confirm_delete"] + " ").lower() in ["y", "yes", "s", "si", "sí"]:
                    os.remove(profile_path)
                    print(self.texts["deleted_success"])
                    input(self.texts["continue_prompt"])
                    break
            elif choice == 6:
                break
    
    def show_program_info(self):
        """Display program information"""
        clear_screen()
        print(self.texts["program_info"])
        input(self.texts["continue_prompt"])

def main():
    app = SockSpy()
    app.select_language()
    app.display_welcome()
    app.main_menu()

if __name__ == "__main__":
    main()

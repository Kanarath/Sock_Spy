#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2025 Kanarath.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


Sock Spy: CLI Tool for Generating OSINT Sock Puppets
A tool to create realistic and customizable personas for OSINT investigations.
"""

import os
import sys
import json
import random
import datetime
import time # Import time for sleep

# Correctly import all necessary functions from utils
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
    # load_hierarchical_data, # Likely not needed anymore, commenting out
    generate_random_password,
    get_random_hierarchical_item,
    handle_dynamic_list_selection,
)

# English texts ONLY
TEXTS = {
    "en": {
        "welcome": "Welcome to Sock Spy: OSINT Sock Puppet Generator",
        # "language_select": "Select language:", # Removed
        # "language_options": ["English", "Spanish"], # Removed
        "gender_select": "Select gender for the persona:",
        "gender_options": ["Male", "Female"],
        "nationality_continent": "Select continent/region for nationality:",
        "nationality_specific": "Select a specific nationality:",
        "name_select": "Select a first name:",
        "lastname_select": "Select a last name:",
        "age_prompt": "Enter the age of the persona (18-99):",
        "age_error": "Please enter a valid age between 18 and 99.",
        "username_suggestions": "Username suggestions:",
        "username_prompt": "Enter a username for the persona:",
        "username_confirm": "Confirm username '{}'? (y/n):",
        "password_prompt": "Enter a password for the persona:",
        "password_confirm": "Confirm password '{}'? (y/n):",
        "platforms_prompt": "Enter comma-separated list of platforms (e.g., Twitter, Facebook, Instagram):",
        "add_picture_prompt": "Add profile picture? (y/n):",
        "add_phrases_prompt": "Add common phrases? (y/n):",
        "profile_preview": "Generated Profile Preview:",
        "edit_profile_prompt": "Do you want to edit any fields? (y/n):",
        "edit_field_prompt": "Enter the number of the field to edit (or press Enter to finish):", # Changed for edit_profile
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
            "Create random persona", # Keep this
            "Load existing persona",
            "View program information",
            "Exit"
        ],
        "random_level_select": "Select level of random persona detail:",
        "random_level_options": [
            "1. Minimal (Name, Gender, Age, Nationality, Profession)",
            "2. Standard (Adds Basic Location, Username, Password)",
            "3. Detailed (Adds Specific Location, Platforms, Interests)",
            "4. Full (Adds Phrases, Picture)" # Simplified full
        ],
        "random_generating": "Generating {item}...", # For visual feedback
        "random_generation_complete": "Random persona generation complete.",
        "confirm_save_random": "Do you want to save this generated profile? (y/n):",
        "back_option": "Back",
        "exit_option": "Exit",
        "invalid_choice": "Invalid choice. Please try again.",
        "program_info": """
Sock Spy: CLI Tool for Generating OSINT Sock Puppets
Sock Spy is Open Source and is licensed under the GNU General Public License v3.0.
Version: 1.0
        """,
        "interests_select": "Select interests category:",
        "interests_subcategory": "Select interests subcategory:",
        "interests_specific": "Select specific interests (enter numbers separated by commas, max 5, or choose an action):", # Updated prompt
        "profession_category": "Select profession category:",
        "profession_subcategory": "Select profession subcategory:",
        "profession_specific": "Select a specific profession:",
        "location_continent": "Select a continent:", # Added continent prompt
        "location_country": "Select a country:",
        "location_region": "Select a region/state:",
        "location_city": "Select a city:",
        "location_neighborhood": "Select a neighborhood (Optional):",
        "biography_prompt": "Enter a short biography (press Enter to generate automatically):", # Still here if needed
        "no_personas_found": "No saved personas found.",
        "select_persona": "Select a persona to load:",
        "persona_loaded": "Persona loaded successfully.",
        "persona_options": "Persona Options:",
        "persona_options_list": [
            "View persona details",
            "Edit persona",
            "Export persona (JSON)", # Clarified export type
            "Export persona (TXT)",  # Clarified export type
            "Delete persona",
            "Back to main menu"
        ],
        "confirm_delete": "Are you sure you want to delete this persona? (y/n):",
        "deleted_success": "Persona deleted successfully.",
        "common_phrases_select": "Select common phrases (enter numbers separated by commas, max 3, or choose an action):", # Updated prompt
        "show_more_options": "Show More Options",
        "regenerate_options": "Show New Options (Regenerate List)",
        "skip_level_and_continue": "Stop here and use current selection", # Simplified skip text
        "select_or_action": "Select an item or choose an action:",
        # Old yes/no prompts removed as they are replaced by numbered actions
    }
    # NO "es": {} block anymore
}

class SockSpy:
    def __init__(self):
        # self.language = "en" # No longer needed, hardcoded english
        self.texts = TEXTS["en"] # Directly use english texts
        self.profile = {}
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")
        self.exports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")

        # Ensure directories exist
        for directory in [self.profiles_dir, self.exports_dir]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError as e:
                     print(f"Error creating directory {directory}: {e}. Profiles/Exports might not save.")
                     input("Press Enter to acknowledge.") # Pause so user sees the error

    # --- REMOVED select_language method ---

    def display_welcome(self):
        """Display welcome screen with ASCII art"""
        clear_screen()
        display_ascii_art(self.data_dir)
        print(self.texts["welcome"])
        input(self.texts["continue_prompt"]) # Waits for Enter

    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            clear_screen()
            print(self.texts["main_menu"])
            options = self.texts["main_menu_options"]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options))
            if choice is None: continue # Loop if user just presses Enter

            if choice == 1: # Create new persona
                self.create_persona()
            elif choice == 2: # Create random persona
                self.create_random_persona() # Call the correct method
            elif choice == 3: # Load existing persona
                self.load_persona()
            elif choice == 4: # View program information
                self.show_program_info()
            elif choice == 5: # Exit
                print("Exiting Sock Spy. Goodbye!")
                sys.exit(0)

    def create_persona(self):
        """Guide user through persona creation process"""
        self.profile = {} # Reset profile
        print("\n--- Starting New Persona Creation ---")

        # Select gender (Simple choice)
        clear_screen()
        print(self.texts["gender_select"])
        gender_options = self.texts["gender_options"]
        for i, gender in enumerate(gender_options, 1):
            print(f"{i}. {gender}")
        gender_choice = get_numeric_choice(1, len(gender_options))
        if gender_choice is None: return # Allow cancel
        # Store gender consistently (e.g., 'male', 'female') for file paths
        gender_map = {1: "male", 2: "female"}
        self.profile["gender"] = gender_map.get(gender_choice, "male") # Default if error

        # Select nationality (Simple choice)
        self.select_nationality()
        # Check if selection was cancelled or failed
        if "nationality" not in self.profile or not self.profile["nationality"]:
             print("Nationality selection is required. Aborting persona creation.")
             # Optionally pause: input(self.texts["continue_prompt"])
             return # Exit creation process

        # Select first name (Using helper)
        self.select_name(self.profile["gender"], self.profile["nationality"])
        if "first_name" not in self.profile: return # Check if selection was cancelled

        # Select last name (Using helper)
        self.select_lastname(self.profile["nationality"])
        if "last_name" not in self.profile: return # Check if selection was cancelled

        # Get age
        clear_screen()
        while True:
            try:
                age_str = get_input(self.texts["age_prompt"]).strip()
                if not age_str: return # Allow cancel
                age = int(age_str)
                if 18 <= age <= 99:
                    self.profile["age"] = age
                    break
                else:
                    print(self.texts["age_error"])
            except ValueError:
                print(self.texts["age_error"])

        # Generate username suggestions (Using helper)
        self.select_username()
        if "username" not in self.profile: return # Check if selection was cancelled

        # Get password
        clear_screen()
        while True:
            password = get_input(self.texts["password_prompt"])
            if not password: return # Allow cancel
            confirm = get_input(self.texts["password_confirm"].format('*'*len(password)) + " ") # Mask password in prompt
            if confirm.lower() in ["y", "yes"]:
                self.profile["password"] = password
                break
            elif confirm.lower() in ["n", "no"]:
                continue # Ask for password again
            else: # Handle cancel/other input
                return

        # Get platforms
        clear_screen()
        platforms_input = get_input(self.texts["platforms_prompt"])
        self.profile["platforms"] = [p.strip() for p in platforms_input.split(",") if p.strip()]

        # Select interests hierarchically
        self.select_hierarchical_interests()
        # No need to check for cancel here, skipping is handled internally

        # Select profession hierarchically
        self.select_hierarchical_profession()
        # No need to check for cancel here

        # Select location
        self.select_location()
        # No need to check for cancel here

        # Add common phrases if desired (Using helper)
        clear_screen()
        if get_input(self.texts["add_phrases_prompt"] + " ").lower() in ["y", "yes"]:
            self.select_common_phrases()

        # Add profile picture if desired (Using helper)
        clear_screen()
        if get_input(self.texts["add_picture_prompt"] + " ").lower() in ["y", "yes"]:
            self.select_profile_picture()

        # Preview profile
        self.preview_profile()

        # Edit profile if desired
        if get_input(self.texts["edit_profile_prompt"] + " ").lower() in ["y", "yes"]:
            self.edit_profile() # Use the updated edit function

        # Add appendix if desired
        clear_screen()
        if get_input(self.texts["add_appendix_prompt"] + " ").lower() in ["y", "yes"]:
            appendix = get_input(self.texts["appendix_prompt"])
            self.profile["appendix"] = appendix

        # --- Save profile ---
        clear_screen()
        # Suggest a filename based on profile name
        default_filename = f"{self.profile.get('first_name', 'profile')}_{self.profile.get('last_name', str(random.randint(100,999)))}".lower()
        filename_prompt = self.texts["filename_prompt"] + f" (Leave blank for '{default_filename}')"
        filename = get_input(filename_prompt).strip()
        if not filename:
            filename = default_filename

        # Save and Export
        saved_path = save_profile(self.profile, filename, self.profiles_dir)
        if saved_path:
            print(self.texts["save_success"].format(saved_path))
            # Export to TXT automatically after saving JSON
            exported_path = export_profile_to_txt(self.profile, filename, self.exports_dir)
            if exported_path:
                print(self.texts["export_success"].format(exported_path))
        else:
            print("Error occurred during saving.")

        input(self.texts["continue_prompt"])

    # --- SELECTION METHODS (Correctly Indented and Updated) ---


    def select_nationality(self):
        """Select nationality using a hierarchical structure (Continent -> Specific)."""
        clear_screen()
        print("Loading nationality data...")
        try:
            nationalities_data = load_json_file(os.path.join(self.data_dir, "nationalities.json"))
            if not nationalities_data or not isinstance(nationalities_data, dict):
                 raise ValueError("Nationalities data is empty or invalid.")
        except Exception as e:
            print(f"Error loading or validating nationalities.json: {e}")
            self.profile["nationality"] = None # Indicate failure
            input(self.texts["continue_prompt"])
            return

        # --- Level 1: Select Continent ---
        clear_screen()
        level_name = self.texts.get("nationality_continent", "Select continent/region for nationality:")
        print(level_name)
        continents = sorted(list(nationalities_data.keys()))
        if not continents:
            print("Error: No continents found in nationalities data.")
            self.profile["nationality"] = None
            input(self.texts["continue_prompt"])
            return

        for i, continent in enumerate(continents, 1):
            print(f"{i}. {continent}")
        print("-" * 20)

        continent_choice = get_numeric_choice(1, len(continents))
        if continent_choice is None:
            print("Nationality selection cancelled.")
            self.profile["nationality"] = None # Signal cancellation
            return

        selected_continent = continents[continent_choice - 1]
        nationality_list = nationalities_data.get(selected_continent, [])

        # --- Level 2: Select Specific Nationality ---
        if not nationality_list:
            print(f"Error: No nationalities listed for {selected_continent}.")
            self.profile["nationality"] = None
            input(self.texts["continue_prompt"])
            return

        clear_screen()
        prompt = self.texts.get("nationality_specific", "Select a specific nationality:")
        specific_nationalities = sorted(nationality_list)

        while True:
            selected_item, action = handle_dynamic_list_selection(
                full_list=specific_nationalities,
                texts=self.texts,
                prompt_msg=prompt,
                initial_show=10, # Show more nationalities at once
                increment=10,
                allow_skip=False # Must select a specific nationality
            )

            if action == 'selected':
                self.profile["nationality"] = selected_item.lower() # Store lowercase
                print(f"\nSelected Nationality: {selected_item}")
                # input(self.texts["continue_prompt"]) # Optional pause
                break
            elif action == 'back': # User cancelled the specific selection
                print("Nationality selection cancelled.")
                self.profile["nationality"] = None # Signal cancellation
                break
            # 'show_more', 'regenerate' handled internally

    def select_name(self, gender, nationality):
        """Select a first name using dynamic list helper"""
        clear_screen()
        prompt = self.texts["name_select"]
        names_file = os.path.join(self.data_dir, "names", gender, f"{nationality}.txt")
        try:
            full_list = load_data_file(names_file)
            if not full_list:
                print(f"Warning: No names found for {gender}/{nationality}. Using generic names.")
                full_list = ["Alex", "Jamie", "Chris", "Pat", "Sam"] # Fallback
        except Exception as e:
            print(f"Warning: Error loading name file {names_file}: {e}. Using generic names.")
            full_list = ["Alex", "Jamie", "Chris", "Pat", "Sam"] # Fallback

        while True:
            selected_item, action = handle_dynamic_list_selection(
                full_list=full_list, texts=self.texts, prompt_msg=prompt,
                initial_show=7, increment=7, allow_skip=False # Show a bit more
            )
            if action == 'selected':
                self.profile["first_name"] = selected_item
                break
            elif action == 'back': # Handle cancellation
                 print("Name selection cancelled.")
                 # Remove key to signal cancellation upstream if needed
                 self.profile.pop("first_name", None)
                 break
            # 'show_more', 'regenerate' handled internally

    def select_lastname(self, nationality):
        """Select a last name using dynamic list helper"""
        # This method was incorrectly indented inside select_name before
        clear_screen()
        prompt = self.texts["lastname_select"]
        lastnames_file = os.path.join(self.data_dir, "last_names", f"{nationality}.txt")
        try:
            full_list = load_data_file(lastnames_file)
            if not full_list:
                print(f"Warning: No last names found for {nationality}. Using generic last names.")
                full_list = ["Smith", "Jones", "Lee", "Garcia", "Chen"] # Fallback
        except Exception as e:
            print(f"Warning: Error loading last name file {lastnames_file}: {e}. Using generic names.")
            full_list = ["Smith", "Jones", "Lee", "Garcia", "Chen"] # Fallback

        while True:
            selected_item, action = handle_dynamic_list_selection(
                full_list=full_list, texts=self.texts, prompt_msg=prompt,
                initial_show=7, increment=7, allow_skip=False
            )
            if action == 'selected':
                self.profile["last_name"] = selected_item
                break
            elif action == 'back':
                 print("Last name selection cancelled.")
                 self.profile.pop("last_name", None)
                 break

    def select_username(self):
        """Generate and select username, allowing custom input or selection"""
        # This method was incorrectly indented inside select_name before
        clear_screen()
        while True:
            print(self.texts["username_suggestions"])
            try:
                # Ensure required profile fields exist before generating
                first = self.profile.get("first_name", "User")
                last = self.profile.get("last_name", str(random.randint(100,999)))
                age = self.profile.get("age", random.randint(18,99))
                suggestions = generate_username_suggestions(first, last, age)
            except Exception as e:
                print(f"Warning: Could not generate username suggestions ({e}).")
                suggestions = [f"{self.profile.get('first_name','user').lower()}{random.randint(10,99)}"]

            if not suggestions: # Handle case where generation fails completely
                 print("No suggestions could be generated.")
                 suggestions = [] # Ensure it's a list

            options = suggestions + ["Enter custom username"]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options))
            if choice is None: # User cancelled
                print("Username selection cancelled.")
                self.profile.pop("username", None)
                return # Exit method

            if choice <= len(suggestions): # Selected a suggestion
                username = suggestions[choice - 1]
                confirm = get_input(self.texts["username_confirm"].format(username) + " ").lower()
                if confirm in ["y", "yes"]:
                    self.profile["username"] = username
                    break # Success
                # If no, loop continues to show suggestions again
            else: # Selected "Enter custom username"
                username = get_input(self.texts["username_prompt"]).strip()
                if not username: # User entered blank custom name
                     print("Custom username cannot be empty. Please try again.")
                     input(self.texts["continue_prompt"]) # Pause
                     continue # Go back to showing suggestions

                confirm = get_input(self.texts["username_confirm"].format(username) + " ").lower()
                if confirm in ["y", "yes"]:
                    self.profile["username"] = username
                    break # Success
                # If no, loop continues to show suggestions again

    def select_hierarchical_interests(self):
        """Select interests using hierarchical structure and new options"""
        # This method was incorrectly indented inside select_name before
        clear_screen()
        print("Loading interests data...")
        try:
            interests_data = load_json_file(os.path.join(self.data_dir, "interests.json"))
            if not interests_data or not isinstance(interests_data, dict):
                 raise ValueError("Interests data empty or invalid.")
        except Exception as e:
            print(f"Warning: Could not load interests data ({e}). Skipping interests selection.")
            self.profile["interests"] = []
            input(self.texts["continue_prompt"])
            return

        current_level_data = interests_data
        path = []
        level_prompt_keys = ["interests_select", "interests_subcategory", "interests_specific"] # Simplified level names
        level = 0

        while isinstance(current_level_data, dict):
            clear_screen()
            level_name = self.texts.get(level_prompt_keys[level], f"Select Interest Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options: break

            selected_option = None
            action = None

            if level == 0: # First level (Category) - Show All, No Skip
                print(level_name)
                for i, option in enumerate(options, 1): print(f"{i}. {option}")
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                if choice is None: action = 'back'
                else: selected_option, action = options[choice - 1], 'selected'
            else: # Subsequent levels - Dynamic List with Skip
                selected_option, action = handle_dynamic_list_selection(
                    full_list=options, texts=self.texts, prompt_msg=level_name,
                    initial_show=10, increment=10, allow_skip=True
                )

            # Process Action/Selection
            if action == 'selected':
                path.append(selected_option)
                next_level_data = current_level_data.get(selected_option)
                if isinstance(next_level_data, (dict, list)):
                    current_level_data = next_level_data
                    level += 1
                else: break # End of branch
            elif action == 'skip': break # Stop navigating deeper
            elif action == 'back': # User cancelled
                if level == 0: self.profile["interests"] = [] # Cancelled at start
                # Otherwise, loop breaks and uses current path/data
                break
            # 'regenerate', 'show_more' handled internally

        # --- Final Level: Specific Interests (Multi-select) ---
        if isinstance(current_level_data, list):
            specific_interests = sorted(current_level_data)
            if specific_interests:
                # Use the manual multi-select loop pattern here
                self._handle_multi_select_final_level(
                    full_list=specific_interests,
                    prompt=self.texts["interests_specific"],
                    profile_key="interests",
                    max_select=5
                )
            else:
                print("No specific interests found at this level.")
                self.profile["interests"] = [] # Or maybe use path? For now, empty.
        elif not self.profile.get("interests"): # If stopped before reaching list
             print("No specific interests selected.")
             # Decide: use path? For now, keep empty if nothing specific selected.
             self.profile["interests"] = []

        # Ensure key exists even if empty
        if "interests" not in self.profile:
             self.profile["interests"] = []

        # input(self.texts["continue_prompt"]) # Pause only if needed

    def select_hierarchical_profession(self):
        """Select profession using hierarchical structure and new options"""
        # This method was incorrectly indented inside select_name before
        clear_screen()
        print("Loading professions data...")
        try:
            professions_data = load_json_file(os.path.join(self.data_dir, "professions.json"))
            if not professions_data or not isinstance(professions_data, dict):
                 raise ValueError("Professions data empty or invalid.")
        except Exception as e:
            print(f"Warning: Could not load professions data ({e}). Setting profession to 'Unspecified'.")
            self.profile["profession"] = "Unspecified"
            input(self.texts["continue_prompt"])
            return

        current_level_data = professions_data
        path = []
        level_prompt_keys = ["profession_category", "profession_subcategory", "profession_specific"]
        level = 0

        while isinstance(current_level_data, dict):
            clear_screen()
            level_name = self.texts.get(level_prompt_keys[level], f"Select Profession Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options: break

            selected_option = None
            action = None

            if level == 0: # First level - Show All, No Skip
                print(level_name)
                for i, option in enumerate(options, 1): print(f"{i}. {option}")
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                if choice is None: action = 'back'
                else: selected_option, action = options[choice - 1], 'selected'
            else: # Subsequent levels - Dynamic List with Skip
                selected_option, action = handle_dynamic_list_selection(
                    full_list=options, texts=self.texts, prompt_msg=level_name,
                    initial_show=10, increment=10, allow_skip=True
                )

            # Process Action/Selection
            if action == 'selected':
                path.append(selected_option)
                next_level_data = current_level_data.get(selected_option)
                if isinstance(next_level_data, (dict, list)):
                    current_level_data = next_level_data
                    level += 1
                else: break
            elif action == 'skip': break
            elif action == 'back':
                if level == 0: self.profile["profession"] = "Unspecified"
                # Otherwise break and use path if available
                break

        # --- Final Level: Specific Profession (Single Select) ---
        final_profession = None
        if isinstance(current_level_data, list):
            specific_professions = sorted(current_level_data)
            if specific_professions:
                clear_screen()
                level_name = self.texts.get(level_prompt_keys[level], f"Select Final Level {level+1}:")
                # Use single-select helper for the final choice
                selected_final, action = handle_dynamic_list_selection(
                    full_list=specific_professions, texts=self.texts,
                    prompt_msg=level_name, allow_skip=True
                )
                if action == 'selected':
                    final_profession = selected_final
            else:
                 print("No specific professions found at this level.")

        # --- Assign Profession ---
        if final_profession:
            self.profile["profession"] = final_profession
        elif path: # Use the last category selected if no specific item chosen/found
            self.profile["profession"] = path[-1]
        elif "profession" not in self.profile: # Ensure key exists
             self.profile["profession"] = "Unspecified"

        print(f"\nSelected Profession: {self.profile['profession']}")
        # input(self.texts["continue_prompt"]) # Pause only if needed


    def select_location(self):
        """Select location with hierarchical structure and new options"""
        # This function was previously outside the class
        clear_screen()
        print("Loading location data...")
        try:
            locations_data = load_json_file(os.path.join(self.data_dir, "locations.json"))
            if not locations_data or not isinstance(locations_data, dict):
                 raise ValueError("Location data is empty or invalid.")
        except Exception as e:
            print(f"Error loading or validating locations.json: {e}")
            self.profile["location"] = "Earth"
            input(self.texts["continue_prompt"])
            return

        current_level_data = locations_data
        path = []
        level_prompt_keys = ["location_continent", "location_country", "location_region", "location_city", "location_neighborhood"]
        level = 0

        while isinstance(current_level_data, dict):
            clear_screen()
            level_name = self.texts.get(level_prompt_keys[level], f"Select Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options: break

            selected_option = None
            action = None

            if level == 0: # Continents - Show All, No Skip
                print(level_name)
                for i, option in enumerate(options, 1): print(f"{i}. {option}")
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                if choice is None: action = 'back'
                else: selected_option, action = options[choice - 1], 'selected'
            else: # Subsequent levels - Dynamic List with Skip
                selected_option, action = handle_dynamic_list_selection(
                    full_list=options, texts=self.texts, prompt_msg=level_name,
                    initial_show=10, increment=10, allow_skip=True
                )

            # Process Action/Selection
            if action == 'selected':
                path.append(selected_option)
                next_level_data = current_level_data.get(selected_option)
                if isinstance(next_level_data, (dict, list)):
                    current_level_data = next_level_data
                    level += 1
                else: break
            elif action == 'skip': break
            elif action == 'back':
                if level == 0: self.profile["location"] = "Undetermined"
                break

        # Final Level (e.g., Neighborhoods) - Single Select (Optional)
        if isinstance(current_level_data, list):
            final_options = sorted(current_level_data)
            if final_options:
                clear_screen()
                level_name = self.texts.get(level_prompt_keys[level], f"Select Final Level {level+1}:")
                selected_final, action = handle_dynamic_list_selection(
                    full_list=final_options, texts=self.texts,
                    prompt_msg=level_name + " (Optional)", allow_skip=True
                )
                if action == 'selected':
                    path.append(selected_final)
            # else: print("No specific options listed at this final level.") # Optional msg

        # Format Location String
        if path:
            self.profile["location"] = ", ".join(reversed(path))
            print(f"\nSelected Location: {self.profile['location']}")
        elif 'location' not in self.profile:
            print("\nNo specific location selected.")
            self.profile["location"] = "Unknown Location"

        # input(self.texts["continue_prompt"]) # Pause only if needed

    def select_common_phrases(self):
        """Select common phrases using manual loop with actions"""
        # This function was previously outside the class
        clear_screen()
        language_file = "english.txt" # Simplified or use nationality logic
        phrases_file = os.path.join(self.data_dir, "common_phrases", language_file)
        try:
            full_list = load_data_file(phrases_file)
            if not full_list:
                print(f"Warning: No common phrases found in {phrases_file}. Skipping.")
                self.profile["common_phrases"] = []
                input(self.texts["continue_prompt"])
                return
        except Exception as e:
            print(f"Warning: Error loading phrases file {phrases_file}: {e}. Skipping.")
            self.profile["common_phrases"] = []
            input(self.texts["continue_prompt"])
            return

        # Use the reusable multi-select handler
        self._handle_multi_select_final_level(
             full_list=full_list,
             prompt=self.texts["common_phrases_select"],
             profile_key="common_phrases",
             max_select=3
        )
        if "common_phrases" in self.profile:
             print(f"Selected phrases: {self.profile['common_phrases']}")
        # input(self.texts["continue_prompt"]) # Pause only if needed

    def select_profile_picture(self):
        """Select a profile picture URL using dynamic helper"""
        # Updated to use the helper
        clear_screen()
        prompt = "Select a profile picture:"
        pictures_file = os.path.join(self.data_dir, "profile_pictures.txt")
        try:
            pictures = load_data_file(pictures_file)
            if not pictures:
                print("Warning: profile_pictures.txt is empty. Skipping.")
                self.profile.pop("profile_picture", None)
                input(self.texts["continue_prompt"])
                return

            # Filter by gender (Handles /men/ and /women/)
            gender = self.profile.get("gender", "neutral")
            keywords = []
            if gender == "male": keywords = ["/male/", "/men/"]
            elif gender == "female": keywords = ["/female/", "/women/"]
            full_list = [pic for pic in pictures if any(kw in pic.lower() for kw in keywords)]

            if not full_list: # Fallback if no gender match
                print(f"No pictures found for gender '{gender}'. Showing all.")
                full_list = pictures

        except Exception as e:
            print(f"Warning: Error loading profile pictures file: {e}. Skipping.")
            self.profile.pop("profile_picture", None)
            input(self.texts["continue_prompt"])
            return

        while True:
            selected_item, action = handle_dynamic_list_selection(
                full_list=full_list, texts=self.texts, prompt_msg=prompt,
                initial_show=5, increment=5, allow_skip=False
            )
            if action == 'selected':
                self.profile["profile_picture"] = selected_item
                break
            elif action == 'back':
                 print("Profile picture selection cancelled.")
                 self.profile.pop("profile_picture", None)
                 break

    # --- Helper for Multi-Select Lists (like interests, phrases) ---
    def _handle_multi_select_final_level(self, full_list, prompt, profile_key, max_select=5):
        """Internal helper for multi-select lists with actions"""
        clear_screen()
        initial_show = 10
        increment = 5
        available_indices = list(range(len(full_list)))
        displayed_indices = random.sample(available_indices, min(initial_show, len(full_list)))
        displayed_indices.sort()

        while True:
            clear_screen()
            print(prompt)
            current_options_map = {i + 1: full_list[idx] for i, idx in enumerate(displayed_indices)}
            for num, item in current_options_map.items(): print(f"{num}. {item}")

            print("-" * 20)
            option_offset = len(current_options_map)
            show_more_opt_num = option_offset + 1
            regenerate_opt_num = option_offset + 2
            current_max_action_num = option_offset

            text_show_more = self.texts.get("show_more_options", "Show More Options")
            text_regenerate = self.texts.get("regenerate_options", "Show New Options")
            text_invalid_choice = self.texts.get("invalid_choice", "Invalid choice.")

            can_show_more = len(displayed_indices) < len(full_list)
            if can_show_more:
                print(f"{show_more_opt_num}. {text_show_more}")
                current_max_action_num = show_more_opt_num
            else: show_more_opt_num = -1

            print(f"{regenerate_opt_num}. {text_regenerate}")
            current_max_action_num = regenerate_opt_num

            print(f"\nEnter numbers (1-{len(current_options_map)}) separated by commas (max {max_select}), or choose an action:")
            user_input = get_input("> ").strip()

            if not user_input: # Select none
                self.profile[profile_key] = []
                print("No items selected.")
                break

            try: # Check for actions first
                action_choice = int(user_input)
                if can_show_more and action_choice == show_more_opt_num:
                    remaining_indices = [i for i in available_indices if i not in displayed_indices]
                    if remaining_indices:
                        num_to_add = min(increment, len(remaining_indices))
                        displayed_indices.extend(random.sample(remaining_indices, num_to_add))
                        displayed_indices.sort()
                    continue
                elif action_choice == regenerate_opt_num:
                    displayed_indices = random.sample(available_indices, min(initial_show, len(full_list)))
                    displayed_indices.sort()
                    continue
            except ValueError: pass # Not a single number action

            try: # Process item selection
                choices_str = [x.strip() for x in user_input.split(',') if x.strip()]
                item_choices = [int(x) for x in choices_str]

                selected_items = []
                valid = True
                for choice_num in item_choices:
                    if choice_num in current_options_map:
                        selected_items.append(current_options_map[choice_num])
                    else:
                        valid = False; break

                if not valid:
                    print("Invalid selection number detected. Please try again.")
                    input(self.texts["continue_prompt"]); continue

                self.profile[profile_key] = selected_items[:max_select]
                break
            except ValueError:
                print(text_invalid_choice + " Please enter valid item numbers or an action number.")
                input(self.texts["continue_prompt"]); continue

    # --- Other Methods (preview_profile, etc.) ---

    def preview_profile(self):
        """Display a preview of the generated or loaded profile"""
        clear_screen()
        print(self.texts["profile_preview"])
        print("\n" + "=" * 40 + "\n")
        # Use .get with defaults for safety
        print(f"Name: {self.profile.get('first_name', 'N/A')} {self.profile.get('last_name', 'N/A')}")
        print(f"Gender: {self.profile.get('gender', 'N/A').capitalize()}")
        print(f"Age: {self.profile.get('age', 'N/A')}")
        print(f"Nationality: {self.profile.get('nationality', 'N/A').capitalize()}")
        print(f"Location: {self.profile.get('location', 'N/A')}")
        print(f"Username: {self.profile.get('username', 'N/A')}")
        print(f"Password: {'*' * len(self.profile.get('password', '')) if self.profile.get('password') else 'N/A'}") # Mask password

        platforms = self.profile.get("platforms", [])
        if platforms:
            print("\nPlatforms:")
            for platform in platforms: print(f"- {platform}")

        interests = self.profile.get("interests", [])
        if interests:
            print("\nInterests:")
            for interest in interests: print(f"- {interest}")

        print(f"\nProfession: {self.profile.get('profession', 'N/A')}")

        common_phrases = self.profile.get("common_phrases", [])
        if common_phrases:
            print("\nCommon Phrases:")
            for phrase in common_phrases: print(f"- {phrase}")

        profile_picture = self.profile.get("profile_picture")
        if profile_picture:
            print(f"\nProfile Picture: {profile_picture}")

        appendix = self.profile.get("appendix")
        if appendix:
            print(f"\nAppendix: {appendix}")

        print("\n" + "=" * 40 + "\n")
        input(self.texts["continue_prompt"])

    def edit_profile(self):
        """Allow user to edit profile fields (improved version)"""
        while True:
            clear_screen()
            print("--- Edit Profile ---")
            editable_fields = {}
            i = 1
            # Display current values nicely, map number to key
            for key, value in self.profile.items():
                 display_value = ', '.join(map(str, value)) if isinstance(value, (list, tuple)) else value
                 # Mask password during edit display
                 if key == 'password': display_value = '*' * len(str(display_value))
                 print(f"{i}. {key.replace('_', ' ').capitalize()}: {display_value}")
                 editable_fields[i] = key
                 i += 1

            print(f"\n{i}. Finish Editing")
            prompt = self.texts.get("edit_field_prompt", "Enter field number to edit, or press Enter to finish:")
            field_choice_str = get_input(prompt + " ")

            if not field_choice_str: break # Finish if Enter pressed

            try:
                field_choice = int(field_choice_str)
                if field_choice == i: break # Finish Editing option
                if field_choice in editable_fields:
                    field_to_edit = editable_fields[field_choice]
                    current_value = self.profile[field_to_edit]
                    # Use specific prompts for different types
                    if isinstance(current_value, list):
                        print(f"\nEditing '{field_to_edit.replace('_', ' ').capitalize()}'. Current: {current_value}")
                        print("Enter new values separated by commas (or leave blank to keep current):")
                        new_value_str = get_input("> ")
                        if new_value_str.strip():
                            self.profile[field_to_edit] = [v.strip() for v in new_value_str.split(',') if v.strip()]
                    elif isinstance(current_value, int):
                        print(f"\nEditing '{field_to_edit.replace('_', ' ').capitalize()}'. Current: {current_value}")
                        print("Enter new numeric value:")
                        while True:
                            new_value_str = get_input("> ")
                            if not new_value_str.strip(): break # Allow blank to keep current
                            try:
                                new_value = int(new_value_str)
                                if field_to_edit == 'age' and not (18 <= new_value <= 99):
                                     print(self.texts["age_error"]); continue
                                self.profile[field_to_edit] = new_value; break
                            except ValueError: print("Invalid number.")
                    else: # Assume string
                        print(f"\nEditing '{field_to_edit.replace('_', ' ').capitalize()}'.") # Don't show password
                        new_value = get_input(self.texts["edit_value_prompt"] + " ")
                        self.profile[field_to_edit] = new_value
                    print("... Updated.")
                    time.sleep(0.7) # Brief pause
                else:
                    print(self.texts["invalid_choice"]); time.sleep(1)
            except ValueError:
                print(self.texts["invalid_choice"]); time.sleep(1)
        # Preview after finishing all edits?
        # self.preview_profile()

    def load_persona(self):
        """Load an existing persona from file"""
        clear_screen()
        if not os.path.exists(self.profiles_dir):
            print(f"Profiles directory '{self.profiles_dir}' not found.")
            input(self.texts["continue_prompt"]); return

        try:
             profiles = [f for f in os.listdir(self.profiles_dir) if f.endswith('.json')]
        except OSError as e:
             print(f"Error accessing profiles directory: {e}")
             input(self.texts["continue_prompt"]); return

        if not profiles:
            print(self.texts["no_personas_found"])
            input(self.texts["continue_prompt"]); return

        print(self.texts["select_persona"])
        for i, profile_filename in enumerate(profiles, 1):
            print(f"{i}. {profile_filename[:-5]}")

        choice = get_numeric_choice(1, len(profiles))
        if choice is None: print("Loading cancelled."); return

        selected_filename = profiles[choice - 1]
        profile_path = os.path.join(self.profiles_dir, selected_filename)

        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
            print(f"\n{self.texts['persona_loaded']}")
            input(self.texts["continue_prompt"])
            # Pass name for export defaults etc.
            self.persona_options(profile_path, selected_filename[:-5])
        except FileNotFoundError:
            print(f"Error: Profile file '{selected_filename}' not found.")
            input(self.texts["continue_prompt"])
        except json.JSONDecodeError:
            print(f"Error: Profile file '{selected_filename}' is corrupted.")
            input(self.texts["continue_prompt"])
        except Exception as e:
            print(f"An unexpected error occurred loading profile: {e}")
            input(self.texts["continue_prompt"])

    def persona_options(self, profile_path, profile_name):
        """Display options for loaded persona"""
        while True:
            clear_screen()
            print(f"--- Options for Persona: {profile_name} ---")
            # print(self.texts["persona_options"]) # Generic title if preferred
            options_list = self.texts["persona_options_list"]
            for i, option in enumerate(options_list, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options_list))
            if choice is None: continue # Loop on empty input

            if choice == 1: # View details
                self.preview_profile()
            elif choice == 2: # Edit persona
                self.edit_profile()
                # Save changes after editing
                try:
                    with open(profile_path, "w", encoding="utf-8") as f:
                        json.dump(self.profile, f, indent=2, ensure_ascii=False)
                    print("Changes saved.")
                except IOError as e:
                     print(f"Error saving changes: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 3: # Export persona as JSON
                if not os.path.exists(self.exports_dir): os.makedirs(self.exports_dir)
                export_filename = f"{profile_name}_export_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                export_path = os.path.join(self.exports_dir, export_filename)
                try:
                    with open(export_path, "w", encoding="utf-8") as f:
                        json.dump(self.profile, f, indent=2, ensure_ascii=False)
                    print(self.texts["export_success"].format(export_path))
                except IOError as e: print(f"Error exporting JSON: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 4: # Export persona as TXT
                if not os.path.exists(self.exports_dir): os.makedirs(self.exports_dir)
                try:
                    txt_filepath = export_profile_to_txt(self.profile, profile_name, self.exports_dir)
                    if txt_filepath: print(self.texts["export_success"].format(txt_filepath))
                    else: print("Error during TXT export.")
                except Exception as e: print(f"Error exporting TXT: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 5: # Delete persona
                confirm = get_input(self.texts["confirm_delete"] + " ").lower()
                if confirm in ["y", "yes"]:
                    try:
                        os.remove(profile_path)
                        print(self.texts["deleted_success"])
                        self.profile = {} # Clear loaded profile
                        input(self.texts["continue_prompt"])
                        break # Exit persona options menu
                    except OSError as e:
                        print(f"Error deleting file: {e}")
                        input(self.texts["continue_prompt"])
                else:
                    print("Deletion cancelled.")
                    input(self.texts["continue_prompt"])
            elif choice == 6: # Back to main menu
                break

    def create_random_persona(self):
        """Creates a persona with randomly selected attributes based on user-chosen detail level and shows the process."""
        clear_screen()
        print(self.texts["random_level_select"])
        level_options = self.texts["random_level_options"]
        for option in level_options: print(option)

        level_choice = get_numeric_choice(1, len(level_options))
        if level_choice is None:
            print("Random persona generation cancelled.")
            input(self.texts["continue_prompt"]) # Pause before returning
            return

        clear_screen()
        print("\n--- Generating Random Persona ---")
        print("Please wait...\n")
        self.profile = {} # Start fresh profile
        pause_time = 0.4 # Seconds to pause between steps for visibility

        # --- Load Data Files (with simplified warnings) ---
        print("Loading data sets...")
        # Nationalities (Now uses JSON)
        nationalities_data = load_json_file(os.path.join(self.data_dir, "nationalities.json"))
        if not nationalities_data: print("Warning: Nationalities data missing or empty.")

        # Professions (JSON)
        professions_data = load_json_file(os.path.join(self.data_dir, "professions.json"))
        if not professions_data: print("Warning: Professions data missing or empty.")

        # Locations (JSON)
        locations_data = load_json_file(os.path.join(self.data_dir, "locations.json"))
        if not locations_data: print("Warning: Locations data missing or empty.")

        # Interests (JSON)
        interests_data = load_json_file(os.path.join(self.data_dir, "interests.json"))
        if not interests_data: print("Warning: Interests data missing or empty.")

        # Phrases (TXT)
        phrases_data = load_data_file(os.path.join(self.data_dir, "common_phrases", "english.txt"))
        if not phrases_data: print("Warning: Common phrases file missing or empty.")

        # Pictures (TXT)
        pictures_data = load_data_file(os.path.join(self.data_dir, "profile_pictures.txt"))
        if not pictures_data: print("Warning: Profile pictures file missing or empty.")

        time.sleep(pause_time * 2) # Longer pause after loading

        # --- Level 1: Minimal ---
        print("\n--- Generating Minimal Details ---")

        # Gender
        print(self.texts.get("random_generating","Generating {item}...").format(item="Gender"))
        self.profile["gender"] = random.choice(["male", "female"])
        print(f"-> Gender: {self.profile['gender'].capitalize()}")
        time.sleep(pause_time)

        # Nationality (using hierarchical data)
        print(self.texts.get("random_generating","Generating {item}...").format(item="Nationality"))
        selected_nationality = None
        if nationalities_data:
            item, _ = get_random_hierarchical_item(nationalities_data) # Get nationality string
            selected_nationality = item
        # Fallback if data missing or random selection fails
        self.profile["nationality"] = selected_nationality.lower() if selected_nationality else "american"
        print(f"-> Nationality: {self.profile['nationality'].capitalize()}")
        time.sleep(pause_time)

        # Age
        print(self.texts.get("random_generating","Generating {item}...").format(item="Age"))
        self.profile["age"] = random.randint(18, 70)
        print(f"-> Age: {self.profile['age']}")
        time.sleep(pause_time)

        # Name & Lastname (based on gender/nationality)
        print(self.texts.get("random_generating","Generating {item}...").format(item="Name"))
        first_name = "Alex" # Default fallback
        try:
            names_file = os.path.join(self.data_dir, "names", self.profile["gender"], f"{self.profile['nationality']}.txt")
            names = load_data_file(names_file)
            if names: first_name = random.choice(names)
        except Exception: pass # Keep fallback on error
        self.profile["first_name"] = first_name
        print(f"-> First Name: {self.profile['first_name']}")
        time.sleep(pause_time)

        print(self.texts.get("random_generating","Generating {item}...").format(item="Last Name"))
        last_name = "Smith" # Default fallback
        try:
            lastnames_file = os.path.join(self.data_dir, "last_names", f"{self.profile['nationality']}.txt")
            lastnames = load_data_file(lastnames_file)
            if lastnames: last_name = random.choice(lastnames)
        except Exception: pass # Keep fallback on error
        self.profile["last_name"] = last_name
        print(f"-> Last Name: {self.profile['last_name']}")
        time.sleep(pause_time)

        # Profession (using hierarchical data)
        print(self.texts.get("random_generating","Generating {item}...").format(item="Profession"))
        selected_profession = "Unspecified" # Default fallback
        if professions_data:
            item, path = get_random_hierarchical_item(professions_data)
            # Prefer specific item, fallback to last category in path
            selected_profession = item if item else (path[-1] if path else "Unspecified")
        self.profile["profession"] = selected_profession
        print(f"-> Profession: {self.profile['profession']}")
        time.sleep(pause_time)

        # --- Level 2: Standard ---
        if level_choice >= 2:
            print("\n--- Adding Standard Details ---")

            # Location (Basic - Continent, Country)
            print(self.texts.get("random_generating","Generating {item}...").format(item="Basic Location"))
            location = "Earth" # Default fallback
            if locations_data:
                 _ , path = get_random_hierarchical_item(locations_data)
                 # Take Continent, Country if path is long enough
                 parts = path[:2]
                 if parts: location = ", ".join(reversed(parts))
            self.profile["location"] = location
            print(f"-> Location: {self.profile['location']}")
            time.sleep(pause_time)

            # Username
            print(self.texts.get("random_generating","Generating {item}...").format(item="Username"))
            username = f"{self.profile.get('first_name','user').lower()}{random.randint(10,99)}" # Fallback
            try:
                suggestions = generate_username_suggestions(self.profile["first_name"], self.profile["last_name"], self.profile["age"])
                if suggestions: username = random.choice(suggestions)
            except Exception: pass # Keep fallback on error
            self.profile["username"] = username
            print(f"-> Username: {self.profile['username']}")
            time.sleep(pause_time)

            # Password
            print(self.texts.get("random_generating","Generating {item}...").format(item="Password"))
            self.profile["password"] = generate_random_password()
            print(f"-> Password: {'*' * len(self.profile['password'])}") # Masked
            time.sleep(pause_time)

        # --- Level 3: Detailed ---
        if level_choice >= 3:
            print("\n--- Adding Detailed Information ---")

            # Location (Specific - Up to City level)
            print(self.texts.get("random_generating","Generating {item}...").format(item="Specific Location"))
            if locations_data:
                 item, path = get_random_hierarchical_item(locations_data) # Get full path + item
                 if item: path.append(item) # Add neighborhood/final item if selected
                 parts = path[:4] # Limit to ~City level depth
                 if parts: # Overwrite basic location only if specific path found
                     self.profile["location"] = ", ".join(reversed(parts))
                 # else keep the basic location from Level 2
            # else keep basic location
            print(f"-> Refined Location: {self.profile['location']}")
            time.sleep(pause_time)

            # Platforms
            print(self.texts.get("random_generating","Generating {item}...").format(item="Platforms"))
            possible = ["Twitter", "Facebook", "Instagram", "Reddit", "LinkedIn", "TikTok", "Pinterest", "YouTube", "Discord", "Telegram", "Snapchat", "Mastodon", "Bluesky"]
            self.profile["platforms"] = random.sample(possible, random.randint(1, 4))
            print(f"-> Platforms: {', '.join(self.profile['platforms'])}")
            time.sleep(pause_time)

            # Interests (using hierarchical data)
            print(self.texts.get("random_generating","Generating {item}...").format(item="Interests"))
            selected_interests = []
            if interests_data:
                 # Try getting 3 distinct random interests for better variety
                 attempts = 0
                 while len(selected_interests) < 3 and attempts < 10:
                     item, _ = get_random_hierarchical_item(interests_data)
                     if item and item not in selected_interests:
                         selected_interests.append(item)
                     attempts += 1
            self.profile["interests"] = selected_interests[:5] # Ensure max 5, even if loop found fewer
            print(f"-> Interests: {', '.join(self.profile.get('interests',[]))}")
            time.sleep(pause_time)

        # --- Level 4: Full ---
        if level_choice >= 4:
            print("\n--- Adding Final Touches ---")

            # Common Phrases
            print(self.texts.get("random_generating","Generating {item}...").format(item="Common Phrases"))
            if phrases_data:
                self.profile["common_phrases"] = random.sample(phrases_data, min(len(phrases_data), random.randint(1, 3)))
            else: self.profile["common_phrases"] = []
            print(f"-> Common Phrases: {len(self.profile.get('common_phrases',[]))} selected")
            time.sleep(pause_time)

            # Profile Picture (Gender specific)
            print(self.texts.get("random_generating","Generating {item}...").format(item="Profile Picture"))
            picture_selected = False
            if pictures_data:
                # Use the correct paths based on randomuser.me URLs
                gender_path = "/men/" if self.profile["gender"] == "male" else "/women/"
                gender_pics = [p for p in pictures_data if gender_path in p.lower()]
                if gender_pics:
                    self.profile["profile_picture"] = random.choice(gender_pics)
                    picture_selected = True
                elif pictures_data: # Fallback to any picture if no gender match
                    self.profile["profile_picture"] = random.choice(pictures_data)
                    picture_selected = True
            print(f"-> Profile Picture Added: {'Yes' if picture_selected else 'No'}")
            time.sleep(pause_time)

            # Optional: Add a basic Biography?
            # print(self.texts.get("random_generating","Generating {item}...").format(item="Biography"))
            # self.profile["biography"] = f"A {self.profile['age']}-year-old {self.profile['profession']} from {self.profile['location']} interested in {', '.join(self.profile.get('interests', ['various things']))[:50]}..."
            # print("-> Basic Biography Added")
            # time.sleep(pause_time)


        # --- Completion ---
        print(f"\n{self.texts['random_generation_complete']}")
        input(self.texts["continue_prompt"]) # Pause before showing preview

        self.preview_profile() # Show the generated profile

        # --- Ask to Save ---
        save_choice = get_input(self.texts.get("confirm_save_random", "Save this profile? (y/n): ")).lower()
        if save_choice in ["y", "yes"]:
            clear_screen()
            default_filename = f"{self.profile.get('first_name', 'random')}_{self.profile.get('last_name', 'profile')}".lower().replace(" ","_")
            filename_prompt = self.texts["filename_prompt"] + f" (Leave blank for '{default_filename}')"
            filename = get_input(filename_prompt).strip()
            if not filename: filename = default_filename

            saved_path = save_profile(self.profile, filename, self.profiles_dir)
            if saved_path:
                 print(self.texts["save_success"].format(saved_path))
                 exported_path = export_profile_to_txt(self.profile, filename, self.exports_dir)
                 if exported_path: print(self.texts["export_success"].format(exported_path))
            else: print("Error occurred during saving.")
            input(self.texts["continue_prompt"])
        else:
            print("Profile not saved.")
            input(self.texts["continue_prompt"])


    def show_program_info(self):
        """Display program information"""
        clear_screen()
        print(self.texts["program_info"])
        input(self.texts["continue_prompt"])

# --- Main Execution ---
def main():
    app = SockSpy()
    # app.select_language() # REMOVED THIS LINE
    app.display_welcome() # Start with welcome screen
    app.main_menu()       # Proceed to main menu

if __name__ == "__main__":
    main()
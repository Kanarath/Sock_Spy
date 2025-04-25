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
    # load_hierarchical_data, # Likely not needed anymore
    generate_random_password,
    get_random_hierarchical_item,
    handle_dynamic_list_selection,
    load_data_file,
    FILE_NOT_FOUND,
    FILE_EMPTY,
)

# English texts ONLY
# fmt: off
TEXTS = {
    "en": {
        "welcome": "Welcome to Sock Spy: OSINT Sock Puppet Generator",
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
        "password_method_select": "How do you want to set the password?",
        "password_method_options": ["Enter manually", "Generate random password"],
        "password_length_select": "Select desired password length:",
        "password_length_options": ["Standard (12 characters)", "Strong (24 characters)", "Very Strong (32 characters)"],
        "password_generated_confirm": "Generated password: {} Confirm? (y/n):", # NOTE: Password isn't shown here, just confirmation text
        "password_prompt": "Enter a password for the persona:",
        "password_confirm": "Confirm password '{}'? (y/n):", # NOTE: Password shown as '*' here
        "platforms_prompt": "Enter comma-separated list of platforms (e.g., Twitter, Facebook, Instagram):",
        "add_picture_prompt": "Add profile picture? (y/n):",
        "add_phrases_prompt": "Add common phrases? (y/n):",
        "profile_preview": "Generated Profile Preview:",
        "edit_profile_prompt": "Do you want to edit any fields? (y/n):",
        "edit_field_prompt": "Enter the number of the field to edit (or press Enter to finish):",
        "edit_value_prompt": "Enter the new value:",
        "add_appendix_prompt": "Do you want to add an appendix to the profile? (y/n):",
        "appendix_prompt": "Enter appendix text:",
        "filename_prompt": "Enter filename to save the profile (without extension):",
        "save_success": "Profile saved to {}",
        "export_success": "Profile exported to {}",
        "continue_prompt": "Press Enter to continue...",
        "main_menu": "Main Menu:",
        "main_menu_options": ["Create new persona", "Create random persona", "Load existing persona", "View program information", "Exit"],
        "random_level_select": "Select level of random persona detail:",
        "random_level_options": ["Minimal (Name, Gender, Age, Nationality, Profession)", "Standard (Adds Basic Location, Username, Password)", "Detailed (Adds Specific Location, Platforms, Interests)", "Full (Adds Phrases, Picture)"],
        "random_generating": "Generating {item}...",
        "random_generation_complete": "Random persona generation complete.",
        "confirm_save_random": "Do you want to save this generated profile?:",
        "back_option": "Back",
        "exit_option": "Exit",
        "invalid_choice": "Invalid choice. Please try again.",
        "program_info": "Sock Spy is a tool for educational use in OSINT and cybersecurity. \nIt allows simulation of realistic fake profiles for awareness, training, and practical exercises in ethical hacking environments.\nSock Spy is Open Source and is licensed under the GNU General Public License v3.0.\nActual Version: 1.0 \nStay dafe, stay Ethical.",
        "interests_select": "Select interests category:",
        "interests_subcategory": "Select interests subcategory:",
        "interests_specific": "Select specific interests (max 5):",
        "profession_category": "Select profession category:",
        "profession_subcategory": "Select profession subcategory:",
        "profession_specific": "Select a specific profession:",
        "location_continent": "Select a continent:",
        "location_country": "Select a country:",
        "location_region": "Select a region/state:",
        "location_city": "Select a city:",
        "location_neighborhood": "Select a neighborhood (Optional):",
        "biography_prompt": "Enter a short biography (press Enter to generate automatically):",
        "no_personas_found": "No saved personas found.",
        "select_persona": "Select a persona to load:",
        "persona_loaded": "Persona loaded successfully.",
        "persona_options": "Persona Options:",
        "persona_options_list": ["View persona details", "Edit persona", "Export persona (JSON)", "Export persona (TXT)", "Delete persona", "Back to main menu"],
        "confirm_delete": "Are you sure you want to delete this persona?:",
        "deleted_success": "Persona deleted successfully.",
        "common_phrases_select": "Select common phrases (max 3):",
        "show_more_options": "Show More Options",
        "regenerate_options": "Show New Options (Regenerate List)",
        "skip_level_and_continue": "Stop here and use current selection",
        "select_or_action": "Select an item or choose an action:",
        "empty_name_list_warning": "Warning: The name list for this selection ({filepath}) is currently empty.",
        "name_list_contribution_prompt": "We are working hard to bring more data! Perhaps you could help contribute names to this list?",
        "go_back_prompt": "Would you like to go back and change your selection? (y/n):",
        "random_name_retry_warning": "Warning: Could not find name data for {nationality}. Retrying with another nationality...",
        "random_name_fallback_warning": "Warning: Failed to find name data after several attempts. Using default names.",
    }
}
# fmt: on

# ==============================================================================
# SockSpy Class Definition
# ==============================================================================
class SockSpy:
    """Main class for the Sock Spy application."""

    def __init__(self):
        """Initialize paths, texts, and ensure directories exist."""
        self.texts = TEXTS["en"]
        self.profile = {}
        # Determine base directory safely
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, "data")
        self.profiles_dir = os.path.join(base_dir, "profiles")
        self.exports_dir = os.path.join(base_dir, "exports")

        # Ensure essential directories exist
        for directory in [self.profiles_dir, self.exports_dir]:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f"Created directory: {directory}")
                except OSError as e:
                    print(f"FATAL ERROR: Could not create directory {directory}: {e}")
                    print("Please check permissions and run again.")
                    sys.exit(1) # Exit if essential dirs can't be created

    # --------------------------------------------------------------------------
    # Core Application Flow Methods
    # --------------------------------------------------------------------------

    def display_welcome(self):
        """Display welcome screen with ASCII art."""
        clear_screen()
        display_ascii_art(self.data_dir)
        print(self.texts["welcome"])
        input(self.texts["continue_prompt"]) # Waits for Enter

    def main_menu(self):
        """Display main menu and handle user choices."""
        while True:
            clear_screen()
            print(self.texts["main_menu"])
            options = self.texts["main_menu_options"]
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options))
            if choice is None:
                continue

            if choice == 1:
                self.create_persona()
            elif choice == 2:
                self.create_random_persona()
            elif choice == 3:
                self.load_persona() # Assuming this method exists
            elif choice == 4:
                self.show_program_info()
            elif choice == 5: # Exit
                clear_screen()
                display_ascii_art(self.data_dir)
                print("\nThank you for using Sock Spy!")
                print("We hope to see you back soon.")
                print("\nExiting in 4 seconds...")
                time.sleep(4)
                clear_screen()
                sys.exit(0)


    def create_persona(self):
        """Guide user through persona creation process with loop-back logic."""
        self.profile = {}
        print("\n--- Starting New Persona Creation ---")

        # === Gender (Independent first step) ===
        if not self._select_gender():
            print("\nPersona creation cancelled during Gender selection.")
            input(self.texts["continue_prompt"])
            return # Exit method completely

        # === Nationality / Name / Lastname Block (Dependent steps) ===
        while True: # Loop allows going back to nationality if name selection fails/is rejected
            print("\n--- Selecting Nationality and Names ---")

            # --- Select Nationality ---
            # _select_nationality currently returns True/False based on if nationality was set.
            # False here means user cancelled nationality selection itself.
            if not self._select_nationality():
                print("\nPersona creation cancelled during Nationality selection.")
                input(self.texts["continue_prompt"])
                return # Exit method completely

            # --- Select First Name (Depends on Gender and Nationality) ---
            # _select_name returns False if empty file + user says 'y' OR user cancels dynamic list
            if not self._select_name():
                print("\nReturning to Nationality selection...")
                time.sleep(1.5)
                # Clear potentially selected nationality from profile to ensure re-selection
                self.profile.pop("nationality", None)
                continue # Restart the while loop (go back to nationality)

            # --- Select Last Name (Depends on Nationality) ---
            # _select_lastname returns False if empty file + user says 'y' OR user cancels dynamic list
            if not self._select_lastname():
                print("\nReturning to Nationality selection...")
                time.sleep(1.5)
                # Clear potentially selected names/nationality from profile
                self.profile.pop("nationality", None)
                self.profile.pop("first_name", None)
                continue # Restart the while loop (go back to nationality)

            # --- Success for this block ---
            # If we reach here, Nationality, Name, and Lastname are successfully set.
            print("\nNationality and Names selected successfully.")
            time.sleep(1)
            break # Exit the Nationality/Name/Lastname loop

        # === Remaining Independent Steps ===
        # If the loop above was exited successfully, continue with other steps.
        print("\n--- Selecting Remaining Details ---")

        if not self._select_age():
            print("\nPersona creation cancelled during Age selection.")
            input(self.texts["continue_prompt"])
            return # Exit method

        if not self._select_username():
            print("\nPersona creation cancelled during Username selection.")
            input(self.texts["continue_prompt"])
            return # Exit method

        if not self._select_password():
            print("\nPersona creation cancelled during Password selection.")
            input(self.texts["continue_prompt"])
            return # Exit method

        # Optional steps (These don't return False to cancel the whole process)
        self._select_platforms()
        self._select_hierarchical_interests()
        self._select_hierarchical_profession()
        self._select_location()
        self._select_optional_phrases()
        self._select_optional_picture()

        # === Final Steps (Preview, Edit, Save) ===
        print("\n--- Finalizing Persona ---")
        self.preview_profile()
        if get_input(self.texts["edit_profile_prompt"] + " ").lower() in ["y", "yes"]:
            self.edit_profile() # Assuming this method exists
        self._add_optional_appendix()
        self._save_and_export_profile()

        print("\nPersona creation process complete.")
        # The pause is handled within _save_and_export_profile

    # --------------------------------------------------------------------------
    # Helper Methods for Persona Creation Steps (to keep create_persona clean)
    # --------------------------------------------------------------------------

    def _select_gender(self):
        """Selects gender."""
        clear_screen() # CORRECTED: Separated from print
        print(self.texts["gender_select"])
        options = self.texts["gender_options"]
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = get_numeric_choice(1, len(options))
        if choice is None:
            return False # Cancelled
        self.profile["gender"] = {1: "male", 2: "female"}.get(choice, "male")
        return True

    def _select_nationality(self):
        """Selects nationality hierarchically."""
        self.select_nationality() # Call the main selection logic
        return self.profile.get("nationality") is not None # Return True if selected, False if cancelled

    def _select_name(self):
        """Selects first name."""
        self.select_name(self.profile["gender"], self.profile["nationality"])
        return self.profile.get("first_name") is not None

    def _select_lastname(self):
        """Selects last name."""
        self.select_lastname(self.profile["nationality"])
        return self.profile.get("last_name") is not None

    def _select_age(self):
        """Selects age."""
        clear_screen() # CORRECTED: Separated
        while True:
            try:
                age_str = get_input(self.texts["age_prompt"]).strip()
                # Check for empty input to allow cancellation
                if not age_str:
                    print("Age selection cancelled.") # Optional feedback
                    return False # Indicate cancelled

                # Convert to integer
                age = int(age_str)

                # Validate range
                if 18 <= age <= 99:
                    self.profile["age"] = age
                    return True # Indicate success
                else:
                    # Age is outside the valid range
                    print(self.texts["age_error"])
            except ValueError:
                # Input was not a valid number
                print(self.texts["age_error"])
            # Loop continues if there was an error

    def _select_username(self):
        """Selects username."""
        self.select_username()
        return self.profile.get("username") is not None

    def _select_password(self):
        """Selects password (manual or generated)."""
        clear_screen() # CORRECTED: Separated
        print(self.texts["password_method_select"])
        method_options = self.texts["password_method_options"]
        # Using list comp for printing is okay, but loop is more standard
        for i, opt in enumerate(method_options, 1): print(f"{i}. {opt}")
        method_choice = get_numeric_choice(1, len(method_options))
        if method_choice is None:
            return False # Cancelled
        password_to_confirm = None
        if method_choice == 1: # Manual
            while True:
                password = get_input(self.texts["password_prompt"])
                if not password:
                    print("Password cannot be empty.")
                    continue
                # Use '*' for confirmation prompt masking
                confirm = get_input(self.texts["password_confirm"].format('*'*len(password)) + " ").lower()
                if confirm in ["y", "yes"]:
                    password_to_confirm = password
                    break
                elif confirm in ["n", "no"]:
                    continue
                else: # Any other input treated as cancel? Or should it loop? Assuming cancel for now.
                    print("Password confirmation cancelled.")
                    return False # Cancelled
        elif method_choice == 2: # Generate
            clear_screen() # CORRECTED: Separated
            print(self.texts["password_length_select"])
            length_options = self.texts["password_length_options"]
            length_map = {1: 12, 2: 24, 3: 32}
            for i, opt in enumerate(length_options, 1): print(f"{i}. {opt}") # List comp okay
            length_choice = get_numeric_choice(1, len(length_options))
            if length_choice is None:
                return False # Cancelled
            selected_length = length_map.get(length_choice, 12)
            password_to_confirm = generate_random_password(selected_length)
            # Display masked password confirmation
            print(f"\nGenerated Password: {'*' * len(password_to_confirm)}") # CORRECTED: Separated print
            print("Generated password set.") # CORRECTED: Separated print
            time.sleep(1.5)
        # Assign password if one was set
        if password_to_confirm:
            self.profile["password"] = password_to_confirm
            return True
        else:
            return False # Failed or cancelled

    def _select_platforms(self):
        """Selects platforms."""
        clear_screen() # CORRECTED: Separated
        platforms_input = get_input(self.texts["platforms_prompt"])
        self.profile["platforms"] = [p.strip() for p in platforms_input.split(",") if p.strip()]
        return True # Always succeeds even if list is empty

    def _select_hierarchical_interests(self):
        """Selects interests hierarchically."""
        self.select_hierarchical_interests()
        return True # Selection handles internal skipping/cancelling

    def _select_hierarchical_profession(self):
        """Selects profession hierarchically."""
        self.select_hierarchical_profession()
        return True

    def _select_location(self):
        """Selects location hierarchically."""
        self.select_location()
        return True

    def _select_optional_phrases(self):
        """Optionally selects common phrases."""
        clear_screen() # CORRECTED: Separated
        if get_input(self.texts["add_phrases_prompt"] + " ").lower() in ["y", "yes"]:
            self.select_common_phrases()
        return True

    def _select_optional_picture(self):
        """Optionally selects profile picture."""
        clear_screen() # CORRECTED: Separated
        if get_input(self.texts["add_picture_prompt"] + " ").lower() in ["y", "yes"]:
            self.select_profile_picture()
        return True

    def _add_optional_appendix(self):
        """Optionally adds an appendix."""
        clear_screen() # CORRECTED: Separated
        if get_input(self.texts["add_appendix_prompt"] + " ").lower() in ["y", "yes"]:
            appendix = get_input(self.texts["appendix_prompt"])
            if appendix:
                self.profile["appendix"] = appendix
        return True

    def _save_and_export_profile(self):
        """Handles filename prompt, saving, and exporting."""
        clear_screen() # CORRECTED: Separated
        default_filename = f"{self.profile.get('first_name', 'profile')}_{self.profile.get('last_name', str(random.randint(100,999)))}".lower().replace(" ","_")
        filename_prompt = self.texts["filename_prompt"] + f" (Leave blank for '{default_filename}')"
        filename = get_input(filename_prompt).strip()
        filename = filename if filename else default_filename
        saved_path = save_profile(self.profile, filename, self.profiles_dir)
        if saved_path:
            print(self.texts["save_success"].format(saved_path))
            exported_path = export_profile_to_txt(self.profile, filename, self.exports_dir)
            if exported_path:
                print(self.texts["export_success"].format(exported_path)) # CORRECTED: Separated from export call
            # Consider adding an else for export failure here if desired
        else:
            print("Error saving profile.")
        input(self.texts["continue_prompt"])

    # --------------------------------------------------------------------------
    # Selection Logic Methods (Called by creation steps)
    # --------------------------------------------------------------------------


    def select_nationality(self):
        """Select nationality using hierarchical structure (Continent -> Specific), showing counts."""

        # --- Load Name Counts Cache ---
        cache_file_path = os.path.join(os.path.dirname(__file__), "name_counts.json")
        loaded_name_counts = {} # Default to empty dict
        try:
            # Use load_json_file utility if it handles errors, otherwise basic load
            # Assuming load_json_file returns {} or None on error/not found
            temp_counts = load_json_file(cache_file_path)
            if temp_counts:
                 loaded_name_counts = temp_counts
            # else: keep loaded_name_counts as {}
        except Exception as e:
            print(f"Warning: Could not load name counts cache ({cache_file_path}): {e}")
            # Proceed without counts if cache fails

        # --- Load Nationalities Data ---
        clear_screen()
        print("Loading nationality data...")
        try:
            nationalities_data = load_json_file(os.path.join(self.data_dir, "nationalities.json"))
            assert nationalities_data and isinstance(nationalities_data, dict)
        except Exception as e:
            print(f"Error loading nationalities: {e}")
            self.profile["nationality"] = None
            input(self.texts["continue_prompt"])
            return False # Indicate failure

        # --- Continent Selection ---
        clear_screen()
        level_name = self.texts.get("nationality_continent")
        print(level_name)
        continents = sorted(list(nationalities_data.keys()))
        if not continents:
            print("Error: No continents found in data.")
            self.profile["nationality"] = None
            input(self.texts["continue_prompt"])
            return False

        for i, continent in enumerate(continents, 1):
            print(f"{i}. {continent}")
        print("-" * 20)
        continent_choice = get_numeric_choice(1, len(continents))
        if continent_choice is None:
            print("Cancelled.")
            self.profile["nationality"] = None
            return False # Indicate cancellation

        # --- Prepare Nationality List with Counts ---
        selected_continent = continents[continent_choice - 1]
        raw_nationality_list = sorted(nationalities_data.get(selected_continent, []))
        if not raw_nationality_list:
            print(f"Error: No nationalities listed for {selected_continent}.")
            self.profile["nationality"] = None
            input(self.texts["continue_prompt"])
            return False

        # Create list of strings formatted for display
        display_options = []
        for nat_name in raw_nationality_list:
            nat_key = nat_name.lower()
            # Get counts from cache, default to 0s if not found
            counts = loaded_name_counts.get(nat_key, {"male": 0, "female": 0, "last": 0})
            # Format the display string
            display_text = f"{nat_name} (M:{counts['male']}, F:{counts['female']}, L:{counts['last']})"
            display_options.append(display_text)

        # --- Nationality Selection using Dynamic Handler ---
        clear_screen()
        prompt = self.texts.get("nationality_specific")
        while True:
            # Pass the formatted display list to the handler
            # The handler will return the *index* of the selected formatted string
            # Args: list_to_display, texts, prompt, page_size=10, allow_skip=False, allow_back=True
            selected_display_item, action = handle_dynamic_list_selection(
                display_options, # Pass the list with counts
                self.texts,
                prompt,
                10,
                False,
                True
            )

            if action == 'selected':
                # IMPORTANT: We need the original nationality name, not the formatted string
                # Find the original name based on the selected display item
                original_nationality = None
                for nat_name in raw_nationality_list: # Iterate through original names
                    # Re-create the display format to find a match
                    nat_key = nat_name.lower()
                    counts = loaded_name_counts.get(nat_key, {"male": 0, "female": 0, "last": 0})
                    expected_display_text = f"{nat_name} (M:{counts['male']}, F:{counts['female']}, L:{counts['last']})"
                    if selected_display_item == expected_display_text:
                        original_nationality = nat_name
                        break

                if original_nationality:
                    self.profile["nationality"] = original_nationality.lower()
                    print(f"\nSelected: {original_nationality}")
                    return True # Indicate success
                else:
                    # This shouldn't happen if handle_dynamic... returns a valid item from the list
                    print("Error: Could not map selected display item back to original nationality.")
                    self.profile["nationality"] = None
                    return False # Indicate failure

            elif action == 'back':
                print("Nationality selection cancelled.")
                self.profile["nationality"] = None
                return False # Indicate cancellation

            # Handle other potential actions from the handler if necessary
            # else: # e.g., skip? - currently allow_skip is False
            #     print("Invalid action returned by handler.")
            #     self.profile["nationality"] = None
            #     return False

    def select_name(self, gender, nationality):
        """Select a first name using dynamic list helper"""
        clear_screen() # CORRECTED: Separated
        prompt = self.texts["name_select"]
        names_file = os.path.join(self.data_dir, "names", gender, f"{nationality}.txt")
        full_list = load_data_file(names_file)
        if full_list is FILE_NOT_FOUND:
            # File non-existent or error reading - treat as cancellation
            print(f"Error: Could not load name file for {gender}/{nationality}.")
            input(self.texts["continue_prompt"])
            self.profile.pop("first_name", None)
            return False # Signal failure/cancel to create_persona

        if full_list == FILE_EMPTY:
            # File exists but is empty
            print(self.texts["empty_name_list_warning"].format(filepath=f"{gender}/{nationality}.txt"))
            print(self.texts["name_list_contribution_prompt"])
            go_back = get_input(self.texts["go_back_prompt"] + " ").lower()
            if go_back in ['y', 'yes']:
                self.profile.pop("first_name", None)
                return False # Signal user wants to go back
            else:
                # User chose not to go back, proceed with an empty list (handle_dynamic will show nothing)
                # Or, assign a default? For now, let handle_dynamic show no options.
                full_list = [] # Ensure it's an empty list for the next step
                print("Proceeding without name options for this selection.")
                time.sleep(1.5)
                # Fall through to handle_dynamic_list_selection which will show no items
                # and likely result in 'back' action if user cancels there.

        # --- End Check ---

        # If full_list is valid (non-empty list), proceed with selection
        # Note: If user chose *not* to go back on empty list, full_list is now []
        while True:
            # Args: list, texts, prompt, page_size=7, allow_skip=False, allow_back=True
            selected_item, action = handle_dynamic_list_selection(full_list, self.texts, prompt, 7, False, True)
            if action == 'selected':
                self.profile["first_name"] = selected_item
                break
            elif action == 'back':
                # This will trigger if user exits the dynamic list (e.g., if it was empty)
                print("Name selection step cancelled.")
                self.profile.pop("first_name", None)
                return False # Signal cancellation back to create_persona

        return True # Indicate success

    def select_lastname(self, nationality):
        """Select a last name using dynamic list helper"""
        clear_screen() # CORRECTED: Separated
        prompt = self.texts["lastname_select"]
        lastnames_file = os.path.join(self.data_dir, "last_names", f"{nationality}.txt")
        full_list = load_data_file(lastnames_file)
        if full_list is FILE_NOT_FOUND:
            print(f"Error: Could not load last name file for {nationality}.")
            input(self.texts["continue_prompt"])
            self.profile.pop("last_name", None)
            return False

        if full_list == FILE_EMPTY:
            print(self.texts["empty_name_list_warning"].format(filepath=f"{nationality}.txt"))
            print(self.texts["name_list_contribution_prompt"])
            go_back = get_input(self.texts["go_back_prompt"] + " ").lower()
            if go_back in ['y', 'yes']:
                self.profile.pop("last_name", None)
                return False
            else:
                full_list = []
                print("Proceeding without last name options for this selection.")
                time.sleep(1.5)
        # --- End Check ---

        while True:
            # Args: list, texts, prompt, page_size=7, allow_skip=False, allow_back=True
            selected_item, action = handle_dynamic_list_selection(full_list, self.texts, prompt, 7, False, True)
            if action == 'selected':
                self.profile["last_name"] = selected_item
                break
            elif action == 'back':
                print("Last name selection step cancelled.")
                self.profile.pop("last_name", None)
                return False

        return True # Indicate success

    def select_username(self):
        """Generate and select username, allowing custom input or selection"""
        clear_screen()
        while True:
            print(self.texts["username_suggestions"])
            suggestions = []
            try:
                first = self.profile.get("first_name", "User") # CORRECTED: Separated assignment
                last = self.profile.get("last_name", "")        # CORRECTED: Separated assignment
                age = self.profile.get("age", 30)               # CORRECTED: Separated assignment
                suggestions = generate_username_suggestions(first, last, age)
            except Exception as e:
                print(f"Warning: Username suggestion error ({e}). Using fallback.") # Added detail
            # Ensure fallback is always available
            fallback = f"{self.profile.get('first_name','user')[:4].lower()}{random.randint(100,999)}"
            if not suggestions: suggestions.append(fallback) # Only add if suggestions failed
            elif fallback not in suggestions: suggestions.append(fallback) # Add if not already present

            options = list(dict.fromkeys(suggestions)) # Ensure unique suggestions
            options.append("Enter custom username") # Add custom option last

            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options))
            if choice is None:
                self.profile.pop("username", None) # CORRECTED: Separated
                return # Indicate cancel

            username_to_set = ""
            if choice <= len(suggestions): # If choice is one of the suggestions
                 username_to_set = options[choice - 1]
            elif choice == len(options): # If choice is "Enter custom username"
                 username_to_set = get_input(self.texts["username_prompt"]).strip()

            # Validate the chosen/entered username
            if not username_to_set:
                print("Username cannot be empty.") # CORRECTED: Separated
                input(self.texts["continue_prompt"]) # Use standard pause
                continue

            # Confirm the final username
            confirm = get_input(self.texts["username_confirm"].format(username_to_set) + " ").lower()
            if confirm in ["y", "yes"]:
                self.profile["username"] = username_to_set # CORRECTED: Separated
                break
            # If not confirmed, loop back to show suggestions/ask again

    def select_hierarchical_interests(self):
        """Select interests using hierarchical structure and new options"""
        clear_screen() # CORRECTED: Separated
        print("Loading interests data...")
        try:
            interests_data = load_json_file(os.path.join(self.data_dir, "interests.json"))
            assert interests_data and isinstance(interests_data, dict)
        except Exception as e:
            print(f"Warning: Interests data error ({e}). Skipping interests selection.") # CORRECTED: Separated
            self.profile["interests"] = []                                              # CORRECTED: Separated
            input(self.texts["continue_prompt"])                                        # CORRECTED: Separated
            return

        current_level_data = interests_data
        path = [] # CORRECTED: Separated assignment
        level_prompt_keys = ["interests_select", "interests_subcategory", "interests_specific"]
        level = 0
        while isinstance(current_level_data, dict):
            clear_screen() # CORRECTED: Separated
            level_name = self.texts.get(level_prompt_keys[level], f"Select Category Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options:
                print("No further options available in this branch.")
                break # No more levels down this path

            selected_option = None # CORRECTED: Separated assignment
            action = None          # CORRECTED: Separated assignment
            if level == 0: # Simple menu for the first level
                print(level_name)
                for i, o in enumerate(options, 1): print(f"{i}. {o}") # List comp okay here
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                action = 'back' if choice is None else 'selected'
                selected_option = options[choice - 1] if action == 'selected' else None
            else: # Use dynamic handler for subsequent levels
                # Args: list, texts, prompt, page_size=10, allow_skip=True, allow_back=True
                selected_option, action = handle_dynamic_list_selection(options, self.texts, level_name, 10, True, True)

            if action == 'selected':
                path.append(selected_option)
                next_data = current_level_data.get(selected_option)
                # Ensure we only proceed if next level is dict or list
                current_level_data = next_data if isinstance(next_data, (dict, list)) else {}
                level += 1
            elif action == 'skip':
                print("Skipping further selection in this branch.")
                break # Stop drilling down
            elif action == 'back':
                if level == 0: # Back from the very first level means cancel all
                    print("Interests selection cancelled.")
                    self.profile["interests"] = []
                    return # Exit method
                else: # Go back up one level
                    print("Going back one level...")
                    path.pop() # Remove last selection from path
                    # Reconstruct the parent data (this is tricky without storing parent ref)
                    # For simplicity, we might just break here or restart the process.
                    # Let's break for now, user can restart if needed.
                    print("Returning to previous level selection is complex, stopping selection here.")
                    break # Stop drilling down

        # Handle final level if it's a list
        final_selected_interests = []
        if isinstance(current_level_data, list):
            specific_interests = sorted(current_level_data)
            if specific_interests:
                # Use the multi-select helper for the final list
                self._handle_multi_select_final_level(specific_interests, self.texts["interests_specific"], "interests", 5)
                # The helper modifies self.profile["interests"] directly
                final_selected_interests = self.profile.get("interests", [])
            else:
                print("No specific interests found at the end of this branch.")
                self.profile["interests"] = [] # Ensure key exists
        elif path and not isinstance(current_level_data, (dict, list)):
             # If user skipped/stopped at a dict level, use the path items?
             # Let's default to empty list if final level isn't a list of choices
             print("Selection stopped before reaching specific items.")
             self.profile["interests"] = []

        # Ensure key exists even if skipped early or list empty
        if "interests" not in self.profile:
            self.profile["interests"] = []

        # Optionally print final selection summary
        final_selection = self.profile.get("interests", [])
        if final_selection:
            print(f"\nFinal Selected Interests: {', '.join(final_selection)}")
        else:
            print("\nNo specific interests selected.")


    def select_hierarchical_profession(self):
        """Select profession using hierarchical structure and new options"""
        clear_screen()
        print("Loading professions data...")
        try:
            professions_data = load_json_file(os.path.join(self.data_dir, "professions.json"))
            assert professions_data and isinstance(professions_data, dict)
        except Exception as e:
            print(f"Warning: Professions data error ({e}). Setting profession to 'Unspecified'.")
            self.profile["profession"] = "Unspecified"
            input(self.texts["continue_prompt"])
            return

        current_level_data = professions_data
        path = []
        level_prompt_keys = ["profession_category", "profession_subcategory", "profession_specific"]
        level = 0
        final_profession = None # Variable to hold the single final choice

        # --- Loop through DICTIONARY levels ---
        while isinstance(current_level_data, dict):
            clear_screen()
            level_name = self.texts.get(level_prompt_keys[level], f"Select Category Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options:
                print("No further options available in this branch.")
                break # Exit while loop

            selected_option = None # Result for this level's choice
            action = None

            if level == 0: # Simple menu for the first level
                print(level_name)
                for i, o in enumerate(options, 1): print(f"{i}. {o}")
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                action = 'back' if choice is None else 'selected'
                selected_option = options[choice - 1] if action == 'selected' else None
            else: # Use dynamic handler for subsequent dictionary levels
                # *** CORRECTED CALL for hierarchical levels ***
                # Uses 'options' list, stores in 'selected_option', page_size=10
                # Args: list, texts, prompt, page_size=10, allow_skip=True, allow_back=True
                selected_option, action = handle_dynamic_list_selection(options, self.texts, level_name, 10, True, True)

            # --- Handle action from this level's selection ---
            if action == 'selected':
                path.append(selected_option)
                next_data = current_level_data.get(selected_option)
                # Update current_level_data for the NEXT iteration or the check after the loop
                current_level_data = next_data if isinstance(next_data, (dict, list)) else {}
                level += 1
            elif action == 'skip':
                print("Stopping profession selection at this category level.")
                final_profession = path[-1] if path else "Unspecified" # Use last category
                break # Exit while loop
            elif action == 'back':
                if level == 0:
                    print("Profession selection cancelled.")
                    self.profile["profession"] = "Unspecified"
                    return # Exit function entirely
                else:
                    # Go back up one level in the loop (requires recalculating parent data)
                    # Simple approach: Stop selection here, use current category path
                    print("Going back one level...")
                    if path: path.pop() # Remove last step from path
                    final_profession = path[-1] if path else "Unspecified" # Use new last category
                    print(f"Stopping selection. Current category: {final_profession}")
                    break # Exit while loop

        # --- After the while loop (current_level_data is NOT a dict anymore) ---

        # Handle final level IF it's a list of specific professions
        if isinstance(current_level_data, list):
            specific_professions = sorted(current_level_data) # Define variable HERE
            if specific_professions:
                clear_screen()
                # Determine the correct prompt text for the final level
                final_level_index = min(level, len(level_prompt_keys) - 1)
                level_name = self.texts.get(level_prompt_keys[final_level_index], f"Select Final Profession {level+1}:")

                # *** CORRECTED CALL for final list selection ***
                # Uses 'specific_professions' list, stores in 'selected_final', page_size=15
                # Args: list, texts, prompt, page_size=15, allow_skip=True, allow_back=True
                selected_final, action = handle_dynamic_list_selection(specific_professions, self.texts, level_name, 15, True, True)

                if action == 'selected':
                    final_profession = selected_final # Assign the specific job title
                elif action == 'skip' or action == 'back':
                     # If skipped/backed from final list, use the last category from path
                     final_profession = path[-1] if path else "Unspecified"
                     print(f"Using category: {final_profession}")
                # If action is None (e.g., error in handler), final_profession remains as set before or None
            else:
                 # List was empty
                 print("No specific professions found at the end of this branch.")
                 final_profession = path[-1] if path else "Unspecified" # Use last category

        # --- Assign Final Profession ---
        # Assign the determined profession (could be specific title, category, or fallback)
        # 'final_profession' might have been set by 'skip'/'back' inside the loop,
        # or by selection/skip/back in the final list handling, or it might still be None.
        if final_profession is None and path: # If loop finished naturally at a dict/empty list & no final selection made
             final_profession = path[-1] # Default to last category path item

        self.profile["profession"] = final_profession if final_profession else "Unspecified"
        print(f"\nSelected Profession: {self.profile.get('profession', 'N/A')}") # Use get for safety

    def select_location(self):
        """Select location with hierarchical structure and new options"""
        clear_screen() # CORRECTED: Separated
        print("Loading location data...")
        try:
            locations_data = load_json_file(os.path.join(self.data_dir, "locations.json"))
            assert locations_data and isinstance(locations_data, dict)
        except Exception as e:
            print(f"Error loading locations.json: {e}. Setting location to 'Earth'.") # CORRECTED: Separated
            self.profile["location"] = "Earth"                                       # CORRECTED: Separated
            input(self.texts["continue_prompt"])                                     # CORRECTED: Separated
            return

        current_level_data = locations_data
        path = [] # CORRECTED: Separated assignment
        level_prompt_keys = ["location_continent", "location_country", "location_region", "location_city", "location_neighborhood"]
        level = 0

        while isinstance(current_level_data, dict):
            clear_screen() # CORRECTED: Separated
            level_name = self.texts.get(level_prompt_keys[level], f"Select Location Level {level+1}:")
            options = sorted(list(current_level_data.keys()))
            if not options:
                print("No further options available in this branch.")
                break

            selected_option = None # CORRECTED: Separated assignment
            action = None          # CORRECTED: Separated assignment
            # Determine if skipping should be allowed (e.g., allow skipping State/Region)
            allow_skip_here = level >= 2 # Allow skipping from Region onwards

            if level == 0: # Simple menu for Continent
                print(level_name)
                for i, o in enumerate(options, 1): print(f"{i}. {o}")
                print("-" * 20)
                choice = get_numeric_choice(1, len(options))
                action = 'back' if choice is None else 'selected'
                selected_option = options[choice - 1] if action == 'selected' else None
            else: # Use dynamic handler for subsequent levels
                            # Args: list, texts, prompt, page_size=10, allow_skip=allow_skip_here, allow_back=True
                            selected_option, action = handle_dynamic_list_selection(options, self.texts, level_name, 10, allow_skip_here, True)

            if action == 'selected':
                path.append(selected_option)
                next_data = current_level_data.get(selected_option)
                current_level_data = next_data if isinstance(next_data, (dict, list)) else {}
                level += 1
            elif action == 'skip':
                print("Stopping location selection at this level.")
                break # Stop drilling down, use current path
            elif action == 'back':
                if level == 0:
                    print("Location selection cancelled.")
                    self.profile["location"] = "Undetermined"
                    return
                else:
                    print("Going back one level...")
                    if path: path.pop() # Go back up the path
                    level -= 1
                    # Need to reconstruct current_level_data based on new path end
                    # This is complex. Let's just break and use the current path.
                    print("Returning to previous level selection is complex, stopping selection here.")
                    break

        # Handle final level if it's a list (e.g., neighborhoods, optional final step)
        if isinstance(current_level_data, list):
            final_options = sorted(current_level_data)
            if final_options:
                clear_screen() # CORRECTED: Separated
                final_level_index = min(level, len(level_prompt_keys) - 1) # Avoid index error
                level_name = self.texts.get(level_prompt_keys[final_level_index], f"Select Final Location {level+1}:")
                # Args: list, texts, prompt, page_size=10, allow_skip=True, allow_back=True
                selected_final, action = handle_dynamic_list_selection(final_options, self.texts, level_name + " (Optional)", 10, True, True)
                if action == 'selected':
                    path.append(selected_final)
                # If skipped/backed, just use the path as it was before this step

        # Format the final location string from the path
        self.profile["location"] = ", ".join(reversed(path)) if path else "Unknown Location"
        print(f"\nSelected Location: {self.profile.get('location', 'N/A')}")

    def select_common_phrases(self):
        """Select common phrases using reusable multi-select helper"""
        clear_screen() # CORRECTED: Separated
        phrases_file = os.path.join(self.data_dir, "common_phrases", "english.txt")
        full_list = load_data_file(phrases_file)
        if not full_list:
            print("Warning: No common phrases found. Skipping.") # CORRECTED: Separated
            self.profile["common_phrases"] = []                 # CORRECTED: Separated
            input(self.texts["continue_prompt"])                # CORRECTED: Separated
            return
        # Call the helper, which will update self.profile['common_phrases']
        self._handle_multi_select_final_level(full_list, self.texts["common_phrases_select"], "common_phrases", 3)

        # Optionally print summary after selection is done
        selected_phrases = self.profile.get("common_phrases", [])
        if selected_phrases:
            print("\nSelected Phrases:")
            for phrase in selected_phrases:
                print(f"- {phrase}")
        else:
            print("\nNo common phrases selected.")
        # Add pause if needed after printing summary
        # input(self.texts["continue_prompt"])

    def select_profile_picture(self):
        """Select a profile picture URL using dynamic helper"""
        clear_screen() # CORRECTED: Separated
        prompt = "Select a profile picture:"
        pictures_file = os.path.join(self.data_dir, "profile_pictures.txt")
        full_list = [] # CORRECTED: Separated assignment

        pictures = load_data_file(pictures_file) # Load first
        if not pictures:
            print("Warning: No pictures file found or list is empty. Cannot select picture.") # CORRECTED: Separated
            self.profile.pop("profile_picture", None) # Ensure key isn't present # CORRECTED: Separated
            input(self.texts["continue_prompt"]) # CORRECTED: Separated
            return

        try:
            gender = self.profile.get("gender", "female") # Default gender if needed
            keywords = ["/men/"] if gender == "male" else ["/women/"]
            full_list = [p for p in pictures if any(kw in p.lower() for kw in keywords)]
            if not full_list:
                print(f"Warning: No specific pictures found for '{gender}'. Showing all available pictures.") # CORRECTED: Separated
                full_list = pictures # Fallback to all pictures
        except Exception as e:
            print(f"Warning: Picture filtering error ({e}). Showing all available pictures.") # CORRECTED: Separated
            full_list = pictures # Fallback to all pictures

        # Final check if list is empty even after fallbacks
        if not full_list:
            print("Warning: No pictures available to select after filtering/fallback.") # CORRECTED: Separated
            self.profile.pop("profile_picture", None) # Ensure key isn't present # CORRECTED: Separated
            input(self.texts["continue_prompt"]) # CORRECTED: Separated
            return

        # Loop for selection using the dynamic helper
        while True:
            # Args: list, texts, prompt, page_size=5, allow_skip=False, allow_back=True
            selected_item, action = handle_dynamic_list_selection(full_list, self.texts, prompt, 5, False, True)
            if action == 'selected':
                self.profile["profile_picture"] = selected_item # CORRECTED: Separated
                print(f"\nSelected Picture: {selected_item}") # Give feedback
                break
            elif action == 'back':
                print("Picture selection cancelled.") # CORRECTED: Separated
                self.profile.pop("profile_picture", None) # Ensure key removed on cancel # CORRECTED: Separated
                break # Indicate cancel

    # --- _handle_multi_select_final_level - Structure looks okay now ---
    def _handle_multi_select_final_level(self, full_list, prompt, profile_key, max_select=5):
        """Internal helper for multi-select lists with actions and progressive selection."""
        clear_screen() # CORRECTED: Separated
        initial_show = 10
        increment = 5
        available_indices = list(range(len(full_list)))
        # Sample initial indices
        displayed_indices = random.sample(available_indices, min(initial_show, len(available_indices)))
        displayed_indices.sort()
        # Get existing selections or start fresh, ensure it's a mutable copy
        selected_items_list = list(self.profile.get(profile_key, [])) # Use list() for copy

        while True:
            clear_screen()
            print(prompt)
            print("-" * 30)
            print(f"Currently Selected ({len(selected_items_list)}/{max_select}):")
            if selected_items_list:
                for item in selected_items_list:
                    print(f"- {item}")
            else:
                print("(None)")
            print("-" * 30)
            print("Available Options:")
            # Map displayed options that are NOT already selected
            current_options_map = {
                i + 1: full_list[idx]
                for i, idx in enumerate(displayed_indices)
                if full_list[idx] not in selected_items_list
            }
            if not current_options_map:
                print("(No more selectable options in current view)")
            else:
                 for num, item in current_options_map.items():
                     print(f"{num}. {item}")

            print("-" * 20)
            # Determine action numbers dynamically
            action_num_start = max(current_options_map.keys()) + 1 if current_options_map else 1
            show_more_opt_num = -1 # Default to invalid
            regenerate_opt_num = -1
            finish_opt_num = -1
            current_max_choice = max(current_options_map.keys()) if current_options_map else 0 # Start with highest item number

            can_show_more = len(displayed_indices) < len(available_indices)

            # Display actions and update max choice number
            if can_show_more:
                show_more_opt_num = action_num_start
                print(f"{show_more_opt_num}. {self.texts.get('show_more_options', 'Show More')}") # CORRECTED: Separated
                current_max_choice = show_more_opt_num
                action_num_start += 1

            regenerate_opt_num = action_num_start
            print(f"{regenerate_opt_num}. {self.texts.get('regenerate_options', 'Regenerate List')}") # CORRECTED: Separated
            current_max_choice = regenerate_opt_num
            action_num_start += 1

            finish_opt_num = action_num_start
            print(f"{finish_opt_num}. Finish Selecting") # CORRECTED: Separated
            current_max_choice = finish_opt_num

            # Determine the absolute max number user can enter
            actual_max_input = current_max_choice # Max is now the highest action number

            # Construct prompt text dynamically
            item_num_range_str = f"1-{max(current_options_map.keys())}" if current_options_map else "N/A"
            prompt_text = f"\nEnter item # ({item_num_range_str}) to add/select, or action #:"

            user_choice = get_numeric_choice(1, actual_max_input, prompt=prompt_text)

            if user_choice is None: # User pressed Enter or invalid input handled by get_numeric_choice
                print("Finishing selection.") # CORRECTED: Separated
                break

            # --- Handle Actions ---
            if user_choice == show_more_opt_num and can_show_more:
                remaining_indices = [i for i in available_indices if i not in displayed_indices]
                if remaining_indices:
                    num_to_add = min(increment, len(remaining_indices))
                    new_indices = random.sample(remaining_indices, num_to_add)
                    displayed_indices.extend(new_indices)
                    displayed_indices.sort()
                continue # Redisplay

            elif user_choice == regenerate_opt_num:
                num_to_show = min(initial_show, len(available_indices))
                displayed_indices = random.sample(available_indices, num_to_show)
                displayed_indices.sort()
                continue # Redisplay

            elif user_choice == finish_opt_num:
                print("Finishing selection.") # CORRECTED: Separated
                break # Exit loop

            # --- Handle Item Selection ---
            elif user_choice in current_options_map:
                item_to_add = current_options_map[user_choice]
                if len(selected_items_list) < max_select:
                    selected_items_list.append(item_to_add)
                    print(f"Added: {item_to_add}") # CORRECTED: Separated
                    time.sleep(0.8)
                else:
                    print(f"Cannot add more than {max_select} item(s).") # CORRECTED: Separated
                    time.sleep(1)
                continue # Continue loop after attempting to add item

            else: # Choice was not a valid item or action number
                print(self.texts.get("invalid_choice", "Invalid selection.")) # CORRECTED: Separated
                time.sleep(1)
                continue # Ask again

        # After loop finishes (break), update the profile with the final list
        self.profile[profile_key] = selected_items_list


    # --------------------------------------------------------------------------
    # Profile Management & Utility Methods
    # --------------------------------------------------------------------------


    def _update_name_counts_cache(self):
        """
        Scans name files based on nationalities.json, counts names,
        and saves the counts to a cache file (name_counts.json).
        """
        print("Initializing name count update...")
        nationalities_path = os.path.join(self.data_dir, "nationalities.json")
        cache_file_path = os.path.join(os.path.dirname(__file__), "name_counts.json") # Cache in base dir

        name_counts = {}
        total_nationalities = 0
        processed_count = 0

        try:
            nationalities_data = load_json_file(nationalities_path)
            if not nationalities_data:
                print("Warning: Could not load nationalities.json. Skipping name count update.")
                return

            # First count total nationalities for progress bar
            for continent_list in nationalities_data.values():
                total_nationalities += len(continent_list)

            if total_nationalities == 0:
                print("Warning: No nationalities found in nationalities.json.")
                return

            print(f"Found {total_nationalities} nationalities to process.")
            time.sleep(0.5) # Brief pause

            # Iterate and count
            for continent, nationality_list in nationalities_data.items():
                for nationality in nationality_list:
                    processed_count += 1
                    nat_key = nationality.lower() # Use lowercase key

                    # --- Construct Paths ---
                    male_path = os.path.join(self.data_dir, "names", "male", f"{nat_key}.txt")
                    female_path = os.path.join(self.data_dir, "names", "female", f"{nat_key}.txt")
                    last_path = os.path.join(self.data_dir, "last_names", f"{nat_key}.txt")

                    # --- Load and Count ---
                    male_list = load_data_file(male_path)
                    female_list = load_data_file(female_path)
                    last_list = load_data_file(last_path)

                    # Get length if list is valid (not None, includes []), else 0
                    male_count = len(male_list) if isinstance(male_list, list) else 0
                    female_count = len(female_list) if isinstance(female_list, list) else 0
                    last_count = len(last_list) if isinstance(last_list, list) else 0

                    # --- Store Counts ---
                    name_counts[nat_key] = {
                        "male": male_count,
                        "female": female_count,
                        "last": last_count
                    }

                    # --- Update Progress ---
                    progress = int((processed_count / total_nationalities) * 100)
                    bar_length = 20
                    filled_length = int(bar_length * processed_count // total_nationalities)
                    bar = '#' * filled_length + '-' * (bar_length - filled_length)
                    # Use \r to return to beginning of line, end='' to prevent newline
                    print(f"\rProcessing: [{bar}] {progress}% ({processed_count}/{total_nationalities}) - {nationality}", end='')

            print() # Newline after the loop finishes

            # --- Save Cache ---
            print(f"Saving counts to {cache_file_path}...")
            try:
                with open(cache_file_path, "w", encoding="utf-8") as f:
                    json.dump(name_counts, f, indent=2, ensure_ascii=False)
                print("Name counts cache updated successfully.")
            except IOError as e:
                print(f"Error saving name counts cache: {e}")
            except Exception as e:
                 print(f"An unexpected error occurred saving cache: {e}")

        except Exception as e:
            print(f"\nAn error occurred during name count update: {e}")
            # Optionally log the error traceback here if needed
            # import traceback
            # traceback.print_exc()
            print("Proceeding without updated name counts.")

        time.sleep(1) # Pause briefly after completion/error message


    def preview_profile(self):
        """Display a preview of the generated or loaded profile"""
        clear_screen() # CORRECTED: Separated
        print(self.texts["profile_preview"])
        print("\n" + "=" * 40 + "\n")
        # Use .get() for safety, provide default values like 'N/A'
        print(f"Name: {self.profile.get('first_name', 'N/A')} {self.profile.get('last_name', 'N/A')}")
        print(f"Gender: {self.profile.get('gender', 'N/A').capitalize()}")
        print(f"Age: {self.profile.get('age', 'N/A')}")
        print(f"Nationality: {self.profile.get('nationality', 'N/A').capitalize()}")
        print(f"Location: {self.profile.get('location', 'N/A')}")
        print(f"Username: {self.profile.get('username', 'N/A')}")
        # Mask password display
        password = self.profile.get('password')
        print(f"Password: {'*' * len(password) if password else 'N/A'}")
        # Handle list types gracefully
        platforms = self.profile.get("platforms", [])
        interests = self.profile.get("interests", [])
        common_phrases = self.profile.get("common_phrases", [])
        profile_picture = self.profile.get("profile_picture")
        appendix = self.profile.get("appendix")

        if platforms:
            print("\nPlatforms:")
            for p in platforms: print(f"- {p}") # List comp okay here
        if interests:
            print("\nInterests:")
            for i in interests: print(f"- {i}") # List comp okay here

        print(f"\nProfession: {self.profile.get('profession', 'N/A')}")

        if common_phrases:
            print("\nCommon Phrases:")
            for p in common_phrases: print(f"- {p}") # List comp okay here
        if profile_picture:
            print(f"\nProfile Picture: {profile_picture}")
        if appendix:
            print(f"\nAppendix: {appendix}")

        print("\n" + "=" * 40 + "\n") # CORRECTED: Separated
        input(self.texts["continue_prompt"])

    def edit_profile(self):
        """Allow user to edit profile fields."""
        while True:
            clear_screen() # CORRECTED: Separated
            print("--- Edit Profile ---")
            editable_fields = {}
            i = 1

            # Create a sorted list of keys for consistent display order
            # Filter out keys that maybe shouldn't be directly edited if needed
            profile_keys = sorted([k for k in self.profile.keys()]) # e.g. add condition: if k not in ['internal_id']

            # Display current values nicely, map number to key
            for key in profile_keys:
                value = self.profile[key]
                display_value = value # Default display
                # Format list values
                if isinstance(value, (list, tuple)):
                     display_value = ', '.join(map(str, value)) if value else "(Empty List)"
                # Mask password
                elif key == 'password':
                    display_value = '*' * len(str(value)) if value else "(No Password Set)"

                print(f"{i}. {key.replace('_', ' ').capitalize()}: {display_value}")
                editable_fields[i] = key
                i += 1

            # Add the "Finish Editing" option
            print(f"\n{i}. Finish Editing")

            # Get user's choice
            prompt = self.texts.get("edit_field_prompt", "Enter field number to edit (or press Enter to finish):")
            field_choice_str = get_input(prompt + " ").strip()

            if not field_choice_str: # Exit if user presses Enter
                break

            try:
                field_choice = int(field_choice_str)

                if field_choice == i: # Chose "Finish Editing"
                    break

                if field_choice in editable_fields:
                    field_to_edit = editable_fields[field_choice]
                    current_value = self.profile[field_to_edit]

                    print(f"\n--- Editing '{field_to_edit.replace('_', ' ').capitalize()}' ---")

                    # Handle different input types
                    if isinstance(current_value, list):
                        print(f"Current list: {current_value}")
                        print("Enter new comma-separated values (or leave blank to keep current):")
                        new_value_str = get_input("> ")
                        if new_value_str.strip():
                            self.profile[field_to_edit] = [v.strip() for v in new_value_str.split(',') if v.strip()]
                        # else: keep current value

                    elif isinstance(current_value, int) or field_to_edit == 'age': # Treat age as int
                        print(f"Current number: {current_value}")
                        print("Enter new number (or leave blank to keep current):")
                        while True:
                            new_value_str = get_input("> ").strip()
                            if not new_value_str:
                                break # Keep current
                            try:
                                new_value = int(new_value_str)
                                if field_to_edit == 'age' and not (18 <= new_value <= 99):
                                    print(self.texts["age_error"])
                                    continue # Ask for age again
                                self.profile[field_to_edit] = new_value
                                break # Valid number entered
                            except ValueError:
                                print("Invalid number. Please try again.")

                    else: # Assume string type for others (gender, name, username, password, location, profession, picture, appendix)
                        current_display = current_value if field_to_edit != 'password' else '*' * len(str(current_value))
                        print(f"Current value: {current_display}")
                        prompt_text = self.texts["edit_value_prompt"] + " (leave blank to keep current): "
                        new_value = get_input(prompt_text) # Don't strip immediately if spaces might be intended, unless for password/username
                        # Special handling for certain fields
                        if field_to_edit in ['username', 'password']:
                            new_value = new_value.strip() # Remove leading/trailing spaces

                        if new_value or (field_to_edit == 'password' and new_value == ''): # Allow setting empty password explicitly
                             if field_to_edit == 'password' and not new_value:
                                 print("Password will be cleared.")
                                 # Add confirmation maybe?
                             self.profile[field_to_edit] = new_value
                        # else: keep current value if blank was entered (except for password)

                    print("... Field updated (if a new value was provided).") # CORRECTED: Separated
                    time.sleep(0.8) # Brief pause

                else:
                    print(self.texts["invalid_choice"]) # CORRECTED: Separated
                    time.sleep(1)

            except ValueError:
                print(self.texts["invalid_choice"]) # CORRECTED: Separated
                time.sleep(1)
            # Outer while loop continues

    # --- persona_options and create_random_persona were assumed correct from previous turns ---
    # --- Add them back here if they were part of the original file content provided ---

    # Example placeholder for load_persona if it wasn't defined before
    def load_persona(self):
        """Loads an existing persona from a JSON file."""
        clear_screen()
        try:
            profiles = [f for f in os.listdir(self.profiles_dir) if f.endswith(".json")]
        except FileNotFoundError:
            print(f"Error: Profiles directory not found at {self.profiles_dir}")
            input(self.texts["continue_prompt"])
            return
        except OSError as e:
            print(f"Error accessing profiles directory: {e}")
            input(self.texts["continue_prompt"])
            return

        if not profiles:
            print(self.texts["no_personas_found"])
            input(self.texts["continue_prompt"])
            return

        print(self.texts["select_persona"])
        for i, profile_name in enumerate(profiles, 1):
            # Strip .json for display
            print(f"{i}. {profile_name[:-5]}")

        choice = get_numeric_choice(1, len(profiles))
        if choice is None:
            print("Loading cancelled.")
            input(self.texts["continue_prompt"])
            return

        selected_profile_file = profiles[choice - 1]
        profile_path = os.path.join(self.profiles_dir, selected_profile_file)
        profile_name_base = selected_profile_file[:-5] # Name without extension

        loaded_profile = load_json_file(profile_path)
        if loaded_profile:
            self.profile = loaded_profile
            print(self.texts["persona_loaded"])
            input(self.texts["continue_prompt"])
            # Call persona options menu AFTER loading
            self.persona_options(profile_path, profile_name_base)
        else:
            # load_json_file should print its own error
            print("Failed to load persona.")
            input(self.texts["continue_prompt"])


    # --- Added persona_options from previous turn for completeness ---
    def persona_options(self, profile_path, profile_name):
        """Display options for loaded persona, including deleting TXT export."""
        while True:
            clear_screen()
            print(f"--- Options for Persona: {profile_name} ---")
            # Use the text definition from TEXTS dict
            options_list = self.texts["persona_options_list"]
            for i, option in enumerate(options_list, 1):
                print(f"{i}. {option}")

            choice = get_numeric_choice(1, len(options_list))
            if choice is None: # Assume None means user wants to go back or cancelled input
                 print("Returning to main menu...")
                 time.sleep(1)
                 break # Exit the options loop

            if choice == 1:  # View details (using preview)
                self.preview_profile()
            elif choice == 2:  # Edit persona
                self.edit_profile() # Use the existing edit method
                # Save changes after editing
                try:
                    with open(profile_path, "w", encoding="utf-8") as f:
                        json.dump(self.profile, f, indent=2, ensure_ascii=False)
                    print("Changes saved.")
                except IOError as e:
                    print(f"Save Error after edit: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 3:  # Export persona (JSON)
                if not os.path.exists(self.exports_dir):
                    try:
                        os.makedirs(self.exports_dir)
                    except OSError as e:
                        print(f"Error creating exports directory: {e}")
                        input(self.texts["continue_prompt"])
                        continue # Skip export if dir fails

                # Create a timestamped export filename
                export_filename = f"{profile_name}_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                export_path = os.path.join(self.exports_dir, export_filename)
                try:
                    with open(export_path, "w", encoding="utf-8") as f:
                        json.dump(self.profile, f, indent=2, ensure_ascii=False)
                    print(self.texts["export_success"].format(export_path))
                except IOError as e:
                    print(f"JSON Export Error: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 4:  # Export persona (TXT)
                if not os.path.exists(self.exports_dir):
                     try:
                        os.makedirs(self.exports_dir)
                     except OSError as e:
                        print(f"Error creating exports directory: {e}")
                        input(self.texts["continue_prompt"])
                        continue
                try:
                    # export_profile_to_txt should handle its own file writing
                    txt_filepath = export_profile_to_txt(self.profile, profile_name, self.exports_dir) # Use base name for TXT
                    if txt_filepath:
                        print(self.texts["export_success"].format(txt_filepath))
                    else:
                        # export_profile_to_txt might return None/False or raise exception on error
                        print("TXT Export failed (check function implementation).")
                except Exception as e: # Catch potential errors from the export function itself
                    print(f"TXT Export Error: {e}")
                input(self.texts["continue_prompt"])
            elif choice == 5:  # Delete persona
                confirm = get_input(self.texts["confirm_delete"] + " (y/n): ").lower() # Added (y/n) hint
                if confirm in ["y", "yes"]:
                    deleted_json = False
                    deleted_txt = False
                    # Try deleting JSON profile
                    try:
                        os.remove(profile_path)
                        print(f"Deleted JSON: {profile_path}")
                        deleted_json = True
                    except OSError as e:
                        print(f"Error deleting JSON profile ({profile_path}): {e}")

                    # Try deleting corresponding TXT export (assuming name.txt)
                    txt_export_path = os.path.join(self.exports_dir, f"{profile_name}.txt")
                    if os.path.exists(txt_export_path):
                        try:
                            os.remove(txt_export_path)
                            print(f"Deleted TXT export: {txt_export_path}")
                            deleted_txt = True
                        except OSError as e:
                            print(f"Error deleting TXT export ({txt_export_path}): {e}")
                    else:
                        # If TXT doesn't exist, it's okay for deletion purpose
                        print(f"TXT export ({txt_export_path}) not found, skipping deletion.")
                        deleted_txt = True # Consider deletion successful if TXT wasn't there

                    if deleted_json: # Only proceed if JSON was deleted
                        if deleted_txt: # And TXT was deleted or didn't exist
                             print(self.texts["deleted_success"])
                             self.profile = {}  # Clear the loaded profile data in memory
                             input(self.texts["continue_prompt"])
                             break  # Exit options menu, return to main menu
                        else:
                             print("Deleted JSON, but could not remove associated TXT export.")
                             input(self.texts["continue_prompt"])
                             # Stay in options menu? Or break? Let's stay for now.
                    else:
                        print("Could not delete the main profile JSON file. No files removed.")
                        input(self.texts["continue_prompt"])
                else:
                    print("Deletion cancelled.")
                    input(self.texts["continue_prompt"])
            elif choice == 6: # Back to main menu
                break # Exit the while loop

    # --- Added create_random_persona from previous turn for completeness ---
    def create_random_persona(self):
        """Creates a persona with randomly selected attributes based on chosen level."""
        clear_screen()
        print(self.texts["random_level_select"])
        # Display options clearly
        level_options = self.texts["random_level_options"]
        for i, opt_desc in enumerate(level_options, 1):
             # Extract level number from description if needed, or just use index
             print(f"{i}. {opt_desc}") # Assumes format "N. Description"

        level_choice = get_numeric_choice(1, len(level_options))
        if level_choice is None:
            print("Random persona creation cancelled.")
            input(self.texts["continue_prompt"])
            return

        clear_screen()
        print("\n--- Generating Random Persona ---")
        print("Please wait while data is loaded and attributes are generated...\n")
        self.profile = {} # Start fresh
        pause_time = 0.3 # Shorter pause for slightly faster generation display

        # --- Load Data ---
        print("Loading necessary data files...")
        time.sleep(pause_time * 1.5) # Pause after loading message
        # Use try-except blocks for robustness when loading each file
        nationalities_data = load_json_file(os.path.join(self.data_dir, "nationalities.json"))
        professions_data = load_json_file(os.path.join(self.data_dir, "professions.json"))
        locations_data = load_json_file(os.path.join(self.data_dir, "locations.json"))
        interests_data = load_json_file(os.path.join(self.data_dir, "interests.json"))
        # Assuming english.txt for phrases, adjust if language selection is added
        phrases_data = load_data_file(os.path.join(self.data_dir, "common_phrases", "english.txt"))
        pictures_data = load_data_file(os.path.join(self.data_dir, "profile_pictures.txt"))
        # Need names and last names data loaded here too for Level 1
        # We'll load them dynamically based on selected nationality later

        # --- Level 1: Minimal ---
        print("\n--- Generating Level 1 Details ---")

        # Gender (Select first)
        print(f"{self.texts['random_generating'].format(item='Gender')}")
        self.profile["gender"] = random.choice(["male", "female"])
        print(f"-> Gender: {self.profile['gender'].capitalize()}")
        time.sleep(pause_time)

        # --- Loop to find valid Name/Nationality ---
        first_name = "Alex" # Default fallback
        last_name = "Smith" # Default fallback
        selected_nationality = "american" # Default fallback
        found_names = False
        max_retries = 50 # Safety break
        retries = 0

        print(f"{self.texts['random_generating'].format(item='Nationality & Names')}") # Combined message

        while not found_names and retries < max_retries:
            retries += 1
            current_nationality = "american" # Reset default for this attempt

            # Select Nationality for this attempt
            if nationalities_data:
                item, _ = get_random_hierarchical_item(nationalities_data)
                if item:
                    current_nationality = item.lower()
            # else: keep 'american' default

            # Try loading names for this nationality
            names_file = os.path.join(self.data_dir, "names", self.profile["gender"], f"{current_nationality}.txt")
            names_list = load_data_file(names_file)

            lastnames_file = os.path.join(self.data_dir, "last_names", f"{current_nationality}.txt")
            lastnames_list = load_data_file(lastnames_file)

            # Check if both lists are valid (not None and not empty)
            if names_list and lastnames_list: # Checks for None and [] implicitly (empty lists are False)
                selected_nationality = current_nationality # Store the successful nationality
                first_name = random.choice(names_list)
                last_name = random.choice(lastnames_list)
                found_names = True # Signal success
                # print(f"Debug: Found names for {selected_nationality} on attempt {retries}") # Optional debug
            else:
                 if retries % 5 == 0: # Print warning occasionally if it takes long
                     print(self.texts["random_name_retry_warning"].format(nationality=current_nationality))
                     time.sleep(0.1) # Small pause if retrying

        # --- End Loop ---

        # Handle fallback if loop finished without success
        if not found_names:
            print(self.texts["random_name_fallback_warning"])
            # Defaults for name/lastname/nationality are already set

        # Assign the found (or default) values
        self.profile["nationality"] = selected_nationality
        self.profile["first_name"] = first_name
        self.profile["last_name"] = last_name

        # Print results after loop/fallback
        print(f"-> Nationality: {self.profile['nationality'].capitalize()}")
        time.sleep(pause_time)
        # Print First Name separately now
        # print(f"{self.texts['random_generating'].format(item='First Name')}") # Message already printed above
        print(f"-> First Name: {self.profile['first_name']}")
        time.sleep(pause_time)
        # Print Last Name separately now
        # print(f"{self.texts['random_generating'].format(item='Last Name')}") # Message already printed above
        print(f"-> Last Name: {self.profile['last_name']}")
        time.sleep(pause_time)

        # Age (can remain as before)
        print(f"{self.texts['random_generating'].format(item='Age')}")
        self.profile["age"] = random.randint(18, 75)
        print(f"-> Age: {self.profile['age']}")
        time.sleep(pause_time)

        # Profession (can remain as before)
        print(f"{self.texts['random_generating'].format(item='Profession')}")
        selected_profession = "Unspecified"
        if professions_data:
            item, path = get_random_hierarchical_item(professions_data)
            selected_profession = item if item else (path[-1] if path else "Unspecified")
        self.profile["profession"] = selected_profession
        print(f"-> Profession: {self.profile['profession']}")
        time.sleep(pause_time)

        # --- Level 2: Standard ---
        if level_choice >= 2:
            print("\n--- Generating Level 2 Details ---")
            # Basic Location (e.g., Country, Region from random path)
            print(f"{self.texts['random_generating'].format(item='Basic Location')}")
            basic_location = "Earth"
            if locations_data:
                _, path = get_random_hierarchical_item(locations_data) # Get a random path
                # Take first 2 elements (e.g., Continent, Country) or fewer if path is short
                parts = path[:2]
                if parts: basic_location = ", ".join(reversed(parts)) # Format as Country, Continent
            # For level 2, we overwrite location if it exists, otherwise create it
            self.profile["location"] = basic_location
            print(f"-> Location: {self.profile['location']}")
            time.sleep(pause_time)
            # Username (using suggestions)
            print(f"{self.texts['random_generating'].format(item='Username')}")
            generated_user = f"{self.profile['first_name'][:4].lower()}{random.randint(100,999)}" # Fallback
            try:
                suggestions = generate_username_suggestions(self.profile['first_name'], self.profile['last_name'], self.profile['age'])
                if suggestions: generated_user = random.choice(suggestions)
            except Exception: pass # Use fallback if suggestion fails
            self.profile["username"] = generated_user
            print(f"-> Username: {self.profile['username']}")
            time.sleep(pause_time)
            # Password (standard length)
            print(f"{self.texts['random_generating'].format(item='Password')}")
            generated_password = generate_random_password(length=12) # Standard length
            self.profile["password"] = generated_password
            print(f"-> Password: {'*' * len(generated_password)}")
            time.sleep(pause_time)

        # --- Level 3: Detailed ---
        if level_choice >= 3:
            print("\n--- Generating Level 3 Details ---")
            # Detailed Location (overwrite L2 location)
            print(f"{self.texts['random_generating'].format(item='Detailed Location')}")
            detailed_location = self.profile.get("location", "Earth") # Start with previous if exists
            if locations_data:
                item, path = get_random_hierarchical_item(locations_data)
                if item: path.append(item) # Add leaf node if found
                # Take up to 4 elements (e.g., City, Region, Country, Continent)
                parts = path[:4]
                if parts: detailed_location = ", ".join(reversed(parts))
            self.profile["location"] = detailed_location # Overwrite location
            print(f"-> Location: {self.profile['location']}")
            time.sleep(pause_time)
            # Platforms
            print(f"{self.texts['random_generating'].format(item='Platforms')}")
            possible_platforms = [
                "Twitter", "Facebook", "Instagram", "Reddit", "LinkedIn", "TikTok",
                "Pinterest", "YouTube", "Discord", "Telegram", "Snapchat", "Mastodon", "Bluesky"
            ]
            num_platforms = random.randint(1, 4) # Choose 1 to 4 platforms
            num_platforms = min(num_platforms, len(possible_platforms)) # Ensure not asking for more than available
            selected_platforms = random.sample(possible_platforms, num_platforms)
            self.profile["platforms"] = selected_platforms
            print(f"-> Platforms: {', '.join(self.profile['platforms'])}")
            time.sleep(pause_time)
            # Interests (multiple random hierarchical)
            print(f"{self.texts['random_generating'].format(item='Interests')}")
            selected_interests = []
            if interests_data:
                attempts = 0
                max_interests_to_add = 5
                max_attempts_per_interest = 15 # Prevent infinite loop if data is sparse
                while len(selected_interests) < max_interests_to_add and attempts < max_attempts_per_interest * max_interests_to_add:
                    item, _ = get_random_hierarchical_item(interests_data)
                    if item and item not in selected_interests:
                        selected_interests.append(item)
                    attempts += 1
            self.profile["interests"] = selected_interests
            print(f"-> Interests: {', '.join(self.profile['interests']) if self.profile['interests'] else '(None found)'}")
            time.sleep(pause_time)

        # --- Level 4: Full ---
        if level_choice >= 4:
            print("\n--- Generating Level 4 Details ---")
            # Common Phrases
            print(f"{self.texts['random_generating'].format(item='Common Phrases')}")
            selected_phrases = []
            if phrases_data:
                num_phrases = random.randint(1, 3) # Choose 1 to 3 phrases
                num_phrases = min(num_phrases, len(phrases_data)) # Ensure not asking for more than available
                selected_phrases = random.sample(phrases_data, num_phrases)
            self.profile["common_phrases"] = selected_phrases
            print(f"-> Common Phrases: {len(self.profile['common_phrases'])} added")
            time.sleep(pause_time)
            # Profile Picture (filtered by gender if possible)
            print(f"{self.texts['random_generating'].format(item='Profile Picture')}")
            picture_url = None
            picture_added = False
            if pictures_data:
                gender_path_part = "/men/" if self.profile.get("gender") == "male" else "/women/"
                gender_specific_pics = [p for p in pictures_data if gender_path_part in p.lower()]
                if gender_specific_pics:
                    picture_url = random.choice(gender_specific_pics)
                elif pictures_data: # Fallback to any picture if no gender-specific found
                    picture_url = random.choice(pictures_data)

                if picture_url:
                    self.profile["profile_picture"] = picture_url
                    picture_added = True
            print(f"-> Picture Added: {'Yes' if picture_added else 'No'}")
            time.sleep(pause_time)

        # --- Completion & Save Prompt ---
        print(f"\n{self.texts['random_generation_complete']}") # CORRECTED: Separated
        input(self.texts["continue_prompt"])

        self.preview_profile() # Show the generated profile

        # Ask to save
        save_choice = get_input(self.texts.get("confirm_save_random", "Save this generated profile? (y/n): ")).lower().strip()
        if save_choice in ["y", "yes"]:
            # Call the existing save/export helper method
             self._save_and_export_profile() # This handles filename prompt, save, export, and pause
        else:
            print("Profile not saved.") # CORRECTED: Separated
            input(self.texts["continue_prompt"])


    def show_program_info(self):
        """Display program information."""
        clear_screen() # CORRECTED: Separated
        display_ascii_art(self.data_dir)
        print(self.texts["program_info"])
        input(self.texts["continue_prompt"]) # CORRECTED: Separated




# ==============================================================================
# Main Execution Block
# ==============================================================================
def main():
    """Main function to run the Sock Spy application."""
    # Perform environment checks if necessary (e.g., Python version)
    if sys.version_info < (3, 8): # Example check
         print("Sock Spy requires Python 3.8 or newer.")
         sys.exit(1)

    app = SockSpy()
    try:
        # --- Add Cache Update Call Here ---
        clear_screen()
        display_ascii_art(app.data_dir) # Show logo while processing
        print("\nPerforming startup tasks...")
        app._update_name_counts_cache() # Run the calculation
        # --- End Cache Update Call ---

        # Proceed with normal startup
        # app.display_welcome() # Welcome message is now part of display_welcome
        input("Press Enter to proceed to the main menu...") # Pause after cache update

        app.main_menu() # Go to main menu

    except KeyboardInterrupt:
        clear_screen()
        display_ascii_art(app.data_dir) # Access data_dir via app instance
        print("\n\nOperation cancelled by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        # Generic error handler for unexpected issues
        clear_screen()
        print("\n--- UNEXPECTED ERROR ---")
        print(f"An error occurred: {e}")
        import traceback
        print("\n--- Traceback ---")
        traceback.print_exc()
        print("\n--------------------")
        print("Please report this issue if it persists.")
        input("Press Enter to attempt to exit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
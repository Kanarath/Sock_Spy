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
------------------------
Utility functions for Sock Spy CLI Tool
"""

import os
import sys
import json
import random
import datetime
import string

def clear_screen():
    """Clear the terminal screen based on operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data_file(filepath):
    """Load data from a text file, one item per line"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read lines, strip whitespace, and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        # Keep error messages concise for the user
        print(f"Warning: Data file not found: {filepath}")
        return []
    except Exception as e:
        print(f"Warning: Error reading file {filepath}: {e}")
        return []

def load_json_file(filepath):
    """Load data from a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: JSON file not found: {filepath}")
        return {} # Return empty dict for consistency
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in file: {filepath}")
        return {} # Return empty dict
    except Exception as e:
        print(f"Warning: Error reading JSON file {filepath}: {e}")
        return {}

def save_profile(profile, filename, profiles_dir):
    """Save profile to a JSON file"""
    try:
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)

        # Sanitize filename slightly (replace spaces, avoid path traversal)
        safe_filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-')).rstrip()
        if not safe_filename:
            safe_filename = f"profile_{random.randint(1000,9999)}"

        filepath = os.path.join(profiles_dir, f"{safe_filename}.json")

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        return filepath
    except Exception as e:
        print(f"Error saving profile to {filename}.json: {e}")
        return None

def export_profile_to_txt(profile, filename, exports_dir):
    """Export profile to a text file"""
    # --- NOTE: This function still contains Spanish headers ---
    # You might want to replace "Datos básicos", "Credenciales", etc. with English equivalents
    # from your TEXTS["en"] dictionary for consistency.
    try:
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)

        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-')).rstrip()
        if not safe_filename:
            safe_filename = f"profile_{random.randint(1000,9999)}"

        filepath = os.path.join(exports_dir, f"{safe_filename}.txt")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("===== SOCK SPY PROFILE =====\n\n")

            # Basic Data (Example using English keys, update headers manually)
            f.write("===== BASIC DATA =====\n") # Changed header
            f.write(f"First Name: {profile.get('first_name', 'N/A')}\n")
            f.write(f"Last Name: {profile.get('last_name', 'N/A')}\n")
            f.write(f"Gender: {profile.get('gender', 'N/A').capitalize()}\n") # Capitalize for display
            f.write(f"Age: {profile.get('age', 'N/A')}\n")
            f.write(f"Nationality: {profile.get('nationality', 'N/A').capitalize()}\n") # Capitalize
            f.write(f"Location: {profile.get('location', 'N/A')}\n\n")

            # Credentials
            f.write("===== CREDENTIALS =====\n") # Changed header
            f.write(f"Username: {profile.get('username', 'N/A')}\n")
            f.write(f"Password: {profile.get('password', 'N/A')}\n\n") # Consider omitting/masking password in export

            # Platforms
            f.write("===== PLATFORMS =====\n")
            platforms = profile.get('platforms', [])
            if platforms:
                for platform in platforms:
                    f.write(f"- {platform}\n")
            else:
                f.write("No platforms specified\n")
            f.write("\n")

            # Interests
            f.write("===== INTERESTS =====\n")
            interests = profile.get('interests', [])
            if interests:
                for interest in interests:
                    f.write(f"- {interest}\n")
            else:
                f.write("No interests specified\n")
            f.write("\n")

            # Profession
            f.write(f"Profession: {profile.get('profession', 'N/A')}\n\n")

            # Biography (Check if 'biography' key exists)
            if 'biography' in profile:
                f.write("===== BIOGRAPHY =====\n")
                f.write(f"{profile.get('biography', 'No biography available')}\n\n")

            # Common Phrases
            if 'common_phrases' in profile and profile['common_phrases']:
                f.write("===== COMMON PHRASES =====\n")
                for phrase in profile['common_phrases']:
                    f.write(f"- {phrase}\n")
                f.write("\n")

            # Profile Picture
            if 'profile_picture' in profile:
                f.write(f"Profile Picture URL: {profile['profile_picture']}\n\n")

            # Appendix
            if 'appendix' in profile:
                f.write("===== APPENDIX =====\n")
                f.write(f"{profile['appendix']}\n\n")

            f.write("===== END OF PROFILE =====\n")

        return filepath
    except Exception as e:
        print(f"Error exporting profile to {filename}.txt: {e}")
        return None


def display_ascii_art(data_dir):
    """Display a random ASCII art from the ascii_art directory"""
    ascii_dir = os.path.join(data_dir, "ascii_art")
    displayed = False
    if os.path.exists(ascii_dir) and os.path.isdir(ascii_dir):
        try:
            ascii_files = [f for f in os.listdir(ascii_dir) if f.endswith('.txt')]
            if ascii_files:
                ascii_file = os.path.join(ascii_dir, random.choice(ascii_files))
                try:
                    with open(ascii_file, 'r', encoding='utf-8') as f:
                        print(f.read())
                    displayed = True
                except Exception as e:
                    print(f"Warning: Could not read ASCII file {ascii_file}: {e}")
        except Exception as e:
            print(f"Warning: Could not list ASCII files in {ascii_dir}: {e}")

    # Fallback ASCII art if no files are found or errors occur
    if not displayed:
        print("""
   _____            _      _____
  / ____|          | |    / ____|
 | (___   ___   ___| | __| (___  _ __  _   _
  \___ \ / _ \ / __| |/ /\___ \| '_ \| | | |
  ____) | (_) | (__|   < ____) | |_) | |_| |
 |_____/ \___/ \___|_|\_\_____/| .__/ \__, |
                               | |     __/ |
                               |_|    |___/
        """)

def get_input(prompt):
    """Get user input with a prompt, handling potential EOFError"""
    try:
        return input(prompt + " ")
    except EOFError:
        print("\nInput stream closed unexpectedly. Exiting.")
        sys.exit(1)


# --- MODIFIED/NEW FUNCTIONS BELOW ---

def get_numeric_choice(min_val, max_val, prompt="> "):
    """
    Gets numeric input within a specified range.
    Returns the integer choice or None if input is empty.
    """
    while True:
        try:
            choice_str = get_input(prompt).strip() # Use get_input helper
            if not choice_str: # Allow empty input to cancel/go back
                return None
            choice = int(choice_str)
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        # Removed EOFError handling here as it's in get_input

def handle_dynamic_list_selection(full_list, texts, prompt_msg, initial_show=5, increment=5, allow_skip=False):
    """
    Handles displaying a list with options for 'Show More', 'Regenerate', and optionally 'Skip/Stop'.

    Args:
        full_list (list): The complete list of items to choose from.
        texts (dict): The dictionary containing UI text strings (needs specific keys defined).
        prompt_msg (str): The specific question/prompt to display before the list.
        initial_show (int): Number of items to show initially.
        increment (int): Number of items to add when 'Show More' is chosen.
        allow_skip (bool): If True, add the 'Skip/Stop Here' option.

    Returns:
        tuple: (selected_item, action)
            - selected_item: The item chosen by the user, or None if an action was taken/list empty.
            - action: 'selected', 'regenerate', 'show_more', 'skip', 'back'
                        ('back' used if list is empty or choice is None)
    """
    if not full_list:
        print("No options available for this selection.")
        # input(texts.get("continue_prompt", "Press Enter to continue...")) # Optional pause
        return None, 'back' # Indicate nothing to select

    # Use indices for easier management of displayed vs. available
    available_indices = list(range(len(full_list)))
    displayed_indices = random.sample(available_indices, min(initial_show, len(full_list)))
    displayed_indices.sort() # Keep displayed items ordered by original list index initially

    # Text keys expected in the 'texts' dictionary
    text_select_action = texts.get("select_or_action", "Select an item or choose an action:")
    text_show_more = texts.get("show_more_options", "Show More Options")
    text_regenerate = texts.get("regenerate_options", "Show New Options (Regenerate List)")
    text_skip_level = texts.get("skip_level_and_continue", "Use current selection level and continue")
    text_invalid_choice = texts.get("invalid_choice", "Invalid choice.")
    text_continue = texts.get("continue_prompt", "Press Enter to continue...")


    while True:
        clear_screen()
        print(prompt_msg)
        print(text_select_action)

        current_options_map = {i + 1: full_list[idx] for i, idx in enumerate(displayed_indices)}

        for num, item in current_options_map.items():
            print(f"{num}. {item}")

        print("-" * 20) # Separator

        option_offset = len(current_options_map)
        show_more_opt_num = option_offset + 1
        regenerate_opt_num = option_offset + 2
        skip_opt_num = option_offset + 3 if allow_skip else -1 # Only valid if allow_skip is True

        current_max_choice = option_offset # Start with max item number

        # Option: Show More
        can_show_more = len(displayed_indices) < len(full_list)
        if can_show_more:
            print(f"{show_more_opt_num}. {text_show_more}")
            current_max_choice = show_more_opt_num
        else:
            # Don't print the option if all items are already shown
            show_more_opt_num = -1 # Invalidate the number


        # Option: Regenerate
        print(f"{regenerate_opt_num}. {text_regenerate}")
        current_max_choice = regenerate_opt_num

        # Option: Skip/Stop
        if allow_skip:
            print(f"{skip_opt_num}. {text_skip_level}")
            current_max_choice = skip_opt_num

        # Get user choice using the updated get_numeric_choice
        choice = get_numeric_choice(1, current_max_choice)

        if choice is None:
            # Empty input likely means user wants to cancel/go back
            print("Selection cancelled.")
            # input(text_continue) # Optional pause
            return None, 'back'

        # --- Handle Actions ---
        if can_show_more and choice == show_more_opt_num:
            remaining_indices = [i for i in available_indices if i not in displayed_indices]
            if remaining_indices:
                num_to_add = min(increment, len(remaining_indices))
                # Sample from remaining, don't add duplicates
                new_indices = random.sample(remaining_indices, num_to_add)
                displayed_indices.extend(new_indices)
                displayed_indices.sort() # Maintain order if desired
            # Loop continues to redisplay with more items
            continue

        elif choice == regenerate_opt_num:
            # Resample completely new indices from all available
            num_to_show = min(initial_show, len(full_list)) # Start with initial count again
            displayed_indices = random.sample(available_indices, num_to_show)
            displayed_indices.sort()
            # Loop continues to redisplay regenerated list
            continue

        elif allow_skip and choice == skip_opt_num:
            # Signal to the calling function to skip/stop at the current level
            return None, 'skip'

        # --- Handle Item Selection ---
        # Check if the choice is a valid item number from the current display
        elif choice in current_options_map:
            selected_item = current_options_map[choice]
            return selected_item, 'selected'

        else:
            # This case should ideally not be reached if get_numeric_choice is correct
            print(text_invalid_choice)
            input(text_continue) # Pause to show error
            # Loop continues

# --- End of new / modified functions ---


def generate_username_suggestions(first_name, last_name, age):
    """Generate username suggestions based on name and age"""
    suggestions = []
    fn = first_name.lower().replace(" ", "") # Remove spaces
    ln = last_name.lower().replace(" ", "")
    if not fn: fn = "user"
    if not ln: ln = str(random.randint(100,999))

    try:
        # Basic combinations
        suggestions.append(f"{fn}{ln}")
        suggestions.append(f"{fn}_{ln}")
        suggestions.append(f"{fn}{ln[0] if ln else ''}") # First name + last initial
        suggestions.append(f"{fn[0] if fn else ''}{ln}") # First initial + last name

        # Add age or birth year
        if 18 <= age <= 99:
            suggestions.append(f"{fn}{ln}{age}")
            try:
                birth_year = get_current_year() - age
                suggestions.append(f"{fn}{ln}{str(birth_year)[-2:]}") # Last two digits of birth year
            except Exception: pass # Ignore errors calculating year

        # Add random numbers
        suggestions.append(f"{fn}{ln}{random.randint(10, 999)}")
        suggestions.append(f"{fn}_{ln}{random.randint(10, 99)}")

        # Mix initials and numbers
        suggestions.append(f"{fn[0] if fn else 'u'}{ln[0] if ln else 's'}{random.randint(100, 9999)}")

        # Use parts of names
        fn_part = fn[:max(1, len(fn)//2)] # First half of first name
        ln_part = ln[:max(1, len(ln)//2)] # First half of last name
        suggestions.append(f"{fn_part}{ln_part}{random.randint(10, 99)}")

        # Ensure unique suggestions and limit count
        unique_suggestions = list(dict.fromkeys(suggestions)) # Remove duplicates preserving order
        return unique_suggestions[:8] # Return max 8 suggestions
    except Exception as e:
        # Fallback in case of unexpected errors with names/age
        print(f"Warning: Could not generate all username suggestions: {e}")
        return [f"{fn}{ln}{random.randint(100,999)}"]


def get_current_year():
    """Get the current year"""
    return datetime.datetime.now().year

def load_hierarchical_data(data_dir, category, subcategory=None):
    """
    DEPRECATED/REDUNDANT?
    Load hierarchical data. Consider removing if main script loads full JSON directly.
    """
    # This function might be less useful if the main script now handles the
    # hierarchical navigation directly by loading the full JSON file.
    # Keeping it for now, but review its usage in your main script.
    try:
        filepath = os.path.join(data_dir, f"{category}.json")
        if os.path.exists(filepath):
            data = load_json_file(filepath) # Use existing JSON loader
            if subcategory:
                # Basic check for subcategory key
                return data.get(subcategory, {})
            return data
        else:
            # Fallback to flat file if hierarchical data doesn't exist (optional)
            filepath_flat = os.path.join(data_dir, category, "general.txt")
            if os.path.exists(filepath_flat):
                return {"General": load_data_file(filepath_flat)}
            else:
                print(f"Warning: Neither {filepath} nor fallback {filepath_flat} found.")
                return {}
    except Exception as e:
        print(f"Error loading hierarchical data for {category}: {e}")
        return {}

def generate_random_password(length=12):
    """Generates a random password with letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    # Ensure password meets complexity if needed (e.g., at least one of each type)
    # For simplicity now, just pick random characters
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def get_random_hierarchical_item(data):
    """
    Navigates a nested dictionary/list structure randomly and returns a
    random item from the deepest list found, along with the path taken.

    Args:
        data: The nested dictionary or list.

    Returns:
        tuple: (selected_item, path_list) or (None, []) if error/no list found.
        selected_item is None if the deepest level wasn't a non-empty list.
    """
    current_level = data
    path = []
    max_depth = 10 # Prevent infinite loops in case of weird data

    try:
        for _ in range(max_depth):
            if isinstance(current_level, dict):
                if not current_level: break # Stop if dict is empty
                key = random.choice(list(current_level.keys()))
                path.append(key)
                current_level = current_level[key]
            elif isinstance(current_level, list):
                if not current_level: break # Stop if list is empty
                selected_item = random.choice(current_level)
                # path.append(selected_item) # Option: Add the item itself to the path?
                return selected_item, path # Found a list, return item and path leading to it
            else:
                # Reached a non-dict/non-list item before finding a list
                break
    except Exception as e:
        print(f"Warning: Error during random hierarchical navigation: {e}")
        return None, [] # Return empty on error

    # If loop finished without returning (empty dict/list encountered, or max depth reached)
    # Return the last valid part of the path, or None if nothing selected
    last_item = path[-1] if path else None
    return None, path # Indicate no specific item selected from a list

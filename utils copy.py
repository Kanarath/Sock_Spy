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

def clear_screen():
    """Clear the terminal screen based on operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data_file(filepath):
    """Load data from a text file, one item per line"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return []

def load_json_file(filepath):
    """Load data from a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {filepath}")
        return {}

def save_profile(profile, filename, profiles_dir):
    """Save profile to a JSON file"""
    if not os.path.exists(profiles_dir):
        os.makedirs(profiles_dir)
    
    filepath = os.path.join(profiles_dir, f"{filename}.json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    return filepath

def export_profile_to_txt(profile, filename, exports_dir):
    """Export profile to a text file"""
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    filepath = os.path.join(exports_dir, f"{filename}.txt")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("===== SOCK SPY PROFILE =====\n\n")
        
        # Datos básicos
        f.write(f"First Name: {profile.get('first_name', 'N/A')}\n")
        f.write(f"Last Name: {profile.get('last_name', 'N/A')}\n")
        f.write(f"Gender: {profile.get('gender', 'N/A')}\n")
        f.write(f"Age: {profile.get('age', 'N/A')}\n")
        f.write(f"Nationality: {profile.get('nationality', 'N/A')}\n")
        f.write(f"Location: {profile.get('location', 'N/A')}\n\n")
        
        # Credenciales
        f.write("===== CREDENTIALS =====\n")
        f.write(f"Username: {profile.get('username', 'N/A')}\n")
        f.write(f"Password: {profile.get('password', 'N/A')}\n\n")
        
        # Plataformas
        f.write("===== PLATFORMS =====\n")
        platforms = profile.get('platforms', [])
        if platforms:
            for platform in platforms:
                f.write(f"- {platform}\n")
        else:
            f.write("No platforms specified\n")
        f.write("\n")
        
        # Intereses
        f.write("===== INTERESTS =====\n")
        interests = profile.get('interests', [])
        if interests:
            for interest in interests:
                f.write(f"- {interest}\n")
        else:
            f.write("No interests specified\n")
        f.write("\n")
        
        # Profesión
        f.write(f"Profession: {profile.get('profession', 'N/A')}\n\n")
        
        # Biografía
        f.write("===== BIOGRAPHY =====\n")
        f.write(f"{profile.get('biography', 'No biography available')}\n\n")
        
        # Frases comunes
        if 'common_phrases' in profile:
            f.write("===== COMMON PHRASES =====\n")
            for phrase in profile['common_phrases']:
                f.write(f"- {phrase}\n")
            f.write("\n")
        
        # Foto de perfil
        if 'profile_picture' in profile:
            f.write(f"Profile Picture URL: {profile['profile_picture']}\n\n")
        
        # Apéndice
        if 'appendix' in profile:
            f.write("===== APPENDIX =====\n")
            f.write(f"{profile['appendix']}\n\n")
        
        f.write("===== END OF PROFILE =====\n")
    
    return filepath

def display_ascii_art(data_dir):
    """Display a random ASCII art from the ascii_art directory"""
    ascii_dir = os.path.join(data_dir, "ascii_art")
    if os.path.exists(ascii_dir):
        ascii_files = [f for f in os.listdir(ascii_dir) if f.endswith('.txt')]
        if ascii_files:
            ascii_file = os.path.join(ascii_dir, random.choice(ascii_files))
            try:
                with open(ascii_file, 'r', encoding='utf-8') as f:
                    print(f.read())
                return
            except Exception:
                pass
    
    # Fallback ASCII art if no files are found
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
    """Get user input with a prompt"""
    return input(prompt + " ")

def get_numeric_choice(min_val, max_val):
    """Get a numeric choice from user within a range"""
    while True:
        try:
            choice = int(input("> "))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")

def generate_username_suggestions(first_name, last_name, age):
    """Generate username suggestions based on name and age"""
    suggestions = []
    
    # First and last name (lowercase)
    suggestions.append(f"{first_name.lower()}{last_name.lower()}")
    
    # First name, last name, and age
    suggestions.append(f"{first_name.lower()}{last_name.lower()}{age}")
    
    # First name, last name, and birth year
    birth_year = get_current_year() - age
    suggestions.append(f"{first_name.lower()}{last_name.lower()}{birth_year}")
    
    # First name initial and last name initial, plus a random number
    suggestions.append(f"{first_name[0].lower()}{last_name[0].lower()}{random.randint(100, 999)}")
    
    # First three letters of the first and last names
    first_three = first_name[:3].lower() if len(first_name) >= 3 else first_name.lower()
    last_three = last_name[:3].lower() if len(last_name) >= 3 else last_name.lower()
    suggestions.append(f"{first_three}{last_three}{random.randint(10, 99)}")
    
    return suggestions

def get_current_year():
    """Get the current year"""
    return datetime.datetime.now().year

def load_hierarchical_data(data_dir, category, subcategory=None):
    """Load hierarchical data for interests and professions"""
    try:
        filepath = os.path.join(data_dir, f"{category}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if subcategory:
                    return data.get(subcategory, {})
                return data
        else:
            # Fallback to flat file if hierarchical data doesn't exist
            filepath = os.path.join(data_dir, category, "general.txt")
            return {"General": load_data_file(filepath)}
    except Exception as e:
        print(f"Error loading hierarchical data: {e}")
        return {"General": []}

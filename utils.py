import json

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:  # Agregar encoding
        json.dump(data, f, indent=4, ensure_ascii=False) # Asegurar que se guarden bien caracteres especiales

def load_list(filename):
    with open(filename, "r", encoding="utf-8") as f:  # Agregar encoding
        return [line.strip() for line in f]
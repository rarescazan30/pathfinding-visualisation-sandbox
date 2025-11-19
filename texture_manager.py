import pygame
import os
from graphical_interface.constants import *

# Definim categoriile pe baza folderului tău de assets
TEXTURE_CATEGORIES = [
    'wall', 'start', 'end', 'path', 
    'search', 'margin_of_search', 'background'
]
TEXTURE_NAMES = {
    'wall': 'Wall',
    'start': 'Start',
    'end': 'End',
    'path': 'Path',
    'search': 'Search',
    'margin_of_search': 'Visited', # Am mapat "search_end" la "Visited"
    'background': 'Ground'
}


class TextureManager:
    def __init__(self):
        """
        Încarcă toate texturile originale la inițializare
        folosind numele de fișiere specifice.
        """
        
        # --- MODIFICARE ---
        # Am înlocuit bucla care genera nume cu această hartă
        # care conține numele fișierelor tale.
        self.texture_filename_map = {
            'wall': ['brick_wall.png', 'stone_wall.png', 'wood_wall.png'],
            'start': ['woman_start.png', 'main_character_start.png', 'evil_main_character_start.png'],
            'end': ['brick_end.png', 'stone_end.png', 'wood_end.png'],
            'path': ['carpet_path.png', 'coin_path.png', 'romania_path.png'],
            'search': ['spiral_search.png', 'sparkle_search.png', 'truce_search.png'],
            'margin_of_search': ['spiral_search_end.png', 'sparkle_search_end.png', 'truce_search_end.png'],
            'background': ['grass_background.png', 'rock_background.png', 'dirt_background.png']
        }
        # --- SFÂRȘIT MODIFICARE ---
        
        self.original_textures = {}
        self.active_texture_index = {}
        self.scaled_textures = {}
        
        base_path = os.path.join('assets', 'textures')

        # --- MODIFICARE ---
        # Acum iterăm prin "harta" de nume, nu mai generăm nume.
        for category, filenames in self.texture_filename_map.items():
            self.original_textures[category] = []
            self.active_texture_index[category] = 0
            self.scaled_textures[category] = []
            
            for filename in filenames:
                path = os.path.join(base_path, filename)
                if os.path.exists(path):
                    try:
                        image = pygame.image.load(path).convert_alpha()
                        self.original_textures[category].append(image)
                    except pygame.error as e:
                        print(f"Eroare la încărcarea texturii: {path} - {e}")
                else:
                    # Acest avertisment este acum mult mai specific
                    print(f"AVERTISMENT: Textura lipsă! Nu am găsit: {path}")
        # --- SFÂRȘIT MODIFICARE ---
        
        print("Managerul de texturi a încărcat imaginile (cu nume personalizate).")


    def update_scaled_textures(self, gap):
        """
        Redimensionează toate texturile originale la mărimea 'gap'
        și le stochează în self.scaled_textures.
        (Nicio modificare aici)
        """
        self.scaled_textures = {}
        new_size = (gap, gap)
        
        for category, images in self.original_textures.items():
            scaled_images = []
            for img in images:
                try:
                    scaled_img = pygame.transform.scale(img, new_size)
                    scaled_images.append(scaled_img)
                except Exception as e:
                    print(f"Eroare la scalarea imaginii pentru {category}: {e}")
            self.scaled_textures[category] = scaled_images

    def get_active_texture(self, category):
        """
        Returnează textura activă (și scalată) pentru o categorie dată.
        (Nicio modificare aici)
        """
        if category not in self.scaled_textures:
            # Fallback dacă o categorie nu e mapată corect
            print(f"EROARE: Categoria '{category}' nu a fost găsită în texturile scalate.")
            # Încercăm să returnăm un fundal ca fallback
            if 'background' in self.scaled_textures and self.scaled_textures['background']:
                return self.scaled_textures['background'][0]
            else:
                # Fallback extrem
                return pygame.Surface((10,10)) 
            
        index = self.active_texture_index[category]
        
        if index < len(self.scaled_textures[category]):
            return self.scaled_textures[category][index]
        else:
            # Fallback dacă indexul e invalid
            print(f"Index invalid {index} pentru {category}, folosim index 0.")
            if self.scaled_textures[category]:
                 self.active_texture_index[category] = 0
                 return self.scaled_textures[category][0]
            else:
                # Fallback extrem dacă lista e goală
                print(f"EROARE: Nicio textură scalată încărcată pentru {category}")
                return pygame.Surface((10,10))

    def set_active_texture_index(self, category, index):
        """
        Setează indexul activ (0, 1, sau 2) pentru o categorie.
        (Nicio modificare aici)
        """
        if category in self.active_texture_index:
            if 0 <= index < len(self.original_textures[category]):
                self.active_texture_index[category] = index
            else:
                print(f"AVERTISMENT: Indexul {index} este invalid pentru categoria {category}.")
        else:
            print(f"AVERTISMENT: Categoria {category} nu există în managerul de texturi.")
            
    def get_original_texture(self, category, index):
        """
        Returnează o textură originală (nescalată) după categorie și index.
        Util pentru a afișa miniaturi pe butoane.
        (Nicio modificare aici)
        """
        try:
            return self.original_textures[category][index]
        except (KeyError, IndexError):
            print(f"Eroare: Nu s-a putut obține textura originală {category}[{index}]")
            # Returnăm o suprafață goală ca fallback
            return pygame.Surface((60, 60))
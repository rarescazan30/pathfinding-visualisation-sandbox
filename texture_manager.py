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
    'margin_of_search': 'Visited', 
    'background': 'Ground'
}


class TextureManager:
    def __init__(self):
        """
        Încarcă texturile originale și definește culorile pentru al 3-lea set.
        """
        
        # 1. Harta pentru IMAGINI (doar primele 2 seturi)
        self.texture_filename_map = {
            'wall': ['wall_garden.png', 'wall_2.png'],
            'start': ['start_1.png', 'start_2.png'],
            'end': ['end_1_green.png', 'end_2.png'],
            'path': ['path_1.png', 'path_2.png'],
            'margin_of_search': ['visited_1.png', 'visited_2.png'],
            'search': ['margin_1.png', 'margin_2.png'],
            'background': ['background_1.png', 'back_1.png']
        }

        # 2. Harta pentru CULORI (al 3-lea set - Modern Flat Theme)
        self.color_theme_map = {
            'wall': (44, 62, 80),          # Midnight Blue (Solid)
            'start': (231, 76, 60),        # Alizarin Red (Vibrant)
            'end': (241, 196, 15),         # Sunflower Yellow (Bright)
            'path': (155, 89, 182),        # Amethyst (Distinct)
            'search': (46, 204, 113),      # Emerald Green (Active)
            'margin_of_search': (26, 188, 156), # Turquoise (Visited)
            'background': (253, 225, 150)  # Warm Cream
        }
        
        self.original_textures = {}
        self.active_texture_index = {}
        self.scaled_textures = {}
        
        base_path = os.path.join('assets', 'textures')

        # Încărcăm imaginile și generăm culorile
        for category in TEXTURE_CATEGORIES:
            self.original_textures[category] = []
            
            # --- MODIFICARE: Setăm default la 2 (Culori/Flat Theme) ---
            # Index 0 = Imagine 1, Index 1 = Imagine 2, Index 2 = Culori
            self.active_texture_index[category] = 2 
            # --- SFÂRȘIT MODIFICARE ---
            
            self.scaled_textures[category] = []
            
            # Pasul A: Încărcăm imaginile (Index 0 și 1)
            filenames = self.texture_filename_map.get(category, [])
            for filename in filenames:
                path = os.path.join(base_path, filename)
                if os.path.exists(path):
                    try:
                        image = pygame.image.load(path).convert_alpha()
                        self.original_textures[category].append(image)
                    except pygame.error as e:
                        print(f"Eroare la încărcarea texturii: {path} - {e}")
                else:
                    print(f"AVERTISMENT: Textura lipsă! Nu am găsit: {path}")
            
            # Pasul B: Generăm "Imaginea" de culoare (Index 2)
            if category in self.color_theme_map:
                color_surface = pygame.Surface((60, 60))
                color_surface.fill(self.color_theme_map[category])
                self.original_textures[category].append(color_surface)

        print("Managerul de texturi a încărcat imaginile și a generat culorile.")


    def update_scaled_textures(self, gap):
        """
        Redimensionează toate texturile (inclusiv cele generate din culori)
        la mărimea 'gap' și le stochează în self.scaled_textures.
        """
        self.scaled_textures = {}
        safe_gap = max(1, gap)
        new_size = (safe_gap, safe_gap)
        
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
        """
        if category not in self.scaled_textures:
            print(f"EROARE: Categoria '{category}' nu a fost găsită în texturile scalate.")
            if 'background' in self.scaled_textures and self.scaled_textures['background']:
                return self.scaled_textures['background'][0]
            else:
                return pygame.Surface((10,10)) 
            
        index = self.active_texture_index[category]
        
        if index < len(self.scaled_textures[category]):
            return self.scaled_textures[category][index]
        else:
            print(f"Index invalid {index} pentru {category}, folosim index 0.")
            if self.scaled_textures[category]:
                 self.active_texture_index[category] = 0
                 return self.scaled_textures[category][0]
            else:
                print(f"EROARE: Nicio textură scalată încărcată pentru {category}")
                return pygame.Surface((10,10))

    def set_active_texture_index(self, category, index):
        """
        Setează indexul activ (0, 1, sau 2) pentru o categorie.
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
        """
        try:
            return self.original_textures[category][index]
        except (KeyError, IndexError):
            print(f"Eroare: Nu s-a putut obține textura originală {category}[{index}]")
            return pygame.Surface((60, 60))
import pygame
import os
from ui.constants import *

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
        # load original textures and color theme
        self.texture_filename_map = {
            'wall': ['wall_garden.png', 'wall_2.png'],
            'start': ['start_1.png', 'start_2.png'],
            'end': ['end_1_green.png', 'end_2.png'],
            'path': ['path_1.png', 'path_2.png'],
            'margin_of_search': ['visited_1.png', 'visited_2.png'],
            'search': ['margin_1.png', 'margin_2.png'],
            'background': ['background_1.png', 'back_1.png']
        }

        self.color_theme_map = {
            'wall': (44, 62, 80),
            'start': (231, 76, 60),
            'end': (241, 196, 15),
            'path': (155, 89, 182),
            'search': (46, 204, 113),
            'margin_of_search': (26, 188, 156),
            'background': (253, 225, 150)
        }

        self.original_textures = {}
        self.active_texture_index = {}
        self.scaled_textures = {}
        
        base_path = os.path.join('assets', 'textures')

        for category in TEXTURE_CATEGORIES:
            self.original_textures[category] = []
            self.active_texture_index[category] = 2  # Default to color theme
            self.scaled_textures[category] = []

            filenames = self.texture_filename_map.get(category, [])
            for filename in filenames:
                path = os.path.join(base_path, filename)
                if os.path.exists(path):
                    try:
                        image = pygame.image.load(path).convert_alpha()
                        self.original_textures[category].append(image)
                    except pygame.error:
                        pass

            if category in self.color_theme_map:
                color_surface = pygame.Surface((60, 60))
                color_surface.fill(self.color_theme_map[category])
                self.original_textures[category].append(color_surface)

    # Scale all textures to gap size
    def update_scaled_textures(self, gap):
        self.scaled_textures = {}
        safe_gap = max(1, gap)
        new_size = (safe_gap, safe_gap)

        for category, images in self.original_textures.items():
            scaled_images = []
            for img in images:
                try:
                    scaled_img = pygame.transform.scale(img, new_size)
                    scaled_images.append(scaled_img)
                except Exception:
                    pass
            self.scaled_textures[category] = scaled_images

    def get_active_texture(self, category):
        if category not in self.scaled_textures or not self.scaled_textures[category]:
            return pygame.Surface((10, 10))
        index = self.active_texture_index[category]
        if index < len(self.scaled_textures[category]):
            return self.scaled_textures[category][index]
        self.active_texture_index[category] = 0
        return self.scaled_textures[category][0]

    def set_active_texture_index(self, category, index):
        if category in self.active_texture_index and 0 <= index < len(self.original_textures[category]):
            self.active_texture_index[category] = index

    def get_original_texture(self, category, index):
        try:
            return self.original_textures[category][index]
        except (KeyError, IndexError):
            return pygame.Surface((60, 60))

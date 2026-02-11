"""
Player Selection Screen for Aggravation Game

This module provides a UI for selecting player types (Human/AI) and AI strategies
before starting a game.
"""

import pygame
from pygame.locals import *


# Player type constants
PLAYER_TYPE_HUMAN = "Human"
PLAYER_TYPE_AI = "AI"

# AI strategy names (matching ai_player.py)
AI_STRATEGIES = ["Random", "Aggressive", "Defensive"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
P1COLOR = (255, 0, 0)      # Red
P2COLOR = (0, 0, 128)      # Navy
P3COLOR = (255, 255, 0)    # Yellow
P4COLOR = (128, 0, 128)    # Purple

PLAYER_COLORS = {
    1: P1COLOR,
    2: P2COLOR,
    3: P3COLOR,
    4: P4COLOR
}


class PlayerConfig:
    """Configuration for a single player."""
    
    def __init__(self, player_number: int):
        """
        Initialize player configuration.
        
        Args:
            player_number: Player number (1-4)
        """
        self.player_number = player_number
        self.player_type = PLAYER_TYPE_HUMAN
        self.ai_strategy = AI_STRATEGIES[0]  # Default to Random
    
    def is_human(self) -> bool:
        """Check if this player is human-controlled."""
        return self.player_type == PLAYER_TYPE_HUMAN
    
    def is_ai(self) -> bool:
        """Check if this player is AI-controlled."""
        return self.player_type == PLAYER_TYPE_AI
    
    def toggle_type(self):
        """Toggle between Human and AI."""
        if self.player_type == PLAYER_TYPE_HUMAN:
            self.player_type = PLAYER_TYPE_AI
        else:
            self.player_type = PLAYER_TYPE_HUMAN
    
    def cycle_strategy(self):
        """Cycle to next AI strategy."""
        current_idx = AI_STRATEGIES.index(self.ai_strategy)
        next_idx = (current_idx + 1) % len(AI_STRATEGIES)
        self.ai_strategy = AI_STRATEGIES[next_idx]


class PlayerSelectionScreen:
    """
    Interactive screen for selecting player types and AI strategies.
    """
    
    def __init__(self, screen_width: int = 600, screen_height: int = 500):
        """
        Initialize player selection screen.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_configs = [PlayerConfig(i) for i in range(1, 5)]
        self.font_large = None
        self.font_medium = None
        self.font_small = None
    
    def initialize_fonts(self):
        """Initialize pygame fonts (must be called after pygame.init())."""
        self.font_large = pygame.font.Font('freesansbold.ttf', 32)
        self.font_medium = pygame.font.Font('freesansbold.ttf', 20)
        self.font_small = pygame.font.Font('freesansbold.ttf', 16)
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the player selection screen.
        
        Args:
            surface: pygame Surface to draw on
        """
        # Clear background
        surface.fill(WHITE)
        
        # Draw title
        title_text = self.font_large.render("Select Players", True, BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 40))
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_small.render("Click player type to toggle Human/AI", True, DARK_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 75))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw player configuration sections (4 rows)
        y_start = 120
        row_height = 70
        
        for i, config in enumerate(self.player_configs):
            y_pos = y_start + (i * row_height)
            self._draw_player_row(surface, config, y_pos)
        
        # Draw Start Game button
        start_button_rect = self._get_start_button_rect()
        self._draw_button(surface, "Start Game", start_button_rect, GREEN)
        
        # Draw Watch AI vs AI button
        watch_button_rect = self._get_watch_button_rect()
        self._draw_button(surface, "Watch AI vs AI", watch_button_rect, BLUE)
    
    def _draw_player_row(self, surface: pygame.Surface, config: PlayerConfig, y_pos: int):
        """Draw a single player configuration row."""
        x_margin = 50
        
        # Player number label with color
        player_color = PLAYER_COLORS[config.player_number]
        player_label = self.font_medium.render(f"Player {config.player_number}:", True, player_color)
        surface.blit(player_label, (x_margin, y_pos))
        
        # Player type button (Human/AI toggle)
        type_button_rect = pygame.Rect(x_margin + 120, y_pos - 5, 100, 35)
        type_color = LIGHT_GRAY if config.is_human() else BLUE
        self._draw_button(surface, config.player_type, type_button_rect, type_color)
        
        # AI Strategy button (only visible if AI)
        if config.is_ai():
            strategy_button_rect = pygame.Rect(x_margin + 240, y_pos - 5, 140, 35)
            self._draw_button(surface, config.ai_strategy, strategy_button_rect, LIGHT_GRAY)
    
    def _draw_button(self, surface: pygame.Surface, text: str, rect: pygame.Rect, color: tuple):
        """Draw a button with text."""
        # Draw button background
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)  # Border
        
        # Draw button text
        text_surf = self.font_small.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
    
    def _get_start_button_rect(self) -> pygame.Rect:
        """Get rectangle for Start Game button."""
        width = 200
        height = 50
        x = (self.screen_width // 2) - (width // 2)
        y = self.screen_height - 100
        return pygame.Rect(x, y, width, height)
    
    def _get_watch_button_rect(self) -> pygame.Rect:
        """Get rectangle for Watch AI vs AI button."""
        width = 200
        height = 40
        x = (self.screen_width // 2) - (width // 2)
        y = self.screen_height - 45
        return pygame.Rect(x, y, width, height)
    
    def _get_type_button_rect(self, player_number: int) -> pygame.Rect:
        """Get rectangle for player type button."""
        x_margin = 50
        y_start = 120
        row_height = 70
        y_pos = y_start + ((player_number - 1) * row_height)
        return pygame.Rect(x_margin + 120, y_pos - 5, 100, 35)
    
    def _get_strategy_button_rect(self, player_number: int) -> pygame.Rect:
        """Get rectangle for AI strategy button."""
        x_margin = 50
        y_start = 120
        row_height = 70
        y_pos = y_start + ((player_number - 1) * row_height)
        return pygame.Rect(x_margin + 240, y_pos - 5, 140, 35)
    
    def handle_click(self, pos: tuple) -> str:
        """
        Handle mouse click event.
        
        Args:
            pos: (x, y) position of click
            
        Returns:
            Action string: 'start', 'watch', 'type_N', 'strategy_N', or None
        """
        # Check Start button
        if self._get_start_button_rect().collidepoint(pos):
            return 'start'
        
        # Check Watch AI vs AI button
        if self._get_watch_button_rect().collidepoint(pos):
            return 'watch'
        
        # Check player type buttons
        for i in range(1, 5):
            if self._get_type_button_rect(i).collidepoint(pos):
                return f'type_{i}'
        
        # Check AI strategy buttons
        for i in range(1, 5):
            if self.player_configs[i-1].is_ai():
                if self._get_strategy_button_rect(i).collidepoint(pos):
                    return f'strategy_{i}'
        
        return None
    
    def process_action(self, action: str):
        """
        Process an action from handle_click.
        
        Args:
            action: Action string from handle_click
        """
        if action is None:
            return
        
        if action.startswith('type_'):
            player_num = int(action.split('_')[1])
            self.player_configs[player_num - 1].toggle_type()
        
        elif action.startswith('strategy_'):
            player_num = int(action.split('_')[1])
            self.player_configs[player_num - 1].cycle_strategy()
    
    def get_player_configs(self) -> list:
        """Get list of player configurations."""
        return self.player_configs
    
    def set_all_ai(self):
        """Set all players to AI for watch mode."""
        for config in self.player_configs:
            config.player_type = PLAYER_TYPE_AI


def run_player_selection() -> list:
    """
    Run the player selection screen and return player configurations.
    
    Returns:
        List of PlayerConfig objects (one for each player)
        Returns None if user cancels
    """
    pygame.init()
    
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('Aggravation - Player Selection')
    
    selection_screen = PlayerSelectionScreen()
    selection_screen.initialize_fonts()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return None
            
            if event.type == MOUSEBUTTONDOWN:
                action = selection_screen.handle_click(event.pos)
                
                if action == 'start':
                    return selection_screen.get_player_configs()
                
                elif action == 'watch':
                    # Set all to AI and return
                    selection_screen.set_all_ai()
                    return selection_screen.get_player_configs()
                
                else:
                    selection_screen.process_action(action)
        
        # Draw screen
        selection_screen.draw(screen)
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    # Test the player selection screen
    configs = run_player_selection()
    
    if configs:
        print("\nPlayer Configuration:")
        print("=" * 50)
        for config in configs:
            if config.is_human():
                print(f"Player {config.player_number}: Human")
            else:
                print(f"Player {config.player_number}: AI ({config.ai_strategy})")
    else:
        print("Player selection cancelled")

"""
Animations for Aggravation Terminal Game
Provides GitHub CLI-style animations for dice rolls, marble movement, and victory.
"""

import time
import random
from typing import Optional
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich import box


# Dice face Unicode characters (0-indexed: DICE_FACES[0] = die showing 1, DICE_FACES[5] = die showing 6)
DICE_FACES = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']

# Color gradient for title animation
TITLE_COLORS = ["red", "yellow", "green", "cyan", "blue", "magenta"]


class Animator:
    """Handles all animations for the terminal game."""
    
    def __init__(self, console: Console, no_animation: bool = False):
        """
        Initialize the animator.
        
        Args:
            console: Rich Console instance
            no_animation: If True, skip animations for slow connections
        """
        self.console = console
        self.no_animation = no_animation
    
    def animated_title(self):
        """Display animated startup title with gradient colors (GitHub CLI style)."""
        if self.no_animation:
            self.console.print(Panel("🎲 [bold magenta]AGGRAVATION[/] 🎲", 
                                    box=box.DOUBLE,
                                    expand=False))
            return
        
        title_text = "🎲 AGGRAVATION 🎲"
        
        with Live(refresh_per_second=10, console=self.console) as live:
            for i in range(30):
                color = TITLE_COLORS[i % len(TITLE_COLORS)]
                text = Text(title_text, style=f"bold {color}")
                panel = Panel(text, box=box.DOUBLE, expand=False)
                live.update(panel)
                time.sleep(0.05)
        
        # Final static display
        self.console.print(Panel("🎲 [bold magenta]AGGRAVATION[/] 🎲", 
                                box=box.DOUBLE,
                                expand=False))
    
    def dice_roll_animation(self, final_roll: int):
        """
        Animate dice rolling with spinning faces before revealing result.
        
        Args:
            final_roll: The final dice value (1-6)
        """
        if self.no_animation:
            self.console.print(f"  [bold green]{DICE_FACES[final_roll-1]}[/] You rolled: [bold]{final_roll}[/]")
            return
        
        # Spinning animation
        spin_count = 15
        for _ in range(spin_count):
            dice_face = random.choice(DICE_FACES)
            self.console.print(f"  [bold yellow]{dice_face}[/] Rolling...", end='\r')
            time.sleep(0.08)
        
        # Clear the line and show final result
        self.console.print(" " * 50, end='\r')
        self.console.print(f"  [bold green]{DICE_FACES[final_roll-1]}[/] You rolled: [bold cyan]{final_roll}[/]")
    
    def marble_movement_animation(self, marble_symbol: str, from_pos: Optional[tuple], to_pos: tuple, player_color: str):
        """
        Show marble "sliding" animation.
        
        Args:
            marble_symbol: Emoji symbol for the marble (e.g., 🔴)
            from_pos: Starting position (x, y) or None if from home
            to_pos: Ending position (x, y)
            player_color: Color name for the player
        """
        if self.no_animation:
            if from_pos:
                self.console.print(f"  {marble_symbol} Moving from {from_pos} → {to_pos}")
            else:
                self.console.print(f"  {marble_symbol} Entering board at {to_pos}")
            return
        
        # Animated dots showing movement
        if from_pos:
            msg = f"  {marble_symbol} Moving from [{player_color}]{from_pos}[/{player_color}]"
        else:
            msg = f"  {marble_symbol} Entering board"
        
        for i in range(4):
            dots = "." * (i + 1)
            self.console.print(f"{msg}{dots}", end='\r')
            time.sleep(0.15)
        
        self.console.print(" " * 60, end='\r')
        self.console.print(f"  {marble_symbol} Now at [{player_color}]{to_pos}[/{player_color}]")
    
    def aggravation_animation(self, aggressor_symbol: str, victim_symbol: str):
        """
        Flash/shake effect when sending opponent home (aggravation).
        
        Args:
            aggressor_symbol: Marble symbol of attacking player
            victim_symbol: Marble symbol of victim player
        """
        if self.no_animation:
            self.console.print(f"  [bold red]AGGRAVATION![/] {aggressor_symbol} sent {victim_symbol} home!")
            return
        
        # Flashing effect
        for i in range(3):
            if i % 2 == 0:
                self.console.print(f"  [bold red on white]💥 AGGRAVATION! 💥[/]", end='\r')
            else:
                self.console.print(f"  [bold yellow]💥 AGGRAVATION! 💥[/]", end='\r')
            time.sleep(0.2)
        
        self.console.print(" " * 50, end='\r')
        self.console.print(f"  [bold red]AGGRAVATION![/] {aggressor_symbol} sent {victim_symbol} home!")
    
    def victory_animation(self, player_num: int, player_name: str, player_symbol: str):
        """
        Celebratory confetti-style effect for victory.
        
        Args:
            player_num: Winning player number
            player_name: Name of winning player
            player_symbol: Marble symbol of winner
        """
        if self.no_animation:
            self.console.print(Panel(
                f"[bold green]🎉 {player_symbol} {player_name} WINS! 🎉[/]",
                box=box.DOUBLE,
                expand=False
            ))
            return
        
        # Confetti animation
        confetti = ['🎊', '🎉', '✨', '🌟', '⭐', '💫']
        
        with Live(refresh_per_second=10, console=self.console) as live:
            for i in range(20):
                # Random confetti
                left_conf = random.choice(confetti)
                right_conf = random.choice(confetti)
                
                text = Text()
                text.append(f"{left_conf} ", style="bold yellow")
                text.append(f"{player_symbol} {player_name} WINS!", style="bold green")
                text.append(f" {right_conf}", style="bold yellow")
                
                panel = Panel(text, box=box.DOUBLE, expand=False)
                live.update(panel)
                time.sleep(0.1)
        
        # Final display
        self.console.print(Panel(
            f"[bold green]🎉 {player_symbol} {player_name} WINS! 🎉[/]",
            box=box.DOUBLE,
            expand=False
        ))
    
    def turn_indicator(self, player_num: int, player_name: str, player_symbol: str):
        """
        Display whose turn it is.
        
        Args:
            player_num: Current player number
            player_name: Player name
            player_symbol: Player's marble symbol
        """
        self.console.print(f"\n[bold yellow]═══ {player_symbol} {player_name}'s Turn ═══[/]\n")
    
    def waiting_for_input(self):
        """Show a subtle waiting animation."""
        if not self.no_animation:
            self.console.print("[dim]...[/]", end='\r')

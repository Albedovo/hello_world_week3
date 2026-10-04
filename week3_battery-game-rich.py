# Terminal styling follows the class deep-deep-forest-rich example.
# Install Rich: python3 -m pip install rich
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

console = Console()


def show_status(battery, distance):
    console.rule("[bold cyan]Your journey home[/]")
    console.print(f"Battery: [bold yellow]{battery}%[/] | Distance home: [bold cyan]{distance} blocks[/]")
    # RICH: a built-in bar shows the remaining starting battery reserve.
    progress = Progress(
        TextColumn("Battery reserve"),
        BarColumn(bar_width=25, complete_style="yellow", finished_style="yellow"),
        TextColumn("{task.completed}/10"),
        console=console,
    )
    progress.add_task("Battery", total=10, completed=battery)
    console.print(progress)


def show_choices():
    # RICH: Table handles the borders, spacing, and colors.
    table = Table(title="Choose your next move")
    table.add_column("Key", style="bold cyan")
    table.add_column("Action")
    table.add_column("Cost", style="yellow")
    table.add_column("Success")
    table.add_row("1", "Use GPS", "4%", "Always")
    table.add_row("2", "Call for directions", "3%", "Roll 1-8 (80%)")
    table.add_row("3", "Ask a stranger", "2%", "Roll 1-5 (50%)")
    table.add_row("4", "Walk randomly", "1%", "Roll 1-3 (30%)")
    console.print(table)


def roll_dice(target):
    # RICH: the same built-in spinner used in the class example.
    with console.status("[bold yellow]Rolling the dice...[/]", spinner="bouncingBall"):
        time.sleep(1.2)
    roll = random.randint(1, 10)
    success = roll <= target
    color = "green" if success else "red"
    console.print(Panel(
        f"You rolled [bold {color}]{roll}[/] out of 10.\n"
        f"Success requires [bold]{target} or less[/].",
        title="Dice result", border_style=color, expand=False,
    ))
    return success


def play_game():
    battery = 10
    distance = 3
    console.print(Panel(
        "[bold yellow]10% BATTERY: FIND YOUR WAY HOME[/]\n\n"
        "You are 3 blocks from home with only 10% battery.\n"
        "Choose how to find your way before your phone dies.\n"
        "[dim]Reaching home with exactly 0% battery still counts as a win.[/]",
        title="The story so far...", border_style="cyan",
    ))

    while battery > 0 and distance > 0:
        show_status(battery, distance)
        show_choices()
        # RICH: Prompt automatically asks again for invalid choices.
        choice = Prompt.ask("[bold]What do you do?[/]", choices=["1", "2", "3", "4"])
        if choice == "1":
            cost = 4
        elif choice == "2":
            cost = 3
        elif choice == "3":
            cost = 2
        else:
            cost = 1

        if battery < cost:
            console.print("[bold red]Not enough battery.[/] Choose a cheaper action.")
            continue

        battery -= cost
        console.print(f"[yellow]Battery used: {cost}%[/]")
        if choice == "1":
            with console.status("[cyan]Finding your route...[/]", spinner="dots"):
                time.sleep(0.8)
            distance -= 1
            console.print("[green]GPS shows the way. Move 1 block closer! No roll needed.[/]")
        elif choice == "2":
            if roll_dice(8):
                distance -= 1
                console.print("[green]Correct directions! Move 1 block closer.[/]")
            else:
                distance += 1
                console.print("[red]Wrong directions! Move 1 block farther away.[/]")
        elif choice == "3":
            if roll_dice(5):
                distance -= 1
                console.print("[green]Someone helps you! Move 1 block closer.[/]")
            else:
                console.print("[yellow]Nobody knows the way. Stay in place.[/]")
        else:
            if roll_dice(3):
                distance -= 1
                console.print("[green]Lucky choice! Move 1 block closer.[/]")
            else:
                distance += 1
                console.print("[red]Wrong turn! Move 1 block farther away.[/]")

    # Check arrival before battery so an exact-zero arrival wins.
    if distance == 0:
        console.print(Panel("[bold green]You made it home! YOU WIN![/]", border_style="green"))
    else:
        console.print(Panel("[bold red]Battery dead. GAME OVER![/]", border_style="red"))

    table = Table(title="Final result")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="bold")
    table.add_row("Battery", f"{battery}%")
    table.add_row("Distance home", f"{distance} blocks")
    console.print(table)


if __name__ == "__main__":
    play_game()

import os
import ctypes
import subprocess

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


def clear_screen():
    os.system("cls")


def pause():
    input("\nPress ENTER to continue...")


def execute(command):
    """Executes a Windows command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True
        )

        return result.returncode == 0

    except Exception as error:
        print(f"[red]✘ Error: {error}[/red]")
        return False


def is_admin():
    """Checks if the program is running as administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def header():
    clear_screen()

    console.print(
        Panel(
            "[bold cyan]WINDOWS CLEANER[/bold cyan]\n"
            "[dim]Cleaning and maintenance tool[/dim]",
            border_style="cyan",
            expand=False
        )
    )


def clean_temp_files():

    header()

    console.print(
        Panel(
            "[bold white]TEMPORARY FILE CLEANUP[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Cleaning user temporary files...[/yellow]")

    execute(
        r'del /q /f /s "%TEMP%\*"'
    )

    print("[green]✔ User temporary files processed.[/green]")

    print("\n[yellow]→ Cleaning Windows temporary files...[/yellow]")

    execute(
        r'del /q /f /s "%WINDIR%\Temp\*"'
    )

    print("[green]✔ Windows temporary files processed.[/green]")

    pause()


def clear_dns_cache():

    header()

    console.print(
        Panel(
            "[bold white]DNS CACHE CLEANUP[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Clearing DNS cache...[/yellow]")

    if execute("ipconfig /flushdns"):
        print("[green]✔ DNS cache cleared successfully.[/green]")
    else:
        print("[red]✘ Failed to clear DNS cache.[/red]")

    pause()


def clean_windows_update():

    header()

    console.print(
        Panel(
            "[bold white]WINDOWS UPDATE CLEANUP[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Stopping Windows Update...[/yellow]")
    execute("net stop wuauserv")

    print("[yellow]→ Stopping BITS...[/yellow]")
    execute("net stop bits")

    print("[yellow]→ Cleaning downloaded files...[/yellow]")

    execute(
        r'del /q /f /s "%WINDIR%\SoftwareDistribution\Download\*"'
    )

    print("[yellow]→ Starting BITS...[/yellow]")
    execute("net start bits")

    print("[yellow]→ Starting Windows Update...[/yellow]")
    execute("net start wuauserv")

    print("\n[green]✔ Windows Update cleanup completed.[/green]")

    pause()


def clean_windows_components():

    header()

    console.print(
        Panel(
            "[bold white]WINDOWS COMPONENT CLEANUP[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Running DISM...[/yellow]")
    print("[dim]This may take a few minutes.[/dim]\n")

    if execute(
        "DISM /Online /Cleanup-Image /StartComponentCleanup"
    ):
        print("\n[green]✔ Old components processed.[/green]")
    else:
        print("\n[red]✘ DISM encountered a problem.[/red]")

    pause()


def check_system():

    header()

    console.print(
        Panel(
            "[bold white]SYSTEM CHECK[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Running SFC...[/yellow]")
    print("[dim]Checking protected Windows system files.[/dim]\n")

    execute("sfc /scannow")

    print("\n[yellow]→ Running DISM...[/yellow]")
    print("[dim]Checking the Windows image.[/dim]\n")

    execute(
        "DISM /Online /Cleanup-Image /RestoreHealth"
    )

    print("\n[green]✔ System check completed.[/green]")

    pause()


def disk_cleanup():

    header()

    console.print(
        Panel(
            "[bold white]DISK CLEANUP[/bold white]",
            border_style="blue"
        )
    )

    print("\n[yellow]→ Opening Windows Disk Cleanup...[/yellow]")

    execute("cleanmgr")

    pause()


def full_cleanup():

    header()

    console.print(
        Panel(
            "[bold yellow]FULL CLEANUP[/bold yellow]\n\n"
            "This option will run all available "
            "cleanup operations.",
            border_style="yellow"
        )
    )

    confirm = input("\nDo you want to continue? [Y/N]: ").strip().lower()

    if confirm != "y":
        print("\n[yellow]Operation cancelled.[/yellow]")
        pause()
        return

    print("\n[bold cyan]━━━ 1/4 • TEMPORARY FILES ━━━[/bold cyan]")

    execute(r'del /q /f /s "%TEMP%\*"')
    execute(r'del /q /f /s "%WINDIR%\Temp\*"')

    print("[green]✔ Temporary files cleanup completed.[/green]")

    print("\n[bold cyan]━━━ 2/4 • DNS CACHE ━━━[/bold cyan]")

    execute("ipconfig /flushdns")

    print("[green]✔ DNS cache cleanup completed.[/green]")

    print("\n[bold cyan]━━━ 3/4 • WINDOWS UPDATE ━━━[/bold cyan]")

    execute("net stop wuauserv")
    execute("net stop bits")

    execute(
        r'del /q /f /s "%WINDIR%\SoftwareDistribution\Download\*"'
    )

    execute("net start bits")
    execute("net start wuauserv")

    print("[green]✔ Windows Update cleanup completed.[/green]")

    print("\n[bold cyan]━━━ 4/4 • WINDOWS COMPONENTS ━━━[/bold cyan]")

    execute(
        "DISM /Online /Cleanup-Image /StartComponentCleanup"
    )

    print("[green]✔ Windows components cleanup completed.[/green]")

    console.print(
        Panel(
            "[bold green]✔ FULL CLEANUP COMPLETED[/bold green]",
            border_style="green"
        )
    )

    pause()


def menu():

    while True:

        header()

        table = Table(
            title="MAIN MENU",
            border_style="cyan",
            header_style="bold cyan"
        )

        table.add_column("Option", justify="center", style="bold")
        table.add_column("Function", style="white")

        table.add_row("1", "Full Cleanup")
        table.add_row("2", "Clear DNS Cache")
        table.add_row("3", "Temporary Files")
        table.add_row("4", "Windows Update")
        table.add_row("5", "Check / Repair Windows")
        table.add_row("6", "Disk Cleanup")
        table.add_row("0", "Exit")

        console.print(table)

        option = input("\nChoose an option: ").strip()

        if option == "1":
            full_cleanup()

        elif option == "2":
            clear_dns_cache()

        elif option == "3":
            clean_temp_files()

        elif option == "4":
            clean_windows_update()

        elif option == "5":
            check_system()

        elif option == "6":
            disk_cleanup()

        elif option == "0":
            clear_screen()

            console.print(
                Panel(
                    "[bold cyan]Thank you for using Windows Cleaner![/bold cyan]",
                    border_style="cyan"
                )
            )

            break

        else:
            print("\n[red]✘ Invalid option.[/red]")
            pause()


if __name__ == "__main__":

    if not is_admin():

        clear_screen()

        console.print(
            Panel(
                "[bold yellow]⚠ RUN AS ADMINISTRATOR[/bold yellow]\n\n"
                "Some Windows Cleaner functions require "
                "administrative privileges.",
                border_style="yellow"
            )
        )

        pause()

    else:
        menu()
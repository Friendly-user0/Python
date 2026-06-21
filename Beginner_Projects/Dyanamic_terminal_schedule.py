import datetime
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.console import Group

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
    import select

console = Console()
old_term_settings = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def dramatic_print(text_style_string, delay=0.015):
    """Types out text character by character with rich formatting parsing intact."""
    with console.capture() as capture:
        console.print(text_style_string, end="")
    rendered_output = capture.get()

    for char in rendered_output:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

def get_ordinal_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def is_time_in_range(start_hour, start_min, end_hour, end_min):
    now = datetime.datetime.now().time()
    start = datetime.time(start_hour, start_min)

    if end_hour == 0 and end_min == 0:
        end = datetime.time(23, 59, 59)
    else:
        end = datetime.time(end_hour, end_min)

    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end

def init_terminal_mode():
    """Engages single-character input interception mode."""
    global old_term_settings
    if os.name != 'nt':
        try:
            fd = sys.stdin.fileno()
            old_term_settings = termios.tcgetattr(fd)
            tty.setcbreak(fd)
        except Exception:
            pass

def restore_terminal_mode():
    """Restores terminal back to classic line-buffered execution."""
    global old_term_settings
    if os.name != 'nt' and old_term_settings is not None:
        try:
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSADRAIN, old_term_settings)
        except Exception:
            pass

def check_live_key():
    """Captures and normalizes key presses instantly using low-level unbuffered I/O."""
    if os.name == 'nt':
        if msvcrt.kbhit():
            try:
                ch = msvcrt.getch()
                if ch in (b'\r', b'\n'):
                    return "ENTER"
                if ch == b'\x08':
                    return "BACKSPACE"
                return ch.decode('utf-8', errors='ignore')
            except Exception:
                return None
    else:
        try:
            if select.select([sys.stdin], [], [], 0)[0]:
                fd = sys.stdin.fileno()
                ch = os.read(fd, 1).decode('utf-8', errors='ignore')
                if ch in ('\n', '\r'):
                    return "ENTER"
                if ch in ('\x7f', '\x08'):
                    return "BACKSPACE"
                return ch
        except Exception:
            return None
    return None

def format_viewport_tasks(task_list, max_display=5):
    """Filters and slices tasks to prevent terminal height overflow while tracking everything."""
    if not task_list:
        return ""
    if len(task_list) <= max_display:
        return "• " + "\n• ".join(task_list)

    hidden_count = len(task_list) - max_display
    visible_slice = task_list[-max_display:]
    return f"[bold dim yellow]• [... {hidden_count} older tasks scrolled up][/bold dim yellow]\n• " + "\n• ".join(visible_slice)

def generate_dashboard(frame_counter, current_input_text, dynamic_tasks):
    pulse_color = "red" if frame_counter % 2 == 0 else "blue"
    alt_pulse = "gold3" if frame_counter % 2 == 0 else "light_salmon3"

    header_text = Text()
    header_text.append(f"“Your faith will be answered.”\n\n", style=f"bold {alt_pulse} justify=center")
    header_text.append("God says: ", style="bold gold3")
    header_text.append("You are never facing your battles alone, because my hand is holding yours. ", style="italic white")
    header_text.append("Do not be afraid, ", style="bold light_salmon3")
    header_text.append("for I will help you every step of the way.", style="italic white")

    header_panel = Panel(
        header_text,
        title=f"[{pulse_color}] RUNNING ENGINE [/{pulse_color}]",
        border_style="dark_blue",
        padding=(1, 2)
    )

    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day_num = now.day
    suffix = get_ordinal_suffix(day_num)
    year = now.year

    date_panel = Panel(
        Text(f"{day_name} — {month_name} {day_num}{suffix}, {year}", style="bold deep_sky_blue1 justify=center"),
        border_style="red"
    )

    input_panel = Panel(
        Text(f"> {current_input_text}█", style="bold white"),
        title="[bold gold3]⌨ LIVE TASK ENGINE (Type freely & press Enter to log into the active block)[/bold gold3]",
        border_style="gold3"
    )

    table = Table(title="ACHIEVE", title_style=f"bold {pulse_color}", show_header=True, header_style="bold dark_blue", expand=True)
    table.add_column("Timeline", width=38, no_wrap=True)
    table.add_column("Tasks...", style="white")

    b1 = " [bold green][ACTIVE][/bold green]" if is_time_in_range(8, 0, 10, 30) else ""
    b2 = " [bold green][ACTIVE][/bold green]" if is_time_in_range(13, 0, 17, 0) else ""
    b3 = " [bold green][ACTIVE][/bold green]" if is_time_in_range(17, 0, 18, 30) else ""
    b4 = " [bold green][ACTIVE][/bold green]" if is_time_in_range(18, 30, 20, 0) else ""
    b5 = " [bold green][ACTIVE][/bold green]" if is_time_in_range(20, 0, 0, 0) else ""

    t1_text = format_viewport_tasks(dynamic_tasks["b1"])
    t2_text = format_viewport_tasks(dynamic_tasks["b2"])
    t3_text = format_viewport_tasks(dynamic_tasks["b3"])
    t4_text = format_viewport_tasks(dynamic_tasks["b4"])
    t5_text = format_viewport_tasks(dynamic_tasks["b5"])

    table.add_row(f"[ 08:00 AM : 10:30 AM ]{b1}", t1_text, style="bold dark_red" if b1 else "white")
    table.add_row(f"[ 01:00 PM : 05:00 PM ]{b2}", t2_text, style="bold dark_red" if b2 else "white")
    table.add_row(f"[ 05:00 PM : 06:30 PM ]{b3}", t3_text, style="bold dark_red" if b3 else "white")
    table.add_row(f"[ 06:30 PM : 08:00 PM ]{b4}", t4_text, style="bold dark_red" if b4 else "white")
    table.add_row(f"[ 08:00 PM : 12:00 AM ]{b5}", t5_text, style="bold dark_red" if b5 else "white")

    layout_group = Group(header_panel, date_panel, input_panel, table)
    return Panel(layout_group, border_style="dark_blue")

def execute_audit():
    clear_screen()
    now = datetime.datetime.now()

    console.print(Panel(Text("The Lord is my light and my salvation; whom shall I fear?", style="bold red justify=center"), border_style="red"))
    time.sleep(0.9)

    console.print("\n[bold yellow]1. Did you deliver what you promised today?[/bold yellow]")
    console.print("[bold cyan][ SPEAK ]: [/bold cyan]", end="")
    ans1 = sys.stdin.readline().strip().lower()
    q1_success = ans1.startswith('y') or ans1.startswith('c')
    q1_detail = ""

    time.sleep(0.3)
    if q1_success:
        dramatic_print("[bold green]Yes, I achieved it.[/bold green]")
        time.sleep(0.2)
        console.print("[bold green]❯ State your achievement: [/bold green]", end="")
        q1_detail = sys.stdin.readline().strip()
    else:
        dramatic_print("[bold red]No, I'm worthless today.[/bold red]")
        time.sleep(1.2)

    time.sleep(0.9)
    console.print("\n[bold yellow]2. Did your actual execution look like that of a top 0.016%, or did you play small hiding behind an excuse?[/bold yellow]")
    console.print("[bold cyan][ ANSWER ]: [/bold cyan]", end="")
    ans2 = sys.stdin.readline().strip().lower()
    q2_success = ans2.startswith('y') or ans2.startswith('c')

    time.sleep(0.3)
    if q2_success:
        dramatic_print("[bold green]Yes, my performance was divine.[/bold green]")
    else:
        dramatic_print("[bold red]No, I chose being pathetic.[/bold red]")
        time.sleep(1.2)

    time.sleep(0.4)
    if not q1_success and not q2_success:
        clear_screen()
        dramatic_print("[bold white on red]🚨 SYSTEM CRUMBLING... 🚨[/bold white on red]\n")
        dramatic_print("[bold red]You failed on your promises and expect to achieve power far beyond your limits? You have no rights to even dream about it. Go beyond it or accept defeat.[/bold red]", delay=0.02)
        status_tier = "pathetic"
        q3_entries = ["Total operational default."]
    else:
        status_tier = "ascended" if (q1_success and q2_success) else "average"

        console.print("\n[bold yellow]3. What have you achieved?[/bold yellow]")
        console.print(Panel("[bold green]SYSTEM INSTRUCTIONS:[/bold green]\n1. Press Enter for new lines. \n2. Type achievements step-by-step.\n[ Give me your word ]: '[red]I will reach heights, unseen beyond your comparison[/red]'", border_style="gold3"))

        q3_entries = []
        counter = 1
        while True:
            console.print(f"[bold cyan]  {counter}. [/bold cyan]", end="")
            line = sys.stdin.readline().strip()
            if line.strip() == "I will reach heights, unseen beyond your comparison":
                break
            if line == "":
                continue
            q3_entries.append(line)
            counter += 1

        time.sleep(0.3)
        dramatic_print(f"\n[bold red] What makes you think you deserve what's waiting beyond that achievement?[/bold red]\n", delay=0.02)

    time.sleep(0.2)
    console.print("[bold yellow]❯ Enter a summary of your day in few words: [/bold yellow]", end="")
    log_modifier = sys.stdin.readline().strip().replace(" ", "_")

    base_dir = "Operational_Logs"
    tier_dir = os.path.join(base_dir, status_tier)
    os.makedirs(tier_dir, exist_ok=True)

    log_filename = f"{now.strftime('%Y_%m_%d')}_{log_modifier}.txt"
    full_path = os.path.join(tier_dir, log_filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"TIMESTAMP: {now.strftime('%Y-%m-%d %H:%M:%S')} | TIER: {status_tier.upper()}\n")
        f.write("="*60 + "\n")
        f.write(f"Q1: {q1_detail if q1_success else 'FAILED'}\n")
        f.write("Achievements:\n")
        for entry in q3_entries:
            f.write(f"- {entry}\n")

    time.sleep(0.4)
    dramatic_print(f"\n[bold green]Saved: {full_path}[/bold green]")
    time.sleep(0.5)
    dramatic_print("\n[bold red] You do not have the privilege to rest. There is no Mercy neither will there ever be. GET BACK UP.[/bold red]\n", delay=0.025)
    time.sleep(3)

if __name__ == "__main__":
    frame = 0
    current_input_text = ""
    dynamic_tasks = {"b1": [], "b2": [], "b3": [], "b4": [], "b5": []}

    clear_screen()
    init_terminal_mode()
    last_refresh = time.time()

    try:
        with Live(generate_dashboard(frame, current_input_text, dynamic_tasks), screen=False, auto_refresh=False) as live:
            while True:
                time.sleep(0.015)
                key = check_live_key()
                mutated = False

                if key:
                    mutated = True
                    if key == "ENTER":
                        if current_input_text.strip():
                            active_slot = None
                            if is_time_in_range(8, 0, 10, 30): active_slot = "b1"
                            elif is_time_in_range(13, 0, 17, 0): active_slot = "b2"
                            elif is_time_in_range(17, 0, 18, 30): active_slot = "b3"
                            elif is_time_in_range(18, 30, 20, 0): active_slot = "b4"
                            elif is_time_in_range(20, 0, 0, 0): active_slot = "b5"

                            if active_slot:
                                dynamic_tasks[active_slot].append(current_input_text.strip())
                                try:
                                    now = datetime.datetime.now()
                                    base_dir = "Operational_Logs"
                                    os.makedirs(base_dir, exist_ok=True)
                                    backup_file = os.path.join(base_dir, f"{now.strftime('%Y_%m_%d')}_live_append.txt")
                                    with open(backup_file, "a", encoding="utf-8") as f:
                                        f.write(f"[{now.strftime('%H:%M:%S')}][{active_slot.upper()}] {current_input_text.strip()}\n")
                                except Exception:
                                    pass
                            current_input_text = ""
                    elif key == "BACKSPACE":
                        current_input_text = current_input_text[:-1]
                    else:
                        if len(key) == 1 and key.isprintable():
                            current_input_text += key

                if mutated or (time.time() - last_refresh >= 0.5):
                    if not mutated:
                        frame += 1
                    live.update(generate_dashboard(frame, current_input_text, dynamic_tasks), refresh=True)
                    last_refresh = time.time()

    except KeyboardInterrupt:
        restore_terminal_mode()
        execute_audit()
    finally:
        restore_terminal_mode()

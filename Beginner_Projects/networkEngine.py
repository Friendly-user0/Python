import os
import sys
import time
import socket
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.console import Group

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_latency(host="8.8.8.8", port=53, timeout=2):
    """Measures connection responsiveness via ultra-lightweight TCP handshakes."""
    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return (time.time() - start_time) * 1000  # Convert to milliseconds
    except (socket.timeout, socket.error):
        return None

def generate_panel(history, current_latency):
    now = datetime.datetime.now().strftime("%X")

    if current_latency is None:
        status_text = "DISCONNECTED (No Route / Offline)"
        status_color = "magenta"
    elif current_latency < 30:
        status_text = f"EXCELLENT ({current_latency:.1f} ms) — Peak Bandwidth Available"
        status_color = "gold3"
    elif current_latency < 150:
        status_text = f"STABLE / GOOD ({current_latency:.1f} ms) — Reliable Throughput"
        status_color = "deep_sky_blue1"
    else:
        status_text = f"SEVERE LAG / SLOW ({current_latency:.1f} ms) — Network Congested"
        status_color = "red"

    info_text = Text()
    info_text.append(f" ⏱ Last Checked: ", style="bold white")
    info_text.append(f"{now}\n", style="dim white")
    info_text.append(f" 📡 Connection State: ", style="bold white")
    info_text.append(f"{status_text}\n", style=f"bold {status_color}")

    graph_text = Text("\n Activity Timeline (Recent ➔):\n [ ")

    for i, lat in enumerate(history):
        if lat is None:
            graph_text.append("-", style="bold magenta")  # SLEEP
        elif lat < 30:
            graph_text.append("█", style="gold3")         # Excellent
        elif lat < 150:
            graph_text.append("▇", style="deep_sky_blue1")  # Stable
        else:
            graph_text.append("▃", style="red")           # BAD

        # Add a light spacer after every symbol except the very last one
        if i < len(history) - 1:
            graph_text.append(" ")

    graph_text.append(" ]")

    # Legend Layout
    legend = Text("\n\n Legend: ", style="bold dim white")
    legend.append("█ Gold (Optimal)   ", style="gold3")
    legend.append("▇ Blue (Stable)   ", style="deep_sky_blue1")
    legend.append("▃ Red (Choked/Slow)   ", style="red")
    legend.append("- Magenta (Down)", style="magenta")

    layout_group = Group(info_text, graph_text, legend)

    return Panel(
        layout_group,
        title="[bold white]🌐 NETWORK ANALYSIS[/bold white]",
        border_style=status_color,
        padding=(1, 2)
    )

if __name__ == "__main__":
    clear_screen()

    # Set a balanced timeline depth so it spans beautifully across the frame with spaces
    max_history_length = 40
    telemetry_history = [0.0] * max_history_length

    try:
        with Live(generate_panel(telemetry_history, 0), screen=False, auto_refresh=False) as live:
            while True:
                latency = check_latency()

                telemetry_history.append(latency)
                if len(telemetry_history) > max_history_length:
                    telemetry_history.pop(0)

                live.update(generate_panel(telemetry_history, latency), refresh=True)
                time.sleep(2.0)

    except KeyboardInterrupt:
        console.print("\n[bold red]Monitoring Engine Stopped.[/bold red]\n")

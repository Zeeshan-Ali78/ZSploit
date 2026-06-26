#!/usr/bin/env python3
"""
Z-Sploit - Modular Penetration Testing Framework
Author: Zeeshan Ali
Compatible with: Termux (Android) | Kali Linux
"""

import os
import sys
import shutil
import subprocess
import time
import random

# ─────────────────────────────────────────────
#  ANSI Color Helpers
# ─────────────────────────────────────────────
RED    = "\033[1;31m"
GREEN  = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN   = "\033[1;36m"
WHITE  = "\033[1;37m"
MAGENTA = "\033[1;35m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def red(t):    return f"{RED}{t}{RESET}"
def green(t):  return f"{GREEN}{t}{RESET}"
def yellow(t): return f"{YELLOW}{t}{RESET}"
def cyan(t):   return f"{CYAN}{t}{RESET}"
def white(t):  return f"{WHITE}{t}{RESET}"
def magenta(t): return f"{MAGENTA}{t}{RESET}"
def bold(t):   return f"{BOLD}{t}{RESET}"

def clear():
    os.system("clear")

def pause(secs=0.6):
    time.sleep(secs)

# ─────────────────────────────────────────────
#  Environment Detection
# ─────────────────────────────────────────────
def detect_env():
    """Return 'termux', 'kali', or 'unknown'."""
    if os.path.isdir("/data/data/com.termux"):
        return "termux"
    try:
        with open("/etc/os-release") as f:
            content = f.read().lower()
        if "kali" in content:
            return "kali"
    except FileNotFoundError:
        pass
    return "unknown"

ENV = detect_env()

def pkg_install(package):
    """Install a package using the right package manager."""
    if ENV == "termux":
        return os.system(f"pkg install -y {package}")
    else:
        return os.system(f"sudo apt-get install -y {package}")

# ─────────────────────────────────────────────
#  Tool Check & Install
# ─────────────────────────────────────────────
def check_tool(display_name, binary, install_fn):
    """
    Check if `binary` is on PATH.
    If found  → print confirmation and return True.
    If absent → install via install_fn and return result.
    """
    print(f"\n{cyan('▶')} Checking {bold(display_name)} ...", end=" ", flush=True)
    pause(0.3)

    if shutil.which(binary):
        print(green("✔  Already installed — OK"))
        return True
    else:
        print(yellow("✘  Not found — installing ..."))
        ret = install_fn()
        if ret == 0:
            print(green(f"   ✔  {display_name} installed successfully."))
            return True
        else:
            print(red(f"   ✘  Failed to install {display_name}. Check your connection/permissions."))
            return False

# ── Individual install functions ───────────────

def install_tor():
    if ENV == "termux":
        return os.system("pkg install -y tor")
    return os.system("sudo apt-get install -y tor")

def install_metasploit():
    if ENV == "termux":
        return os.system("pkg install -y unstable-repo && pkg install -y metasploit")
    return os.system("sudo apt-get install -y metasploit-framework")

def install_nmap():
    return pkg_install("nmap")

def install_zsploit_deps():
    """Z-Sploit itself is this script; we just ensure Python deps."""
    try:
        import socket      # stdlib – always present
        return 0
    except ImportError:
        return 1

# ─────────────────────────────────────────────
#  Dependency Bootstrap
# ─────────────────────────────────────────────
def bootstrap():
    clear()
    print(bold(cyan("=" * 55)))
    print(bold(cyan("   Z-Sploit  ·  Dependency Check & Setup")))
    print(bold(cyan("=" * 55)))

    results = {
        "Tor"         : check_tool("Tor",         "tor",    install_tor),
        "Metasploit"  : check_tool("Metasploit",  "msfconsole", install_metasploit),
        "Nmap"        : check_tool("Nmap",         "nmap",   install_nmap),
        "Z-Sploit"    : check_tool("Z-Sploit Core","python3", install_zsploit_deps),
    }

    print()
    failed = [name for name, ok in results.items() if not ok]
    if failed:
        print(yellow(f"⚠  Some tools could not be installed: {', '.join(failed)}"))
        print(yellow("   Proceeding with available tools.\n"))
    else:
        print(green("✔  All tools verified.\n"))

    pause(1.0)

# ─────────────────────────────────────────────
#  Banners (Metasploit-style random banner roulette)
# ─────────────────────────────────────────────

BANNER_1 = r"""
 ______     _____       _       _ _
|___  /    / ____|     | |     (_) |
   / / ___| (___  _ __ | | ___  _| |_
  / / / __|\___ \| '_ \| |/ _ \| | __|
 / /__\__ \____) | |_) | | (_) | | |_
/_____|___/_____/| .__/|_|\___/|_|\__|
                 | |
                 |_|
"""

BANNER_2 = r"""
 ▒███████▒      ░██████  ██▓███   ██▓     ▒█████   ██▓▄▄▄█████▓
 ▒ ▒ ▒ ▄▀░    ▒██    ▒ ▓██░  ██▒▓██▒    ▒██▒  ██▒▓██▒▓  ██▒ ▓▒
 ░ ▒ ▄▀▒░     ░ ▓██▄   ▓██░ ██▓▒▒██░    ▒██░  ██▒▒██▒▒ ▓██░ ▒░
   ▄▀▒   ░      ▒   ██▒▒██▄█▓▒ ▒▒██░    ▒██   ██░░██░░ ▓██▓ ░
 ▒███████▒    ▒██████▒▒▒██▒ ░  ░░██████▒░ ████▓▒░░██░  ▒██▒ ░
 ░▒▒ ▓░▒░▒    ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░ ░▓    ▒ ░░
"""

BANNER_3 = r"""
   _____            ______           _   _
  |__  /            / / __ \         | | (_)
    / / ______ ___  | |  | |_   _____ | |__| |_
   / / |_  / _` \ \ / / |  | \ \ / / '_ \| __| __|
  / /__/ / (_| |\ V /| |__| |\ V /| | | | |  | |_
 /_____/___\__,_| \_/  \____/  \_/ |_| |_|_|   \__|

         [ stay sharp. stay legal. stay ethical ]
"""

BANNER_4 = r"""
 #######            #####           ##        #####    #### #########
   ##    ###  ###  ##        #####  ##  ####  ##   ##    ##      ##
  ##    ##  ##  ## ##       ##   ## ## ##  ## ##    ##   ##      ##
 ##     ########## ##       ##   ## ## ##  ## ##    ##   ##      ##
######  ##      ##  #####    #####  ##  #### ##   ##  ######    ##

        >> framework loaded :: tor + nmap + msf <<
"""

BANNER_5 = r"""
       d8888 8888888b.        d8888 8888888888 8888888888
      d88888 888  "Y88b      d88888 888        888
     d88P888 888    888     d88P888 888        888
    d88P 888 888    888    d88P 888 8888888    8888888
   d88P  888 888    888   d88P  888 888        888
  d88P   888 888    888  d88P   888 888        888
 d88P    888 888  .d88P d88P    888 888        888
d8888888888888 8888888P" d8888888888 8888888888 8888888888

   (this banner intentionally left mysterious. - Zeeshan Ali)
"""

# Heart-shaped banner spelling "ZF" inside it (Metasploit-style novelty banner)
BANNER_HEART = r"""
{heart}    ███████╗      ███████╗{heart}
{heart}    ╚══███╔╝      ██╔════╝{heart}
{heart}      ███╔╝       █████╗  {heart}
{heart}     ███╔╝        ██╔══╝  {heart}
{heart}    ███████╗      ██║     {heart}
{heart}    ╚══════╝      ╚═╝     {heart}

           {heartword} Z-Sploit  ·  by Zeeshan Ali {heartword}
"""

def render_heart_banner():
    """Builds the heart banner using a red ASCII heart glyph, Metasploit-novelty style."""
    heart = red("\u2764")   # ❤ in red
    line = BANNER_HEART.format(heart=heart, heartword=heart)
    return line

BANNERS = [BANNER_1, BANNER_2, BANNER_3, BANNER_4, BANNER_5]

def random_banner():
    """Pick one of the six banners at random (5 normal + 1 heart), like msfconsole's banner roulette."""
    choice = random.randint(0, len(BANNERS))  # len(BANNERS) index reserved for heart banner
    if choice == len(BANNERS):
        return render_heart_banner()
    return BANNERS[choice]

# ─────────────────────────────────────────────
#  Welcome Screen
# ─────────────────────────────────────────────
def welcome():
    clear()
    width = 58
    print(cyan(random_banner()))
    print(bold(white("Z-Sploit".center(width))))
    print(cyan("Zeeshan Ali".center(width)))
    print()
    print("─" * width)
    desc = (
        "Z-Sploit is a modular, terminal-based penetration\n"
        "testing framework designed for Termux and Kali Linux.\n"
        
        "vulnerability assessment, and Metasploit exploitation\n"
        "into a single, guided workflow — no manual chaining\n"
        "required."
    )
    for line in desc.splitlines():
        print(line.center(width))
    print("─" * width)
    print(yellow(f"Type {bold('help')} at any prompt to see usage information."))
    update_status = check_for_updates()
    if update_status is True:
        print(magenta(f"⚡ A newer version of Z-Sploit is available — choose 'Update' in the menu."))
    print()

# ─────────────────────────────────────────────
#  Self-Update (git pull from Z-Sploit repo)
# ─────────────────────────────────────────────
ZSPLOIT_REPO_URL = "https://github.com/Zeeshan-Ali78/Z-Sploit.git"

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def check_for_updates():
    """
    Check if the local copy is inside a git repo tied to the Z-Sploit
    GitHub repo. If so, fetch + report whether updates are available.
    Returns True if updates are available, False otherwise (or on error).
    """
    repo_dir = get_script_dir()
    git_dir = os.path.join(repo_dir, ".git")

    if not os.path.isdir(git_dir):
        return None  # not a git checkout

    try:
        subprocess.run(
            ["git", "-C", repo_dir, "fetch", "origin"],
            check=True, capture_output=True, text=True, timeout=30
        )
        local = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "@"],
            check=True, capture_output=True, text=True
        ).stdout.strip()
        remote = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "@{u}"],
            check=True, capture_output=True, text=True
        ).stdout.strip()
        return local != remote
    except Exception:
        return None


def run_update():
    """
    Update Z-Sploit from its GitHub repo.
      - If the script is running inside a git checkout, do `git pull`.
      - Otherwise, offer to clone the repo fresh into ./Z-Sploit-latest
        next to the current script (since there's nothing to pull into).
    """
    print(bold(cyan("\n[*] Checking for Z-Sploit updates ...")))
    repo_dir = get_script_dir()
    git_dir = os.path.join(repo_dir, ".git")

    if os.path.isdir(git_dir):
        # We're inside a git checkout — do a normal pull
        try:
            result = subprocess.run(
                ["git", "-C", repo_dir, "pull", "--ff-only", "origin"],
                capture_output=True, text=True, timeout=60
            )
            print(result.stdout.strip())
            if result.returncode == 0:
                if "Already up to date" in result.stdout or "Already up-to-date" in result.stdout:
                    print(green("[✔] Z-Sploit is already up to date."))
                else:
                    print(green("[✔] Z-Sploit updated successfully. Restart the script to use the new version."))
            else:
                print(red("[!] Update failed:"))
                print(red(result.stderr.strip()))
                print(yellow("    If you have local changes, commit/stash them first, or re-clone the repo."))
        except FileNotFoundError:
            print(red("[!] 'git' is not installed. Install it first (e.g. 'apt install git' or 'pkg install git')."))
        except subprocess.TimeoutExpired:
            print(red("[!] Update timed out. Check your network connection and try again."))
        except Exception as e:
            print(red(f"[!] Unexpected error during update: {e}"))
    else:
        # Not a git checkout — offer a fresh clone alongside the current script
        print(yellow("[!] This copy of Z-Sploit isn't a git checkout, so there's nothing to 'pull'."))
        dest = os.path.join(repo_dir, "Z-Sploit-latest")
        ans = input(
            bold(f"    Clone the latest version from GitHub into '{dest}'? (yes/no): ")
        ).strip().lower()
        if ans in ("yes", "y"):
            try:
                result = subprocess.run(
                    ["git", "clone", ZSPLOIT_REPO_URL, dest],
                    capture_output=True, text=True, timeout=120
                )
                if result.returncode == 0:
                    print(green(f"[✔] Cloned latest Z-Sploit into: {dest}"))
                else:
                    print(red("[!] Clone failed:"))
                    print(red(result.stderr.strip()))
            except FileNotFoundError:
                print(red("[!] 'git' is not installed. Install it first (e.g. 'apt install git' or 'pkg install git')."))
            except subprocess.TimeoutExpired:
                print(red("[!] Clone timed out. Check your network connection and try again."))
            except Exception as e:
                print(red(f"[!] Unexpected error during clone: {e}"))
        else:
            print(cyan("    Skipped. You can grab updates manually from:"))
            print(cyan(f"    {ZSPLOIT_REPO_URL}"))

    input(yellow("\nPress Enter to continue..."))



def show_help():
    clear()
    width = 58
    print(bold(cyan("=" * width)))
    print(bold(white("Z-Sploit — Help / Usage Guide".center(width))))
    print(bold(cyan("=" * width)))
    print(f"""
{bold('OVERVIEW')}
  Z-Sploit is a guided wrapper that chains together
  well-known, legitimate security tools:
    - Tor       (traffic anonymisation)
    - Nmap      (host/service discovery & scanning)
    - Metasploit (exploitation framework console)

{bold('LEGAL / ETHICAL NOTICE')}
  Only run Z-Sploit against systems you own or have
  explicit written authorization to test. Unauthorized
  scanning or exploitation of systems is illegal in most
  jurisdictions.

{bold('MAIN MENU OPTIONS')}
  1  Vulnerability Scan   Runs Nmap (-sV -sC -O) against
                           the target.
  2  IP Trace              Runs reverse DNS, WHOIS, and
                           traceroute against the target.
  3  Both                  Runs scan + trace, then opens
                           msfconsole pre-seeded with the
                           target as RHOSTS.
  4  Help                  Shows this help screen.
  5  Update                Pulls the latest Z-Sploit from
                           GitHub ({ZSPLOIT_REPO_URL}).
  6  Exit                  Quits Z-Sploit.

{bold('TOR CONTROL')}
  Tor is started automatically at launch. You'll be asked
  whether to disconnect it when you finish your session.

{bold('COMMAND LINE')}
  python3 zsploit.py          Launch normally.
  python3 zsploit.py --help   Show this help and exit.
  python3 zsploit.py -h       Same as --help.

{bold('TIPS')}
  - Re-run the dependency check any time by restarting the
    script; missing tools are auto (re)installed where
    possible.
""")
    print(bold(cyan("=" * width)))
    input(yellow("\nPress Enter to return..."))

# ─────────────────────────────────────────────
#  Tor Control
# ─────────────────────────────────────────────
def start_tor():
    print(cyan("\n[*] Starting Tor service ..."))
    if ENV == "termux":
        os.system("tor &")
    else:
        os.system("sudo service tor start")
    pause(2)
    print(green("[✔] Tor is running. Traffic routed through onion network."))

def stop_tor():
    print(cyan("\n[*] Stopping Tor service ..."))
    if ENV == "termux":
        os.system("pkill tor")
    else:
        os.system("sudo service tor stop")
    print(green("[✔] Tor disconnected."))

# ─────────────────────────────────────────────
#  Operations
# ─────────────────────────────────────────────

def validate_ip(ip: str) -> bool:
    """Basic IPv4 / hostname validation."""
    import re
    ipv4 = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    if ipv4.match(ip):
        parts = ip.split(".")
        return all(0 <= int(p) <= 255 for p in parts)
    # Accept hostnames too
    hostname = re.compile(r"^[a-zA-Z0-9._-]+$")
    return bool(hostname.match(ip))


def run_vulnerability_scan(ip: str):
    """Nmap scan."""
    print(bold(cyan(f"\n[*] Starting Vulnerability Scan on {ip} ...")))
    print("─" * 50)

    # ── Nmap aggressive scan ──────────────────────
    if shutil.which("nmap"):
        print(yellow("\n[Nmap] Running service & version detection scan ..."))
        os.system(f"nmap -sV -sC -O --open -T4 {ip}")
    else:
        print(red("[!] Nmap not available — skipping Nmap scan."))

    print(green("\n[✔] Vulnerability scan complete."))


def run_ip_trace(ip: str):
    """Traceroute + WHOIS + reverse-DNS lookup."""
    print(bold(cyan(f"\n[*] Starting IP Trace on {ip} ...")))
    print("─" * 50)

    print(yellow("\n[Trace] Reverse DNS lookup ..."))
    os.system(f"nslookup {ip} 2>/dev/null || host {ip} 2>/dev/null || echo 'nslookup/host not available'")

    if shutil.which("whois"):
        print(yellow("\n[Trace] WHOIS information ..."))
        os.system(f"whois {ip}")
    else:
        print(yellow("[!] whois not installed — skipping WHOIS lookup."))

    tracer = "traceroute" if shutil.which("traceroute") else (
             "tracert"   if shutil.which("tracert")    else None)
    if tracer:
        print(yellow(f"\n[Trace] Running {tracer} ..."))
        os.system(f"{tracer} {ip}")
    else:
        print(yellow("[!] traceroute not found — skipping route trace."))

    print(green("\n[✔] IP trace complete."))


def launch_metasploit(ip: str):
    """Open msfconsole pre-seeded with the target host."""
    if not shutil.which("msfconsole"):
        print(red("[!] Metasploit (msfconsole) not found — skipping."))
        return
    print(bold(cyan(f"\n[*] Launching Metasploit against {ip} ...")))
    print(yellow("    Type 'exit' inside msfconsole to return to Z-Sploit.\n"))
    pause(1)
    rc_script = f"/tmp/zsploit_msf_{ip.replace('.','_')}.rc"
    with open(rc_script, "w") as f:
        f.write(f"setg RHOSTS {ip}\n")
        f.write("db_nmap -sV -O " + ip + "\n")
        f.write("vulns\n")
    os.system(f"msfconsole -r {rc_script}")
    try:
        os.remove(rc_script)
    except OSError:
        pass

# ─────────────────────────────────────────────
#  Main Flow
# ─────────────────────────────────────────────
def get_ip() -> str:
    while True:
        ip = input(bold("\n[?] Enter target IP address or hostname: ")).strip()
        if ip.lower() == "help":
            show_help()
            continue
        if ip and validate_ip(ip):
            return ip
        print(red("    Invalid IP / hostname. Please try again."))


def choose_action() -> str:
    print(bold(cyan("\n[?] Select an action:")))
    print(f"    {white('1')}  Vulnerability Scan  (Nmap)")
    print(f"    {white('2')}  IP Trace            (WHOIS + Traceroute + rDNS)")
    print(f"    {white('3')}  Both                (Scan + Trace + Metasploit)")
    print(f"    {white('4')}  Help")
    print(f"    {white('5')}  Update              (git pull from GitHub)")
    print(f"    {white('6')}  Exit")

    while True:
        choice = input(bold("\n    Your choice [1-6]: ")).strip().lower()
        if choice == "help":
            choice = "4"
        if choice == "update":
            choice = "5"
        if choice in ("1", "2", "3", "4", "5", "6"):
            if choice == "4":
                show_help()
                print(bold(cyan("\n[?] Select an action:")))
                print(f"    {white('1')}  Vulnerability Scan  (Nmap)")
                print(f"    {white('2')}  IP Trace            (WHOIS + Traceroute + rDNS)")
                print(f"    {white('3')}  Both                (Scan + Trace + Metasploit)")
                print(f"    {white('4')}  Help")
                print(f"    {white('5')}  Update              (git pull from GitHub)")
                print(f"    {white('6')}  Exit")
                continue
            if choice == "5":
                run_update()
                print(bold(cyan("\n[?] Select an action:")))
                print(f"    {white('1')}  Vulnerability Scan  (Nmap)")
                print(f"    {white('2')}  IP Trace            (WHOIS + Traceroute + rDNS)")
                print(f"    {white('3')}  Both                (Scan + Trace + Metasploit)")
                print(f"    {white('4')}  Help")
                print(f"    {white('5')}  Update              (git pull from GitHub)")
                print(f"    {white('6')}  Exit")
                continue
            return choice
        print(red("    Please enter 1, 2, 3, 4, 5, or 6."))


def ask_disconnect_tor() -> bool:
    ans = input(bold(yellow("\n[?] Disconnect Tor now? (yes/no): "))).strip().lower()
    return ans in ("yes", "y")


def main():
    # --help / -h command line flag
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        show_help()
        sys.exit(0)

    # Step 1 — dependency checks
    bootstrap()

    # Step 2 — welcome screen (random banner each run)
    welcome()

    # Step 3 — start Tor
    start_tor()

    # Step 4 — get target IP
    ip = get_ip()

    # Step 5 — choose action
    action = choose_action()

    if action == "6":
        print(cyan("\n[*] Exiting Z-Sploit. Goodbye!\n"))
        sys.exit(0)

    print()
    print("═" * 55)

    if action in ("1", "3"):
        run_vulnerability_scan(ip)

    if action in ("2", "3"):
        run_ip_trace(ip)

    if action == "3":
        launch_metasploit(ip)

    # Step 6 — Tor disconnect
    print("\n" + "═" * 55)
    if ask_disconnect_tor():
        stop_tor()
    else:
        print(cyan("[*] Tor remains active."))

    # Step 7 — graceful exit
    print()
    print(bold(green("╔══════════════════════════════════════╗")))
    print(bold(green("║   Z-Sploit session complete. Stay    ║")))
    print(bold(green("║        Ethical. Zeeshan Ali ©        ║")))
    print(bold(green("╚══════════════════════════════════════╝")))
    print()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(red("\n\n[!] Interrupted by user. Exiting cleanly.\n"))
        sys.exit(0)
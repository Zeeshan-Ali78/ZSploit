# Z-Sploit

**A guided, terminal-based wrapper around Tor, Nmap, and Metasploit for streamlined penetration-testing workflows.**

Z-Sploit chains together well-known, legitimate security tools into a single guided session — no manual chaining required. It checks for and installs missing dependencies, anonymises traffic through Tor, runs Nmap reconnaissance, and (optionally) hands the target straight to Metasploit, all from one menu.

---

## ⚠️ Legal & Ethical Notice

Z-Sploit is intended **only** for use against systems you own or have explicit, written authorization to test. Unauthorized scanning, probing, or exploitation of systems you do not control is illegal in most jurisdictions and may carry serious civil and criminal penalties.

The author and contributors take no responsibility for misuse of this tool. By using Z-Sploit you agree to use it ethically and legally.

---

## Features

- **Automatic dependency checks** — detects and installs Tor, Nmap, and Metasploit if missing (via `apt` on Kali Linux or `pkg` on Termux).
- **Tor integration** — automatically starts Tor at launch and offers to disconnect it when you're done.
- **Guided menu** — pick a vulnerability scan, an IP trace, or both, without remembering tool syntax.
- **Nmap vulnerability scan** — runs `nmap -sV -sC -O --open -T4` against your target.
- **IP trace** — reverse DNS, WHOIS, and traceroute in one step.
- **Metasploit handoff** — launches `msfconsole` pre-seeded with the target as `RHOSTS`, plus an automatic `db_nmap` import.
- **Random startup banners** — six rotating ASCII banners (Metasploit-style banner roulette), including a red-heart "ZF" novelty banner.
- **Built-in help system** — `help` command from any prompt, or `--help` / `-h` from the command line.
- **Self-updater** — pulls the latest version straight from this GitHub repo.
- **Cross-platform** — works on both Kali Linux and Termux (Android).

---

## Requirements

- Python 3.6+
- One of:
  - **Kali Linux** (or another Debian-based distro with `apt`)
  - **Termux** on Android
- `git` (for the self-update feature)
- Root/sudo access on Linux for installing packages and managing the Tor service

Z-Sploit will attempt to install missing tools automatically, but you can also install them manually beforehand:

```bash
# Kali Linux / Debian-based
sudo apt-get install -y tor nmap metasploit-framework whois traceroute git

# Termux
pkg install -y tor nmap unstable-repo metasploit git
```

---

## Installation

```bash
git clone https://github.com/Zeeshan-Ali78/Z-Sploit.git
cd Z-Sploit
chmod +x zsploit.py
```

---

## Usage

Run the script:

```bash
python3 zsploit.py
```

Show the help guide without launching the full workflow:

```bash
python3 zsploit.py --help
# or
python3 zsploit.py -h
```

### Walkthrough

1. **Dependency check** — Z-Sploit verifies Tor, Nmap, and Metasploit are installed, installing anything missing.
2. **Welcome screen** — a random banner is shown, along with an update notice if a newer version is available on GitHub.
3. **Tor starts automatically** to anonymise your traffic.
4. **Enter a target** — an IP address or hostname. Type `help` here at any time to view the help guide.
5. **Choose an action** from the menu:

   | Option | Action               | Description                                                        |
   |--------|----------------------|---------------------------------------------------------------------|
   | 1      | Vulnerability Scan   | Runs an Nmap service/version/OS detection scan against the target.  |
   | 2      | IP Trace             | Runs reverse DNS, WHOIS, and traceroute against the target.         |
   | 3      | Both                 | Runs the scan and trace, then opens `msfconsole` against the target.|
   | 4      | Help                 | Shows the in-app help guide.                                        |
   | 5      | Update               | Pulls the latest Z-Sploit release from GitHub.                      |
   | 6      | Exit                 | Quits Z-Sploit.                                                      |

6. **Tor disconnect prompt** — choose whether to stop Tor when you're finished.

---

## Updating

If you cloned Z-Sploit with `git`, you can update in two ways:

- From inside the app: choose **5. Update** from the main menu.
- From the command line:

  ```bash
  cd Z-Sploit
  git pull --ff-only origin
  ```

If your local copy isn't a git checkout, the in-app updater will offer to clone a fresh copy into a `Z-Sploit-latest` folder alongside the script.

---

## Project Structure

```
Z-Sploit/
├── zsploit.py     # Main application
└── README.md      # This file
```

---

## Contributing

Issues and pull requests are welcome. Please keep contributions focused on usability, reliability, and ethical-use safeguards (e.g., clearer authorization warnings, better input validation).

---

## Author

**Zeeshan Ali**

---

## License

Specify your preferred license here (e.g., MIT, GPLv3). If you haven't chosen one yet, [choosealicense.com](https://choosealicense.com/) can help you pick.

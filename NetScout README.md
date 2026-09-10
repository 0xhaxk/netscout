# NetScout 🔎

**NetScout** is a lightweight Python-based network port and service scanner built on top of **Nmap**.

The project was created as a practical cybersecurity learning project to strengthen my understanding of **network reconnaissance, service enumeration, Python automation, and security assessment workflows**.

> **For authorized security testing and personal lab environments only.**

---

## 🎯 Project Goals

The main goals of NetScout are to:

- Discover open TCP ports on a target.
- Identify services running on those ports.
- Detect service versions.
- Provide clean and readable scan results.
- Save scan results as structured JSON.
- Practice automating common reconnaissance tasks with Python.

---

## 🛠️ Technologies

- **Python 3**
- **Nmap**
- **python-nmap**
- Linux
- JSON

---

## ✨ Features

- IPv4, IPv6, and hostname target support
- Single-port scanning
- Port-range scanning
- TCP SYN scanning
- Service/version detection
- Open-port filtering
- Input validation
- Nmap dependency checking
- Human-readable terminal output
- Timestamped JSON reports
- Basic error handling
- Command-line arguments

---

## 📁 Project Structure

```text
NetScout/
│
├── netscout.py
├── reports/
│   └── scan_<target>_<timestamp>.json
│
└── README.md
```

---

# ⚙️ Installation

## 1. Install Nmap

### Debian / Ubuntu / Kali

```bash
sudo apt update
sudo apt install nmap
```

Verify the installation:

```bash
nmap --version
```

---

## 2. Install Python dependency

```bash
pip install python-nmap
```

---

# 🚀 Usage

NetScout can be used interactively:

```bash
python3 netscout.py
```

The program will ask for the target.

You can also provide the target directly:

```bash
python3 netscout.py 192.168.56.10
```

The default port range is:

```text
1-1000
```

---

## 🔌 Scan a Port Range

```bash
python3 netscout.py 192.168.56.10 -p 1-1000
```

Example:

```text
Target : 192.168.56.10
Ports  : 1-1000
Mode   : TCP SYN + service detection

Starting scan...
```

---

## 🎯 Scan a Specific Port

```bash
python3 netscout.py 192.168.56.10 -p 80
```

---

## 📊 Save Reports

NetScout automatically saves scan results as JSON.

Example:

```text
reports/
└── scan_192.168.56.10_20260910_110000.json
```

A report contains information such as:

```json
{
  "tool": "NetScout",
  "version": "1.0",
  "target": "192.168.56.10",
  "ports_scanned": "1-1000",
  "results": []
}
```

This makes the results easier to process later with other scripts or security tools.

---

# 🔍 How It Works

The current scanning workflow is:

```text
            Target
               │
               ▼
        Input Validation
               │
               ▼
          Nmap Scanner
               │
        ┌──────┴──────┐
        │             │
     Port Scan    Service Detection
        │             │
        └──────┬──────┘
               ▼
        Parse Scan Results
               │
        ┌──────┴──────┐
        │             │
     Terminal       JSON
      Output        Report
```

NetScout uses Nmap with:

```text
-sS
```

for TCP SYN scanning and:

```text
-sV
```

for service/version detection.

The:

```text
--open
```

option limits the displayed results to open ports.

---

# 🧪 Lab Testing

This project is intended to be tested inside an authorized environment.

For example:

```text
Host Machine
     │
     └── Virtual Network
            │
            ├── Kali Linux
            │
            ├── Ubuntu Server
            │
            └── Windows VM
```

Example workflow:

```text
1. Start the lab machines
        ↓
2. Identify their IP addresses
        ↓
3. Run NetScout
        ↓
4. Identify exposed ports
        ↓
5. Identify services and versions
        ↓
6. Analyze the results
        ↓
7. Save the JSON report
```

---

# 📸 Example Output

Example terminal output:

```text
PORT      STATE     SERVICE           VERSION
----------------------------------------------------------------
22/tcp    open      ssh               OpenSSH
80/tcp    open      http              Apache
443/tcp   open      https             nginx
----------------------------------------------------------------

Open ports found: 3

JSON report saved to:
reports/scan_192.168.56.10_20260910_110000.json
```

*The actual output depends on the services running on the authorized target.*

---

# 🧠 What I Learned

Building NetScout helped me practice:

### Network Reconnaissance

Understanding how port scanning can reveal the attack surface of a system.

### Service Enumeration

Understanding how service/version detection provides additional context about exposed services.

### Python Automation

Using Python to interact with an external security tool and process its results.

### Input Validation

Handling targets and port ranges safely instead of assuming user input is valid.

### Structured Data

Saving scan information as JSON so it can be consumed by other tools or scripts.

### Security Workflow

Moving from:

```text
Discovery
   ↓
Enumeration
   ↓
Analysis
   ↓
Documentation
```

rather than treating scanning as the entire penetration-testing process.

---

# 🔮 Future Improvements

Planned improvements:

- [ ] Host discovery mode
- [ ] UDP scanning support
- [ ] Custom Nmap arguments
- [ ] XML output support
- [ ] HTML report generation
- [ ] Better service fingerprinting
- [ ] Scan comparison
- [ ] Detect newly exposed ports
- [ ] Report severity/context
- [ ] Concurrent scanning of multiple authorized hosts
- [ ] Configuration file support
- [ ] Unit tests
- [ ] Better logging

---

# ⚠️ Legal & Ethical Use

NetScout is intended for:

- Personal cybersecurity labs
- CTF environments
- Systems you own
- Systems where you have explicit authorization to perform security testing

**Do not scan systems or networks without permission.**

Unauthorized scanning may violate organizational policies or applicable laws.

---

# 👨‍💻 Author

**Veereswar**

Cybersecurity enthusiast focused on:

- Web Application Penetration Testing
- Security Engineering
- Network Security
- Linux
- Python Security Automation

---

## 📚 References

- Nmap documentation
- Python `python-nmap` library documentation

---

## 📌 Project Status

**Version:** `1.0`

**Status:** Active learning project

Future versions will focus on improving automation, reporting, and integration with a broader penetration-testing workflow.
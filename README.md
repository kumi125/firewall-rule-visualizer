<p align="center">
  <img src="assets/icons/app_icon.png" width="150"/>
</p>


# 🛡️ Firewall Rule Visualizer

A **Windows-only GUI tool** to view, manage, and simulate firewall rules in real-time.  
It helps visualize your firewall configuration, simulate network traffic, and perform quick rule management—all from a single application.

---

## 🚀 Features

| Feature | Status | Description |
|--------|--------|-------------|
| Create rule | ✅ | Add firewall rules with full parameters |
| Delete rule | ✅ | Remove existing rules |
| Enable / Disable rule | ✅ | Toggle rule usage |
| Refresh rules | ✅ | Reload rules from file |
| Light/Dark mode | ✅ | Switch UI themes |
| Simulate traffic | ⚠️ Basic | Shows allow/block preview |
| Export rules to file | ⚠️ Basic | Save rules into JSON |
| Real-time traffic graph | 🔜 Planned | Live matplotlib traffic graph |
| Rule search & filter | 🔜 Planned | Filter rules by port/IP |

---

## 📸 Screenshots

**SCREENSHOT 1**  
![Screenshot 1](firewall_rule_visualizer/assets/screenshots/fw1.png)

**SCREENSHOT 2**  
![Screenshot 2](firewall_rule_visualizer/assets/screenshots/fw2.png)

**SCREENSHOT 3**  
![Screenshot 3](firewall_rule_visualizer/assets/screenshots/fw3.png)

**SCREENSHOT 4**  
![Screenshot 4](firewall_rule_visualizer/assets/screenshots/fw4.png)

**SCREENSHOT 5**  
![Screenshot 5](firewall_rule_visualizer/assets/screenshots/fw5.png)

**SCREENSHOT 6**  
![Screenshot 6](firewall_rule_visualizer/assets/screenshots/fw6.png)

---

## 🛠️ Requirements

- Windows OS (7/10/11)
- Python 3.12+
- Python Libraries:
  - `tkinter` (usually comes with Python)
  - `matplotlib`

---

## ⚡ Installation & Run

1. Clone the repository:

```bash
git clone https://github.com/kumi125/firewall-rule-visualizer.git
cd firewall-rule-visualizer

    Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate

    Install dependencies:

pip install -r requirements.txt

    Run the application:

python firewall_gui.py

    Note: This tool is Windows-only and requires administrator privileges for creating/deleting firewall rules.

📁 Usage Example

    Refresh rules to see current firewall configuration.

    Create a new rule using the ➕ Create Rule button.

    Simulate traffic by pinging a host and view the response graph.

    Toggle dark/light mode or search for specific rules.

    Export rules to firewall_rules.txt for backup or analysis.

## 🛣️ Roadmap

- [ ] Real-time traffic logs
- [ ] Advanced SIEM-style alert panel
- [ ] Import firewall rules from CSV
- [ ] Export rules to IPTables (Linux)
- [ ] Export rules to Windows Firewall format
- [ ] Auto-detect blocked traffic


#📝 License

This project is licensed under the MIT License.

#👤 Author

Kumail Hussain
Cybersecurity Student & Python Developer
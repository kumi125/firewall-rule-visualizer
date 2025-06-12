import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import re
import matplotlib.pyplot as plt

# Global variables
all_rules = ""
ping_result = ""
is_dark_mode = True
search_mode = "Firewall"

def get_firewall_rules():
    try:
        return subprocess.check_output("netsh advfirewall firewall show rule name=all", shell=True, text=True)
    except subprocess.CalledProcessError:
        return "Could not retrieve firewall rules."

def refresh_rules():
    global all_rules
    all_rules = get_firewall_rules()
    text_box.delete(1.0, tk.END)
    insert_with_highlights(all_rules)
    status_label.config(text="✅ Firewall rules loaded")

def export_rules_to_file():
    with open("firewall_rules.txt", "w", encoding="utf-8") as file:
        file.write(text_box.get(1.0, tk.END))
    status_label.config(text="✅ Rules exported to 'firewall_rules.txt'")

def simulate_traffic():
    global ping_result
    try:
        result = subprocess.check_output("ping 8.8.8.8 -n 4", shell=True, text=True)
        ping_result = result
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Simulated Traffic: Pinging 8.8.8.8\n\n" + result)
        status_label.config(text="✅ Simulated traffic completed")

        ping_times = re.findall(r"time[=<]\s*(\d+)\s*ms", result)
        if ping_times:
            show_ping_graph(list(map(int, ping_times)))
    except subprocess.CalledProcessError:
        text_box.insert(tk.END, "Error: Could not run simulated traffic")
        status_label.config(text="❌ Error in simulation")

def show_ping_graph(ping_times):
    plt.figure(figsize=(5, 3))
    plt.plot(ping_times, marker='o', linestyle='-', color='skyblue')
    plt.title("Ping Response Times (ms)")
    plt.xlabel("Ping Attempt")
    plt.ylabel("Response Time (ms)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def search_rules():
    keyword = search_entry.get().lower()
    text_box.tag_remove("highlight", "1.0", tk.END)
    content = all_rules if search_mode == "Firewall" else ping_result

    if keyword == "":
        text_box.delete(1.0, tk.END)
        insert_with_highlights(content)
        status_label.config(text=f"Showing all {search_mode.lower()} data")
        return

    filtered_lines = [line for line in content.splitlines() if keyword in line.lower()]
    text_box.delete(1.0, tk.END)
    insert_with_highlights("\n".join(filtered_lines))

    start = "1.0"
    while True:
        start = text_box.search(keyword, start, stopindex=tk.END, nocase=True)
        if not start:
            break
        end = f"{start}+{len(keyword)}c"
        text_box.tag_add("highlight", start, end)
        start = end

    status_label.config(text=f"🔍 Showing results for '{keyword}' in {search_mode.lower()}")

def insert_with_highlights(text):
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    for keyword, tag in [("allow", "allow"), ("block", "block"), ("inbound", "inbound"), ("outbound", "outbound")]:
        start = "1.0"
        while True:
            start = text_box.search(keyword, start, stopindex=tk.END, nocase=True)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            text_box.tag_add(tag, start, end)
            start = end

def toggle_search_mode():
    global search_mode
    search_mode = "Ping" if search_mode == "Firewall" else "Firewall"
    mode_button.config(text=f"Mode: {search_mode}")
    status_label.config(text=f"🔄 Switched to {search_mode} search")

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

def apply_theme():
    if is_dark_mode:
        bg, fg, entry_bg = "#1e1e1e", "white", "#2e2e2e"
        theme_button.config(text="🌞 Light Mode")
    else:
        bg, fg, entry_bg = "white", "black", "white"
        theme_button.config(text="🌙 Dark Mode")

    root.configure(bg=bg)
    title_label.config(bg=bg, fg=fg)
    search_frame.config(bg=bg)
    search_label.config(bg=bg, fg=fg)
    search_entry.config(bg=entry_bg, fg=fg, insertbackground=fg)
    button_frame.config(bg=bg)
    status_label.config(bg=bg, fg="green")
    text_box.config(bg=entry_bg, fg=fg, insertbackground=fg)

def toggle_rule():
    rule_name = simpledialog.askstring("Toggle Rule", "Enter the exact rule name:")
    if not rule_name:
        return
    try:
        current_rules = subprocess.check_output(f'netsh advfirewall firewall show rule name="{rule_name}"', shell=True, text=True)
        if "Enabled: Yes" in current_rules:
            subprocess.check_output(f'netsh advfirewall firewall set rule name="{rule_name}" new enable=no', shell=True, text=True)
            status_label.config(text=f"🚫 Disabled rule: {rule_name}")
        else:
            subprocess.check_output(f'netsh advfirewall firewall set rule name="{rule_name}" new enable=yes', shell=True, text=True)
            status_label.config(text=f"✅ Enabled rule: {rule_name}")
        refresh_rules()
    except subprocess.CalledProcessError:
        status_label.config(text=f"❌ Could not toggle rule: {rule_name}")

def delete_rule():
    rule_name = simpledialog.askstring("Delete Rule", "Enter the exact rule name to delete:")
    if not rule_name:
        return
    try:
        subprocess.check_output(f'netsh advfirewall firewall delete rule name="{rule_name}"', shell=True, text=True)
        status_label.config(text=f"🗑️ Deleted rule: {rule_name}")
        refresh_rules()
    except subprocess.CalledProcessError:
        status_label.config(text=f"❌ Could not delete rule: {rule_name}")

def create_rule():
    name = simpledialog.askstring("Rule Name", "Enter a name for the rule:")
    if not name:
        return
    protocol = simpledialog.askstring("Protocol", "Enter protocol (TCP/UDP):")
    if protocol not in ["TCP", "UDP"]:
        messagebox.showerror("Invalid Input", "Protocol must be TCP or UDP")
        return
    direction = simpledialog.askstring("Direction", "Enter direction (in/out):")
    if direction.lower() not in ["in", "out"]:
        messagebox.showerror("Invalid Input", "Direction must be 'in' or 'out'")
        return
    action = simpledialog.askstring("Action", "Enter action (allow/block):")
    if action.lower() not in ["allow", "block"]:
        messagebox.showerror("Invalid Input", "Action must be 'allow' or 'block'")
        return

    cmd = f'netsh advfirewall firewall add rule name="{name}" dir={direction} action={action} protocol={protocol} enable=yes'
    try:
        subprocess.check_output(cmd, shell=True, text=True)
        status_label.config(text=f"✅ Created rule: {name}")
        refresh_rules()
    except subprocess.CalledProcessError:
        status_label.config(text=f"❌ Failed to create rule: {name}")

# GUI Setup
root = tk.Tk()
root.title("Firewall Rule Visualizer")
root.geometry("980x730")
root.iconbitmap("app_icon.ico")


title_label = tk.Label(root, text="Firewall Rules", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)

search_label = tk.Label(search_frame, text="Search:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="🔍 Search", command=search_rules)
search_button.pack(side=tk.LEFT, padx=5)

mode_button = tk.Button(search_frame, text="Mode: Firewall", command=toggle_search_mode)
mode_button.pack(side=tk.LEFT, padx=5)

text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10), yscrollcommand=scrollbar.set)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=text_box.yview)

text_box.tag_configure("allow", foreground="green")
text_box.tag_configure("block", foreground="red")
text_box.tag_configure("inbound", foreground="blue")
text_box.tag_configure("outbound", foreground="orange")
text_box.tag_configure("highlight", background="yellow", foreground="black")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="🔄 Refresh Rules", command=refresh_rules).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="💾 Export to File", command=export_rules_to_file).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="🌐 Simulate Traffic", command=simulate_traffic).grid(row=0, column=2, padx=5)
theme_button = tk.Button(button_frame, text="🌞 Light Mode", command=toggle_theme)
theme_button.grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="🚦 Enable/Disable Rule", command=toggle_rule).grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="🗑️ Delete Rule", command=delete_rule).grid(row=0, column=5, padx=5)
tk.Button(button_frame, text="➕ Create Rule", command=create_rule).grid(row=0, column=6, padx=5)

status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=5)

refresh_rules()
apply_theme()
root.mainloop()

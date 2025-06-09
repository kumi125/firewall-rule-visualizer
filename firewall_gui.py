import tkinter as tk
import subprocess

def fetch_firewall_rules():
    try:
        result = subprocess.check_output(
            ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Split rules by divider line for readability
        rules = result.split("---------------------------------------------------------------------")
        
        # Clear box
        text_box.delete(1.0, tk.END)
        
        # Show each rule with spacing
        for rule in rules:
            if "Rule Name" in rule:
                text_box.insert(tk.END, rule.strip() + "\n\n" + "-"*60 + "\n\n")
                
    except subprocess.CalledProcessError as e:
        text_box.insert(tk.END, "Error:\n" + str(e.output))

# GUI setup
root = tk.Tk()
root.title("Firewall Rule Visualizer")
root.geometry("800x600")

# Heading label
label = tk.Label(root, text="Firewall Rule Visualizer", font=("Arial", 16))
label.pack(pady=10)

# Button to show rules
button = tk.Button(root, text="Show Firewall Rules", command=fetch_firewall_rules)
button.pack(pady=10)

# Scrollable text box
text_box = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

root.mainloop()

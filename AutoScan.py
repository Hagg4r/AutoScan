import subprocess
import os

def run_command(command):
    """Run a command and return its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def save_to_file(filepath, data):
    """Save data to a file."""
    with open(filepath, 'a') as file:
        file.write(data + '\n')

def install_tools():
    """Install necessary tools if not already installed."""
    tools = {
        "ffuf": "sudo apt-get install -y ffuf",
        "amass": "sudo apt-get install -y amass",
        "uniscan": "sudo apt-get install -y uniscan"
    }
    
    for tool, install_command in tools.items():
        print(f"Checking if {tool} is installed...")
        if not is_tool_installed(tool):
            print(f"{tool} not found. Installing {tool}...")
            stdout, stderr = run_command(install_command.split())
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
        else:
            print(f"{tool} is already installed.")

def is_tool_installed(tool_name):
    """Check if a tool is installed."""
    return subprocess.call(["which", tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def main():
    install_tools()

    link = input("Inserisci il link da scannerizzare: ")
    
    # Determina il percorso del desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = os.path.join(desktop_path, "scan_results.txt")
    
    # Clear the file if it exists
    open(output_file, 'w').close()
    
    tools = {
        "sqlmap": ["sqlmap", "-u", link, "--batch"],
        "ffuf": ["ffuf", "-u", f"{link}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"],
        "whois": ["whois", link],
        "nikto": ["nikto", "-h", link],
        "uniscan": ["uniscan", "-u", link]
    }
    
    for tool_name, command in tools.items():
        print(f"Esecuzione di {tool_name}...")
        stdout, stderr = run_command(command)
        save_to_file(output_file, f"=== Risultati {tool_name} ===\n")
        if stdout:
            save_to_file(output_file, stdout)
        if stderr:
            save_to_file(output_file, f"Errori:\n{stderr}")
    
    # Aggiungi la firma alla fine del file
    save_to_file(output_file, "\nby Haggar")

if __name__ == "__main__":
    main()
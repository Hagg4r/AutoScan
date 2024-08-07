import subprocess
import os

def run_command(command):
    """Run a command and return its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def run_sudo_command(command):
    """Run a command with sudo and return its output."""
    result = subprocess.run(['sudo'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def save_to_file(filepath, data):
    """Save data to a file."""
    with open(filepath, 'a') as file:
        file.write(data + '\n')

def install_tools():
    """Install necessary tools if not already installed."""
    tools = {
        "amass": "sudo apt-get install -y amass",
        "uniscan": "sudo apt-get install -y uniscan",
        "nmap": "sudo apt-get install -y nmap",
        "sqlmap": "sudo apt-get install -y sqlmap",
        "nikto": "sudo apt-get install -y nikto",
        "whois": "sudo apt-get install -y whois",
        "subfinder": "sudo apt-get install -y subfinder",
    }
    
    for tool, install_command in tools.items():
        print(f"Checking if {tool} is installed...")
        if not is_tool_installed(tool):
            print(f"{tool} not found. Installing {tool}...")
            stdout, stderr = run_sudo_command(install_command.split())
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
        else:
            print(f"{tool} is already installed.")

def is_tool_installed(tool_name):
    """Check if a tool is installed."""
    return subprocess.call(["which", tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header 'hagg4rscan'."""
    header = """
     ▄▀▀▄ ▄▄   ▄▀▀█▄   ▄▀▀▀▀▄    ▄▀▀▀▀▄    ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄  ▄▀▄▄▄▄   ▄▀▀█▄   ▄▀▀▄ ▀▄ 
█  █   ▄▀ ▐ ▄▀ ▀▄ █         █         █   █   █ █ █   ▐ █ █    ▌ ▐ ▄▀ ▀▄ █  █ █ █ 
▐  █▄▄▄█    █▄▄▄█ █    ▀▄▄  █    ▀▄▄  ▐  █▀▀█▀     ▀▄   ▐ █        █▄▄▄█ ▐  █  ▀█ 
   █   █   ▄▀   █ █     █ █ █     █ █  ▄▀    █  ▀▄   █    █       ▄▀   █   █   █  
  ▄▀  ▄▀  █   ▄▀  ▐▀▄▄▄▄▀ ▐ ▐▀▄▄▄▄▀ ▐ █     █    █▀▀▀    ▄▀▄▄▄▄▀ █   ▄▀  ▄▀   █   
 █   █    ▐   ▐   ▐         ▐         ▐     ▐    ▐      █     ▐  ▐   ▐   █    ▐   
 ▐   ▐                                                  ▐                ▐        
    """
    print(header)

def main():
    install_tools()
    
    # Clear the screen after installing the tools
    clear_screen()

    # Print the header
    print_header()

    link = input("Target: ")
    
    # Determine the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_dir = os.path.join(desktop_path, link)
    os.makedirs(target_dir, exist_ok=True)
    output_file = os.path.join(target_dir, "domain.txt")
    
    # Clear the file if it exists
    open(output_file, 'w').close()
    
    tools = {
        "subfinder": ["subfinder", "-d", link, "-o", output_file],
        "sqlmap": ["sqlmap", "--url", link],
        "whois": ["whois", link],
        "nikto": ["nikto", "-h", link],
        "uniscan": ["uniscan", "-u", link, "-qd"],
        "nmap": ["nmap", link],
    }

    total_tools = len(tools)
    
    for i, (tool_name, command) in enumerate(tools.items(), 1):
        print(f"Esecuzione di {tool_name} ({i}/{total_tools})...")
        stdout, stderr = run_command(command)
        save_to_file(output_file, f"=== Risultati {tool_name} ===\n")
        if stdout:
            save_to_file(output_file, stdout)
        if stderr:
            save_to_file(output_file, f"Errori:\n{stderr}")
        
        # Calculate and print the progress
        progress = (i / total_tools) * 100
        print(f"Progresso: {progress:.2f}%")

    # Execute additional SQLMap commands to retrieve database information
    additional_sqlmap_commands = [
        f"sqlmap -u {link} --dbs",
        f"sqlmap -u {link} -D <nome_database> --tables",
        f"sqlmap -u {link} -D <nome_database> -T <nome_tabella> --columns",
        f"sqlmap -u {link} -D <nome_database> -T <nome_tabella> -C <nome_colonna> --dump"
    ]
    
    for command in additional_sqlmap_commands:
        stdout, stderr = run_command(command.split())
        save_to_file(output_file, f"=== Risultati SQLMap ===\n")
        if stdout:
            save_to_file(output_file, stdout)
        if stderr:
            save_to_file(output_file, f"Errori:\n{stderr}")

if __name__ == "__main__":
    main()
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
        "uniscan": "sudo apt-get install -y uniscan",
        "nmap": "sudo apt-get install -y nmap",
        "sqlmap": "sudo apt-get install -y sqlmap",
        "nikto": "sudo apt-get install -y nikto",
        "whois": "sudo apt-get install -y whois"
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

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header 'hagg4rscan'."""
    header = """
     __  __                       __ __           ____                               
/\ \/\ \                         /\ \\ \         /\  _`\                             
\ \ \_\ \     __       __      __\ \ \\ \    _ __\ \,\L\_\    ___     __      ___    
 \ \  _  \  /'__`\   /'_ `\  /'_ `\ \ \\ \_ /\`'__\/_\__ \   /'___\ /'__`\  /' _ `\  
  \ \ \ \ \/\ \L\.\_/\ \L\ \/\ \L\ \ \__ ,__\ \ \/  /\ \L\ \/\ \__//\ \L\.\_/\ \/\ \ 
   \ \_\ \_\ \__/.\_\ \____ \ \____ \/_/\_\_/\ \_\  \ `\____\ \____\ \__/.\_\ \_\ \_\
    \/_/\/_/\/__/\/_/\/___L\ \/___L\ \ \/_/   \/_/   \/_____/\/____/\/__/\/_/\/_/\/_/
                       /\____/ /\____/                                               
                       \_/__/  \_/__/                                                

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
    output_file = os.path.join(desktop_path, "scan_results.txt")
    
    # Clear the file if it exists
    open(output_file, 'w').close()
    
    tools = {
        "sqlmap": ["sqlmap", "--url", link, "--batch"],
        "ffuf": ["ffuf", "-u", f"{link}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"],
        "whois": ["whois", link],
        "nikto": ["nikto", "-u", link],
        "uniscan": ["uniscan", "-u", link, "-d"],
        "nmap": ["nmap", "-v", link]
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
    
    # Add signature at the end of the file
    save_to_file(output_file, "\nby Haggar")

if __name__ == "__main__":
    main()
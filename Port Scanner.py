import socket
import time
import concurrent.futures

# Comprehensive list of ports and their associated service names
port_names = {
    1: "TCP Port Service Multiplexer (TCPMUX)",
    7: "Echo",
    9: "Discard",
    11: "Active Users",
    13: "Daytime",
    17: "Quote of the Day",
    19: "Chargen",
    20: "FTP Data Transfer",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP (Server)",
    68: "DHCP (Client)",
    69: "Trivial File Transfer Protocol (TFTP)",
    80: "HTTP",
    110: "POP3",
    119: "Network News Transfer Protocol (NNTP)",
    123: "Network Time Protocol (NTP)",
    143: "IMAP",
    161: "Simple Network Management Protocol (SNMP)",
    162: "SNMP Trap",
    179: "Border Gateway Protocol (BGP)",
    443: "HTTPS",
    465: "SMTPS",
    514: "Syslog",
    587: "SMTP (Submission)",
    631: "Internet Printing Protocol (IPP)",
    993: "IMAPS",
    995: "POP3S",
    1080: "SOCKS Proxy",
    1433: "Microsoft SQL Server",
    1434: "Microsoft SQL Monitor",
    1521: "Oracle Database Listener",
    3306: "MySQL",
    3389: "Remote Desktop Protocol (RDP)",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP Alternative",
    8443: "HTTPS Alternative",
    27017: "MongoDB",
    5000: "UPnP",
    6000: "X Window System",
    6660: "Internet Relay Chat (IRC)",
    6666: "Internet Relay Chat (IRC)",
    8081: "HTTP Alternative",
    9000: "HTTP Alt (various)",
    27015: "Steam (gaming)",
    49152: "Dynamic/Private Port Range Start",
    49153: "Dynamic/Private Port Range End",
    # Add more ports as needed for your specific use case
}

# Function to scan a specific port
def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout to avoid hanging for too long
    result = sock.connect_ex((target, port))  # Returns 0 if the connection is successful
    sock.close()  # Close the socket after checking
    return port if result == 0 else None  # Return the port if it's open, otherwise return None

# Function to get the name of a port if available in the dictionary
def get_port_name(port):
    return port_names.get(port, "Unknown Service")

# Function to scan ports concurrently and display results in real-time
def port_scan(target, start_port, end_port):
    open_ports = []  # List to store open ports
    print("Scanning ports... Please wait.")
    
    # Start the scan using a ThreadPoolExecutor for concurrency
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start scanning all ports concurrently
        future_to_port = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            result = future.result()
            if result:
                port_name = get_port_name(result)
                open_ports.append((result, port_name))  # Store open port and service name
                print(f"Port {result} ({port_name}) is open!")

    # If no open ports were found, let the user know
    if not open_ports:
        print(f"No open ports found on {target} in the range {start_port}-{end_port}.")
    
    print("\nPort scan complete.")

# Example usage
if __name__ == "__main__":
    target = ""  # Replace with the target IP address
    start_port = 1
    end_port = 1024  # Limiting range to 1-1024 to scan well-known ports
    port_scan(target, start_port, end_port)

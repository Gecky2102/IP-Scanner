# Configurazione IP Scanner

# Porte comuni da scansionare
PORTE_COMUNI = [
    20,    # FTP-data
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    67,    # DHCP Server
    68,    # DHCP Client
    69,    # TFTP
    80,    # HTTP
    88,    # Kerberos
    110,   # POP3
    123,   # NTP
    135,   # RPC
    137,   # NetBIOS Name Service
    138,   # NetBIOS Datagram
    139,   # NetBIOS Session
    143,   # IMAP
    161,   # SNMP
    162,   # SNMP Trap
    389,   # LDAP
    443,   # HTTPS
    445,   # SMB
    465,   # SMTPS
    500,   # IPsec/IKE
    587,   # SMTP Submission
    636,   # LDAPS
    993,   # IMAPS
    995,   # POP3S
    1433,  # MS SQL
    1521,  # Oracle
    1723,  # PPTP
    2049,  # NFS
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    5900,  # VNC
    6379,  # Redis
    8080,  # HTTP Proxy
    8443,  # HTTPS Alt
    9100,  # Printer
    27017, # MongoDB
    27018  # MongoDB Shard
]

# Timeout per le connessioni (secondi)
TIMEOUT_DEFAULT = 1

# Numero massimo di thread
MAX_THREADS = 100

# Porte per servizi web comuni
WEB_PORTS = [80, 443, 8080, 8443, 3000, 5000, 8000]

# Porte per database comuni
DB_PORTS = [3306, 5432, 1433, 5984, 27017]

# Porte per servizi di rete comuni
NETWORK_PORTS = [21, 22, 23, 25, 53, 110, 143, 993, 995]

# 🔍 IP Scanner

Un potente scansionatore di rete e porte scritto in Python con interfaccia a linea di comando e **interfaccia grafica moderna** con tema scuro.

## ✨ Caratteristiche

### 🎯 **Scansione Intelligente**
- **Rilevamento automatico rete locale** - Trova automaticamente la tua rete
- **Scansione IP singoli** - Verifica host specifici
- **Scansione reti intere** - Analizza interi subnet (es: 192.168.1.0/24)
- **Range di porte personalizzabili** - Da singole porte a range completi (1-65535)

### 🚀 **Performance Avanzate**
- **Multithreading** - Fino a 500 thread per scansioni ultra-veloci
- **Timeout intelligente** - Ottimizza velocità vs accuratezza
- **Progress tracking** - Monitoraggio in tempo reale con ETA
- **Cancellazione immediata** - Stop istantaneo delle scansioni

### 🎨 **Interfaccia Grafica Moderna**
- **⚫ Tema scuro professionale** - Design elegante e moderno
- **📊 Dashboard in tempo reale** - Statistiche live durante la scansione
- **⏱️ Tempo stimato (ETA)** - Calcolo dinamico del tempo rimanente
- **🌐 Auto-detect rete** - Rileva automaticamente la configurazione di rete
- **💾 Esportazione avanzata** - Salva in JSON o TXT con metadati

### 🔧 **Modalità Porte Intelligenti**
- **Porte Comuni** - Le 50+ porte più utilizzate
- **Solo Web** - HTTP/HTTPS e varianti (80, 443, 8080, 8443)
- **Solo Database** - MySQL, PostgreSQL, MongoDB, Redis
- **Solo Rete** - FTP, SSH, DNS, SMTP, POP3
- **Personalizzate** - Lista custom (es: 80,443,22,3306)
- **Range** - Intervalli (es: 1-1000, 8000-9000)

### 💡 **Funzionalità Professionali**
- **🏠 Risoluzione hostname** - Nomi host automatici per ogni IP
- **📋 Identificazione servizi** - Riconosce 50+ servizi comuni
- **� MAC Address Detection** - Rileva indirizzi fisici via ARP
- **💻 Device Name Recognition** - Identifica nomi dispositivi (NetBIOS)
- **📊 Report Avanzati** - Export in CSV, Excel, JSON, HTML interattivo
- **🌐 Tabella Finale Automatica** - Report HTML si apre automaticamente
- **�💬 Interfaccia italiana** - Completamente localizzata
- **🛡️ Uso responsabile** - Guide sicurezza integrate
- **📈 Statistiche dettagliate** - Report completi con metriche

## 🚀 Installazione

1. Clona il repository:
```bash
git clone https://github.com/Gecky2102/IP-Scanner.git
cd IP-Scanner
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## 📖 Utilizzo

### 🎨 Interfaccia Grafica (Consigliata)

Avvia l'interfaccia grafica moderna:

```bash
python run_gui.py
```

**Caratteristiche dell'interfaccia grafica:**
- ⚫ **Tema scuro professionale** con design moderno
- 🌐 **Auto-detect rete locale** - Rileva automaticamente la tua rete
- 📊 **Monitoraggio tempo reale** - Progress bar, statistiche live, ETA
- 🔧 **Raccolta automatica MAC** - Indirizzi fisici via ARP
- 💻 **Identificazione dispositivi** - Nomi device via NetBIOS/DNS
- 📊 **Report finale automatico** - HTML interattivo si apre al termine
- 💾 **Esportazione multi-formato** - CSV, Excel, JSON, HTML
- 🎯 **Modalità porte preconfigurate**:
  - Porte Comuni (50+ porte più utilizzate)
  - Solo Web (80, 443, 8080, 8443)
  - Solo Database (3306, 5432, 1433, MongoDB, Redis)
  - Solo Rete (21, 22, 23, 25, 53, SMTP, DNS)
  - Personalizzate (es: 80,443,22)
  - Range (es: 1-1000)
- ⚡ **Controlli avanzati** (timeout, thread, cancellazione)
-  **Pulsanti rapidi** per reti comuni
- ⏹️ **Stop immediato** con stato preservato

### 📊 **Report Automatici al Completamento:**
- **🌐 HTML Interattivo**: Tabella con ricerca, filtri, statistiche
- **📋 Informazioni Complete**: IP, Status, Hostname, MAC, Nome Device
- **🔍 Ricerca Dinamica**: Filtra per qualsiasi campo
- **📱 Design Responsive**: Ottimizzato per desktop e mobile
- **📊 Statistiche Visive**: Contatori e percentuali automatiche

### 💻 Modalità Linea di Comando

#### Scansiona un IP singolo
```bash
python ip_scanner.py -t 192.168.1.1
```

#### Scansiona una rete intera
```bash
python ip_scanner.py -t 192.168.1.0/24
```

#### Scansiona porte specifiche
```bash
python ip_scanner.py -t 192.168.1.1 -p 80,443,22
```

#### Scansiona un range di porte
```bash
python ip_scanner.py -t 192.168.1.1 -p 1-1000
```

#### Modalità Interattiva
```bash
python ip_scanner.py
```

#### Opzioni avanzate
```bash
python ip_scanner.py -t 192.168.1.0/24 -p 80,443 --timeout 2 --threads 50
```

## 🛠️ Parametri

- `-t, --target`: IP o rete da scansionare (obbligatorio)
- `-p, --ports`: Porte da scansionare (opzionale, default: porte comuni)
- `--timeout`: Timeout in secondi (default: 1)
- `--threads`: Numero massimo di thread (default: 100)

## 📋 Esempi

### Esempio 1: Scansione veloce di un server web
```bash
python ip_scanner.py -t google.com -p 80,443
```

### Esempio 2: Scansione completa rete locale
```bash
python ip_scanner.py -t 192.168.1.0/24
```

### Esempio 3: Scansione approfondita con porte personalizzate
```bash
python ip_scanner.py -t 10.0.0.1 -p 21,22,23,80,443,3389 --timeout 3
```

## 🎯 Porte Comuni Scansionate

Per default, lo scanner verifica queste porte comuni:

| Porta | Servizio | Descrizione |
|-------|----------|-------------|
| 21    | FTP      | File Transfer Protocol |
| 22    | SSH      | Secure Shell |
| 23    | Telnet   | Telnet |
| 25    | SMTP     | Simple Mail Transfer |
| 53    | DNS      | Domain Name System |
| 80    | HTTP     | Web Server |
| 443   | HTTPS    | Web Server Sicuro |
| 3389  | RDP      | Remote Desktop |
| 3306  | MySQL    | Database MySQL |
| 5900  | VNC      | Virtual Network Computing |

## 📁 Struttura File

```
IP-Scanner/
├── ip_scanner.py          # Programma principale CLI
├── gui_scanner.py         # Interfaccia grafica principale
├── run_gui.py             # Launcher GUI
├── report_manager.py      # Sistema report avanzati
├── config.py              # File di configurazione
├── esempi.py              # Esempi di utilizzo CLI
├── esempi_report.py       # Esempi report avanzati
├── start_gui.bat          # Script Windows avvio
├── requirements.txt       # Dipendenze Python
├── README.md              # Questo file
├── GUI_GUIDE.md           # Guida interfaccia grafica
├── REPORTS_GUIDE.md       # Guida report avanzati
├── SECURITY.md            # Guida sicurezza
├── FAQ.md                 # Domande frequenti
├── .gitignore             # File Git ignore
└── LICENSE               # Licenza
```

## 🔧 Personalizzazione

Puoi modificare il file `config.py` per personalizzare:

- Porte comuni da scansionare
- Timeout di default
- Numero massimo di thread
- Liste di porte specifiche per servizi

## ⚡ Performance

- **Thread multipli**: Fino a 100 thread simultanei per scansioni veloci
- **Timeout ottimizzato**: 1 secondo di default per bilanciare velocità e accuratezza
- **Scansioni intelligenti**: Verifica prima se l'host è attivo
- **GUI reattiva**: Aggiornamenti in tempo reale senza blocchi

## 🎨 Screenshot GUI

L'interfaccia grafica include:
- 🌙 **Tema scuro** moderno e professionale
- 📊 **Dashboard** con statistiche in tempo reale
- ⚙️ **Pannello configurazione** facile da usare
- 📈 **Progress bar** con indicatori di stato
- 💾 **Esportazione** risultati con un click
- 🎯 **Modalità porte** preconfigurate per uso specifico

## 🚨 Note Importanti

- **Uso responsabile**: Usa questo strumento solo su reti di tua proprietà o con autorizzazione
- **Firewall**: Alcuni firewall potrebbero bloccare o rallentare le scansioni
- **Performance**: Su reti grandi, considera di aumentare il timeout o ridurre i thread
- **Sicurezza**: Leggi `SECURITY.md` per le best practice

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## 👨‍💻 Autore

- **Gecky2102** - [GitHub Profile](https://github.com/Gecky2102)

## 🆘 Supporto

Se hai problemi o domande:

1. Controlla gli esempi in `esempi.py`
2. Leggi la documentazione completa in `FAQ.md`
3. Consulta la guida sicurezza in `SECURITY.md`
4. Apri una issue su GitHub

---

**Buona scansione! 🔍✨**

## 📖 Utilizzo

### Modalità Interattiva

Esegui il programma senza parametri per la modalità interattiva:

```bash
python ip_scanner.py
```

### Modalità Linea di Comando

#### Scansiona un IP singolo
```bash
python ip_scanner.py -t 192.168.1.1
```

#### Scansiona una rete intera
```bash
python ip_scanner.py -t 192.168.1.0/24
```

#### Scansiona porte specifiche
```bash
python ip_scanner.py -t 192.168.1.1 -p 80,443,22
```

#### Scansiona un range di porte
```bash
python ip_scanner.py -t 192.168.1.1 -p 1-1000
```

#### Opzioni avanzate
```bash
python ip_scanner.py -t 192.168.1.0/24 -p 80,443 --timeout 2 --threads 50
```

## 🛠️ Parametri

- `-t, --target`: IP o rete da scansionare (obbligatorio)
- `-p, --ports`: Porte da scansionare (opzionale, default: porte comuni)
- `--timeout`: Timeout in secondi (default: 1)
- `--threads`: Numero massimo di thread (default: 100)

## 📋 Esempi

### Esempio 1: Scansione veloce di un server web
```bash
python ip_scanner.py -t google.com -p 80,443
```

### Esempio 2: Scansione completa rete locale
```bash
python ip_scanner.py -t 192.168.1.0/24
```

### Esempio 3: Scansione approfondita con porte personalizzate
```bash
python ip_scanner.py -t 10.0.0.1 -p 21,22,23,80,443,3389 --timeout 3
```

## 🎯 Porte Comuni Scansionate

Per default, lo scanner verifica queste porte comuni:

| Porta | Servizio | Descrizione |
|-------|----------|-------------|
| 21    | FTP      | File Transfer Protocol |
| 22    | SSH      | Secure Shell |
| 23    | Telnet   | Telnet |
| 25    | SMTP     | Simple Mail Transfer |
| 53    | DNS      | Domain Name System |
| 80    | HTTP     | Web Server |
| 443   | HTTPS    | Web Server Sicuro |
| 3389  | RDP      | Remote Desktop |
| 3306  | MySQL    | Database MySQL |
| 5900  | VNC      | Virtual Network Computing |

## 📁 Struttura File

```
IP-Scanner/
├── ip_scanner.py      # Programma principale
├── config.py          # File di configurazione
├── esempi.py          # Esempi di utilizzo
├── requirements.txt   # Dipendenze (vuoto, usa librerie standard)
├── README.md          # Questo file
└── LICENSE           # Licenza
```

## 🔧 Personalizzazione

Puoi modificare il file `config.py` per personalizzare:

- Porte comuni da scansionare
- Timeout di default
- Numero massimo di thread
- Liste di porte specifiche per servizi

## ⚡ Performance

- **Thread multipli**: Fino a 100 thread simultanei per scansioni veloci
- **Timeout ottimizzato**: 1 secondo di default per bilanciare velocità e accuratezza
- **Scansioni intelligenti**: Verifica prima se l'host è attivo

## 🚨 Note Importanti

- **Uso responsabile**: Usa questo strumento solo su reti di tua proprietà o con autorizzazione
- **Firewall**: Alcuni firewall potrebbero bloccare o rallentare le scansioni
- **Performance**: Su reti grandi, considera di aumentare il timeout o ridurre i thread

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## 👨‍💻 Autore

- **Gecky2102** - [GitHub Profile](https://github.com/Gecky2102)

## 🆘 Supporto

Se hai problemi o domande:

1. Controlla gli esempi in `esempi.py`
2. Leggi la documentazione completa
3. Apri una issue su GitHub

---

**Buona scansione! 🔍✨**
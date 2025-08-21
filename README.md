# 🔍 IP Scanner

Un potente scansionatore di rete e porte scritto in Python con interfaccia completamente in italiano.

## ✨ Caratteristiche

- 🎯 **Scansione IP singoli** - Verifica se un host è attivo e scansiona le porte
- 🌐 **Scansione reti intere** - Scansiona automaticamente tutti gli host in una rete
- 🔓 **Scansione porte personalizzate** - Definisci le porte da scansionare
- 📊 **Range di porte** - Scansiona un intervallo di porte (es: 1-1000)
- 🏃‍♂️ **Multithreading** - Scansioni veloci con thread multipli
- 🏠 **Risoluzione hostname** - Ottiene i nomi host degli IP scansionati
- 📋 **Identificazione servizi** - Riconosce i servizi comuni sulle porte
- 💬 **Interfaccia italiana** - Tutti i messaggi e l'interfaccia in italiano

## 🚀 Installazione

1. Clona il repository:
```bash
git clone https://github.com/Gecky2102/IP-Scanner.git
cd IP-Scanner
```

2. Il progetto usa solo librerie standard di Python, non servono dipendenze aggiuntive!

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
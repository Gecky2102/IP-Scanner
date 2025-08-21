# ❓ FAQ e Risoluzione Problemi

## 🔧 Problemi Comuni

### ❌ "Host non raggiungibile" su IP validi

**Possibili cause:**
- Firewall che blocca le connessioni
- Host effettivamente spento
- Rete non raggiungibile
- Timeout troppo basso

**Soluzioni:**
```bash
# Aumenta il timeout
python ip_scanner.py -t 192.168.1.1 --timeout 5

# Prova con porte specifiche
python ip_scanner.py -t 192.168.1.1 -p 80,443,22
```

### 🐌 Scansioni molto lente

**Cause:**
- Troppi thread
- Timeout troppo alto
- Rete congestionata

**Soluzioni:**
```bash
# Riduci i thread
python ip_scanner.py -t 192.168.1.0/24 --threads 20

# Riduci il timeout
python ip_scanner.py -t 192.168.1.0/24 --timeout 1
```

### 🚫 Nessuna porta aperta trovata

**Possibili cause:**
- Firewall che blocca le porte
- Servizi effettivamente non attivi
- Scansione delle porte sbagliate

**Soluzioni:**
```bash
# Prova le porte più comuni
python ip_scanner.py -t 192.168.1.1 -p 80,443,22,21,25,53

# Scansiona un range più ampio
python ip_scanner.py -t 192.168.1.1 -p 1-1000
```

## 💡 Domande Frequenti

### Q: Posso scansionare qualsiasi IP su Internet?
**A:** ❌ **NO!** Puoi scansionare solo:
- I tuoi dispositivi e reti
- Sistemi per cui hai autorizzazione scritta
- Ambienti di test isolati

### Q: È normale che alcune scansioni siano lente?
**A:** ✅ Sì, dipende da:
- Dimensione della rete
- Numero di porte da scansionare
- Velocità della rete
- Configurazione firewall

### Q: Perché non vedo l'hostname di alcuni IP?
**A:** È normale, può dipendere da:
- DNS inverso non configurato
- Firewall che blocca query DNS
- IP che non hanno hostname associato

### Q: Posso usare questo strumento in azienda?
**A:** ⚠️ Solo con autorizzazione del team IT e rispettando le policy aziendali.

### Q: Come faccio a scansionare solo porte web?
**A:** 
```bash
python ip_scanner.py -t 192.168.1.1 -p 80,443,8080,8443
```

### Q: È possibile salvare i risultati in un file?
**A:** Attualmente no, ma puoi redirigere l'output:
```bash
python ip_scanner.py -t 192.168.1.1 > risultati.txt
```

## 🔍 Diagnostica Avanzata

### Test di connettività base
```bash
# Test ping (se disponibile)
ping 192.168.1.1

# Test con telnet (se disponibile)
telnet 192.168.1.1 80
```

### Verifica configurazione rete
```python
# Script di test rapido
python -c "import socket; print(socket.gethostbyname('google.com'))"
```

### Debug modalità verbose
Per avere più informazioni, modifica temporaneamente il codice aggiungendo print di debug:

```python
# In ip_scanner.py, aggiungi nella funzione scansiona_porta:
print(f"Debug: Testando {ip}:{porta}")
```

## 🛠️ Ottimizzazione Performance

### Per reti piccole (< 50 host):
```bash
python ip_scanner.py -t 192.168.1.0/26 --threads 50 --timeout 1
```

### Per reti medie (50-200 host):
```bash
python ip_scanner.py -t 192.168.1.0/24 --threads 30 --timeout 2
```

### Per reti grandi (> 200 host):
```bash
python ip_scanner.py -t 10.0.0.0/24 --threads 20 --timeout 3
```

## 🔧 Personalizzazioni Avanzate

### Aggiungere nuove porte al file config.py:
```python
# Nel file config.py
PORTE_PERSONALIZZATE = [8080, 9000, 9090, 3000, 5000]
```

### Modificare timeout per servizi specifici:
```python
# Timeout diversi per servizi diversi
TIMEOUT_WEB = 2      # Per porte web
TIMEOUT_DB = 5       # Per database
TIMEOUT_SSH = 3      # Per SSH
```

## 📊 Interpretazione Risultati

### Porte Aperte vs Chiuse:
- ✅ **Aperta**: Il servizio risponde alla connessione
- ❌ **Chiusa/Filtrata**: Nessuna risposta o connessione rifiutata

### Stati possibili:
- **Host attivo**: Almeno una porta risponde
- **Host non raggiungibile**: Nessuna risposta su nessuna porta testata
- **Porte aperte**: Servizi attivi e raggiungibili

## 🆘 Quando Contattare il Supporto

Apri una issue su GitHub se:
- L'applicazione va in crash con errori Python
- Comportamenti inaspettati persistenti
- Suggerimenti per nuove funzionalità
- Bug confermati e riproducibili

**Include sempre:**
- Versione Python usata
- Sistema operativo
- Comando esatto eseguito
- Output completo dell'errore

## 🔄 Aggiornamenti

Per aggiornare il tool:
```bash
git pull origin main
```

Controlla sempre il changelog per nuove funzionalità o modifiche importanti.

---

**Non trovi la risposta? Apri una issue su GitHub! 🚀**

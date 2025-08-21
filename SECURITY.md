# 🛡️ Guida alla Sicurezza e Best Practices

## ⚠️ IMPORTANTE: Uso Responsabile

Questo strumento deve essere utilizzato **SOLO** in conformità con le leggi locali e internazionali. L'uso improprio può essere illegale.

## ✅ Usi Consentiti

- **Reti proprie**: Scansiona solo reti di tua proprietà
- **Test autorizzati**: Con esplicita autorizzazione scritta del proprietario
- **Penetration testing**: In ambiente controllato e autorizzato
- **Sicurezza aziendale**: Per audit di sicurezza interni
- **Ricerca educativa**: In ambienti di laboratorio isolati

## ❌ Usi Vietati

- **Reti altrui**: Scansionare reti senza autorizzazione
- **Ricognizione**: Raccogliere informazioni per attacchi
- **Violazione privacy**: Accedere a sistemi non autorizzati
- **Disturbo servizi**: Causare denial of service o rallentamenti

## 🔒 Best Practices di Sicurezza

### 1. **Autorizzazioni**
```bash
# ✅ GIUSTO: Testa la tua rete locale
python ip_scanner.py -t 192.168.1.0/24

# ❌ SBAGLIATO: Scansionare reti esterne senza permesso
python ip_scanner.py -t 1.1.1.0/24
```

### 2. **Controllo del Traffico**
- Usa timeout ragionevoli (`--timeout 2` o superiore)
- Limita i thread per reti grandi (`--threads 20`)
- Evita scansioni massive su Internet

### 3. **Documentazione**
- Mantieni log delle scansioni autorizzate
- Documenta lo scopo dei test
- Conserva le autorizzazioni scritte

### 4. **Rispetto delle Risorse**
```bash
# Per reti grandi, usa parametri conservativi
python ip_scanner.py -t 10.0.0.0/24 --timeout 3 --threads 20
```

## 🚨 Avvertenze Legali

### Italia
- **Codice Penale Art. 615-ter**: Accesso abusivo a sistema informatico
- **Codice Penale Art. 635-bis**: Danneggiamento di sistemi informatici
- **GDPR**: Rispetto della privacy e protezione dati

### Responsabilità
L'utente è **completamente responsabile** dell'uso di questo strumento. Gli autori non si assumono responsabilità per:
- Uso improprio o illegale
- Danni causati a sistemi terzi
- Violazioni di leggi locali o internazionali

## 🛠️ Configurazioni Sicure

### Scansioni Conservative
```python
# Configurazione per uso sicuro
scanner = IPScanner()
scanner.timeout = 3        # Timeout più alto
scanner.thread_max = 20    # Meno thread
```

### Test su Laboratorio
```bash
# Configura un ambiente di test isolato
# Usa macchine virtuali o container Docker
# Testa solo su 127.0.0.1 o reti locali isolate
```

## 📋 Checklist Prima della Scansione

- [ ] Ho l'autorizzazione per scansionare questo target?
- [ ] La scansione è su una mia rete o ambiente controllato?
- [ ] Ho verificato le leggi locali applicabili?
- [ ] Sto usando parametri conservativi (timeout, thread)?
- [ ] Ho documentato lo scopo del test?

## 🆘 In Caso di Problemi

### Se ricevi reclami:
1. **Ferma immediatamente** qualsiasi scansione
2. **Documenta** che era autorizzata (se vero)
3. **Contatta** un legale se necessario
4. **Collabora** con le autorità se richiesto

### Se noti attività sospette:
1. **Non investigare** oltre
2. **Segnala** alle autorità competenti
3. **Documenta** ciò che hai osservato

## 📚 Risorse Aggiuntive

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Penetration Testing Execution Standard](http://www.pentest-standard.org/)

## 🤝 Contributi Responsabili

Se contribuisci al progetto:
- Assicurati che il codice non faciliti usi impropri
- Aggiungi controlli di sicurezza dove possibile
- Migliora la documentazione sulla sicurezza

---

**Ricorda: Con grandi poteri derivano grandi responsabilità! 🕷️**

**Usa questo strumento in modo etico e responsabile.**

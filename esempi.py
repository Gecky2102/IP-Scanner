#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempi di utilizzo dell'IP Scanner
"""

from ip_scanner import IPScanner

def esempio_scansione_singola():
    """Esempio di scansione di un singolo IP"""
    print("=== ESEMPIO: Scansione IP Singolo ===")
    scanner = IPScanner()
    risultato = scanner.scansiona_host("8.8.8.8")  # Google DNS
    return risultato

def esempio_scansione_rete_locale():
    """Esempio di scansione rete locale"""
    print("=== ESEMPIO: Scansione Rete Locale ===")
    scanner = IPScanner()
    # ATTENZIONE: Modifica con la tua rete locale
    risultati = scanner.scansiona_rete("192.168.1.0/24")
    return risultati

def esempio_scansione_porte_personalizzate():
    """Esempio di scansione con porte personalizzate"""
    print("=== ESEMPIO: Porte Personalizzate ===")
    scanner = IPScanner()
    porte_web = [80, 443, 8080, 8443]
    risultato = scanner.scansiona_host("google.com", porte_web)
    return risultato

def esempio_scansione_range_porte():
    """Esempio di scansione range di porte"""
    print("=== ESEMPIO: Range di Porte ===")
    scanner = IPScanner()
    # Scansiona porte da 20 a 100 su localhost
    scanner.scansiona_porta_singola("127.0.0.1", 20, 100)

if __name__ == "__main__":
    print("🔍 ESEMPI DI UTILIZZO IP SCANNER")
    print("=" * 50)
    
    # Esegui gli esempi
    try:
        esempio_scansione_singola()
        print("\n" + "-" * 50 + "\n")
        
        esempio_scansione_porte_personalizzate()
        print("\n" + "-" * 50 + "\n")
        
        esempio_scansione_range_porte()
        print("\n" + "-" * 50 + "\n")
        
        # Decommentare per testare la rete locale
        # esempio_scansione_rete_locale()
        
    except KeyboardInterrupt:
        print("\n👋 Esempi interrotti dall'utente")
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione degli esempi: {e}")

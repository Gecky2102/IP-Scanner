#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher per IP Scanner GUI
Avvia l'interfaccia grafica moderna
"""

import sys
import os

def main():
    """Avvia l'interfaccia grafica"""
    print("🚀 Avvio IP Scanner GUI...")
    print("=" * 50)
    
    try:
        # Importa e avvia l'interfaccia
        from gui_scanner import IPScannerGUI
        
        print("✅ Moduli caricati correttamente")
        print("🎨 Inizializzazione interfaccia grafica...")
        
        app = IPScannerGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Errore importazione moduli: {e}")
        print("\n💡 Installa le dipendenze con:")
        print("pip install customtkinter pillow")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Errore nell'avvio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

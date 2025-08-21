#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio di utilizzo del Report Manager
Dimostra come generare report avanzati con MAC address e nomi dispositivi
"""

from report_manager import ReportManager
import time

def esempio_report_completo():
    """Esempio di generazione report completo"""
    print("📊 ESEMPIO: Generazione Report Completo")
    print("=" * 50)
    
    # Crea il report manager
    rm = ReportManager()
    
    # Simula alcuni risultati di scansione
    print("🔍 Simulazione risultati scansione...")
    
    # Aggiungi alcuni host di esempio
    esempio_hosts = [
        ("192.168.1.1", True, "router.local", [80, 443, 22]),
        ("192.168.1.100", True, "pc-giacomo", [135, 139, 445]),
        ("192.168.1.101", True, "smartphone-android", []),
        ("192.168.1.50", False, None, []),
        ("192.168.1.200", True, "printer-hp", [80, 631, 9100]),
    ]
    
    for ip, attivo, hostname, porte in esempio_hosts:
        print(f"  📋 Aggiungendo {ip}...")
        
        # Per host attivi, prova a ottenere MAC e nome dispositivo
        if attivo:
            print(f"    🔍 Raccolta info rete per {ip}...")
            mac = rm.get_mac_address(ip, timeout=1)
            device_name = rm.get_device_name(ip, mac)
        else:
            mac = None
            device_name = None
            
        rm.add_result(
            ip=ip,
            active=attivo,
            hostname=hostname,
            open_ports=porte,
            mac_address=mac,
            device_name=device_name
        )
    
    # Imposta metadati scansione
    rm.set_scan_metadata(
        target="192.168.1.0/24",
        total_scanned=254,
        duration=45.2,
        ports_mode="comuni"
    )
    
    print("\n📄 Generazione report in tutti i formati...")
    
    # Genera tutti i formati
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_filename = f"esempio_report_{timestamp}"
    
    results = rm.export_all_formats(base_filename)
    
    print("\n✅ Report generati:")
    for fmt, result in results.items():
        status = "✅" if result['success'] else "❌"
        print(f"  {status} {fmt.upper()}: {result['filename']}")
    
    # Apri report HTML
    html_result = results.get('html')
    if html_result and html_result['success']:
        print(f"\n🌐 Apertura report HTML: {html_result['filename']}")
        rm.open_html_report(html_result['filename'])
    
    return results

def esempio_mac_detection():
    """Esempio di rilevamento MAC address"""
    print("\n🔧 ESEMPIO: Rilevamento MAC Address")
    print("=" * 50)
    
    rm = ReportManager()
    
    # Test su alcuni IP comuni
    test_ips = ["127.0.0.1", "192.168.1.1", "8.8.8.8"]
    
    for ip in test_ips:
        print(f"\n🔍 Test MAC per {ip}:")
        mac = rm.get_mac_address(ip, timeout=2)
        device_name = rm.get_device_name(ip, mac)
        
        print(f"  🔧 MAC: {mac if mac else 'Non trovato'}")
        print(f"  💻 Dispositivo: {device_name if device_name != 'N/A' else 'Non identificato'}")

def esempio_html_personalizzato():
    """Esempio di report HTML personalizzato"""
    print("\n🌐 ESEMPIO: Report HTML Personalizzato")
    print("=" * 50)
    
    rm = ReportManager()
    
    # Aggiungi dati di esempio
    rm.add_result("192.168.1.1", True, "Gateway", [80, 443], "aa:bb:cc:dd:ee:ff", "Router TP-Link")
    rm.add_result("192.168.1.100", True, "PC-Desktop", [135, 445], "11:22:33:44:55:66", "Windows Desktop")
    rm.add_result("192.168.1.50", False, None, [], None, None)
    
    rm.set_scan_metadata("192.168.1.0/24", 3, 12.5, "comuni")
    
    filename = f"report_personalizzato_{time.strftime('%Y%m%d_%H%M%S')}.html"
    
    if rm.generate_html_report(filename):
        print(f"✅ Report HTML generato: {filename}")
        print("🌐 Apertura nel browser...")
        rm.open_html_report(filename)
    else:
        print("❌ Errore nella generazione del report")

if __name__ == "__main__":
    print("🚀 ESEMPI REPORT MANAGER")
    print("=" * 60)
    
    try:
        # Esegui gli esempi
        risultati = esempio_report_completo()
        esempio_mac_detection()
        esempio_html_personalizzato()
        
        print("\n" + "=" * 60)
        print("✅ Tutti gli esempi completati con successo!")
        print("\n💡 Controlla i file generati nella directory corrente.")
        
    except KeyboardInterrupt:
        print("\n👋 Esempi interrotti dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")
        import traceback
        traceback.print_exc()

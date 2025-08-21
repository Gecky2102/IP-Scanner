#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP Scanner - Scansionatore di rete e porte
Creato per scansionare indirizzi IP e porte aperte in una rete
"""

import socket
import threading
import ipaddress
import sys
import time
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class IPScanner:
    def __init__(self):
        self.porte_comuni = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
        self.timeout = 1
        self.thread_max = 100
        
    def stampa_banner(self):
        """Stampa il banner dell'applicazione"""
        print("=" * 60)
        print("🔍 IP SCANNER - Scansionatore di Rete")
        print("=" * 60)
        print("Versione: 1.0")
        print("Autore: IP-Scanner")
        print("Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("=" * 60)
        print()

    def verifica_host_attivo(self, ip):
        """Verifica se un host è attivo tramite ping socket"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            # Prova a connettersi alla porta 80 o 443
            for porta in [80, 443, 22, 21]:
                try:
                    risultato = sock.connect_ex((str(ip), porta))
                    if risultato == 0:
                        sock.close()
                        return True
                except:
                    continue
            sock.close()
            return False
        except:
            return False

    def scansiona_porta(self, ip, porta):
        """Scansiona una singola porta su un IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            risultato = sock.connect_ex((str(ip), porta))
            sock.close()
            
            if risultato == 0:
                return porta
            return None
        except:
            return None

    def ottieni_info_servizio(self, porta):
        """Restituisce informazioni sul servizio della porta"""
        servizi = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            135: "RPC",
            139: "NetBIOS",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            1723: "PPTP",
            3306: "MySQL",
            3389: "RDP",
            5900: "VNC",
            8080: "HTTP-Alt"
        }
        return servizi.get(porta, "Sconosciuto")

    def risolvi_hostname(self, ip):
        """Tenta di risolvere l'hostname dell'IP"""
        try:
            hostname = socket.gethostbyaddr(str(ip))[0]
            return hostname
        except:
            return "N/A"

    def scansiona_host(self, ip, porte_personalizzate=None):
        """Scansiona un singolo host per porte aperte"""
        porte_da_scansionare = porte_personalizzate if porte_personalizzate else self.porte_comuni
        porte_aperte = []
        
        print(f"🔍 Scansionando {ip}...", end=" ")
        
        # Verifica se l'host è attivo
        if not self.verifica_host_attivo(ip):
            print("❌ Host non raggiungibile")
            return None
            
        hostname = self.risolvi_hostname(ip)
        print(f"✅ Host attivo (Hostname: {hostname})")
        
        # Scansiona le porte
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_porta = {executor.submit(self.scansiona_porta, ip, porta): porta 
                             for porta in porte_da_scansionare}
            
            for future in as_completed(future_to_porta):
                porta_risultato = future.result()
                if porta_risultato:
                    porte_aperte.append(porta_risultato)
        
        if porte_aperte:
            porte_aperte.sort()
            print(f"  📋 Porte aperte trovate: {len(porte_aperte)}")
            for porta in porte_aperte:
                servizio = self.ottieni_info_servizio(porta)
                print(f"    ▶ Porta {porta}: {servizio}")
        else:
            print("  ⚠️  Nessuna porta aperta trovata")
            
        return {
            'ip': str(ip),
            'hostname': hostname,
            'porte_aperte': porte_aperte,
            'attivo': True
        }

    def scansiona_rete(self, rete, porte_personalizzate=None):
        """Scansiona una intera rete"""
        try:
            network = ipaddress.ip_network(rete, strict=False)
            print(f"🌐 Iniziando scansione della rete: {network}")
            print(f"📊 Numero totale di host da scansionare: {network.num_addresses}")
            print("-" * 60)
            
            host_attivi = []
            inizio_tempo = time.time()
            
            with ThreadPoolExecutor(max_workers=self.thread_max) as executor:
                future_to_ip = {executor.submit(self.scansiona_host, ip, porte_personalizzate): ip 
                              for ip in network.hosts()}
                
                for future in as_completed(future_to_ip):
                    risultato = future.result()
                    if risultato:
                        host_attivi.append(risultato)
            
            fine_tempo = time.time()
            tempo_totale = fine_tempo - inizio_tempo
            
            # Stampa riassunto
            print("\n" + "=" * 60)
            print("📈 RISULTATI SCANSIONE")
            print("=" * 60)
            print(f"⏱️  Tempo totale: {tempo_totale:.2f} secondi")
            print(f"🎯 Host attivi trovati: {len(host_attivi)}")
            print(f"📡 Host totali scansionati: {network.num_addresses}")
            print(f"📊 Percentuale host attivi: {(len(host_attivi)/network.num_addresses)*100:.2f}%")
            
            if host_attivi:
                print("\n📋 DETTAGLI HOST ATTIVI:")
                print("-" * 60)
                for host in host_attivi:
                    print(f"🖥️  IP: {host['ip']} | Hostname: {host['hostname']}")
                    if host['porte_aperte']:
                        porte_str = ", ".join([f"{p}({self.ottieni_info_servizio(p)})" 
                                             for p in host['porte_aperte']])
                        print(f"   🔓 Porte: {porte_str}")
                    print()
            
            return host_attivi
            
        except ValueError as e:
            print(f"❌ Errore: Formato rete non valido - {e}")
            return []

    def scansiona_porta_singola(self, ip, porta_iniziale, porta_finale=None):
        """Scansiona un range di porte su un singolo IP"""
        if porta_finale is None:
            porta_finale = porta_iniziale
            
        print(f"🔍 Scansionando porte {porta_iniziale}-{porta_finale} su {ip}")
        
        if not self.verifica_host_attivo(ip):
            print("❌ Host non raggiungibile")
            return
            
        hostname = self.risolvi_hostname(ip)
        print(f"✅ Host attivo (Hostname: {hostname})")
        
        porte_aperte = []
        porte_totali = porta_finale - porta_iniziale + 1
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_porta = {executor.submit(self.scansiona_porta, ip, porta): porta 
                             for porta in range(porta_iniziale, porta_finale + 1)}
            
            completate = 0
            for future in as_completed(future_to_porta):
                porta_risultato = future.result()
                completate += 1
                
                if completate % 100 == 0 or completate == porte_totali:
                    progresso = (completate / porte_totali) * 100
                    print(f"📊 Progresso: {progresso:.1f}% ({completate}/{porte_totali})")
                
                if porta_risultato:
                    porte_aperte.append(porta_risultato)
        
        print(f"\n📋 Scansione completata!")
        print(f"🎯 Porte aperte trovate: {len(porte_aperte)}")
        
        if porte_aperte:
            porte_aperte.sort()
            print("\n🔓 PORTE APERTE:")
            for porta in porte_aperte:
                servizio = self.ottieni_info_servizio(porta)
                print(f"  ▶ Porta {porta}: {servizio}")


def main():
    scanner = IPScanner()
    scanner.stampa_banner()
    
    parser = argparse.ArgumentParser(description='IP Scanner - Scansionatore di rete e porte')
    parser.add_argument('-t', '--target', help='IP o rete da scansionare (es: 192.168.1.1 o 192.168.1.0/24)')
    parser.add_argument('-p', '--ports', help='Porte da scansionare (es: 80,443 o 1-1000)')
    parser.add_argument('--timeout', type=int, default=1, help='Timeout in secondi (default: 1)')
    parser.add_argument('--threads', type=int, default=100, help='Numero massimo di thread (default: 100)')
    
    args = parser.parse_args()
    
    # Configura scanner
    if args.timeout:
        scanner.timeout = args.timeout
    if args.threads:
        scanner.thread_max = args.threads
    
    # Modalità interattiva se non ci sono argomenti
    if not args.target:
        print("🎯 MODALITÀ INTERATTIVA")
        print("\nScegli un'opzione:")
        print("1. Scansiona un singolo IP")
        print("2. Scansiona una rete")
        print("3. Scansiona porte specifiche su un IP")
        print("4. Esci")
        
        while True:
            try:
                scelta = input("\nInserisci la tua scelta (1-4): ").strip()
                
                if scelta == "1":
                    ip = input("Inserisci l'IP da scansionare: ").strip()
                    try:
                        ipaddress.ip_address(ip)
                        scanner.scansiona_host(ip)
                    except ValueError:
                        print("❌ IP non valido!")
                
                elif scelta == "2":
                    rete = input("Inserisci la rete da scansionare (es: 192.168.1.0/24): ").strip()
                    scanner.scansiona_rete(rete)
                
                elif scelta == "3":
                    ip = input("Inserisci l'IP: ").strip()
                    porta_input = input("Inserisci le porte (es: 80,443 o 1-1000): ").strip()
                    
                    try:
                        ipaddress.ip_address(ip)
                        
                        if "-" in porta_input:
                            inizio, fine = map(int, porta_input.split("-"))
                            scanner.scansiona_porta_singola(ip, inizio, fine)
                        elif "," in porta_input:
                            porte = [int(p.strip()) for p in porta_input.split(",")]
                            scanner.scansiona_host(ip, porte)
                        else:
                            porta = int(porta_input)
                            scanner.scansiona_porta_singola(ip, porta)
                    except ValueError:
                        print("❌ IP o formato porte non valido!")
                
                elif scelta == "4":
                    print("👋 Arrivederci!")
                    break
                
                else:
                    print("❌ Scelta non valida!")
                    
            except KeyboardInterrupt:
                print("\n👋 Arrivederci!")
                break
    
    else:
        # Modalità da linea di comando
        porte_personalizzate = None
        if args.ports:
            if "-" in args.ports:
                inizio, fine = map(int, args.ports.split("-"))
                porte_personalizzate = list(range(inizio, fine + 1))
            elif "," in args.ports:
                porte_personalizzate = [int(p.strip()) for p in args.ports.split(",")]
            else:
                porte_personalizzate = [int(args.ports)]
        
        try:
            # Verifica se è un IP singolo o una rete
            if "/" in args.target:
                scanner.scansiona_rete(args.target, porte_personalizzate)
            else:
                ipaddress.ip_address(args.target)
                scanner.scansiona_host(args.target, porte_personalizzate)
        except ValueError:
            print(f"❌ Target non valido: {args.target}")


if __name__ == "__main__":
    main()

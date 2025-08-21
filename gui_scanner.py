#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP Scanner GUI - Interfaccia Grafica per IP Scanner
Interfaccia moderna con tema scuro usando CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import ipaddress
import json
from datetime import datetime
import sys
import os
import socket
import time
import psutil

# Importa il motore di scansione
from ip_scanner import IPScanner
from config import PORTE_COMUNI, WEB_PORTS, DB_PORTS, NETWORK_PORTS
from report_manager import ReportManager

# Configura il tema scuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IPScannerGUI:
    def __init__(self):
        # Finestra principale
        self.root = ctk.CTk()
        self.root.title("🔍 IP Scanner - Scansionatore di Rete")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Icona (se disponibile)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Scanner engine
        self.scanner = IPScanner()
        self.scan_running = False
        self.current_scan_thread = None
        
        # Report manager
        self.report_manager = ReportManager()
        
        # Variabili per tracking progresso
        self.start_time = None
        self.hosts_completed = 0
        self.total_hosts = 0
        self.hosts_found = 0
        self.total_ports_found = 0
        
        # Variabili UI
        self.target_var = ctk.StringVar()
        self.timeout_var = ctk.StringVar(value="1")
        self.threads_var = ctk.StringVar(value="100")
        self.port_mode_var = ctk.StringVar(value="comuni")
        self.custom_ports_var = ctk.StringVar()
        
        # Rileva automaticamente la rete locale
        self.auto_detect_network()
        
        # Risultati
        self.scan_results = []
        
        self.setup_ui()
        self.setup_styles()
        
    def auto_detect_network(self):
        """Rileva automaticamente la rete locale"""
        try:
            # Ottieni l'IP locale e calcola la rete
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Se è localhost, prova con le interfacce di rete
            if local_ip.startswith('127.'):
                for interface_name, interface_addresses in psutil.net_if_addrs().items():
                    for address in interface_addresses:
                        if address.family == socket.AF_INET and not address.address.startswith('127.'):
                            local_ip = address.address
                            break
                    if not local_ip.startswith('127.'):
                        break
            
            # Calcola la rete /24
            ip_obj = ipaddress.IPv4Address(local_ip)
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            
            # Imposta il target automaticamente
            self.target_var.set(str(network))
            
        except Exception as e:
            # Fallback per rete comune
            self.target_var.set("192.168.1.0/24")
            print(f"Errore rilevamento rete: {e}")
            
    def get_network_info(self):
        """Ottiene informazioni dettagliate sulla rete locale"""
        info = {
            'local_ip': 'N/A',
            'gateway': 'N/A',
            'network': 'N/A',
            'interfaces': []
        }
        
        try:
            # IP locale
            hostname = socket.gethostname()
            info['local_ip'] = socket.gethostbyname(hostname)
            
            # Interfacce di rete
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                for address in interface_addresses:
                    if address.family == socket.AF_INET and not address.address.startswith('127.'):
                        info['interfaces'].append({
                            'name': interface_name,
                            'ip': address.address,
                            'netmask': address.netmask
                        })
            
            # Gateway (approssimazione)
            if info['local_ip'] != 'N/A':
                ip_parts = info['local_ip'].split('.')
                info['gateway'] = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
                info['network'] = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
                
        except Exception as e:
            print(f"Errore informazioni rete: {e}")
            
        return info
        
    def setup_styles(self):
        """Configura gli stili personalizzati"""
        # Colori personalizzati
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'accent': '#0078d4',
            'success': '#16c60c',
            'warning': '#ffb900',
            'error': '#d13438',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale con padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Contenuto principale in due colonne
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Colonna sinistra - Configurazione
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10), pady=0)
        
        # Colonna destra - Risultati
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=0)
        
        self.create_config_panel(left_frame)
        self.create_results_panel(right_frame)
        
        # Footer con stato
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Crea l'header dell'applicazione"""
        header_frame = ctk.CTkFrame(parent, height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Titolo
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🔍 IP Scanner",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        # Sottotitolo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Scansionatore di Rete Professionale",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()
        
    def create_config_panel(self, parent):
        """Crea il pannello di configurazione"""
        config_frame = ctk.CTkScrollableFrame(parent, width=400, label_text="⚙️ Configurazione Scansione")
        config_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Informazioni rete rilevata
        network_info_frame = ctk.CTkFrame(config_frame)
        network_info_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(network_info_frame, text="🌐 Informazioni Rete Rilevata", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        
        network_info = self.get_network_info()
        info_text = f"🖥️  IP Locale: {network_info['local_ip']}\n"
        info_text += f"🌍 Gateway: {network_info['gateway']}\n"
        info_text += f"📡 Rete Suggerita: {network_info['network']}"
        
        info_label = ctk.CTkLabel(
            network_info_frame, 
            text=info_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        info_label.pack(pady=(0, 10), padx=10)
        
        # Pulsante per auto-rilevamento
        auto_button = ctk.CTkButton(
            network_info_frame,
            text="🔄 Rileva Automaticamente",
            command=self.auto_detect_and_update,
            height=30
        )
        auto_button.pack(pady=(0, 10))
        
        # Target
        target_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        target_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(target_frame, text="🎯 Target:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        # Frame per target entry e pulsanti suggerimenti
        target_input_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        target_input_frame.pack(fill="x", pady=(5, 5))
        
        self.target_entry = ctk.CTkEntry(
            target_input_frame, 
            textvariable=self.target_var,
            placeholder_text="es: 192.168.1.1 o 192.168.1.0/24",
            width=300
        )
        self.target_entry.pack(fill="x")
        
        # Pulsanti suggerimenti rapidi
        suggestions_frame = ctk.CTkFrame(target_frame, fg_color="transparent")
        suggestions_frame.pack(fill="x", pady=(5, 0))
        
        quick_buttons = [
            ("🏠 Rete Casa", "192.168.1.0/24"),
            ("🏢 Rete Ufficio", "192.168.0.0/24"),
            ("🔒 Localhost", "127.0.0.1")
        ]
        
        for i, (text, value) in enumerate(quick_buttons):
            if i % 2 == 0:
                button_frame = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
                button_frame.pack(fill="x", pady=2)
            
            button = ctk.CTkButton(
                button_frame,
                text=text,
                command=lambda v=value: self.target_var.set(v),
                width=130,
                height=25
            )
            
            if i % 2 == 0:
                button.pack(side="left", padx=(0, 5))
            else:
                button.pack(side="right", padx=(5, 0))
        
        # Modalità porte (resto del codice rimane uguale)
        ports_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        ports_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(ports_frame, text="🔓 Modalità Porte:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        port_options = [
            ("Porte Comuni", "comuni"),
            ("Solo Web", "web"),
            ("Solo Database", "database"),
            ("Solo Rete", "rete"),
            ("Personalizzate", "custom"),
            ("Range", "range")
        ]
        
        for text, value in port_options:
            radio = ctk.CTkRadioButton(
                ports_frame,
                text=text,
                variable=self.port_mode_var,
                value=value,
                command=self.on_port_mode_change
            )
            radio.pack(anchor="w", pady=2)
        
        # Porte personalizzate
        self.custom_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        self.custom_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(self.custom_frame, text="📝 Porte/Range:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.custom_entry = ctk.CTkEntry(
            self.custom_frame,
            textvariable=self.custom_ports_var,
            placeholder_text="es: 80,443,22 o 1-1000",
            width=300,
            state="disabled"
        )
        self.custom_entry.pack(fill="x", pady=(5, 0))
        
        # Parametri avanzati
        advanced_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        advanced_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(advanced_frame, text="⚡ Parametri Avanzati:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        # Timeout
        timeout_subframe = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        timeout_subframe.pack(fill="x", pady=(5, 5))
        
        ctk.CTkLabel(timeout_subframe, text="Timeout (sec):").pack(side="left")
        timeout_entry = ctk.CTkEntry(timeout_subframe, textvariable=self.timeout_var, width=80)
        timeout_entry.pack(side="right")
        
        # Thread
        thread_subframe = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        thread_subframe.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(thread_subframe, text="Thread Max:").pack(side="left")
        thread_entry = ctk.CTkEntry(thread_subframe, textvariable=self.threads_var, width=80)
        thread_entry.pack(side="right")
        
        # Pulsanti azione
        button_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        self.scan_button = ctk.CTkButton(
            button_frame,
            text="🚀 Avvia Scansione",
            command=self.start_scan,
            font=ctk.CTkFont(weight="bold"),
            height=40
        )
        self.scan_button.pack(fill="x", pady=(0, 10))
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Ferma Scansione",
            command=self.stop_scan,
            state="disabled",
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        self.stop_button.pack(fill="x", pady=(0, 10))
        
        # Pulsanti utilità
        util_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        util_frame.pack(fill="x", pady=(10, 0))
        
        # Prima riga pulsanti
        util_row1 = ctk.CTkFrame(util_frame, fg_color="transparent")
        util_row1.pack(fill="x", pady=(0, 5))
        
        export_all_button = ctk.CTkButton(
            util_row1,
            text="📊 Esporta Tutto",
            command=self.export_all_formats,
            width=120,
            fg_color="green",
            hover_color="darkgreen"
        )
        export_all_button.pack(side="left", padx=(0, 5))
        
        html_report_button = ctk.CTkButton(
            util_row1,
            text="🌐 Report HTML",
            command=self.generate_html_report,
            width=120,
            fg_color="orange",
            hover_color="darkorange"
        )
        html_report_button.pack(side="right", padx=(5, 0))
        
        # Seconda riga pulsanti
        util_row2 = ctk.CTkFrame(util_frame, fg_color="transparent")
        util_row2.pack(fill="x")
        
        save_csv_button = ctk.CTkButton(
            util_row2,
            text="📋 CSV",
            command=self.save_csv,
            width=80
        )
        save_csv_button.pack(side="left", padx=(0, 5))
        
        save_excel_button = ctk.CTkButton(
            util_row2,
            text="📊 Excel",
            command=self.save_excel,
            width=80
        )
        save_excel_button.pack(side="left", padx=(0, 5))
        
        clear_button = ctk.CTkButton(
            util_row2,
            text="🗑️ Pulisci",
            command=self.clear_results,
            width=80
        )
        clear_button.pack(side="right", padx=(5, 0))
        
    def auto_detect_and_update(self):
        """Rileva automaticamente la rete e aggiorna l'interfaccia"""
        self.auto_detect_network()
        # Aggiorna anche le informazioni mostrate
        self.refresh_network_info()
        
    def refresh_network_info(self):
        """Aggiorna le informazioni di rete nell'interfaccia"""
        # Questo metodo può essere chiamato per aggiornare dinamicamente
        # le informazioni di rete se necessario
        pass
        
    def create_results_panel(self, parent):
        """Crea il pannello dei risultati"""
        results_frame = ctk.CTkFrame(parent, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header risultati
        results_header = ctk.CTkFrame(results_frame, height=40)
        results_header.pack(fill="x", pady=(0, 10))
        results_header.pack_propagate(False)
        
        ctk.CTkLabel(
            results_header,
            text="📊 Risultati Scansione",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.results_count_label = ctk.CTkLabel(
            results_header,
            text="Host trovati: 0",
            font=ctk.CTkFont(size=14)
        )
        self.results_count_label.pack(side="right", padx=10, pady=10)
        
        # Area risultati con scrollbar
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.results_text.pack(fill="both", expand=True)
        
        # Messaggio iniziale
        self.results_text.insert("1.0", "💡 Configura i parametri di scansione e premi 'Avvia Scansione' per iniziare.\n\n")
        self.results_text.insert("end", "🎯 Esempi di target:\n")
        self.results_text.insert("end", "  • IP singolo: 192.168.1.1\n")
        self.results_text.insert("end", "  • Rete: 192.168.1.0/24\n")
        self.results_text.insert("end", "  • Hostname: google.com\n\n")
        self.results_text.insert("end", "🔓 Modalità porte:\n")
        self.results_text.insert("end", "  • Comuni: Porte più utilizzate\n")
        self.results_text.insert("end", "  • Web: 80, 443, 8080, 8443\n")
        self.results_text.insert("end", "  • Database: 3306, 5432, 1433\n")
        self.results_text.insert("end", "  • Personalizzate: 80,443,22\n")
        self.results_text.insert("end", "  • Range: 1-1000\n")
        
    def create_footer(self, parent):
        """Crea il footer con informazioni di stato"""
        footer_frame = ctk.CTkFrame(parent, height=120)
        footer_frame.pack(fill="x", pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        # Progress section
        progress_section = ctk.CTkFrame(footer_frame, fg_color="transparent")
        progress_section.pack(fill="x", padx=10, pady=5)
        
        # Progress bar con etichetta
        progress_header = ctk.CTkFrame(progress_section, fg_color="transparent")
        progress_header.pack(fill="x")
        
        self.progress_label = ctk.CTkLabel(
            progress_header,
            text="🔄 Progresso Scansione",
            font=ctk.CTkFont(weight="bold")
        )
        self.progress_label.pack(side="left")
        
        self.progress_percentage = ctk.CTkLabel(
            progress_header,
            text="0%",
            font=ctk.CTkFont(weight="bold")
        )
        self.progress_percentage.pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(progress_section)
        self.progress_bar.pack(fill="x", pady=(5, 10))
        self.progress_bar.set(0)
        
        # Statistics section
        stats_section = ctk.CTkFrame(footer_frame, fg_color="transparent")
        stats_section.pack(fill="x", padx=10, pady=(0, 5))
        
        # Prima riga statistiche
        stats_row1 = ctk.CTkFrame(stats_section, fg_color="transparent")
        stats_row1.pack(fill="x")
        
        self.hosts_stats_label = ctk.CTkLabel(
            stats_row1,
            text="🎯 Host: 0/0",
            font=ctk.CTkFont(size=12)
        )
        self.hosts_stats_label.pack(side="left")
        
        self.time_stats_label = ctk.CTkLabel(
            stats_row1,
            text="⏱️ Tempo: 00:00",
            font=ctk.CTkFont(size=12)
        )
        self.time_stats_label.pack(side="right")
        
        # Seconda riga statistiche
        stats_row2 = ctk.CTkFrame(stats_section, fg_color="transparent")
        stats_row2.pack(fill="x", pady=(2, 0))
        
        self.found_stats_label = ctk.CTkLabel(
            stats_row2,
            text="✅ Trovati: 0 host, 0 porte",
            font=ctk.CTkFont(size=12)
        )
        self.found_stats_label.pack(side="left")
        
        self.eta_label = ctk.CTkLabel(
            stats_row2,
            text="🕐 Tempo stimato: --",
            font=ctk.CTkFont(size=12)
        )
        self.eta_label.pack(side="right")
        
        # Status principale
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="🟢 Pronto per la scansione",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=(5, 10))
        
    def on_port_mode_change(self):
        """Gestisce il cambio di modalità porte"""
        mode = self.port_mode_var.get()
        
        if mode in ["custom", "range"]:
            self.custom_entry.configure(state="normal")
            if mode == "custom":
                self.custom_entry.configure(placeholder_text="es: 80,443,22,3306")
            else:  # range
                self.custom_entry.configure(placeholder_text="es: 1-1000")
        else:
            self.custom_entry.configure(state="disabled")
            
    def validate_input(self):
        """Valida l'input dell'utente"""
        # Verifica target
        target = self.target_var.get().strip()
        if not target:
            messagebox.showerror("Errore", "❌ Inserire un target da scansionare!")
            return False
            
        # Verifica se è un IP/rete valida
        try:
            if "/" in target:
                ipaddress.ip_network(target, strict=False)
            else:
                # Prova come IP
                try:
                    ipaddress.ip_address(target)
                except:
                    # Potrebbe essere un hostname
                    pass
        except ValueError:
            messagebox.showerror("Errore", f"❌ Target non valido: {target}")
            return False
            
        # Verifica timeout
        try:
            timeout = float(self.timeout_var.get())
            if timeout <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Errore", "❌ Timeout deve essere un numero positivo!")
            return False
            
        # Verifica thread
        try:
            threads = int(self.threads_var.get())
            if threads <= 0 or threads > 500:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Errore", "❌ Thread deve essere tra 1 e 500!")
            return False
            
        # Verifica porte personalizzate
        mode = self.port_mode_var.get()
        if mode in ["custom", "range"]:
            custom_ports = self.custom_ports_var.get().strip()
            if not custom_ports:
                messagebox.showerror("Errore", "❌ Specificare porte o range per modalità personalizzata!")
                return False
                
        return True
        
    def get_ports_to_scan(self):
        """Restituisce la lista delle porte da scansionare"""
        mode = self.port_mode_var.get()
        
        if mode == "comuni":
            return PORTE_COMUNI
        elif mode == "web":
            return WEB_PORTS
        elif mode == "database":
            return DB_PORTS
        elif mode == "rete":
            return NETWORK_PORTS
        elif mode == "custom":
            ports_str = self.custom_ports_var.get().strip()
            try:
                return [int(p.strip()) for p in ports_str.split(",")]
            except ValueError:
                raise ValueError("Formato porte non valido")
        elif mode == "range":
            range_str = self.custom_ports_var.get().strip()
            try:
                if "-" in range_str:
                    start, end = map(int, range_str.split("-"))
                    return list(range(start, end + 1))
                else:
                    return [int(range_str)]
            except ValueError:
                raise ValueError("Formato range non valido")
                
        return PORTE_COMUNI
        
    def start_scan(self):
        """Avvia la scansione"""
        if not self.validate_input():
            return
            
        # Prepara parametri
        target = self.target_var.get().strip()
        timeout = float(self.timeout_var.get())
        threads = int(self.threads_var.get())
        
        try:
            ports = self.get_ports_to_scan()
        except ValueError as e:
            messagebox.showerror("Errore", f"❌ {e}")
            return
            
        # Configura scanner
        self.scanner.timeout = timeout
        self.scanner.thread_max = threads
        
        # UI state
        self.scan_running = True
        self.scan_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)
        
        # Pulisci risultati
        self.results_text.delete("1.0", "end")
        self.scan_results = []
        
        # Avvia scansione in thread separato
        self.current_scan_thread = threading.Thread(
            target=self.run_scan,
            args=(target, ports),
            daemon=True
        )
        self.current_scan_thread.start()
        
    def run_scan(self, target, ports):
        """Esegue la scansione in background"""
        try:
            self.update_status("🔍 Inizializzazione scansione...")
            self.start_time = time.time()
            self.hosts_completed = 0
            self.hosts_found = 0
            self.total_ports_found = 0
            
            # Pulisci report precedente
            self.report_manager.clear_results()
            
            if "/" in target:
                # Scansione rete
                self.scan_network(target, ports)
            else:
                # Scansione singola
                self.total_hosts = 1
                self.update_scan_stats()
                self.scan_single_host(target, ports)
                
            end_time = time.time()
            duration = end_time - self.start_time
            
            if self.scan_running:
                self.update_status("🔍 Raccolta informazioni di rete...")
                
                # Imposta metadati scansione
                ports_mode = self.port_mode_var.get()
                self.report_manager.set_scan_metadata(target, self.total_hosts, duration, ports_mode)
                
                # Avvia raccolta informazioni di rete in background
                self.enhance_results_thread = threading.Thread(
                    target=self.enhance_results_with_network_info,
                    daemon=True
                )
                self.enhance_results_thread.start()
                
        except Exception as e:
            if self.scan_running:
                self.update_status(f"❌ Errore durante la scansione: {e}")
                self.append_result(f"❌ ERRORE: {e}\n")
        finally:
            if self.scan_running and not hasattr(self, 'enhance_results_thread'):
                self.scan_completed()
                
    def enhance_results_with_network_info(self):
        """Raccoglie informazioni di rete avanzate per tutti gli host attivi"""
        try:
            active_hosts = [r for r in self.scan_results if r['porte_aperte'] or True]  # Tutti gli host per ora
            total_active = len(active_hosts)
            
            if total_active == 0:
                self.scan_completed()
                return
                
            self.update_status(f"🔍 Raccolta MAC addresses e nomi dispositivi... (0/{total_active})")
            
            for i, host_result in enumerate(active_hosts):
                if not self.scan_running:
                    break
                    
                ip = host_result['ip']
                
                # Aggiorna status
                self.update_status(f"🔍 Analizzando {ip}... ({i+1}/{total_active})")
                
                # Ottieni MAC address
                mac_address = self.report_manager.get_mac_address(ip)
                
                # Ottieni nome dispositivo
                device_name = self.report_manager.get_device_name(ip, mac_address)
                
                # Aggiungi al report manager
                self.report_manager.add_result(
                    ip=ip,
                    active=True,
                    hostname=host_result['hostname'],
                    open_ports=host_result['porte_aperte'],
                    mac_address=mac_address,
                    device_name=device_name
                )
                
                # Aggiorna risultati nella UI
                if mac_address and mac_address != 'N/A':
                    self.append_result(f"  🔧 MAC: {mac_address}\n")
                if device_name and device_name != 'N/A':
                    self.append_result(f"  💻 Dispositivo: {device_name}\n")
                    
            # Aggiungi anche host inattivi al report
            for result in self.scan_results:
                if not result.get('porte_aperte'):  # Host probabilmente inattivo
                    self.report_manager.add_result(
                        ip=result['ip'],
                        active=False,
                        hostname=result.get('hostname', 'N/A')
                    )
            
            if self.scan_running:
                self.update_status("✅ Scansione completata! Generazione report...")
                self.show_scan_summary()
                
                # Genera automaticamente il report HTML
                self.auto_generate_final_report()
                
        except Exception as e:
            self.update_status(f"❌ Errore raccolta informazioni: {e}")
        finally:
            if self.scan_running:
                self.scan_completed()
                
    def auto_generate_final_report(self):
        """Genera automaticamente il report finale e lo apre"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"scan_report_{timestamp}.html"
            
            if self.report_manager.generate_html_report(html_filename):
                self.append_result(f"\n🌐 Report HTML generato: {html_filename}\n")
                
                # Apri automaticamente nel browser
                if self.report_manager.open_html_report(html_filename):
                    self.append_result("🌐 Report aperto nel browser!\n")
                else:
                    self.append_result("⚠️ Impossibile aprire automaticamente il report\n")
                    
                # Mostra dialog con opzioni
                self.show_export_dialog()
            else:
                self.append_result("❌ Errore nella generazione del report HTML\n")
                
        except Exception as e:
            self.append_result(f"❌ Errore generazione report: {e}\n")
                
    def scan_network(self, network, ports):
        """Scansiona una rete con aggiornamenti in tempo reale"""
        try:
            net = ipaddress.ip_network(network, strict=False)
            self.total_hosts = net.num_addresses
            
            self.append_result(f"🌐 Scansione rete: {network}\n")
            self.append_result(f"📊 Host totali da scansionare: {self.total_hosts}\n")
            self.append_result("=" * 60 + "\n\n")
            
            # Aggiorna statistiche iniziali
            self.update_scan_stats()
            
            hosts = list(net.hosts()) if net.num_addresses > 2 else [net.network_address]
            self.total_hosts = len(hosts)  # Aggiusta per host effettivi
            
            for i, ip in enumerate(hosts):
                if not self.scan_running:
                    break
                    
                # Aggiorna progresso
                self.hosts_completed = i
                progress = i / len(hosts) if len(hosts) > 0 else 0
                self.update_progress(progress)
                self.update_scan_stats()
                
                # Calcola ETA
                if i > 0:
                    elapsed = time.time() - self.start_time
                    avg_time_per_host = elapsed / i
                    remaining_hosts = len(hosts) - i
                    eta_seconds = remaining_hosts * avg_time_per_host
                    self.update_eta(eta_seconds)
                
                # Scansiona host
                result = self.scanner.scansiona_host(str(ip), ports)
                
                if result:
                    self.hosts_found += 1
                    self.total_ports_found += len(result['porte_aperte'])
                    self.scan_results.append(result)
                    
                    self.append_result(f"✅ {result['ip']} ({result['hostname']})\n")
                    if result['porte_aperte']:
                        for porta in result['porte_aperte']:
                            servizio = self.scanner.ottieni_info_servizio(porta)
                            self.append_result(f"   🔓 Porta {porta}: {servizio}\n")
                    self.append_result("\n")
                else:
                    self.append_result(f"❌ {ip} - Non raggiungibile\n")
                
                # Aggiorna statistiche trovate
                self.update_found_stats()
                
            # Completa il progresso
            self.hosts_completed = len(hosts)
            self.update_progress(1.0)
            self.update_scan_stats()
                
        except Exception as e:
            raise Exception(f"Errore scansione rete: {e}")
            
    def scan_single_host(self, target, ports):
        """Scansiona un singolo host"""
        self.append_result(f"🎯 Scansione host: {target}\n")
        self.append_result("=" * 40 + "\n\n")
        
        self.update_status(f"🔍 Scansionando {target}...")
        
        result = self.scanner.scansiona_host(target, ports)
        
        self.hosts_completed = 1
        self.update_progress(1.0)
        self.update_scan_stats()
        
        if result:
            self.hosts_found = 1
            self.total_ports_found = len(result['porte_aperte'])
            self.scan_results.append(result)
            
            self.append_result(f"✅ Host attivo: {result['ip']}\n")
            self.append_result(f"🏠 Hostname: {result['hostname']}\n\n")
            
            if result['porte_aperte']:
                self.append_result(f"🔓 Porte aperte ({len(result['porte_aperte'])}):\n")
                for porta in result['porte_aperte']:
                    servizio = self.scanner.ottieni_info_servizio(porta)
                    self.append_result(f"   ▶ Porta {porta}: {servizio}\n")
            else:
                self.append_result("⚠️ Nessuna porta aperta trovata\n")
        else:
            self.append_result("❌ Host non raggiungibile\n")
            
        self.update_found_stats()
        
    def update_progress(self, progress):
        """Aggiorna la progress bar (thread-safe)"""
        percentage = int(progress * 100)
        self.root.after(0, lambda: self.progress_bar.set(progress))
        self.root.after(0, lambda: self.progress_percentage.configure(text=f"{percentage}%"))
        
    def update_scan_stats(self):
        """Aggiorna le statistiche di scansione (thread-safe)"""
        stats_text = f"🎯 Host: {self.hosts_completed}/{self.total_hosts}"
        self.root.after(0, lambda: self.hosts_stats_label.configure(text=stats_text))
        
        # Aggiorna tempo trascorso
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.update_time_stats(elapsed)
            
    def update_time_stats(self, elapsed_seconds, completed=False):
        """Aggiorna le statistiche del tempo (thread-safe)"""
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        time_text = f"⏱️ Tempo: {minutes:02d}:{seconds:02d}"
        if completed:
            time_text += " (Completato)"
        self.root.after(0, lambda: self.time_stats_label.configure(text=time_text))
        
    def update_found_stats(self):
        """Aggiorna le statistiche degli host trovati (thread-safe)"""
        stats_text = f"✅ Trovati: {self.hosts_found} host, {self.total_ports_found} porte"
        self.root.after(0, lambda: self.found_stats_label.configure(text=stats_text))
        
    def update_eta(self, eta_seconds):
        """Aggiorna il tempo stimato rimanente (thread-safe)"""
        if eta_seconds < 60:
            eta_text = f"🕐 Tempo stimato: {int(eta_seconds)}s"
        else:
            eta_minutes = int(eta_seconds // 60)
            eta_secs = int(eta_seconds % 60)
            eta_text = f"🕐 Tempo stimato: {eta_minutes}m {eta_secs}s"
        self.root.after(0, lambda: self.eta_label.configure(text=eta_text))
        
    def stop_scan(self):
        """Ferma la scansione"""
        self.scan_running = False
        self.update_status("⏹️ Scansione fermata dall'utente")
        self.scan_completed()
        
    def scan_completed(self):
        """Chiamata quando la scansione è completata"""
        self.scan_running = False
        self.scan_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        # Aggiorna ETA finale
        self.eta_label.configure(text="🏁 Completato!")
        
    def clear_results(self):
        """Pulisce i risultati"""
        if messagebox.askyesno("Conferma", "🗑️ Vuoi cancellare tutti i risultati?"):
            self.results_text.delete("1.0", "end")
            self.scan_results = []
            self.update_results_count()
            
            # Reset statistiche
            self.progress_bar.set(0)
            self.progress_percentage.configure(text="0%")
            self.hosts_stats_label.configure(text="🎯 Host: 0/0")
            self.time_stats_label.configure(text="⏱️ Tempo: 00:00")
            self.found_stats_label.configure(text="✅ Trovati: 0 host, 0 porte")
            self.eta_label.configure(text="🕐 Tempo stimato: --")
            
            self.update_status("🟢 Risultati cancellati")
        
    def append_result(self, text):
        """Aggiunge testo ai risultati (thread-safe)"""
        self.root.after(0, lambda: self._append_result_main_thread(text))
        
    def _append_result_main_thread(self, text):
        """Aggiunge testo ai risultati nel thread principale"""
        self.results_text.insert("end", text)
        self.results_text.see("end")
        
    def update_status(self, status):
        """Aggiorna lo status (thread-safe)"""
        self.root.after(0, lambda: self.status_label.configure(text=status))
        
    def update_results_count(self):
        """Aggiorna il contatore risultati"""
        count = len(self.scan_results)
        self.results_count_label.configure(text=f"Host trovati: {count}")
        
    def show_scan_summary(self):
        """Mostra il riassunto della scansione"""
        if not self.scan_results:
            return
            
        self.append_result("\n" + "=" * 60 + "\n")
        self.append_result("📈 RIASSUNTO SCANSIONE\n")
        self.append_result("=" * 60 + "\n")
        
        total_hosts = len(self.scan_results)
        total_ports = sum(len(r['porte_aperte']) for r in self.scan_results)
        
        self.append_result(f"🎯 Host attivi trovati: {total_hosts}\n")
        self.append_result(f"🔓 Porte aperte totali: {total_ports}\n")
        
        if total_hosts > 0:
            avg_ports = total_ports / total_hosts
            self.append_result(f"📊 Media porte per host: {avg_ports:.1f}\n")
            
    def show_export_dialog(self):
        """Mostra dialog per opzioni di esportazione"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("📊 Opzioni Esportazione")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centra il dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Contenuto
        ctk.CTkLabel(
            dialog, 
            text="📊 Esportazione Completata!", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog, 
            text="Il report HTML è stato aperto automaticamente.\nVuoi esportare anche in altri formati?",
            justify="center"
        ).pack(pady=10)
        
        # Pulsanti
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="📋 Esporta CSV",
            command=lambda: [self.save_csv(), dialog.destroy()],
            width=150
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="📊 Esporta Excel",
            command=lambda: [self.save_excel(), dialog.destroy()],
            width=150
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="📦 Esporta Tutto",
            command=lambda: [self.export_all_formats(), dialog.destroy()],
            width=150
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="❌ Chiudi",
            command=dialog.destroy,
            width=150,
            fg_color="gray"
        ).pack(pady=10)
        
    def save_csv(self):
        """Salva risultati in formato CSV"""
        if not self.report_manager.results_data:
            messagebox.showwarning("Attenzione", "⚠️ Nessun dato da esportare!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salva report CSV"
        )
        
        if filename:
            if self.report_manager.export_to_csv(filename):
                messagebox.showinfo("Successo", f"✅ Report CSV salvato:\n{filename}")
            else:
                messagebox.showerror("Errore", "❌ Errore durante il salvataggio CSV")
                
    def save_excel(self):
        """Salva risultati in formato Excel"""
        if not self.report_manager.results_data:
            messagebox.showwarning("Attenzione", "⚠️ Nessun dato da esportare!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Salva report Excel"
        )
        
        if filename:
            if self.report_manager.export_to_excel(filename):
                messagebox.showinfo("Successo", f"✅ Report Excel salvato:\n{filename}")
            else:
                messagebox.showerror("Errore", "❌ Errore durante il salvataggio Excel")
                
    def generate_html_report(self):
        """Genera e apre report HTML"""
        if not self.report_manager.results_data:
            messagebox.showwarning("Attenzione", "⚠️ Nessun dato da esportare!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Salva report HTML"
        )
        
        if filename:
            if self.report_manager.generate_html_report(filename):
                self.report_manager.open_html_report(filename)
                messagebox.showinfo("Successo", f"✅ Report HTML generato e aperto:\n{filename}")
            else:
                messagebox.showerror("Errore", "❌ Errore durante la generazione HTML")
                
    def export_all_formats(self):
        """Esporta in tutti i formati disponibili"""
        if not self.report_manager.results_data:
            messagebox.showwarning("Attenzione", "⚠️ Nessun dato da esportare!")
            return
            
        # Chiedi la directory di destinazione
        directory = filedialog.askdirectory(title="Seleziona cartella per esportazione completa")
        
        if directory:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = os.path.join(directory, f"scan_report_{timestamp}")
            
            results = self.report_manager.export_all_formats(base_filename)
            
            # Mostra risultati
            success_count = sum(1 for r in results.values() if r['success'])
            total_count = len(results)
            
            if success_count == total_count:
                messagebox.showinfo(
                    "Successo", 
                    f"✅ Tutti i {total_count} formati esportati con successo!\n\n" +
                    "\n".join([f"📄 {fmt.upper()}: {r['filename']}" for fmt, r in results.items() if r['success']])
                )
                
                # Apri report HTML se disponibile
                html_result = results.get('html')
                if html_result and html_result['success']:
                    self.report_manager.open_html_report(html_result['filename'])
            else:
                failed = [fmt for fmt, r in results.items() if not r['success']]
                messagebox.showwarning(
                    "Parziale", 
                    f"⚠️ {success_count}/{total_count} formati esportati.\n\nFalliti: {', '.join(failed)}"
                )
            
    def clear_results(self):
        """Pulisce i risultati"""
        if messagebox.askyesno("Conferma", "🗑️ Vuoi cancellare tutti i risultati?"):
            self.results_text.delete("1.0", "end")
            self.scan_results = []
            self.update_results_count()
            self.progress_bar.set(0)
            self.update_status("🟢 Risultati cancellati")
            
    def run(self):
        """Avvia l'applicazione"""
        # Setup finale
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centra la finestra
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Avvia loop principale
        self.root.mainloop()
        
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        if self.scan_running:
            if messagebox.askokcancel("Chiudi", "🔍 Scansione in corso. Vuoi fermarla e uscire?"):
                self.scan_running = False
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Funzione principale"""
    try:
        app = IPScannerGUI()
        app.run()
    except Exception as e:
        print(f"Errore nell'avvio dell'applicazione: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

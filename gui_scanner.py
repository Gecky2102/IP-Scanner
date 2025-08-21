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

# Importa il motore di scansione
from ip_scanner import IPScanner
from config import PORTE_COMUNI, WEB_PORTS, DB_PORTS, NETWORK_PORTS

# Configura il tema scuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IPScannerGUI:
    def __init__(self):
        # Finestra principale
        self.root = ctk.CTk()
        self.root.title("🔍 IP Scanner - Scansionatore di Rete")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Icona (se disponibile)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Scanner engine
        self.scanner = IPScanner()
        self.scan_running = False
        self.current_scan_thread = None
        
        # Variabili
        self.target_var = ctk.StringVar()
        self.timeout_var = ctk.StringVar(value="1")
        self.threads_var = ctk.StringVar(value="100")
        self.port_mode_var = ctk.StringVar(value="comuni")
        self.custom_ports_var = ctk.StringVar()
        
        # Risultati
        self.scan_results = []
        
        self.setup_ui()
        self.setup_styles()
        
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
        config_frame = ctk.CTkScrollableFrame(parent, width=350, label_text="⚙️ Configurazione Scansione")
        config_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Target
        target_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        target_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(target_frame, text="🎯 Target:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.target_entry = ctk.CTkEntry(
            target_frame, 
            textvariable=self.target_var,
            placeholder_text="es: 192.168.1.1 o 192.168.1.0/24",
            width=300
        )
        self.target_entry.pack(fill="x", pady=(5, 0))
        
        # Modalità porte
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
        util_frame.pack(fill="x")
        
        save_button = ctk.CTkButton(
            util_frame,
            text="💾 Salva",
            command=self.save_results,
            width=100
        )
        save_button.pack(side="left", padx=(0, 5))
        
        clear_button = ctk.CTkButton(
            util_frame,
            text="🗑️ Pulisci",
            command=self.clear_results,
            width=100
        )
        clear_button.pack(side="right", padx=(5, 0))
        
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
        footer_frame = ctk.CTkFrame(parent, height=60)
        footer_frame.pack(fill="x", pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        # Progress bar
        self.progress_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="🟢 Pronto per la scansione",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack()
        
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
            self.update_status("🔍 Scansione in corso...")
            start_time = datetime.now()
            
            if "/" in target:
                # Scansione rete
                self.scan_network(target, ports)
            else:
                # Scansione singola
                self.scan_single_host(target, ports)
                
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if self.scan_running:
                self.update_status(f"✅ Scansione completata in {duration:.2f} secondi")
                self.show_scan_summary()
                
        except Exception as e:
            if self.scan_running:
                self.update_status(f"❌ Errore durante la scansione: {e}")
                self.append_result(f"❌ ERRORE: {e}\n")
        finally:
            if self.scan_running:
                self.scan_completed()
                
    def scan_network(self, network, ports):
        """Scansiona una rete"""
        try:
            net = ipaddress.ip_network(network, strict=False)
            total_hosts = net.num_addresses
            
            self.append_result(f"🌐 Scansione rete: {network}\n")
            self.append_result(f"📊 Host totali da scansionare: {total_hosts}\n")
            self.append_result("=" * 60 + "\n\n")
            
            hosts = list(net.hosts()) if net.num_addresses > 2 else [net.network_address]
            completed = 0
            
            for ip in hosts:
                if not self.scan_running:
                    break
                    
                result = self.scanner.scansiona_host(str(ip), ports)
                completed += 1
                
                # Aggiorna progress
                progress = completed / len(hosts)
                self.root.after(0, lambda p=progress: self.progress_bar.set(p))
                
                if result:
                    self.scan_results.append(result)
                    self.append_result(f"✅ {result['ip']} ({result['hostname']})\n")
                    if result['porte_aperte']:
                        for porta in result['porte_aperte']:
                            servizio = self.scanner.ottieni_info_servizio(porta)
                            self.append_result(f"   🔓 Porta {porta}: {servizio}\n")
                    self.append_result("\n")
                else:
                    self.append_result(f"❌ {ip} - Non raggiungibile\n")
                    
                # Aggiorna contatore
                self.root.after(0, lambda: self.update_results_count())
                
        except Exception as e:
            raise Exception(f"Errore scansione rete: {e}")
            
    def scan_single_host(self, target, ports):
        """Scansiona un singolo host"""
        self.append_result(f"🎯 Scansione host: {target}\n")
        self.append_result("=" * 40 + "\n\n")
        
        result = self.scanner.scansiona_host(target, ports)
        self.progress_bar.set(1.0)
        
        if result:
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
            
        self.update_results_count()
        
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
        self.progress_bar.set(1.0)
        
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
            
    def save_results(self):
        """Salva i risultati in un file"""
        if not self.scan_results:
            messagebox.showwarning("Attenzione", "⚠️ Nessun risultato da salvare!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Salva risultati scansione"
        )
        
        if not filename:
            return
            
        try:
            if filename.endswith('.json'):
                # Salva in formato JSON
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'target': self.target_var.get(),
                    'results': self.scan_results
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                # Salva in formato testo
                with open(filename, 'w', encoding='utf-8') as f:
                    content = self.results_text.get("1.0", "end")
                    f.write(content)
                    
            messagebox.showinfo("Successo", f"✅ Risultati salvati in: {filename}")
            
        except Exception as e:
            messagebox.showerror("Errore", f"❌ Errore nel salvataggio: {e}")
            
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

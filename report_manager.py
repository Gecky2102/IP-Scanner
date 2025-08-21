#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Manager per IP Scanner
Gestisce l'esportazione e visualizzazione dei risultati
"""

import pandas as pd
import json
import csv
import html
import webbrowser
import os
import socket
import subprocess
import platform
from datetime import datetime
from scapy.all import ARP, Ether, srp
import threading
import time

class ReportManager:
    def __init__(self):
        self.results_data = []
        self.network_info = {}
        self.scan_metadata = {}
        
    def add_result(self, ip, active, hostname=None, open_ports=None, mac_address=None, device_name=None):
        """Aggiunge un risultato al report"""
        result = {
            'ip': ip,
            'active': active,
            'hostname': hostname or 'N/A',
            'open_ports': open_ports or [],
            'ports_count': len(open_ports) if open_ports else 0,
            'mac_address': mac_address or 'N/A',
            'device_name': device_name or 'N/A',
            'status': '✅ Attivo' if active else '❌ Inattivo',
            'timestamp': datetime.now().isoformat()
        }
        self.results_data.append(result)
        
    def set_scan_metadata(self, target, total_scanned, duration, ports_mode):
        """Imposta i metadati della scansione"""
        self.scan_metadata = {
            'target': target,
            'total_scanned': total_scanned,
            'duration': duration,
            'ports_mode': ports_mode,
            'scan_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'active_hosts': len([r for r in self.results_data if r['active']]),
            'total_ports_found': sum(r['ports_count'] for r in self.results_data)
        }
        
    def get_mac_address(self, ip, timeout=2):
        """Ottiene il MAC address di un IP tramite ARP"""
        try:
            # Crea un pacchetto ARP request
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # Invia il pacchetto e ricevi la risposta
            answered_list = srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]
            
            if answered_list:
                return answered_list[0][1].hwsrc
            return None
        except Exception as e:
            print(f"Errore MAC address per {ip}: {e}")
            return None
            
    def get_device_name(self, ip, mac_address=None):
        """Tenta di ottenere il nome del dispositivo"""
        device_name = "N/A"
        
        try:
            # Prova con hostname reverse
            hostname = socket.gethostbyaddr(ip)[0]
            if hostname and not hostname.startswith(ip):
                device_name = hostname
        except:
            pass
            
        # Prova con NetBIOS (Windows)
        if device_name == "N/A" and platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["nbtstat", "-A", ip], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '<00>' in line and 'UNIQUE' in line:
                            device_name = line.split()[0].strip()
                            break
            except:
                pass
                
        return device_name
        
    def enhance_results_with_network_info(self, progress_callback=None):
        """Arricchisce i risultati con MAC address e nomi dispositivi"""
        total = len(self.results_data)
        
        for i, result in enumerate(self.results_data):
            if result['active']:
                # Ottieni MAC address
                mac = self.get_mac_address(result['ip'])
                result['mac_address'] = mac if mac else 'N/A'
                
                # Ottieni nome dispositivo
                device_name = self.get_device_name(result['ip'], mac)
                result['device_name'] = device_name
                
            # Callback per progress
            if progress_callback:
                progress_callback(i + 1, total)
                
    def export_to_csv(self, filename):
        """Esporta i risultati in formato CSV"""
        try:
            df = pd.DataFrame(self.results_data)
            
            # Riordina le colonne
            columns_order = ['ip', 'status', 'hostname', 'mac_address', 'device_name', 
                           'ports_count', 'open_ports', 'timestamp']
            df = df[columns_order]
            
            # Converte lista porte in stringa
            df['open_ports'] = df['open_ports'].apply(lambda x: ', '.join(map(str, x)) if x else '')
            
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"Errore esportazione CSV: {e}")
            return False
            
    def export_to_excel(self, filename):
        """Esporta i risultati in formato Excel"""
        try:
            df = pd.DataFrame(self.results_data)
            
            # Riordina le colonne
            columns_order = ['ip', 'status', 'hostname', 'mac_address', 'device_name', 
                           'ports_count', 'open_ports', 'timestamp']
            df = df[columns_order]
            
            # Converte lista porte in stringa
            df['open_ports'] = df['open_ports'].apply(lambda x: ', '.join(map(str, x)) if x else '')
            
            # Rinomina colonne per Excel
            df.columns = ['IP Address', 'Status', 'Hostname', 'MAC Address', 'Device Name',
                         'Ports Count', 'Open Ports', 'Scan Time']
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Scan Results', index=False)
                
                # Formattazione
                worksheet = writer.sheets['Scan Results']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
            return True
        except Exception as e:
            print(f"Errore esportazione Excel: {e}")
            return False
            
    def export_to_json(self, filename):
        """Esporta i risultati in formato JSON dettagliato"""
        try:
            export_data = {
                'scan_metadata': self.scan_metadata,
                'network_info': self.network_info,
                'results': self.results_data,
                'summary': {
                    'total_scanned': len(self.results_data),
                    'active_hosts': len([r for r in self.results_data if r['active']]),
                    'inactive_hosts': len([r for r in self.results_data if not r['active']]),
                    'total_ports_found': sum(r['ports_count'] for r in self.results_data),
                    'devices_with_mac': len([r for r in self.results_data if r['mac_address'] != 'N/A']),
                    'devices_with_name': len([r for r in self.results_data if r['device_name'] != 'N/A'])
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore esportazione JSON: {e}")
            return False
            
    def generate_html_report(self, filename):
        """Genera un report HTML interattivo"""
        try:
            # Template HTML
            html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP Scanner - Report Scansione</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .table-container {
            padding: 30px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9em;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .status-active {
            color: #28a745;
            font-weight: bold;
        }
        .status-inactive {
            color: #dc3545;
            font-weight: bold;
        }
        .ports {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            background: #f1f3f4;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .mac-address {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #666;
        }
        .device-name {
            font-weight: 500;
            color: #333;
        }
        .footer {
            padding: 20px 30px;
            background: #f8f9fa;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }
        .search-box {
            width: 100%;
            max-width: 400px;
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            margin-bottom: 20px;
            transition: border-color 0.3s;
        }
        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }
        .filter-buttons {
            margin-bottom: 20px;
            text-align: center;
        }
        .filter-btn {
            padding: 8px 16px;
            margin: 0 5px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn:hover, .filter-btn.active {
            background: #667eea;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 IP Scanner Report</h1>
            <p>Scansione completata il {scan_date}</p>
            <p>Target: {target} | Durata: {duration:.2f}s</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_scanned}</div>
                <div class="stat-label">Host Scansionati</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{active_hosts}</div>
                <div class="stat-label">Host Attivi</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_ports}</div>
                <div class="stat-label">Porte Aperte</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{devices_with_mac}</div>
                <div class="stat-label">Dispositivi con MAC</div>
            </div>
        </div>
        
        <div class="table-container">
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Cerca IP, hostname o dispositivo...">
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterTable('all')">Tutti</button>
                <button class="filter-btn" onclick="filterTable('active')">Solo Attivi</button>
                <button class="filter-btn" onclick="filterTable('inactive')">Solo Inattivi</button>
            </div>
            
            <table id="resultsTable">
                <thead>
                    <tr>
                        <th>🌐 IP Address</th>
                        <th>📊 Status</th>
                        <th>🏠 Hostname</th>
                        <th>🔧 MAC Address</th>
                        <th>💻 Nome Dispositivo</th>
                        <th>🔓 Porte Aperte</th>
                        <th>⏰ Scan Time</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>📄 Report generato da IP Scanner | 🕐 {generation_time}</p>
            <p>⚠️ Utilizzare responsabilmente - Solo su reti autorizzate</p>
        </div>
    </div>
    
    <script>
        // Funzione di ricerca
        document.getElementById('searchBox').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.getElementById('resultsTable');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            }
        });
        
        // Funzione di filtro
        function filterTable(filter) {
            const table = document.getElementById('resultsTable');
            const rows = table.getElementsByTagName('tr');
            
            // Update active button
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const status = row.getElementsByTagName('td')[1].textContent;
                
                if (filter === 'all') {
                    row.style.display = '';
                } else if (filter === 'active') {
                    row.style.display = status.includes('Attivo') ? '' : 'none';
                } else if (filter === 'inactive') {
                    row.style.display = status.includes('Inattivo') ? '' : 'none';
                }
            }
        }
    </script>
</body>
</html>
            """
            
            # Genera le righe della tabella
            table_rows = ""
            for result in self.results_data:
                ports_str = ', '.join(map(str, result['open_ports'])) if result['open_ports'] else 'Nessuna'
                status_class = 'status-active' if result['active'] else 'status-inactive'
                
                table_rows += f"""
                <tr>
                    <td>{html.escape(result['ip'])}</td>
                    <td><span class="{status_class}">{html.escape(result['status'])}</span></td>
                    <td>{html.escape(result['hostname'])}</td>
                    <td><span class="mac-address">{html.escape(result['mac_address'])}</span></td>
                    <td><span class="device-name">{html.escape(result['device_name'])}</span></td>
                    <td><span class="ports">{html.escape(ports_str)}</span></td>
                    <td>{html.escape(result['timestamp'][:19])}</td>
                </tr>
                """
            
            # Sostituisce i placeholder
            html_content = html_template.format(
                scan_date=self.scan_metadata.get('scan_date', 'N/A'),
                target=html.escape(self.scan_metadata.get('target', 'N/A')),
                duration=self.scan_metadata.get('duration', 0),
                total_scanned=len(self.results_data),
                active_hosts=len([r for r in self.results_data if r['active']]),
                total_ports=sum(r['ports_count'] for r in self.results_data),
                devices_with_mac=len([r for r in self.results_data if r['mac_address'] != 'N/A']),
                table_rows=table_rows,
                generation_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Errore generazione HTML: {e}")
            return False
            
    def open_html_report(self, filename):
        """Apre il report HTML nel browser"""
        try:
            webbrowser.open(f'file://{os.path.abspath(filename)}')
            return True
        except Exception as e:
            print(f"Errore apertura HTML: {e}")
            return False
            
    def export_all_formats(self, base_filename):
        """Esporta in tutti i formati disponibili"""
        results = {}
        
        # Determina il nome base senza estensione
        if '.' in base_filename:
            base_name = '.'.join(base_filename.split('.')[:-1])
        else:
            base_name = base_filename
            
        # Esporta in tutti i formati
        formats = [
            ('csv', self.export_to_csv),
            ('xlsx', self.export_to_excel),
            ('json', self.export_to_json),
            ('html', self.generate_html_report)
        ]
        
        for fmt, export_func in formats:
            filename = f"{base_name}.{fmt}"
            success = export_func(filename)
            results[fmt] = {'success': success, 'filename': filename}
            
        return results
        
    def clear_results(self):
        """Pulisce tutti i risultati"""
        self.results_data = []
        self.scan_metadata = {}
        self.network_info = {}

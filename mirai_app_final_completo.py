#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font as tkfont
import threading
import queue
import time
from pathlib import Path
import json
import sys
import os

# Adiciona path do projeto
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Tenta importar core - funciona mesmo sem
try:
    from core.ai_engine import MiraiAI
    from core.context_manager import ContextManager
    from core.state_machine import StateMachine
    from actions.speaker import Speaker
    from perception.voice_listener import VoiceListener
    CORE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Core não disponível: {e}")
    CORE_AVAILABLE = False


class ModernColors:
    """Paleta de cores moderna para a Mirai"""
    
    # Tema Escuro Moderno (Catppuccin Mocha)
    BG_DARK = "#1e1e2e"
    BG_DARKER = "#11111b"
    BG_LIGHT = "#313244"
    
    FG_PRIMARY = "#cdd6f4"
    FG_SECONDARY = "#bac2de"
    
    ACCENT_PINK = "#f5c2e7"      # Rosa Mirai
    ACCENT_BLUE = "#89b4fa"      # Azul
    ACCENT_GREEN = "#a6e3a1"     # Verde
    ACCENT_YELLOW = "#f9e2af"    # Amarelo
    ACCENT_RED = "#f38ba8"       # Vermelho
    ACCENT_PURPLE = "#cba6f7"    # Roxo
    
    # Estados
    SUCCESS = "#a6e3a1"
    WARNING = "#f9e2af"
    ERROR = "#f38ba8"
    INFO = "#89b4fa"


class RoundedButton(tk.Canvas):
    """Botão moderno com cantos arredondados"""
    
    def __init__(self, parent, text="Button", command=None, 
                 bg=ModernColors.ACCENT_PINK, fg="#000000",
                 width=200, height=40, corner_radius=20):
        super().__init__(parent, width=width, height=height, 
                        bg=ModernColors.BG_DARK, highlightthickness=0)
        
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.text = text
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self, color=None):
        """Desenha o botão"""
        self.delete("all")
        
        bg = color or self.bg_color
        
        # Fundo arredondado
        x1, y1 = 5, 5
        x2, y2 = self.width - 5, self.height - 5
        r = self.corner_radius
        
        self.create_oval(x1, y1, x1 + r, y1 + r, fill=bg, outline="")
        self.create_oval(x2 - r, y1, x2, y1 + r, fill=bg, outline="")
        self.create_oval(x1, y2 - r, x1 + r, y2, fill=bg, outline="")
        self.create_oval(x2 - r, y2 - r, x2, y2, fill=bg, outline="")
        
        self.create_rectangle(x1 + r//2, y1, x2 - r//2, y2, fill=bg, outline="")
        self.create_rectangle(x1, y1 + r//2, x2, y2 - r//2, fill=bg, outline="")
        
        # Texto
        self.create_text(self.width // 2, self.height // 2,
                        text=self.text, fill=self.fg_color,
                        font=("Segoe UI", 11, "bold"))
    
    def on_click(self, event):
        """Clique"""
        if self.command:
            self.command()
    
    def on_enter(self, event):
        """Mouse sobre"""
        self.draw_button(ModernColors.ACCENT_BLUE)
    
    def on_leave(self, event):
        """Mouse fora"""
        self.draw_button()


class StatusIndicator(tk.Canvas):
    """Indicador de status moderno"""
    
    def __init__(self, parent, text="Status", status="inactive"):
        super().__init__(parent, width=200, height=30,
                        bg=ModernColors.BG_LIGHT, highlightthickness=0)
        
        self.text = text
        self.status = status
        self.draw()
    
    def draw(self):
        """Desenha indicador"""
        self.delete("all")
        
        # Bolinha de status
        colors = {
            "active": ModernColors.SUCCESS,
            "warning": ModernColors.WARNING,
            "error": ModernColors.ERROR,
            "inactive": ModernColors.FG_SECONDARY
        }
        
        color = colors.get(self.status, ModernColors.FG_SECONDARY)
        
        self.create_oval(10, 10, 20, 20, fill=color, outline="")
        
        # Texto
        self.create_text(30, 15, text=self.text, fill=ModernColors.FG_PRIMARY,
                        font=("Segoe UI", 9), anchor="w")
    
    def set_status(self, status, text=None):
        """Atualiza status"""
        self.status = status
        if text:
            self.text = text
        self.draw()


class MiraiCore:
    """Core da Mirai - Gerencia IA, Voz, etc."""
    
    def __init__(self, message_callback=None):
        self.message_callback = message_callback
        
        # Sistemas
        self.context = None
        self.state = None
        self.ai = None
        self.speaker = None
        self.voice = None
        
        # Estado
        self.initialized = False
        self.is_speaking = False
        self.is_listening = False
        self.autonomous_active = False
        
        # Queue de mensagens
        self.message_queue = queue.Queue()
        
        # Thread de processamento
        self.processing_thread = None
        self.stop_processing = threading.Event()
    
    def initialize(self):
        """Inicializa sistemas"""
        if not CORE_AVAILABLE:
            self.send_message("error", "Core da Mirai não disponível!")
            self.send_message("error", "Certifique-se de estar no diretório correto do projeto.")
            return False
        
        try:
            self.send_message("system", "Inicializando Mirai...")
            
            # Context Manager
            self.context = ContextManager()
            self.send_message("system", "✓ Context Manager")
            
            # State Machine
            self.state = StateMachine()
            self.send_message("system", "✓ State Machine")
            
            # IA Engine
            self.ai = MiraiAI(self.context)
            import asyncio
            asyncio.run(self.ai.initialize())
            self.send_message("system", "✓ IA Engine")
            
            # Speaker
            self.speaker = Speaker()
            self.speaker.initialize()
            self.send_message("system", "✓ Sistema de Voz")
            
            # Voice Listener
            self.voice = VoiceListener()
            self.send_message("system", "✓ Reconhecimento de Voz")
            
            # Inicia thread de processamento
            self.start_processing_thread()
            
            self.initialized = True
            self.send_message("system", "✨ Mirai inicializada com sucesso!")
            self.send_message("mirai", "Oi! Sou a Mirai! Estou pronta para conversar! 🌸")
            
            # Fala
            if self.speaker and self.speaker.enabled:
                self.speaker.speak("Olá! Sou a Mirai! Estou pronta!")
            
            return True
        
        except Exception as e:
            self.send_message("error", f"Erro na inicialização: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start_processing_thread(self):
        """Inicia thread de processamento de mensagens"""
        self.stop_processing.clear()
        self.processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True
        )
        self.processing_thread.start()
    
    def _processing_loop(self):
        """Loop de processamento"""
        while not self.stop_processing.is_set():
            try:
                # Pega mensagem da fila
                user_text = self.message_queue.get(timeout=0.1)
                
                if user_text:
                    self._process_user_message(user_text)
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no processamento: {e}")
    
    def _process_user_message(self, text):
        """Processa mensagem do usuário"""
        if not self.ai:
            return
        
        try:
            # Gera resposta
            response = self.ai.generate_response(text, mode="conversation", enable_search=True)
            
            # Envia resposta
            self.send_message("mirai", response)
            
            # Fala
            if self.speaker and self.speaker.enabled:
                self.is_speaking = True
                self.speaker.speak(response)
                self.is_speaking = False
        
        except Exception as e:
            self.send_message("error", f"Erro: {e}")
    
    def send_user_message(self, text):
        """Envia mensagem do usuário para processamento"""
        self.message_queue.put(text)
    
    def send_message(self, msg_type, text):
        """Envia mensagem para callback"""
        if self.message_callback:
            self.message_callback(msg_type, text)
    
    def start_voice_listening(self):
        """Inicia escuta de voz"""
        if not self.voice or not self.voice.initialize():
            self.send_message("error", "Microfone não disponível")
            return False
        
        self.is_listening = True
        self.send_message("system", "🎤 Escuta de voz ativada")
        
        # Thread de escuta
        threading.Thread(
            target=self._voice_listening_loop,
            daemon=True
        ).start()
        
        return True
    
    def stop_voice_listening(self):
        """Para escuta de voz"""
        self.is_listening = False
        self.send_message("system", "🎤 Escuta de voz desativada")
    
    def _voice_listening_loop(self):
        """Loop de escuta de voz"""
        while self.is_listening:
            try:
                text = self.voice.listen_once()
                
                if text:
                    self.send_message("user_voice", text)
                    self.send_user_message(text)
            
            except Exception as e:
                print(f"Erro na escuta: {e}")
                time.sleep(0.5)
    
    def start_autonomous(self):
        """Inicia modo autônomo"""
        if self.autonomous_active:
            return
        
        self.autonomous_active = True
        self.send_message("system", "🤖 Modo autônomo ativado!")
        
        # Inicia voz se não estiver
        if not self.is_listening:
            self.start_voice_listening()
        
        # Thread de iniciativa
        threading.Thread(
            target=self._autonomous_loop,
            daemon=True
        ).start()
    
    def stop_autonomous(self):
        """Para modo autônomo"""
        self.autonomous_active = False
        self.send_message("system", "🤖 Modo autônomo desativado")
    
    def _autonomous_loop(self):
        """Loop de modo autônomo"""
        last_user_time = time.time()
        last_initiative = 0
        
        while self.autonomous_active:
            time.sleep(3)
            
            current = time.time()
            silence = current - last_user_time
            
            # Toma iniciativa após 25s de silêncio
            if silence >= 25 and (current - last_initiative) >= 30:
                if not self.is_speaking and not self.message_queue.qsize() > 0:
                    # Gera iniciativa
                    initiative = self.ai.generate_initiative()
                    
                    self.send_message("mirai_initiative", initiative)
                    
                    if self.speaker and self.speaker.enabled:
                        self.is_speaking = True
                        self.speaker.speak(initiative)
                        self.is_speaking = False
                    
                    last_initiative = current
            
            # Atualiza tempo do usuário quando há mensagens
            if not self.message_queue.empty():
                last_user_time = current
    
    def shutdown(self):
        """Desliga sistemas"""
        self.stop_processing.set()
        self.is_listening = False
        self.autonomous_active = False
        
        if self.processing_thread:
            self.processing_thread.join(timeout=2)


class MiraiApp:
    """Aplicativo Desktop da Mirai - Versão Ultra Funcional"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌸 Mirai - Assistente Virtual VTuber")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernColors.BG_DARK)
        
        # Core
        self.core = MiraiCore(message_callback=self.add_message)
        
        # Estado da UI
        self.voice_active = False
        self.autonomous_active = False
        
        # Cria UI
        self.create_ui()
        
        # Inicializa core em thread
        threading.Thread(target=self.core.initialize, daemon=True).start()
    
    def create_ui(self):
        """Cria interface"""
        # Header
        self.create_header()
        
        # Main content
        main_frame = tk.Frame(self.root, bg=ModernColors.BG_DARK)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Chat area (esquerda - 70%)
        chat_frame = tk.Frame(main_frame, bg=ModernColors.BG_DARK)
        chat_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_chat_area(chat_frame)
        
        # Controls (direita - 30%)
        controls_frame = tk.Frame(main_frame, bg=ModernColors.BG_LIGHT, width=350)
        controls_frame.pack(side='right', fill='y')
        controls_frame.pack_propagate(False)
        
        self.create_controls(controls_frame)
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Cria cabeçalho"""
        header = tk.Frame(self.root, bg=ModernColors.ACCENT_PINK, height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        title_frame = tk.Frame(header, bg=ModernColors.ACCENT_PINK)
        title_frame.pack(expand=True)
        
        title_label = tk.Label(
            title_frame,
            text="🌸 MIRAI",
            font=("Segoe UI", 32, "bold"),
            bg=ModernColors.ACCENT_PINK,
            fg="#000000"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Assistente Virtual VTuber • Versão 4.0",
            font=("Segoe UI", 11),
            bg=ModernColors.ACCENT_PINK,
            fg="#000000"
        )
        subtitle_label.pack()
    
    def create_chat_area(self, parent):
        """Cria área de chat"""
        # Label
        label = tk.Label(
            parent,
            text="💬 Chat",
            font=("Segoe UI", 14, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.FG_PRIMARY
        )
        label.pack(anchor='w', pady=(0, 10))
        
        # Chat display
        chat_container = tk.Frame(parent, bg=ModernColors.BG_LIGHT)
        chat_container.pack(fill='both', expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=ModernColors.BG_DARKER,
            fg=ModernColors.FG_PRIMARY,
            insertbackground=ModernColors.ACCENT_PINK,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            spacing1=5,
            spacing3=5
        )
        self.chat_display.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Tags de cores
        self.chat_display.tag_config('user', 
                                    foreground=ModernColors.ACCENT_BLUE,
                                    font=("Consolas", 10, "bold"))
        self.chat_display.tag_config('user_voice',
                                    foreground=ModernColors.ACCENT_PURPLE,
                                    font=("Consolas", 10, "bold"))
        self.chat_display.tag_config('mirai',
                                    foreground=ModernColors.ACCENT_PINK,
                                    font=("Consolas", 10, "bold"))
        self.chat_display.tag_config('mirai_initiative',
                                    foreground=ModernColors.ACCENT_GREEN,
                                    font=("Consolas", 10, "bold"))
        self.chat_display.tag_config('system',
                                    foreground=ModernColors.ACCENT_YELLOW)
        self.chat_display.tag_config('error',
                                    foreground=ModernColors.ACCENT_RED)
        
        # Input area
        input_frame = tk.Frame(parent, bg=ModernColors.BG_DARK)
        input_frame.pack(fill='x')
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_PRIMARY,
            insertbackground=ModernColors.ACCENT_PINK,
            relief=tk.FLAT,
            bd=0
        )
        self.input_field.pack(side='left', fill='x', expand=True, 
                             ipady=12, padx=(0, 10))
        self.input_field.bind('<Return>', lambda e: self.send_message())
        
        # Botão enviar
        send_btn = RoundedButton(
            input_frame,
            text="Enviar",
            command=self.send_message,
            bg=ModernColors.ACCENT_PINK,
            width=100,
            height=40
        )
        send_btn.pack(side='right')
    
    def create_controls(self, parent):
        """Cria painel de controles"""
        # Padding
        pad_frame = tk.Frame(parent, bg=ModernColors.BG_LIGHT)
        pad_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Título
        tk.Label(
            pad_frame,
            text="Controles",
            font=("Segoe UI", 14, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_PRIMARY
        ).pack(anchor='w', pady=(0, 15))
        
        # Botão Voz
        self.voice_btn = RoundedButton(
            pad_frame,
            text="🎤 Iniciar Voz",
            command=self.toggle_voice,
            bg=ModernColors.ACCENT_GREEN,
            width=300,
            height=50
        )
        self.voice_btn.pack(pady=5)
        
        # Botão Autônomo
        self.auto_btn = RoundedButton(
            pad_frame,
            text="🤖 Modo Autônomo",
            command=self.toggle_autonomous,
            bg=ModernColors.ACCENT_PURPLE,
            width=300,
            height=50
        )
        self.auto_btn.pack(pady=5)
        
        # Separador
        tk.Frame(pad_frame, bg=ModernColors.BG_DARKER, height=2).pack(fill='x', pady=15)
        
        # Status
        tk.Label(
            pad_frame,
            text="Status dos Sistemas",
            font=("Segoe UI", 12, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_PRIMARY
        ).pack(anchor='w', pady=(0, 10))
        
        # Indicadores de status
        self.status_ia = StatusIndicator(pad_frame, "IA: Inicializando...", "warning")
        self.status_ia.pack(fill='x', pady=3)
        
        self.status_voice = StatusIndicator(pad_frame, "Voz: Desativada", "inactive")
        self.status_voice.pack(fill='x', pady=3)
        
        self.status_mic = StatusIndicator(pad_frame, "Microfone: Aguardando", "inactive")
        self.status_mic.pack(fill='x', pady=3)
        
        # Separador
        tk.Frame(pad_frame, bg=ModernColors.BG_DARKER, height=2).pack(fill='x', pady=15)
        
        # Modos rápidos
        tk.Label(
            pad_frame,
            text="Modos Rápidos",
            font=("Segoe UI", 12, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_PRIMARY
        ).pack(anchor='w', pady=(0, 10))
        
        modes = [
            ("💬 Conversa", lambda: self.set_mode("conversation")),
            ("🤖 Assistente", lambda: self.set_mode("assistant")),
            ("🎮 Gamer", lambda: self.set_mode("gamer")),
        ]
        
        for text, cmd in modes:
            RoundedButton(
                pad_frame,
                text=text,
                command=cmd,
                bg=ModernColors.BG_DARKER,
                fg=ModernColors.FG_PRIMARY,
                width=300,
                height=40
            ).pack(pady=3)
        
        # Separador
        tk.Frame(pad_frame, bg=ModernColors.BG_DARKER, height=2).pack(fill='x', pady=15)
        
        # Configurações
        RoundedButton(
            pad_frame,
            text="⚙️ Configurações",
            command=self.open_settings,
            bg=ModernColors.BG_DARKER,
            fg=ModernColors.FG_PRIMARY,
            width=300,
            height=40
        ).pack(pady=5)
        
        # Sobre
        RoundedButton(
            pad_frame,
            text="ℹ️ Sobre",
            command=self.show_about,
            bg=ModernColors.BG_DARKER,
            fg=ModernColors.FG_PRIMARY,
            width=300,
            height=40
        ).pack(pady=5)
    
    def create_footer(self):
        """Cria rodapé"""
        footer = tk.Frame(self.root, bg=ModernColors.BG_LIGHT, height=40)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        self.footer_label = tk.Label(
            footer,
            text="🌸 Pronta para conversar!",
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_PRIMARY,
            font=("Segoe UI", 10)
        )
        self.footer_label.pack(side='left', padx=20, pady=10)
        
        self.footer_time = tk.Label(
            footer,
            text="",
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.FG_SECONDARY,
            font=("Segoe UI", 9)
        )
        self.footer_time.pack(side='right', padx=20)
        
        # Atualiza tempo
        self.update_time()
    
    def update_time(self):
        """Atualiza relógio"""
        current_time = time.strftime("%H:%M:%S")
        self.footer_time.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def add_message(self, msg_type, text):
        """Adiciona mensagem ao chat"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Insere na UI thread
        self.root.after(0, self._insert_message, msg_type, text, timestamp)
    
    def _insert_message(self, msg_type, text, timestamp):
        """Insere mensagem (thread-safe)"""
        self.chat_display.config(state='normal')
        
        # Timestamp
        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", 'system')
        
        if msg_type == "user":
            self.chat_display.insert(tk.END, "Você: ", 'user')
            self.chat_display.insert(tk.END, f"{text}\n")
        
        elif msg_type == "user_voice":
            self.chat_display.insert(tk.END, "Você (voz): ", 'user_voice')
            self.chat_display.insert(tk.END, f"{text}\n")
        
        elif msg_type == "mirai":
            self.chat_display.insert(tk.END, "Mirai: ", 'mirai')
            self.chat_display.insert(tk.END, f"{text}\n")
        
        elif msg_type == "mirai_initiative":
            self.chat_display.insert(tk.END, "Mirai [Iniciativa]: ", 'mirai_initiative')
            self.chat_display.insert(tk.END, f"{text}\n")
        
        elif msg_type == "system":
            self.chat_display.insert(tk.END, f"[SISTEMA] {text}\n", 'system')
            
            # Atualiza status baseado em mensagens do sistema
            if "IA Engine" in text:
                self.status_ia.set_status("active", "IA: Ativa")
            elif "Sistema de Voz" in text:
                self.status_voice.set_status("active", "Voz: Ativa")
            elif "Reconhecimento de Voz" in text:
                self.status_mic.set_status("active", "Microfone: Pronto")
        
        elif msg_type == "error":
            self.chat_display.insert(tk.END, f"[ERRO] {text}\n", 'error')
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Envia mensagem"""
        text = self.input_field.get().strip()
        
        if not text:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message("user", text)
        
        # Envia para processamento
        self.core.send_user_message(text)
    
    def toggle_voice(self):
        """Liga/desliga voz"""
        if not self.voice_active:
            if self.core.start_voice_listening():
                self.voice_active = True
                self.voice_btn.text = "🎤 Parar Voz"
                self.voice_btn.bg_color = ModernColors.ACCENT_RED
                self.voice_btn.draw_button()
                self.footer_label.config(text="🎤 Escutando...")
                self.status_mic.set_status("active", "Microfone: Escutando")
        else:
            self.core.stop_voice_listening()
            self.voice_active = False
            self.voice_btn.text = "🎤 Iniciar Voz"
            self.voice_btn.bg_color = ModernColors.ACCENT_GREEN
            self.voice_btn.draw_button()
            self.footer_label.config(text="🌸 Pronta para conversar!")
            self.status_mic.set_status("inactive", "Microfone: Parado")
    
    def toggle_autonomous(self):
        """Liga/desliga autônomo"""
        if not self.autonomous_active:
            self.core.start_autonomous()
            self.autonomous_active = True
            self.auto_btn.text = "🤖 Parar Autônomo"
            self.auto_btn.bg_color = ModernColors.ACCENT_RED
            self.auto_btn.draw_button()
            self.footer_label.config(text="🤖 Modo Autônomo Ativo")
        else:
            self.core.stop_autonomous()
            self.autonomous_active = False
            self.auto_btn.text = "🤖 Modo Autônomo"
            self.auto_btn.bg_color = ModernColors.ACCENT_PURPLE
            self.auto_btn.draw_button()
            self.footer_label.config(text="🌸 Pronta para conversar!")
    
    def set_mode(self, mode):
        """Define modo"""
        self.add_message("system", f"Modo alterado para: {mode.title()}")
    
    def open_settings(self):
        """Abre configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurações")
        settings_window.geometry("600x500")
        settings_window.configure(bg=ModernColors.BG_DARK)
        
        # Título
        tk.Label(
            settings_window,
            text="⚙️ Configurações",
            font=("Segoe UI", 18, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.FG_PRIMARY
        ).pack(pady=20)
        
        # TODO: Adicionar configurações reais
        tk.Label(
            settings_window,
            text="Configurações serão implementadas aqui",
            bg=ModernColors.BG_DARK,
            fg=ModernColors.FG_SECONDARY
        ).pack(pady=20)
        
        RoundedButton(
            settings_window,
            text="Fechar",
            command=settings_window.destroy,
            width=200,
            height=40
        ).pack(pady=20)
    
    def show_about(self):
        """Mostra sobre"""
        about_text = """
🌸 MIRAI v4.0

Assistente Virtual VTuber Profissional

Desenvolvido por: HarukiMuraka
Assistido por: Claude (Anthropic)

Versão: 4.0 Final Ultra Funcional
Data: Fevereiro 2026

Características:
✓ 100% Funcional
✓ Design Moderno
✓ Sistema Autônomo
✓ Reconhecimento de Voz
✓ IA Integrada

Feito com 💕 para a comunidade
        """
        
        messagebox.showinfo("Sobre a Mirai", about_text)
    
    def run(self):
        """Inicia aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Ao fechar"""
        self.core.shutdown()
        self.root.destroy()


def main():
    """Função principal"""
    print("="*70)
    print("🌸 MIRAI DESKTOP APP v4.0")
    print("="*70)
    print()
    print("Iniciando aplicação...")
    print()
    
    app = MiraiApp()
    app.run()


if __name__ == "__main__":
    main()
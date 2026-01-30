"""
Mirai Desktop App v2.0
Aplicativo Desktop com Interface Gráfica

Requisitos:
pip install PyQt5 PyQt5-WebEngine
"""

import sys
import asyncio
from pathlib import Path
from PyQt5.QtWidgets import ( 
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QTextEdit, QLineEdit, QLabel,
    QGroupBox, QSlider, QComboBox, QProgressBar, QMessageBox,
    QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer 
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Importa componentes da Mirai
sys.path.insert(0, str(Path(__file__).parent))
from core.ai_engine import MiraiAI
from core.context_manager import ContextManager
from core.state_machine import StateMachine
from actions.speaker import Speaker
from perception.voice_listener import VoiceListener
from vtuber.vrm_engine import VRMEngine


class VoiceThread(QThread):
    """Thread para reconhecimento de voz"""
    recognized = pyqtSignal(str)
    
    def __init__(self, voice_listener):
        super().__init__()
        self.voice_listener = voice_listener
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            try:
                text = self.voice_listener.listen_once()
                if text:
                    self.recognized.emit(text)
            except:
                pass
    
    def stop(self):
        self.running = False


class AIThread(QThread):
    """Thread para processamento da IA"""
    response_ready = pyqtSignal(str)
    
    def __init__(self, ai_engine):
        super().__init__()
        self.ai_engine = ai_engine
        self.user_input = ""
    
    def set_input(self, text):
        self.user_input = text
    
    def run(self):
        if self.user_input:
            response = self.ai_engine.generate_response(self.user_input)
            self.response_ready.emit(response)


class MiraiDesktopApp(QMainWindow):
    """Aplicativo Desktop da Mirai"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializa componentes da Mirai
        self.context = ContextManager()
        self.state = StateMachine()
        self.ai = MiraiAI(self.context)
        self.speaker = Speaker()
        self.voice = VoiceListener()
        self.vtuber = VRMEngine()
        
        # Threads
        self.voice_thread = None
        self.ai_thread = None
        
        # Configurações
        self.dark_mode = True
        
        # Inicializa UI
        self.init_ui()
        
        # Inicializa sistemas
        QTimer.singleShot(100, self.initialize_systems)
    
    def init_ui(self):
        """Inicializa interface gráfica"""
        self.setWindowTitle("🌸 Mirai - IA VTuber Desktop")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal com splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Painel esquerdo: VTuber
        self.vtuber_panel = self.create_vtuber_panel()
        main_splitter.addWidget(self.vtuber_panel)
        
        # Painel direito: Abas
        self.tabs_panel = self.create_tabs_panel()
        main_splitter.addWidget(self.tabs_panel)
        
        # Proporção 40:60
        main_splitter.setSizes([560, 840])
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        central_widget.setLayout(layout)
        
        # Aplica tema
        self.apply_theme()
    
    def create_vtuber_panel(self):
        """Cria painel do VTuber"""
        panel = QGroupBox("🎭 Modelo VTuber")
        layout = QVBoxLayout()
        
        # Área do modelo (WebView para futuro suporte a VRM)
        self.vtuber_view = QWebEngineView()
        self.vtuber_view.setHtml(self.get_vtuber_placeholder_html())
        layout.addWidget(self.vtuber_view)
        
        # Status VTuber
        status_layout = QHBoxLayout()
        self.vtuber_status = QLabel("Status: Aguardando...")
        self.vtuber_status.setStyleSheet("color: #888;")
        status_layout.addWidget(self.vtuber_status)
        
        self.vtuber_expression = QLabel("Expressão: Neutro")
        self.vtuber_expression.setStyleSheet("color: #888;")
        status_layout.addWidget(self.vtuber_expression)
        
        layout.addLayout(status_layout)
        
        # Botões de teste
        buttons_layout = QHBoxLayout()
        
        expressions = ["😊 Feliz", "😢 Triste", "😮 Surpreso", "😐 Neutro"]
        for expr in expressions:
            btn = QPushButton(expr)
            btn.clicked.connect(lambda checked, e=expr: self.test_expression(e))
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        panel.setLayout(layout)
        return panel
    
    def get_vtuber_placeholder_html(self):
        """HTML placeholder para VTuber"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: Arial, sans-serif;
                }
                .avatar-container {
                    text-align: center;
                    color: white;
                }
                .avatar {
                    width: 200px;
                    height: 200px;
                    margin: 0 auto 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 50%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 100px;
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
                h1 { margin: 0; font-size: 32px; }
                p { margin: 10px 0; opacity: 0.8; }
            </style>
        </head>
        <body>
            <div class="avatar-container">
                <div class="avatar">🌸</div>
                <h1>Mirai</h1>
                <p>IA VTuber Assistente</p>
                <p style="font-size: 12px;">Configure VSeeFace para ver o modelo 3D</p>
            </div>
        </body>
        </html>
        """
    
    def create_tabs_panel(self):
        """Cria painel de abas"""
        tabs = QTabWidget()
        
        # Aba 1: Chat
        tabs.addTab(self.create_chat_tab(), "💬 Chat")
        
        # Aba 2: Comandos
        tabs.addTab(self.create_commands_tab(), "🎮 Comandos")
        
        # Aba 3: Configurações IA
        tabs.addTab(self.create_ai_config_tab(), "🤖 IA")
        
        # Aba 4: Configurações Voz
        tabs.addTab(self.create_voice_config_tab(), "🔊 Voz")
        
        # Aba 5: Configurações VTuber
        tabs.addTab(self.create_vtuber_config_tab(), "🎭 VTuber")
        
        # Aba 6: Sobre
        tabs.addTab(self.create_about_tab(), "ℹ️ Sobre")
        
        return tabs
    
    def create_chat_tab(self):
        """Cria aba de chat"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Área de conversa
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Conversa com a Mirai aparecerá aqui...")
        layout.addWidget(self.chat_display)
        
        # Entrada de texto
        input_layout = QHBoxLayout()
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Digite sua mensagem...")
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)
        
        # Botões
        send_btn = QPushButton("📤 Enviar")
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        voice_btn = QPushButton("🎤 Voz")
        voice_btn.clicked.connect(self.toggle_voice)
        voice_btn.setCheckable(True)
        self.voice_btn = voice_btn
        input_layout.addWidget(voice_btn)
        
        clear_btn = QPushButton("🗑️ Limpar")
        clear_btn.clicked.connect(self.clear_chat)
        input_layout.addWidget(clear_btn)
        
        layout.addLayout(input_layout)
        
        # Status
        self.chat_status = QLabel("Status: Pronto")
        self.chat_status.setStyleSheet("color: #888;")
        layout.addWidget(self.chat_status)
        
        tab.setLayout(layout)
        return tab
    
    def create_commands_tab(self):
        """Cria aba de comandos"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        commands_widget = QWidget()
        commands_layout = QVBoxLayout()
        
        # Grupos de comandos
        command_groups = {
            "🖥️ Aplicativos": [
                ("Abrir Chrome", "abrir chrome"),
                ("Abrir Spotify", "abrir spotify"),
                ("Abrir Discord", "abrir discord"),
                ("Abrir VSCode", "abrir vscode"),
            ],
            "🔍 Pesquisa": [
                ("Pesquisar Web", "pesquisar [termo]"),
                ("Me fala sobre", "me fala sobre [assunto]"),
            ],
            "📸 Tela": [
                ("Ver Tela", "ver tela"),
                ("Capturar Tela", "capturar tela"),
            ],
            "🎮 Jogos": [
                ("Jogar", "jogar"),
                ("Listar Jogos", "listar jogos"),
            ]
        }
        
        for group_name, commands in command_groups.items():
            group = QGroupBox(group_name)
            group_layout = QVBoxLayout()
            
            for cmd_name, cmd_text in commands:
                btn = QPushButton(cmd_name)
                btn.clicked.connect(lambda checked, txt=cmd_text: self.quick_command(txt))
                group_layout.addWidget(btn)
            
            group.setLayout(group_layout)
            commands_layout.addWidget(group)
        
        commands_widget.setLayout(commands_layout)
        scroll.setWidget(commands_widget)
        layout.addWidget(scroll)
        
        tab.setLayout(layout)
        return tab
    
    def create_ai_config_tab(self):
        """Cria aba de configuração da IA"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Seleção de modelo
        model_group = QGroupBox("🤖 Modelo de IA")
        model_layout = QVBoxLayout()
        
        self.ai_model_combo = QComboBox()
        self.ai_model_combo.addItems(["Gemini (Recomendado)", "Ollama (Local)", "Fallback (Offline)"])
        self.ai_model_combo.currentIndexChanged.connect(self.change_ai_model)
        model_layout.addWidget(QLabel("Modelo:"))
        model_layout.addWidget(self.ai_model_combo)
        
        # Status
        self.ai_status = QLabel("Status: Verificando...")
        self.ai_status.setStyleSheet("color: #888;")
        model_layout.addWidget(self.ai_status)
        
        # Teste
        test_btn = QPushButton("🧪 Testar IA")
        test_btn.clicked.connect(self.test_ai)
        model_layout.addWidget(test_btn)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Chave Gemini
        gemini_group = QGroupBox("🔑 Configuração Gemini")
        gemini_layout = QVBoxLayout()
        
        gemini_layout.addWidget(QLabel("Chave API:"))
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setPlaceholderText("Cole sua chave API do Gemini...")
        self.gemini_key_input.setEchoMode(QLineEdit.Password)
        gemini_layout.addWidget(self.gemini_key_input)
        
        save_key_btn = QPushButton("💾 Salvar Chave")
        save_key_btn.clicked.connect(self.save_gemini_key)
        gemini_layout.addWidget(save_key_btn)
        
        link_label = QLabel('<a href="https://makersuite.google.com/app/apikey">Obter chave gratuita</a>')
        link_label.setOpenExternalLinks(True)
        gemini_layout.addWidget(link_label)
        
        gemini_group.setLayout(gemini_layout)
        layout.addWidget(gemini_group)
        
        # Estatísticas
        stats_group = QGroupBox("📊 Estatísticas")
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel("Carregando...")
        stats_layout.addWidget(self.stats_label)
        
        refresh_btn = QPushButton("🔄 Atualizar")
        refresh_btn.clicked.connect(self.update_stats)
        stats_layout.addWidget(refresh_btn)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_voice_config_tab(self):
        """Cria aba de configuração de voz"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # TTS (Text-to-Speech)
        tts_group = QGroupBox("🔊 Síntese de Voz (TTS)")
        tts_layout = QVBoxLayout()
        
        # Volume
        tts_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.change_volume)
        tts_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("80%")
        tts_layout.addWidget(self.volume_label)
        
        # Teste TTS
        test_tts_btn = QPushButton("🧪 Testar Voz")
        test_tts_btn.clicked.connect(self.test_tts)
        tts_layout.addWidget(test_tts_btn)
        
        tts_group.setLayout(tts_layout)
        layout.addWidget(tts_group)
        
        # Reconhecimento de Voz
        stt_group = QGroupBox("🎤 Reconhecimento de Voz (STT)")
        stt_layout = QVBoxLayout()
        
        self.mic_status = QLabel("Status: Não inicializado")
        stt_layout.addWidget(self.mic_status)
        
        test_mic_btn = QPushButton("🧪 Testar Microfone")
        test_mic_btn.clicked.connect(self.test_microphone)
        stt_layout.addWidget(test_mic_btn)
        
        stt_group.setLayout(stt_layout)
        layout.addWidget(stt_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_vtuber_config_tab(self):
        """Cria aba de configuração VTuber"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Informações VRM
        info_group = QGroupBox("ℹ️ Informações")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "Para usar o modelo VRM 3D:\n\n"
            "1. Baixe VSeeFace: www.vseeface.icu\n"
            "2. Baixe um modelo VRM: hub.vroid.com\n"
            "3. No VSeeFace: Settings → Enable VMC Protocol\n"
            "4. Porta: 39539\n\n"
            "A Mirai se conectará automaticamente!"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Status VRM
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout()
        
        self.vrm_status_label = QLabel("Verificando...")
        status_layout.addWidget(self.vrm_status_label)
        
        reconnect_btn = QPushButton("🔄 Reconectar")
        reconnect_btn.clicked.connect(self.reconnect_vrm)
        status_layout.addWidget(reconnect_btn)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_about_tab(self):
        """Cria aba sobre"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        about_text = QLabel(
            "<h2>🌸 Mirai Desktop v2.0</h2>"
            "<p><b>IA VTuber Assistente 100% Gratuita</b></p>"
            "<p>Desenvolvida com:</p>"
            "<ul>"
            "<li>Python 3.10+</li>"
            "<li>PyQt5 (Interface)</li>"
            "<li>Gemini AI (IA)</li>"
            "<li>VSeeFace (VRM)</li>"
            "</ul>"
            "<p><b>Funcionalidades:</b></p>"
            "<ul>"
            "<li>✨ Conversa natural (texto e voz)</li>"
            "<li>🖥️ Controle de aplicativos</li>"
            "<li>🔍 Pesquisa web integrada</li>"
            "<li>📸 Análise de tela</li>"
            "<li>🎮 Integração com jogos (RetroArch)</li>"
            "<li>🎭 Modelo VRM 3D</li>"
            "</ul>"
            "<p><b>Licença:</b> MIT</p>"
            "<p><b>Versão:</b> 2.0.0</p>"
        )
        about_text.setWordWrap(True)
        layout.addWidget(about_text)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def apply_theme(self):
        """Aplica tema escuro"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    font-size: 13px;
                }
                QGroupBox {
                    border: 2px solid #444;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #667eea;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #764ba2;
                }
                QPushButton:pressed {
                    background-color: #5568d3;
                }
                QPushButton:checked {
                    background-color: #43a047;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                    border-radius: 4px;
                    padding: 5px;
                    color: #ffffff;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                    border-radius: 4px;
                }
                QTabBar::tab {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    padding: 10px 20px;
                    border: 1px solid #444;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #667eea;
                }
                QSlider::groove:horizontal {
                    height: 8px;
                    background: #2d2d2d;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #667eea;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
            """)
    
    def initialize_systems(self):
        """Inicializa sistemas da Mirai"""
        try:
            # Inicializa IA
            asyncio.run(self.ai.initialize())
            self.update_ai_status()
            
            # Inicializa Speaker
            self.speaker.initialize()
            
            # Inicializa Voice
            if self.voice.initialize():
                self.mic_status.setText("Status: ✅ Pronto")
            else:
                self.mic_status.setText("Status: ❌ Não disponível")
            
            # Inicializa VTuber
            asyncio.run(self.vtuber.initialize())
            self.update_vrm_status()
            
            # Carrega chave Gemini
            if self.ai.gemini_api_key:
                self.gemini_key_input.setText(self.ai.gemini_api_key)
            
            self.add_system_message("✅ Sistema inicializado com sucesso!")
            
        except Exception as e:
            self.add_system_message(f"❌ Erro na inicialização: {e}")
    
    def send_message(self):
        """Envia mensagem para IA"""
        text = self.chat_input.text().strip()
        if not text:
            return
        
        # Adiciona mensagem do usuário
        self.add_user_message(text)
        self.chat_input.clear()
        
        # Processa com IA
        self.chat_status.setText("Status: 🤔 Pensando...")
        
        # Thread para não travar UI
        self.ai_thread = AIThread(self.ai)
        self.ai_thread.set_input(text)
        self.ai_thread.response_ready.connect(self.on_ai_response)
        self.ai_thread.start()
    
    def on_ai_response(self, response):
        """Recebe resposta da IA"""
        self.add_mirai_message(response)
        self.chat_status.setText("Status: ✅ Pronto")
        
        # Fala a resposta
        try:
            self.speaker.speak_async(response)
        except:
            pass
        
        # Atualiza expressão VTuber
        if self.vtuber.is_active:
            try:
                asyncio.run(self.vtuber.set_emotion_from_text(response))
            except:
                pass
    
    def add_user_message(self, text):
        """Adiciona mensagem do usuário ao chat"""
        self.chat_display.append(f'<p style="color: #667eea;"><b>Você:</b> {text}</p>')
    
    def add_mirai_message(self, text):
        """Adiciona mensagem da Mirai ao chat"""
        self.chat_display.append(f'<p style="color: #764ba2;"><b>🌸 Mirai:</b> {text}</p>')
    
    def add_system_message(self, text):
        """Adiciona mensagem do sistema"""
        self.chat_display.append(f'<p style="color: #888;"><i>{text}</i></p>')
    
    def toggle_voice(self):
        """Ativa/desativa reconhecimento de voz"""
        if self.voice_btn.isChecked():
            # Inicia reconhecimento
            self.voice_thread = VoiceThread(self.voice)
            self.voice_thread.recognized.connect(self.on_voice_recognized)
            self.voice_thread.start()
            self.add_system_message("🎤 Reconhecimento de voz ativado!")
            self.chat_status.setText("Status: 🎤 Escutando...")
        else:
            # Para reconhecimento
            if self.voice_thread:
                self.voice_thread.stop()
                self.voice_thread = None
            self.add_system_message("🎤 Reconhecimento de voz desativado!")
            self.chat_status.setText("Status: ✅ Pronto")
    
    def on_voice_recognized(self, text):
        """Callback de voz reconhecida"""
        self.chat_input.setText(text)
        self.send_message()
    
    def clear_chat(self):
        """Limpa chat"""
        self.chat_display.clear()
        self.context.clear_context()
        self.add_system_message("Chat limpo!")
    
    def quick_command(self, command):
        """Executa comando rápido"""
        self.chat_input.setText(command)
        self.send_message()
    
    def change_ai_model(self, index):
        """Troca modelo de IA"""
        if index == 0:  # Gemini
            self.ai.use_gemini = True
            self.ai.use_ollama = False
        elif index == 1:  # Ollama
            self.ai.use_gemini = False
            self.ai.use_ollama = True
        else:  # Fallback
            self.ai.use_gemini = False
            self.ai.use_ollama = False
        
        self.update_ai_status()
        self.add_system_message(f"Modelo alterado: {self.ai_model_combo.currentText()}")
    
    def update_ai_status(self):
        """Atualiza status da IA"""
        if self.ai.use_gemini:
            self.ai_status.setText("Status: ✅ Gemini Ativo")
            self.ai_status.setStyleSheet("color: #43a047;")
        elif self.ai.use_ollama:
            self.ai_status.setText("Status: ✅ Ollama Ativo")
            self.ai_status.setStyleSheet("color: #43a047;")
        else:
            self.ai_status.setText("Status: ⚠️ Modo Offline")
            self.ai_status.setStyleSheet("color: #ff9800;")
    
    def test_ai(self):
        """Testa IA"""
        self.add_system_message("🧪 Testando IA...")
        self.chat_input.setText("Diga olá em uma frase curta")
        self.send_message()
    
    def save_gemini_key(self):
        """Salva chave Gemini"""
        key = self.gemini_key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Erro", "Digite uma chave válida!")
            return
        
        try:
            # Salva no arquivo
            key_path = Path("config/gemini_key.txt")
            key_path.parent.mkdir(exist_ok=True)
            with open(key_path, 'w') as f:
                f.write(key)
            
            # Atualiza na IA
            self.ai.gemini_api_key = key
            self.ai.use_gemini = True
            self.ai.use_ollama = False
            
            self.update_ai_status()
            QMessageBox.information(self, "Sucesso", "Chave Gemini salva com sucesso!")
            self.add_system_message("✅ Chave Gemini configurada!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar chave: {e}")
    
    def update_stats(self):
        """Atualiza estatísticas"""
        duration = self.context.get_session_duration()
        messages = len(self.context.conversation_history)
        
        stats = f"""
Sessão Atual:
• Duração: {duration // 60}m {duration % 60}s
• Mensagens: {messages}
• Estado: {self.state.get_state().value}

Sistema de IA:
• Gemini: {'✅' if self.ai.use_gemini else '❌'}
• Ollama: {'✅' if self.ai.use_ollama else '❌'}

Voz:
• TTS: {'✅' if self.speaker.enabled else '❌'}
• STT: {'✅' if self.voice.microphone else '❌'}

VTuber:
• VRM: {'✅' if self.vtuber.is_active else '❌'}
        """
        
        self.stats_label.setText(stats)
    
    def change_volume(self, value):
        """Altera volume"""
        volume = value / 100
        self.speaker.set_volume(volume)
        self.volume_label.setText(f"{value}%")
    
    def test_tts(self):
        """Testa TTS"""
        self.speaker.speak("Sistema de voz funcionando! Yatta!")
        self.add_system_message("🔊 Testando voz...")
    
    def test_microphone(self):
        """Testa microfone"""
        self.add_system_message("🎤 Fale agora!")
        text = self.voice.listen_once()
        if text:
            self.add_system_message(f"✅ Reconhecido: {text}")
        else:
            self.add_system_message("❌ Nada reconhecido")
    
    def test_expression(self, expr):
        """Testa expressão VTuber"""
        expr_map = {
            "😊 Feliz": "happy",
            "😢 Triste": "sad",
            "😮 Surpreso": "surprised",
            "😐 Neutro": "neutral"
        }
        
        expression = expr_map.get(expr, "neutral")
        
        if self.vtuber.is_active:
            asyncio.run(self.vtuber.set_expression(expression))
            self.vtuber_expression.setText(f"Expressão: {expr}")
            self.add_system_message(f"Expressão alterada: {expr}")
        else:
            self.add_system_message("❌ VTuber não está ativo")
    
    def update_vrm_status(self):
        """Atualiza status VRM"""
        if self.vtuber.is_active:
            self.vrm_status_label.setText("Status: ✅ Conectado (VSeeFace)")
            self.vrm_status_label.setStyleSheet("color: #43a047;")
            self.vtuber_status.setText("Status: ✅ Ativo")
            self.vtuber_status.setStyleSheet("color: #43a047;")
        else:
            self.vrm_status_label.setText("Status: ❌ Não conectado")
            self.vrm_status_label.setStyleSheet("color: #ff5252;")
            self.vtuber_status.setText("Status: ❌ Inativo")
            self.vtuber_status.setStyleSheet("color: #ff5252;")
    
    def reconnect_vrm(self):
        """Reconecta VRM"""
        self.add_system_message("🔄 Reconectando VTuber...")
        asyncio.run(self.vtuber.initialize())
        self.update_vrm_status()
    
    def closeEvent(self, event):
        """Evento de fechamento"""
        # Para threads
        if self.voice_thread:
            self.voice_thread.stop()
        
        # Encerra sistemas
        if self.vtuber:
            asyncio.run(self.vtuber.stop())
        
        event.accept()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    app.setApplicationName("Mirai Desktop")
    app.setStyle("Fusion")  # Estilo moderno
    
    window = MiraiDesktopApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
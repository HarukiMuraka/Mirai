from colorama import Fore, Style
import asyncio

class MainMenu:
    """Menu principal da Mirai - PORTA CORRIGIDA!"""
    
    def __init__(self, mirai_instance):
        self.mirai = mirai_instance
        self.running = True
    
    def print_menu(self):
        """Imprime o menu principal"""
        print(f"\n{Fore.MAGENTA}╔════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║          🌸 MIRAI 🌸           ║")
        print(f"{Fore.MAGENTA}║      IA VTuber Local v1.0      ║")
        print(f"{Fore.MAGENTA}╠════════════════════════════════╣")
        print(f"{Fore.CYAN}║ 1 ▶ Conversa                   ║")
        print(f"{Fore.CYAN}║ 2 ▶ Assistente IA              ║")
        print(f"{Fore.CYAN}║ 3 ▶ Gamer / Jogos              ║")
        print(f"{Fore.CYAN}║ 4 ▶ Observação & Análise       ║")
        print(f"{Fore.CYAN}║ 5 ▶ Modo Voz Ativo (Mãos-livres)║")
        print(f"{Fore.CYAN}║ 6 ▶ Streamer (Lives)           ║")
        print(f"{Fore.CYAN}║ 7 ▶ Sistema & Configurações    ║")
        print(f"{Fore.CYAN}║ 8 ▶ Sobre a Mirai              ║")
        print(f"{Fore.RED}║ 0 ▶ Sair                       ║")
        print(f"{Fore.MAGENTA}╚════════════════════════════════╝{Style.RESET_ALL}\n")
    
    async def show(self):
        """Mostra e gerencia o menu"""
        from modes.conversation import ConversationMode
        from modes.assistant import AssistantMode
        from modes.gamer import GamerMode
        from modes.observer import ObserverMode
        
        # Importa voice_active SE disponível
        try:
            from modes.voice_active import VoiceActiveMode
            VOICE_ACTIVE_OK = True
        except:
            VOICE_ACTIVE_OK = False
        
        # Importa streamer SE disponível
        try:
            from modes.streamer import StreamerMode
            STREAMER_OK = True
        except:
            STREAMER_OK = False
        
        while self.running:
            self.print_menu()
            
            choice = input(f"{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}")
            
            if choice == "1":
                mode = ConversationMode(self.mirai)
                await mode.enter()
                await mode.exit()
            
            elif choice == "2":
                mode = AssistantMode(self.mirai)
                await mode.enter()
                await mode.exit()
            
            elif choice == "3":
                mode = GamerMode(self.mirai)
                await mode.enter()
                await mode.exit()
            
            elif choice == "4":
                mode = ObserverMode(self.mirai)
                await mode.enter()
                await mode.exit()
            
            elif choice == "5":
                if VOICE_ACTIVE_OK:
                    mode = VoiceActiveMode(self.mirai)
                    await mode.enter()
                    await mode.exit()
                else:
                    print(f"{Fore.RED}❌ Modo Voz Ativo não disponível!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Instale: pip install SpeechRecognition pyaudio{Style.RESET_ALL}")
                    input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
            
            elif choice == "6":
                if STREAMER_OK:
                    mode = StreamerMode(self.mirai)
                    await mode.enter()
                    await mode.exit()
                else:
                    print(f"{Fore.RED}❌ Modo Streamer não disponível!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Arquivo modes/streamer.py não encontrado{Style.RESET_ALL}")
                    input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
            
            elif choice == "7":
                await self.show_settings_menu()
            
            elif choice == "8":
                self.show_about()
            
            elif choice == "0":
                self.running = False
                break
            
            else:
                print(f"{Fore.RED}Opção inválida! Tenta de novo, ne~{Style.RESET_ALL}")
    
    async def show_settings_menu(self):
        """Menu de configurações"""
        while True:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.MAGENTA}⚙️ SISTEMA & CONFIGURAÇÕES")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            print("1. 🔊 Configurações de Voz")
            print("2. 🤖 Configurações da IA")
            print("3. 🧪 Testar Ollama")
            print("4. 🗑️ Limpar Memória Temporária")
            print("5. 💾 Gerenciar Memória Permanente")
            print("6. 📊 Ver Estatísticas")
            print("7. 🔄 Reativar Ollama")
            print("0. ⬅️ Voltar")
            
            choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}")
            
            if choice == "1":
                self.settings_voice()
            elif choice == "2":
                self.settings_ia()
            elif choice == "3":
                await self.test_ollama()
            elif choice == "4":
                self.clear_memory()
            elif choice == "5":
                self.manage_permanent_memory()
            elif choice == "6":
                self.show_stats()
            elif choice == "7":
                await self.reactivate_ollama()
            elif choice == "0":
                break
    
    def settings_voice(self):
        """Configurações de voz"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}🔊 CONFIGURAÇÕES DE VOZ")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"Status: {'✓ Ativa' if self.mirai.speaker.enabled else '✗ Desativada'}")
        print(f"Volume: {self.mirai.speaker.voice_volume:.1f}")
        print(f"Sistema: gTTS (Google)")
        
        print(f"\n{Fore.YELLOW}Opções:{Style.RESET_ALL}")
        print("1. Ajustar volume")
        print("2. Testar voz")
        print("0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}")
        
        if choice == "1":
            try:
                volume = input(f"Novo volume (0.0-1.0): ")
                if volume:
                    self.mirai.speaker.set_volume(float(volume))
                    print(f"{Fore.GREEN}✓ Volume ajustado!{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Valor inválido!{Style.RESET_ALL}")
        
        elif choice == "2":
            print(f"\n{Fore.CYAN}Testando voz...{Style.RESET_ALL}")
            self.mirai.speaker.speak("Sistema de voz funcionando! Yatta!")
            print(f"{Fore.GREEN}✓ Teste concluído!{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    def settings_ia(self):
        """Configurações da IA"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}🤖 CONFIGURAÇÕES DA IA")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"Modo atual: {Fore.GREEN if self.mirai.ai.use_ollama else Fore.YELLOW}", end='')
        print(f"{'Ollama (IA Avançada)' if self.mirai.ai.use_ollama else 'Fallback (Respostas Base)'}{Style.RESET_ALL}")
        
        if self.mirai.ai.use_ollama:
            print(f"Modelo: {self.mirai.ai.ollama_model}")
            print(f"URL: {self.mirai.ai.ollama_url}")
            print(f"\n{Fore.GREEN}✓ Ollama funcionando perfeitamente!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️ Ollama não está ativo{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Para ativar:{Style.RESET_ALL}")
            print("1. Abra um terminal separado")
            print("2. Execute: ollama serve")
            print("3. Execute: ollama pull llama3")
            print("4. Use opção 6 no menu (Reativar Ollama)")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def test_ollama(self):
        """Testa Ollama - PORTA CORRETA!"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}🧪 TESTE OLLAMA")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        import requests
        
        try:
            # Teste 1: Conexão - PORTA CORRETA!
            print(f"{Fore.YELLOW}[1/3] Testando conexão na porta 11434...{Style.RESET_ALL}")
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}   ✓ Ollama rodando!{Style.RESET_ALL}")
                
                # Teste 2: Modelos
                print(f"\n{Fore.YELLOW}[2/3] Verificando modelos...{Style.RESET_ALL}")
                data = response.json()
                models = data.get('models', [])
                
                if models:
                    print(f"\n   Modelos instalados:")
                    for model in models:
                        name = model.get('name', 'unknown')
                        print(f"   • {name}")
                    
                    has_llama = any('llama3' in m.get('name', '').lower() for m in models)
                    
                    if has_llama:
                        print(f"\n{Fore.GREEN}   ✓ llama3 encontrado!{Style.RESET_ALL}")
                        
                        # Detecta qual versão
                        model_to_use = None
                        for model in models:
                            name = model.get('name', '')
                            if 'llama3' in name.lower():
                                model_to_use = name
                                break
                        
                        # Teste 3: Geração
                        print(f"\n{Fore.YELLOW}[3/3] Testando geração com {model_to_use}...{Style.RESET_ALL}")
                        
                        test_response = requests.post(
                            "http://localhost:11434/api/generate",
                            json={
                                'model': model_to_use,
                                'prompt': 'Responda apenas: funcionando',
                                'stream': False,
                                'options': {'num_predict': 10}
                            },
                            timeout=30
                        )
                        
                        if test_response.status_code == 200:
                            result = test_response.json()
                            answer = result.get('response', '').strip()
                            print(f"{Fore.GREEN}   ✓ Resposta recebida: {answer}{Style.RESET_ALL}")
                            print(f"\n{Fore.GREEN}{'='*60}")
                            print("✅ OLLAMA FUNCIONANDO PERFEITAMENTE!")
                            print(f"{'='*60}{Style.RESET_ALL}")
                            
                            # Ativa e atualiza modelo
                            self.mirai.ai.use_ollama = True
                            self.mirai.ai.ollama_model = model_to_use
                            print(f"\n{Fore.CYAN}✨ Mirai configurada para usar: {model_to_use}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}   ✗ Geração falhou (status: {test_response.status_code}){Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.RED}   ✗ llama3 não instalado!{Style.RESET_ALL}")
                        print(f"\n{Fore.CYAN}Execute: ollama pull llama3{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}   ✗ Nenhum modelo instalado!{Style.RESET_ALL}")
                    print(f"\n{Fore.CYAN}Execute: ollama pull llama3{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}   ✗ Erro HTTP: {response.status_code}{Style.RESET_ALL}")
        
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}   ✗ Ollama não está rodando!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'='*60}")
            print("📋 SOLUÇÃO PASSO A PASSO:")
            print(f"{'='*60}{Style.RESET_ALL}\n")
            print("1️⃣ Abra um NOVO terminal (CMD ou PowerShell)")
            print("2️⃣ Execute: ollama serve")
            print("3️⃣ DEIXE esse terminal ABERTO (não feche!)")
            print("4️⃣ Volte aqui e teste novamente")
            print(f"\n{Fore.YELLOW}💡 O Ollama precisa estar SEMPRE rodando em segundo plano!{Style.RESET_ALL}")
        
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}   ✗ Timeout (Ollama demorou muito){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Tente novamente ou reinicie o Ollama{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}   ✗ Erro: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def reactivate_ollama(self):
        """Tenta reativar Ollama - PORTA CORRETA!"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}🔄 REATIVAR OLLAMA")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Verificando Ollama na porta 11434...{Style.RESET_ALL}\n")
        
        import requests
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                has_llama = any('llama3' in m.get('name', '').lower() for m in models)
                
                if has_llama:
                    # Detecta modelo
                    for model in models:
                        name = model.get('name', '')
                        if 'llama3' in name.lower():
                            self.mirai.ai.ollama_model = name
                            break
                    
                    self.mirai.ai.use_ollama = True
                    print(f"{Fore.GREEN}✅ Ollama reativado com sucesso!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}   Modelo: {self.mirai.ai.ollama_model}{Style.RESET_ALL}")
                    self.mirai.speaker.speak("Ollama reativado! Yatta!")
                else:
                    print(f"{Fore.RED}❌ llama3 não encontrado{Style.RESET_ALL}")
                    print(f"\n{Fore.CYAN}Execute: ollama pull llama3{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Ollama não respondeu (status: {response.status_code}){Style.RESET_ALL}")
        
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}❌ Ollama offline{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Execute em outro terminal: ollama serve{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    def clear_memory(self):
        """Limpa memória"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}🗑️ LIMPAR MEMÓRIA")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        confirm = input(f"{Fore.YELLOW}Limpar histórico de conversas? (s/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 's':
            self.mirai.context.clear_context()
            if hasattr(self.mirai.ai, 'conversation_history'):
                self.mirai.ai.conversation_history = []
            print(f"{Fore.GREEN}✓ Memória limpa!{Style.RESET_ALL}")
            self.mirai.speaker.speak("Memória limpa!")
        else:
            print("Cancelado.")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    def show_stats(self):
        """Mostra estatísticas"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.MAGENTA}📊 ESTATÍSTICAS")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        duration = self.mirai.context.get_session_duration()
        messages = len(self.mirai.context.conversation_history)
        
        print(f"Sessão:")
        print(f"  Duração: {duration // 60}m {duration % 60}s")
        print(f"  Mensagens: {messages}")
        print(f"  Estado: {self.mirai.state.get_state().value}")
        
        print(f"\nIA:")
        print(f"  Modo: {Fore.GREEN if self.mirai.ai.use_ollama else Fore.YELLOW}", end='')
        print(f"{'Ollama' if self.mirai.ai.use_ollama else 'Fallback'}{Style.RESET_ALL}")
        
        if self.mirai.ai.use_ollama:
            print(f"  Modelo: {self.mirai.ai.ollama_model}")
            print(f"  URL: {self.mirai.ai.ollama_url}")
        
        print(f"\nVoz:")
        print(f"  Status: {Fore.GREEN if self.mirai.speaker.enabled else Fore.RED}", end='')
        print(f"{'Ativa' if self.mirai.speaker.enabled else 'Desativada'}{Style.RESET_ALL}")
        print(f"  Volume: {self.mirai.speaker.voice_volume:.1f}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    def show_about(self):
        """Sobre a Mirai"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"🌸 SOBRE A MIRAI")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Nome:{Style.RESET_ALL} Mirai")
        print(f"{Fore.CYAN}Versão:{Style.RESET_ALL} 1.0.0")
        print(f"{Fore.CYAN}Tipo:{Style.RESET_ALL} Assistente Virtual VTuber")
        
        print(f"\n{Fore.YELLOW}Personalidade:{Style.RESET_ALL}")
        print("  • Líder divertida e responsável")
        print("  • Debochada e nerd")
        print("  • Ansiosa mas esforçada")
        print("  • Extrovertida e amigável")
        
        print(f"\n{Fore.YELLOW}Gostos:{Style.RESET_ALL}")
        print("  • Minecraft, Genshin Impact, Honkai Star Rail")
        print("  • Tecnologia, programação e jogos")
        print("  • Conversar com você!")
        
        print(f"\n{Fore.YELLOW}Funcionalidades:{Style.RESET_ALL}")
        print("  • Conversa natural (Ollama ou Fallback)")
        print("  • Assistente com análise de tela")
        print("  • Jogos retrô (RetroArch)")
        print("  • Modo Voz Ativo (mãos-livres)")
        print("  • Streaming (YouTube + Twitch)")
        print("  • 100% local e privada")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
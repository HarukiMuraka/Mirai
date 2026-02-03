from colorama import Fore, Style
import asyncio
import json
from pathlib import Path


class MenuPrincipal:
    """Menu Principal Simplificado"""
    
    def __init__(self, mirai_instance):
        self.mirai = mirai_instance
        self.running = True
    
    def print_banner(self):
        """Banner da Mirai"""
        print(f"\n{Fore.MAGENTA}╔════════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║           🌸 MIRAI v2.0 🌸                ║")
        print(f"{Fore.MAGENTA}║      Assistente Virtual Completa          ║")
        print(f"{Fore.MAGENTA}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def print_menu(self):
        """Menu simplificado"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                MENU PRINCIPAL              ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════╣")
        print(f"{Fore.GREEN}║                                            ║")
        print(f"{Fore.GREEN}║  1 ▶ 🌸 INICIAR MIRAI                     ║")
        print(f"{Fore.GREEN}║      (Todos os recursos)                   ║")
        print(f"{Fore.GREEN}║                                            ║")
        print(f"{Fore.CYAN}║  2 ▶ ⚙️  CONFIGURAÇÕES                    ║")
        print(f"{Fore.CYAN}║      (IA, VRM, Voz, Sistema)               ║")
        print(f"{Fore.CYAN}║                                            ║")
        print(f"{Fore.YELLOW}║  3 ▶ ℹ️  SOBRE & AJUDA                    ║")
        print(f"{Fore.YELLOW}║                                            ║")
        print(f"{Fore.RED}║  0 ▶ 🚪 SAIR                               ║")
        print(f"{Fore.RED}║                                            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    async def show(self):
        """Mostra menu"""
        while self.running:
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Fore.GREEN}Escolha (0-3): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                # MODO PRINCIPAL (todos os recursos)
                await self.iniciar_mirai()
            
            elif choice == "2":
                # CONFIGURAÇÕES
                await self.configuracoes()
            
            elif choice == "3":
                # SOBRE
                self.sobre()
            
            elif choice == "0":
                # SAIR
                self.running = False
                break
            
            else:
                print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                await asyncio.sleep(1)
    
    async def iniciar_mirai(self):
        """Inicia modo principal"""
        from modes.modo_principal import ModoPrincipal
        
        modo = ModoPrincipal(self.mirai)
        await modo.enter()
        await modo.exit()
    
    async def configuracoes(self):
        """Menu de configurações"""
        while True:
            print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║              ⚙️  CONFIGURAÇÕES              ║")
            print(f"{Fore.CYAN}╠════════════════════════════════════════════╣")
            print(f"{Fore.YELLOW}║  1 ▶ 🤖 Configurar IA                      ║")
            print(f"{Fore.YELLOW}║  2 ▶ 🎭 Configurar VRM/Avatar              ║")
            print(f"{Fore.YELLOW}║  3 ▶ 🔊 Configurar Voz                     ║")
            print(f"{Fore.YELLOW}║  4 ▶ 🎮 Configurar Emuladores              ║")
            print(f"{Fore.YELLOW}║  5 ▶ 💾 Gerenciar Memória                  ║")
            print(f"{Fore.YELLOW}║  6 ▶ 📊 Ver Status do Sistema              ║")
            print(f"{Fore.CYAN}║  0 ▶ ⬅️  Voltar                            ║")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
            
            choice = input(f"{Fore.GREEN}Opção: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                await self.config_ia()
            elif choice == "2":
                await self.config_vrm()
            elif choice == "3":
                await self.config_voz()
            elif choice == "4":
                await self.config_emuladores()
            elif choice == "5":
                await self.gerenciar_memoria()
            elif choice == "6":
                await self.ver_status()
            elif choice == "0":
                break
    
    async def config_ia(self):
        """Configuração da IA"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║           🤖 CONFIGURAÇÃO DE IA            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        # Carrega config atual
        config_path = Path("config/ai.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {
                "model": {"name": "gemini", "temperature": 0.9},
                "personality": {"style": "casual", "use_japanese": True}
            }
        
        # Mostra config atual
        print(f"{Fore.YELLOW}Configuração Atual:{Style.RESET_ALL}\n")
        print(f"  Modelo: {config['model']['name']}")
        print(f"  Temperatura: {config['model']['temperature']}")
        print(f"  Estilo: {config['personality']['style']}")
        print(f"  Usa japonês: {config['personality']['use_japanese']}\n")
        
        print(f"{Fore.CYAN}Opções:{Style.RESET_ALL}")
        print("  1. Trocar modelo (gemini/ollama/local)")
        print("  2. Ajustar criatividade (temperatura)")
        print("  3. Mudar estilo de conversa")
        print("  4. Toggle japonês")
        print("  5. Configurar chave Gemini")
        print("  0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            print(f"\n{Fore.YELLOW}Modelos disponíveis:{Style.RESET_ALL}")
            print("  1. Gemini (recomendado - melhor qualidade)")
            print("  2. Ollama (local - privado)")
            print("  3. Local (offline - básico)")
            
            model_choice = input(f"\n{Fore.GREEN}Modelo: {Style.RESET_ALL}").strip()
            
            if model_choice == "1":
                config['model']['name'] = "gemini"
                print(f"{Fore.GREEN}✓ Modelo: Gemini{Style.RESET_ALL}")
            elif model_choice == "2":
                config['model']['name'] = "ollama"
                print(f"{Fore.GREEN}✓ Modelo: Ollama{Style.RESET_ALL}")
            elif model_choice == "3":
                config['model']['name'] = "local"
                print(f"{Fore.GREEN}✓ Modelo: Local{Style.RESET_ALL}")
        
        elif choice == "2":
            print(f"\n{Fore.YELLOW}Temperatura (0.0 = conservador, 1.0 = criativo):{Style.RESET_ALL}")
            temp = input(f"{Fore.GREEN}Valor (0.0-1.0): {Style.RESET_ALL}").strip()
            
            try:
                temp_val = float(temp)
                if 0.0 <= temp_val <= 1.0:
                    config['model']['temperature'] = temp_val
                    print(f"{Fore.GREEN}✓ Temperatura: {temp_val}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Valor inválido!{Style.RESET_ALL}")
        
        elif choice == "3":
            print(f"\n{Fore.YELLOW}Estilos:{Style.RESET_ALL}")
            print("  1. Casual (amigável)")
            print("  2. Formal (profissional)")
            print("  3. Fofo (kawaii)")
            
            style_choice = input(f"\n{Fore.GREEN}Estilo: {Style.RESET_ALL}").strip()
            
            styles = {"1": "casual", "2": "formal", "3": "kawaii"}
            if style_choice in styles:
                config['personality']['style'] = styles[style_choice]
                print(f"{Fore.GREEN}✓ Estilo: {styles[style_choice]}{Style.RESET_ALL}")
        
        elif choice == "4":
            current = config['personality']['use_japanese']
            config['personality']['use_japanese'] = not current
            status = "Ativado" if not current else "Desativado"
            print(f"{Fore.GREEN}✓ Japonês: {status}{Style.RESET_ALL}")
        
        elif choice == "5":
            print(f"\n{Fore.CYAN}Configurar Chave Gemini:{Style.RESET_ALL}\n")
            print("  1. Obtenha chave grátis: https://makersuite.google.com/app/apikey")
            print("  2. Cole abaixo:\n")
            
            key = input(f"{Fore.GREEN}Chave: {Style.RESET_ALL}").strip()
            
            if key:
                key_path = Path("config/gemini_key.txt")
                key_path.parent.mkdir(exist_ok=True)
                with open(key_path, 'w') as f:
                    f.write(key)
                print(f"{Fore.GREEN}✓ Chave salva!{Style.RESET_ALL}")
        
        # Salva config
        if choice in ["1", "2", "3", "4"]:
            config_path.parent.mkdir(exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"\n{Fore.GREEN}✓ Configurações salvas!{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def config_vrm(self):
        """Configuração VRM"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║         🎭 CONFIGURAÇÃO DE VRM             ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        config_path = Path("config/vtuber.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {
                "enabled": True,
                "engine": "vrm",
                "vmc_port": 39539
            }
        
        print(f"{Fore.YELLOW}Configuração Atual:{Style.RESET_ALL}\n")
        print(f"  VRM ativado: {config.get('enabled', True)}")
        print(f"  Engine: {config.get('engine', 'vrm')}")
        print(f"  Porta VMC: {config.get('vmc_port', 39539)}\n")
        
        print(f"{Fore.CYAN}Opções:{Style.RESET_ALL}")
        print("  1. Ativar/Desativar VRM")
        print("  2. Configurar porta VMC")
        print("  3. Testar conexão VSeeFace")
        print("  0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            config['enabled'] = not config.get('enabled', True)
            status = "Ativado" if config['enabled'] else "Desativado"
            print(f"{Fore.GREEN}✓ VRM: {status}{Style.RESET_ALL}")
        
        elif choice == "2":
            port = input(f"{Fore.GREEN}Porta VMC (padrão 39539): {Style.RESET_ALL}").strip()
            try:
                config['vmc_port'] = int(port)
                print(f"{Fore.GREEN}✓ Porta: {port}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Porta inválida!{Style.RESET_ALL}")
        
        elif choice == "3":
            print(f"\n{Fore.CYAN}Testando VSeeFace...{Style.RESET_ALL}")
            
            import socket
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.sendto(b"/VMC/Ok", ("127.0.0.1", config.get('vmc_port', 39539)))
                print(f"{Fore.GREEN}✓ VSeeFace detectado!{Style.RESET_ALL}")
            except:
                print(f"{Fore.YELLOW}✗ VSeeFace não detectado{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}Para usar VRM:{Style.RESET_ALL}")
                print("  1. Baixe VSeeFace: https://www.vseeface.icu")
                print("  2. Carregue modelo VRM")
                print("  3. Settings → Enable VMC Protocol")
        
        # Salva
        if choice in ["1", "2"]:
            config_path.parent.mkdir(exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"\n{Fore.GREEN}✓ Salvo!{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def config_voz(self):
        """Configuração de voz"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          🔊 CONFIGURAÇÃO DE VOZ            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Status:{Style.RESET_ALL}")
        print(f"  Voz: {'Ativa' if self.mirai.speaker.enabled else 'Desativada'}")
        print(f"  Volume: {self.mirai.speaker.voice_volume:.1f}")
        
        print(f"\n{Fore.CYAN}Opções:{Style.RESET_ALL}")
        print("  1. Ajustar volume")
        print("  2. Testar voz")
        print("  3. Ativar/Desativar")
        print("  0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            vol = input(f"{Fore.GREEN}Volume (0.0-1.0): {Style.RESET_ALL}").strip()
            try:
                self.mirai.speaker.set_volume(float(vol))
                print(f"{Fore.GREEN}✓ Volume ajustado!{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Valor inválido!{Style.RESET_ALL}")
        
        elif choice == "2":
            print(f"\n{Fore.CYAN}Testando voz...{Style.RESET_ALL}")
            self.mirai.speaker.speak("Sistema de voz funcionando perfeitamente! Yatta!")
            print(f"{Fore.GREEN}✓ Teste concluído!{Style.RESET_ALL}")
        
        elif choice == "3":
            self.mirai.speaker.enabled = not self.mirai.speaker.enabled
            status = "Ativada" if self.mirai.speaker.enabled else "Desativada"
            print(f"{Fore.GREEN}✓ Voz: {status}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def config_emuladores(self):
        """Config emuladores"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║        🎮 CONFIGURAR EMULADORES            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        # Verifica RetroArch
        retroarch_path = None
        paths = [
            "C:/RetroArch/retroarch.exe",
            "C:/Program Files/RetroArch/retroarch.exe"
        ]
        
        for path in paths:
            if Path(path).exists():
                retroarch_path = path
                break
        
        print(f"{Fore.YELLOW}Status:{Style.RESET_ALL}\n")
        
        if retroarch_path:
            print(f"{Fore.GREEN}✓ RetroArch: {retroarch_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ RetroArch não encontrado{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  Baixe: https://www.retroarch.com{Style.RESET_ALL}")
        
        # ROMs
        roms_path = Path("C:/Mirai/roms")
        print(f"\n  Pasta de ROMs: {roms_path}")
        print(f"  Existe: {'Sim' if roms_path.exists() else 'Não'}")
        
        if not roms_path.exists():
            print(f"\n{Fore.YELLOW}Deseja criar pasta de ROMs?{Style.RESET_ALL}")
            if input(f"{Fore.GREEN}(s/n): {Style.RESET_ALL}").lower() == 's':
                roms_path.mkdir(parents=True, exist_ok=True)
                print(f"{Fore.GREEN}✓ Pasta criada!{Style.RESET_ALL}")
        
        # Cores
        print(f"\n{Fore.CYAN}Cores necessários no RetroArch:{Style.RESET_ALL}")
        cores = [
            "NES: fceumm",
            "SNES: snes9x",
            "GBA: mgba",
            "N64: mupen64plus_next",
            "PS1: pcsx_rearmed",
            "3DS: citra",  # Citra core
            "NDS: desmume"
        ]
        
        for core in cores:
            print(f"  • {core}")
        
        print(f"\n{Fore.YELLOW}Instale cores pelo RetroArch:{Style.RESET_ALL}")
        print("  Online Updater → Core Downloader")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def gerenciar_memoria(self):
        """Gerenciar memória"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          💾 GERENCIAR MEMÓRIA              ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Opções:{Style.RESET_ALL}")
        print("  1. Ver estatísticas")
        print("  2. Limpar memória temporária")
        print("  3. Backup de memória")
        print("  0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Opção: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Stats
            messages = len(self.mirai.context.conversation_history)
            duration = self.mirai.context.get_session_duration()
            
            print(f"\n{Fore.CYAN}Estatísticas:{Style.RESET_ALL}")
            print(f"  Mensagens: {messages}")
            print(f"  Duração: {duration//60}m {duration%60}s")
            print(f"  Estado: {self.mirai.state.current_state.value}")
        
        elif choice == "2":
            print(f"\n{Fore.YELLOW}Limpar memória temporária?{Style.RESET_ALL}")
            if input(f"{Fore.GREEN}(s/n): {Style.RESET_ALL}").lower() == 's':
                self.mirai.context.clear_context()
                print(f"{Fore.GREEN}✓ Memória limpa!{Style.RESET_ALL}")
        
        elif choice == "3":
            print(f"{Fore.CYAN}Função de backup não implementada ainda{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    async def ver_status(self):
        """Status do sistema"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║           📊 STATUS DO SISTEMA             ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        # IA
        print(f"{Fore.YELLOW}🤖 IA:{Style.RESET_ALL}")
        if hasattr(self.mirai.ai, 'use_gemini'):
            if self.mirai.ai.use_gemini:
                print(f"  {Fore.GREEN}✓ Gemini ativo{Style.RESET_ALL}")
            elif hasattr(self.mirai.ai, 'use_ollama') and self.mirai.ai.use_ollama:
                print(f"  {Fore.GREEN}✓ Ollama ativo{Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}○ Modo offline{Style.RESET_ALL}")
        
        # Voz
        print(f"\n{Fore.YELLOW}🔊 Voz:{Style.RESET_ALL}")
        print(f"  {'✓ Ativa' if self.mirai.speaker.enabled else '✗ Desativada'}")
        
        # VRM
        print(f"\n{Fore.YELLOW}🎭 VRM:{Style.RESET_ALL}")
        if self.mirai.vtuber and self.mirai.vtuber.is_active:
            print(f"  {Fore.GREEN}✓ VSeeFace conectado{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}○ VSeeFace não conectado{Style.RESET_ALL}")
        
        # Sessão
        print(f"\n{Fore.YELLOW}📊 Sessão:{Style.RESET_ALL}")
        duration = self.mirai.context.get_session_duration()
        messages = len(self.mirai.context.conversation_history)
        print(f"  Duração: {duration//60}m {duration%60}s")
        print(f"  Mensagens: {messages}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
    
    def sobre(self):
        """Sobre a Mirai"""
        print(f"\n{Fore.MAGENTA}╔════════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║           🌸 SOBRE A MIRAI 🌸              ║")
        print(f"{Fore.MAGENTA}╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}MIRAI v2.0 - Assistente Virtual Completa{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Recursos:{Style.RESET_ALL}")
        print("  ✅ Conversa natural (texto/voz)")
        print("  ✅ Análise de imagem com seleção de área")
        print("  ✅ OCR completo (extração de texto)")
        print("  ✅ Emuladores (RetroArch com Citra 3DS)")
        print("  ✅ Modo mãos-livres")
        print("  ✅ Assistente inteligente")
        print("  ✅ VTuber (VRM/VSeeFace)")
        
        print(f"\n{Fore.YELLOW}IAs Suportadas:{Style.RESET_ALL}")
        print("  • Gemini (recomendado)")
        print("  • Ollama (local)")
        print("  • Modo offline")
        
        print(f"\n{Fore.YELLOW}Emuladores:{Style.RESET_ALL}")
        print("  • NES, SNES, GBA")
        print("  • N64, PS1, Genesis")
        print("  • Nintendo 3DS (Citra)")
        print("  • Nintendo DS")
        
        print(f"\n{Fore.CYAN}Desenvolvido com ❤️ pela comunidade{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter...{Style.RESET_ALL}")
import asyncio
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab
from colorama import Fore, Style
from datetime import datetime
from pathlib import Path
import pytesseract
import subprocess
import threading
import os
from typing import Dict, List, Any, Optional, Tuple

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ModoPrincipal:
    """Modo Principal Unificado - CORRIGIDO"""
    
    def __init__(self, mirai_instance: Any) -> None:
        self.mirai = mirai_instance
        self.ai = mirai_instance.ai
        self.context = mirai_instance.context
        self.state = mirai_instance.state
        self.vtuber = mirai_instance.vtuber
        self.speaker = mirai_instance.speaker
        self.is_active: bool = False
        
        # Importa dinamicamente
        from perception.text_input import TextInput
        from perception.voice_listener import VoiceListener
        
        self.text_input = TextInput()
        self.voice_listener = VoiceListener()
        
        # Emuladores
        self.retroarch_path: Optional[str] = self._find_retroarch()
        self.roms_path = Path("C:/Mirai/roms")
        self.current_game: Optional[Dict[str, Any]] = None
        self.game_process: Optional[subprocess.Popen] = None
        
        # Cores RetroArch
        self.cores_config: Dict[str, str] = {
            'nes': 'fceumm_libretro.dll',
            'snes': 'snes9x_libretro.dll',
            'gba': 'mgba_libretro.dll',
            'n64': 'mupen64plus_next_libretro.dll',
            'ps1': 'pcsx_rearmed_libretro.dll',
            'genesis': 'genesis_plus_gx_libretro.dll',
            '3ds': 'citra_libretro.dll',
            'nds': 'desmume_libretro.dll'
        }
    
    def _find_retroarch(self) -> Optional[str]:
        """Procura RetroArch"""
        paths = [
            "C:/RetroArch/retroarch.exe",
            "C:/Program Files/RetroArch/retroarch.exe",
            "C:/Program Files (x86)/RetroArch/retroarch.exe",
            os.path.expanduser("~/RetroArch/retroarch.exe")
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        return None
    
    async def enter(self) -> None:
        """Entra no modo principal"""
        self.is_active = True
        self.state.set_state("principal")
        
        if hasattr(self.voice_listener, 'initialize'):
            self.voice_listener.initialize()
        
        self.print_header()
        await self.menu_principal()
    
    def print_header(self) -> None:
        """Header"""
        print(f"\n{Fore.MAGENTA}╔════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║      🌸 MIRAI - MODO PRINCIPAL 🌸     ║")
        print(f"{Fore.MAGENTA}║   Assistente Virtual Completa v2.0     ║")
        print(f"{Fore.MAGENTA}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    async def menu_principal(self) -> None:
        """Menu principal"""
        while self.is_active:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}O que você gostaria de fazer?{Style.RESET_ALL}\n")
            
            print(f"{Fore.CYAN}💬 CONVERSA:{Style.RESET_ALL}")
            print("  1. Conversar por texto")
            print("  2. Conversar por voz")
            print("  3. Modo autônomo")
            
            print(f"\n{Fore.CYAN}👁️ VISÃO & ANÁLISE:{Style.RESET_ALL}")
            print("  4. Analisar tela completa")
            print("  5. Selecionar área e analisar ⭐")
            print("  6. Monitoramento contínuo")
            print("  7. Ler texto da tela (OCR)")
            
            print(f"\n{Fore.CYAN}🎮 JOGOS:{Style.RESET_ALL}")
            print("  8. Jogar (RetroArch)")
            
            print(f"\n{Fore.CYAN}🤖 ASSISTENTE:{Style.RESET_ALL}")
            print("  9. Abrir aplicativo")
            print("  10. Pesquisar na web")
            print("  11. Criar conteúdo")
            
            print(f"\n{Fore.CYAN}🎤 VOZ ATIVA:{Style.RESET_ALL}")
            print("  12. Modo mãos-livres")
            
            print(f"\n{Fore.RED}  0. Voltar{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.GREEN}Escolha (0-12): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                await self.conversa_texto()
            elif choice == "2":
                await self.conversa_voz()
            elif choice == "3":
                await self.modo_autonomo()
            elif choice == "4":
                await self.analisar_tela_completa()
            elif choice == "5":
                await self.selecionar_e_analisar()
            elif choice == "6":
                await self.monitoramento_continuo()
            elif choice == "7":
                await self.ler_texto_tela()
            elif choice == "8":
                await self.menu_jogos()
            elif choice == "9":
                await self.abrir_aplicativo()
            elif choice == "10":
                await self.pesquisar_web()
            elif choice == "11":
                await self.criar_conteudo()
            elif choice == "12":
                await self.modo_maos_livres()
            elif choice == "0":
                break
    
    # CONVERSA
    async def conversa_texto(self) -> None:
        """Conversa texto"""
        print(f"\n{Fore.GREEN}💬 Conversa por Texto{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(Digite 'sair' para voltar){Style.RESET_ALL}\n")
        
        while True:
            user_input = self.text_input.get_input(f"{Fore.CYAN}Você: {Style.RESET_ALL}")
            
            if not user_input or user_input.lower() in ['sair', 'exit', 'voltar']:
                break
            
            response = await self._processar_mensagem(user_input, False)
            
            if response:
                print(f"{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
                asyncio.create_task(self._falar_async(response))
    
    async def conversa_voz(self) -> None:
        """Conversa voz"""
        print(f"\n{Fore.GREEN}🎤 Conversa por Voz{Style.RESET_ALL}\n")
        
        while True:
            text = self.voice_listener.listen_once()
            
            if not text:
                continue
            
            if text.lower() in ['sair', 'exit', 'parar']:
                break
            
            print(f"{Fore.CYAN}Você: {text}{Style.RESET_ALL}")
            
            response = await self._processar_mensagem(text, True)
            
            if response:
                print(f"{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
                self.speaker.speak(response)
    
    async def modo_autonomo(self) -> None:
        """Modo autônomo"""
        print(f"\n{Fore.GREEN}🤖 Modo Autônomo{Style.RESET_ALL}\n")
        self.speaker.speak("Modo autônomo ativado!")
        
        try:
            while True:
                await asyncio.sleep(5)
                
                if self.ai.should_take_initiative():
                    initiative = self.ai.generate_initiative()
                    print(f"\n{Fore.MAGENTA}Mirai: {initiative}{Style.RESET_ALL}\n")
                    self.speaker.speak(initiative)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Modo encerrado{Style.RESET_ALL}")
    
    # ANÁLISE
    async def analisar_tela_completa(self) -> None:
        """Análise completa"""
        print(f"\n{Fore.CYAN}📸 Capturando em 2s...{Style.RESET_ALL}")
        await asyncio.sleep(2)
        
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        
        print(f"{Fore.CYAN}Analisando...{Style.RESET_ALL}")
        
        # OCR
        text = pytesseract.image_to_string(screenshot, lang='por+eng')
        words = len(text.split())
        
        print(f"\n{Fore.GREEN}✓ Análise:{Style.RESET_ALL}")
        print(f"  Palavras: {words}")
        print(f"  Salvo: {filename}\n")
        
        prompt = f"Analise brevemente: imagem capturada com {words} palavras detectadas."
        response = await self._processar_mensagem(prompt, False)
        
        print(f"{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
        self.speaker.speak(response[:150])
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    async def selecionar_e_analisar(self) -> None:
        """Seleção de área"""
        print(f"\n{Fore.CYAN}🎯 Seleção de Área{Style.RESET_ALL}\n")
        print("Instruções: Clique e arraste | ENTER=OK | ESC=Cancelar\n")
        
        input(f"{Fore.GREEN}Enter para começar...{Style.RESET_ALL}")
        
        try:
            screenshot = ImageGrab.grab()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            start_point: Optional[Tuple[int, int]] = None
            end_point: Optional[Tuple[int, int]] = None
            current_img = screenshot_cv.copy()
            
            def select_area(event: int, x: int, y: int, flags: int, param: Any) -> None:
                nonlocal start_point, end_point, current_img
                
                if event == cv2.EVENT_LBUTTONDOWN:
                    start_point = (x, y)
                elif event == cv2.EVENT_MOUSEMOVE and start_point:
                    end_point = (x, y)
                    current_img = screenshot_cv.copy()
                    cv2.rectangle(current_img, start_point, end_point, (0, 255, 0), 2)
                elif event == cv2.EVENT_LBUTTONUP:
                    end_point = (x, y)
            
            window_name = 'Selecione - ENTER=OK | ESC=Cancelar'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window_name, select_area)
            
            while True:
                cv2.imshow(window_name, current_img)
                key = cv2.waitKey(1) & 0xFF
                
                if key == 13:
                    break
                elif key == 27:
                    cv2.destroyAllWindows()
                    print(f"{Fore.YELLOW}Cancelado{Style.RESET_ALL}")
                    return
            
            cv2.destroyAllWindows()
            
            if start_point and end_point:
                x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
                x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])
                
                selected = screenshot.crop((x1, y1, x2, y2))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"area_{timestamp}.png"
                selected.save(filename)
                
                print(f"\n{Fore.GREEN}✓ Área: {x2-x1}x{y2-y1}px{Style.RESET_ALL}")
                
                # OCR
                text = pytesseract.image_to_string(selected, lang='por+eng')
                words = len(text.split())
                
                print(f"  Palavras: {words}")
                print(f"  Salvo: {filename}\n")
                
                if text.strip():
                    print(f"{Fore.CYAN}Texto:{Style.RESET_ALL}\n{text[:200]}...\n")
                
                prompt = f"Analise: área {x2-x1}x{y2-y1}px com {words} palavras. Texto: {text[:100]}"
                response = await self._processar_mensagem(prompt, False)
                
                print(f"{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
                self.speaker.speak(response[:150])
        
        except Exception as e:
            print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    async def monitoramento_continuo(self) -> None:
        """Monitoramento"""
        print(f"\n{Fore.CYAN}👁️ Monitoramento{Style.RESET_ALL}\n")
        
        interval_str = input(f"{Fore.YELLOW}Intervalo (s, padrão=10): {Style.RESET_ALL}").strip()
        interval = int(interval_str) if interval_str.isdigit() else 10
        
        print(f"\n{Fore.GREEN}✓ Monitorando a cada {interval}s (Ctrl+C=parar){Style.RESET_ALL}\n")
        
        try:
            while True:
                timestamp = datetime.now().strftime("%H:%M:%S")
                screenshot = pyautogui.screenshot()
                text = pytesseract.image_to_string(screenshot, lang='por')
                words = len(text.split())
                
                print(f"{Fore.CYAN}[{timestamp}] Palavras: {words:4d}{Style.RESET_ALL}")
                
                await asyncio.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}✓ Encerrado{Style.RESET_ALL}")
    
    async def ler_texto_tela(self) -> None:
        """OCR"""
        print(f"\n{Fore.CYAN}📝 Leitura de Texto{Style.RESET_ALL}\n")
        await asyncio.sleep(2)
        
        screenshot = pyautogui.screenshot()
        text = pytesseract.image_to_string(screenshot, lang='por+eng')
        
        if text.strip():
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            
            print(f"{Fore.GREEN}✓ {len(lines)} linhas{Style.RESET_ALL}\n")
            
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:2d}. {line}")
            
            with open('texto_extraido.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"\n{Fore.GREEN}✓ Salvo: texto_extraido.txt{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Nenhum texto{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    # JOGOS
    async def menu_jogos(self) -> None:
        """Menu jogos"""
        if not self.retroarch_path:
            print(f"\n{Fore.RED}RetroArch não encontrado{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
            return
        
        roms = self._list_roms()
        
        if not roms:
            print(f"\n{Fore.YELLOW}Nenhum jogo encontrado{Style.RESET_ALL}\n")
            input(f"{Fore.CYAN}Enter...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🎮 JOGOS:{Style.RESET_ALL}\n")
        
        for i, rom in enumerate(roms, 1):
            print(f"  {i}. [{rom['console'].upper()}] {rom['name']}")
        
        print(f"\n  0. Voltar")
        
        choice = input(f"\n{Fore.GREEN}Jogo: {Style.RESET_ALL}").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(roms):
                await self.launch_game(roms[idx])
    
    def _list_roms(self) -> List[Dict[str, Any]]:
        """Lista ROMs"""
        roms: List[Dict[str, Any]] = []
        
        if not self.roms_path.exists():
            return roms
        
        for console, core in self.cores_config.items():
            console_path = self.roms_path / console
            if console_path.exists():
                for rom in console_path.glob("*.*"):
                    roms.append({
                        'console': console,
                        'name': rom.stem,
                        'path': str(rom),
                        'core': core
                    })
        
        return sorted(roms, key=lambda x: x['name'])
    
    async def launch_game(self, game: Dict[str, Any]) -> None:
        """Lança jogo"""
        print(f"\n{Fore.CYAN}🎮 Iniciando {game['name']}...{Style.RESET_ALL}")
        self.speaker.speak(f"Iniciando {game['name']}!")
        
        try:
            cmd = [str(self.retroarch_path), "-L", game['core'], game['path']]
            self.game_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            await asyncio.sleep(3)
            
            if self.game_process.poll() is None:
                print(f"{Fore.GREEN}✓ Jogo iniciado!{Style.RESET_ALL}\n")
                self.game_process.wait()
                print(f"\n{Fore.YELLOW}Jogo encerrado{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    # ASSISTENTE
    async def abrir_aplicativo(self) -> None:
        """Abre app"""
        print(f"\n{Fore.CYAN}🚀 Abrir App{Style.RESET_ALL}\n")
        
        apps = {
            '1': ('Chrome', 'chrome'),
            '2': ('Firefox', 'firefox'),
            '3': ('VS Code', 'code')
        }
        
        for k, (name, _) in apps.items():
            print(f"  {k}. {name}")
        
        choice = input(f"\n{Fore.GREEN}App: {Style.RESET_ALL}").strip()
        
        if choice in apps:
            name, cmd = apps[choice]
            try:
                subprocess.Popen([cmd], shell=True)
                print(f"{Fore.GREEN}✓ {name} aberto{Style.RESET_ALL}")
                self.speaker.speak(f"{name} aberto!")
            except Exception:
                print(f"{Fore.RED}Erro{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    async def pesquisar_web(self) -> None:
        """Pesquisa"""
        print(f"\n{Fore.CYAN}🔍 Pesquisa{Style.RESET_ALL}\n")
        
        query = input(f"{Fore.GREEN}Pesquisar: {Style.RESET_ALL}").strip()
        
        if query:
            response = await self._processar_mensagem(f"Pesquise: {query}", True)
            print(f"\n{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
            self.speaker.speak(response[:150])
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    async def criar_conteudo(self) -> None:
        """Cria conteúdo"""
        print(f"\n{Fore.CYAN}✏️ Criar Conteúdo{Style.RESET_ALL}\n")
        
        topic = input(f"{Fore.GREEN}Sobre: {Style.RESET_ALL}").strip()
        
        if topic:
            response = await self._processar_mensagem(f"Crie texto sobre: {topic}", False)
            print(f"\n{Fore.MAGENTA}Mirai:{Style.RESET_ALL}\n{response}\n")
        
        input(f"\n{Fore.CYAN}Enter...{Style.RESET_ALL}")
    
    # VOZ MÃOS-LIVRES
    async def modo_maos_livres(self) -> None:
        """Mãos-livres"""
        print(f"\n{Fore.GREEN}🎤 Modo Mãos-Livres{Style.RESET_ALL}\n")
        self.speaker.speak("Modo mãos-livres! Diga Mirai para ativar.")
        
        wake_words = ['mirai', 'hey mirai']
        
        try:
            while True:
                text = self.voice_listener.listen_once_silent()
                
                if text and any(w in text.lower() for w in wake_words):
                    print(f"{Fore.GREEN}ATIVADA!{Style.RESET_ALL}")
                    self.speaker.speak("Oi!")
                    
                    command = self.voice_listener.listen_once()
                    
                    if command:
                        if command.lower() in ['parar', 'sair']:
                            self.speaker.speak("Desativando!")
                            break
                        
                        print(f"{Fore.CYAN}Você: {command}{Style.RESET_ALL}")
                        response = await self._processar_mensagem(command, True)
                        print(f"{Fore.MAGENTA}Mirai: {response}{Style.RESET_ALL}\n")
                        self.speaker.speak(response)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Encerrado{Style.RESET_ALL}")
    
    # PROCESSAMENTO
    async def _processar_mensagem(self, text: str, enable_search: bool) -> str:
        """Processa mensagem"""
        self.context.add_message("user", text)
        response = self.ai.generate_response(text, mode="principal", enable_search=enable_search)
        self.context.add_message("assistant", response)
        return response
    
    async def _falar_async(self, text: str) -> None:
        """Fala async"""
        if len(text) > 200:
            text = text[:200]
        threading.Thread(target=self.speaker.speak, args=(text,), daemon=True).start()
    
    async def exit(self) -> None:
        """Sai"""
        self.is_active = False
        if self.game_process:
            try:
                self.game_process.terminate()
            except Exception:
                pass
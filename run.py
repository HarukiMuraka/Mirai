#!/usr/bin/env python3
"""
Mirai Launcher

Inicia a assistente virtual Mirai
"""

import sys
import asyncio
from pathlib import Path

# Adiciona pasta mirai ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importa a função main
from mirai.main import main

if __name__ == "__main__":
    # Executa a função async corretamente
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
        sys.exit(0)
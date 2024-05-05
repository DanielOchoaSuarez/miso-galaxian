import asyncio

from src.engine.game_engine import GameEngine

if __name__ == '__main__':
    engine = GameEngine()
    asyncio.run(engine.run('MENU_SCENE'))

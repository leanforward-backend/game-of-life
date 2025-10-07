import pygame
import asyncio
import random
import sys

pygame.init()


COLOR_SCHEMES = [
    {
        "name": "Simple",
        "background": (0, 0, 0),
        "cell": (255, 255, 255),
        "grid": (0, 0, 0)
    },
    {
        "name": "Dark Mode",
        "background": (20, 20, 30),
        "cell": (100, 200, 255),
        "grid": (60, 60, 80)
    },
    {
        "name": "Matrix",
        "background": (0, 0, 0),
        "cell": (0, 255, 0),
        "grid": (0, 100, 0)
    },
    {
        "name": "Sunset",
        "background": (25, 10, 50),
        "cell": (255, 100, 100),
        "grid": (100, 50, 100)
    },
    {
        "name": "Ocean",
        "background": (10, 20, 40),
        "cell": (0, 200, 255),
        "grid": (40, 80, 120)
    },
    {
        "name": "Classic",
        "background": (0, 0, 0),
        "cell": (0, 255, 255),
        "grid": (255, 255, 255)
    },
    {
        "name": "Winter",
        "background": (20, 20, 40),
        "cell": (255, 255, 255),
        "grid": (60, 60, 80)
    },
    {
        "name": "pink",
        "background": (255, 55, 55),
        "cell": (255, 155, 155),
        "grid": (255, 100, 100)
    }

]

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def setup_web_buttons():
    """Add HTML buttons for web builds that inject keyboard events"""
    if sys.platform == "emscripten":
        try:
            import platform
            
            platform.window.eval("""
                const style = document.createElement('style');
                style.innerHTML = `
                    #game-controls {
                        position: absolute;
                        top: 10px;
                        left: 50%;
                        transform: translateX(-50%);
                        z-index: 1000;
                        display: flex;
                        gap: 10px;
                        flex-wrap: wrap;
                        justify-content: center;
                        max-width: 90%;
                    }
                    .game-btn {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 14px;
                        margin: 2px;
                        cursor: pointer;
                        border-radius: 5px;
                        font-weight: bold;
                        transition: background-color 0.3s;
                    }
                    .game-btn:hover {
                        background-color: #45a049;
                    }
                    .game-btn:active {
                        background-color: #3d8b40;
                        transform: translateY(1px);
                    }
                    .game-btn.pause {
                        background-color: #ff9800;
                    }
                    .game-btn.pause:hover {
                        background-color: #e68900;
                    }
                    .game-btn.clear {
                        background-color: #f44336;
                    }
                    .game-btn.clear:hover {
                        background-color: #da190b;
                    }
                    .game-btn.theme {
                        background-color: #9c27b0;
                    }
                    .game-btn.theme:hover {
                        background-color: #7b1fa2;
                    }
                    .game-btn.speed {
                        background-color: #2196F3;
                    }
                    .game-btn.speed:hover {
                        background-color: #0b7dda;
                    }
                `;
                document.head.appendChild(style);
            """)
            
            platform.window.eval("""
                const controlsDiv = document.createElement('div');
                controlsDiv.id = 'game-controls';
                controlsDiv.innerHTML = `
                    <button class="game-btn pause" onclick="simulateKey('Space')">Play/Pause</button>
                    <button class="game-btn clear" onclick="simulateKey('KeyC')">Clear</button>
                    <button class="game-btn" onclick="simulateKey('KeyG')">Generate</button>
                    <button class="game-btn theme" onclick="simulateKey('KeyT')">Theme</button>
                    <button class="game-btn speed" onclick="simulateKey('KeyR')">Slower</button>
                    <button class="game-btn speed" onclick="simulateKey('KeyE')">Faster</button>
                `;
                document.body.insertBefore(controlsDiv, document.body.firstChild);
                
                window.simulateKey = function(keyCode) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    const canvas = document.getElementById('canvas');
                    
                    const keydownEvent = new KeyboardEvent('keydown', {
                        code: keyCode,
                        key: keyCode === 'Space' ? ' ' : keyCode.replace('Key', '').toLowerCase(),
                        keyCode: keyCode === 'Space' ? 32 : keyCode.charCodeAt(keyCode.length - 1),
                        which: keyCode === 'Space' ? 32 : keyCode.charCodeAt(keyCode.length - 1),
                        bubbles: true,
                        cancelable: true,
                        composed: true
                    });
                    
                    document.dispatchEvent(keydownEvent);
                    canvas.dispatchEvent(keydownEvent);
                    
                    setTimeout(() => {
                        const keyupEvent = new KeyboardEvent('keyup', {
                            code: keyCode,
                            key: keyCode === 'Space' ? ' ' : keyCode.replace('Key', '').toLowerCase(),
                            keyCode: keyCode === 'Space' ? 32 : keyCode.charCodeAt(keyCode.length - 1),
                            which: keyCode === 'Space' ? 32 : keyCode.charCodeAt(keyCode.length - 1),
                            bubbles: true,
                            cancelable: true,
                            composed: true
                        });
                        document.dispatchEvent(keyupEvent);
                        canvas.dispatchEvent(keyupEvent);
                    }, 50);
                };
            """)
        except Exception as e:
            print(f"Could not setup web buttons: {e}")

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions, color_scheme):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, color_scheme["cell"], (*top_left, TILE_SIZE, TILE_SIZE))
        
    if color_scheme["grid"] != color_scheme["background"]:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(screen, color_scheme["grid"], (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, color_scheme["grid"], (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2,3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions

def get_neighbors(pos):
    x,y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x +dx > GRID_WIDTH:
            continue
        for dy in [-1,0,1]:
            if y + dy < 0 or y +dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))  


    return neighbors          

async def main():
    setup_web_buttons()
    
    running = True
    playing = False
    count = 0
    update_freq = 30
    current_scheme = 0

    positions = set()
    positions.add((GRID_WIDTH/2, GRID_HEIGHT/2))

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        scheme_name = COLOR_SCHEMES[current_scheme]["name"]
        pygame.display.set_caption(f"{scheme_name} - {'Playing' if playing else 'Paused'} {update_freq}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    update_freq = update_freq + 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    update_freq = update_freq - 2


            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)
                
                if event.key == pygame.K_t:
                    current_scheme = (current_scheme + 1) % len(COLOR_SCHEMES)


        screen.fill(COLOR_SCHEMES[current_scheme]["background"])            
        draw_grid(positions, COLOR_SCHEMES[current_scheme])
        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
                    
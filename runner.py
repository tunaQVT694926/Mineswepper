import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 10
WIDTH = 10 
MINES = 16

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Minesweeper AI")

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/bomb-at-clicked-block.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))
empty = pygame.image.load("assets/images/empty-block.png")
empty = pygame.transform.scale(empty, (cell_size, cell_size))
unclicked = pygame.image.load("assets/images/unclicked-bomb.png")
unclicked = pygame.transform.scale(unclicked, (cell_size, cell_size))
safecell = pygame.image.load("assets/images/safe.png")
safecell = pygame.transform.scale(safecell, (cell_size, cell_size))
a0 = pygame.image.load("assets/images/0.png")
a0 = pygame.transform.scale(a0, (cell_size, cell_size))
a1 = pygame.image.load("assets/images/1.png")
a1 = pygame.transform.scale(a1, (cell_size, cell_size))
a2 = pygame.image.load("assets/images/2.png")
a2 = pygame.transform.scale(a2, (cell_size, cell_size))
a3 = pygame.image.load("assets/images/3.png")
a3 = pygame.transform.scale(a3, (cell_size, cell_size))
a4 = pygame.image.load("assets/images/4.png")
a4 = pygame.transform.scale(a4, (cell_size, cell_size))
a5 = pygame.image.load("assets/images/5.png")
a5 = pygame.transform.scale(a5, (cell_size, cell_size))
a6 = pygame.image.load("assets/images/6.png")
a6 = pygame.transform.scale(a6, (cell_size, cell_size))
a7 = pygame.image.load("assets/images/7.png")
a7 = pygame.transform.scale(a7, (cell_size, cell_size))
a8 = pygame.image.load("assets/images/8.png")
a8 = pygame.transform.scale(a8, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
nearzero = set()
unclicked_bomb = set()
safe = set()
lost = False

# Show instructions initially
instructions = True            
          

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            screen.blit(empty, rect)
            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in unclicked_bomb:
                screen.blit(unclicked, rect)
            elif (i, j) in safe:
                screen.blit(safecell, rect)
            elif (i, j) in revealed:
                neighbors = game.nearby_mines((i, j))
                if neighbors == 1:
                    screen.blit(a1, rect)
                elif neighbors == 2:
                    screen.blit(a2, rect)
                elif neighbors == 3:
                    screen.blit(a3, rect)
                elif neighbors == 4:
                    screen.blit(a4, rect)
                elif neighbors == 5:
                    screen.blit(a5, rect)
                elif neighbors == 6:
                    screen.blit(a6, rect)
                elif neighbors == 7:
                    screen.blit(a7, rect)
                elif neighbors == 8:
                    screen.blit(a8, rect)
                else :
                    screen.blit(a0, rect)
                    for element in game.find_neighbor((i, j)):
                        if element not in revealed:
                            nearzero.add(element)
                    while len(nearzero) > 0:
                        first_element = nearzero.pop()
                        if first_element in safe:
                            safe.remove(first_element)
                        temp = game.nearby_mines(first_element)
                        revealed.add(first_element)
                        ai.add_knowledge(first_element, temp)
                        
                        if temp == 0:
                            for element in game.find_neighbor(first_element):
                                if element not in revealed:
                                    nearzero.add(element)
                    
            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Help Button
    helpButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 90,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Help", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = helpButton.center
    pygame.draw.rect(screen, WHITE, helpButton)
    screen.blit(buttonText, buttonRect)

    # Show Mines Button
    smButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 160,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Show Mines", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = smButton.center
    pygame.draw.rect(screen, WHITE, smButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags or len(revealed) == HEIGHT*WIDTH - MINES else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, 35)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        if resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            safe = set()
            unclicked_bomb = set()
            continue
        
        # Help: show safe moves 
        if helpButton.collidepoint(mouse):
            print("Safe moves: ", ai.safes - ai.moves_made)
            safe = ai.safes - ai.moves_made
            for element in safe:
                safe.add(element)
            time.sleep(0.2)
        
        # ShowMines Button 
        if smButton.collidepoint(mouse):
            print("Known mines: ", ai.mines)
            for element in ai.mines:
                unclicked_bomb.add(element)
            time.sleep(0.2)      
        # User-made move
        if not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
        else:
            if move in safe:
                safe.remove(move)
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
        

    pygame.display.flip()

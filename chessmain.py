# import pip
# pip.main(['install', 'pygame'])
import sys
import pygame as p
import ChessEngine, ChessBot, Menu
#Âm thanh
import pygame
import pygame.mixer
import Menu
pygame.init()
start_sound = pygame.mixer.Sound('sounds/game-start.mp3')
quit_sound = pygame.mixer.Sound(r'sounds/game-end.mp3')
move_self = pygame.mixer.Sound(r'sounds/move-self.mp3')
move_opponent = pygame.mixer.Sound(r'sounds/move-opponent.mp3')
move_check = pygame.mixer.Sound(r'sounds/move-check.mp3')
pre_move = pygame.mixer.Sound(r'sounds/premove.mp3')
tenseconds_time= pygame.mixer.Sound(r'sounds/tenseconds - time.mp3')
background_music = pygame.mixer.Sound(r'sounds/music-background.mp3')
notify = pygame.mixer.Sound(r'sounds/notify.mp3')
p.init()
font = pygame.font.Font(None, 36)
WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = HEIGHT//DIMENTION     #kích thước 1 cạnh của ô vuông nhỏ trên bàn cờ
MAX_FPS = 15
IMAGES = {}
# Hàm tải ảnh
def loadImages():
    pieces = ['bp','bR','bN','bB','bQ','bK','wp','wR','wN','wB','wQ','wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        # transform.scale nhằm làm cho hình ảnh các quân cờ phù hợp kích thước với các ô vuông trên bàn cờ
    # Có thể sử dụng hình ảnh mỗi quân cờ bằng cách IMAGES['piece']
    # VD: IMAGES['bp'] lấy hình ảnh quân tốt đen


# Hàm chính
def main(singlePlayer = False ):

    screen = p.display.set_mode((WIDTH+140,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(135, 206, 250))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False # đánh dấu khi nòa thì move nên có animate
    loadImages()
    running = True
    sqSelect = ()   # lưu dữ liệu của ô được nhấp chuột, ban đầu chưa ô nào được nhấp (row, col)
    playerClicks = []   #lưu trữ vị trí ban đầu và vị trí muốn di chuyển tới của quân cờ trên bàn cờ
    gameOver = False

    if singlePlayer:
        playerOne = True
        playerTwo = False
    else:
        playerOne = True
        playerTwo = True

    while running:

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        # tạo các nút trong trò chơi cờ vua: UNDO, RESTART, MENU
        p.draw.rect(screen, 'gray', p.Rect(520, 10, 125, 40))
        p.draw.rect(screen, 'gray', p.Rect(520, 100, 125, 40))
        p.draw.rect(screen, 'gray', p.Rect(520, 190, 125, 40))
        start_text = font.render("  UNDO", True, 'black')
        quit_text = font.render("RESTART", True, 'black')
        about_me_react = font.render("  MENU", True, 'black')
        screen.blit(start_text, (535, 15))
        screen.blit(quit_text, (528, 105))
        screen.blit(about_me_react, (530, 195))

        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
            elif i.type == p.MOUSEBUTTONDOWN:
                # tương tác với các nút bấm trong lúc chơi

                location = p.mouse.get_pos()  # lấy tọa độ x, y khi nhấn chuột
                x1 = location[0]
                y1 = location[1]

                # khi nhấn nút UNDO
                if (x1 >= 520 and x1 <= 645 and y1 >= 10 and y1 <= 50):
                    pre_move.play()
                    gs.undoMoved()
                    moveMade = True
                    animate = False

                # khi nhấn nút RESTART
                elif (x1 >= 520 and x1 <= 645 and y1 >= 100 and y1 <= 140):
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelect = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

                # khi nhấn nút MENU
                elif (x1 >= 520 and x1 <= 645 and y1 >= 190 and y1 <= 230):
                    # p.quit
                    # sys.exit()
                    Menu.menu()
                elif x1 >= 520:
                    continue
                elif not gameOver and humanTurn:
                    # location = p.mouse.get_pos()   # lấy tọa độ (x,y) trên bảng khi nhấp chuột
                    start_sound.play()
                    # lấy vị trí hàng và cột tương ứng
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelect == (row,col):    # nhấp 2 lần cùng 1 ô
                        notify.play()
                        sqSelect = ()   # Đặt lại
                        playerClicks = []
                    else:
                        sqSelect = (row,col)
                        playerClicks.append(sqSelect)   # mảng chỉ có tối đa 2 phần tử lưu giá trị ban đầu và giá trị muốn di chuyển đến
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):   # nếu nước đi là 1 nước đi hợp lệ
                            if move == validMoves[i]:
                                gs.makeMoved(validMoves[i])
                                move_self.play()
                                animate = True
                                moveMade = True      # thể hiện nước đi đã thực hiện
                                sqSelect = ()
                                playerClicks = []
                        if not moveMade:

                            playerClicks = [sqSelect]
            # Quay lại nước đi trước khi nhấn 1 phím
            elif i.type == p.KEYDOWN:
                if i.key == p.K_z:   # quay lại nước đi trước khi nhấn phím 'z'
                    pre_move.play()
                    gs.undoMoved()
                    moveMade = True
                    animate = False
                if i.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelect = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                if i.key == p.K_m:
                    Menu.menu()

        #AI
        if not gameOver and not humanTurn:
            AIMove = ChessBot.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessBot.randomMove(validMoves)
            gs.makeMoved(AIMove)
            moveMade = True
            animate = True

        # Nếu nước đi thỏa mãn được điều kiện thì sẽ thực hiện các nước đi hợp lệ tiếp theo
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, sqSelect)
        
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()
    sys.exit()

#Hiển thị các nước có thể di chuyển được của một quân khi được chọn
def highlighSquares(screen, gs, validMoves, sqSelect):
     if sqSelect != ():
            r, c = sqSelect
            if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # khi đến lượt nào chỉ quân màu đó được highlight
                # highlight ô được chọn
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # Làm mờ màu đi từ 0 -> 255
                s.fill(p.Color('blue'))
                screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
                # highlight ô gợi ý
                s.fill(p.Color('green'))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
     #Highlight vua nếu bị chiếu
     if gs.inCheck():
        r, c = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # Làm mờ màu đi từ 0 -> 255
        s.fill(p.Color('red'))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelect):   # hiển thị bàn cờ và quân cờ
    drawBoard(screen) #vẽ các ô trên bàn cờ
    highlighSquares(screen, gs, validMoves, sqSelect)
    drawPieces(screen, gs.board) 

def drawBoard(screen):
    #vẽ bàn cờ vua có ô trắng và xám
    global colors
    colors = [p.Color('#789658'), p.Color('#eaedd0')]
    #duyệt các ô trên bàn cờ
    for i in range(DIMENTION):
        for j in range(DIMENTION):
            # cách xác định các ô trắng và xám trên bàn cờ
            color = colors[(i+j)%2]
            p.draw.rect(screen,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    # in các quân cờ lên bàn cờ
    for row in range(DIMENTION):
        for column in range(DIMENTION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # Khung hình để di chuyển trong 1 ô
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Xóa quân ở ô đang đi đến
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Vẽ quân bị bắt ở ô cuối
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Vẽ quân đang di chuyển
        # if move.pieceMoved != '--':
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
    # screen.blit(screen, (75, 100))





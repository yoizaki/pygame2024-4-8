import pygame
import sys
import variable
import Class
import os


# 尋找路徑
def get_project_root():
    """Return the root directory of the project."""
    if getattr(sys, 'frozen', False):  # 判斷是否打包成exe
        return os.path.dirname(sys.executable)  # 如果是打包成exe，回傳執行檔的目錄
    elif __file__:
        return os.path.dirname(os.path.abspath(__file__))  # 如果是直接運行 Python 程式，回傳程式所在目錄


# 設定相對路徑
root = get_project_root()
os.chdir(root)

# 初始化遊戲
pygame.init()

V = variable  # 偷懶用簡寫
# 設定好視窗
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("詐一個大的")
icon = pygame.image.load("images/icon/icon_v3.64.png")
pygame.display.set_icon(icon)

room_path = 'images/room/room_lv0.png'  # 房間全圖路徑

# 撥放bgm
pygame.mixer.music.load('music/bgm2.mp3')
pygame.mixer.music.set_volume(70)
pygame.mixer.music.play(loops=-1)


# 遊戲主迴圈
while True:
    # 確認各項事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if V.state == 'start':
            # 點擊右鍵後轉場並撥放開頭動畫
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                V.state = 'anime'

                image = pygame.image.load('images/anime/opening/01.jpg').convert_alpha()
                image = pygame.transform.scale(image, (800, 600))
                Class.transition.ready(image)
                Class.transition.hacker()

                Class.anime.image = image
                Class.animeText.x_y = (400, 500)
                Class.animeText.text_alpha = 255
                Class.anime.opening()

                image = pygame.image.load(room_path).convert_alpha()
                Class.transition.ready(image)
                Class.transition.hacker()

                V.state = 'room'
                Class.room.back()

        if V.state == 'room':
            if not V.room_flag:
                Class.room.check(event)

        if V.state == 'blackjack':
            Class.blackjack.running(event)

        if V.state == 'work':
            Class.work.check(event)

    if V.state == 'start':
        Class.anime.start_screen()

    if V.state == 'room':
        if V.room_flag:
            Class.room.back()
            V.room_flag = False

    if V.state == 'train':
        Class.train.running()
        Class.train.check()

    if V.state == 'blackjack':
        if Class.blackjack.stand:
            Class.blackjack.show_cards()
            Class.blackjack.check()
            if Class.blackjack.stand:
                Class.blackjack.computer_hit()
                Class.FUNCS.delay(10)

    if V.state == 'work' and Class.work.game_flag:
        Class.work.game_running()
    Class.FUNCS.update()

import pygame
import random
import sys
import variable

FPS = 60  # 設定每秒幾幀
fpsClock = pygame.time.Clock()  # Clock縮寫
FULLSCREEN = (800, 600)  # 視窗大小tuple
SCREEN_CENTER = (400, 300)  # 視窗中心tuple
SCREEN = pygame.display.set_mode(FULLSCREEN)  # 偷懶用簡寫
BLACK = (0, 0, 0)  # 黑色RGB
WHITE = (255, 255, 255)  # 白色RGB
room_path = 'images/room/room_lv0.png'  # 房間全圖路徑
pygame.init()  # 初始化pygame


class FUNCS:  # 使用class與function把各種因為很懶所以不想重寫的程式包起來

    @staticmethod
    def update():
        pygame.display.update()  # pygame裡的更新顯示
        fpsClock.tick(FPS)  # 設定螢幕更新率為60幀

    @staticmethod
    def delay(x):
        pygame.time.delay(x)  # 等待

    @staticmethod
    def quit_game():  # 這一整串就是讓視窗上右上角的叉叉可以作用
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class TRANSITION:  # 轉場動畫的class
    def __init__(self, screen, end_picture):  # 第一次呼叫此class時會做的動作
        self.screen = screen  # 將外面的變數改成self的變數，這樣包在這個class裡的function都可以共用

        self.end_picture = end_picture
        self.end_picture_rect = SCREEN_CENTER

        self.hacker0 = pygame.image.load("images/loading/hacker0.png").convert_alpha()  # 載入圖片並轉換成比較好用的形式
        self.hacker1 = pygame.image.load("images/loading/hacker1.png").convert_alpha()
        self.hacker0 = pygame.transform.scale(self.hacker0, (200, 200))  # 改變圖片的大小
        self.hacker1 = pygame.transform.scale(self.hacker1, (200, 200))

        self.hacker0_rect = self.hacker0.get_rect(center=SCREEN_CENTER)  # 設定圖片的位置為螢幕正中央
        self.hacker1_rect = self.hacker1.get_rect(center=SCREEN_CENTER)

        self.alpha = 0  # 設定初始不透明度
        self.alpha_speed = 5  # 設定不透明度改變速度

        self.black_surface = pygame.Surface(FULLSCREEN)  # 用pygame做一個大小跟螢幕一樣大的面
        self.black_surface.fill(BLACK)  # 把他塗黑
        self.black_surface.set_alpha(self.alpha)  # 設定他的初始透明度

    def ready(self, end_picture):
        self.end_picture = pygame.transform.scale(end_picture, FULLSCREEN)
        self.end_picture_rect = self.end_picture.get_rect(center=SCREEN_CENTER)

    def hacker(self):
        while self.alpha < 255:  # 漸黑
            self.alpha += self.alpha_speed  # 每跑一次就改變一點點透明度
            self.screen.blit(self.black_surface, (0, 0))  # 把之前做的面貼到screen上
            self.black_surface.set_alpha(self.alpha)  # 把透明度設置為改過的透明度
            FUNCS.update()
            FUNCS.delay(10)
        for _ in range(3):  # 閃爍圖片
            self.screen.blit(self.hacker0, self.hacker0_rect)
            FUNCS.update()
            FUNCS.delay(300)
            self.screen.blit(self.hacker1, self.hacker1_rect)
            FUNCS.update()
            FUNCS.delay(300)
        self.alpha = 255
        while self.alpha > 0:  # 漸亮
            self.alpha -= self.alpha_speed
            self.screen.blit(self.end_picture, self.end_picture_rect)  # 將原本螢幕顯示的圖片再貼回去螢幕上
            self.screen.blit(self.black_surface, (0, 0))
            self.black_surface.set_alpha(self.alpha)  # 把透明度設置為改過的透明度
            FUNCS.update()
            FUNCS.delay(10)


transition = TRANSITION(SCREEN, None)  # 把transition宣告為這個class


class CreateText:
    def __init__(self, screen, text, fontcolor, backcolor, text_pos, size, n):  # n為一行的字數
        self.screen = screen
        self.size = size
        self.font = pygame.font.Font("fonts/NaikaiFont-Light.ttf", self.size)  # 設定字體和大小
        self.text = text
        self.text_alpha = 255
        self.fontCOLOR = fontcolor
        self.backCOLOR = backcolor
        self.x_y = text_pos
        self.n = n
        self.sentence = None  # 反正就先宣告出來，之後會用到
        self.rect = None
        self.sentences = []
        self.rects = []

    def draw(self):
        if len(self.text) > self.n:  # 如果文字的長度大於一行的字數的話
            x = len(self.text) // self.n + 1  # 看文字是幾行，取整數
            for i in range(x):
                self.sentences[i].set_alpha(self.text_alpha)
                self.screen.blit(self.sentences[i], self.rects[i])  # 一行一行重複貼到螢幕上
        else:
            self.sentence.set_alpha(self.text_alpha)
            self.screen.blit(self.sentence, self.rect)

    def new_sentence(self):
        self.font = pygame.font.Font("fonts/NaikaiFont-Light.ttf", self.size)
        if len(self.text) > self.n:
            x = len(self.text) // self.n

            # 前面的\是讓程式可以讀到下面一行讓程式不要那麼長，用sentences把文字存起來然後留五個保險給他
            self.sentences = \
                [self.font.render(self.text[i:self.n + i], True, self.fontCOLOR, self.backCOLOR) for i in range(x + 5)]
            self.rects = [self.x_y for _ in range(x + 5)]  # 把位置也用rects都存起來
            t = 0

            for i in range(0, len(self.text), self.n):
                # 把文字和位置一行一行塞進去，但最後一行不行塞，因為最後一行不足n個字，如果讀進來會爆掉
                self.sentences[t] = self.font.render(self.text[i:self.n + i], True, self.fontCOLOR, self.backCOLOR)
                self.rects[t] = self.sentences[t].get_rect()
                self.rects[t].center = (self.x_y[0], self.x_y[1] + self.size * t)  # 調整因為換行而重疊的文字的位置
                t += 1
            x *= self.n  # 下面是最後一行字的特判，x是已經讀的字
            self.sentences[t] = self.text[x:]  # 把x後面的字都放進去sentences
        else:
            # 上面的單行的版本
            self.sentence = self.font.render(self.text, True, self.fontCOLOR, self.backCOLOR)
            self.sentence.set_alpha(self.text_alpha)
            self.rect = self.sentence.get_rect()
            self.rect.center = self.x_y

    # 更新各項數值並利用剛剛寫的東西把他放到螢幕上
    def update_val(self):
        self.x_y = (130, 75)
        self.text = '體力 : ' + str(variable.energy) + ' / ' + str(variable.ME)
        self.new_sentence()
        self.draw()
        self.text = '存款 : ' + str(variable.money) + '元 '
        self.x_y = (self.x_y[0], self.x_y[1] + self.size)  # 配合字體大小改變y位置
        self.new_sentence()
        self.draw()
        if variable.CP >= 7:  # 根據數值改變呈現的文字
            self.text = '創造力 : 豐富'
        elif variable.CP >= 4:
            self.text = '創造力 : 一般'
        else:
            self.text = '創造力 : 貧乏'
        self.x_y = (self.x_y[0], self.x_y[1] + self.size)
        self.new_sentence()
        self.draw()
        if variable.SA >= 7:
            self.text = '話術 : 熟練'
        elif variable.SA >= 4:
            self.text = '話術 : 一般'
        else:
            self.text = '話術 : 生疏'
        self.x_y = (self.x_y[0], self.x_y[1] + self.size)
        self.new_sentence()
        self.draw()
        # 設定經歷天數與周幾
        self.text = ('Week : ' + variable.week[variable.today] +
                     '  經歷天數 : ' + str(variable.days))
        self.x_y = (400, 10)
        self.new_sentence()
        self.draw()


# 把各種需要的文字宣告為這個class
animeText = CreateText(SCREEN, '', BLACK, None, (300, 400), 26, 28)
val = CreateText(SCREEN, '', BLACK, None, (400, 10), 22, 90)
roomText = CreateText(SCREEN, '', BLACK, None, (300, 500), 28, 32)
blackjack_text = CreateText(SCREEN, '', BLACK, None, (300, 400), 22, 30)
workText = CreateText(SCREEN, '', BLACK, None, (300, 500), 30, 24)
gameText = CreateText(SCREEN, '', BLACK, None, (300, 400), 20, 10)


class ANIME:
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load('images/start/start_2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, FULLSCREEN)
        self.rect = self.image.get_rect()

        # 各結局劇本
        self.opening_text = (
            '剛考完學測的你，義氣風發的走出考場，對你光明的未來感到十分驕傲。',
            '然而，你考的跟屎一樣，真的就是屎本身。',
            '你不理解你怎麼可能考的這麼爛，你還想到未來的人生都要跟狗一樣活著 阿阿阿阿阿阿阿阿阿阿阿！',
            '突然！你想到了！只要你現在去找一個工作賺錢，別人還在讀大學，你就有一堆錢可以去投資然後財富自由了。',
            '於是你開始查找各種相關資料，對，相關資料。',
            '一則簡訊跳了出來，有間公司對你伸出了橄欖枝。',
            '完全沒想到事情過的那麼順利，不過好耶。',
            '+1',
            'b',
            '公司同意了你的加入，你開始對光明的未來感到驕傲',
            '但是公司說他們每個禮拜都會抽成，而且還抽不少。',
            '不過沒差啦！可以賺錢就好，加入！',
            '於是你跑到南投租了一間小房間當作你新生活開端。',
            '你透過不斷的訓練增加自己的能力。',
            '訓練',
            '從此，你勵志要不斷的鍛鍊提升自己的能力，並同時靠詐騙發大財，靠著詐騙成為台灣首富，再一舉買下公司成為台灣詐騙天王！'
        )

        self.ending_boss_text = (
            '「你真的是沒救的廢物！」',
            '老闆看到你賺的錢後覺得你就是個廢物，還害他提高被抓的可能性',
            '於是他把你拖去不知道是在哪裡的醫院。',
            '還把你綁到手術台上。',
            '你在被注射麻醉藥後就睡過去了。',
            '在你昏睡時，醫生不知道對你的身體做了甚麼。',
            '你醒來時感覺身體少了什麼，醫生跟你說，你的腎、膽、胃、骨髓全部都被拿去賣掉了，大概只能再活一天。',
            '你對你的人生完全沒有希望了，你後悔當初為什麼不好好讀書，要跑來詐騙。',
            '你死了。',
            '過了一個月後，沒有人記得這件事，你就是個廢物。'
        )

        self.ending_good_end_text = (
            '經過了這段時間的奮鬥，你終於賺到一大堆錢並變成成功人士。',
            '你買下了原本招聘你的公司，並繼續招募學測考不好的高中生成為詐騙的一分子。',
            '你的名號廣布，但你利用錢和關係所以不管你去哪，做了什麼都不會被補。',
            '你的人生到了巔峰，別人還在讀大學，你已經成為了台灣前幾有錢的人，成為台灣詐騙天王了！'
        )

        self.ending_jail_text = (
            '你被關進監獄了。',
            '法官判你3年有期徒刑，因為台灣的法律說詐騙只能判五年以下。',
            '你上了新聞，新聞說你是社會敗類，民眾開始熱烈的討論詐騙的罪應該要加重，不要讓這種垃圾再出來禍害人間。',
            '你在監獄裡，日子過得不太好受，但你心中還是有希望，畢竟三年而已。',
            '三年過去，你從監獄出來了。',
            '當初說要改法律也都被忘記了，根本沒有人管也根本沒有人記得，於是你開始了全新的人生。'
        )

        self.ending_tired_text = (
            '很遺憾，你過勞死了，你的身體負荷不住你沒人性的壓榨。',
            '在你死後三十天才有人發現你的屍體，你的屍體長灰，房間裏都是腐爛的味道。',
            '法醫來驗屍後還發現你的肝跟煤炭一樣黑。',
            '老闆非常生氣，為什麼這個廢物沒有賺錢還害他提高被補的風險。',
            '過了一個月後，沒有任何人記得這件事，你這個廢物。'
        )

        animeText.text = '~~~點擊左鍵開始遊戲~~~'
        animeText.x_y = (400, 450)
        animeText.new_sentence()  # 呼叫上面寫過的函式
        self.text_alpha = 255
        self.alpha_flag = True   # 透明度旗標 決定透明度增加或減少
        animeText.text_alpha = self.text_alpha

        # 設定對話框圖像
        self.text_box = pygame.image.load("images/game/square.png").convert_alpha()
        self.text_box = pygame.transform.scale(self.text_box, (800, 180))
        self.text_box.set_alpha(200)
        self.text_box_rect = self.text_box.get_rect(center=(400, 520))

        self.click_flag = False
        self.skip_flag = False

    # 做一個把圖片和字貼到螢幕上的function
    def show(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_box, self.text_box_rect)
        animeText.draw()
        FUNCS.update()

    # 開頭動畫
    def opening(self):
        animeText.text = self.opening_text[0]
        animeText.new_sentence()
        for i in range(2, 15):
            j = i - 1
            FUNCS.quit_game()
            # 利用迴圈將每個圖片依序貼到螢幕上
            if i < 10:
                image = 'images/anime/opening/0' + str(i) + '.jpg'  # 利用字串相加讓迴圈改變載入甚麼圖片
            else:
                image = 'images/anime/opening/' + str(i) + '.jpg'
            self.show()
            animeText.text = self.opening_text[j]
            animeText.new_sentence()
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, FULLSCREEN)
            self.click_flag = False
            self.check()
        self.image = pygame.image.load('images/anime/train1_1.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, FULLSCREEN)
        self.show()
        animeText.text = self.opening_text[14]
        animeText.new_sentence()
        self.click_flag = False
        self.check()
        # 下面這段是循環播放訓練
        for i in range(2):
            FUNCS.quit_game()
            image = ('images/anime/train1_1.jpg',
                     'images/anime/train1_2.jpg',
                     'images/anime/train2_1.jpg',
                     'images/anime/train2_2.jpg')
            for j in range(4):
                self.image = pygame.image.load(image[j]).convert_alpha()
                self.image = pygame.transform.scale(self.image, FULLSCREEN)
                self.show()
                self.click_flag = False
                self.check()
        # 下面這段是把最後一張圖片和字放上去
        self.image = pygame.image.load('images/anime/opening/14.jpg')
        self.image = pygame.transform.scale(self.image, FULLSCREEN)
        animeText.text = self.opening_text[15]
        animeText.new_sentence()
        self.show()
        self.click_flag = False
        self.check()
        self.skip_flag = False
        self.click_flag = False

    # 點擊時切換到下一張
    def check(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click_flag = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.skip_flag = True

            if self.click_flag or self.skip_flag:
                break
    # 開始畫面
    def start_screen(self):
        self.screen.blit(self.image, self.rect)
        # 讓~~~點擊左鍵開始遊戲~~~變透明，但不要完全透明
        if self.alpha_flag:
            self.text_alpha -= 10
            if self.text_alpha < 100:
                self.text_alpha = 100
                self.alpha_flag = False
        # 讓~~~點擊左鍵開始遊戲~~~變不透明
        else:
            self.text_alpha += 10
            if self.text_alpha > 255:
                self.text_alpha = 255
                self.alpha_flag = True
        # 把它貼到螢幕上然後更新螢幕
        animeText.text_alpha = self.text_alpha
        self.screen.blit(self.image, self.rect)
        animeText.draw()
        FUNCS.update()

    # 未達目標BAD END
    def ending_boss(self):
        # 利用迴圈將每個圖片依序貼到螢幕上
        for i in range(10):
            j = i + 1
            FUNCS.quit_game()
            path = 'images/anime/ending/boss/boss_' + str(j) + '.jpg'  # 利用字串相加讓迴圈改變載入甚麼圖片
            background = pygame.image.load(path)
            self.image = pygame.transform.scale(background, FULLSCREEN)
            animeText.text = self.ending_boss_text[i]
            animeText.x_y = (400, 500)
            animeText.new_sentence()
            self.show()
            FUNCS.delay(3000)
        # 讓BAD END利用迴圈在黑背景中慢慢變得不透明
        animeText.text = 'BAD　END'
        animeText.x_y = SCREEN_CENTER
        animeText.fontCOLOR = (255, 0, 0)
        animeText.size = 100
        for alpha in range(1, 256):
            FUNCS.quit_game()
            self.screen.fill(BLACK)
            animeText.text_alpha = alpha
            animeText.new_sentence()
            animeText.draw()
            FUNCS.update()
            FUNCS.delay(10)
        while True:
            FUNCS.quit_game()

    # 達成目標的GOOD END
    def ending_good_end(self):
        # 利用迴圈將每個圖片依序貼到螢幕上
        for i in range(4):
            j = i + 1
            FUNCS.quit_game()
            path = 'images/anime/ending/good_end/happy_' + str(j) + '.jpg'
            background = pygame.image.load(path)
            self.image = pygame.transform.scale(background, FULLSCREEN)
            animeText.text = self.ending_good_end_text[i]
            animeText.x_y = (400, 500)
            animeText.new_sentence()
            self.show()
            FUNCS.delay(3000)
        # 讓GOOD END利用迴圈在白背景中慢慢變得不透明
        self.screen.fill(WHITE)
        animeText.text = 'GOOD　END'
        animeText.x_y = SCREEN_CENTER
        animeText.fontCOLOR = BLACK
        animeText.size = 100
        for alpha in range(1, 256):
            FUNCS.quit_game()
            self.screen.fill(WHITE)
            animeText.text_alpha = alpha
            animeText.new_sentence()
            animeText.draw()
            FUNCS.update()
            FUNCS.delay(10)
        while True:
            FUNCS.quit_game()

    # 被捕結局
    def ending_jail(self):
        # 利用迴圈將每個圖片依序貼到螢幕上
        for i in range(6):
            j = i + 1
            FUNCS.quit_game()
            path = 'images/anime/ending/jail/jail_' + str(j) + '.jpg'
            background = pygame.image.load(path)
            self.image = pygame.transform.scale(background, FULLSCREEN)
            animeText.text = self.ending_jail_text[i]
            animeText.x_y = (400, 500)
            animeText.new_sentence()
            self.show()
            FUNCS.delay(3000)
        # 讓END利用迴圈在白背景中慢慢變得不透明
        self.screen.fill(WHITE)
        animeText.text = 'END'
        animeText.x_y = SCREEN_CENTER
        animeText.fontCOLOR = BLACK
        animeText.size = 100
        for alpha in range(1, 256):
            FUNCS.quit_game()
            self.screen.fill(WHITE)
            animeText.text_alpha = alpha
            animeText.new_sentence()
            animeText.draw()
            FUNCS.update()
            FUNCS.delay(10)
        while True:
            FUNCS.quit_game()

    # 過勞死結局
    def ending_tired(self):
        # 利用迴圈將每個圖片依序貼到螢幕上
        for i in range(5):
            j = i + 1
            FUNCS.quit_game()
            path = 'images/anime/ending/tired/tired_' + str(j) + '.jpg'
            background = pygame.image.load(path)
            self.image = pygame.transform.scale(background, FULLSCREEN)
            animeText.text = self.ending_tired_text[i]
            animeText.x_y = (400, 500)
            animeText.new_sentence()
            self.show()
            FUNCS.delay(3000)
        # 讓BAD END利用迴圈在黑背景中慢慢變得不透明
        animeText.text = 'BAD　END'
        animeText.x_y = SCREEN_CENTER
        animeText.fontCOLOR = (255, 0, 0)
        animeText.size = 100
        for alpha in range(1, 256):
            FUNCS.quit_game()
            self.screen.fill(BLACK)
            animeText.text_alpha = alpha
            animeText.new_sentence()
            animeText.draw()
            FUNCS.update()
            FUNCS.delay(10)
        while True:
            FUNCS.quit_game()


anime = ANIME(SCREEN)


class Vocabulary:
    def __init__(self):
        self.verb = (
            "幫過", "操作", "繳交", "扣除", "複查", "結清", "追究", "承擔", "規定", "調查", "盜取", "69",
            "幹", "研究", "理解", "指導", "刪掉", "拿過來", "咀嚼", "關閉", "收集", "放置", "鼓勵", "抓住",
            "攪拌", "搖動", "揮舞", "清理", "傳教士", "做愛心便當", "吃屌", "引誘", "尋找", "破壞", "喚醒",
            "覺醒", "卍解", "變身", "燒掉", "親親", "打手槍"
        )
        self.noun = (
            "影片", "滿分", "台南二中", "信用", "欠款", "費用", "成績", "廁所", "公司", "銀行", "大尾鱸鰻", "額外收入",
            "時間", "努力", "收穫", "股票", "資金", "gogoro", "請假單", "數學考卷", "浴室", "速度與激情", "香蕉船",
            "臭豆腐", "咖啡因", "熱狗", "消防栓", "衛生紙", "電腦", "窗簾", "紅毛丹", "蓮霧", "基督教", "愛情", "夢想",
            "自由", "跳蛋", "記過單", "畢業紀念冊", "豆漿", "橘子", "精液", "警局", "妓院", "雪屋", "我家", "尖嘴鉗"
        )
        self.people = (
            "老師", "賴清德", "試務人員", "競選團隊", "專業人員", "國文老師", "詐騙集團", "專業黑客", "黃氏兄弟",
            "海龍王", "三角形", "馬鈴薯", "竹聯幫", "草帽海賊團", "忍刀七人眾", "老蟹", "鳥哥", "復興國小3年8班",
            "護庭十三番", "調查兵團", "火箭隊", "基紐特種部隊", "復仇者聯盟", "微笑棺木", "媽祖", "幻影旅團", "黑人",
            "原住民", "勞贖"
        )

    def get_noun(self):  # 隨機取出9個不一樣的名詞放進noun_list裡
        noun_list = []
        while len(noun_list) < 9:
            noun = random.choice(self.noun)
            if noun not in noun_list:
                noun_list.append(noun)
        return noun_list  # 把list回傳回去用

    def get_verb(self):  # 隨機取出9個不一樣的動詞放進verb_list裡
        verb_list = []
        while len(verb_list) < 9:
            verb = random.choice(self.verb)
            if verb not in verb_list:
                verb_list.append(verb)
        return verb_list  # 把list回傳回去用

    def get_people(self):  # 隨機取出9個不一樣的人詞放進people_list裡
        people_list = []
        while len(people_list) < 9:
            people = random.choice(self.people)
            if people not in people_list:
                people_list.append(people)
        return people_list  # 把list回傳回去用


vocabulary = Vocabulary()  # 把vocabulary宣告為這個class


class QTE:  # 健身小遊戲
    def __init__(self, screen):  # 把該load的圖都整理好
        self.screen = screen

        self.text_box = pygame.image.load("images/game/square.png").convert_alpha()
        self.text_box = pygame.transform.scale(self.text_box, (800, 180))
        self.text_box.set_alpha(200)
        self.text_box_rect = self.text_box.get_rect(center=(400, 520))

        self.buttonA = pygame.image.load("images/QTE/buttonA.png").convert()
        self.buttonA.set_colorkey(BLACK)
        self.buttonA = pygame.transform.scale(self.buttonA, (200, 200))
        self.buttonD = pygame.image.load("images/QTE/buttonD.png").convert()
        self.buttonD.set_colorkey(BLACK)
        self.buttonD = pygame.transform.scale(self.buttonD, (200, 200))
        self.buttonW = pygame.image.load("images/QTE/buttonW.png").convert()
        self.buttonW.set_colorkey(BLACK)
        self.buttonW = pygame.transform.scale(self.buttonW, (200, 200))
        self.buttonS = pygame.image.load("images/QTE/buttonS.png").convert()
        self.buttonS.set_colorkey(BLACK)
        self.buttonS = pygame.transform.scale(self.buttonS, (200, 200))

        self.button = self.buttonA

        self.background1 = pygame.image.load("images/anime/train1_1.jpg").convert_alpha()
        self.background1 = pygame.transform.scale(self.background1, FULLSCREEN)
        self.background1_rect = self.background1.get_rect()
        self.background1_rect.center = SCREEN_CENTER

        self.background2 = pygame.image.load("images/anime/train1_2.jpg").convert_alpha()
        self.background2 = pygame.transform.scale(self.background2, FULLSCREEN)
        self.background2_rect = self.background2.get_rect()
        self.background2_rect.center = SCREEN_CENTER

        self.background3 = pygame.image.load("images/anime/train2_1.jpg").convert_alpha()
        self.background3 = pygame.transform.scale(self.background3, FULLSCREEN)
        self.background3_rect = self.background3.get_rect()
        self.background3_rect.center = SCREEN_CENTER

        self.background4 = pygame.image.load("images/anime/train2_2.jpg").convert_alpha()
        self.background4 = pygame.transform.scale(self.background4, FULLSCREEN)
        self.background4_rect = self.background4.get_rect()
        self.background4_rect.center = SCREEN_CENTER

        # 隨機設定圈圈的位置
        self.circle_centerX = random.randrange(200, 600)
        self.circle_centerY = random.randrange(200, 400)

        self.button_rect = self.button.get_rect()
        self.button_rect.center = (self.circle_centerX, self.circle_centerY)

        self.R = 200
        self.score = 0
        self.background_flag = 0
        self.speed = 1

        # 隨機取WASD其中一個跳出來當要按的按鍵
        self.keys = ('W', 'A', 'S', 'D')
        self.now_key = random.choice(self.keys)

        # 設定音效檔案路徑
        sound_paths = {
            "sound1": "music/train_1.mp3",
            "sound2": "music/train_2.mp3",
            "sound3": "music/train_3.mp3",
            "sound4": "music/train_4.mp3"
        }

        # 讀入音效
        self.Sound_effects = {}
        for key, path in sound_paths.items():
            self.Sound_effects[key] = pygame.mixer.Sound(path)

    def start_game(self):  # 把該準備的都準備好
        self.circle_centerX = random.randrange(200, 600)
        self.circle_centerY = random.randrange(200, 400)
        self.button_rect = self.button.get_rect()
        self.button_rect.center = (self.circle_centerX, self.circle_centerY)
        self.R = 200
        self.score = 0
        self.background_flag = 0
        self.speed = 1.5
        # 隨機取鍵後，把self.button設為分別的鍵
        self.now_key = random.choice(self.keys)
        if self.now_key == 'W':
            self.button = self.buttonW
        elif self.now_key == 'A':
            self.button = self.buttonA
        elif self.now_key == 'S':
            self.button = self.buttonS
        elif self.now_key == 'D':
            self.button = self.buttonD
        pygame.mixer.music.stop()

    def change_position(self):  # 位置與按鍵都在隨機一次然後加速
        self.now_key = random.choice(self.keys)
        if self.now_key == 'W':
            self.button = self.buttonW
        elif self.now_key == 'A':
            self.button = self.buttonA
        elif self.now_key == 'S':
            self.button = self.buttonS
        elif self.now_key == 'D':
            self.button = self.buttonD
        self.circle_centerX = random.randrange(200, 600)
        self.circle_centerY = random.randrange(200, 400)
        self.button_rect.center = (self.circle_centerX, self.circle_centerY)
        self.speed += 0.08
        FUNCS.delay(50)

    def change_background(self):  # 判定然後改flag，讓他循環
        if self.background_flag < 3:
            self.background_flag += 1
        else:
            self.background_flag = 0

    def check(self):  # 判定有沒有按到
        # 如果圓圈縮到最小然後還沒有按到的話就game_over
        if self.R <= 73:
            self.end_game()
        # 判定有沒有在圓圈夠小的時候按正確的鍵
        elif self.R <= 88:
            key = pygame.key.get_pressed()  # pygame偵測有沒有按按鍵的函式

            # 如果現在該按W而且按到W了，就變換位置變換背景然後加一分
            if key[pygame.K_w]:
                if self.now_key == 'W':
                    FUNCS.delay(80)
                    self.R = 200
                    self.change_position()
                    self.score += 1
                    self.change_background()
                # 按錯了就game_over
                else:
                    self.end_game()

            # 如果現在該按S而且按到S了，就變換位置變換背景然後加一分
            elif key[pygame.K_s]:
                if self.now_key == 'S':
                    FUNCS.delay(80)
                    self.R = 200
                    self.change_position()
                    self.score += 1
                    self.change_background()
                # 按錯了就game_over
                else:
                    self.end_game()
            # 如果現在該按A而且按到A了，就變換位置變換背景然後加一分
            elif key[pygame.K_a]:
                if self.now_key == 'A':
                    FUNCS.delay(80)
                    self.R = 200
                    self.change_position()
                    self.score += 1
                    self.change_background()
                # 按錯了game_over
                else:
                    self.end_game()
            # 如果現在該按D而且按到D了，就變換位置變換背景然後加一分
            elif key[pygame.K_d]:
                if self.now_key == 'D':
                    FUNCS.delay(80)
                    self.R = 200
                    self.change_position()
                    self.score += 1
                    self.change_background()
                # 按錯了game_over
                else:
                    self.end_game()

        # 太早按也game_over
        elif 88 < self.R <= 180:
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.end_game()
            elif key[pygame.K_s]:
                self.end_game()
            elif key[pygame.K_a]:
                self.end_game()
            elif key[pygame.K_d]:
                self.end_game()

        if 195 <= self.R <= 200:
            self.Sound_effects['sound1'].play()
        elif 160 <= self.R <= 165:
            self.Sound_effects['sound2'].play()
        elif 123 <= self.R <= 128:
            self.Sound_effects['sound3'].play()
        elif 85 <= self.R <= 90:
            self.Sound_effects['sound4'].play()

    def running(self):
        self.R -= self.speed  # 讓圓的半徑依照速度變小
        # 依照flag改變背景
        if self.background_flag == 0:
            self.screen.blit(self.background1, self.background1_rect)
        elif self.background_flag == 1:
            self.screen.blit(self.background2, self.background2_rect)
        elif self.background_flag == 2:
            self.screen.blit(self.background3, self.background3_rect)
        elif self.background_flag == 3:
            self.screen.blit(self.background4, self.background4_rect)
        # 把中間的圖案和圈圈都放到螢幕上
        self.screen.blit(self.button, self.button_rect)
        pygame.draw.circle(self.screen, WHITE, (self.circle_centerX, self.circle_centerY), self.R, 10)

    def end_game(self):
        for sound in self.Sound_effects.values():
            sound.stop()
        pygame.mixer.music.play(loops=-1)
        variable.ME += self.score // 2  # 根據分數增加體力上限
        # 根據分數在全黑的螢幕上寫不同的字
        self.screen.fill(BLACK)
        self.screen.blit(self.text_box, self.text_box_rect)
        if self.score // 2 >= 10:
            animeText.text = '你感覺現在自己甚至能舉起重機，體力上限提升了: ' + str(self.score // 2)
        elif self.score // 2 >= 5:
            animeText.text = '健身頗有成效，體力上限提升了: ' + str(self.score // 2)
        elif self.score // 2 > 0:
            animeText.text = '健身沒甚麼效果，體力上限提升了: ' + str(self.score // 2)
        else:
            animeText.text = '你花了大把的精力做白工，體力上限沒有提升'
        animeText.new_sentence()
        animeText.draw()
        FUNCS.update()
        FUNCS.delay(3000)
        image = pygame.image.load(room_path)
        transition.ready(image)
        transition.hacker()
        room.back()


train = QTE(SCREEN)  # 把train宣告為這個class


class BlackJack:  # 賭博的21點小遊戲
    def __init__(self, screen):
        self.screen = screen

        self.bet = 0  # 初始化押注金額

        # 將self.dealer、self.computer、self.player分別宣告成之後下面出現的class
        self.dealer = BlackJack.Dealer()
        self.computer = BlackJack.Role()
        self.player = BlackJack.Role()

        # 載入圖片
        self.table = pygame.image.load('images/21/table.png')
        self.deal_Btn = pygame.image.load('images/21/dealBtn.png')
        self.hit_Btn = pygame.image.load('images/21/hitBtn.png')
        self.stand_Btn = pygame.image.load('images/21/standBtn.png')
        self.exit_Btn = pygame.image.load('images/21/exitBtn.png')
        self.bet_background = pygame.image.load('images/21/bet_background.png')
        self.minus_Btn = pygame.image.load('images/21/minusBtn.png')
        self.plus_Btn = pygame.image.load('images/21/plusBtn.png')

        # 改圖片大小
        self.table = pygame.transform.scale(self.table, FULLSCREEN)
        self.deal_Btn = pygame.transform.scale(self.deal_Btn, (135, 55))
        self.hit_Btn = pygame.transform.scale(self.hit_Btn, (135, 55))
        self.stand_Btn = pygame.transform.scale(self.stand_Btn, (135, 55))
        self.exit_Btn = pygame.transform.scale(self.exit_Btn, (135, 55))
        self.bet_background = pygame.transform.scale(self.bet_background, (135, 55))
        self.minus_Btn = pygame.transform.scale(self.minus_Btn, (70, 55))
        self.plus_Btn = pygame.transform.scale(self.plus_Btn, (70, 55))

        # 改圖片位置
        self.table_rect = self.table.get_rect(center=SCREEN_CENTER)
        self.deal_Btn_rect = self.deal_Btn.get_rect(center=(720, 150))
        self.hit_Btn_rect = self.hit_Btn.get_rect(center=(720, 250))
        self.stand_Btn_rect = self.stand_Btn.get_rect(center=(720, 350))
        self.exit_Btn_rect = self.exit_Btn.get_rect(center=(720, 450))
        self.display_money_rect = self.bet_background.get_rect(center=(400, 40))
        self.minus_Btn_rect = self.minus_Btn.get_rect(center=(260, 40))
        self.plus_Btn_rect = self.plus_Btn.get_rect(center=(540, 40))

        # 設定玩家與電腦手牌的位置
        self.player_card_pos = (490, 350)
        self.computer_card_pos = (50, 100)

        # 階段的旗標
        self.deal = False
        self.stand = False

    # 卡牌的各項數值
    class Card:
        def __init__(self, card_type, card_text, card_value):
            self.card_type = card_type
            self.card_text = card_text
            self.card_value = card_value
            self.card_img_name = card_type + card_text

    class Dealer:
        def __init__(self):
            # 設定好花色、文字和數值
            self.cards = []
            all_card_type = ('heart', 'diamond', 'club', 'spade')
            all_card_text = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
            all_card_value = [1, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]

            # 利用迴圈將每一張卡牌的花色、文字、數值結合起來，然後一一放進self.cards這個list裡面，就是創造一副牌
            for card_type in all_card_type:
                for index, card_text in enumerate(all_card_text):
                    card = BlackJack.Card(card_type, card_text, all_card_value[index])
                    self.cards.append(card)
            # 把list裡面隨機排序，也就是洗牌
            random.shuffle(self.cards)

            # 利用迴圈將所有卡牌圖樣與花色文字和卡背都load進self.cards_image這個字典
            self.cards_image = {}
            for Type in all_card_type:
                for text in all_card_text:
                    key = Type + text
                    self.cards_image[key] = pygame.image.load('images/21/' + key + '.jpg').convert()
            self.cards_image['back'] = pygame.image.load('images/21/back.jpg').convert()

        def send_card(self, role, num=1):
            # 將剛剛的self.cards裡面的牌pop出來，然後再把那張牌append到role.cards_in_hand這個list
            for i in range(num):
                card = self.cards.pop()
                role.cards_in_hand.append(card)
            role.calc_point()  # 重新計算手牌大小

        def shuffle_cards(self):
            # 像init一樣創造牌然後洗牌
            self.cards = []
            all_card_type = ('heart', 'diamond', 'club', 'spade')
            all_card_text = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
            all_card_value = [1, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
            for card_type in all_card_type:
                for index, card_text in enumerate(all_card_text):
                    card = BlackJack.Card(card_type, card_text, all_card_value[index])
                    self.cards.append(card)
            random.shuffle(self.cards)

    class Role:
        def __init__(self):
            self.points = 0
            self.cards_in_hand = []

        def calc_point(self):
            self.points = 0

            # 把手牌裡的每張牌的數值都利用剛剛字典加到自己的分數
            for card in self.cards_in_hand:
                self.points += card.card_value

            # 特別判定如果卡牌是A的話，如果不會爆就再加10變11，會爆就一樣是1
            for card in self.cards_in_hand:
                if card.card_text == 'A' and self.points + 10 <= 21:
                    self.points += 10

        def burst(self):
            # 算分數然後如果比21點大就爆
            self.calc_point()
            return self.points > 21

    def game_start(self):
        self.deal = False
        self.stand = False

        self.bet = 0

        # 把兩個人的手牌清空
        self.player.cards_in_hand = []
        self.computer.cards_in_hand = []

        blackjack.dealer.shuffle_cards()

        # 把圖片都貼到螢幕上
        self.screen.fill(BLACK)
        self.screen.blit(self.table, self.table_rect)
        self.screen.blit(self.deal_Btn, self.deal_Btn_rect)
        self.screen.blit(self.hit_Btn, self.hit_Btn_rect)
        self.screen.blit(self.stand_Btn, self.stand_Btn_rect)
        self.screen.blit(self.exit_Btn, self.exit_Btn_rect)
        self.screen.blit(self.bet_background, self.display_money_rect)
        self.screen.blit(self.minus_Btn, self.minus_Btn_rect)
        self.screen.blit(self.plus_Btn, self.plus_Btn_rect)

        # 把押注金額貼到螢幕上
        blackjack_text.text = str(self.bet)
        blackjack_text.x_y = self.display_money_rect.center
        blackjack_text.new_sentence()
        blackjack_text.draw()

        # 把體力跟存款都貼到螢幕上
        blackjack_text.text = (
                '   體力 : ' + str(variable.energy) + ' / ' + str(variable.ME) +
                '   存款 :' + str(variable.money)
        )
        blackjack_text.x_y = (320, 520)
        blackjack_text.new_sentence()
        blackjack_text.draw()

    # 把雙方手牌渲染到桌面
    def show_cards(self):
        self.player_card_pos = (490, 350)
        self.computer_card_pos = (50, 100)

        # 把玩家的每張手牌都貼到螢幕上，每放一張卡牌就把下一張卡牌往左一點
        for card in self.player.cards_in_hand:
            self.screen.blit(self.dealer.cards_image[card.card_img_name], self.player_card_pos)
            self.player_card_pos = (self.player_card_pos[0] - 105, (self.player_card_pos[1]))

        # 如果停牌的話，把電腦的每張手牌都貼到螢幕上，每放一張卡牌就把下一張卡牌往右一點
        if self.stand:
            for card in self.computer.cards_in_hand:
                self.screen.blit(self.dealer.cards_image[card.card_img_name], self.computer_card_pos)
                self.computer_card_pos = (self.computer_card_pos[0] + 105, (self.computer_card_pos[1]))

        # 如果沒有停牌的話，把一個卡背貼到螢幕上(莊家的第一張蓋牌)，然後往右一點再貼開的那張牌
        elif len(self.computer.cards_in_hand) > 1:
            self.screen.blit(self.dealer.cards_image['back'], self.computer_card_pos)
            self.computer_card_pos = (self.computer_card_pos[0] + 105, (self.computer_card_pos[1]))
            self.screen.blit(self.dealer.cards_image[self.computer.cards_in_hand[1].card_img_name],
                             self.computer_card_pos)

    def check(self):
        # 用role裡面的burst()看電腦的手牌是不是爆了，如果是，就加錢，然後在螢幕上貼'對家爆牌了'，然後再重新把該貼的都貼去
        if self.computer.burst():
            variable.money += self.bet
            blackjack_text.text = '對家爆牌了'
            blackjack_text.x_y = (320, 540)
            blackjack_text.new_sentence()
            blackjack_text.draw()
            FUNCS.update()
            FUNCS.delay(3000)
            self.game_start()

        # 用role裡面的burst()看玩家的手牌是不是爆了，如果是，就扣錢，然後在螢幕上貼'你爆牌了'，然後再重新把該貼的都貼去
        elif self.player.burst():
            variable.money -= self.bet
            blackjack_text.text = '你爆牌了'
            blackjack_text.x_y = (320, 540)
            blackjack_text.new_sentence()
            blackjack_text.draw()
            FUNCS.update()
            FUNCS.delay(3000)
            self.game_start()

        # 如果玩家的手牌超過五張，就賺兩倍，然後在螢幕上貼'你過五關了'，然後再重新把該貼的都貼去
        elif len(self.player.cards_in_hand) >= 5:
            variable.money += self.bet * 2
            blackjack_text.text = '你過五關了'
            blackjack_text.x_y = (320, 540)
            blackjack_text.new_sentence()
            blackjack_text.draw()
            FUNCS.update()
            FUNCS.delay(3000)
            self.game_start()
        # 如果電腦的手牌超過五張，就扣兩倍，然後在螢幕上貼'對家過五關了'，然後再重新把該貼的都貼去
        elif len(self.computer.cards_in_hand) >= 5:
            variable.money -= self.bet * 2
            blackjack_text.text = '對家過五關了'
            blackjack_text.x_y = (320, 540)
            blackjack_text.new_sentence()
            blackjack_text.draw()
            FUNCS.update()
            FUNCS.delay(3000)
            self.game_start()

    def running(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 偵測是不是點滑鼠左鍵了
            if self.deal_Btn_rect.collidepoint(event.pos):  # 偵測是不是點在deal那個框框裡

                # 如果還沒發牌而且押注金額大於0，那就扣體力然後發牌
                if not self.deal:
                    self.deal = True
                    if self.bet > 0:
                        variable.energy -= 1
                        self.dealer.send_card(self.player, 2)
                        self.dealer.send_card(self.computer, 2)
                        self.show_cards()
                        self.check()

                # 如果還沒發牌而且押注金額等於於0，那就貼'你還沒下注'到螢幕上
                    else:
                        blackjack_text.text = '你還沒下注'
                        blackjack_text.x_y = (320, 540)
                        blackjack_text.new_sentence()
                        blackjack_text.draw()
                        FUNCS.update()
                        FUNCS.delay(1000)
                        self.game_start()

            # 如果點hit那個框框而且已經發牌了，那就再發給玩家一張牌
            if self.hit_Btn_rect.collidepoint(event.pos):
                if self.deal:
                    self.dealer.send_card(self.player, 1)
                    self.show_cards()
                    self.check()

            # 如果點stand那個框框而且已經發牌了，那就把發牌(deal)變回False，然後把停牌(stand)變成True
            if self.stand_Btn_rect.collidepoint(event.pos):
                if self.deal:
                    self.deal = False
                    self.stand = True

            # 如果按exit那個框框，那就過場，然後回房間
            if self.exit_Btn_rect.collidepoint(event.pos):
                if not self.deal and not self.stand:
                    image = pygame.image.load(room_path)
                    transition.ready(image)
                    transition.hacker()
                    room.back()

            # 如果按那個減號而且沒有發牌也沒停牌再而且你已經有押注金額的話，就把押注金額-100然後重新貼到螢幕上
            if self.minus_Btn_rect.collidepoint(event.pos):
                if not self.deal and not self.stand:
                    if self.bet >= 100:
                        self.bet -= 100
                    self.screen.blit(self.bet_background, self.display_money_rect)
                    blackjack_text.text = str(self.bet)
                    blackjack_text.x_y = self.display_money_rect.center
                    blackjack_text.new_sentence()
                    blackjack_text.draw()

            # 如果按那個加號而且沒有發牌也沒停牌再而且你有錢可以下注100的話，就把押注金額+100然後重新貼到螢幕上
            if self.plus_Btn_rect.collidepoint(event.pos):
                if not self.deal and not self.stand:
                    if self.bet + 100 <= variable.money:
                        self.bet += 100
                    self.screen.blit(self.bet_background, self.display_money_rect)
                    blackjack_text.text = str(self.bet)
                    blackjack_text.x_y = self.display_money_rect.center
                    blackjack_text.new_sentence()
                    blackjack_text.draw()

    def computer_hit(self):
        # 算分數，然後如果電腦的分數比玩家低的話就加牌到電腦手牌，如果電腦手牌=21或比玩家的手牌大就呼叫函式is_win
        self.computer.calc_point()
        self.player.calc_point()
        if self.computer.points < self.player.points:
            self.dealer.send_card(self.computer, 1)
        elif self.computer.points == 21:
            self.is_win()
        else:
            self.is_win()

    def is_win(self):
        # 如果電腦和玩家都沒爆，那就算分數
        if not self.computer.burst() and not self.player.burst():
            self.computer.calc_point()
            self.player.calc_point()
            player_points = self.player.points
            computer_points = self.computer.points

            # 如果分數一樣，就把該放的文字放一放然後重新開始
            if player_points == computer_points:
                blackjack_text.text = (
                        '你的點數為' + str(player_points) +
                        '對家的點數為' + str(computer_points) +
                        '，平局'
                )
                blackjack_text.x_y = (320, 540)
                blackjack_text.new_sentence()
                blackjack_text.draw()
                FUNCS.update()
                FUNCS.delay(3000)
                self.game_start()

            # 如果分數不一樣，就扣錢，然後把該放的文字放一放，然後重新開始
            else:
                variable.money -= self.bet
                blackjack_text.text = (
                        '你的點數為' + str(player_points) +
                        '對家的點數為' + str(computer_points) +
                        '，你輸了'
                )
                blackjack_text.x_y = (320, 540)
                blackjack_text.new_sentence()
                blackjack_text.draw()
                FUNCS.update()
                FUNCS.delay(3000)
                self.game_start()


blackjack = BlackJack(SCREEN)  # 把blackjack宣告為這個class


# 定義房間class
class ROOM:
    # 初始化
    def __init__(self, screen):
        self.screen = screen

        # 設定對話框圖像
        self.text_box = pygame.image.load("images/game/square.png").convert_alpha()  # 讀入圖像
        self.text_box = pygame.transform.scale(self.text_box, (800, 180))  # 改變至適當大小
        self.text_box.set_alpha(230)  # 設定透明度 並非所有圖像皆需要
        self.text_box_rect = self.text_box.get_rect(center=(400, 520))  # 設定邊界與中心

        # 設定房間背景
        self.room = pygame.image.load("images/room/none.png").convert_alpha()
        self.room = pygame.transform.scale(self.room, FULLSCREEN)
        self.room_rect = self.room.get_rect()

        # 設定說明圖像
        self.information_Btn = pygame.image.load('images/room/informationBtn1.png')
        self.information_Btn = pygame.transform.scale(self.information_Btn, (80, 80))
        self.information_Btn_rect = self.information_Btn.get_rect(center=(760, 40))
        self.work_info = pygame.image.load('images/room/game_information.png').convert()
        self.work_info.set_colorkey(WHITE)
        self.work_info = pygame.transform.scale(self.work_info, (576, 432))
        self.work_info_rect = self.work_info.get_rect(center=SCREEN_CENTER)
        self.casino_info = pygame.image.load('images/room/blackjack_information.png').convert()
        self.casino_info.set_colorkey(WHITE)
        self.casino_info = pygame.transform.scale(self.casino_info, (576, 432))
        self.casino_info_rect = self.casino_info.get_rect(center=SCREEN_CENTER)
        self.train_info = pygame.image.load('images/room/train_information.png').convert()
        self.train_info.set_colorkey(WHITE)
        self.train_info = pygame.transform.scale(self.train_info, (576, 432))
        self.train_info_rect = self.train_info.get_rect(center=SCREEN_CENTER)
        
        # 設定房間內物件圖像
        self.items = {
            'phone': pygame.image.load("images/room/phone.png").convert_alpha(),
            'door': pygame.image.load("images/room/door_closed.png").convert_alpha(),
            'door_closed': pygame.image.load("images/room/door_closed_1.png").convert_alpha(),
            'bed': pygame.image.load("images/room/bed.png").convert_alpha(),
            'book': pygame.image.load("images/room/level0.png").convert_alpha(),
            'exercise': pygame.image.load("images/room/exercise.png").convert_alpha()
        }

        # 縮放物件圖像
        self.items['phone'] = pygame.transform.scale(self.items['phone'], (23, 31))
        self.items['door'] = pygame.transform.scale(self.items['door'], (368 / 3, 890 / 3))
        self.items['door_closed'] = pygame.transform.scale(self.items['door_closed'], FULLSCREEN)
        self.items['bed'] = pygame.transform.scale(self.items['bed'], (931 / 3, 466 / 3))
        self.items['exercise'] = pygame.transform.scale(self.items['exercise'], (219 / 3, 280 / 3))
        self.items['book'] = pygame.transform.scale(self.items['book'], (366 / 3, 535 / 3))

        # 設定物件邊緣發亮時圖像
        self.items_light = {
            'phone': pygame.image.load("images/room/phone_l.png").convert_alpha(),
            'door': pygame.image.load("images/room/door_open.png").convert_alpha(),
            'light': pygame.image.load("images/room/door_light.png").convert_alpha(),
            'bed': pygame.image.load("images/room/bed_l.png").convert_alpha(),
            'book': pygame.image.load("images/room/level0_l.png").convert_alpha(),
            'exercise': pygame.image.load("images/room/exercise_l.png").convert_alpha()
        }

        # 縮放發亮圖像
        self.items_light['phone'] = pygame.transform.scale(self.items_light['phone'], (23, 31))
        self.items_light['door'] = pygame.transform.scale(self.items_light['door'], FULLSCREEN)
        self.items_light['light'] = pygame.transform.scale(self.items_light['light'], FULLSCREEN)
        self.items_light['bed'] = pygame.transform.scale(self.items_light['bed'], (896 / 3, 450 / 3))
        self.items_light['exercise'] = pygame.transform.scale(self.items_light['exercise'], (219 / 3, 280 / 3))
        self.items_light['book'] = pygame.transform.scale(self.items_light['book'], (366 / 3, 535 / 3))

        # 設定物件的矩形邊界
        self.rect = {
            'phone': self.items['phone'].get_rect(),
            'door': self.items['door'].get_rect(),
            'door_closed': self.items['door_closed'].get_rect(),
            'book': self.items['book'].get_rect(),
            'exercise': self.items['exercise'].get_rect(),
            'bed': self.items['bed'].get_rect(),
            'phone_l': self.items_light['phone'].get_rect(),
            'door_l': self.items_light['door'].get_rect(),
            'light': self.items_light['light'].get_rect(),
            'book_l': self.items_light['book'].get_rect(),
            'exercise_l': self.items_light['exercise'].get_rect(),
            'bed_l': self.items_light['bed'].get_rect()
        }

        # 設定物件矩形中心的位置
        self.rect['phone'].center = (300, 400)
        self.rect['door'].center = (120, 380)
        self.rect['door_closed'].center = SCREEN_CENTER
        self.rect['bed'].center = (640, 530)
        self.rect['exercise'].center = (300, 540)
        self.rect['book'].center = (500, 332)

        self.rect['phone_l'].center = (300, 400)
        self.rect['door_l'].center = SCREEN_CENTER
        self.rect['light'].center = SCREEN_CENTER
        self.rect['bed_l'].center = (640, 530)
        self.rect['exercise_l'].center = (300, 540)
        self.rect['book_l'].center = (500, 332)

        # 設定按鈕圖像及矩形邊界
        self.button = pygame.image.load("images/room/button.png").convert_alpha()
        self.button = pygame.transform.scale(self.button, (300, 100))
        self.button_rect = self.button.get_rect(center=(400, 200))

        # 設定狀態欄圖像及矩形邊界
        self.status_bar = pygame.image.load("images/room/status.png").convert_alpha()
        self.status_bar = pygame.transform.scale(self.status_bar, FULLSCREEN)
        self.status_bar_rect = self.status_bar.get_rect(center=SCREEN_CENTER)

        # 初始化每日吃飯旗標
        self.eating_flag = False

        # 初始化說明旗標
        self.info_flag = True

        # 初始化書櫃的等級為 0
        self.book_LV = 0

    # 回房間時渲染畫面
    def back(self):
        variable.state = 'room'
        variable.room_flag = True
        self.screen.blit(self.room, self.room_rect)
        self.screen.blit(self.items['phone'], self.rect['phone'])
        self.screen.blit(self.items['door_closed'], self.rect['door_closed'])
        self.screen.blit(self.items['bed'], self.rect['bed'])
        self.screen.blit(self.items['exercise'], self.rect['exercise'])
        self.screen.blit(self.items['book'], self.rect['book'])
        self.screen.blit(self.status_bar, self.status_bar_rect)
        val.update_val()
        val.draw()
        FUNCS.update()

    # 檢查房間內各種事件
    def check(self, event):
        global room_path
        # 鼠標移動到物件上時發亮提示
        if event.type == pygame.MOUSEMOTION:
            if self.rect['phone'].collidepoint(event.pos):
                self.screen.blit(self.items_light['phone'], self.rect['phone_l'])
            elif self.rect['door'].collidepoint(event.pos):
                self.screen.blit(self.room, self.room_rect)
                self.screen.blit(self.items['phone'], self.rect['phone'])
                self.screen.blit(self.items_light['door'], self.rect['door_l'])
                self.screen.blit(self.items_light['light'], self.rect['light'])
                self.screen.blit(self.items['bed'], self.rect['bed'])
                self.screen.blit(self.items['exercise'], self.rect['exercise'])
                self.screen.blit(self.items['book'], self.rect['book'])
                self.screen.blit(self.status_bar, self.status_bar_rect)
                val.update_val()
                val.draw()
            elif self.rect['bed'].collidepoint(event.pos):
                self.screen.blit(self.items_light['bed'], self.rect['bed_l'])
            elif self.rect['exercise'].collidepoint(event.pos):
                self.screen.blit(self.items_light['exercise'], self.rect['exercise_l'])
            elif self.rect['book'].collidepoint(event.pos):
                self.screen.blit(self.items_light['book'], self.rect['book_l'])
            else:
                self.back()

        # 鼠標點擊各物件時觸發事件
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 點擊手機時選擇是否前往工作
            if self.rect['phone'].collidepoint(event.pos):
                if self.check_event('phone'):
                    variable.energy -= 15
                    image = pygame.image.load("images/room/work.png")
                    transition.ready(image)
                    transition.hacker()  # 轉場
                    # 工作事件的初始化
                    event_num = work.random_event()
                    work.event_init(work.events[event_num])
                    work.next_question()
                    variable.state = 'work'
                else:
                    self.back()
            # 點擊房門時選擇是否出門與前往哪裡
            if self.rect['door'].collidepoint(event.pos):
                if self.check_event('door'):
                    self.screen.blit(self.room, self.room_rect)
                    self.screen.blit(self.items['phone'], self.rect['phone'])
                    self.screen.blit(self.items_light['door'], self.rect['door_l'])
                    self.screen.blit(self.items_light['light'], self.rect['light'])
                    self.screen.blit(self.items['bed'], self.rect['bed'])
                    self.screen.blit(self.items['exercise'], self.rect['exercise'])
                    self.screen.blit(self.items['book'], self.rect['book'])
                    self.screen.blit(self.status_bar, self.status_bar_rect)
                    val.update_val()
                    val.draw()
                    roomText.text = '要去哪裡'
                    self.screen.blit(self.text_box, self.text_box_rect)
                    roomText.x_y = (400, 500)
                    roomText.new_sentence()
                    roomText.draw()
                    FUNCS.update()
                    # 選擇前往賭場或購物中心
                    res = self.where()
                    if res == 'casino':
                        variable.energy -= 5
                        # 前往賭場的初始化
                        variable.state = 'blackjack'
                        image = pygame.image.load('images/21/table.png')
                        transition.ready(image)
                        transition.hacker()  # 轉場
                        blackjack.game_start()
                    elif res == 'shop':
                        variable.energy -= 5
                        # 前往購物中心
                        image = pygame.image.load('images/room/shopping_mall.png')
                        transition.ready(image)
                        transition.hacker()  # 轉場
                        # 選擇在購物中心的事件
                        res = self.shopping()
                        # 選擇吃飯
                        if res == 'eating':
                            variable.money -= 150  # 吃飯要付錢
                            variable.energy += 20  # 吃飯回體力
                            # 超出體力上限時只回到體力上限
                            if variable.energy > variable.ME:
                                variable.energy = variable.ME
                            image = pygame.image.load(room_path).convert_alpha()
                            transition.ready(image)
                            transition.hacker()  # 轉場
                            self.screen.blit(self.text_box, self.text_box_rect)
                            roomText.text = '吃飽後回復了一些體力'
                            roomText.x_y = (400, 500)
                            roomText.new_sentence()
                            roomText.draw()
                            FUNCS.update()
                            FUNCS.delay(2000)
                            self.back()
                        # 選擇升級書櫃
                        elif res == 'buy books':
                            variable.money -= 200  # 買書要付錢
                            self.book_LV += 1  # 書櫃升級
                            # 改書櫃的圖
                            path = "images/room/level" + str(self.book_LV) + ".png"
                            self.items['book'] = pygame.image.load(path).convert_alpha()
                            self.items['book'] = pygame.transform.scale(self.items['book'], (366 / 3, 535 / 3))
                            path = "images/room/level" + str(self.book_LV) + "_l.png"
                            self.items_light['book'] = pygame.image.load(path).convert_alpha()
                            self.items_light['book'] = pygame.transform.scale(self.items_light['book'], (366 / 3, 535 / 3))
                            room_path = "images/room/room_lv" + str(self.book_LV) + ".png"
                            image = pygame.image.load(room_path).convert_alpha()
                            transition.ready(image)
                            transition.hacker()  # 轉場
                            self.screen.blit(self.text_box, self.text_box_rect)
                            roomText.text = '書櫃變得更充實了'
                            roomText.x_y = (400, 500)
                            roomText.new_sentence()
                            roomText.draw()
                            FUNCS.update()
                            FUNCS.delay(2000)
                        # 選擇觀察人群提升話術
                        elif res == 'observe':
                            variable.energy -= 10  # 減少體力
                            variable.SA += 1  # 提升話術
                            image = pygame.image.load(room_path).convert_alpha()
                            transition.ready(image)
                            transition.hacker()  # 轉場
                            self.screen.blit(self.text_box, self.text_box_rect)
                            roomText.text = '透過觀察銷售員的口條，你學到了一些技巧'
                            roomText.x_y = (400, 500)
                            roomText.new_sentence()
                            roomText.draw()
                            FUNCS.update()
                            FUNCS.delay(2000)
                            self.back()
                    else:
                        self.back()
                else:
                    self.back()
            # 點擊床是否睡覺回復體力並換日
            if self.rect['bed'].collidepoint(event.pos):
                if self.check_event('bed'):
                    variable.energy += variable.ME  # 回復最大體力的數值
                    if variable.energy >= variable.ME:  # 大於最大體力時只回復到最大體力
                        variable.energy = variable.ME
                        roomText.text = '你睡得很好，感覺精力充沛'
                    elif variable.energy >= 0:  # 體力為負數時不會回滿
                        roomText.text = '可能是昨天太累了，你起床時仍然很疲倦'
                    elif variable.energy < 0:  # 回復後體力仍為負數時進入BAD END
                        variable.state = 'end'
                        background = pygame.image.load('images/anime/ending/tired/tired_1.jpg')
                        transition.ready(background)
                        transition.hacker()
                        anime.ending_tired()  # BAD END 動畫
                    roomText.x_y = (400, 500)
                    variable.days += 1   # 將經歷天數+1
                    if variable.days == 7:  # 經歷7天後進行結局判定
                        variable.state = 'end'  # 更改state
                        if variable.catch >= 100:  # 被捕率過高 進入監獄結局
                            background = pygame.image.load('images/anime/ending/jail/jail_1.jpg')
                            transition.ready(background)
                            transition.hacker()
                            anime.ending_jail()
                        elif variable.money < variable.KPI:  # 未達成目標金額 進入BAD END
                            background = pygame.image.load('images/anime/ending/boss/boss_1.jpg')
                            transition.ready(background)
                            transition.hacker()  # 轉場
                            anime.ending_boss()  # BAD END 動畫
                        else:  # 達成目標金額 進入GOOD END
                            background = pygame.image.load('images/anime/ending/good_end/happy_1.jpg')
                            transition.ready(background)
                            transition.hacker()  # 轉場
                            anime.ending_good_end()  # GOOD END 動畫
                    if variable.today == 6:  # 週日後變回週一
                        variable.today = 0
                    else:
                        variable.today += 1
                    self.eating_flag = False  # 換日後重製旗標
                    image = pygame.image.load(room_path).convert_alpha()
                    transition.ready(image)
                    transition.hacker()  # 轉場
                    self.screen.blit(self.text_box, self.text_box_rect)
                    roomText.new_sentence()
                    roomText.draw()
                    FUNCS.update()
                    FUNCS.delay(2000)
                    self.back()
                else:
                    self.back()
            # 點擊健身器材選擇是否進行QTE小遊戲
            if self.rect['exercise'].collidepoint(event.pos):
                if self.check_event('exercise'):
                    image = pygame.image.load("images/anime/train1_1.jpg").convert_alpha()
                    transition.ready(image)
                    transition.hacker()  # 轉場
                    variable.energy -= 20  # 扣除體力
                    variable.state = 'train'  # 更改state
                    train.start_game()
                else:
                    self.back()
            # 點擊書櫃選擇是否閱讀增加創造力與話術
            if self.rect['book'].collidepoint(event.pos):
                if self.check_event('book'):
                    variable.energy -= 10  # 扣除體力
                    variable.CP += 1 + self.book_LV  # 創造力增加量取決於書櫃等級
                    variable.SA += 1 + self.book_LV // 2  # 話術增加量取決於書櫃等級
                    image = pygame.image.load(room_path).convert_alpha()
                    transition.ready(image)
                    transition.hacker()  # 轉場
                    self.screen.blit(self.text_box, self.text_box_rect)
                    roomText.x_y = (400, 500)
                    roomText.text = '你讀了一陣子書，增加了一些創造力與話術'
                    roomText.new_sentence()
                    roomText.draw()
                    FUNCS.update()
                    FUNCS.delay(2000)
                    self.back()
                else:
                    self.back()

    # 各項事件的確認
    def check_event(self, event_item):
        if event_item == 'phone':
            if variable.energy < 15:
                return self.no_energy(event_item)
            else:
                roomText.text = '要工作嗎(消耗15體力開啟事件)'
        elif event_item == 'door':
            if variable.energy < 5:
                return self.no_energy(event_item)
            else:
                roomText.text = '要出門嗎(消耗5體力)'
        elif event_item == 'bed':
            roomText.text = '要睡覺了嗎(回復體力)'
        elif event_item == 'exercise':
            if variable.energy < 20:
                return self.no_energy(event_item)
            else:
                roomText.text = '要開始健身嗎(消耗20體力增加體力上限)'
        elif event_item == 'book':
            if variable.energy < 10:
                return self.no_energy(event_item)
            else:
                roomText.text = '要讀書嗎(消耗10體力增加創造力與話術)'
        self.screen.blit(self.text_box, self.text_box_rect)
        roomText.x_y = (400, 500)
        roomText.new_sentence()
        roomText.draw()
        FUNCS.update()
        return self.yes_or_no(event_item)

    # 體力不足時的提醒
    def no_energy(self, event_item):
        self.screen.blit(self.text_box, self.text_box_rect)
        roomText.text = '你累壞了 確定還要繼續嗎'
        roomText.x_y = (400, 500)
        roomText.new_sentence()
        roomText.draw()
        FUNCS.update()
        return self.yes_or_no(event_item)

    # 是否的判斷
    def yes_or_no(self, event_item):
        self.button_rect.center = (400, 200)
        self.screen.blit(self.button, self.button_rect)
        # 用來判斷點擊的邊界
        temp_rect = pygame.Rect(
            self.button_rect.x,
            self.button_rect.y + 100,
            self.button_rect.width,
            self.button_rect.height
        )
        self.screen.blit(self.button, temp_rect)
        roomText.text = '確認進行'
        roomText.x_y = self.button_rect.center
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '還是算了'
        roomText.x_y = (self.button_rect.centerx, self.button_rect.centery + 100)
        roomText.new_sentence()
        roomText.draw()
        if event_item == 'phone' or event_item == 'exercise':
            self.screen.blit(self.information_Btn, self.information_Btn_rect)
        FUNCS.update()
        self.info_flag = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.info_flag:
                        if self.button_rect.collidepoint(event.pos):
                            return True
                        elif temp_rect.collidepoint(event.pos):
                            return False
                if event.type == pygame.MOUSEMOTION:
                    if self.information_Btn_rect.collidepoint(event.pos):
                        if self.information_Btn_rect.collidepoint(event.pos):
                            if event_item == 'phone':
                                self.screen.blit(self.work_info, self.work_info_rect)
                                FUNCS.update()
                                self.info_flag = False
                            elif event_item == 'exercise':
                                self.screen.blit(self.train_info, self.train_info_rect)
                                FUNCS.update()
                                self.info_flag = False
                        self.info_flag = False
                    elif not self.info_flag:
                        self.info_flag = True
                        self.screen.blit(self.room, self.room_rect)
                        self.screen.blit(self.items['phone'], self.rect['phone'])
                        self.screen.blit(self.items['door_closed'], self.rect['door_closed'])
                        self.screen.blit(self.items['bed'], self.rect['bed'])
                        self.screen.blit(self.items['exercise'], self.rect['exercise'])
                        self.screen.blit(self.items['book'], self.rect['book'])
                        self.screen.blit(self.status_bar, self.status_bar_rect)
                        val.update_val()
                        val.draw()
                        return self.check_event(event_item)

    # 回傳出門的地點
    def where(self):
        self.button_rect.center = (400, 150)
        self.screen.blit(self.button, self.button_rect)
        # 用來判斷點擊的邊界
        temp_rect1 = pygame.Rect(
            self.button_rect.x,
            self.button_rect.y + 100,
            self.button_rect.width,
            self.button_rect.height
        )
        # 用來判斷點擊的邊界
        temp_rect2 = pygame.Rect(
            self.button_rect.x,
            self.button_rect.y + 200,
            self.button_rect.width,
            self.button_rect.height
        )
        self.screen.blit(self.button, temp_rect1)
        self.screen.blit(self.button, temp_rect2)
        roomText.text = '去賭場'
        roomText.x_y = self.button_rect.center
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '去購物中心'
        roomText.x_y = (temp_rect1.centerx, temp_rect1.centery)
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '還是算了'
        roomText.x_y = (temp_rect2.centerx, temp_rect2.centery)
        roomText.new_sentence()
        roomText.draw()
        self.screen.blit(self.information_Btn, self.information_Btn_rect)
        FUNCS.update()
        self.info_flag = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.info_flag:
                        if self.button_rect.collidepoint(event.pos):
                            return 'casino'
                        elif temp_rect1.collidepoint(event.pos):
                            return 'shop'
                        elif temp_rect2.collidepoint(event.pos):
                            return 'back'
                if event.type == pygame.MOUSEMOTION:
                    if self.information_Btn_rect.collidepoint(event.pos):
                        self.screen.blit(self.casino_info, self.casino_info_rect)
                        FUNCS.update()
                        self.info_flag = False
                    elif not self.info_flag:
                        self.info_flag = True
                        self.screen.blit(self.room, self.room_rect)
                        self.screen.blit(self.items['phone'], self.rect['phone'])
                        self.screen.blit(self.items['door_closed'], self.rect['door_closed'])
                        self.screen.blit(self.items['bed'], self.rect['bed'])
                        self.screen.blit(self.items['exercise'], self.rect['exercise'])
                        self.screen.blit(self.items['book'], self.rect['book'])
                        self.screen.blit(self.status_bar, self.status_bar_rect)
                        val.update_val()
                        val.draw()
                        return self.where()

    # 購物中心中的事件
    def shopping(self):
        # 渲染購物中心的背景、對話框、按鈕
        background = pygame.image.load("images/room/shopping_mall.png")
        background = pygame.transform.scale(background, FULLSCREEN)
        background_rect = background.get_rect(center=SCREEN_CENTER)
        self.screen.blit(background, background_rect)
        self.screen.blit(self.text_box, self.text_box_rect)
        self.button_rect.center = (400, 100)
        self.screen.blit(self.button, self.button_rect)
        # 用來判斷點擊的邊界
        temp_rect1 = pygame.Rect(
            self.button_rect.x,
            self.button_rect.y + 100,
            self.button_rect.width,
            self.button_rect.height
        )
        # 用來判斷點擊的邊界
        temp_rect2 = pygame.Rect(
            self.button_rect.x,
            self.button_rect.y + 200,
            self.button_rect.width,
            self.button_rect.height
        )
        self.screen.blit(self.button, temp_rect1)
        self.screen.blit(self.button, temp_rect2)
        roomText.text = '在購物中心要幹嘛'
        roomText.x_y = (400, 500)
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '找餐廳吃飯(150元)'
        roomText.x_y = self.button_rect.center
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '買新書(200元)'
        roomText.x_y = temp_rect1.center
        roomText.new_sentence()
        roomText.draw()
        roomText.text = '觀察人群(10體力)'
        roomText.x_y = temp_rect2.center
        roomText.new_sentence()
        roomText.draw()
        FUNCS.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        if self.eating_flag:  # 確認今日是否吃過了
                            self.screen.fill(BLACK)
                            self.screen.blit(self.text_box, self.text_box_rect)
                            roomText.text = '你今天吃過飯了'
                            roomText.x_y = (400, 500)
                            roomText.new_sentence()
                            roomText.draw()
                            FUNCS.update()
                            FUNCS.delay(2000)
                            return self.shopping()  # 回去重選
                        else:
                            if variable.money >= 150:  # 確認是否有錢
                                self.eating_flag = True  # 該改旗標
                                return 'eating'
                            else:
                                self.screen.fill(BLACK)
                                self.screen.blit(self.text_box, self.text_box_rect)
                                roomText.text = '你窮死了'
                                roomText.x_y = (400, 500)
                                roomText.new_sentence()
                                roomText.draw()
                                FUNCS.update()
                                FUNCS.delay(2000)
                                return self.shopping()  # 回去重選
                    elif temp_rect1.collidepoint(event.pos):
                        if self.book_LV < 4:  # 確認書櫃是否已滿等
                            if variable.money >= 200:  # 確認是否有錢
                                return 'buy books'
                            else:
                                self.screen.fill(BLACK)
                                self.screen.blit(self.text_box, self.text_box_rect)
                                roomText.text = '你窮死了'
                                roomText.x_y = (400, 500)
                                roomText.new_sentence()
                                roomText.draw()
                                FUNCS.update()
                                FUNCS.delay(2000)
                                return self.shopping()
                        else:
                            self.screen.fill(BLACK)
                            self.screen.blit(self.text_box, self.text_box_rect)
                            roomText.text = '沒什麼新書好買了'
                            roomText.x_y = (400, 500)
                            roomText.new_sentence()
                            roomText.draw()
                            FUNCS.update()
                            FUNCS.delay(2000)
                            return self.shopping()
                    elif temp_rect2.collidepoint(event.pos):  # 選擇觀察人群
                        return 'observe'


room = ROOM(SCREEN)  # 把room宣告為這個class


# 主要遊戲(打地鼠)的class
class MainGame:
    # 初始化
    def __init__(self, screen):
        self.screen = screen

        # 對話框圖像的設定
        self.text_box = pygame.image.load("images/game/square.png").convert_alpha()
        self.text_box = pygame.transform.scale(self.text_box, (800, 200))
        self.text_box.set_alpha(255)
        self.text_box_rect = self.text_box.get_rect(center=(400, 525))

        # 手機螢幕與背景圖像的設定
        self.phone_screen = pygame.image.load("images/game/phone_screen.png").convert_alpha()
        self.phone_screen = pygame.transform.scale(self.phone_screen, FULLSCREEN)
        self.phone_screen_rect = self.phone_screen.get_rect(center=SCREEN_CENTER)

        # 被點擊圖像(地鼠)的設定
        self.idea = pygame.image.load("images/game/mole.png").convert_alpha()
        self.idea = pygame.transform.scale(self.idea, (170, 170))
        self.idea_rect = self.idea.get_rect(center=(400, 300))
        self.idea_alpha = 0

        # 對話紀錄圖像的設定
        self.conversation_record_image = pygame.image.load("images/game/conversation_record/none.png")
        self.conversation_record_rect = self.conversation_record_image.get_rect(center=(630, 230))
        self.image_path = ''  # 讀取圖像路徑

        # 信賴度條圖像設定
        self.trust_value_image = pygame.image.load("images/game/trust_image/-0.png")
        self.trust_value_rect = self.trust_value_image.get_rect(center=(180, 15))

        self.text = ()  # 問題句子

        self.line_color = (134, 159, 193)  # line底色

        self.time = 0  # 時間變數

        self.idea_disappear_speed = 256 + variable.CP * 10  # 地鼠消失速度
        self.answer_appear_frequency = random.randint(1, max(4, 10 - variable.CP))  # 正確答案出現頻率

        self.trust_init_value = 4 + variable.SA  # 初始信賴度
        self.trust_decrease_value = 0  # 下降信賴度

        self.word_type = ()  # 出現詞語詞性
        self.answer_word = ()  # 正確答案
        self.now_word = ''  # 現在出現詞語

        self.word_list = ()  # 可能出現詞語list

        self.now_question_num = 0  # 現在問題編號變數
        self.question_line = ()  # 第幾行會出現問題
        self.now_line = 0  # 現在在第幾行
        self.event_line_num = 0  # 本事件問題共有幾行

        self.game_flag = False  # 判斷是否進到遊戲的flag
        self.answer_frequency_flag = 0  # 已經幾次沒出現正確答案
        self.check_flag = False  # 避免誤觸 第一次check時不會觸發點擊事件

        # 各項事件
        self.events = []
        self.events.append(
            (
                ('結清', '追究', '信用', '承擔'),
                ('verb', 'verb', 'noun', 'verb'),
                (2, 4),
                ('受委託方Tenga的委託，你還有欠費尾數尚未___，現在已經正式開始___，請馬上回覆否則後果自負。',
                 '受委託方Tenga的委託，你還有欠費尾數尚未結清，現在已經正式開始___，請馬上回覆否則後果自負。',
                 '還有三天時間處理欠費問題，避免欠費糾紛影響到___不良記錄，超過時限自己___二十萬罰款',
                 '還有三天時間處理欠費問題，避免欠費糾紛影響到信用不良記錄，超過時限自己___二十萬罰款'
                 ),
                1,
                6
            )
        )
        self.events.append(
            (
                ('努力', '收穫', '公司', '規定'),
                ('noun', 'noun', 'noun', 'verb'),
                (0, 2),
                ('打字生財！靠自己的___從網路賺錢！一份耕耘一分___，只要你認真打字，錢源滾滾來！',
                 '打字生財！靠自己的努力從網路賺錢！一份耕耘一分___，只要你認真打字，錢源滾滾來！',
                 '當然可以阿，只要每天都達到______的配給量，我們就會把錢直接傳去你的信用卡喔。',
                 '當然可以阿，只要每天都達到公司___的配給量，我們就會把錢直接傳去你的信用卡喔。'
                 ),
                2,
                6
            )
        )
        self.events.append(
            (
                ('詐騙集團', '專業黑客'),
                ('people', 'people'),
                (2, None),
                ('只要妳傳給我們___的line或電話，我們公司的___就可以盜取對方資料並把錢拿回來。',
                 '只要妳傳給我們詐騙集團的line或電話，我們公司的___就可以盜取對方資料並把錢拿回來。',
                 ),
                3,
                6
            )
        )
        self.events.append(
            (
                ('老師', '股票', '調查', '資金'),
                ('people', 'noun', 'verb', 'noun'),
                (0, 2),
                ('散戶的力量小！團結的散戶力量大！只要輕鬆跟著___走，立馬從___賺大錢。',
                 '散戶的力量小！團結的散戶力量大！只要輕鬆跟著老師走，立馬從___賺大錢。',
                 '老師會去___哪支股票適合投資，再找參與的散戶一起將___灌入股票市場，等老師指令再全數賣出就可以了。',
                 '老師會去調查哪支股票適合投資，再找參與的散戶一起將___灌入股票市場，等老師指令再全數賣出就可以了。'
                 ),
                4,
                6
            )
        )
        self.events.append(
            (
                ('台南二中', '國文老師', '幫過', '請假單'),
                ('noun', 'people', 'verb', 'noun'),
                (0, 4),
                ('您好，我是______鄭旭風。',
                 '您好，我是台南二中___鄭旭風。',
                 '你現在___我，我承諾之後都幫你簽___，謝謝。',
                 '你現在幫過我，我承諾之後都幫你簽___，謝謝。'
                 ),
                5,
                6
            )
        )
        self.events.append(
            (
                ('滿分', '數學考卷', '69', '影片'),
                ('noun', 'noun', 'verb', 'noun'),
                (2, 4),
                ('我現在被困在沒有___的___裡，還差70000元就可以逃出來。我的支付寶號碼是6969696969。',
                 '我現在被困在沒有滿分的___裡，還差70000元就可以逃出來。我的支付寶號碼是6969696969。',
                 '你現在幫過我，我承諾讓你跟我___，還會讓你出現在我們最新的___裡，謝謝',
                 '你現在幫過我，我承諾讓你跟我69，還會讓你出現在我們最新的___裡，謝謝'
                 ),
                6,
                6
            )
        )
        self.events.append(
            (
                ('欠款', '繳交', '費用', '扣除'),
                ('noun', 'verb', 'noun', 'verb'),
                (2, 4),
                ('我們銀行這邊發現你有一項___還未繳交，這邊可能要麻煩您再重新___一次喔。',
                 '我們銀行這邊發現你有一項欠款還未繳交，這邊可能要麻煩您再重新___一次喔。',
                 '基本上是帳戶更新相關的___，如果沒有即時繳交可能會直接從您的銀行帳戶___更多款項喔。',
                 '基本上是帳戶更新相關的費用，如果沒有即時繳交可能會直接從您的銀行帳戶___更多款項喔。'
                 ),
                7,
                6
            )
        )
        self.events.append(
            (
                ('操作', '額外收入', '時間', '專業人員'),
                ('verb', 'noun', 'noun', 'people'),
                (2, 4),
                ('我們主要跟著團隊指令來___創造廣告流量,用互惠合作的模式來增加___。一天增加600-1500的零用錢，一個月下來也很可觀!',
                 '我們主要跟著團隊指令來操作創造廣告流量,用互惠合作的模式來增加___。一天增加600-1500的零用錢，一個月下來也很可觀!',
                 '如果妳有興趣每天用一點點___增加收入的話,可以請___跟妳解釋+評估妳的 適合項目唷，方便的話請傳給我身分證、健保卡的照片。',
                 '如果妳有興趣每天用一點點時間增加收入的話,可以請___跟妳解釋+評估妳的 適合項目唷，方便的話請傳給我身分證、健保卡的照片。'
                 ),
                8,
                6
            )
        )
        self.events.append(
            (
                ('成績', '複查', '費用', '銀行'),
                ('noun', 'verb', 'noun', 'noun'),
                (0, 2),
                ('113學科能力測驗___通知，應試號碼11277886699國:6,英:7,數A:5,數B:1,社:3,自:7。如需___成績請回覆。',
                 '113學科能力測驗成績通知，應試號碼11277886699國:6,英:7,數A:5,數B:1,社:3,自:7。如需___成績請回覆。',
                 '如需複查成績，請繳交___到此___帳戶：6969696969。',
                 '如需複查成績，請繳交費用到此___帳戶：6969696969。'
                 ),
                9,
                6
            )
        )
        self.events.append(
            (
                ('賴清德', '廁所', '競選團隊', '大尾鱸鰻'),
                ('people', 'noun', 'people', 'noun'),
                (2, 4),
                (
                    '我還沒死，我現在被困在___競選總部的___，還差50000元就可以逃出來。我的支付寶號碼是6969696969。',
                    '我還沒死，我現在被困在賴清德競選總部的___，還差50000元就可以逃出來。我的支付寶號碼是6969696969。',
                    '你現在幫過我，我承諾讓你加入我的___，並邀請你一起拍___4，謝謝。',
                    '你現在幫過我，我承諾讓你加入我的競選團隊，並邀請你一起拍___4，謝謝。'
                ),
                10,
                6
            )
        )
    @staticmethod
    def random_event():
        return random.randint(0, 9)

    # 事件初始化 event = (正確答案, 詞條詞性, 第幾行出現問題, 問題句子, 事件編號, 事件有幾行)
    def event_init(self, events):
        self.answer_word = events[0]
        self.word_type = events[1]
        self.question_line = events[2]
        self.text = events[3]
        self.image_path = 'images/game/conversation_record/' + str(events[4]) + '/'
        self.now_question_num = 0
        self.now_line = 0
        self.event_line_num = events[5]
        self.trust_init_value = 4 + variable.SA
        self.trust_value_image = pygame.image.load("images/game/trust_image/-0.png")
        self.trust_value_rect = self.trust_value_image.get_rect(center=(180, 15))
        self.check_flag = False
        self.time = 0

        self.idea_disappear_speed = 256 + variable.CP * 10
        # 設定數值上限
        if self.idea_disappear_speed > 300:
            self.idea_disappear_speed = 300
        self.answer_appear_frequency = random.randint(1, max(4, 10 - variable.CP))

        self.trust_init_value = 4 + variable.SA
        self.trust_decrease_value = 0
        self.answer_frequency_flag = 0

    # 事件UI初始化
    def event_UI_init(self):
        self.screen.fill(self.line_color)
        self.screen.blit(self.conversation_record_image, self.conversation_record_rect)
        self.screen.blit(self.phone_screen, self.phone_screen_rect)
        self.screen.blit(self.text_box, self.text_box_rect)

    # 取得可能出現詞條list
    def get_word_list(self):
        if self.word_type[self.now_question_num] == 'noun':
            self.word_list = vocabulary.get_noun()
        if self.word_type[self.now_question_num] == 'verb':
            self.word_list = vocabulary.get_verb()
        if self.word_type[self.now_question_num] == 'people':
            self.word_list = vocabulary.get_people()
        if self.answer_word[self.now_question_num] not in self.word_list:
            self.word_list.append(self.answer_word[self.now_question_num])

    # 遊戲UI初始化
    def game_UI_init(self):
        self.screen.fill(self.line_color)
        self.screen.blit(self.conversation_record_image, self.conversation_record_rect)
        self.screen.blit(self.phone_screen, self.phone_screen_rect)
        self.screen.blit(self.text_box, self.text_box_rect)
        self.screen.blit(self.trust_value_image, self.trust_value_rect)

    # 改變地鼠位置與更換詞條
    def change_idea_pos(self):
        idea_x = random.randint(150, 400)
        idea_y = random.randint(100, 400)
        self.idea_rect.center = (idea_x, idea_y)

        # 如果錯過正確答案會使信賴降低
        if self.now_word == self.answer_word[self.now_question_num]:
            self.trust_decrease_value += 1
            if self.trust_decrease_value <= 4:
                self.trust_value_image = \
                    pygame.image.load('images/game/trust_image/-' + str(self.trust_decrease_value) + '.png')
                self.trust_value_rect = self.trust_value_image.get_rect(center=(180, 15))

        # 確認正確答案在一定次數內會出現
        if self.answer_frequency_flag < self.answer_appear_frequency:
            self.now_word = random.choice(self.word_list)
            if self.now_word == self.answer_word[self.now_question_num]:
                self.answer_frequency_flag = 0
            else:
                self.answer_frequency_flag += 1
        else:
            self.now_word = self.answer_word[self.now_question_num]
            self.answer_frequency_flag = 0
            self.answer_appear_frequency = random.randint(1, max(4, 10 - variable.CP))
        # 更換詞條
        gameText.text = self.now_word
        gameText.x_y = (idea_x, idea_y)
        gameText.new_sentence()

    # 前往下個問題
    def next_question(self):
        self.check_flag = False
        self.game_flag = False

        # 判斷是否到了結尾
        if self.now_line <= self.event_line_num:
            # 判斷是否為第一行決定對話紀錄所需圖片
            if self.now_line != 0:
                self.conversation_record_image = pygame.image.load(self.image_path + str(self.now_line - 1) + '.png')
                self.conversation_record_rect = self.conversation_record_image.get_rect(center=(630, 230))
            else:
                self.conversation_record_image = pygame.image.load('images/game/conversation_record/none.png')
                self.conversation_record_rect = self.conversation_record_image.get_rect(center=(630, 230))

            # 判斷現在是否需要進入遊戲
            if self.now_line in self.question_line:
                self.game_UI_init()
                # 填上問題句子
                workText.text = self.text[self.now_question_num]
                workText.x_y = (400, 500)
                workText.new_sentence()
                FUNCS.update()
                FUNCS.delay(300)

                # 使句子逐漸浮現達到提醒與轉場的效果
                for alpha in range(0, 256, 5):
                    self.game_UI_init()
                    self.screen.blit(self.text_box, self.text_box_rect)
                    workText.text_alpha = alpha
                    workText.draw()
                    FUNCS.update()
                    FUNCS.delay(1)

                self.game_init()
                self.game_flag = True
                FUNCS.delay(50)
            else:
                self.event_UI_init()
                FUNCS.update()
                if self.now_line == 0:
                    FUNCS.delay(1000)
                else:
                    FUNCS.delay(3000)
                self.now_line += 1
                self.next_question()
        else:
            self.game_over()

    # 初始化遊戲
    def game_init(self):
        self.word_list = []
        self.get_word_list()
        self.answer_appear_frequency = random.randint(1, max(4, 10 - variable.CP))
        self.change_idea_pos()
        self.time = 0

    # 主遊戲進行
    def game_running(self):
        self.game_UI_init()
        if self.time < self.idea_disappear_speed:
            self.time += 2.5
        else:
            self.time = 0
            self.change_idea_pos()

        if self.time <= 255:
            self.idea_alpha = self.time
        else:
            self.idea_alpha = 255
        self.idea.set_alpha(self.idea_alpha)

        self.screen.blit(self.idea, self.idea_rect)
        gameText.draw()
        workText.draw()

    # 確認是否點擊在圖片上 與答案是否正確
    def check(self, event):
        if self.check_flag:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.idea_rect.collidepoint(event.pos):
                    if self.now_word == self.answer_word[self.now_question_num]:
                        if self.now_question_num % 2 == 0:
                            self.now_question_num += 1
                            self.next_question()
                            FUNCS.delay(100)
                        else:
                            self.now_question_num += 1
                            self.now_line += 1
                            self.next_question()
                    else:
                        self.game_flag = False
                        self.event_fail()
        # 吃掉轉場時誤觸
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_flag = True

    # 事件失敗
    def event_fail(self):
        variable.catch += 20
        image = pygame.image.load(room_path).convert_alpha()
        transition.ready(image)
        transition.hacker()
        self.screen.blit(self.text_box, self.text_box_rect)
        workText.x_y = (400, 500)
        workText.text = '因為你傳了意義不明的句子過去，對方沒有回覆你，你不只沒騙到錢還十分可疑，被捕率上升了'
        workText.new_sentence()
        workText.draw()
        FUNCS.update()
        FUNCS.delay(2000)
        room.back()

    # 事件結算
    def game_over(self):
        if self.trust_decrease_value == 0:
            reward = 500 + self.trust_init_value * 25
            variable.money += reward
            variable.SA += 2
            image = pygame.image.load(room_path).convert_alpha()
            transition.ready(image)
            transition.hacker()
            self.screen.blit(self.text_box, self.text_box_rect)
            workText.x_y = (400, 500)
            workText.text = '你成功賺到了' + str(reward) + '元，這次的經驗使你的技巧提升了'
            workText.new_sentence()
            workText.draw()
            FUNCS.update()
            FUNCS.delay(2000)
            room.back()
        elif self.trust_decrease_value <= 3:
            reward = 500 + self.trust_init_value * 15
            variable.money += reward
            image = pygame.image.load(room_path).convert_alpha()
            transition.ready(image)
            transition.hacker()
            self.screen.blit(self.text_box, self.text_box_rect)
            workText.x_y = (400, 500)
            workText.text = '對方似乎對你有些懷疑，但你還是賺到了' + str(reward) + '元'
            workText.new_sentence()
            workText.draw()
            FUNCS.update()
            FUNCS.delay(2000)
            room.back()
        else:
            variable.catch += self.trust_decrease_value * 5
            image = pygame.image.load(room_path).convert_alpha()
            transition.ready(image)
            transition.hacker()
            self.screen.blit(self.text_box, self.text_box_rect)
            workText.x_y = (400, 500)
            workText.text = '雖然你沒傳出奇怪的句子能十分可疑，不只沒賺到錢被捕率還提升了'
            workText.new_sentence()
            workText.draw()
            FUNCS.update()
            FUNCS.delay(2000)
            room.back()


work = MainGame(SCREEN)  # 把work宣告為這個class

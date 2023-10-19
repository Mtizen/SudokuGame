import pygame
import pygame.mixer
import json
import os
from model import SudokuModel
from model import format_time

#Tạo giao diện
width, height = 500, 889
board_size = width - (width * 5/100)
cube_size = board_size / 9
x_board = width * 5/200
y_board = height * 26.71875/100


class Image:
    def __init__(self):
        ### Tải hình ảnh nền và các icon
        self.background = pygame.image.load(r'image\screen\background.png')
        self.sudoku1 = pygame.image.load(r'image\text\sudoku1.png')
        self.plane = pygame.image.load(r'image\icon\plane.png')
        self.setting = pygame.image.load(r'image\icon\setting.png')
        self.credit = pygame.image.load(r'image\text\credit.png')
        self.play = pygame.image.load(r'image\text\play.png')
        self.return_game = pygame.image.load(r'image\text\return_game.png')
        self.stats = pygame.image.load(r'image\text\stats.png')
        self.on = pygame.image.load(r'image\icon\on.png')
        self.off = pygame.image.load(r'image\icon\off.png')

        self.page1 = pygame.image.load(r'image\screen\page1.png')
        self.page2 = pygame.image.load(r'image\screen\page2.png')
        self.page3 = pygame.image.load(r'image\screen\page3.png')
        self.page4 = pygame.image.load(r'image\screen\page4.png')
        self.page5 = pygame.image.load(r'image\screen\page5.png')
        self.easy_stats = pygame.image.load(r'image\screen\easy_stats.png')
        self.medium_stats = pygame.image.load(r'image\screen\medium_stats.png')
        self.hard_stats = pygame.image.load(r'image\screen\hard_stats.png')

        self.diff_screen = pygame.image.load(r'image\screen\difficult.png')
        self.sudoku2 = pygame.image.load(r'image\text\sudoku2.png')
        self.back_icon = pygame.image.load(r'image\icon\back.png')
        self.pause = pygame.image.load(r'image\screen\pause1.png')
        self.pause_icon = pygame.image.load(r'image\icon\pause_icon.png')
        self.hint = pygame.image.load(r'image\icon\hint.png')
        self.congrat = pygame.image.load(r'image\icon\congrat.png')
        self.heheboi = pygame.image.load(r'image\icon\heheboi.png')
        self.return_home = pygame.image.load(r'image\text\return_home.png')

        self.black = pygame.image.load(r'image\screen\black.png')
        self.black = self.black.convert()
        self.black.set_alpha(128)
        self.white1 = pygame.image.load(r'image\screen\setting.png')
        self.white = pygame.image.load(r'image\screen\white.png')
 

class Sound:
    global mode1, mode2
    def __init__(self, sound_settings):
        pygame.mixer.init()  # Khởi tạo hệ thống âm thanh cho game
        self.soundtrack = pygame.mixer.Sound('sound\soundtrack.mp3')
        self.soundtrack.set_volume(0.3)  # Thiết lập âm lượng với 0.3 là mức âm lượng (từ 0.0 đến 1.0)
        self.click_effect = pygame.mixer.Sound(r'sound\button1.mp3')

        # Tải trạng thái âm thanh từ tệp JSON
        self.sound_settings = sound_settings
        self.sound_enable = sound_settings.get("sound_enabled", True)
        self.effect_enable = sound_settings.get("effect_enabled", True)
        if self.sound_enable == True:
            self.soundtrack.play(-1)  # Phát âm thanh (Tùy chọn -1 để lặp lại âm thanh)


    def toggle_sound(self):
        if self.sound_enable:
            self.soundtrack.stop()  # Tắt âm thanh
            self.sound_enable = False
        else:
            self.soundtrack.play(-1)
            self.sound_enable = True

    
    def toggle_effect(self):
        if self.effect_enable:
            self.effect_enable = False
        else:
            self.effect_enable = True    

    def button_play(self):            
        self.click_effect.play()

class SudokuView:
    def __init__(self, sound_settings):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 889))
        pygame.display.set_caption('Sudoku')
        self.icon = pygame.image.load(r'image\icon\logo.png')
        pygame.display.set_icon(self.icon)
        self.image = Image()
        self.sound = Sound(sound_settings)
        self.board = SudokuModel(9, 9, board_size, board_size, self.screen)
        self.game_mode = None 
        self.stats_mode = "Dễ"
        self.guide_mode = "Trang1"


    # Hiển thị giao diện cho trạng thái "Menu chính"
    def home_display(self, is_ending, secs):
        self.screen.blit(self.image.background,(0,0))
        self.screen.blit(self.image.plane,(width - self.image.plane.get_width()-18, 24.5))
        self.screen.blit(self.image.sudoku1,(width/2 - self.image.sudoku1.get_width()/2, 145))
        self.screen.blit(self.image.setting,(20, 22))
        self.screen.blit(self.image.credit,(5, height - self.image.credit.get_height() - 5))
        self.screen.blit(self.image.play,(width/2 - self.image.play.get_width()/2, 575))
        self.screen.blit(self.image.stats,(width/2 - self.image.stats.get_width()/2, 695))
        
        if is_ending == False:
            self.screen.blit(self.image.return_game,(width/2 - self.image.play.get_width()/2, 455))
            font_bold = r'font\arial\arialbd.ttf'
            info_font_bold = pygame.font.Font(font_bold, 18)
            info_game = info_font_bold.render("Độ khó: " + self.game_mode + " - " + "Thời gian: " + format_time(secs), 1, (131,129,150))
            self.screen.blit(info_game, (width/2 - info_game.get_width()/2, 507))

    def are_you_sure(self, secs):
        self.screen.blit(self.image.background,(0,0))
        self.screen.blit(self.image.plane,(width - self.image.plane.get_width()-18, 24.5))
        self.screen.blit(self.image.sudoku1,(width/2 - self.image.sudoku1.get_width()/2, 145))
        self.screen.blit(self.image.setting,(20, 22))
        self.screen.blit(self.image.credit,(5, height - self.image.credit.get_height() - 5))
        self.screen.blit(self.image.play,(width/2 - self.image.play.get_width()/2, 575))
        self.screen.blit(self.image.stats,(width/2 - self.image.stats.get_width()/2, 695))
        self.screen.blit(self.image.return_game,(width/2 - self.image.play.get_width()/2, 455))
        font_bold = r'font\arial\arialbd.ttf'
        info_font_bold = pygame.font.Font(font_bold, 18)
        info_game = info_font_bold.render("Độ khó: " + self.game_mode + " - " + "Thời gian: " + format_time(secs), 1, (131,129,150))
        self.screen.blit(info_game, (width/2 - info_game.get_width()/2, 507))
        self.screen.blit(self.image.black, (0,0))
        self.screen.blit(self.image.pause, (0,0))

    def setting_display(self):
        self.screen.blit(self.image.white1,(0,0))
        if self.sound.sound_enable == True: 
            self.screen.blit(self.image.on,(400,72))
        else:
            self.screen.blit(self.image.off,(400,72))

        if self.sound.effect_enable == True: 
            self.screen.blit(self.image.on,(400,140))
        else:
            self.screen.blit(self.image.off,(400,140))

    def guide_display(self):
        self.screen.blit(self.image.page1,(0,0)) if self.guide_mode == "Trang1" else None
        self.screen.blit(self.image.page2,(0,0)) if self.guide_mode == "Trang2" else None
        self.screen.blit(self.image.page3,(0,0)) if self.guide_mode == "Trang3" else None
        self.screen.blit(self.image.page4,(0,0)) if self.guide_mode == "Trang4" else None
        self.screen.blit(self.image.page5,(0,0)) if self.guide_mode == "Trang5" else None

    # Hiển thị giao diện cho trạng thái "Chọn độ khó"
    def difficulty_display(self):
        self.screen.blit(self.image.diff_screen,(0,0))
        self.screen.blit(self.image.sudoku1,(width/2 - self.image.sudoku1.get_width()/2, 145))
        self.screen.blit(self.image.back_icon, (20, 22))

    def statistics_display(self):
        # Hiển thị giao diện cho trạng thái "Thống kê"
        game_stats = {}
        game_stats = self.load_game_stats()
        play_count = 0 
        no_mistake = 0
        win_rate = 0 
        current_streak = 0 
        best_streak = 0
        best_time_min = "--:--"
        average_time = "--:--"
        if game_stats is not None and self.stats_mode in game_stats:
            play_count = game_stats[self.stats_mode]["play_count"]
            no_mistake = game_stats[self.stats_mode]["no_mistake"]
            win_rate = game_stats[self.stats_mode]["win_rate"]
            best_time_min = game_stats[self.stats_mode]["best_time_minute"]
            average_time = game_stats[self.stats_mode]["average_time"]
            current_streak = game_stats[self.stats_mode]["current_streak"]
            best_streak = game_stats[self.stats_mode]["best_streak"]

        # Hiển thị giao diện thống kê ở đây khi cần
        self.screen.blit(self.image.easy_stats, (0,0)) if self.stats_mode == "Dễ" else None
        self.screen.blit(self.image.medium_stats, (0,0)) if self.stats_mode == "Trung bình" else None
        self.screen.blit(self.image.hard_stats, (0,0)) if self.stats_mode == "Khó" else None

        font_bold = r'font\arial\arialbd.ttf'
        stats_font_bold = pygame.font.Font(font_bold, 20)

        # Hiển thị dữ liệu thống kê
        text = stats_font_bold.render(f"{play_count}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 210))
        text = stats_font_bold.render(f"{no_mistake}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 280))
        text = stats_font_bold.render(f"{win_rate}%", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 350))
        text = stats_font_bold.render(f"{best_time_min}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 490))
        text = stats_font_bold.render(f"{average_time}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 560))
        text = stats_font_bold.render(f"{current_streak}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 710))
        text = stats_font_bold.render(f"{best_streak}", True, (0, 0, 0))
        self.screen.blit(text, (width - text.get_width()-55, 780))

    def game_display(self, secs, strikes, state):
        # In nền và bảng
        self.screen.blit(self.image.background, (0,0))
        self.board.draw_board()

        # Cài đặt phông chữ
        font_light = r'font\roboto\RobotoCondensed-Regular.ttf'
        font_bold = r'font\roboto\RobotoCondensed-BoldItalic.ttf'
        font_x = r'font\comic_sans\comic.ttf'
        font_talk = r'font\roboto\RobotoCondensed-Italic.ttf'
        game_font_light = pygame.font.Font(font_light, 23)
        game_font_bold = pygame.font.Font(font_bold, 24)
        game_font_x = pygame.font.Font(font_x, 60)
        game_font_talk = pygame.font.Font(font_talk, 18)
        time_text = game_font_light.render("Thời gian", 1, (0,0,0))
        time_count = game_font_bold.render(format_time(secs), 1, (0,0,0))        
        wrong_text = game_font_light.render("Số lỗi", 1, (0,0,0))
        wrong_strikes = game_font_bold.render(str(strikes) + "/3", 1, (144, 144, 159))
        wrong_x = game_font_x.render("X " * strikes, 1, (255, 0, 0))
        wrong_talk = game_font_talk.render("Bắt đầu game đi!", 1, (0,0,0))
        difficult_text = game_font_light.render("Độ khó", 1, (0,0,0))
        if self.game_mode == "Dễ":
            difficult_type = game_font_bold.render(self.game_mode, 1, (0,225,0))
        elif self.game_mode == "Trung bình":
            difficult_type = game_font_bold.render(self.game_mode, 1, (255,225,0))
        elif self.game_mode == "Khó":
            difficult_type = game_font_bold.render(self.game_mode, 1, (255,0,0))        

        # In hình hiển thị
        self.screen.blit(self.image.pause_icon, (width *70/100, height * 20.7/100))
        self.screen.blit(self.image.back_icon, (20, 22))
        self.screen.blit(self.image.setting,(width - self.image.setting.get_width()-19, 20))
        self.screen.blit(self.image.hint,(380, 760))

        # Vẽ hình chữ nhật to 
        pygame.draw.rect(self.screen, (0,0,0), (40, 768, 187, 72))
        # Vẽ hình chữ nhật con bên trong để tạo viền rỗng
        pygame.draw.rect(self.screen, (255, 255, 255), (40 + 3, 768 + 3, 187 - 2 * 3, 72 - 2 * 3))
        #if strikes == 1:

        # In ra văn bản
        self.screen.blit(self.image.sudoku2, (width *26/100, height * 10/100))
        self.screen.blit(time_text, (width *80.8/100, height * 20/100))
        self.screen.blit(time_count, (width *87.1/100, height * 23/100))
        self.screen.blit(wrong_text, (width *34/100, height * 20/100))
        self.screen.blit(wrong_strikes, (width *36/100, height * 23/100))
        self.screen.blit(wrong_x, (50, 760))
        self.screen.blit(wrong_talk, (40, 745))
        self.screen.blit(difficult_text, (width *2.5/100, height * 20/100))
        self.screen.blit(difficult_type, (width *2.5/100, height * 23/100))        

        if state == "Tạm dừng":
            self.screen.blit(self.image.black, (0,0))
            self.screen.blit(self.image.pause, (0,0))

        if state == "Hoàn thành":
            # Cài đặt phông chữ
            font_light = r'font\roboto\RobotoCondensed-Regular.ttf'
            font_bold = r'font\roboto\RobotoCondensed-Bold.ttf'
            end_font_light = pygame.font.Font(font_light, 34)
            end_font_bold = pygame.font.Font(font_bold, 34)

            # Thiết lập phông chữ cho lời chúc mừng
            congrat_text1 = end_font_bold.render("Chúc mừng bạn đã", 1, (0,0,0))
            congrat_text2 = end_font_bold.render("hoàn thành màn chơi", 1, (0,0,0))
            congrat_text3 = end_font_bold.render("Chúc mừng bạn đã", 1, (0,0,0))
            congrat_text4 = end_font_bold.render("unlock skill mới :v", 1, (0,0,0))
            # Thiết lập phông chữ cho thời gian
            time_text = end_font_light.render("Thời gian", 1, (0,0,0))
            time_count = end_font_bold.render(format_time(secs), 1, (0,0,0))
            # Thiết lập phông chữ cho lỗi sai
            wrong_text = end_font_light.render("Số lỗi", 1, (0,0,0))
            wrong_strikes = end_font_bold.render("0" + str(strikes) if strikes < 10 else None, 1, (144, 144, 159))
            # Thiết lập phông chữ cho độ khó
            difficult_text = end_font_light.render("Cấp độ", 1, (0,0,0))
            if self.game_mode == "Dễ":
                difficult_type = end_font_bold.render(self.game_mode, 1, (0,225,0))
            elif self.game_mode == "Trung bình":
                difficult_type = end_font_bold.render(self.game_mode, 1, (255,225,0))
            elif self.game_mode == "Khó":
                difficult_type = end_font_bold.render(self.game_mode, 1, (255,0,0))

            # In hình hiển thị  
            self.screen.blit(self.image.black, (0,0))
            self.screen.blit(self.image.white, (42.5,220))
            self.screen.blit(self.image.return_home, (75,610))
            # In lời chúc mừng
            if strikes != 3:
                self.screen.blit(congrat_text1, (width/2 - congrat_text1.get_width()/2,245))
                self.screen.blit(congrat_text2, (width/2 - congrat_text2.get_width()/2,293))  
                self.screen.blit(self.image.congrat, (width/2 - self.image.congrat.get_width()/2,355))
            else:
                self.screen.blit(congrat_text3, (width/2 - congrat_text3.get_width()/2,245))
                self.screen.blit(congrat_text4, (width/2 - congrat_text4.get_width()/2,293))
                self.screen.blit(self.image.heheboi,(width/2 - self.image.heheboi.get_width()/2,350))      
            # In thời gian
            self.screen.blit(time_text, (width/2 - time_text.get_width()/2,495))
            self.screen.blit(time_count, (width/2 - time_count.get_width()/2,540))
            #In lỗi sai
            self.screen.blit(wrong_text, (335,385))
            self.screen.blit(wrong_strikes, (355,430))
            #In độ khó
            self.screen.blit(difficult_text, (78,385)) 
            if self.game_mode == "Dễ":
                self.screen.blit(difficult_type, (113,430))
            elif self.game_mode == "Trung bình":
                self.screen.blit(difficult_type, (54,430))
            elif self.game_mode == "Khó":
                self.screen.blit(difficult_type, (104,430)) 


    def load_game_stats(self):
        try:
            with open(r'data\sudoku_stats.json', "r") as file:
                stats = json.load(file)
                return stats
        except FileNotFoundError:
            # Xử lý trường hợp file không tồn tại
            return None    
        

    def set_game_mode(self, new_state):
        self.game_mode = new_state



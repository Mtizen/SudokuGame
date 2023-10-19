import pygame
import webbrowser
from model import SudokuModel
from model import SudokuSolver
from view import SudokuView
from model import update_stats
from model import load_sound_state, update_enabled
from model import load_sudoku_list, choose_random_puzzle, delete_sudoku

#Tạo giao diện
width, height = 500, 889
board_size = width - (width * 5/100)
cube_size = board_size / 9
x_board = width * 5/200
y_board = height * 26.71875/100


### Tạo các vùng tương tác (Các vùng hình chữ nhật)
''' Giao diện home '''
class Button:
    def __init__(self):
        self.play_button = pygame.Rect(30, 575, 445, 79)
        self.statistics_button = pygame.Rect(30, 695, 445, 79)
        self.feedback_button = pygame.Rect(425, 15, 53, 49)
        self.return_button = pygame.Rect(30, 455, 445, 79)
        self.pause_button = pygame.Rect(width *70/100, height * 20.7/100, 42, 42)
        self.quit_button = pygame.Rect(80, 565, 335, 65)
        self.hint_button = pygame.Rect(380, 760, 50, 83)
        self.continue_button = pygame.Rect(80, 640, 335, 65)
        self.home_button = pygame.Rect(80, 607, 335, 80)

        ''' Giao diện difficult '''
        self.setting1_button = pygame.Rect(20, 22, 60, 60)
        self.setting2_button = pygame.Rect(425, 20, 60, 60)
        self.soundtrack = pygame.Rect(400, 72, 82, 34)
        self.effect = pygame.Rect(400, 140, 82, 34)

        self.guide = pygame.Rect(0,190,500,66)
        self.previous = pygame.Rect(40,802,60,60)
        self.next = pygame.Rect(399,802,60,60)
        
        self.back_button = pygame.Rect(12, 15, 40, 60)
        self.easy_level = pygame.Rect(30, 500, 380, 70)
        self.medium_level = pygame.Rect(30, 620, 380, 70)
        self.hard_level = pygame.Rect(30, 740, 380, 70)

        self.easy_stats = pygame.Rect(40, 75, 35, 30)
        self.medium_stats = pygame.Rect(175, 75, 150, 30)
        self.hard_stats = pygame.Rect(410, 75, 50, 30)


class SudokuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.button = Button()
        self.current_state = "Menu chính"  # Trạng thái hiện tại của game
        self.previous_state = None
        self.is_ending = True
        self.is_paused = False
        self.file_name = None
        self.clicked = None
        self.key = None
        self.strikes = 0
        self.start_ticks = 0
        self.elapsed_time = 0
        self.total_seconds = 0

    def running(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == pygame.KEYDOWN:
                    if self.clicked != None:
                        self.handle_keyboard_press(event)
                    elif event.key == pygame.K_TAB:
                        self.is_paused = True
                        self.view.board.solve_gui()     
            if self.view.board.is_finished() or self.strikes == 3: 
                self.end_game() 

            self.sketch_temp() if self.key != None else None
            self.total_time()
            self.display_state()

            pygame.display.update()  


    def handle_mouse_click(self, event):
        if self.current_state == "Menu chính":
            self.handle_home_screen_click(event)
        elif self.current_state == "Cài đặt":
            self.handle_setting_screen_click(event)
        elif self.current_state == "Hướng dẫn":
            self.handle_guide_screen_click(event)       
        elif self.current_state == "Chọn độ khó":
            self.handle_difficulty_screen_click(event)
        elif self.current_state == "Trò chơi":
            self.handle_game_screen_click(event)
        elif self.current_state == "Mày chắc chứ":
            self.handle_aus_screen_click(event) 
        elif self.current_state == "Tạm dừng":
            self.handle_pause_screen_click(event)    
        elif self.current_state == "Hoàn thành":
            self.handle_finish_screen_click(event)  
        elif self.current_state == "Thống kê":
            self.handle_statistics_screen_click(event)
    
    def handle_keyboard_press(self, event):
        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
            self.key = 1
        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
            self.key = 2
        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
            self.key = 3
        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
            self.key = 4    
        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
            self.key = 5
        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
            self.key = 6
        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
            self.key = 7
        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
            self.key = 8
        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
            self.key = 9

        elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_0 or event.key == pygame.K_KP0:
            self.view.board.clear()

        elif event.key == pygame.K_TAB:
            self.is_paused = True
            self.view.board.solve_gui()

        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            row, col = self.view.board.cube_selected
            # Kiểm tra giá trị đã nhập vào ô
            if self.view.board.cubes[row][col].temp_value != 0:
                if self.view.board.check(self.view.board.cubes[row][col].temp_value) == False:
                    self.strikes += 1


    # Xử lý các sự kiện click trong màn hình chính
    def handle_home_screen_click(self, event):
        if self.button.play_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            if self.is_ending == False:
                self.current_state = "Mày chắc chứ"
            else:    
                self.current_state = "Chọn độ khó"
        elif self.button.statistics_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None  
            self.current_state = "Thống kê"
        elif self.button.setting1_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None  
            self.previous_state = self.current_state
            self.current_state = "Cài đặt"
        elif self.button.feedback_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            webbrowser.open('https://forms.gle/YTGfz9WEZMrnKYoUA')

        if self.is_ending == False:
            if self.button.return_button.collidepoint(event.pos):
                self.current_state = "Trò chơi"
                self.is_paused = False
                self.start_ticks = pygame.time.get_ticks()

    def handle_setting_screen_click(self, event):
        global sound_settings
        if self.button.back_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            if self.previous_state == "Menu chính":
                self.current_state = "Menu chính"
            elif self.previous_state == "Trò chơi":
                self.current_state = "Trò chơi" 
                self.is_paused = False
                self.start_ticks = pygame.time.get_ticks()    
        elif self.button.soundtrack.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None  
            update_enabled("sound_enabled")
            self.view.sound.toggle_sound()
        elif self.button.effect.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == False else None        
            update_enabled("effect_enabled")
            self.view.sound.toggle_effect()
            print(self.view.sound.sound_settings)
        elif self.button.guide.collidepoint(event.pos): 
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Hướng dẫn"  

    def handle_guide_screen_click(self, event):
        if self.button.back_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            if self.previous_state == "Menu chính":
                self.current_state = "Menu chính"
            elif self.previous_state == "Trò chơi":
                self.current_state = "Trò chơi" 
                self.is_paused = False
                self.start_ticks = pygame.time.get_ticks()
            self.view.guide_mode = "Trang1"  
        elif self.button.next.collidepoint(event.pos) and self.view.guide_mode != "Trang5":
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            if self.view.guide_mode == "Trang1":
                self.view.guide_mode = "Trang2" 
            elif self.view.guide_mode == "Trang2":
                self.view.guide_mode = "Trang3" 
            elif self.view.guide_mode == "Trang3":
                self.view.guide_mode = "Trang4" 
            elif self.view.guide_mode == "Trang4":
                self.view.guide_mode = "Trang5"                     
        elif self.button.previous.collidepoint(event.pos) and self.view.guide_mode != "Trang1":
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            if self.view.guide_mode == "Trang2":
                self.view.guide_mode = "Trang1" 
            elif self.view.guide_mode == "Trang3":
                self.view.guide_mode = "Trang2" 
            elif self.view.guide_mode == "Trang4":
                self.view.guide_mode = "Trang3" 
            elif self.view.guide_mode == "Trang5":
                self.view.guide_mode = "Trang4"
                  
    def handle_difficulty_screen_click(self, event):
        if self.button.easy_level.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.view.set_game_mode("Dễ")
            self.file_name = r"data\file_easy.json"
            self.current_state = "Trò chơi"
        elif self.button.medium_level.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.view.set_game_mode("Trung bình")
            self.file_name = r"data\file_medium.json"
            self.current_state = "Trò chơi"
        elif self.button.hard_level.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.view.set_game_mode("Khó")
            self.file_name = r"data\file_hard.json"
            self.current_state = "Trò chơi"
        elif self.button.back_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Menu chính"
            
        if self.current_state == "Trò chơi":
            global stt
            #self.model.generate_sudoku(self.view.game_mode)
            board = self.choose_file()
            if "Sudoku" in board:
                SudokuModel.board = board["Sudoku"]
                stt = board["STT"]
            self.view.board = SudokuModel(9, 9, board_size, board_size, self.view.screen)
            self.view.board.is_started()
            self.view.board.update_model()
            self.view.board.solve()
            self.is_paused = False
            self.is_ending = False
            self.clicked = None
            self.elapsed_time = 0
            self.total_seconds = 0
            self.strikes = 0  
            self.start_ticks = pygame.time.get_ticks()

    def handle_game_screen_click(self, event):
        if self.button.back_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.is_paused = True
            self.elapsed_time += pygame.time.get_ticks() - self.start_ticks
            self.previous_state = self.current_state
            self.current_state = "Menu chính"
        elif self.button.setting2_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.is_paused = True
            self.elapsed_time += pygame.time.get_ticks() - self.start_ticks
            self.previous_state = self.current_state
            self.current_state = "Cài đặt"       
        elif self.button.pause_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Tạm dừng"
            self.is_paused = True
            self.elapsed_time += pygame.time.get_ticks() - self.start_ticks
        elif self.button.hint_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None 
            self.view.board.hint()

        
        else:
            pos = pygame.mouse.get_pos()              #Lấy tọa độ của click trên screen
            self.clicked = self.view.board.click(pos)      #Lấy vị trí hàng, cột của cube (Nếu có)
            if self.clicked != None:
                self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.check_clicked()
                

    def handle_pause_screen_click(self, event):
        # Xử lý các sự kiện click trong màn hình tạm dừng
        if self.button.continue_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Trò chơi"
            self.is_paused = False
            self.start_ticks = pygame.time.get_ticks()
        elif self.button.quit_button.collidepoint(event.pos):    
            self.current_state = "Menu chính"
            self.previous_state = None

    def handle_finish_screen_click(self, event):
        if self.button.home_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Menu chính"

    def handle_aus_screen_click(self, event):
        if self.button.continue_button.collidepoint(event.pos):
            self.view.sound.button_play() if self.view.sound.effect_enable == True else None
            self.current_state = "Trò chơi"
            self.is_paused = False
            self.start_ticks = pygame.time.get_ticks()
        elif self.button.quit_button.collidepoint(event.pos):    
            self.current_state = "Chọn độ khó"
            self.is_ending = True
            self.previous_state = None

    def handle_statistics_screen_click(self, event):
        if self.button.back_button.collidepoint(event.pos):
            self.current_state = "Menu chính"
        elif self.button.easy_stats.collidepoint(event.pos):
            self.view.stats_mode = "Dễ"    
        elif self.button.medium_stats.collidepoint(event.pos):
            self.view.stats_mode = "Trung bình" 
        elif self.button.hard_stats.collidepoint(event.pos):     
            self.view.stats_mode = "Khó"

    def choose_file(self):
        file_name = self.file_name
        file_puzzles = load_sudoku_list(file_name)
        if not file_puzzles:
            print("Không có dữ liệu Sudoku.")
            return {}  # Hoặc trả về giá trị mặc định khác
        else:
            puzzle = choose_random_puzzle(file_puzzles)
            return puzzle

    def check_clicked(self):
        if self.clicked != None:    
            row, col = self.clicked
        if self.clicked != None and self.view.board.cubes[row][col].main_value != 0:
            self.view.board.select(row, col)
            self.key = None     #Cho key = 0 TH người dùng chưa chọn ô trống nào mà đã bấm số 
        elif self.clicked != None and self.view.board.cubes[row][col].main_value == 0:
            self.view.board.select(row, col)

    def sketch_temp(self):
        if self.view.board.cube_selected:
            self.view.board.sketch(self.key)
            self.key = None

    def total_time(self):
        if self.is_paused == False:
            self.total_seconds = (pygame.time.get_ticks() - self.start_ticks + self.elapsed_time) // 1000

    def end_game(self):
        if self.current_state == "Trò chơi":
            self.is_paused = True
            self.is_ending = True
            self.previous_state = None
            if self.strikes == 3:
                update_stats(self.view.game_mode, 0, self.strikes)
            else:
                update_stats(self.view.game_mode, self.total_seconds, self.strikes)
                delete_sudoku(self.file_name, stt)  

            self.current_state = "Hoàn thành"


    def display_state(self):
        if self.current_state == "Menu chính":
            self.view.home_display(self.is_ending, self.total_seconds)
        elif self.current_state == "Cài đặt":
            self.view.setting_display()
        elif self.current_state == "Hướng dẫn":
            self.view.guide_display()    
        elif self.current_state == "Chọn độ khó":
            self.view.difficulty_display()
        elif self.current_state == "Trò chơi":
            self.view.game_display(self.total_seconds, self.strikes, self.current_state)
        elif self.current_state == "Mày chắc chứ":
             self.view.are_you_sure(self.total_seconds)   
        elif self.current_state == "Thống kê":
            self.view.statistics_display()
        elif self.current_state == "Tạm dừng":
            self.view.game_display(self.total_seconds, self.strikes, self.current_state)
        elif self.current_state == "Hoàn thành":
            self.view.game_display(self.total_seconds, self.strikes, self.current_state)



if __name__ == "__main__":
    # Khởi tạo model, view và controller
    sound_settings = load_sound_state()
    view = SudokuView(sound_settings)
    model = SudokuSolver()
    controller = SudokuController(model, view)

    # Chạy trò chơi
    controller.running()        
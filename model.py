import random
import json
import os
import pygame

#Tạo giao diện
width, height = 500, 889
board_size = width - (width * 5/100)
cube_size = board_size / 9
x_board = width * 5/200
y_board = height * 26.71875/100

###
class SudokuModel:
    global width, height
    
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    
    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None    #Lưu các bản sao của bảng giá trị sudoku mỗi khi có sự thay đổi
        self.update_model()
        self.cube_selected = None    #Kiểu dữ liệu Tuple
        self.screen = screen

    ## Cập nhật giá trị mới cho bảng giá trị sudoku
    def update_model(self):
        self.model = [[self.cubes[i][j].main_value for j in range(self.cols)] for i in range(self.rows)]

    ## Vẽ bảng
    def draw_board(self):
        #Vẽ nền bảng
        rect_color = (255, 255, 255)
        rect = pygame.Rect(x_board, y_board, board_size, board_size)
        pygame.draw.rect(self.screen, rect_color, rect)
        
        #Vẽ các đường kẻ
        for i in range(0,10,1):    #Đường nhạt
            if (i % 3 == 0):
                continue
            #Nét thẳng
            pygame.draw.line(self.screen, (145, 148, 158), (x_board + cube_size*i, y_board), (x_board + cube_size*i, y_board + cube_size*9), 1)
            #Nét ngang
            pygame.draw.line(self.screen, (145, 148, 158), (x_board, y_board + cube_size*i), (x_board + cube_size*9, y_board + cube_size*i), 1)
 
        for i in range(0,10,3):    #Đường đậm
            pygame.draw.line(self.screen, (0,0,0), (x_board + cube_size*i, y_board), (x_board + cube_size*i, y_board + cube_size*9), 3)
            pygame.draw.line(self.screen, (0,0,0), (x_board, y_board + cube_size*i), (x_board + cube_size*9, y_board + cube_size*i), 3)
        
        #Vẽ các khối
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].draw_cube(self.screen)

    ## Lấy tọa độ của click chuột 
    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] > x_board and pos[0] < x_board + board_size and pos[1] > y_board and pos[1] < y_board + board_size:
            cube_row = (pos[1] - y_board) // cube_size
            cube_col = (pos[0] - x_board) // cube_size

            return (int(cube_row),int(cube_col))
        else:
            return None


    ## Xác định ô được chọn
    def select(self, row, col):
        #Cho các ô còn lại về False 
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        #Chỉ lấy địa chỉ nếu ô đó chưa có main_value:
        self.cubes[row][col].selected = True
        self.cube_selected = (row, col)

    def is_started(self):
        #Cho tất cả các ô về False 
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cube_selected = None  # Đặt cube_selected về None

    ## Lưu giá trị tạm thời
    def sketch(self, value):
        row, col = self.cube_selected
        self.cubes[row][col].set_temp(value)


    ## Kiểm tra và cài đặt các giá trị main, temp
    def check(self, value):
        row, col = self.cube_selected
        if self.cubes[row][col].main_value == 0:
            self.cubes[row][col].set_main(value)
            self.update_model()

            if valid(self.model, value, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set_main(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    ## Thuật toán quay lui kiểm tra số đã nhập
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    ## Xóa số nháp
    def clear(self):
        if self.cube_selected is not None:
            row, col = self.cube_selected
            if self.cubes[row][col].temp_value != 0:
                self.cubes[row][col].set_temp(0)
    
    ## Kiểm tra game kết thúc
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].main_value == 0:
                    return False
                        
        return True
    
    def hint(self):
        if self.cube_selected is not None:
            row, col = self.cube_selected
            if self.cubes[row][col].temp_value == 0:
                x = self.model[row][col]
                self.cubes[row][col].set_temp(x)

    ## Giải tự động
    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set_main(i)
                self.cubes[row][col].draw_change(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set_main(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.screen, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


###         
class Cube:
    global cube_size, x_board, y_board

    def __init__(self, value, row, col, width, height):
        self.main_value = value    #Biến value là giá trị được nhập vào
        self.temp_value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    #Thiết lập giá trị chính
    def set_main(self, value):
        self.main_value = value
    #Thiết lập giá trị tạm thời
    def set_temp(self, value):
        self.temp_value = value  

    def draw_cube(self, screen):
        #Tạo font cho số
        font = pygame.font.SysFont("comicsans", 40)

        x_cube = self.col * cube_size + x_board
        y_cube = self.row * cube_size + y_board

        #Nếu ô được chọn
        if self.selected:
            if self.main_value == 0:
                pygame.draw.rect(screen, (255,0,0), (x_cube+1 , y_cube+1, cube_size,cube_size), 2)
            else:
                pass

        #Nếu số ở trong ô đang ở dạng nháp (Mới chỉ thiết lập temp_value)
        if self.temp_value != 0 and self.main_value == 0:
            text = font.render(str(self.temp_value), 1, (128,128,128))
            screen.blit(text, (x_cube+5, y_cube+5))

        #Nếu số ở trong ô được điền đúng (Đã thiết lập main_value)
        elif self.main_value != 0:
            text = font.render(str(self.main_value), 1, (0, 0, 0))
            screen.blit(text, (x_cube + (cube_size/2 - text.get_width()/2), y_cube + (cube_size/2 - text.get_height()/2)))    
            
    def draw_change(self, screen, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        x_cube = self.col * cube_size + x_board
        y_cube = self.row * cube_size + y_board

        pygame.draw.rect(screen, (255, 255, 255), (x_cube+1, y_cube+1, cube_size,cube_size), 0)

        text = fnt.render(str(self.main_value), 1, (0, 0, 0))
        screen.blit(text, (x_cube + (cube_size/2 - text.get_width()/2), y_cube + (cube_size/2 - text.get_height()/2)))
        if g:
            pygame.draw.rect(screen, (0,255,0), (x_cube+1 , y_cube+1, cube_size,cube_size), 2)
        else:
            pygame.draw.rect(screen, (255,0,0), (x_cube+1 , y_cube+1, cube_size,cube_size), 2)




#Tìm vị trí của số chưa điền (Bằng 0 ở trong ma trận)    
#Hàm yêu cầu trả về
def find_empty(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)   
            
    return None    #Nếu số được kiểm tra khác 0       


def valid(board, value, pos):
    #Kiểm tra cột
    for i in range(len(board)):
        if board[i][pos[1]] == value and pos[0] != i:
            return False

    #Kiểm tra hàng
    for i in range(len(board[0])):
        if board[pos[0]][i] == value and pos[1] != i:
            return False

    #Kiểm tra các hộp 3x3
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == value and (i,j) != pos:
                return False

    return True

class SudokuSolver:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
    def generate_sudoku(self, difficulty):
        # Tạo một bảng Sudoku hợp lệ ban đầu
        self.solve()
        self.update_model()
        
        # Loại bỏ các ô để tạo độ khó
        if difficulty == "Dễ":
            num_to_remove = random.randint(40, 45)
        elif difficulty == "Trung bình":
            num_to_remove = random.randint(46, 50)
        elif difficulty == "Khó":
            num_to_remove = random.randint(51, 55)
        
        self.remove_cells(num_to_remove)
    
    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None  
    
    def valid(self, num, pos):
        row, col = pos
        # Kiểm tra hàng
        if num in self.board[row]:
            return False
        # Kiểm tra cột
        if num in [self.board[i][col] for i in range(9)]:
            return False
        # Kiểm tra trong ô 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True
    
    def update_model(self):
        self.model = [[self.board[i][j] for j in range(9)] for i in range(9)]
    
    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        row, col = find
        
        # Danh sách chứa các số từ 1 đến 9 và trộn nó
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.valid(num, (row, col)):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False
    
    def remove_cells(self, num_to_remove):
        for _ in range(num_to_remove):
            while True:
                row, col = random.randint(0, 8), random.randint(0, 8)
                if self.board[row][col] != 0:
                    self.board[row][col] = 0
                    break


# Xác định thư mục cho tệp dữ liệu
data = "data"  # Tên thư mục bạn muốn sử dụng

# Đảm bảo thư mục tồn tại hoặc tạo nếu nó chưa tồn tại
if not os.path.exists(data):
    os.makedirs(data)

# Xác định đường dẫn tới tệp dữ liệu trong thư mục
file_path = os.path.join(data, "sudoku_stats.json")

# Hàm định dạng thời gian
def format_time(secs):
    sec = int(secs % 60)
    minute = int(secs // 60)

    mm = "0" + str(minute) if minute < 10 else str(minute)
    ss = "0" + str(sec) if sec < 10 else str(sec)
    return mm + ":" + ss

# Hàm để tạo một tệp dữ liệu trống
def create_empty_stats_file():
    stats = {
        "Dễ": {"play_count": 0, "game_win": 0, "no_mistake": 0, "win_rate":0, "best_time_sec": None, "best_time_minute": "--:--", "total_time": 0.0, "average_time": "--:--", "current_streak": 0, "best_streak": 0},
        "Trung bình": {"play_count": 0, "game_win": 0, "no_mistake": 0, "win_rate":0, "best_time_sec": None, "best_time_minute": "--:--", "total_time": 0.0, "average_time": "--:--", "current_streak": 0, "best_streak": 0},
        "Khó": {"play_count": 0, "game_win": 0, "no_mistake": 0, "win_rate":0, "best_time_sec": None, "best_time_minute": "--:--", "total_time": 0.0, "average_time": "--:--", "current_streak": 0, "best_streak": 0}
    }

    with open(file_path, "w") as file:
        json.dump(stats, file)

# Hàm so sánh 2 thời gian
def compare_times(sec1, sec2):
    # So sánh thời gian
    if sec1 < sec2:
        return -1
    elif sec1 > sec2:
        return 1
    else:
        return 0
    
def compare_streak(streak1, streak2):
    if streak1 < streak2:
        return -1
    elif streak1 > streak2:
        return 1
    else:
        return 0    

# Hàm để cập nhật thông tin cho một độ khó cụ thể
def update_stats(difficulty, play_time, strikes):
    # Đọc thông tin hiện tại từ tệp
    with open(r"data\sudoku_stats.json", "r") as file:
        stats = json.load(file)

    # Tính và cập nhật average_time
    stats[difficulty]["play_count"] += 1
    if strikes != 3:
        stats[difficulty]["game_win"] += 1
        stats[difficulty]["current_streak"] += 1
    else:
        stats[difficulty]["current_streak"] = 0    
        
    if strikes == 0:
        stats[difficulty]["no_mistake"] += 1

    stats[difficulty]["total_time"] += play_time
    play_count = stats[difficulty]["play_count"]
    game_win = stats[difficulty]["game_win"]
    total_time = stats[difficulty]["total_time"]

    average_time = "--:--"
    win_rate = game_win * 100 / play_count
    win_rate = round(win_rate, 2)
    if int(win_rate * 100 % 100) == 0:
        win_rate = int(win_rate)
    elif int(win_rate * 100 % 10) == 0:
        win_rate = round(win_rate, 1)

    if game_win == 0:
        pass
    else:
        average_time = total_time // game_win
        average_time = format_time(average_time)
        best_time_minute = format_time(play_time)
    
    # Cập nhật thông tin
    if play_time != 0 and (stats[difficulty]["best_time_sec"] is None or compare_times(play_time, stats[difficulty]["best_time_sec"]) < 0):
        stats[difficulty]["best_time_sec"] = play_time
        stats[difficulty]["best_time_minute"] = best_time_minute

    if stats[difficulty]["best_streak"] == 0 or compare_streak(stats[difficulty]["current_streak"], stats[difficulty]["best_streak"]) > 0:
        stats[difficulty]["best_streak"] = stats[difficulty]["current_streak"]

    stats[difficulty]["average_time"] = average_time
    stats[difficulty]["win_rate"] = win_rate

    # Lưu thông tin cập nhật lại vào tệp
    with open(r"data\sudoku_stats.json", "w") as file:
        json.dump(stats, file)

# Kiểm tra xem tệp dữ liệu đã tồn tại chưa. Nếu chưa, tạo một tệp dữ liệu mới.
try:
    with open(file_path, "r") as file:
        pass
except FileNotFoundError:
    create_empty_stats_file()


# Xác định đường dẫn tới tệp dữ liệu trong thư mục
file_sound = os.path.join(data, "sudoku_sound.json")    

def load_sound_state():
    # Hàm để tải trạng thái âm thanh từ tệp JSON
    if os.path.exists(file_sound):
        with open(file_sound, "r") as file:
            sound_settings = json.load(file)
            return sound_settings
    else:
        # Trạng thái mặc định nếu tệp không tồn tại
        return {
            "sound_enabled": True,
            "effect_enabled": True
        }

def update_enabled(mode):
    sound_settings = load_sound_state()
    sound_settings[mode] = not sound_settings[mode]
    with open("data/sudoku_sound.json", "w") as file:
        json.dump(sound_settings, file)
        

###
file_easy = os.path.join(data, "file_easy.json") 
file_medium = os.path.join(data, "file_medium.json") 
file_hard = os.path.join(data, "file_hard.json") 
# Hàm để tải danh sách các đề Sudoku từ tệp JSON (nếu có)

def load_sudoku_list(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def choose_random_puzzle(file_puzzles):
    if file_puzzles:
        return random.choice(file_puzzles)
    else:
        return None
    
# Hàm để xóa một đề Sudoku dựa trên số thứ tự
def delete_sudoku(filename, sudoku_id):
    try:
        with open(filename, 'r') as file:
            sudoku_list = json.load(file)
    except FileNotFoundError:
        sudoku_list = []

    # Tìm và xóa bảng Sudoku cụ thể dựa trên sudoku_id
    updated_sudoku_list = [sudoku for sudoku in sudoku_list if sudoku.get("STT") != sudoku_id]

    # Ghi lại danh sách đã cập nhật vào tệp JSON
    with open(filename, 'w') as file:
        json.dump(updated_sudoku_list, file)
 
import tkinter as tk
from tkinter import messagebox
import time

# Hàm kiểm tra vị trí đặt quân hậu có an toàn không
# Kiểm tra với tất cả các hàng mà đã có quân hậu (board[i] != -1)
def is_safe(board, row, col, n):
    for i in range(n):
        if board[i] != -1 and i != row:
            # Kiểm tra cùng cột hoặc đường chéo
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
    return True

# Biến toàn cục để kiểm soát quá trình giải
stop_solver = False
pause_solver = False

# Hàm dừng hoặc tiếp tục quá trình giải
def toggle_solving():
    global stop_solver, pause_solver
    if stop_solver:
        stop_solver = False
        pause_solver = False
        start_solver()  # Bắt đầu lại quá trình giải
    else:
        pause_solver = not pause_solver  # Tạm dừng hoặc tiếp tục quá trình giải

# Hàm giải bài toán 8 quân hậu với một quân hậu cố định
def solve_n_queens(board, row, n, steps, fixed_pos):
    global stop_solver, pause_solver
    if stop_solver:
        return False  # Dừng giải nếu stop_solver là True
    if row == n:
        return True  # Đã đặt đủ 8 quân hậu
    # Nếu hàng này đã có quân (quân hậu cố định), bỏ qua đặt lại
    if row == fixed_pos[0]:
        return solve_n_queens(board, row + 1, n, steps, fixed_pos)
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            steps.append((row, col, "Đặt"))  # Ghi lại bước đặt quân hậu
            display_solution(board, n)  # Hiển thị bàn cờ
            display_steps(steps)  # Cập nhật lịch sử các bước đi
            root.update()
            time.sleep(speed_slider.get() / 1000.0)  # Chờ theo thời gian từ thanh trượt
            while pause_solver:
                root.update()
                time.sleep(0.1)  # Chờ khi tạm dừng
            if solve_n_queens(board, row + 1, n, steps, fixed_pos):
                return True
            board[row] = -1
            steps.append((row, col, "Xóa"))  # Ghi lại bước xóa quân hậu
            display_solution(board, n)  # Hiển thị bàn cờ
            display_steps(steps)  # Cập nhật lịch sử các bước đi
            root.update()
            time.sleep(speed_slider.get() / 1000.0)  # Chờ theo thời gian từ thanh trượt
            while pause_solver:
                root.update()
                time.sleep(0.1)  # Chờ khi tạm dừng
    return False

# Hàm hiển thị bàn cờ với các quân hậu đã đặt
def display_solution(board, n):
    for widget in frame.winfo_children():
        widget.destroy()  # Xóa các widget hiện tại trên bàn cờ
    
    # Thêm nhãn cột (A, B, C, …)
    for j in range(n):
        label = tk.Label(frame, text=chr(65 + j), width=4, height=2, font=("Arial", 20))
        label.grid(row=0, column=j+1)
    
    # Thêm nhãn hàng (1, 2, 3, …) và các ô bàn cờ
    for i in range(n):
        row_label = tk.Label(frame, text=str(i+1), width=4, height=2, font=("Arial", 20))
        row_label.grid(row=i+1, column=0)
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "gray"  # Màu sắc ô bàn cờ
            text = "Q" if board[i] == j else ""  # Hiển thị quân hậu nếu có
            cell = tk.Label(frame, text=text, width=4, height=2, bg=color, font=("Arial", 20))
            cell.grid(row=i+1, column=j+1)

# Hàm hiển thị bàn cờ trống
def display_empty_board(n):
    for widget in frame.winfo_children():
        widget.destroy()  # Xóa các widget hiện tại trên bàn cờ
    
    # Thêm nhãn cột
    for j in range(n):
        label = tk.Label(frame, text=chr(65 + j), width=4, height=2, font=("Arial", 20))
        label.grid(row=0, column=j+1)
    
    # Thêm nhãn hàng và các ô bàn cờ
    for i in range(n):
        row_label = tk.Label(frame, text=str(i+1), width=4, height=2, font=("Arial", 20))
        row_label.grid(row=i+1, column=0)
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "gray"  # Màu sắc ô bàn cờ
            cell = tk.Label(frame, text="", width=4, height=2, bg=color, font=("Arial", 20))
            cell.grid(row=i+1, column=j+1)

# Hàm hiển thị các bước đi của quân hậu
def display_steps(steps):
    steps_text.delete(1.0, tk.END)  # Xóa nội dung hiện tại
    for step in steps:
        steps_text.insert(tk.END, f"Quân hậu {step[2]} tại hàng {step[0] + 1}, cột {chr(65 + step[1])}\n")

# Hàm bắt đầu giải bài toán
def start_solver():
    global stop_solver, pause_solver
    stop_solver = False
    pause_solver = False
    try:
        position = position_entry.get().upper()
        # Kiểm tra định dạng nhập (ví dụ: A1, H8)
        if len(position) != 2 or position[0] < 'A' or position[0] > 'H' or position[1] < '1' or position[1] > '8':
            messagebox.showerror("Lỗi", "Hãy nhập vị trí hợp lệ (ví dụ: A1, H8)!")
            return
        fixed_col = ord(position[0]) - ord('A')
        fixed_row = int(position[1]) - 1
        board = [-1] * 8
        # Đặt quân hậu cố định vào vị trí được chọn
        board[fixed_row] = fixed_col
        steps = [(fixed_row, fixed_col, "Đặt")]
        display_empty_board(8)  # Hiển thị bàn cờ trống
        root.update()
        time.sleep(speed_slider.get() / 1000.0)  # Chờ theo thời gian từ thanh trượt
        display_solution(board, 8)  # Hiển thị bàn cờ với quân hậu cố định
        root.update()
        time.sleep(speed_slider.get() / 1000.0)  # Chờ theo thời gian từ thanh trượt
        if solve_n_queens(board, 0, 8, steps, (fixed_row, fixed_col)):
            messagebox.showinfo("Kết quả", "Tìm thấy lời giải!")
            display_steps(steps)  # Hiển thị các bước đi
        else:
            if not stop_solver:
                messagebox.showerror("Lỗi", "Không tìm thấy giải pháp.")
    except ValueError:
        messagebox.showerror("Lỗi", "Hãy nhập vị trí hợp lệ!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("8 Quân Hậu")

# Tạo khung nhập liệu
input_frame = tk.LabelFrame(root, text="Nhập liệu", padx=10, pady=10)
input_frame.pack(padx=10, pady=10)

tk.Label(input_frame, text="Vị trí (ví dụ: A1): ").grid(row=0, column=0)
position_entry = tk.Entry(input_frame)
position_entry.grid(row=0, column=1)

tk.Button(input_frame, text="Bắt đầu", command=start_solver).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(input_frame, text="Dừng/Tiếp tục", command=toggle_solving).grid(row=2, column=0, columnspan=2, pady=5)

# Tạo khung hiển thị bàn cờ
board_frame = tk.LabelFrame(root, text="Bàn cờ", padx=10, pady=10)
board_frame.pack(side=tk.LEFT, padx=10, pady=10)

frame = tk.Frame(board_frame)
frame.pack()

# Tạo khung hiển thị lịch sử các bước đi
steps_frame = tk.LabelFrame(root, text="Lịch sử các bước đi", padx=10, pady=10)
steps_frame.pack(side=tk.RIGHT, padx=10, pady=10)

steps_text = tk.Text(steps_frame, width=50, height=20)
steps_text.pack()

# Tạo thanh trượt để điều chỉnh tốc độ
speed_frame = tk.LabelFrame(root, text="Tốc độ", padx=10, pady=10)
speed_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

speed_slider = tk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="Thời gian chờ (ms)")
speed_slider.set(500)
speed_slider.pack()

# Hiển thị bàn cờ trống ngay từ đầu
display_empty_board(8)

root.mainloop()

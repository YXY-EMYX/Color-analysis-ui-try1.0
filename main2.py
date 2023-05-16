import tkinter as tk
from tkinter import filedialog, ttk, Toplevel, IntVar
from tkinterdnd2 import DND_FILES, TkinterDnD
from ttkthemes import ThemedStyle
from PIL import Image
from colorthief import ColorThief

def drop(event):
    file_path = event.data
    selected_file_label.config(text=file_path)

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    selected_file_label.config(text=file_path)

def create_color_block(parent, color, text, row, column):
    color_hex = '#%02x%02x%02x' % color
    color_block = tk.Label(parent, bg=color_hex, width=10, height=2)
    color_block.grid(row=row, column=column)
    color_label = ttk.Label(parent, text=text)
    color_label.grid(row=row+1, column=column)

def analyze_colors():
    # 读取图片
    file_path = selected_file_label.cget("text")
    if not file_path:
        return
    color_thief = ColorThief(file_path)

    # 获取主要颜色和调色板
    dominant_color = color_thief.get_color(quality=1)
    color_count = color_count_var.get()
    palette = color_thief.get_palette(color_count=color_count)

    # 创建新的窗口显示结果
    results_window = Toplevel(root)
    results_window.title("分析结果")

    # 显示主要颜色
    dominant_color_frame = ttk.LabelFrame(results_window, text="主要颜色")
    dominant_color_frame.grid(row=0, column=0, sticky="nsew")
    create_color_block(dominant_color_frame, dominant_color, f"RGB: {dominant_color}", 0, 0)

    # 显示调色板
    palette_frame = ttk.LabelFrame(results_window, text="调色板")
    palette_frame.grid(row=1, column=0, sticky="nsew")
    for i, color in enumerate(palette):
        create_color_block(palette_frame, color, f"RGB: {color}", i // 5 * 2, i % 5)

    # 将结果写入文件
    with open('color_results.txt', 'w') as file:
        file.write(f'Dominant color: RGB {dominant_color}\n')
        file.write('Palette:\n')
        for color in palette:
            file.write(f'RGB {color}\n')

root = TkinterDnD.Tk()
root.title("图片颜色分析器")

style = ThemedStyle(root)
style.set_theme("arc")

drop_frame = tk.Label(root, text="拖拽图片到这里", width=50, height=20, relief="solid")
drop_frame.grid(row=0, column=0, rowspan=8)
drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)

upload_button = ttk.Button(root, text="上传图片", command=open_file_dialog)
upload_button.grid(row=0, column=1)

selected_file_label = ttk.Label(root, text="")
selected_file_label.grid(row=1, column=1)

color_count_var = IntVar(value=6)  # 默认色板颜色数量为6
color_count_entry = ttk.Entry(root, textvariable=color_count_var)
color_count_entry.grid(row=2, column=1)

analyze_button = ttk.Button(root, text="分析颜色", command=analyze_colors)
analyze_button.grid(row=3, column=1)

root.mainloop()

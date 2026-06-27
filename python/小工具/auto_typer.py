import time
import random
import pyautogui
import keyboard as kb
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import win32api  # 新增：用于获取屏幕信息
import win32con  # 新增：Windows常量

class AutoTyper:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.is_running = False
        self.typing_speed = 0.15
        self.mouse_movement = True
        self.current_file = None
        self.loop_typing = True
        self.words_typed = 0
        # 新增：自动滚动相关
        self.auto_scroll = True
        self.scroll_threshold = 15  # 每打15行自动滚动
        self.line_count = 0
        self.last_y_position = None
        
    def get_cursor_position(self):
        """获取当前光标位置（用于判断是否需要滚动）"""
        try:
            # 尝试获取光标位置（需要安装pywin32）
            return pyautogui.position()
        except:
            return None
    
    def scroll_down(self, lines=3):
        """向下滚动文档"""
        try:
            # 方法1：使用Page Down键
            self.keyboard.press(Key.page_down)
            self.keyboard.release(Key.page_down)
            time.sleep(0.2)
            
            # 或者方法2：使用鼠标滚轮
            # pyautogui.scroll(-lines * 3)  # 负数表示向下滚动
            
            print(f"自动向下滚动 {lines} 行")
        except Exception as e:
            print(f"滚动失败: {e}")
    
    def smart_scroll(self):
        """智能滚动 - 根据打字位置判断"""
        if not self.auto_scroll:
            return
            
        self.line_count += 1
        
        # 每打一定行数就滚动
        if self.line_count >= self.scroll_threshold:
            # 随机滚动1-3行
            scroll_lines = random.randint(1, 3)
            self.scroll_down(scroll_lines)
            self.line_count = 0
            
            # 滚动后可能移动鼠标
            if random.random() < 0.3:
                self.random_mouse_move()
    
    def simulate_typing(self, text):
        """模拟人工打字 - 带自动滚动"""
        words = text.split()
        word_count = 0
        target_pause = random.randint(20, 40)
        
        for word in words:
            if not self.is_running:
                break
            
            # 打字前随机停顿
            if random.random() < 0.15:
                think_time = random.uniform(1.5, 5.0)
                print(f"思考中... {think_time:.1f}秒")
                time.sleep(think_time)
            
            # 逐个字母打字
            for char in word:
                if not self.is_running:
                    break
                
                delay = random.uniform(0.08, 0.25)
                time.sleep(delay)
                
                # 偶尔打错字
                if random.random() < 0.005:
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    self.keyboard.type(wrong_char)
                    time.sleep(random.uniform(0.1, 0.3))
                    self.keyboard.press(Key.backspace)
                    self.keyboard.release(Key.backspace)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # 输入正确的字符
                self.keyboard.type(char)
                self.words_typed += 1
                word_count += 1
                
                # 检查是否需要长停顿
                if word_count >= target_pause:
                    pause_time = random.uniform(3, 30)
                    print(f"休息一下... {pause_time:.1f}秒 (已打{self.words_typed}字)")
                    time.sleep(pause_time)
                    word_count = 0
                    target_pause = random.randint(20, 40)
                    
                    if random.random() < 0.3:
                        self.simulate_other_activities()
            
            # 单词后加空格
            self.keyboard.type(' ')
            time.sleep(random.uniform(0.2, 0.5))
            
            # 每打完一个单词就检查是否需要滚动
            self.smart_scroll()
            
            # 偶尔换行
            if random.random() < 0.1:
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                time.sleep(random.uniform(0.5, 1.5))
                # 换行后也可能需要滚动
                if self.line_count > self.scroll_threshold - 5:
                    self.smart_scroll()
            
            # 随机移动鼠标
            if self.mouse_movement and random.random() < 0.1:
                self.random_mouse_move()
    
    def simulate_other_activities(self):
        """模拟其他工作活动"""
        activity = random.choice(['scroll', 'click', 'move_mouse', 'pause', 'page_down'])
        
        if activity == 'scroll':
            pyautogui.scroll(random.randint(-5, -1))  # 向下滚动
            time.sleep(random.uniform(0.5, 1.5))
        elif activity == 'click':
            pyautogui.click()
            time.sleep(random.uniform(0.3, 1))
        elif activity == 'move_mouse':
            current_x, current_y = pyautogui.position()
            pyautogui.moveTo(current_x + random.randint(-100, 100),
                           current_y + random.randint(-50, 50),
                           duration=random.uniform(0.5, 1.5))
            time.sleep(random.uniform(0.5, 1))
        elif activity == 'pause':
            time.sleep(random.uniform(2, 5))
        elif activity == 'page_down':
            self.scroll_down(random.randint(1, 2))
    
    def random_mouse_move(self):
        """随机移动鼠标"""
        current_x, current_y = self.mouse.position
        new_x = current_x + random.randint(-30, 30)
        new_y = current_y + random.randint(-20, 20)
        self.mouse.position = (new_x, new_y)
        time.sleep(random.uniform(0.1, 0.3))
    
    def read_text_file(self, filepath):
        """读取txt文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"读取文件错误: {e}")
            return None
    
    def start_typing(self, content):
        """开始自动打字"""
        self.is_running = True
        self.words_typed = 0
        self.line_count = 0  # 重置行计数
        loop_count = 0
        
        print("3秒后开始自动打字...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("开始自动打字！按F12停止")
        print("提示：程序会自动滚动文档，不用担心超出屏幕")
        time.sleep(random.uniform(0.5, 1.5))
        
        while self.is_running and self.loop_typing:
            loop_count += 1
            print(f"\n=== 第 {loop_count} 轮开始 ===")
            
            self.simulate_typing(content)
            
            if self.is_running and self.loop_typing:
                between_loops_pause = random.uniform(10, 60)
                print(f"\n=== 第 {loop_count} 轮完成！休息 {between_loops_pause:.1f}秒 ===")
                print(f"本轮共打 {self.words_typed} 字")
                
                # 休息时也偶尔滚动
                for _ in range(random.randint(1, 3)):
                    if not self.is_running:
                        break
                    self.simulate_other_activities()
                    time.sleep(random.uniform(2, 5))
                
                time.sleep(between_loops_pause)
        
        print(f"\n打字结束！共完成 {loop_count} 轮，打字数：{self.words_typed}")
        self.is_running = False

class AutoTyperGUI:
    def __init__(self):
        self.auto_typer = AutoTyper()
        self.window = tk.Tk()
        self.window.title("1")
        self.window.geometry("700x600")
        
        self.setup_ui()
        self.setup_hotkey()
        
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_label = tk.Label(self.window, text="无情打字机器", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # 文件选择区域
        file_frame = tk.Frame(self.window)
        file_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(file_frame, text="选择txt文件:").pack(side=tk.LEFT)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, width=40)
        file_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(file_frame, text="浏览", command=self.browse_file).pack(side=tk.LEFT)
        
        # 内容预览
        preview_frame = tk.Frame(self.window)
        preview_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(preview_frame, text="文件内容预览:").pack(anchor=tk.W)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=6, width=60)
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 设置参数
        settings_frame = tk.LabelFrame(self.window, text="设置参数", padx=10, pady=10)
        settings_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # 第一行：打字速度
        row1_frame = tk.Frame(settings_frame)
        row1_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(row1_frame, text="打字速度:").pack(side=tk.LEFT)
        
        self.speed_var = tk.DoubleVar(value=0.15)
        speed_scale = tk.Scale(row1_frame, from_=0.05, to=0.3, resolution=0.01,
                              orient=tk.HORIZONTAL, variable=self.speed_var,
                              length=150, label="秒/字")
        speed_scale.pack(side=tk.LEFT, padx=10)
        
        # 第二行：停顿设置
        row2_frame = tk.Frame(settings_frame)
        row2_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(row2_frame, text="停顿间隔:").pack(side=tk.LEFT)
        
        self.pause_interval_var = tk.IntVar(value=30)
        pause_scale = tk.Scale(row2_frame, from_=10, to=50, resolution=5,
                              orient=tk.HORIZONTAL, variable=self.pause_interval_var,
                              length=150, label="字")
        pause_scale.pack(side=tk.LEFT, padx=10)
        
        tk.Label(row2_frame, text="停顿时间:").pack(side=tk.LEFT, padx=(20,0))
        
        self.pause_duration_var = tk.IntVar(value=15)
        pause_dur_scale = tk.Scale(row2_frame, from_=3, to=30, resolution=1,
                                  orient=tk.HORIZONTAL, variable=self.pause_duration_var,
                                  length=150, label="秒")
        pause_dur_scale.pack(side=tk.LEFT, padx=10)
        
        # 第三行：滚动设置
        row3_frame = tk.Frame(settings_frame)
        row3_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(row3_frame, text="滚动设置:").pack(side=tk.LEFT)
        
        self.scroll_var = tk.BooleanVar(value=True)
        scroll_check = tk.Checkbutton(row3_frame, text="自动滚动文档", 
                                     variable=self.scroll_var)
        scroll_check.pack(side=tk.LEFT, padx=10)
        
        tk.Label(row3_frame, text="滚动间隔:").pack(side=tk.LEFT, padx=(10,0))
        
        self.scroll_interval_var = tk.IntVar(value=15)
        scroll_interval_scale = tk.Scale(row3_frame, from_=5, to=30, resolution=1,
                                        orient=tk.HORIZONTAL, variable=self.scroll_interval_var,
                                        length=100, label="行")
        scroll_interval_scale.pack(side=tk.LEFT, padx=10)
        
        # 第四行：其他选项
        row4_frame = tk.Frame(settings_frame)
        row4_frame.pack(fill=tk.X, pady=5)
        
        self.mouse_var = tk.BooleanVar(value=True)
        mouse_check = tk.Checkbutton(row4_frame, text="模拟鼠标移动", 
                                    variable=self.mouse_var)
        mouse_check.pack(side=tk.LEFT, padx=5)
        
        self.loop_var = tk.BooleanVar(value=True)
        loop_check = tk.Checkbutton(row4_frame, text="循环打字", 
                                   variable=self.loop_var)
        loop_check.pack(side=tk.LEFT, padx=20)
        
        # 开始/停止按钮
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="开始打字", 
                                     command=self.start_typing,
                                     bg="green", fg="white", 
                                     font=("Arial", 12, "bold"),
                                     width=15, height=2)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="停止", 
                                    command=self.stop_typing,
                                    bg="red", fg="white",
                                    font=("Arial", 12, "bold"),
                                    width=15, height=2,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(self.window, textvariable=self.status_var, 
                              font=("Arial", 10), fg="blue")
        status_label.pack(pady=5)
        
        # 提示信息
        tip_text = """使用提示：
1. 选择要打字的txt文件
2. 设置打字速度和停顿参数
3. 开启"自动滚动文档"防止超出屏幕
4. 点击"开始打字"，3秒内切换到Word窗口
5. 程序会自动滚动和循环打字，按F12随时停止"""
        
        tip_label = tk.Label(self.window, text=tip_text, 
                           justify=tk.LEFT, font=("Arial", 9),
                           fg="gray", bg="#f0f0f0")
        tip_label.pack(pady=10, padx=20, fill=tk.X)
        
    def setup_hotkey(self):
        """设置热键"""
        kb.add_hotkey('F12', self.stop_typing)
        
    def browse_file(self):
        """浏览文件"""
        filepath = filedialog.askopenfilename(
            title="选择txt文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            self.file_path_var.set(filepath)
            self.auto_typer.current_file = filepath
            content = self.auto_typer.read_text_file(filepath)
            if content:
                self.preview_text.delete(1.0, tk.END)
                if len(content) > 500:
                    preview = content[:500] + "...\n\n(内容太长，只显示前500字)"
                else:
                    preview = content
                self.preview_text.insert(tk.END, preview)
    
    def start_typing(self):
        """开始打字"""
        if not self.file_path_var.get():
            messagebox.showwarning("警告", "请先选择txt文件！")
            return
        
        content = self.auto_typer.read_text_file(self.file_path_var.get())
        if not content:
            messagebox.showerror("错误", "无法读取文件内容！")
            return
        
        # 更新所有设置
        self.auto_typer.typing_speed = self.speed_var.get()
        self.auto_typer.mouse_movement = self.mouse_var.get()
        self.auto_typer.loop_typing = self.loop_var.get()
        self.auto_typer.auto_scroll = self.scroll_var.get()
        self.auto_typer.scroll_threshold = self.scroll_interval_var.get()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("正在自动打字... 按F12停止")
        
        threading.Thread(target=self.typing_thread, args=(content,), daemon=True).start()
    
    def typing_thread(self, content):
        """打字线程"""
        try:
            self.auto_typer.start_typing(content)
        except Exception as e:
            print(f"打字出错: {e}")
        finally:
            self.window.after(0, self.reset_ui)
    
    def stop_typing(self):
        """停止打字"""
        if self.auto_typer.is_running:
            self.auto_typer.is_running = False
            self.status_var.set("已停止")
            messagebox.showinfo("提示", "已停止自动打字")
    
    def reset_ui(self):
        """重置界面"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("就绪")
    
    def run(self):
        """运行GUI"""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self):
        """窗口关闭事件"""
        if self.auto_typer.is_running:
            if messagebox.askokcancel("退出", "打字任务正在进行中，确定要退出吗？"):
                self.auto_typer.is_running = False
                self.window.destroy()
        else:
            self.window.destroy()

def main():
    app = AutoTyperGUI()
    app.run()

if __name__ == "__main__":
    main()
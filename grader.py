import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

class GradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Grader Pro")
        self.root.geometry("700x900")
        
        # 配置根窗口
        self.root.configure(bg='#f0f0f0')
        self.root.grid_columnconfigure(0, weight=1)  # 使内容水平居中
        
        # 创建主滚动框架
        self.main_canvas = tk.Canvas(root, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas, style='Main.TFrame')
        
        # 配置滚动区域
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局主要组件
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 配置画布权重
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # 配置主题样式
        self.configure_styles()
        
        # 创建内容框架
        content_frame = ttk.Frame(self.scrollable_frame, style='Main.TFrame', padding="20")
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)  # 使内容在框架中居中
        
        # 添加标题
        title_label = ttk.Label(content_frame, 
                              text="Speed Grader Pro", 
                              style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 初始化问题数量输入区域
        self.init_question_count_section(content_frame)
        
        # 初始化分数输入区域（初始为空）
        self.scores_frame = ttk.Frame(content_frame, style='Scores.TFrame')
        self.scores_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")
        self.scores_frame.grid_columnconfigure(0, weight=1)  # 使分数输入区域居中
        
        self.score_entries = []
        self.bonus_entries = []
        
        # 结果显示区域
        result_frame = ttk.Frame(content_frame, style='Result.TFrame')
        result_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")
        result_frame.grid_columnconfigure(0, weight=1)  # 使结果区域居中
        
        result_label = ttk.Label(result_frame, text="Detailed Scores", style='SectionTitle.TLabel')
        result_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.result_text = tk.Text(result_frame, height=12, width=50, font=('Segoe UI', 10),
                                 bg='white', relief='solid', borderwidth=1)
        self.result_text.grid(row=1, column=0, columnspan=2, pady=5)
        
        # 添加总分显示标签
        self.total_score_frame = ttk.Frame(content_frame, style='Total.TFrame')
        self.total_score_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky="ew")
        self.total_score_frame.grid_columnconfigure(0, weight=1)  # 使总分区域居中
        
        total_score_container = ttk.Frame(self.total_score_frame, style='Total.TFrame')
        total_score_container.grid(row=0, column=0)
        
        ttk.Label(total_score_container, text="Total Score:", 
                 style='TotalLabel.TLabel').grid(row=0, column=0, padx=5)
        self.total_score_label = ttk.Label(total_score_container, text="0.0", 
                                         style='TotalScore.TLabel')
        self.total_score_label.grid(row=0, column=1, padx=5)
        
        # 复制按钮
        self.copy_button = ttk.Button(content_frame, text="Copy Results",
                                    command=self.copy_result, style='Action.TButton')
        self.copy_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.copy_button.state(['disabled'])
        
        # 绑定鼠标滚轮事件
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def configure_styles(self):
        style = ttk.Style()
        
        # 配置颜色
        primary_color = '#2196F3'  # Material Blue
        secondary_color = '#757575'  # Gray
        
        # 主框架样式
        style.configure('Main.TFrame', background='#f0f0f0')
        style.configure('Scores.TFrame', background='#f0f0f0')
        style.configure('Result.TFrame', background='#f0f0f0')
        style.configure('Total.TFrame', background='#f0f0f0')
        
        # 标题样式
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=primary_color,
                       background='#f0f0f0')
        
        # 部分标题样式
        style.configure('SectionTitle.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=secondary_color,
                       background='#f0f0f0')
        
        # 标签样式
        style.configure('TLabel',
                       font=('Segoe UI', 10),
                       background='#f0f0f0')
        
        # 输入框样式
        style.configure('TEntry',
                       font=('Segoe UI', 10))
        
        # 按钮样式
        style.configure('TButton',
                       font=('Segoe UI', 10))
        
        style.configure('Action.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        # 总分样式
        style.configure('TotalLabel.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=secondary_color,
                       background='#f0f0f0')
        
        style.configure('TotalScore.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=primary_color,
                       background='#f0f0f0')

    def init_question_count_section(self, parent_frame):
        # 问题数量输入区域
        question_frame = ttk.Frame(parent_frame, style='Main.TFrame')
        question_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")
        question_frame.grid_columnconfigure(0, weight=1)  # 使问题输入区域居中
        
        input_container = ttk.Frame(question_frame, style='Main.TFrame')
        input_container.grid(row=1, column=0)
        
        # 添加说明标签
        instruction_label = ttk.Label(question_frame, 
                                    text="Enter the number of questions:",
                                    style='SectionTitle.TLabel')
        instruction_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        ttk.Label(input_container, text="Regular Questions:").grid(row=0, column=0, padx=10)
        self.regular_count = ttk.Entry(input_container, width=10)
        self.regular_count.grid(row=0, column=1, padx=10)
        
        ttk.Label(input_container, text="Bonus Questions:").grid(row=0, column=2, padx=10)
        self.bonus_count = ttk.Entry(input_container, width=10)
        self.bonus_count.grid(row=0, column=3, padx=10)
        
        confirm_button = ttk.Button(question_frame, text="Confirm",
                                  command=self.create_score_entries,
                                  style='Action.TButton')
        confirm_button.grid(row=2, column=0, pady=20)

    def create_score_entries(self):
        try:
            regular_count = int(self.regular_count.get())
            bonus_count = int(self.bonus_count.get())
            
            if regular_count <= 0:
                messagebox.showerror("Error", "Regular questions count must be greater than 0")
                return
            
            if bonus_count < 0:
                messagebox.showerror("Error", "Bonus questions count cannot be negative")
                return
            
            # 清除现有的输入框
            for widget in self.scores_frame.winfo_children():
                widget.destroy()
            self.score_entries.clear()
            self.bonus_entries.clear()
            
            # 创建容器来居中显示内容
            scores_container = ttk.Frame(self.scores_frame, style='Scores.TFrame')
            scores_container.grid(row=0, column=0)
            
            # 添加说明标签
            score_label = ttk.Label(scores_container, 
                                  text="Enter scores for each question:",
                                  style='SectionTitle.TLabel')
            score_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
            
            # 创建常规题目的分数输入框
            for i in range(regular_count):
                ttk.Label(scores_container, text=f"Question {i+1}:").grid(
                    row=i+1, column=0, padx=10, pady=5, sticky='e')
                entry = ttk.Entry(scores_container, width=10)
                entry.grid(row=i+1, column=1, padx=10, pady=5)
                self.score_entries.append(entry)
            
            # 创建bonus题目的分数输入框
            if bonus_count > 0:
                bonus_label = ttk.Label(scores_container, 
                                      text="Bonus Questions",
                                      style='SectionTitle.TLabel')
                bonus_label.grid(row=regular_count+1, column=0, columnspan=2, 
                               pady=(20, 10))
                
                for i in range(bonus_count):
                    ttk.Label(scores_container, text=f"Bonus {i+1}:").grid(
                        row=regular_count+i+2, column=0, padx=10, pady=5, sticky='e')
                    entry = ttk.Entry(scores_container, width=10)
                    entry.grid(row=regular_count+i+2, column=1, padx=10, pady=5)
                    self.bonus_entries.append(entry)
            
            # 添加计算按钮
            calculate_button = ttk.Button(scores_container, 
                                        text="Calculate Total",
                                        command=self.calculate_total,
                                        style='Action.TButton')
            calculate_button.grid(row=regular_count+bonus_count+3, 
                                column=0, columnspan=2, pady=20)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def calculate_total(self):
        try:
            # 计算常规题目总分
            regular_scores = [float(entry.get()) for entry in self.score_entries]
            regular_total = sum(regular_scores)
            
            # 计算bonus分数
            bonus_total = 0
            if self.bonus_entries:
                bonus_scores = [float(entry.get()) for entry in self.bonus_entries]
                bonus_total = sum(bonus_scores)
            
            # 计算最终总分（不超过100）
            final_total = min(100, regular_total + bonus_total)
            
            # 更新总分显示
            self.total_score_label.config(text=f"{final_total:.1f}")
            
            # 生成详细得分文本
            result_text = ""
            for i, score in enumerate(regular_scores, 1):
                result_text += f"{i}. {score}\n"
            
            if self.bonus_entries:
                result_text += "\nBonus:\n"
                for i, score in enumerate(bonus_scores, 1):
                    result_text += f"B{i}. {score}\n"
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text)
            self.copy_button.state(['!disabled'])
            
        except ValueError:
            messagebox.showerror("Error", "Please ensure all scores are valid numbers")

    def copy_result(self):
        result = self.result_text.get(1.0, tk.END)
        pyperclip.copy(result)
        messagebox.showinfo("Success", "Results copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculator(root)
    root.mainloop()

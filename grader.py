import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

class GradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("成绩计算器")
        self.root.geometry("600x800")
        
        # 样式设置
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 初始化问题数量输入区域
        self.init_question_count_section()
        
        # 初始化分数输入区域（初始为空）
        self.scores_frame = ttk.Frame(self.main_frame)
        self.scores_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.score_entries = []
        self.bonus_entries = []
        
        # 结果显示区域
        self.result_text = tk.Text(self.main_frame, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 复制按钮
        self.copy_button = ttk.Button(self.main_frame, text="复制结果", command=self.copy_result)
        self.copy_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.copy_button.state(['disabled'])

    def init_question_count_section(self):
        # 问题数量输入区域
        question_frame = ttk.Frame(self.main_frame)
        question_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(question_frame, text="常规题目数量:").grid(row=0, column=0, padx=5)
        self.regular_count = ttk.Entry(question_frame, width=10)
        self.regular_count.grid(row=0, column=1, padx=5)
        
        ttk.Label(question_frame, text="Bonus题目数量:").grid(row=0, column=2, padx=5)
        self.bonus_count = ttk.Entry(question_frame, width=10)
        self.bonus_count.grid(row=0, column=3, padx=5)
        
        ttk.Button(question_frame, text="确认", command=self.create_score_entries).grid(row=0, column=4, padx=5)

    def create_score_entries(self):
        try:
            regular_count = int(self.regular_count.get())
            bonus_count = int(self.bonus_count.get())
            
            # 清除现有的输入框
            for widget in self.scores_frame.winfo_children():
                widget.destroy()
            self.score_entries.clear()
            self.bonus_entries.clear()
            
            # 创建常规题目的分数输入框
            for i in range(regular_count):
                ttk.Label(self.scores_frame, text=f"第{i+1}题分数:").grid(row=i, column=0, padx=5, pady=2)
                entry = ttk.Entry(self.scores_frame, width=10)
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.score_entries.append(entry)
            
            # 创建bonus题目的分数输入框
            for i in range(bonus_count):
                ttk.Label(self.scores_frame, text=f"Bonus {i+1}分数:").grid(row=regular_count+i, column=0, padx=5, pady=2)
                entry = ttk.Entry(self.scores_frame, width=10)
                entry.grid(row=regular_count+i, column=1, padx=5, pady=2)
                self.bonus_entries.append(entry)
            
            # 添加计算按钮
            ttk.Button(self.scores_frame, text="计算总分", command=self.calculate_total).grid(
                row=regular_count+bonus_count, column=0, columnspan=2, pady=10)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的题目数量")

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
            
            # 生成详细得分文本
            result_text = ""
            for i, score in enumerate(regular_scores, 1):
                result_text += f"{i}. {score}\n"
            
            if self.bonus_entries:
                result_text += "\nBonus:\n"
                for i, score in enumerate(bonus_scores, 1):
                    result_text += f"B{i}. {score}\n"
            
            result_text += f"\n总分: {final_total:.1f}"
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text)
            self.copy_button.state(['!disabled'])  # 启用复制按钮
            
        except ValueError:
            messagebox.showerror("错误", "请确保所有分数都是有效的数字")

    def copy_result(self):
        result = self.result_text.get(1.0, tk.END)
        pyperclip.copy(result)
        messagebox.showinfo("成功", "结果已复制到剪贴板")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculator(root)
    root.mainloop()

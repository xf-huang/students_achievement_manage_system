# -*- coding:utf-8 -*-

from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.messagebox import *
from matplotlib import pyplot as plt
from Database import Database
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题

# 全局变量
bm = None
v = None
user = None

# 数据库对象
db = Database()


class ManagerUI(object):
    """管理系统界面和后台"""

    def __init__(self):

        self.root = Tk()  # tkinter主窗口
        self.root.resizable(100, 100)  # 调节大小
        self.screen_width = self.root.winfo_screenwidth()  # 获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  # 获得屏幕高度
        # 容器,添加各种组件
        self.frame_1 = Frame(self.root)
        # # 以place的形式添加到root中

        self.frame_1.place(x=0, y=0)

        # 用户名和密码的文本框, show="*"，防止密码泄露
        self.entry_1 = Entry(self.frame_1, bd=5, width=30)
        self.entry_2 = Entry(self.frame_1, bd=5, width=30, show="*")

        self.user = self.entry_1.get()

    # 登录界面
    def login(self):

        """登录界面"""
        self.root.title("登录界面")
        # 设置窗口大小
        screen_width = self.root.winfo_screenwidth()  # 获得屏幕宽度
        screen_height = self.root.winfo_screenheight()  # 获得屏幕高度
        self.root.geometry("280x260+%d+%d" % (self.screen_width / 4, self.screen_height / 7))
        # 背景图片
        global bm
        img = Image.open('./bg.webp')
        img = img.resize((190, 100))
        bm = ImageTk.PhotoImage(img)
        # 容器,添加各种组件
        frame_1 = self.frame_1
        # # 以place的形式添加到root中
        frame_1.place(x=0, y=0)
        # 添加背景图
        label_img = Label(frame_1, image=bm)
        # 添加用户名和密码输入框
        label_1 = Label(frame_1, text="用户名:")
        label_2 = Label(frame_1, text="密码:")

        # 以网格布局的形式加入到root中
        label_img.grid(row=0, column=1, sticky='w')
        label_1.grid(row=1, column=0)
        self.entry_1.grid(row=1, column=1)
        label_2.grid(row=3, column=0)
        self.entry_2.grid(row=3, column=1)

        # 选择学生或教师用户的单选按钮
        global v
        v = StringVar()
        radio_button1 = Radiobutton(frame_1, text="教师", variable=v, value="teacher", indicatoron=False)
        radio_button1.grid(row=5, column=1, sticky='w')
        radio_button2 = Radiobutton(frame_1, text="学生", variable=v, value="student", indicatoron=False)
        radio_button2.grid(row=6, column=1, sticky='w')

        # 添加按钮
        button_1 = Button(frame_1, text="登录", command=lambda: self.judge(), width=10)
        button_3 = Button(frame_1, text="注册", command=lambda: self.register_UI(), width=10)
        button_1.grid(row=4, column=1)
        button_3.grid(row=6, column=1)

        self.root.mainloop()

    def judge(self):
        """判断用户名和密码是否正确"""
        # 获取用户身份
        status = v.get()
        num = self.entry_1.get()
        global user
        user = num
        pw = self.entry_2.get()
        flag = Database.search_user(db, status, num, pw)

        # 如果用户名和密码正确
        if flag and status == 'teacher':
            # 消息提示
            showinfo(title="提示界面", message="登录成功！！！\n欢迎使用学成绩管理系统")
            # 清除登陆界面的组件
            for widget in self.frame_1.winfo_children():
                widget.destroy()
            self.teacher_ui()
        if flag and status == 'student':
            # 消息提示
            showinfo(title="提示界面", message="登录成功！！！\n欢迎使用学成绩管理系统")
            # 清除登陆界面的组件
            for widget in self.frame_1.winfo_children():
                widget.destroy()
            self.student_ui()
        if not flag:
            showerror(title="错误界面", message="用户名或密码错误！！！\n请重新输入！！！")
        else:
            return

    def register_UI(self):
        """注册界面"""
        # 获取用户身份信息
        status = v.get()
        # 如果是教师，显示教师注册页面
        if status == 'teacher':

            # 清除登陆界面的组件
            for widget in self.frame_1.winfo_children():
                widget.destroy()
            self.root.title("注册界面")
            # 设置窗口大小
            self.root.geometry("280x240+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

            label_1 = Label(self.frame_1, text="姓名:")
            label_2 = Label(self.frame_1, text="工号:")
            label_3 = Label(self.frame_1, text="登录密码:")
            label_4 = Label(self.frame_1, text="教师注册码:")
            entry_1 = Entry(self.frame_1, width=30)
            entry_2 = Entry(self.frame_1, width=30)
            entry_3 = Entry(self.frame_1, width=30)
            entry_4 = Entry(self.frame_1, width=30)
            # 以网格布局的形式加入到root中

            label_1.grid(row=1, column=0)
            entry_1.grid(row=1, column=1)
            label_2.grid(row=2, column=0)
            entry_2.grid(row=2, column=1)
            label_3.grid(row=3, column=0)
            entry_3.grid(row=3, column=1)
            label_4.grid(row=4, column=0)
            entry_4.grid(row=4, column=1)

            def register_t():
                # 获取注册信息
                name = entry_1.get()
                number = entry_2.get()
                password = entry_3.get()
                code = entry_4.get()
                # 判断注册信息
                if (number.isdigit() == False) or len(number) != 5:
                    messagebox.showerror("提示", "工号必须是5位整数")
                    return
                if code != '12345':
                    messagebox.showerror("提示", "注册码不正确")
                    return
                else:
                    # 在信息表中插入注册信息
                    Database.register(db, status, name, number, password)
                    messagebox.showinfo("提示", f"注册成功！\n您的用户名是:{number}\n密码是:{password}")

            # 添加按钮
            button_1 = Button(self.frame_1, text="注册", command=register_t, width=10)
            button_1.grid(row=5, column=1)
            self.root.mainloop()

        # 如果是学生，显示学生注册界面
        if status == 'student':

            # 清除登陆界面的组件
            for widget in self.frame_1.winfo_children():
                widget.destroy()
            self.root.title("注册界面")
            # 设置窗口大小
            self.root.geometry("280x240+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

            label_1 = Label(self.frame_1, text="姓名:")
            label_2 = Label(self.frame_1, text="学号:")
            label_3 = Label(self.frame_1, text="班级:")
            label_4 = Label(self.frame_1, text="登录密码:")
            label_5 = Label(self.frame_1, text="学生注册码:")
            entry_1 = Entry(self.frame_1, width=30)
            entry_2 = Entry(self.frame_1, width=30)
            entry_3 = Entry(self.frame_1, width=30)
            entry_4 = Entry(self.frame_1, width=30)
            entry_5 = Entry(self.frame_1, width=30)
            # 以网格布局的形式加入到root_2中

            label_1.grid(row=1, column=0)
            entry_1.grid(row=1, column=1)
            label_2.grid(row=2, column=0)
            entry_2.grid(row=2, column=1)
            label_3.grid(row=3, column=0)
            entry_3.grid(row=3, column=1)
            label_4.grid(row=4, column=0)
            entry_4.grid(row=4, column=1)
            label_5.grid(row=5, column=0)
            entry_5.grid(row=5, column=1)

            def register_s():
                # 获取注册信息
                name = entry_1.get()
                number = entry_2.get()
                Class = entry_3.get()
                password = entry_4.get()
                code = entry_5.get()
                # 判断注册信息
                if (number.isdigit() == False) or len(number) != 8:
                    messagebox.showerror("提示", "学号必须是8位整数")
                    return
                if (Class.isdigit() == False) or len(Class) != 4:
                    messagebox.showerror("提示", "班级必须是4位整数")
                    return
                if code != '12345':
                    messagebox.showerror("提示", "注册码不正确")
                    return
                else:
                    # 在信息表中插入注册信息
                    Database.register(db, status, name, number, password)
                    messagebox.showinfo("提示", f"注册成功！\n您的用户名是:{number}\n密码是:{password}")



            # 提交按钮
            button_1 = Button(self.frame_1, text="注册", command=register_s, width=10)
            button_1.grid(row=6, column=1)

            self.root.mainloop()

    # 教师用户界面
    def teacher_ui(self):
        # 清除登陆界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        # 创建考试成绩表score
        Database.exam_table(db)
        self.root.title("教师用户界面")
        # 设置窗口大小
        self.root.geometry("320x280+%d+%d" % (self.screen_width / 4, self.screen_height / 7))
        # 添加按钮
        button1 = Button(self.frame_1, text="成绩录入", bg='#7CCD7C', width=20, height=5,
                         command=lambda: self.score_record())
        button2 = Button(self.frame_1, text="成绩导出", bg='#7CCD7C', width=20, height=5,
                         command=lambda: self.score_export_ui())
        button3 = Button(self.frame_1, text="成绩分析", bg='#7CCD7C', width=20, height=5,
                         command=lambda: self.score_analise())
        button4 = Button(self.frame_1, text="成绩统计", bg='#7CCD7C', width=20, height=5,
                         command=lambda: self.score_stat_ui())

        # 以网格布局的形式加入到窗口中

        button1.grid(row=0, column=0, padx=5, pady=5)
        button2.grid(row=0, column=1, padx=5, pady=5)
        button3.grid(row=1, column=0, padx=5, pady=5)
        button4.grid(row=1, column=1, padx=5, pady=5)

        self.root.mainloop()

    # 成绩录入界面
    def score_record(self):
        # 清除之前界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("成绩录入界面")
        # 设置窗口大小
        self.root.geometry("800x600+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        label1 = Label(self.frame_1, text="学号", width=10)
        label2 = Label(self.frame_1, text="语文成绩", width=10)
        label3 = Label(self.frame_1, text="数学成绩", width=10)
        label4 = Label(self.frame_1, text="英语成绩", width=10)
        label5 = Label(self.frame_1, text="物理成绩", width=10)
        label6 = Label(self.frame_1, text="化学成绩", width=10)
        label7 = Label(self.frame_1, text="生物成绩", width=10)
        label8 = Label(self.frame_1, text="总分", width=10)
        label9 = Label(self.frame_1, text="排名", width=10)
        label10 = Label(self.frame_1, text="考试日期", width=10)

        entry1 = Entry(self.frame_1, width=10)
        entry2 = Entry(self.frame_1, width=10)
        entry3 = Entry(self.frame_1, width=10)
        entry4 = Entry(self.frame_1, width=10)
        entry5 = Entry(self.frame_1, width=10)
        entry6 = Entry(self.frame_1, width=10)
        entry7 = Entry(self.frame_1, width=10)
        entry8 = Entry(self.frame_1, width=10)
        entry9 = Entry(self.frame_1, width=10)
        entry10 = Entry(self.frame_1, width=10)

        text = Text(self.frame_1)

        def record():
            id = entry1.get()
            yuwen = entry2.get()
            shuxue = entry3.get()
            yingyu = entry4.get()
            wuli = entry5.get()
            huaxue = entry6.get()
            shenwu = entry7.get()
            zongfen = entry8.get()
            paiming = entry9.get()
            kaoshi = entry10.get()

            # 判断信息是否重复
            flag = Database.check_score(db, id, kaoshi)
            if flag:
                Database.add_score(db, id, yuwen, shuxue, yingyu, wuli, huaxue, shenwu, zongfen, paiming, kaoshi)
                # 将录入的成绩信息显示在下方文本框
                line = ' '.join((id, yuwen, shuxue, yingyu, wuli, huaxue, shenwu, zongfen, paiming, kaoshi)) + '\n'
                text.insert(INSERT, line)
            else:
                showerror(title="错误界面", message="已存在该成绩信息，请重新输入")

        # 删除成绩
        def delete_score():
            number = entry1.get()
            date = entry10.get()
            Database.del_score(db, number, date)

        button1 = Button(self.frame_1, text="添加学生", command=lambda: self.allStu_UI())
        button2 = Button(self.frame_1, text="添加考试", command=lambda: self.new_exam_ui())
        button3 = Button(self.frame_1, text="录入成绩", command=record)
        button4 = Button(self.frame_1, text="删除成绩", command=delete_score)
        button5 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())

        label1.grid(row=0, column=0)
        label2.grid(row=0, column=1)
        label3.grid(row=0, column=2)
        label4.grid(row=0, column=3)
        label5.grid(row=0, column=4)
        label6.grid(row=0, column=5)
        label7.grid(row=0, column=6)
        label8.grid(row=0, column=7)
        label9.grid(row=0, column=8)
        label10.grid(row=0, column=9)
        entry1.grid(row=1, column=0)
        entry2.grid(row=1, column=1)
        entry3.grid(row=1, column=2)
        entry4.grid(row=1, column=3)
        entry5.grid(row=1, column=4)
        entry6.grid(row=1, column=5)
        entry7.grid(row=1, column=6)
        entry8.grid(row=1, column=7)
        entry9.grid(row=1, column=8)
        entry10.grid(row=1, column=9)
        button1.grid(row=2, column=5)
        button2.grid(row=2, column=6)
        button3.grid(row=2, column=7)
        button4.grid(row=2, column=8)
        button5.grid(row=2, column=9)
        text.grid(row=3, column=0, rowspan=10, columnspan=9)

    # 添加学生界面
    def allStu_UI(self):
        # 清除之前界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("添加学生界面")
        # 设置窗口大小
        self.root.geometry("400x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        # 创建学生信息表
        Database.stu_info(db)
        label1 = Label(self.frame_1, text="姓名：", width=10)
        label2 = Label(self.frame_1, text="学号：", width=10)
        label3 = Label(self.frame_1, text="班级：", width=10)
        entry1 = Entry(self.frame_1, width=15)
        entry2 = Entry(self.frame_1, width=15)
        entry3 = Entry(self.frame_1, width=15)

        # 添加学生信息
        def add_stu():
            # 获取输入框信息
            name = entry1.get()
            number = entry2.get()
            Class = entry3.get()
            # 判断学生信息
            if (number.isdigit() == False) or len(number) != 8:
                messagebox.showerror("提示", "学号必须是8位整数")
                return
            if (Class.isdigit() == False) or len(Class) != 4:
                messagebox.showerror("提示", "班级必须是4位整数")
                return
            else:
                # 判断学生信息是否重复
                flag = Database.check_student(db, number)
                if flag:
                    # 在stu_info表中插入学生
                    Database.add_student(db, name, number, Class)
                else:
                    showerror(title="错误界面", message="已存在该学生信息，请重新输入")

        # 删除学生信息
        def del_stu():
            number = entry2.get()
            # 判断学号信息
            if (number.isdigit() == False) or len(number) != 8:
                messagebox.showerror("提示", "学号必须是8位整数")
                return
            else:
                # 在stu_info信息表中删除学生
                Database.del_student(db, number)

        button1 = Button(self.frame_1, text="提交", command=add_stu)
        button2 = Button(self.frame_1, text="删除学生", command=del_stu)
        button3 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())

        label1.grid(row=0, column=0, padx=5, pady=5)
        entry1.grid(row=0, column=1, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        entry2.grid(row=1, column=1, padx=5, pady=5)
        label3.grid(row=2, column=0, padx=5, pady=5)
        entry3.grid(row=2, column=1, padx=5, pady=5)
        button1.grid(row=3, column=0, padx=5, pady=5)
        button2.grid(row=3, column=1, padx=5, pady=5)
        button3.grid(row=3, column=2, padx=5, pady=5)

    # 添加新的考试界面
    def new_exam_ui(self):
        # 清除原先界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("添加新考试")
        # 设置窗口大小
        self.root.geometry("400x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        # 创建考试信息表
        Database.exam_info(db)
        label1 = Label(self.frame_1, text="考试名称：", width=10)
        label2 = Label(self.frame_1, text="考试日期：", width=10)
        entry1 = Entry(self.frame_1, width=15)
        entry2 = Entry(self.frame_1, width=15)

        # 添加考试信息
        def add_exam():
            # 获取输入框信息
            name = entry1.get()
            date = entry2.get()
            Database.add_exam(db, name, date)

        button1 = Button(self.frame_1, text="提交", command=add_exam)
        button2 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())
        label1.grid(row=0, column=0, padx=5, pady=5)
        entry1.grid(row=0, column=1, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        entry2.grid(row=1, column=1, padx=5, pady=5)
        button1.grid(row=3, column=0, padx=5, pady=5)
        button2.grid(row=3, column=1, padx=5, pady=5)

    # 成绩导出界面
    def score_export_ui(self):
        # 清除登陆界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("成绩导出界面")
        # 设置窗口大小
        self.root.geometry("600x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        label1 = Label(self.frame_1, text="考试日期：", width=10)
        label2 = Label(self.frame_1, text="导出格式：", width=10)

        cbox1 = ttk.Combobox(self.frame_1)
        cbox2 = ttk.Combobox(self.frame_1)

        dates = Database.get_date(db, 'date')

        cbox1['value'] = dates
        cbox2['value'] = ('xlsx', 'csv', 'txt')

        # 导出成绩表格
        def export():
            date = cbox1.get()
            table = Database.get_score_table(db, date)
            save_format = cbox2.get()
            if save_format == 'txt':
                filenewpath = filedialog.asksaveasfilename(title='保存文件',
                                                           defaultextension='.txt',
                                                           initialdir='C:/Users/Administrator/Desktop')
            if save_format == 'csv':
                filenewpath = filedialog.asksaveasfilename(title='保存文件',
                                                           defaultextension='.csv',
                                                           initialdir='C:/Users/Administrator/Desktop')
            if save_format == 'xlsx':
                filenewpath = filedialog.asksaveasfilename(title='保存文件',
                                                           defaultextension='.xlsx',
                                                           initialdir='C:/Users/Administrator/Desktop')

            with open(filenewpath, 'w') as f:
                f.write("学号, 语文, 数学, 英语, 物理, 化学, 生物, 总分, 排名, 考试日期\n")
                for row in table:
                    f.write(str(row).strip('()') + '\n')

        button = Button(self.frame_1, text="导出", command=export)
        button1 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())

        label1.grid(row=0, column=0, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        cbox1.grid(row=0, column=1, padx=5, pady=5)
        cbox2.grid(row=1, column=1, padx=5, pady=5)
        button.grid(row=3, column=0, padx=5, pady=5)
        button1.grid(row=3, column=1, padx=5, pady=5)

    # 成绩分析界面
    def score_analise(self):
        # 清除登陆界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("成绩分析界面")
        # 设置窗口大小
        self.root.geometry("600x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        label1 = Label(self.frame_1, text="分析项目：", width=10)
        label2 = Label(self.frame_1, text="图表样式：", width=10)

        cbox1 = ttk.Combobox(self.frame_1)
        cbox2 = ttk.Combobox(self.frame_1)

        cbox1['value'] = ('语文', '数学', '英语', '物理', '化学', '生物', '总分')
        cbox2['value'] = ('折线图', '柱状图')

        maps = {
            '语文': 'yuwen',
            '数学': 'shuxue',
            '英语': 'yingyu',
            '物理': 'wuli',
            '化学': 'huaxue',
            '生物': 'shenwu',
            '总分': 'total',
        }

        # 生成分析图表
        def a_plot():
            item = cbox1.get()
            col = maps[item]
            data = Database.get_mean_score(db, col)
            data = [x[0] for x in data]
            kind = cbox2.get()
            x = list(range(1, len(data) + 1))
            if kind == '折线图':
                plt.plot(x, data, '-o')
                plt.xticks(x)
                plt.ylabel(f"{item}平均分")
                plt.show()
            if kind == '柱状图':
                plt.bar(x, data)
                plt.xticks(x)
                plt.ylabel(f"{item}平均分")
                plt.show()

        button = Button(self.frame_1, text="生成图表", command=a_plot)
        button1 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())

        label1.grid(row=0, column=0, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        cbox1.grid(row=0, column=1, padx=5, pady=5)
        cbox2.grid(row=1, column=1, padx=5, pady=5)
        button.grid(row=3, column=0, padx=5, pady=5)
        button1.grid(row=3, column=1, padx=5, pady=5)

    # 成绩统计界面
    def score_stat_ui(self):
        # 清除登陆界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("成绩统计界面")
        # 设置窗口大小
        self.root.geometry("620x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        label1 = Label(self.frame_1, text="考试日期：", width=10)
        label2 = Label(self.frame_1, text="考试科目：", width=10)
        label3 = Label(self.frame_1, text="选择学号：", width=20)

        cbox1 = ttk.Combobox(self.frame_1)
        cbox2 = ttk.Combobox(self.frame_1)
        cbox3 = ttk.Combobox(self.frame_1)

        dates = Database.get_date(db, 'date')
        ids = Database.get_stu_id(db)

        cbox1['value'] = dates
        cbox2['value'] = ('语文', '数学', '英语', '物理', '化学', '生物', '总分')
        cbox3['value'] = ids

        maps = {
            '语文': 'yuwen',
            '数学': 'shuxue',
            '英语': 'yingyu',
            '物理': 'wuli',
            '化学': 'huaxue',
            '生物': 'shenwu',
            '总分': 'total',
        }

        # 总体统计结果
        def general_stat():
            date = cbox1.get()
            item = cbox2.get()
            col = maps[item]
            mean, std = Database.score_stat(db, date, col)
            text.insert(INSERT, f"本次考试的{item}平均分是：{mean}\n标准差是：{std}\n")

        # 单个学生统计结果
        def indivi_stat():
            exam_num = len(dates)
            item = cbox2.get()
            col = maps[item]
            ID = cbox3.get()
            data = Database.get_column(db, col, ID)
            rank = Database.get_column(db, 'rank', ID)
            data = [x[0] for x in data]
            rank = [x[0] for x in rank]
            mean = np.mean(data)
            text.insert(INSERT, f"该学生{exam_num}次考试的{item}分数为：{data}\n平均分为：{mean}\n排名分别为：{rank}\n")

        button1 = Button(self.frame_1, text="总体统计", command=general_stat)
        button2 = Button(self.frame_1, text="单个学生统计", command=indivi_stat)
        button3 = Button(self.frame_1, text="返回", command=lambda: self.teacher_ui())

        text = Text(self.frame_1, width=40, height=30)
        # 以网格布局的形式加入到窗口中

        label1.grid(row=0, column=0, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        label3.grid(row=2, column=0, padx=5, pady=5)
        cbox1.grid(row=0, column=1, padx=5, pady=5)
        cbox2.grid(row=1, column=1, padx=5, pady=5)
        cbox3.grid(row=2, column=1, padx=5, pady=5)
        button1.grid(row=3, column=0, padx=5, pady=0)
        button2.grid(row=3, column=1, padx=5, pady=0, sticky='w')
        button3.grid(row=3, column=1, padx=5, pady=0, sticky='e')
        text.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky='s')

    # 学生用户界面
    def student_ui(self):
        # 清除登陆界面的组件
        for widget in self.frame_1.winfo_children():
            widget.destroy()
        self.root.title("学生用户界面")
        # 设置窗口大小
        self.root.geometry("600x400+%d+%d" % (self.screen_width / 4, self.screen_height / 7))

        label1 = Label(self.frame_1, text="考试日期：", width=10)
        label2 = Label(self.frame_1, text="考试科目：", width=10)
        label3 = Label(self.frame_1, text="是否显示班级排名：", width=20)

        cbox1 = ttk.Combobox(self.frame_1)
        cbox2 = ttk.Combobox(self.frame_1)
        cbox3 = ttk.Combobox(self.frame_1)

        dates = Database.get_date(db, 'date')
        names = Database.get_date(db, 'name')

        cbox1['value'] = dates
        cbox2['value'] = ('语文', '数学', '英语', '物理', '化学', '生物', '总分')
        cbox3['value'] = ('是', '否')

        # 显示查询结果
        def show_results():
            date = cbox1.get()
            subject = cbox2.get()
            flag = cbox3.get()
            maps1 = {
                '语文': 1,
                '数学': 2,
                '英语': 3,
                '物理': 4,
                '化学': 5,
                '生物': 6,
                '总分': 7,

            }

            results = Database.get_scores(db, user, date)
            score = results[maps1[subject]]
            rank = results[-2]
            message1 = f"您本次考试{subject}成绩是：{score}\n"
            message2 = f"您本次考试成绩班级排名：{rank}\n"
            if flag == '是':
                text.insert(INSERT, message1 + message2)
            if flag == '否':
                text.insert(INSERT, message1)

        # 绘制折线图
        def score_plot():
            maps2 = {
                '语文': 'yuwen',
                '数学': 'shuxue',
                '英语': 'yingyu',
                '物理': 'wuli',
                '化学': 'huaxue',
                '生物': 'shenwu',
                '总分': 'total'

            }
            subject = cbox2.get()
            total = Database.get_column(db, 'total', user)
            rank = Database.get_column(db, 'rank', user)
            subject_score = Database.get_column(db, maps2[subject], user)

            x = list(range(1, len(total) + 1))
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
            ax1.plot(x, total, 'o-')
            ax1.set_ylabel("总分")
            #ax1.set_xticks(x, labels=names)

            ax2.plot(x, rank, 'o-')
            ax2.set_ylabel("排名")
            #ax2.set_xticks(x, labels=names)

            ax3.plot(x, subject_score, 'o-')
            ax3.set_ylabel(subject)
            #ax3.set_xticks(x, labels=names)

            plt.show()

        button1 = Button(self.frame_1, text="查询", command=show_results)
        button2 = Button(self.frame_1, text="成绩折线图", command=score_plot)

        text = Text(self.frame_1, width=40, height=30)
        # 以网格布局的形式加入到窗口中

        label1.grid(row=0, column=0, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        label3.grid(row=2, column=0, padx=5, pady=5)
        cbox1.grid(row=0, column=1, padx=5, pady=5)
        cbox2.grid(row=1, column=1, padx=5, pady=5)
        cbox3.grid(row=2, column=1, padx=5, pady=5)
        button1.grid(row=3, column=0, padx=5, pady=5)
        button2.grid(row=3, column=1, padx=5, pady=5)
        text.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky='s')


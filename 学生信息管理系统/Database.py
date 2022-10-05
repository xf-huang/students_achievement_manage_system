# -*- coding:utf-8 -*-

import sqlite3
import numpy as np


class Database:
    """数据库工具类"""

    def __init__(self):
        # 连接数据库获得游标
        self.conn = sqlite3.connect("system.db")
        self.cursor = self.conn.cursor()

    def register(self, status, name, number, password):
        # 创建教师/学生注册信息表
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {status}(name TEXT,number TEXT,password TEXT)")

        # 在信息表中插入注册信息

        try:
            sql = f"INSERT INTO {status} (name, number, password) VALUES ('{name}', '{number}', '{password}')"
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            print("插入注册信息成功")
        except:
            self.conn.rollback()
            print("插入注册信息失败")

    # 搜索用户信息
    def search_user(self, status, num, pw):
        if status == 'teacher':
            cur = self.cursor.execute(f"SELECT * FROM teacher WHERE number=={num} AND password=='{pw}'")
            count = len(cur.fetchall())
            if count >= 1:
                return True
            else:
                return False

        if status == 'student':
            cur = self.cursor.execute(f"SELECT * FROM student WHERE number=={num} AND password=='{pw}'")
            count = len(cur.fetchall())
            if count >= 1:
                return True
            else:
                return False

    # 创建学生信息表
    def stu_info(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stu_info (name TEXT,number INTEGER PRIMARY KEY,class INTEGER)")
        self.conn.commit()

    # 创建考试成绩表
    def exam_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS score (number INTEGER, yuwen INTEGER, shuxue INTEGER,"
                            "yingyu INTEGER, wuli INTEGER, huaxue INTEGER, shenwu INTEGER, total INTEGER, rank INTEGER, date INTEGER)")
        self.conn.commit()

    # 创建考试信息表
    def exam_info(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS exams (name TEXT, date INTEGER);")
        self.conn.commit()

    # 添加考试信息
    def add_exam(self, name, date):
        sql = f"INSERT INTO exams (name, date) VALUES ('{name}', {date})"
        try:
            self.cursor.execute(sql)
            self.conn.commit()

            print("添加考试成功")

        except:
            self.conn.rollback()
            print("添加考试失败")

    # 添加学生
    def add_student(self, name, number, Class):
        sql = f"INSERT INTO stu_info (name, number, class) VALUES ('{name}', {number}, {Class})"
        try:
            self.cursor.execute(sql)
            self.conn.commit()

            print("添加学生成功")

        except:
            self.conn.rollback()
            print("添加学生失败")

    # 删除学生
    def del_student(self, number):
        sql = f"DELETE FROM stu_info WHERE number={number}"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("删除学生成功")

        except:
            self.conn.rollback()
            print("删除学生失败")

    # 录入成绩
    def add_score(self, number, yw, sx, yy, wl, hx, sw, tt, rk, d):
        sql = f"INSERT INTO score (number,yuwen,shuxue,yingyu,wuli,huaxue,shenwu,total,rank,date)" \
              f" VALUES ({number}, {yw}, {sx}, {yy}, {wl}, {hx}, {sw}, {tt}, {rk}, {d})"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("录入成绩成功")

        except:
            self.conn.rollback()
            print("录入成绩失败")

    # 判断学生信息是否重复
    def check_student(self, number):
        """判断学号和考试名是否重复"""
        sql = f"select * from stu_info where number = {number};"

        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row is not None:
            return False
        else:
            return True

    # 判断成绩信息是否重复
    def check_score(self, number, date):
        """判断学号和考试名是否重复"""
        sql = f"select * from score where number = {number} and date == '{date}';"

        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row is not None:
            return False
        else:
            return True

    # 删除成绩
    def del_score(self, number, date):
        sql = f"DELETE FROM score WHERE number={number} AND date={date}"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("删除成绩成功")

        except:
            self.conn.rollback()
            print("删除成绩失败")

    # 获取某个学生某次考试的成绩
    def get_scores(self, ID, date):
        sql = f"SELECT * FROM score WHERE number={ID} and date={date}"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return row

    # 获取某个学生各次考试的某个科目成绩、总分或排名
    def get_column(self, column, ID):
        sql = f"SELECT {column} FROM score WHERE number={ID}"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

    # 获取考试信息
    def get_date(self, column):
        sql = f"SELECT {column} FROM exams"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

    # 获取某次考试的成绩表
    def get_score_table(self, date):
        sql = f"SELECT * FROM score WHERE date={date}"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    # 计算各次考试的平均分
    def get_mean_score(self, column):
        sql = f"SELECT AVG({column}) FROM score GROUP BY date"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

    # 计算某次考试的平均分和标准差
    def score_stat(self, date, column):
        sql = f"SELECT {column} FROM score WHERE date={date}"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        mean = np.mean(row)
        std = np.std(row)
        return mean, std

    # 获取学生学号信息
    def get_stu_id(self):
        sql = f"SELECT number FROM stu_info"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

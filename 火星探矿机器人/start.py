# -*- coding: utf-8 -*-
#主窗口
import random
import sys
from time import sleep
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from Mars_robot_ui import Ui_MarsRobot
from copy import deepcopy
#定义全局变量
region = []
get_diamonds = 0
search_diamonds = 0
diamonds_pos = []

class SearchRobotThread(QThread):
    _signal = pyqtSignal(str)
    def __init__(self,pieces,textBrowser,seach_robot,label_4):
        self.pieces = pieces
        self.textBrowser = textBrowser
        self.seach_robot = seach_robot
        self.seach_robot_id = -1
        self.label_4 = label_4
        super(SearchRobotThread, self).__init__()

    def run(self):
        self.textBrowser.append("探测机器人开始工作......")
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        #八个方向，随机一个前进，遇到边界后转向，碰到障碍绕开，碰到钻石获取
        directions = [(-1,0),(1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
        row_num = len(region)
        col_num = len(region[0])
        #当前位置
        x = self.seach_robot[0]
        y = self.seach_robot[1]
        self.seach_robot_id = region[x][y][3]
        last_direction = -1  # 记录上一次走的方向，以免走回头路
        while 1:
            sleep(0.3)
            #循环判断是否能走
            while 1:
                temp = random.randint(0, 7)
                #判断是否走回头路
                if temp % 2 == 0 and last_direction == temp+1:
                    continue
                elif temp % 2 == 1 and last_direction == temp-1:
                    continue
                #边界
                if x + directions[temp][0] < 0 or x + directions[temp][0] >= row_num or y + directions[temp][1] < 0 or y + directions[temp][1] >= col_num:
                    print("到边界了！")
                #障碍
                elif region[x + directions[temp][0]][y + directions[temp][1]][2] == 2:
                    print("有障碍物!")
                #探测机器人
                elif region[x + directions[temp][0]][y + directions[temp][1]][2] == 4:
                    print("这是采矿机器人！")
                # 钻石
                elif region[x + directions[temp][0]][y + directions[temp][1]][2] == 1:
                    row = x + directions[temp][0]
                    col = y + directions[temp][1]
                    pos_row = region[row][col][0]
                    pos_col = region[row][col][1]
                    #记录钻石位置
                    if (row,col) not in diamonds_pos:
                        global search_diamonds
                        search_diamonds += 1
                        self.label_4.setText('已探测矿产：{}个'.format(search_diamonds))
                        diamonds_pos.append((row,col))
                        self.textBrowser.append("SearchRobot: ({},{})这里有钻石！".format(pos_row,pos_col))
                        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                    # 结束循环
                else:
                    region[x][y][3] = -1  # 重置当前位置id
                    region[x][y][2] = 0  # 重置当前位置资源
                    x = x + directions[temp][0]
                    y = y + directions[temp][1]
                    # 移动到该位置
                    self.pieces[self.seach_robot_id].setGeometry(region[x][y][0], region[x][y][1], 30, 30)
                    region[x][y][3] = self.seach_robot_id  # 重置当前位置id
                    region[x][y][2] = 3  # 重置当前位置资源
                    last_direction = temp
                    # 结束循环
                    break

class WorkRobotThread(QThread):
    _signal = pyqtSignal(list)

    def __init__(self,pieces,textBrowser,work_robot,label_4):
        self.pieces = pieces
        self.textBrowser = textBrowser
        self.work_robot = work_robot
        self.work_robot_id = -1
        self.label_4 = label_4
        super(WorkRobotThread, self).__init__()

    def take_first(self,elem):
        return elem[0]

    def run(self):
        #轮询判断，如果diamonds_pos不为空则开始工作
        while 1:
            sleep(1)
            global diamonds_pos
            if not len(diamonds_pos):
                continue
            target_pos = diamonds_pos[0]
            del diamonds_pos[0]
            global region
            self.textBrowser.append("采矿机器人开始工作......目标{}".format(region[target_pos[0]][target_pos[1]][:2]))
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
            row_num = len(region)
            col_num = len(region[0])
            #当前位置
            x = self.work_robot[0]
            y = self.work_robot[1]
            self.work_robot_id = region[x][y][3]
            # 八个方向，每次选择离钻石最近的那个方向，如果有障碍则选择第二近方向，依此类推
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            t = 0
            while 1:
                # 计算下一步离目标的距离列表
                distances = []
                for i in range(8):
                    row_temp = x + directions[i][0]
                    col_temp = y + directions[i][1]
                    distance = ((row_temp - target_pos[0]) ** 2 + (col_temp - target_pos[1]) ** 2) ** 0.5
                    distances.append((distance, i))
                # 排序
                print(distances)
                distances.sort(key=self.take_first)
                print(distances)
                sleep(0.5)
                #循环判断是否能走
                for i in range(8):
                    direction = directions[distances[i][1]]
                    #边界
                    if x + direction[0] < 0 or x + direction[0] >= row_num or y + direction[1] < 0 or y + direction[1] >= col_num:
                        print("到边界了！")
                    #障碍
                    elif region[x + direction[0]][y + direction[1]][2] == 2:
                        print("有障碍物!")
                    #探测机器人
                    elif region[x + direction[0]][y + direction[1]][2] == 3:
                        print("这是探测机器人！")
                    #钻石
                    elif region[x + direction[0]][y + direction[1]][2] == 1:
                        #判断是不是目标钻石，如果不是就跳过
                        if x + direction[0] != target_pos[0] or y + direction[1] != target_pos[1]:
                            continue
                        region[x][y][3] = -1 #重置当前位置id
                        region[x][y][2] = 0 #重置当前位置资源
                        x = x + direction[0]
                        y = y + direction[1]
                        #获取钻石
                        global get_diamonds
                        get_diamonds += 1
                        #self.label_4.setText('已探测矿产：{}个'.format(get_diamonds))
                        self.textBrowser.append("钻石+1")
                        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
                        #钻石图标消失
                        diamond_id = region[x][y][3]
                        self.pieces[diamond_id].setPixmap(QPixmap(""))
                        #移动到该位置
                        self.work_robot = [x,y]
                        self.pieces[self.work_robot_id].setGeometry(region[x][y][0], region[x][y][1], 30, 30)
                        region[x][y][3] = self.work_robot_id  # 重置当前位置id
                        region[x][y][2] = 4  # 重置当前位置资源
                        #结束循环
                        t = 1
                        break
                    else:
                        region[x][y][3] = -1  # 重置当前位置id
                        region[x][y][2] = 0  # 重置当前位置资源
                        x = x + direction[0]
                        y = y + direction[1]
                        # 移动到该位置
                        self.work_robot = [x, y]
                        self.pieces[self.work_robot_id].setGeometry(region[x][y][0], region[x][y][1], 30, 30)
                        region[x][y][3] = self.work_robot_id  # 重置当前位置id
                        region[x][y][2] = 4  # 重置当前位置资源
                        # 结束循环
                        break
                #如果取到钻石，结束该次任务
                if t:
                    break

# 重新定义Label类
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()


class MyMainForm(QMainWindow, Ui_MarsRobot):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #初始化钻石，障碍，机器人的id
        self.diamond_id = []
        self.hinder_id = []
        self.search_robot_id = []
        self.work_robot_id = []
        #建立开始按钮链接
        self.pushButton.clicked.connect(self.begin)
        #导入图片
        self.rock= QPixmap('./designer/image/rock-removebg-preview.png')
        self.valuable_rock = QPixmap('./designer/image/valuableRock-removebg-preview.png')
        self.search = QPixmap('./designer/image/search-removebg-preview.png')
        self.work = QPixmap('./designer/image/work-removebg-preview.png')
        # 新建225个标签，准备在标签上绘制资源，机器人
        self.pieces = [LaBel(self) for i in range(225)]
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变
        #初始化采矿区域坐标，左上（71，100）右上（578 100）右下（578 568）左下（71 568）
        self.size = 14
        pos = [71,100,0,-1]#四个个元素，分别是x，y坐标，该坐标对应的资源（0表示空，1表示钻石，2表示障碍，3表示探测机器人，4表示工作机器人），该资源的id
        global region
        region = []
        for i in range(self.size-1):
            temp = []
            for j in range(self.size):
                temp.append(deepcopy(pos))
                pos[0] += 37
            region.append(deepcopy(temp))
            pos[1] += 34
            pos[0] = 71
        #print(self.region)

    #初始化钻石，障碍，机器人
    def begin(self):
        global region
        diamonds_num = 20
        hinders_num = 10
        search_robots_num = 1
        work_robots_num = 2
        self.label_2.setText('采矿Robot的个数：{}个'.format(work_robots_num))
        self.label_3.setText('探测Robot的个数：{}个'.format(search_robots_num))
        tmp = [diamonds_num,hinders_num,search_robots_num,work_robots_num]
        diamond = []
        hinder = []
        search_robot = [[0,0]]
        work_robot = [[12,13],[12,0]]
        j = 0
        while j < 2:
            #随机生成钻石的位置
            for i in range(tmp[j]):
                temp = []
                temp.append(random.randint(0,self.size-2))
                temp.append(random.randint(0,self.size-1))
                while self.judge(temp,diamond,hinder,search_robot,work_robot):
                    temp.clear()
                    temp.append(random.randint(0, self.size - 2))
                    temp.append(random.randint(0, self.size - 1))
                if j == 0:
                    diamond.append(temp)
                elif j == 1:
                    hinder.append(temp)
                elif j == 2:
                    search_robot.append(temp)
                else:
                    work_robot.append(temp)
            j += 1
        # print("diamond:{}".format(diamond))
        # print("hinder:{}".format(hinder))
        # print("search_robot:{}".format(search_robot))
        # print("work_robot:{}".format(work_robot))
        #显示钻石，障碍，机器人
        for i in range(diamonds_num):
            self.pieces[i].setPixmap(self.valuable_rock)
            self.pieces[i].setGeometry(region[diamond[i][0]][diamond[i][1]][0],
                                       region[diamond[i][0]][diamond[i][1]][1], 30, 30)  # 设置位置，大小
            region[diamond[i][0]][diamond[i][1]][2] = 1  # 标记为钻石
            region[diamond[i][0]][diamond[i][1]][3] = i# 记录id
        for i in range(hinders_num):
            self.pieces[diamonds_num+i].setPixmap(self.rock)
            self.pieces[diamonds_num+i].setGeometry(region[hinder[i][0]][hinder[i][1]][0],
                                       region[hinder[i][0]][hinder[i][1]][1], 30, 30)
            region[hinder[i][0]][hinder[i][1]][2] = 2  # 标记为障碍
            region[hinder[i][0]][hinder[i][1]][3] = diamonds_num+i# 记录id
        for i in range(search_robots_num):
            self.pieces[diamonds_num+hinders_num+i].setPixmap(self.search)
            self.pieces[diamonds_num+hinders_num+i].setGeometry(region[search_robot[i][0]][search_robot[i][1]][0],
                                       region[search_robot[i][0]][search_robot[i][1]][1], 30, 30)
            region[search_robot[i][0]][search_robot[i][1]][2] = 3 # 标记为搜索机器人
            region[search_robot[i][0]][search_robot[i][1]][3] = diamonds_num+hinders_num+i# 记录id
        for i in range(work_robots_num):
            self.pieces[diamonds_num+hinders_num+search_robots_num+i].setPixmap(self.work)
            self.pieces[diamonds_num+hinders_num+search_robots_num+i].setGeometry(region[work_robot[i][0]][work_robot[i][1]][0],
                                       region[work_robot[i][0]][work_robot[i][1]][1], 30, 30)
            region[work_robot[i][0]][work_robot[i][1]][2] = 4 #标记为工作机器人
            region[work_robot[i][0]][work_robot[i][1]][3] = diamonds_num+hinders_num+search_robots_num+i# 记录id

        #初始化仓库
        depository = LaBel(self)
        depository.setVisible(True)  # 图片可视
        depository.setScaledContents(True)  # 图片大小根据标签大小可变
        repository = QPixmap('./designer/image/repository-removebg-preview.png')
        depository.setPixmap(repository)
        depository.setGeometry(region[12][0][0],region[12][0][1]+34, 30, 30)
        #开启搜索机器人线程
        self.search_robot_thread = SearchRobotThread(self.pieces,self.textBrowser,search_robot[0],self.label_4)
        self.search_robot_thread.start()
        # #开启工作机器人线程
        self.work_robot_thread = WorkRobotThread(self.pieces,self.textBrowser,work_robot[0],self.label_4)
        self.work_robot_thread.start()
        self.work_robot_thread_1 = WorkRobotThread(self.pieces, self.textBrowser,
                                                 work_robot[1], self.label_4)
        self.work_robot_thread_1.start()


    # 判断随机的位置是否已有物体
    def judge(self,temp,diamond,hinder,search_robot,work_robot):
        if len(diamond):#当diamond列表不为空时
            for i in range(len(diamond)):
                if diamond[i][0] == temp[0] and diamond[i][1] == temp[1]:
                    return 1
        if len(hinder):
            for i in range(len(hinder)):
                if hinder[i][0] == temp[0] and hinder[i][1] == temp[1]:
                    return 1
        if len(search_robot):
            for i in range(len(search_robot)):
                if search_robot[i][0] == temp[0] and search_robot[i][1] == temp[1]:
                    return 1
        if len(work_robot):
            for i in range(len(work_robot)):
                if work_robot[i][0] == temp[0] and work_robot[i][1] == temp[1]:
                    return 1
        #四个列表判断都没有问题，返回0
        return 0

    def mousePressEvent(self, e):
        print(e.x(),e.y())

if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    #设置标题图标
    myWin.setWindowIcon(QIcon('./work.ico'))
    #设置标题
    myWin.setWindowTitle('火星探矿机器人')
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
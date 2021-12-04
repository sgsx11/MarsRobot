## 火星探矿机器人

### 一、问题描述

#### 1.1需求分析

“火星探矿机器人”旨在要开发若干个自主机器人，将其送到火星上去搜寻和采集火星上的矿产资源

火星环境对于开发者和自主机器人而言事先不可知,但是可以想象火星表面会有多样化的地形情况,如河流、巨石、凹坑等,机器人在运动过程中会遇到各种障碍;另外,火星

上还可能存在一些未知的动态因素(如风暴等),会使得环境的状况发生变化。概括起来，火星环境具有开放、动态、不可知,难控等特点。
为了简化案例的开发和演示,可以将机器人探矿的区域(即机器人的运动环境)简化和抽象成m*m的单元格,每个单元格代表某个火星区域,火星矿产分布在这些单元格中,同时这些单元格中还存在阻碍机器人运行的障碍物。探矿机器人在这些网格中运动，根据感知到的网格环境信息自主地决定自身的行为。如果所在的单元格有矿产,则采集矿产;如果探测到附近的单元格存在矿产,则移动到该单元格;如果周围的单元格存在障碍物﹐则避开这些障碍物。环境网格有两个特殊的单元格:一个是矿产堆积单元格,用于存放机器人采集到的矿产,如图6-21中的左下角;另一个是能量补充单元格,机器人可以从该单元格获得能量。

#### 1.2 功能

下面通过多个场景描述机器人如何在上述火星环境下采集火星矿产,这些场景分别描述了机器人采矿的不同工作模式,反映了实现这些自主机器人的不同难易程度。

##### 场景一:独立采集矿产。

在该场景中,有多个自主机器人参与到火星矿产的采集工作中,每个机器人都有移动,探测﹑采集,卸载的能力,它们在火星表面随机移动,根据其所在位置探测到的矿产信息和障碍物等环境信息自主地实施行为。但是,这些机器人都是单独工作,它们之间没有任何交互与合作。因此,可以将本场景中的每个机器人都抽象和设计为自主的 Agent

##### 场景二:合作采集矿产。

在该场景中,有多个自主机器人参与到火星矿产的采集工作中,每个机器人都有移动、探测,采集,卸载的能力,它们在完成各自矿产采集任务的同时,相互之间还进行交互和合作,以更高效地开展工作。例如,某个机器人探测到大片的矿产信息,那么它可以将该信息告诉给其他机器人,或者请求其他机器人来该区域采矿。因此,可以将本场景中的机器人抽象和设计为由多个自主Agent所构成的多Agent系统。该系统的设计和实现不仅要考虑到各个自主Agent,还要考虑到这些Agent之间的交互和协同。

##### 场景三:多角色合作采集矿产。

在该场景中,有多个具有不同职责,扮演不同角色的机器人参与到火星矿产的采集工作中,每类机器人承担矿产采集中的某项工作(如探测,采集),它们之间通过交互和合作共同完成矿产采集任务﹐即该场景有多种类型的机器人,包括:①采矿机器人﹐采集矿产并将其运送到指定区域;②探测机器人,负责探测矿产并将其探测到的矿产信息通知给采矿机器人。因此,可以将本场景中的机器人抽象和设计为由多个自主Agent所构成的多Agent系统。该系统的设计和实现不仅要考虑到各个自主Agent,还要考虑到这些Agent之间的交互和协同。显然,该场景比前一个场景更复杂,它涉及的Agent类型和数量、交互和合作关系等更多。

### 二、功能实现

#### 2.1独立采集矿产
![在这里插入图片描述](https://img-blog.csdnimg.cn/c2c7a8a69b054f14a43120b266b632d4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAc2dzeDEx,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/d3d15e4df4a549e5b01b4c6d8eefed69.gif#pic_center)


#### 2.2合作采集矿产
![在这里插入图片描述](https://img-blog.csdnimg.cn/9592a123d9fa444c8bd844c0ebce125b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAc2dzeDEx,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/0f9ebfc4665f4651878c874241de205c.gif#pic_center)


#### 2.3多角色合作采集矿产

##### 2.3.1 探测机器人
![在这里插入图片描述](https://img-blog.csdnimg.cn/71080271e6554083b3e1eef833d2b425.gif#pic_center)



##### 2.3.2 采矿机器人

![在这里插入图片描述](https://img-blog.csdnimg.cn/9e49b2f2d4f04df8b3c885d341dce939.gif#pic_center)

### 三、代码

#### 3.1 探测机器人线程类

```python
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
```



#### 3.2 采矿机器人线程类

```python
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

```



#### 3.3 start.py

```python
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
```

#### 3.4 Mars_robot_ui.py

```python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './designer/Mars_robot_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MarsRobot(object):
    def setupUi(self, MarsRobot):
        MarsRobot.setObjectName("MarsRobot")
        MarsRobot.resize(821, 743)
        MarsRobot.setMinimumSize(QtCore.QSize(821, 743))
        MarsRobot.setMaximumSize(QtCore.QSize(821, 743))
        self.centralwidget = QtWidgets.QWidget(MarsRobot)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(49, 79, 551, 511))
        self.widget.setMinimumSize(QtCore.QSize(551, 511))
        self.widget.setMaximumSize(QtCore.QSize(551, 511))
        self.widget.setStyleSheet("background-image: url(:/image/image/chessboard.png);\n"
"background-color: rgba(255, 255, 255, 150);")
        self.widget.setObjectName("widget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 600, 761, 111))
        self.textBrowser.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 30, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 30, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("\n"
"background-color: rgba(255, 255, 255, 150);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 40, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 80, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(-1, -1, 821, 743))
        self.widget_2.setMinimumSize(QtCore.QSize(821, 743))
        self.widget_2.setMaximumSize(QtCore.QSize(821, 743))
        self.widget_2.setStyleSheet("background-image: url(:/image/image/bg.jpeg);")
        self.widget_2.setObjectName("widget_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(610, 30, 201, 561))
        self.textBrowser_2.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 120, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(620, 160, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(620, 200, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(630, 250, 51, 51))
        self.widget_3.setStyleSheet("background-image: url(:/image/image/search-removebg-preview.png);")
        self.widget_3.setObjectName("widget_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(690, 250, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setGeometry(QtCore.QRect(630, 310, 51, 51))
        self.widget_4.setStyleSheet("background-image: url(:/image/image/work-removebg-preview.png);")
        self.widget_4.setObjectName("widget_4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(690, 310, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.widget_5 = QtWidgets.QWidget(self.centralwidget)
        self.widget_5.setGeometry(QtCore.QRect(630, 370, 51, 51))
        self.widget_5.setStyleSheet("background-image: url(:/image/image/rock-removebg-preview.png);")
        self.widget_5.setObjectName("widget_5")
        self.widget_6 = QtWidgets.QWidget(self.centralwidget)
        self.widget_6.setGeometry(QtCore.QRect(630, 430, 51, 51))
        self.widget_6.setStyleSheet("background-image: url(:/image/image/valuableRock-removebg-preview.png);")
        self.widget_6.setObjectName("widget_6")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(690, 370, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(690, 430, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(630, 650, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(590, 685, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(600, 615, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("")
        self.label_12.setObjectName("label_12")
        self.widget_7 = QtWidgets.QWidget(self.centralwidget)
        self.widget_7.setGeometry(QtCore.QRect(610, 640, 43, 43))
        self.widget_7.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"background-image: url(:/image/image/avator2.png);")
        self.widget_7.setObjectName("widget_7")
        self.widget_8 = QtWidgets.QWidget(self.centralwidget)
        self.widget_8.setGeometry(QtCore.QRect(630, 490, 51, 51))
        self.widget_8.setStyleSheet("background-image: url(:/image/image/repository-removebg-preview.png);")
        self.widget_8.setObjectName("widget_8")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(690, 490, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.widget_2.raise_()
        self.textBrowser_2.raise_()
        self.widget.raise_()
        self.textBrowser.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.widget_3.raise_()
        self.label_6.raise_()
        self.widget_4.raise_()
        self.label_7.raise_()
        self.widget_5.raise_()
        self.widget_6.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.widget_7.raise_()
        self.widget_8.raise_()
        self.label_13.raise_()
        MarsRobot.setCentralWidget(self.centralwidget)

        self.retranslateUi(MarsRobot)
        QtCore.QMetaObject.connectSlotsByName(MarsRobot)

    def retranslateUi(self, MarsRobot):
        _translate = QtCore.QCoreApplication.translate
        MarsRobot.setWindowTitle(_translate("MarsRobot", "MainWindow"))
        self.pushButton.setText(_translate("MarsRobot", "开始"))
        self.pushButton_2.setText(_translate("MarsRobot", "设置"))
        self.label.setText(_translate("MarsRobot", "状态："))
        self.label_2.setText(_translate("MarsRobot", "采矿Robot的个数：0个"))
        self.label_3.setText(_translate("MarsRobot", "探测Robot的个数：0个"))
        self.label_4.setText(_translate("MarsRobot", "已探测矿产：0个"))
        self.label_5.setText(_translate("MarsRobot", "图例说明："))
        self.label_6.setText(_translate("MarsRobot", "探测机器人"))
        self.label_7.setText(_translate("MarsRobot", "采矿机器人"))
        self.label_8.setText(_translate("MarsRobot", "障碍物"))
        self.label_9.setText(_translate("MarsRobot", "矿石"))
        self.label_10.setText(_translate("MarsRobot", "     作者： sgsx"))
        self.label_11.setText(_translate("MarsRobot", "联系方式：1287997451@qq.com"))
        self.label_12.setText(_translate("MarsRobot", "版本 1.1.0 - 2021年12月"))
        self.label_13.setText(_translate("MarsRobot", "仓库"))
import mars_robot_qrc_rc

```

### 四、Github
完整代码已上传Github，有需要可以自取：[https://github.com/sgsx11/MarsRobot/](https://github.com/sgsx11/MarsRobot/)

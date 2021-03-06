
import tkinter as tk
import tkinter.messagebox as msg
from PIL import Image, ImageTk
import pygame
import random
import numpy  as np

class MainWindow():
    _gameWidth = 800
    _gameHeight = 750
    _map = [] # 游戏地图数组
    _gameSize = 10 # 游戏尺寸： 10*10
    _iconCount = _gameSize * _gameSize / 4 # 小头像数量25个
    _iconWidth = 70
    _iconHeight = 70
    _margin = 25
    _icons = []
    _isFirst = True
    _isGameStart = False

    # 连通类型
    NONE_LINK = 0
    LINK_LINK = 1
    NEIGHBOR_LINK = 10
    LINE_LINK = 11
    ONE_LINK = 12
    TWO_LINK = 13

    EMPTY = -1

    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title('连连看')
        # self._gameWidth = 800
        # self._gameHeight = 750
        self.window.minsize(self._gameWidth, self._gameHeight)
        self.windowCenter(self._gameWidth, self._gameHeight)


        self.addComponents()

        # 播放音乐
        pygame.mixer.init()
        self.playMusic(music='audio/melodic minor.mp3')

        # 绘制游戏背景
        self.background_im = False # 定义外部图片
        self.drawBackground()

        # 初始化所有小头像
        self.extractSmallIconList()

        # 进入消息循环
        self.window.mainloop()


    # 初始化地图数组
    def initMap(self):
        records = []
        for i in range(0, int(self._iconCount)):
            for j in range(0, 4):
                records.append(i)
        random.shuffle(records) # 打乱数组
        # 将一维数组转化为2维数组
        self._map = np.array(records).reshape(10, 10)

    # 点位的原点坐标 = 边框 + 横向/纵向排位*小图片宽/高
    # 获取row的x轴的起始坐标
    def getX(self, row):
        return self._margin + row * self._iconWidth

    # 获取column的y轴的起始坐标
    def getY(self, column):
        return self._margin + column * self._iconHeight

    # 获取row, column这个点位的左上角的原点坐标
    def getOriginCoordinate(self, row, column):
        return self.getX(row), self.getY(column)

    # 获取玩家点击的xy坐标在地图上的点位
    def getGamePoint(self, x, y):
        for row in range(0, self._gameSize):
            x1 = self.getX(row)
            x2 = self.getX(row + 1)
            if x >= x1 and x < x2:
                point_row = row

        for column in range(0, self._gameSize):
            j1 = self.getY(column)
            j2 = self.getY(column +1)
            if y >= j1 and y < j2:
                point_column = column

        return Point(point_row, point_column)

    # 根据地图绘制所有小头像
    def drawMap(self):
        for row in range(0, self._gameSize):
            for column in range(0, self._gameSize):
                x, y = self.getOriginCoordinate(row, column)
                self.canvas.create_image((x, y), image=self._icons[self._map[row][column]], anchor='nw', tags='image%d%d'%(row,column))

    def windowCenter(self, width, height):
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, screenwidth/2 - width/2, screenheight/2 - height/2)
        self.window.geometry(size)

    def addComponents(self):
        # 创建菜单
        self.menubar = tk.Menu(self.window, bg='lightgrey', fg='black')
        self.file_menu = tk.Menu(self.menubar, bg='lightgrey', fg='black')
        self.file_menu.add_command(label='新游戏', command=self.file_menu_clicked, accelerator="Ctrl+N")
        self.menubar.add_cascade(label="游戏", menu=self.file_menu) # 级联关系
        self.window.configure(menu=self.menubar)
        # 添加canvas背景画布
        self.canvas = tk.Canvas(self.window, bg='white', width=self._gameWidth, height=self._gameHeight)
        self.canvas.pack()
        # 绑定鼠标动作
        self.canvas.bind('<Button-1>', self.clickCanvas)

    def clickCanvas(self, event):
        if self._isGameStart:
            point = self.getGamePoint(event.x, event.y)
            if self._isFirst:
                print("第一次点击")
                self.playMusic("audio/click1.mp3")
                self._isFirst = False
                self.drawSelectedArea(point)
                self._formerPoint = point # 记录上一次点位
            else:
                print("第二次点击")
                self.playMusic("audio/click2.mp3")
                if point.isEquals(self._formerPoint):
                    print("2次点击的点位相同")
                    self.canvas.delete('rectYellowOne')
                    self._isFirst = True
                else:
                    print("2次点击的点位不同")
                    # type = self.getLinkType(self._formerPoint, point)
                    type = self.getLinkTypeByAStar(self._formerPoint, point)
                    if type['type'] != self.NEIGHBOR_LINK:
                        self.clearLinkedBlocks(self._formerPoint, point)
                        self.canvas.delete('rectYellowOne')
                        self._isFirst = True

    # 消除2个点位的小头像
    def clearLinkedBlocks(self, p1, p2):
        print("消除选中的2个点位上的小头像")
        self.canvas.delete('image%d%d'%(p1.row, p1.column))
        self.canvas.delete('image%d%d'%(p2.row, p2.column))
        self._map[p1.row][p1.column] = self.EMPTY
        self._map[p2.row][p2.column] = self.EMPTY
        self.playMusic("audio/link.mp3")

    # 通过a星寻路算法判断
    def getLinkTypeByAStar(self, p1, p2):
        if self._map[p1.row][p1.column] != self._map[p2.row][p2.column]:
            return {'type': self.NONE_LINK}
        startNode = Node(p1, p2)
        endNode = Node(p2, p2)
        pathList = AStar(self._map, startNode, endNode, self.EMPTY).start()
        if pathList:
            # 绘制路径
            for node in pathList:
                self.drawPathArea(node.point)
            return {'type': self.LINK_LINK}
        else:
            return {'type': self.NONE_LINK}

    # 取得2个点位的连通情况
    def getLinkType(self, p1, p2):
        if self._map[p1.row][p1.column] != self._map[p2.row][p2.column]:
            return {'type': self.NONE_LINK}
        if self.isNeighbor(p1, p2):
            print("相邻连通")
            return {'type': self.NEIGHBOR_LINK}
        elif self.isStraightLink(p1, p2):
            print("直连")
            return {'type': self.LINE_LINK}
        elif self.isOneConrnerLink(p1, p2):
            print("一个角相连")
            return {'type': self.ONE_LINK}
        elif self.isTwoConrnerLink(p1, p2):
            print("2个角相连")
            return {'type': self.TWO_LINK}

    # 判断2个点位是否相邻
    def isNeighbor(self, p1, p2):
        # 垂直方向
        if p1.column == p2.column:
            # 大小判断
            if p2.row < p1.row:
                if p2.row + 1 == p1.row:
                    return True
            else:
                if p1.row + 1 == p2.row:
                    return True
        # 水平方向
        if p1.row == p2.row:
            # 大小判断
            if p2.column < p1.column:
                if p2.column + 1 == p1.column:
                    return True
            else:
                if p1.column + 1 == p2.column:
                    return True

    # 判断2个点位是否直连
    def isStraightLink(self, p1, p2):
        # 水平方向判断
        if p1.row == p2.row:
            if p1.column > p2.column:
                start = p2.column
                end = p1.column
            else:
                start = p1.column
                end = p2.column
            for column in range(start + 1, end):
                if self._map[p1.row][column] != self.EMPTY:
                    return False
            return True
        # 垂直方向判断
        if p1.column == p2.column:
            if p1.row > p2.row:
                start = p2.row
                end = p1.row
            else:
                start = p1.row
                end = p2.row
            for row in range(start + 1, end):
                if self._map[row][p1.column] != self.EMPTY:
                    return False
            return True

    # 一个角相连
    def isOneConrnerLink(self, p1, p2):
        pointCorner = Point(p1.row, p2.column)
        if self.isEmptyInMap(pointCorner) and self.isStraightLink(p1, pointCorner) and self.isStraightLink(p2, pointCorner):
            return pointCorner
        pointCorner = Point(p2.row, p1.column)
        if self.isEmptyInMap(pointCorner) and self.isStraightLink(p1, pointCorner) and self.isStraightLink(p2, pointCorner):
            return pointCorner
        return False

    # 2个角相连
    def isTwoConrnerLink(self, p1, p2):
        # 水平方向
        for column in range(0, self._gameSize):
            if column == p1.column or column == p2.column:
                continue
            pointConrner1 = Point(p1.row, column)
            pointConrner2 = Point(p2.row, column)
            if self.isStraightLink(p1, pointConrner1) and self.isStraightLink(pointConrner1, pointConrner2) and self.isStraightLink(pointConrner2, p2) and self.isEmptyInMap(pointConrner1) and self.isEmptyInMap(pointConrner2):
                return {'p1': pointConrner1, 'p2': pointConrner2}
        # 垂直方向
        for row in range(0, self._gameSize):
            if row == p1.row or row == p2.row:
                continue
            pointConrner1 = Point(row, p1.column)
            pointConrner2 = Point(row, p2.column)
            if self.isStraightLink(p1, pointConrner1) and self.isStraightLink(pointConrner1,
                                                                              pointConrner2) and self.isStraightLink(
                    pointConrner2, p2) and self.isEmptyInMap(pointConrner1) and self.isEmptyInMap(pointConrner2):
                return {'p1': pointConrner1, 'p2': pointConrner2}
        return False

    # 判断一个点位是否为空
    def isEmptyInMap(self, point):
        if self._map[point.row, point.column] == self.EMPTY:
            return True
        else:
            return False

    # 选择的点位标记红框
    def drawSelectedArea(self, point):
        lt_x, lt_y = self.getOriginCoordinate(point.row, point.column)
        rb_x, rb_y = self.getOriginCoordinate(point.row + 1, point.column + 1)
        self.canvas.create_rectangle(lt_x, lt_y, rb_x, rb_y, outline='yellow', tags='rectYellowOne')


    # 路径点位标记红
    def drawPathArea(self, point):
        lt_x, lt_y = self.getOriginCoordinate(point.row, point.column)
        rb_x, rb_y = self.getOriginCoordinate(point.row + 1, point.column + 1)
        self.canvas.create_rectangle(lt_x, lt_y, rb_x, rb_y, outline='red', tags='path%d%d' %(point.row, point.column))

    def file_menu_clicked(self):
        self.stopMusic()
        self.initMap()
        print("游戏地图:")
        print(self._map)
        self.drawMap()

        self._isGameStart = True


    def playMusic(self, music, volume=0.5):
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def stopMusic(self):
        pygame.mixer.music.stop()

    def drawBackground(self):
        pil_image = Image.open(r'images/bg.jpg')
        w, h = pil_image.size
        pil_image_resized = self.resize(w, h, self._gameWidth, self._gameHeight, pil_image)
        self.background_im = ImageTk.PhotoImage(pil_image_resized)
        self.canvas.create_image((0, 0), anchor='nw', image=self.background_im)

    def extractSmallIconList(self):
        for i in range(1, 26):
            pil_image = Image.open(r'images/role{}.png'.format(i))
            w, h = pil_image.size
            pil_image_resized = self.resize(w, h, self._iconWidth, self._iconHeight, pil_image)
            self._icons.append(ImageTk.PhotoImage(pil_image_resized))

    def resize(self, w, h, w_box, h_box, pil_image):
        '''
        resize a pil_image object so it will fit into
        a box of size w_box times h_box, but retain aspect ratio
        对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
        '''
        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

# 游戏中的点位
class Point():
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def isEquals(self, point):
        if self.row == point.row and self.column == point.column:
            return True
        else:
            return False

class Node():
    def __init__(self, point, endPoint):
        self.point = point  # 点位
        self.father = None  # 父节点
        self.g = 0  # 到起点的步数
        self.h = abs(endPoint.row - point.row) + abs(endPoint.column - point.column)  # 到终止节点的估算步数（不考虑障碍物）

# A星寻路算法
# 1. 将起点A加入open list中
# 2. 查看起点A相邻节点，把其中可走节点加入open list中
# 3. 把A从open list中移到close list中
# 4. 从open list中寻找代价最低节点
# 5. 检查代价最低节点相邻节点是否可行
# 6. 重复上面的操作知道结束

class AStar():
    def __init__(self, map, startNode, endNode, passTag):
        self.open_list = []  # 待探索节点列表
        self.close_list = []  # 已探索节点列表
        self.map = map  # 地图
        self.startNode = startNode  # 开始节点
        self.endNode = endNode  # 终止节点
        self.passTag = passTag  # 可行走标记

    def start(self):
        if self.map[self.endNode.point.row][self.endNode.point.column] == self.passTag:
            return
        print('起点:', self.startNode.point.column, self.startNode.point.row)
        print('终点:', self.endNode.point.column, self.endNode.point.row)
        # 将起点加入openlist
        self.open_list.append(self.startNode)
        while (True):
            # 从openlist中查找代价最低的节点
            minFNode = self.findMinFNode()
            # 从openlist中移除并加入closelist
            self.open_list.remove(minFNode)
            self.close_list.append(minFNode)
            # 查找4个邻居节点
            self.searchNearNode(minFNode, 0, -1)  # 向上查找
            self.searchNearNode(minFNode, 1, 0)  # 向右查找
            self.searchNearNode(minFNode, 0, 1)  # 向下查找
            self.searchNearNode(minFNode, -1, 0)  # 向左查找
            # 判断是否终止
            endNode = self.nodeInCloseList(self.endNode)
            if endNode:
                print("2个节点是连通的")
                path = []
                node=  endNode
                while not node.point.isEquals(self.startNode.point):
                    path.append(node)
                    if node.father:
                        node = node.father
                path.reverse()
                return path
            if len(self.open_list) == 0:
                print("2个节点不连通")
                return None

    # 查找邻居节点
    def searchNearNode(self, minFNode, offsetX, offsetY):
        nearPoint = Point(minFNode.point.row + offsetX, minFNode.point.column + offsetY)
        nearNode = Node(nearPoint, self.endNode.point)
        if nearNode.point.row < 0 or nearNode.point.column < 0 or nearNode.point.row > len(self.map) -1 or nearNode.point.column > len(self.map[0] -1):
            print("越界")
            return
        # 障碍物检查
        if self.map[nearNode.point.row][nearNode.point.column] != self.passTag and not nearNode.point.isEquals(self.endNode.point):
            print("障碍")
            return
        # 是否在close list中
        if self.nodeInCloseList(nearNode):
            print("在closelist中")
            return
        print("找到可行节点")
        if not self.nodeInOpenList(nearNode):
            self.open_list.append(nearNode)
            nearNode.father = minFNode
            step = 1
            node = nearNode.father
            while not node.point.isEquals(self.startNode.point):
                step += 1
                node = node.father
            nearNode.g = step
        return nearNode

    # 节点是否在close list中
    def nodeInCloseList(self, nearNode):
        for node in self.close_list:
            if node.point.isEquals(nearNode.point):
                return node
        return False

    # 节点是否在open list中
    def nodeInOpenList(self, nearNode):
        for node in self.open_list:
            if node.point.isEquals(nearNode.point):
                return node
        return False

    # 查找代价最低节点
    def findMinFNode(self):
        oneNode = self.open_list[0]
        for node in self.open_list:
            if node.g + node.h < oneNode.g + oneNode.h:
                oneNode = node
        return oneNode


if __name__ == '__main__':
    MainWindow()
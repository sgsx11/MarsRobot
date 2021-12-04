# MarsRobot
“火星探矿机器人”旨在要开发若干个自主机器人，将其送到火星上去搜寻和采集火星上的矿产资源  火星环境对于开发者和自主机器人而言事先不可知,但是可以想象火星表面会有多样化的地形情况,如河流、巨石、凹坑等,机器人在运动过程中会遇到各种障碍;另外,火星  上还可能存在一些未知的动态因素(如风暴等),会使得环境的状况发生变化。概括起来，火星环境具有开放、动态、不可知,难控等特点。 为了简化案例的开发和演示,可以将机器人探矿的区域(即机器人的运动环境)简化和抽象成m*m的单元格,每个单元格代表某个火星区域,火星矿产分布在这些单元格中,同时这些单元格中还存在阻碍机器人运行的障碍物。探矿机器人在这些网格中运动，根据感知到的网格环境信息自主地决定自身的行为。如果所在的单元格有矿产,则采集矿产;如果探测到附近的单元格存在矿产,则移动到该单元格;如果周围的单元格存在障碍物﹐则避开这些障碍物。环境网格有两个特殊的单元格:一个是矿产堆积单元格,用于存放机器人采集到的矿产,如图6-21中的左下角;另一个是能量补充单元格,机器人可以从该单元格获得能量。

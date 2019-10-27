# **h-tree复现**

### **un-buffered H-tree**

电路描述：该电路来自ispd2009的example电路，有81个sink。

复现说明：原文中是使用H-tree驱动mesh的方式来实现h-tree。我用h-tree驱动子树的方式实现。

##### **2级时钟树**

![2level](/Users/mac/Desktop/2level.png)

##### **3级时钟树**

![3level](/Users/mac/Desktop/3level.png)



### **buffered H-tree**

buffered H-tree相对简单，就是在分支处插buffer，具体实现及实验数据的结果还需要依赖buffer单元库。


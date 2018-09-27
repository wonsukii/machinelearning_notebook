# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.5.2
# ---

# # Softmax & 交叉熵代价函数
#

# softmax经常被添加在分类任务的神经网络中的输出层，神经网络的反向传播中关键的步骤就是求导，从这个过程也可以更深刻地理解反向传播的过程，还可以对梯度传播的问题有更多的思考。
#
# ## softmax 函数
#
# softmax(柔性最大值)函数，一般在神经网络中， softmax可以作为分类任务的输出层。其实可以认为softmax输出的是几个类别选择的概率，比如我有一个分类任务，要分为三个类，softmax函数可以根据它们相对的大小，输出三个类别选取的概率，并且概率和为1。
#
# softmax函数的公式是这种形式：
#
# $$
# S_i = \frac{e^{z_i}}{\sum_k e^{z_k}}
# $$
#
# * $S_i$是经过softmax的类别概率输出
# * $z_k$是神经元的输出
#
#
# 更形象的如下图表示：
#
# ![softmax_demo](images/softmax_demo.png)
#
# softmax直白来说就是将原来输出是$[3,1,-3]$通过softmax函数一作用，就映射成为(0,1)的值，而这些值的累和为1（满足概率的性质），那么我们就可以将它理解成概率，在最后选取输出结点的时候，我们就可以选取概率最大（也就是值对应最大的）结点，作为我们的预测目标！
#
#
#
# 首先是神经元的输出，一个神经元如下图：
#
# ![softmax_neuron](images/softmax_neuron.png)
#
# 神经元的输出设为：
#
# $$
# z_i = \sum_{j} w_{ij} x_{j} + b
# $$
#
# 其中$W_{ij}$是第$i$个神经元的第$j$个权重，$b$是偏置。$z_i$表示该网络的第$i$个输出。
#
# 给这个输出加上一个softmax函数，那就变成了这样：
#
# $$
# a_i = \frac{e^{z_i}}{\sum_k e^{z_k}}
# $$
#
# $a_i$代表softmax的第$i$个输出值，右侧套用了softmax函数。
#
#
# ### 损失函数 loss function
#
# 在神经网络反向传播中，要求一个损失函数，这个损失函数其实表示的是真实值与网络的估计值的误差，知道误差了，才能知道怎样去修改网络中的权重。
#
# 损失函数可以有很多形式，这里用的是交叉熵函数，主要是由于这个求导结果比较简单，易于计算，并且交叉熵解决某些损失函数学习缓慢的问题。**[交叉熵函数](https://blog.csdn.net/u014313009/article/details/51043064)**是这样的：
#
# $$
# C = - \sum_i y_i ln a_i
# $$
#
# 其中$y_i$表示真实的分类结果。
#
#

# ## 推导过程
#
# 首先，我们要明确一下我们要求什么，我们要求的是我们的$loss$对于神经元输出($z_i$)的梯度，即：
#
# $$
# \frac{\partial C}{\partial z_i}
# $$
#
# 根据复合函数求导法则：
#
# $$
# \frac{\partial C}{\partial z_i} = \frac{\partial C}{\partial a_j} \frac{\partial a_j}{\partial z_i}
# $$
#
# 有个人可能有疑问了，这里为什么是$a_j$而不是$a_i$，这里要看一下$softmax$的公式了，因为$softmax$公式的特性，它的分母包含了所有神经元的输出，所以，对于不等于i的其他输出里面，也包含着$z_i$，所有的$a$都要纳入到计算范围中，并且后面的计算可以看到需要分为$i = j$和$i \ne j$两种情况求导。
#
# ### 针对$a_j$的偏导
#
# $$
# \frac{\partial C}{\partial a_j} = \frac{(\partial -\sum_j y_j ln a_j)}{\partial a_j} = -\sum_j y_j \frac{1}{a_j}
# $$
#
# ### 针对$z_i$的偏导
#
# 如果 $i=j$ :
#
# \begin{eqnarray}
# \frac{\partial a_i}{\partial z_i} & = & \frac{\partial (\frac{e^{z_i}}{\sum_k e^{z_k}})}{\partial z_i} \\
#   & = & \frac{\sum_k e^{z_k} e^{z_i} - (e^{z_i})^2}{\sum_k (e^{z_k})^2} \\
#   & = & (\frac{e^{z_i}}{\sum_k e^{z_k}} ) (1 - \frac{e^{z_i}}{\sum_k e^{z_k}} ) \\
#   & = & a_i (1 - a_i)
# \end{eqnarray}
#
# 如果 $i \ne j$:
# \begin{eqnarray}
# \frac{\partial a_j}{\partial z_i} & = & \frac{\partial (\frac{e^{z_j}}{\sum_k e^{z_k}})}{\partial z_i} \\
#   & = &  \frac{0 \cdot \sum_k e^{z_k} - e^{z_j} \cdot e^{z_i} }{(\sum_k e^{z_k})^2} \\
#   & = & - \frac{e^{z_j}}{\sum_k e^{z_k}} \cdot \frac{e^{z_i}}{\sum_k e^{z_k}} \\
#   & = & -a_j a_i
# \end{eqnarray}
#
# 当u，v都是变量的函数时的导数推导公式：
# $$
# (\frac{u}{v})' = \frac{u'v - uv'}{v^2} 
# $$
#
# ### 整体的推导
#
# \begin{eqnarray}
# \frac{\partial C}{\partial z_i} & = & (-\sum_j y_j \frac{1}{a_j} ) \frac{\partial a_j}{\partial z_i} \\
#   & = & - \frac{y_i}{a_i} a_i ( 1 - a_i) + \sum_{j \ne i} \frac{y_j}{a_j} a_i a_j \\
#   & = & -y_i + y_i a_i + \sum_{j \ne i} y_j a_i \\
#   & = & -y_i + a_i \sum_{j} y_j
# \end{eqnarray}

# ## 问题
# 如何将本节所讲的softmax，交叉熵代价函数应用到上节所讲的方法中？

# ## References
#
# * Softmax & 交叉熵
#   * [交叉熵代价函数（作用及公式推导）](https://blog.csdn.net/u014313009/article/details/51043064)
#   * [手打例子一步一步带你看懂softmax函数以及相关求导过程](https://www.jianshu.com/p/ffa51250ba2e)
#   * [简单易懂的softmax交叉熵损失函数求导](https://www.jianshu.com/p/c02a1fbffad6)
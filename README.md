# 中文命名实体识别（NER）

属于NLP任务中的序列标注问题。给定一个输入句子，要求为句子中的每一个token做实体标注（如人名、组织/机构、地名、日期等）。

英文命名实体识别和中文命名实体识别最大的不同在于英文不需要分词，而中文需要分词，所以中文如果分词后做命名实体识别会受限于分词效果。（即分词没分好，导致后续出错；而命名实体很多都是未登陆词，在词表中没有）

**对于中文命名实体识别，基于字符比基于词的方法效果好。**

## 1. 基于规则的方法

## 2. 基于传统机器学习的方法

标准流程分为Training和Predicting两个阶段。

**Training**

* 获取训练数据（文本+标注）
* 设计适合该文本和类别的特征提取方法
* 训练一个类别分类器来预测每个token的label

**Predicting**

* 获取测试数据
* 运行训练好的模型给每个token做标注

## 3. 基于深度学习的方法

paper list:

* Fast and Accurate Entity Recognition with Iterated Dilated Convolutions(2017)
* Chinese NER Using Lattice LSTM(2018)
* Adversarial Transfer Learning for Chinese Named Entity Recognition with Self-Attention Mechanism(2018)
* Adversarial Learning for Chinese NER from Crowd Annotations(2018)
* Adaptive Co-Attention Network for Named Entity Recognition in Tweets(2018)

### 3.1 LSTM+CRF

### 3.2 IDCNN+CRF paper1

目前在NLP领域用的最多的还是要数RNN这一个大类，因为RNN简直就是为文本这类序列数据而生的。但是在实现中也会有很多问题，所以这时候就可能试试CNN。相对于RNN，CNN由于可以并行训练，使得其训练速度远远高与RNN，可以使得在精度不变或损失一点的情况下提高效率。

传统CNN的缺陷。

CNN运用于文本处理，有一个劣势，就是经过卷积之后，末层神经元可能只是得到了原始输入数据中一小部分的信息。所以为了获取上下文信息，可能就需要加入更多的卷积层，导致网络原来越深，参数越来越多，而模型越大越容易导致过拟合问题，所以就需要引入Dropout之类的正则化，带来更多的超参数，整个网络变得庞大冗杂难以训练。

Dilated CNN

基于上述问题，Multi-Scale Context Aggregation by Dilated Convolutions一文中提出了 dilated convolutions ，中文意思大概是“空洞卷积”。正常CNN的filter，都是作用在输入矩阵一片连续的位置上，不断sliding做卷积，接着通过pooling来整合多尺度的上下文信息，这种方式会损失分辨率。既然网络中加入pooling层会损失信息，降低精度。那么不加pooling层会使感受野变小，学不到全局的特征。如果我们单纯的去掉pooling层、扩大卷积核的话，这样纯粹的扩大卷积核势必导致计算量的增大，此时最好的办法就是Dilated Convolutions（扩张卷积或叫空洞卷积）。

Iterated Dilated CNN

论文中提出的IDCNN模型是4个结构相同的Dilated CNN block拼接在一起，每个block里面是dilation width为1,1,2的三层DCNN。

IDCNN对输入句子的每一个字生成一个logits，这里就和biLSTM模型输出logits之后完全一样，放入CRF Layer，用Viterbi算法解码出标注结果。

在biLSTM或者IDCNN这样的深度网络模型后面接上CRF层是一个序列标注很常见的方法。biLSTM或者IDCNN计算出的是每个词分类的概率，而CRF层引入序列的转移概率，最终计算出loss反馈回网络。

### 3.3 Lattice\_LSTM+CRF paper2

Lattice LSTM：LSTM的变体

#### 基于词的LSTM-CRF

一般的pipeline是对文本进行分词之后embedding后输入深度网络预测序列中单词的类别标记。但是这样的话会受限于分词那一步的表现，也就是说如果分词过程效果不好的话，会进一步影响整个NER模型的误差。而对于NER任务中，许多词都是OOV。

#### 基于字的LSTM-CRF

那么把词输入改为字输入是不是会有所改进呢？答案是肯定的。因为字向量可以完美克服上述分词过程引入的误差。但是如果单纯采用字向量的话会丢失句子中词语之间的内在信息。（当然基于该问题，学者们也提出了很多解决方案：例如利用segmentation information作为NER模型的soft features；使用multi-task learning等等）

#### Lattice LSTM

将潜在的词语信息融合到基于字模型的传统LSTM-CRF中去，而其中潜在的词语信息是通过外部词典获得的。Lattice LSTM模型会在字向量的基础上额外获取词特征的信息。

* 模型结构：字LSTM部分。
  这部分和普通LSTM的不同之处在于传入的细胞状态C是**前一个字和相关词输出细胞状态的经过运算得到的**。
  **所以输出细胞状态C不仅包含字符有关的信息，还包含以该字符结尾的词的信息。**
* 模型结构：词LSTM部分。
  这部分和普通LSTM的不同之处在于**没有输出门**。

### 3.4 ATL for NER paper3

# 参考

[Chinese NER Using Lattice LSTM论文笔记](https://www.jianshu.com/p/cdd2061f057b)

[(很好)Chinese NER Using Lattice LSTM](https://blog.csdn.net/sinat_18665801/article/details/90578208)

[Chinese NER Using Lattice LSTM论文笔记](https://www.jianshu.com/p/cdd2061f057b)

[利用Lattice LSTM的最优中文命名实体识别方法](http://baijiahao.baidu.com/s?id=1604786068701856320&wfr=spider&for=pc)


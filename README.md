# 中文命名实体识别（NER）

属于NLP任务中的序列标注问题。给定一个输入句子，要求为句子中的每一个token做实体标注（如人名、组织/机构、地名、日期等）。

## 基于规则的方法

## 基于传统机器学习的方法

标准流程分为Training和Predicting两个阶段。

**Training**

* 获取训练数据（文本+标注）
* 设计适合该文本和类别的特征提取方法
* 训练一个类别分类器来预测每个token的label

**Predicting**

* 获取测试数据
* 运行训练好的模型给每个token做标注

## 基于深度学习的方法

paper list:

* Fast and Accurate Entity Recognition with Iterated Dilated Convolutions(2017)
* Chinese NER Using Lattice LSTM(2018)
* Adversarial Transfer Learning for Chinese Named Entity Recognition with Self-Attention Mechanism(2018)
* Adversarial Learning for Chinese NER from Crowd Annotations(2018)
* Adaptive Co-Attention Network for Named Entity Recognition in Tweets(2018)

### LSTM+CRF

### IDCNN+CRF paper1

目前在NLP领域用的最多的还是要数RNN这一个大类，因为RNN简直就是为文本这类序列数据而生的。但是在实现中也会有很多问题，所以这时候就可能试试CNN。相对于RNN，CNN由于可以并行训练，使得其训练速度远远高与RNN，可以使得在精度不变或损失一点的情况下提高效率。

传统CNN的缺陷。

CNN运用于文本处理，有一个劣势，就是经过卷积之后，末层神经元可能只是得到了原始输入数据中一小部分的信息。所以为了获取上下文信息，可能就需要加入更多的卷积层，导致网络原来越深，参数越来越多，而模型越大越容易导致过拟合问题，所以就需要引入Dropout之类的正则化，带来更多的超参数，整个网络变得庞大冗杂难以训练。

Dilated CNN

基于上述问题，Multi-Scale Context Aggregation by Dilated Convolutions一文中提出了 dilated convolutions ，中文意思大概是“空洞卷积”。正常CNN的filter，都是作用在输入矩阵一片连续的位置上，不断sliding做卷积，接着通过pooling来整合多尺度的上下文信息，这种方式会损失分辨率。既然网络中加入pooling层会损失信息，降低精度。那么不加pooling层会使感受野变小，学不到全局的特征。如果我们单纯的去掉pooling层、扩大卷积核的话，这样纯粹的扩大卷积核势必导致计算量的增大，此时最好的办法就是Dilated Convolutions（扩张卷积或叫空洞卷积）。

Iterated Dilated CNN

论文中提出的IDCNN模型是4个结构相同的Dilated CNN block拼接在一起，每个block里面是dilation width为1,1,2的三层DCNN。

IDCNN对输入句子的每一个字生成一个logits，这里就和biLSTM模型输出logits之后完全一样，放入CRF Layer，用Viterbi算法解码出标注结果。

在biLSTM或者IDCNN这样的深度网络模型后面接上CRF层是一个序列标注很常见的方法。biLSTM或者IDCNN计算出的是每个词分类的概率，而CRF层引入序列的转移概率，最终计算出loss反馈回网络。


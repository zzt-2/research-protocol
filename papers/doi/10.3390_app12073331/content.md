Article

# Modulation Format Identification in a Satellite to Ground Optical Wireless Communication Systems Using a Convolution Neural Network

Yucong Gu 1,2, Zhiyong Wu 1,2,\*, Xueliang Li 1O, Ruotong Tian 1,2, Shuang Ma1 and Tao Jia 1

Changchun Institute of Optics, Fine Mechanics and Physics, Chinese Academy of Sciences, Dongnanhu Road 3888, Changchun 130033, China; guyucong@foxmail.com (Y.G.); lixueliang0202@163.com (X.L.); tianruotong17@mails.ucas.ac.cn (R.T.); jy01892231@126.com (S.M.); jt\_681110@163.com (T.J.)

2University of Chinese Academy of Sciences, Beijing 10049,China

\*Correspondence: wuzy@ciomp.ac.cn; Tel.: +86-0431-8670-8238

Featured Application: In this paper, we put forward a novel modulation format identification (MFI) technique for a free-space optical (FSO) communication system based on a convolution neural network (CNN). The random parameters training method we use can improve the robustness against atmospheric optical turbulence and additive Gaussian white noise (AWGN). The proposed MFI scheme in this paper is a viable solution in the application of an FSO communication simulation channel, which can easily deal with the scene of fast modulation format switch-ing and accurate identification to satisfy system requirements. Therefore, we hope that the MFI scheme we proposed is able to find a practical application in satellite-to-ground FSO systems.

![](images/7c4d5b359f62a046db9068c50298bc803d696fb606ae85839cb4184ff4739baf.jpg)

Citation: Gu, Y.; Wu, Z.; Li, X.; Tian, R.; Ma,S.; Jia,T.Modulation Format Identification ina Satellite to Ground Optical Wireless Communication Systems Using a Convolution Neural Network.Appl. Sci.2022,12,3331. https://doi.org/10.3390/app12073331

Academic Editor: Christos Bouras

Received: 15 February 2022   
Accepted: 21 March 2022   
Published: 25 March 2022

Publisher's Note: MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations.

![](images/47821b7fd806bc334169f3c9d47ab3644980123bd46fc72cfa36e81f71aaa31a.jpg)

Copyright: @ 2022 by the authors. Licensee MDPI,Basel,Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

Abstract: The satelite-to-ground communication system is a significant part of future space commu-nication networks. The free-space optical (FSO) communication technique is a prospective solution for satelite-to-ground communication. However, atmospheric optical turbulence is a major impairment in FSO communication systems. In this paper, to improve the performance and flexibility of a satellite-to-ground laser communication system, we put forward a novel modulation format identification (MFI) technique for an FSO communication system based on a convolution neural network (CNN).The results indicate that our CNN model can blindly and accurately identify the modulation format with classification accuracy up to 99.98% for random channel condition,including the strength of turbulence and signal-to-noise ratio (SNR) of additive Gaussian white noise (AWGN) ranging from 10dB to 30dB. Moreover, the CNN demonstrated robustness against atmospheric op-tical turbulence and suggested immunity to additive noise. Therefore, the proposed methodology proved to be a viable solution in the application of an FSO communication simulation channel, which can easily deal with the scene of fast modulation format switching and accurate identification to satisfy system requirements. Therefore, we hope this scheme can find a practical implementation in satellite-to-ground optical wireless systems.

Keywords: modulation format identification; convolution neural network; free-space optical communication

## 1. Introduction

The satellite-to-ground communication system is a significant part of future space communication networks. Radio frequency (RF) communication links for inter-satellite or satellite-to-ground communication are increasingly limited due to the unideal spectrum availability and limited data rate. A free-space optical (FSO) communication system has become one of the most promising technologies in future communication systems because of it being superior to the traditional RF system [1]. At present, FSO communication links are beginning to take over RF communication links in the field of high bandwidth applications [2]. The requirement tendency of forthcoming satellite data transmission has grown to become a critical boost to the progress of communication technology. Gigantic amounts of information and complicated channel circumstances require high data speed and flexibility at the same time. FSO communication has been taking part in a more vital role in the satellite-to-ground communication step by step [3]. For the flexibility of services and applications, the next-generation FSO network is expected to adjust the modulation format dynamically according to the link conditions and terminal equipment configuration to meet the different requirements of the terminal system and service [4,5]. The traditional method needs to spend time and data processing prior information from the transmitter in the recognition process, which is a great waste in the short connection time of a satellite-toearth link. To promote demodulation eficiency, it is a challenging requirement for an FSO receiver to realize blind modulation format identification (MFI). Over the last few years, several classical MFI techniques for optical communication have been proposed [6-8].

Machine learning (ML) is a powerful interdisciplinary subject combining mathematics, computing, and biological sciences. In recent years, it has been successfully applied in the fields of pattern recognition, computer vision, personalized technology, and data analysis and mining [9]. Recently, techniques from ML have also performed wellin some intelligent expansion directions in the field of optical communication, such as optical performance monitoring (OPM),MFI, and nonlinear impairments compensation [4,9,10]. Compared with traditional methods, the advantage of ML methods for MFI is that it completes the training of the model before practical application [11]. It only needs to let the model know all possible modulation formats during training. In practical use, it can quickly obtain reliable recognition results without sacrificing the processing of prior information. Before that, if the results are not satisfactory in the training process, the model parameters can be adjusted repeatedly before actual communication without adjusting in the time after the actual link is established. As a representative algorithm of machine learning, convolutional neural networks (CNN) have made great achievements in image recognition. Sparse connectivity allows CNN to recognize the local features of input images without all connected feature engineering, which makes CNN distinctly efficient from conventional machine learning techniques [12]. Also, the results of paper [9] show that CNN achieves optimal accuracy and is significantly superior to other ML methods.

However, previous research on MFI has focused mainly on radio and fiber-optic communication networks,and not as much work has been done for MFI in FSO communication networks [13,14]. In this paper, we focus on the performance of the CNN algorithm in modulation format recognition in an FSO communication system. Here, we mainly illus-trate an FSO optical communication system under the random channel condition including the strength of atmosphere turbulence and signal-to-noise ratio (SNR) of AWGN. Four modulation formats were adopted in this paper: (1) On-Off Keying (OOK), (2) Binary Phase Shift Keying (BPSK), (3) Quadrature Phase Shift Keying (QPSK),and (4) 16-Quadrature Amplitude Modulation (16-QAM).

The rest of this paper is organized as follows: Section 2 indicates an overview of CNN's theoretical background. Channel statistics with a gamma-gamma model is dissected in Section 3. The experimental process and the structure of network we designed are introduced in detail in Section 4. Finally, some results and discussions are maintained in Section 5,and conclusions are in Section 6.

## 2. CNN Theoretical Background

CNN is a kind of deep neural network (DNN) that is composed of input layer, hidden layer,and Full-Connected (FC) layer [15]. The hidden layer is a layer with different function, such as convolution layer, Batch Normalization (BN) layer, activation layer, and pooling layer. Generally, a typical structure of CNN is composed of many blocks connected between input and output, in which each block comprises one or several hidden layers $[ 1 6 , 1 7 ]$ .An

FC layer and a classification layer follow the last block and are finally connected to the output layer. A basic network structure is shown in Figure 1.

![](images/aa771d443c9f2c7339757c5ef5f32a6cd717f9c0e00090ba82f0fb6e296e582c.jpg)  
Figure 1. Typical fully connected CNN network architecture.

The convolution layer extracts the feature data from the input data by convolution, to change the data processing of the neural network from a single point to diferent regions and complete data dimensionality reduction. It contains many convolution kernels, which can be regarded as filters. Each element of convolution kernels corresponds to a weight and a bias. When the convolution kernel windows slide on the input data matrix, the filter can convolute with the local data.

Next, the matrix enters the BN layer to convert the data to the same order of magnitude. Then, the matrix enters the activation layer to increase the nonlinearity of the neural network model, so that the neural network can better fit with more kinds of curves and better solve more complex problems. In this paper, we use the rectified linear unit (ReLU) function as the activation function. For the pooling layer, after the input data is divided into many rectangular regions, the output value of each subregion is represented as one point to reduce the dimension for feature extraction. Here, we use the two most common pooling layers, the maximum pooling layer, and the average pooling layer.

Before the final classification decision,the FC layer is used to connect each neuron with each neuron in the previous layer. After the feature map is generated to an appropriate dimension,all neurons are weighted into the FC layer, which can ignore the impact of spatial structure and reduce the impact of location on classification. By activating the classification, the output layer can output the calculated classification results. This article uses the most common Softmax function here, therefore, the probability of each type is mapped to the positive range,and then normalized to (0,1) to obtain the probability of each category. Finally, the output layer outputs the classification decision.

## 3.Channel Statistics with Gamma-Gamma Model

In FSO system, one of the main impairments is atmospheric optical turbulence, which can cause scintillation. Scintillation-induced fading adversely affects FSO links and damages its communication performance.The scintillation results from the index of refraction fluctuations in the atmosphere, which can cause random fluctuations of the received signal intensity and severely reduce the level of the optical signal. The statistics of the scintillation strength is usually regarded as following the gamma-gamma distribution, which is applicable to all turbulence situations from weak to strong. This model, proposed in [18], is based on the modulation process,in which the optical radiation fluctuation through turbulent atmosphere is assumed to be composed of small-scale (scattering) and large-scale (refraction) effects.Therefore, the normalized received irradiance $I _ { t }$ is defined as the product of two statistically independent random processes $I _ { x }$ and $I _ { y }$

$$
I _ { t } = I _ { x } I _ { y }\tag{1}
$$

$I _ { x }$ and $I _ { y }$ are generated by the large-scale and small-scale turbulent eddies, respectively, and both obey the gamma distribution given by [19]. Consequently, their probability density functions (PDF) are given by

$$
p ( I _ { x } ) = \frac { \alpha ( \alpha I _ { x } ) ^ { \alpha - 1 } } { \Gamma ( \alpha ) } \exp ( - \alpha I _ { x } ) ; I _ { x } > 0 ; \alpha > 0\tag{2}
$$

$$
p \left( I _ { y } \right) = \frac { \beta \left( \beta I _ { y } \right) ^ { \alpha - 1 } } { \Gamma ( \beta ) } \exp ( - \beta I _ { y } ) ; I _ { y } > 0 ; \beta > 0\tag{3}
$$

By fixing $I _ { x }$ and using the change of variable, $I _ { y } = I _ { t } / I _ { x . }$ , the conditional PDF given by Equation (4) is obtained, in which $I _ { x }$ is the (conditional) mean value of $I _ { t }$

$$
p \big ( I _ { t } / I _ { x } \big ) = \frac { \beta \big ( \beta I _ { t } / I _ { y } \big ) ^ { \beta - 1 } } { I _ { x } \Gamma ( \beta ) } \exp \bigl ( - \beta I _ { t } / I _ { x } \bigr ) ; I _ { t } > 0\tag{4}
$$

To obtain the unconditionalirradiance distribution, the conditional probability $p ( I _ { t } / I _ { x } )$ is averaged over the statistical distribution of $I _ { x }$ given by Equation (2) to obtain the following gamma-gamma irradiance distribution function.

$$
\begin{array} { r l } { p ( I _ { t } ) } & { = \int _ { 0 } ^ { \infty } p ( I _ { t } / I _ { x } ) p ( I _ { x } ) d I _ { x } } \\ & { = \frac { 2 ( \alpha \beta ) ^ { ( \alpha + \beta ) / 2 } } { \Gamma ( \alpha ) \Gamma ( \beta ) } I _ { t } ^ { ( \frac { \alpha + \beta } { 2 } ) - 1 } K _ { \alpha - \beta } \big ( 2 \sqrt { \alpha \beta I _ { t } } \big ) , I _ { t } > 0 } \end{array}\tag{5}
$$

where $\alpha$ and $\beta$ represent the effective number of large-scale and small-scale eddies in the scatteringprocess,respectively. $\Gamma ( \cdot )$ represents the gamma function,and $K _ { n } ( \cdot )$ is the modified Bessel function of the second kind of order $n .$ If the optical radiation at the receiver is assumed to be a plane wave,then the two parameters& and $\beta$ that characterize the irradiance fluctuation PDF are related to the atmospheric conditions [18],as follows:

$$
\alpha = \left[ \exp \left( { \frac { 0 . 4 9 \sigma _ { l } ^ { 2 } } { \left( 1 + 1 . 1 1 \sigma _ { l } ^ { 1 2 / 5 } \right) ^ { 7 / 6 } } } \right) - 1 \right] ^ { - 1 }\tag{6}
$$

$$
\beta = \left[ \exp \left( \frac { 0 . 5 1 { \sigma _ { l } } ^ { 2 } } { \left( 1 + 0 . 6 9 \sigma _ { l } { } ^ { 1 2 / 5 } \right) ^ { 5 / 6 } } \right) - 1 \right] ^ { - 1 }\tag{7}
$$

while the scintillation index is given by

$$
\sigma _ { N } ^ { 2 } = \exp \left[ \frac { 0 . 4 9 \sigma _ { l } ^ { 2 } } { \left( 1 + 1 . 1 1 \sigma _ { l } ^ { 1 2 / 5 } \right) ^ { 7 / 6 } } + \frac { 0 . 5 1 \sigma _ { l } ^ { 2 } } { \left( 1 + 0 . 6 9 \sigma _ { l } ^ { 1 2 / 5 } \right) ^ { 5 / 6 } } \right] - 1\tag{8}
$$

Often, $\sigma _ { l }$ is the log irradiance variance for a plane wave [19], which is defined as

$$
\sigma _ { l } ^ { 2 } = 1 . 2 3 C _ { n } ^ { 2 } k ^ { 7 / 6 } L ^ { 1 1 / 6 }\tag{9}
$$

In Equation (9), $C _ { n } ^ { 2 }$ is the refractive index structure parameter, which characterizes the atmospheric optical turbulence effect. Generally, the $C _ { n } ^ { 2 ^ { \bullet } }$ range varies from $1 0 ^ { - 1 5 } \mathrm { m } ^ { - 2 / 3 }$ to $1 0 ^ { - 1 2 } \mathrm { m } ^ { - 2 / 3 }$ for the weak to strong turbulence regime, respectively. The gamma-gamma turbulence model given by Equation (5), which is applicable to al turbulence strengths from weak to strong. The values of & and $\beta$ under different turbulence regimes are depicted in Figure 2.

![](images/cf42121443de73d403118ef8b5bc0d88d7dc1fb0fdcea4a7e200df86df01024a.jpg)  
Figure 2. Values of α and $\beta$ under different turbulence regimes: weak, moderate to strong, and saturation.

In this work, we use three different turbulence regimes: weak, moderate to strong, and saturation, as depicted in Figure 3, with the parameters given in [19]. The α, $\beta ,$ and $\sigma _ { l } ^ { 2 }$ values for weak turbulence are 11.6,10.1,and 0.2, respectively. The $\alpha , \beta ,$ and $\sigma _ { l } ^ { 2 }$ values for moderate turbulence are 4, 1.9,and 1.6, respectively. The α, $\beta ,$ and $\sigma _ { l } ^ { 2 }$ values for strong turbulence are 4.2, 1.4, and 3.5, respectively.

![](images/ddee3e60affcbc69dabf0a0eda478d1e2b93e79522323cb13c73edb15a3ac40e.jpg)  
Figure 3. Gamma-gamma probability density function for three different turbulence regimes, weak, moderate, and strong with different &, $\beta ,$ and $\sigma _ { l } ^ { 2 }$ values, respectively.

## 4. Simulation Setup

In this paper, the architecture of our system can be seen in Figure 4. The Communication and Deep Learning Toolbox in MATLAB Software is used for simulation. We chose four typical and promising modulation formats, OOK, BPSK, QPSK,and 16 QAM. A total of 20,000 frames are generated for each modulation format with a length of 1024 samples. Since the network makes each decision based on a single frame rather than multiple con-secutive frames, such as video, each frame must pass through a separate channel. In the transmitter side, the input symbols to the system are sampled and transmitted by a gamma-gamma atmospheric channel with random strength, which ranges from weak to strong added to AWGN whose SNR is generated randomly. At the receiver, the received signal is

$$
y ( t ) = x ( t ) \times h ( t ) + w ( t )\tag{10}
$$

where, $x ( t )$ is the transmitted signal, $h ( t )$ is the gamma-gamma atmospheric channel, and $w ( t )$ is AWGN. Each frame contains 256 symbols, eight sampling points per symbol, and uses a gamma-gamma random variate. Therefore, a coherent time of atmospheric turbulence can be simulated. However, the AWGN is generated for each time step.

![](images/8a96ffe8d1549335ba205978df120d9494e4c762ac7da025a482a38465cab5a3.jpg)  
Figure 4. Proposed optical communication system.

A random number of samples is removed from the beginning of each frame to remove transients and ensure that the frame has a random starting point relative to the symbol boundary. To improve the robustness against atmospheric optical turbulence and AWGN, random parameters are used to ensure the applicability of training data. We set the $\sigma _ { l } ^ { 2 }$ equals as 0.2,1.6,and 3.5,representing the strength of turbulence of weak, moderate, and strong, respectively, for which the three parameter values have been used in most cases [18]. Additionally, we set the SNR of AWGN ranges from 10 to 30 dB.For a given turbulence regime, random fluctuations were added to the signal corresponding to $\overset { \smile } { \sigma _ { l } ^ { 2 } }$ of a particular turbulent regime to make sure al the data of every situation can be considered.

For the subsequent circumstance, the complex input is used as the input dimension of two real inputs, and y(t) is introduced into a narrow two-dimensional convolution network as a set of 2 × 1024 vectors, in which in-phase and quadrature sampling (I/Q) constitute this two-row data, which can be regarded as a two-dimensional image. Figures 5 and 6 show the time domain diagrams and spectrograms of processed data for four modulation formats at present, respectively.

In addition,Figure 7 shows the modulation constellation of the four modulation schemes when the SNR is 10 dB in the case of the weak turbulent channel as a typical example. It can be seen from the constellation points that the modulated signal has been disturbed by turbulence fluctuation and channel additive noise.

Next, the input data were separated into 80% for training, 2O% for validation label accordingly. By ensuring that the number of tags for each modulation format is the same, class imbalance in training data is avoided. In this way, frames of four modulation formats were generated and channel-faded, and their corresponding tags stored and provided to the CNN network.

![](images/a661456979e08b2e832907198a1b1d4735a3e781923826fce3a4b6bff0c6c564.jpg)

![](images/1179595b218492d5e615969cbafab050559f4c6861d30ebe21f862d3b1053181.jpg)

![](images/9c9027620b09906d101bc1a00607a52ddfbb5191e3a6ffb90a6dc56384971992.jpg)

![](images/779d2060f0375b28a844a28fbb3ed54d8271fcbca0c72c6e4d3db1a8665475c3.jpg)  
Figure 5. Amplitude of the real and imaginary parts of the example frames against the sample number. The blue lines are for the real part, while the red ones are for the imaginary part. Weak turbulence with SNR=10 is as an example above.

![](images/74efcfda41012aebf7223a1cbe435c0f6af46e7ce3caf01be86c662845532f0b.jpg)

![](images/0dbf69d6fd3aaef839dcb9d800d786a1a056bc379ee8804577936e8b144c0e29.jpg)

![](images/bef7fc37d1f0c1479b6ba96c6114d9570411f2972bb6a3cd53668a41cf603397.jpg)

![](images/a4ded28b81d1e4373384d63e53ef1f02c942290ed28f5c40636f11b38e2c2e0b.jpg)

Figure 6. Spectrogram of the example frames. Weak turbulence with SNR = 10 is as an example above.  
![](images/f3a9ed481cd76630e2582dfa95a06b61fe28b644e6dc02f5f3e6f858f0006e64.jpg)

![](images/dd91d03cebf1039c01e056b965393b33c213e29e3052bdee7d112644ca414858.jpg)  
(b)

![](images/d5d3b39d94005b65b3f88b217df034e53d7d6aafe51bc4bf13c56d776b92a44a.jpg)  
(c）

![](images/c7e2f8805d4c6ac9086348d8b9c5a26e842ba9cbfbf69ef58583bf795f9e0377.jpg)  
Figure 7. Constellation diagram of (a) OOK,(b) BPSK,(c) QPSK,and (d) 16 QAM.

In the network structure adopted in this paper, six directly connected blocks are used. Each block is directly connected with four layers: convolution layer, BN layer, ReLU layer, and pooling layer. In the first five blocks, the maximum pooling layer is used to extract the meaningful features, and the average pooling layer is used in the last block to avoid erasing the details of the previous feature map. Finally, an FC layer is connected to the Softmax layer to output the classfication decision. The network structure is shown in Figure 8 below.

![](images/450d7e62611cff79096a08cc4768d27f528f45adee9eb7fc161a81431821ef96.jpg)  
Figure 8. Simplified network structure with feature matrix size and stride size.

The parameters of feature matrix size and stride size of major layers are listed in Table 1 below.

Table 1. Network parameters of major layers.
<table><tr><td>Layer Name</td><td>Size</td><td>Stride Size</td></tr><tr><td>Input</td><td> $2 \times 1 0 2 4 \times 1$ </td><td>1×8</td></tr><tr><td>Convolution 1</td><td> $2 \times 1 0 2 4 \times 1 6$ </td><td>1×8</td></tr><tr><td>MaxPooling 1</td><td> $2 \times 5 1 2 \times 1 6$ </td><td>1×2</td></tr><tr><td>Convolution 2</td><td> $2 \times 5 1 2 \times 2 4$ </td><td>1×8</td></tr><tr><td>MaxPooling 2</td><td> $2 \times 2 5 6 \times 2 4$ </td><td>1×2</td></tr><tr><td>Convolution 3</td><td> $2 \times 2 5 6 \times 3 2$ </td><td>1×8</td></tr><tr><td>MaxPooling 3</td><td> $2 \times 1 2 8 \times 3 2$ </td><td>1×2</td></tr><tr><td>Convolution 4</td><td> $2 \times 1 2 8 \times 4 8$ </td><td>1×8</td></tr><tr><td>MaxPooling 4</td><td> $2 \times 6 4 \times 4 8$ </td><td>1×2</td></tr><tr><td>Convolution 5</td><td> $2 \times 6 4 \times 6 4$ </td><td>1×8</td></tr><tr><td>MaxPooling 5</td><td> $2 \times 3 2 \times 6 4$ </td><td>1×2</td></tr><tr><td>Convolution 6</td><td> $2 \times 3 2 \times 9 6$ </td><td>1×8</td></tr><tr><td>AveragePooling</td><td> $2 \times 3 2 \times 9 6$ </td><td>1×2</td></tr><tr><td>FullConnected</td><td> $1 \times 6 1 4 4$ </td><td></td></tr><tr><td>Output</td><td> $1 \times 4$ </td><td></td></tr></table>

After signal preprocessing, the synthesized signal is put into the CNN network whose structure is described in Section 2.Next, we use SGDMsolver with the small batch size of 256. We set the maximum number of rounds to six, as more rounds will not provide further training advantage. The initial learning rate is set to 0.3,and the dropout rate is O.6. After every four rounds, the learning rate will be reduced by a factor of 0.3. Specific parameters are listed in Table 2.

Table 2. Network training parameters.
<table><tr><td>Parameters</td><td>Value</td></tr><tr><td>Small batch size</td><td>256</td></tr><tr><td>Maximum number of rounds</td><td>6</td></tr><tr><td>Initial learning rate</td><td>0.3</td></tr><tr><td>Reducing period</td><td>4</td></tr><tr><td>Learning rate drop factor</td><td>0.3</td></tr><tr><td>Dropout rate</td><td>0.6</td></tr></table>

## 5. Results and Discussion

In the training process,verification is taken at the end of every epoch,and the final verification accuracy reaches over 99.99%. The training progress with accuracy and loss results is shown in Figure 9.

![](images/5462403554546d2d123aa71992ef61d41267008b8e022a798eb4a7fde0153db8.jpg)

![](images/629f787fa1d07b3db9bc85e648f1e724c494ae02844b5482e1f0058c4e9a91bb.jpg)  
Figure 9. Training progress with accuracy and loss results.

When the network training is successful, then the test process is carried out. Using the method of generating training data mentioned above, the random modulated data but with a different random seed is generated. Another 40o0 test frames with random turbulence strength and AWGN with random SNR are generated for each format.

The trained network is used for recognition, and the test accuracy reaches over 99.99%. Three confusion matrix figures for the test data for three gamma-gamma turbulence strengths are shown in Figure 10. Figure 10a depicts the integrated test accuracy under different SNR (10-30 dB) in weak turbulent channels,and the test accuracy can reach 100%. Similarly, Figure 10b,c depict the moderate and strong turbulent channel circum-stances, and the test accuracy can reach 99.9864% and 99.9818%, respectively. Moreover, Figure 11 shows the same meaning more intuitively.

![](images/4ee94a4267ba140dab84f734993cf8fd7629e9e96fa07056d6acd5625287a330.jpg)

![](images/f35815fa5be000e662a50869e19d8ef96c7a6381ebd55eb6d52ca7c27a2c7bfe.jpg)

![](images/defc2f819c35efc0d857bfcab61de819eb539f1f5cd823f2dc9b0d84d4e59ada.jpg)

Figure 10. Confusion matrix for test data for diffrent turbulence strength: (a) weak, (b) moderate, and (c) strong.  
![](images/7e2868580194852b3e5c05f4ef6e9e2ba4f3cfc49fd23f2f5f6d4c51dddb2fb7.jpg)  
Figure 11. SNR vs. test accuracy for weak, moderate, and strong turbulence strength.

## 6. Conclusions

This paper proposes a novel technique for MFI by applying a convolution neural network in an FSO link. Four widely used modulation formats (OOK, BPSK, QPSK, and 16 QAM) were comprehensively investigated. The recognition effect of our training network demonstrated robustness against atmospheric optical turbulence and suggested immunity to additive noise. Successful identification with over 99.98% test accuracy was achieved for studied scenarios.

Although the CNN algorithm achieved high recognition accuracy, the recognition accuracy cannot reach 100% when the modulation format types are similar. Therefore, in the future work, we hope to explore the application of recognition for more format types and feature-based data set construction, to improve the training time cost and accuracy. We believe that the proposed technique has the potential to be embedded in space networking and satellite-to-ground laser communication links.

Author Contributions: Writing-original draft preparation, Y.G.; Writing-review and editing, Y.G.; Visualization, X.L. and R.T.; Supervision, S.M.and T.J.; Project administration, Z.W. Allauthors have read and agreed to the published version of the manuscript.

Funding: This research received no external funding.

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Informed consent was obtained from allsubjects involved in the study.

Data Availability Statement: This study did not report any data.

Acknowledgments: This work is supported by the Research Project of Scientific Research Equipment of Chinese Academy of Sciences. The authors also gratefully acknowledge the Optical Communica-tion Laboratory of CIOMP for the use of their equipment.

Conflicts of Interest: The authors declare no conflict of interest.

## References

1.Khalighi,M.A.; Uysal,M.SurveyonFreeSpace OpticalCommunication: A Communication TheoryPerspective.IEEE Commun. Surv. Tutor. 2014,16,2231-2258.[CrossRef]

2.Gong,S.;Shen,H;Zhao,K.NetworkvailablityaximzatioforFree-SpaceOpticalSateliteommunications.EEWirees Commun. Lett.2019,9,411-415. [CrossRef]

3. Kaushal,H.; Kaddoum,G.OpticalCommunication in Space: Challenges and MitigationTechniques.IEEECommun.Suro.Tutor. 2017,19, 57-96.[CrossRef]

4.MusumeciF;Rotondi,C.;Nag,A.;Macaluso,L;Toratore,M.Anoverviewoapplicationofmachinelearing techiquesin optical networks. IEEE Commun. Suro. Tutor. 2019,21,1383-1408. [CrossRef]

5.AvetaF;Refai,H..Modulationformatandnumberofusesassiationinultiointfrespaceoticalcommunicatonusing convolutional neural network. Opt. Eng. 2020,59, 060501. [CrossRef]

6. Liu,J;Dong,Z.; Zhong,K.; Lau,APT.; Lu,C.;Lu,Y Modulation formatidentification based onreceived signal power distributionsfordigitalcoherentreceivers.InProceedingsof theOpticalFiberCommunicationConference(OFC),Sanrancisco CA, USA, 9-13 March 2014. [CrossRef]

7.Borkowski,R;barD;Cbalero,A;rnnoV;onroyItokesSaceBasedOpticaloduationratRecogitiofor Digital Coherent Receivers.IEEE Photon. Technol. Lett2013,25,2129-2132.[CrossRef]

8. Bilal, S.M.;osoG.; DongZ.;Lau,A.PT.;Lu,CBlnd modulationfrmatidentificationfordigitalcoherenreceiver.Opt. Express 2015,23,26769-26778. [CrossRef] [PubMed]

9. Wang,D.; Zhang,M.; LiZ.;LiJ;FuM.; CuiY; Chen,X.Modulation Format Recognitionand OSNR Estimation Using CNN-based Deep Learning.IEEE Photon. Technol. Lett. 2017,29,1667-1670. [CrossRef]

10.Amirabadi,M.A.;Kahaei,M.H;Nezamaloseini,S.A.;VakilVDeplearngforhanelstimationiFSOcommcation system. Opt. Commun. 2019,459,124989. [CrossRef]

11.Khan,FN;Zhong,K.;A-Arashi,WH;Yu,C;Chao,L;Lau,A.PTodulationFormatIdentificationinCoherentReceiers Using Deep Machine Learning. IEEE Photon. Technol. Lett. 2016,28,1886-1889. [CrossRef]

12.Li,J; ZhangM.;Wang,D; Wu,S.;Zhan,Jointtmospheric turbulencedetectioandaaptiedemodulationechqueusing the CNN for the OAM-FSO communication. Opt. Express 2018,26,10494. [CrossRef] [PubMed]

13.Liu,X.ang,DGal,AE.DeeuralewokieurefoduationiatioIredingsofte5st AsilomarConferenceonSgnals,Systems,ndComputers,acificGrove,CA,USA29October-1November201; .915-919. [CrossRef]

14.Xiang Q.;YangY;ZangQ;Yao,YJint,auateandrobustopticalsignaltooiserationd modulationformatmoitorng scheme usingsingleStokes-parameter-basedartificialneuralnetwork.Opt.Expres 221,29,7276-7287.[CrosRef][PubMed]

15.Khan,FN;Fan,Q;Lu,C.;Lau,A.PT.Machineleaing methodsforopticalcommunicationsystemsandnetworks.IOptical Fiber Telecommunications,7th ed.; Academic Pres: Salty Lake City, UT, USA,2020; pp. 921-978. [CrossRef]

16.OShea,TJ;Corgan,J.;ClancyTC.ConvolutionalRadioodulatioRecognitionNetworks.Commun.Comut.Inf.Sci.01, 213-226. [CrossRef]

17.Darwesh,L.; Aon,S.Deeplearingforfre spaceoptics inadata centerenvironment.LaserCommunicationandPropagation through the AtmosphereandOceansVII Inrocedings oftheSOpticalEnginering +Applications,SanDego,CAUSA, 20-22 August 2018. [CrossRef]

18.Andrews,L.C.;ilis,RL;Hn,CYLseremintiltionihpcios;Sres:Belnghm,WU0.[CrossRef]

19.Ghasemlooy,Z.;Ppola,W;Rajadari,S.Optical WirelessCmmunications:SystemandCannel odelingwihAB, 2nd ed.; CRC Press: Boca Raton,FL, USA,2019; ISBN 9781498742696.
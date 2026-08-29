RESEARCH

Open Access

# Improved demapping for channels with data-dependent noise

![](images/ba9cf4b89bea0bac02897905acee5f45bf57d1b5cb6e1e87817c44065b6ceae6.jpg)

Kelvin J. Layton\* D, Azam Mehboob, William G. Cowley and Gottfried Lechner

## Abstract

A newdemapperis presented for communication channels that can be modeled with data-dependent noise on the received symbols.This includes optical and satelitechannels with various types of distortion.The demapper incorporates the covariance information of the received symbol clusters to capture noise variation across the Constelltion and any dependency between the in-phase and quadrature components.Two communication scenarios are considered,andit is shown that the demapper is advantageous when a system is dominated by distortion as opposed to thermal noise.Channel coding considerations are presented,and reductionsupto4 dB in the required SNR are achieved.

Keywords: Demapping, Nonlinear distortion,Symbol covariance, Satellite channels,Predistortion

## 1 Introduction

Distortions in modern communication systems arise due to hardware imperfections or inherent properties of the channel, e.g.,fading.As the trend towards spectrally efficient modulation and large signal bandwidth continues, distortions often become the main botleneck in system performance.A multitude of techniques exist to combat various types of signal distortion including predistortion at the transmitter [1,2],equalization at the receiver [3], and modulation schemes such as OFDM [4] and errorcorrecting codes [5].In this work,we focus on improved demapping in the presence of distortion.

The demapping task is often posed as a maximum likelihood problem [6].Alternatively, prior information was incorporated for a posteriori probability (APP) demapping in [7,8],which was applied to iterative demapping and decoding for bit interleaved coded modulation. Central to both maximum likelihood and APP demapping is the conditional distribution of the received signal given the transmitted signal. Demapping with a Rayleigh distribution from a fading channel for noncoherent orthogonal modulation was considered in [9].A Poisson model is used for maximum likelihood detection in optical communications [1O]. For amplitude and phase-shift keying (APSK)

modulation, however, demapping algorithms to date have assumed additive white Gaussian noise,which has equal variance for in-phase and quadrature components and is independent of the transmitted signal [7，11，12]. Modern demapping algorithms for APSK modulation incorporate the mean of the noise distribution as a shift in the received symbol centroids,e.g., obtained by pilot symbols [13,14]; however, these works retain the assumption of equal noise variance across the constellation.

To compensate for distortions during demapping, we consider distortions that can be modeled at the symbol level with data-dependent noise.That is, the received symbols have a different noise distribution depending on the transmitted symbol. This noise model is applicable to systems such as NAND flash memory [15],pulse amplitude modulation in optical communications [16],and other nonlinear channel distortions [17,18]. In the current manuscript,we focus on general APSK modulation schemes and apply a data-dependent noise model to capture imperfections in a satellite channel for two scenarios: (i) a nonlinear power amplifier with predistortion at the transmitter and (ii) phase noise at the receiver. The proposed demapper incorporates the mean and covariance of each symbol cluster to model noise variation across the constellation and any asymmetry in the noise distribution. This results in more accurate likelihood ratios,which can be used directly for soft-decoding or to determine better decision regions for hard-decoding.

For a specific type of nonlinear distortion,it may be possible to design a tailored compensation scheme to improve performance.For example,we could search for a channel coding scheme to achieve capacity using a nonuniform distribution of symbols [19]. Alternatively, the input symbols could be transformed by a nonlinear function to create a uniform noise distribution at the receiver, as was proposed for optical systems [16]. The motivation for our approach of demapping with a general model is twofold. First, the generality means the algorithm is applicable to a wide range of nonlinear distortions,including those that are ill-characterized.Secondly, the method is useful when modification to the transmission pipleine is impractical or expensive, e.g., satellite channels [20].

The remainder of the paper is organized as follows. Section 2 describes two communication scenarios and a unifying model based on data-dependent noise. Section 3 discusses methods to estimate the noise distribution and how to exploit this information for demapping. Section 4 presents detailed simulation results to assess the performance of the proposed demapper,and Section 5 concludes the paper.

## 1.1Notation

Before proceeding,we briefly describe the notation used throughout the paper. Random variables for channel input, output,and noise are denoted with capital letters,X, Y,and Z, respectively. The corresponding realizations by lowercase,x,y,and z.I(X; Y) indicates the mutual information between X and Y.Sets are denoted with script, e.g., S,I. Indices are typically $i , j ,$ or k.L values are labeled $L ,$ $L ^ { a } ,$ ,and Le,for the a posteriori (APP),a priori, and extrinsic,respectively. Finally,N(μ,Σ）represents a Gaussian distribution with mean μ and covariance ∑.

## 2 System model

In this section，we describe the system components and present some examples of distortion. Subsequently, a reduced channel model is presented for optimal demapping.

## 2.1 Communication scenarios

We consider two communication scenarios depicted in Fig.1.In both cases,the information bits are encoded with an error-correcting code (Encoder), mapped to symbols (Mapper),and converted to a signal for transmission (Tx Filter).

## 2.1.1Scenario 1: nonlinear amplifier

In the first scenario,a predistorter is used to compensate for the nonlinear power amplifier (PA).This situation is common in satellite communications involving a traveling-wave tube amplifier(TWTA) [21] and wireless applications where power efficiency is important [2]. Imperfect compensation results in an overall system that is nonlinear. For this work,the TWTA characteristics are modeled with the memoryless model proposed by Ghorbani and Sheikhan [22]. The signal predistortion is implemented with a complex-valued polynomial [23], such that the output signal, y,is

$$
y ( n ) = \sum _ { k = 1 } ^ { K } \sum _ { l = 0 } ^ { L } c _ { l , k } x ( n - l ) | x ( n - l ) | ^ { k - 1 } ,\tag{1}
$$

where x(n) is the input signal at sample n and $_ { c _ { l , k } }$ are the complex coefficients for delay l and order k.

## 2.1.2 Scenario 2: phase noise

The second scenario assumes a linear PA (and no predistortion) but the addition of phase noise at the receiver. In this case, the output, y, is

$$
y ( n ) = x ( n ) e ^ { j \phi ( n ) }\tag{2}
$$

where the phase noise Φ(n) is simulated using filtered Gaussian noise to match a given power spectral density mask [24]. Although phase noise is well studied and can be compensated in other ways (e.g., [25, 26]),we use this example to demonstrate the generality of our demapping approach.

![](images/dc07909d93f762e63bec01a1cb77c7c5f7057e30ad89f38debeb54db4c99b8f3.jpg)  
Fig.1SystemmodelBlockdiagramofthebasebandommunicationlinkTwosenariosareshownbythedashdbxesbasedonturcef distortion:(todistortiuetmpefectompesatiooflineamplfieandbtom)paseoeattheeiveresedistorise compensated with a demapper based on the mean and covariance the received symbols

## 2.2Motivating examples

The above system imperfections affect the location of the received symbols.In addition to a shift in the centroid of each cluster of symbols, the spread and shape of the symbol clusters may also be modified,e.g.，due to nonlinear intersymbol interference (ISI).As motivating examples，we simulate scenarios 1 and 2 with a 64-APSK and 64-QAM constellation, respectively. The additive noise had an $E _ { s } / N _ { 0 }$ of 26 dB and received symbols are plotted in Fig. 2a and b (more simulation details are given in Section 4).In scenario 1,the predistortion in (1),combined with the nonlinear amplifier, results in a small shift in centroid locations while the spread of the symbols varies substantially across constellation points. For example,symbols from the outer constellation ring exhibit larger variation compared to the symbols from the inner rings even though they experience the same level of thermal noise; further, correlation between the I and Q components leads to a non-isotropic distribution of symbol locations.Similarly for scenario 2,due

a

## 2.3Reduced channel model

to the nature of phase noise in (2),outer constellation points experience more degradation (Fig. 2b). These effects can be quantified by calculating the covariance matrix for each constellation point,as illustrated in Fig. 2c, d.

The distortions above can be modeled with a general bitwise channel model suitable for demapping,as shown in Fig. 3. Components between the mapper and demapper are represented at the symbol level as a discrete time channel with data-dependent additive noise Z. The input to the channel,X, is mapped from bits $B _ { 1 } , \ldots , B _ { m }$ by the modulator and takes values from a finite alphabet (or constellation), $\mathcal { S } = \{ x _ { 1 } , \ldots , x _ { M } \}$ with $M = 2 ^ { m }$ . For simplicity, we consider the I and Q components of a symbol as elements of a vector. Thus X,Y,and Z are in $\mathbb { R } ^ { \dot { 2 } }$ . The output Y is defined by the signal model,

b  
![](images/b3d313261e71328ddd995aa2f9ed25b9f2ce064851603df90148f3797a0cd141.jpg)

$$
Y = X + Z
$$

C

(3)

![](images/8ce87db918dab2eb7ca3e5419f4d0ad61718d6421b22a47bd105eb83841ae20e.jpg)

![](images/a40c154fec5a60adb49128dcc5f26a177951de6f0235bf277c1292df87deb3a1.jpg)

d  
![](images/c8c998574078b400cf8a38f0826f3b0577a4bf07e00d4575a0243069022e00ef.jpg)  
Fig.2Visualizationofdata-dependentoiseScatediagramoftereceivedsblslQcomponets)ilstratigoliarefectsfro impreciseamplifecompensatiof64-ASKmodulatioadasenosefromeceiveoilltorinstabiliesfo64QAcnstelloe estimatedcovaaahstelpntipidiselps%ofienelvelaliod with a circle and estimated symbol centroids with a cross

![](images/46878819c488f13615b3a8580cfd95e873bedd3cb433bb04fbc6e048c45e6f2d.jpg)  
Fig.3 Reduced channel model. A reduced channel model includes input symbols X,output Y,and additive noise Z.Data-dependent noise $( \mathrm { i } . \mathrm { e } . , Z$ dependent on X) is used to capture certain types of distortions in a communication link.A group of equivalent bit channels is defined by including a mapper to convert bits $B _ { 1 } , \ldots , B _ { m }$ to a symbol and a soft demapper to map a symbol to Lvalu $\mathsf { l e s } , L _ { 1 } , \ldots , L _ { m }$

The noise is characterized by the conditional probability density function (PDF） of Z given $X ~ = ~ x _ { k }$ for $k = 1 , \dots , M$

$$
p z _ { \vert X } ( z \vert x _ { k } ) = \mathcal { N } ( \delta _ { k } , \Sigma _ { k } ) ,\tag{4}
$$

where $\mathcal { N } ( \delta _ { k } , \Sigma _ { k } )$ denotes the bivariate Gaussian distribution with mean $\delta _ { k }$ and covariance $\Sigma _ { k } ;$ the subscript k emphasizes the dependency of the noise distribution on the channel input $x _ { k }$ .The conditional PDF of the channel follows from the signal model,

$$
p _ { Y | X } ( y | x _ { k } ) = \mathcal { N } ( \mu _ { k } , \Sigma _ { k } ) ,\tag{5}
$$

where $\mu _ { k } = x _ { k } + \delta _ { k }$ is the centroid of the received symbol cluster for the kth constellation point.The role of the demapper is to convert the received symbol Y into soft information about the bits,denoted $L _ { 1 } , \dots , L _ { m } .$

In this reduced channel model, the symbol covariance $\Sigma _ { k }$ captures the total uncertainty from two sources: (i) the AWGN and (ii) the nonlinear distortion or phase noise. We refer to the former as thermal noise,SNR,or $E _ { s } / N _ { 0 }$ and the latter as distortion. The reduced channel model is a generalization of the common additive Gaussian noise model used for demapping in QAM systems [7,11],with a non-diagonal covariance that depends on the transmitted symbol. The extra degrees of freedom are useful to represent general nonlinearities such as those described in Section 2.1,while the Gaussian assumption keeps the computations tractable during demapping.

## 3 Methods

This work proposes an improved demapper that uses knowledge of the symbol clusters at the receiver. Demodulation based on the received symbol centroids, $\mu _ { k } ,$ has been proposed previously [13,14]；however, this work extends the concept to exploit the additional information provided by the symbol covariances.Intuitively, for a hard-decision demapper, constellation points with a larger covariance should have a larger decision region to capture the uncertainty. This intuition follows for a soft-decision demapper based on log-likelihood ratios.

The a posteriori probability (APP) demapper produces an L value,for each bit $b _ { i }$ given a received symbol $y =$ $( y _ { I } , y _ { Q } )$ ,defined as

$$
\begin{array} { r l r } {  { L _ { i } = \log \frac { \operatorname* { P r } ( b _ { i } = 0 | y ) } { \operatorname* { P r } ( b _ { i } = 1 | y ) } } } \\ & { } & { = \log \frac { \sum _ { x \in S _ { i } ^ { 0 } } p ( y | x ) p ( x ) } { \sum _ { x \in S _ { i } ^ { 1 } } p ( y | x ) p ( x ) } + \log \frac { \operatorname* { P r } ( b _ { i } = 0 ) } { \operatorname* { P r } ( b _ { i } = 1 ) } , } \end{array}\tag{6}
$$

(7)

where sets $ { \boldsymbol { S } } _ { i } ^ { 0 }$ and $S _ { i } ^ { 1 }$ are the constellation symbols with bit i set to O and 1, respectively. The a posteriori L value, $L _ { i } ,$ in (7) can be written as,

$$
L _ { i } = L _ { i } ^ { e } + L _ { i } ^ { a } ,\tag{8}
$$

where $L _ { i } ^ { a }$ is the a priori L value and $L _ { i } ^ { e }$ is the extrinsic L value for the ith bit [7]. The extrinsic L value is further expanded as,

$$
L _ { i } ^ { e } = \log \frac { \sum _ { x \in \cal S _ { i } ^ { 0 } } p ( y | x ) \prod _ { j \in { \mathcal { Z } } _ { i } ( x ) } e ^ { - L _ { j } ^ { a } } } { \sum _ { x \in \cal S _ { i } ^ { 1 } } p ( y | x ) \prod _ { j \in { \mathcal { Z } } _ { i } ( x ) } e ^ { - L _ { j } ^ { a } } } ,\tag{9}
$$

where $\mathcal { T } _ { i } ( x )$ is the set of bit indices where symbol x has a bit value of 1 (excluding the current index).That is, ${ \mathcal { T } } _ { i } ( x ) ~ = ~ \{ j ~ \in ~ \{ 1 , . . . , m \} ~ | ~ j ~ \neq ~ i ~ \land ~ b _ { j } ~ = ~ 1 \}$ .For APP demapping, the L value in $( 6 ) \AA - ( 8 )$ is used.However, in this work,we also use the extrinsic L value, $L _ { i } ^ { e } ,$ directly for two purposes: first, to compute the maximum achievable rate in Section 4.1; secondly, to exchange soft information in iterative demapping and decoding in Section 4.4.

The extrinsic L values in (9),and corresponding a posteriori L values in (8),depend on the conditional distribution or likelihood, $p ( \boldsymbol { y } | \boldsymbol { x } )$ .For the reduced channel model in (5),the likelihood is a bivariate Gaussian with a PDF defined by

$$
p ( y | x _ { k } ) = \frac { \exp \left( - \frac { 1 } { 2 } ( y - \mu _ { k } ) ^ { T } \Sigma _ { k } ^ { - 1 } ( y - \mu _ { k } ) \right) } { 2 \pi \sqrt { | \Sigma _ { k } | } } ,\tag{10}
$$

where丨·|denotes the determinant of a matrix.The mean $\mu _ { k }$ and covariance $\Sigma _ { k }$ for $k = 1 \ldots , M$ can be estimated from the received symbols,elaborated below. The key distinction between the proposed demapper and existing methods is the use of the symbol-dependent covariance matrix $\Sigma _ { k }$

## 3.1Covariance estimation

In a practical system,a necessary step for the proposed demapping scheme is to estimate the covariance of each symbol cluster.A simple method to estimate the symbol distribution is to use known pilot symbols inserted in the transmitted frame. The received pilots,yi, can be grouped according to the kth constellation point and the sample mean and covariance used as the unbiased estimates of the distribution parameters,

$$
\mu _ { k } \approx \frac { 1 } { N } \sum _ { i = 1 } ^ { N } y _ { i }\tag{11}
$$

$$
\Sigma _ { k } \approx \frac { 1 } { N - 1 } \sum _ { i = 1 } ^ { N } ( y _ { i } - \mu _ { k } ) ( y _ { i } - \mu _ { k } ) ^ { T } .\tag{12}
$$

For a low number of pilots, improved results are pos-sible using multiple frames or biased shrinkage estimates [27]. The estimates above are appropriate for the reduced channel model in Section 2.3. Improved estimates may be possible incorporating prior information from a more detailed nonlinear model; however, in this work,we keep the model general to widen the potential applications.

In the absence of pilot symbols,“blind estimation”of the centroids and covariances must be performed using the received symbols.A fixed set partitioning can be used to group symbols prior to calculation of the centroids [13,28]. A two-step adaptive set partitioning was pro-posed in [14]. Alternatively, we conjecture that a probabilistic approach with soft boundaries would be optimal. We pose the problem as estimating the parameters of a Gaussian mixture model (GMM) from samples of the underlying distribution,where the mixture weights are equal and set to $1 / M .$ That is,we consider the received symbols as the samples from the distribution,

$$
p ( \boldsymbol y | \boldsymbol \theta ) = \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \mathcal N ( \boldsymbol y ; \boldsymbol \mu _ { k } , \boldsymbol \Sigma _ { k } )\tag{13}
$$

where the goal is to estimate the unknown means and covariances $\boldsymbol { \theta } = [ \mu _ { 1 } , \Sigma _ { 1 } , . . . \mu _ { M } , \Sigma _ { M } ] ^ { T }$ from N received symbols $y _ { 1 } , \ldots , y _ { N }$ . These parameters can be estimated efficiently using the expectation-maximization (EM) algorithm [29,30]. The advantage of this algorithm is that hard decisions about the transmitted symbols are not performed; instead, it computes “soft labels”denoted Yi,k, which are posterior probabilities that the kth constellation point was transmitted given the received symbol yi. These are then used to weight the sample mean and covariance calculations.That is,after initialization, the following steps are repeated until convergence:

E-step The posterior probabilities for the transmit symbols $\gamma _ { i , k }$ are computed using Bayes’rule and the current parameters θ [30].

M-step The parameters θ are re-estimated using the current transmit probabilities $\gamma _ { i , k }$ as,

$$
\mu _ { k } \approx \frac { 1 } { \tilde { N } _ { k } } \sum _ { i = 1 } ^ { N } \gamma _ { i , k } y _ { i }\tag{14}
$$

$$
\Sigma _ { k } \approx \frac { 1 } { \tilde { N } _ { k } } \sum _ { i = 1 } ^ { N } \gamma _ { i , k } ( y _ { i } - \mu _ { k } ) ( y _ { i } - \mu _ { k } ) ^ { T } ,\tag{15}
$$

where $\begin{array} { r } { \tilde { N } _ { k } ~ = ~ \sum _ { i } \gamma _ { i , k } } \end{array}$ is the effective number of symbols assigned to cluster k.

We briefly compare the blind GMM algorithm and the pilot-based method through simulation. The symbol covariances were estimated from each algorithm after the nonlinear distortion in Scenario 1. The true covariance was calculated using all the received symbols and knowledge of the transmitted symbols.The normalized mean squared error (NMSE) between the estimated and true covariance was calculated for various levels of distortion at an SNR of 25 dB.Figure 4 illustrates that the GMM algorithm is more accurate for low levels of distortion since accurate assignment of symbols to constellation points can be performed.After assignment, the large number of symbols is used to reduce the error in the estimates.However, as the distortion increases,the cluster boundaries begin to overlap and the accuracy of the covariances decrease.Likewise,the performance of the GMM algorithm degrades for lower SNR.In practice, communication systems without pilots typically have low modulation orders and relatively high SNR-a situation where we expect the GMM algorithm to perform well.

![](images/aae24f2c4c5355bdef1b9bd2f49a18d1cff772ad86243eee67fa5c258767d4b0.jpg)  
Fig.4 Covariance estimation.Normalized mean square error (NMSE) for different covariance estimation methods.Various levels of nonlinear amplifier distortion were tested for scenario 1 with 64-APSK modulation at an SNR of 25 dB

Estimation using 60 or 120 pilot symbols per constellation point results in a relatively constant error of 6 or 3%, respectively, for varying levels of distortion.

This demonstrates that the demapper is applicable to practical systems with or without pilots,using sample means and covariances in the former and blind GMMbased estimation in the latter case.

## 4Simulation results

All simulations were performed in MATLAB (The Mathworks,Natick,MA).Information bits were generated with equal probability with a pseudorandom number generator before coding and modulation. We implemented the coding strategy defined by the Consultative Committee for Space Data Systems (CCSDS),consisting of serial concatenated convolutional codes (SCCC) at the transmitter and a turbo decoder at the receiver [31]. Various puncturing strategies are used to define different code rates.A symbol rate of 25O Msym/s was used for all simulations.After modulation, the signal was synthesized with four times oversamplingand a root-raised-cosine transmit filter with a rolloff of O.35.Complex Gaussian noise was added to simulate thermal noise before the signal was processed by the receive modules.

We compare two demappers: (i) a standard demapper, which assumes circularly symmetric noise with a constant covariance across constellation points and (ii) the proposed covariance-based demapper. Both demappers account for the mean of the symbol-dependent noise distribution using estimates of the cluster centroids.However, the proposed demapper also utilizes the covariance of each symbol cluster. Since the proposed demapper is a generalization of the standard APSK demapping algorithm, this comparison allows us to quantify the improvement obtained by using the covariance information.The means and covariances are estimated using 120 known pilot symbols per constellation point. Using CCSDS frames,this represents a 6% reduction in data rate for a 64 order modulation. Simulations below processed 50 frames $( \sim 1 0 ^ { 7 }$ bits） through the full system model, including distortions,using different demapping algorithms.

Details specific to the two distortion scenarios are elaborated below.

## 4.0.1Scenario 1: nonlinear amplifier

A memoryless model was used to simulate a nonlinear power amplifier [22],where the model parameters were fit to data measured from an X-band TWTA. The level of distortion is controlled by the amplifier backoff, which is the average power of the input signal relative to the amplifier saturation point.A complex-valued polynomial with order 9 was used for predistortion, extracted using an indirect learning strategy with least squares [32]. We consider 64-APSK and 128-APSK constellations.Since the CCSDS standard is limited to modulation orders up to 64,we extended the CCSDS framework to include a 128- APSK constellation from the DVB-S2X standard [33]. The symbols are distributed in four or five constellation rings. There is no phase noise in this scenario.

## 4.0.2 Scenario 2: phase noise

A linear transmission channel is used, but phase noise is considered at the receiver. Phase noise was simulated at baseband using the phase noise mask from the receiver link in the DVB guidelines for the professional service scenario [34].Different levels of phase noise were simulated by shifting the entire mask to achieve a given level (in dBc/Hz) at a frequency offset of 10o Hz from the carrier frequency [24]. Rectangular 64-QAM and 128-QAM schemes were simulated.

## 4.1Maximum achievable rate

Independent of the demapping algorithm， the maximum achievable rate for the reduced channel model in Section 2.3 is given by the mutual information between the received and transmitted symbols.For a uniform input distribution, the mutual information is

$$
I ( Y ; X ) = { \frac { 1 } { M } } \sum _ { x \in S } \int p ( y | x ) \log { \frac { p ( y | x ) } { p ( y ) } } d y .\tag{16}
$$

The mutual information could be computed eficiently using an approximation to the entropy of a Gaussian mixture,e.g., [35],although a loss in accuracy is expected for high modulation orders.Instead, we calculate the maximum rate by numerical integration of (16) over $\mathbb { R } ^ { 2 }$ using a grid of $1 0 0 0 \times 1 0 0 0$ points.The integrand in (l6) can be easily evaluated since the PDFs are known from (1O).This maximum rate is independent of the demapper and serves as a benchmark for different demapping algorithms.

The achievable rate using a specific demapper can be computed from the mutual information between the extrinsic L values in (9) and the transmitted bits for the equivalent bit channels depicted in Fig.3.In this case, the rate was calculated using the area property of the extrinsic information transfer (EXIT) chart [36]. Specifically,a binary erasure channel was simulated as the extrinsic channel to provide varying amounts of a priori information to the demapper. For a given SNR and distortion level, the reduced channel model was simulated with $\sim 1 0 ^ { 7 }$ bits to compute the demapper's EXIT function using the extrinsic L values in (9).The function was evaluated atloo levels of a priori information between O and 1. The achievable rate for the demapper was computed with the mean (area) of the resulting EXIT function [36].

Figure 5 illustrates the maximum achievable rate for the proposed covariance-based demapper and the standard demapper. The nonlinear channel in scenario 1 was simulated with an amplifier backoff of 3 dB for two modulation schemes at various SNR levels.The achievable rate for the proposed demapper matches the theoretical maximum derived from the symbol-level channel model, demonstrating the optimality of the demapper. In contrast,the achievable rate of the standard demapper is reduced when the SNR is high.At high SNR, the symbol scattering is directional and mainly due the nonlinear distortion so knowledge of the covariance matrices is crucial to achieve maximum performance.It is also evident that there is a larger gain for the higher-order 128-APSK modulation.Note that the maximum rate for both modulation schemes is below the corresponding number of bits,even for infinite SNR,due to the fixed level of distortion.

![](images/3646ac139c6e7795017e0c4035b79f20df7e5c1f54633c34ab06c0bebb2c2157.jpg)  
Fig.5Maximum rate.Maximumachievable rate for different demappers for the nonlinear channel in scenario 1.The achievable rate for the proposed covariance-based demapper (solid line) and standard demapper (dashed line) is compared to the theoretical limit obtained from the symbol-level channel model (dots). Rates are plotted for 64-APSK and 128-APSK modulation schemes foran input power of -3 dB relative to amplifier saturation

To examine the effect of the distortion level on the demapper performance,we calculated the mutual information for SNR values between 5-30 dB and distortion levels defined by input powers between -1O and -2 dB. We define the gain as the difference in the achievable rate between the proposed demapper and the standard demapper. Figure 6 plots the achievable rate gain for a l28-APSK modulation scheme for different pairs of SNR values and distortion levels.We see that there is a gain in regions with high distortion and high SNR.This is expected since the symbol distributions are less isotropic,captured by the covariance of each cluster. We refer to this region as “distortion dominated" Conversely, regions with low SNR or low distortion have relatively circular and constant symbol covariances,so the gain is minimal. We refer to this region as (thermal) “noise dominated."The maximum gain is 0.16 bits per channel use,obtained when there is severe distortion and minimal noise.

![](images/5a7629b686c67a4144414a222acca7f8a2b55dcfbb92e87b3eb66b167c2d49ef.jpg)  
Fig.6 Gain in maximum rate. Gain in maximum achievable rate when using the proposed demapper for the nonlinear channel in scenario 1 using 128-APSK modulation.The gain is shown for various levels of distortion (controlled by the input power) and SNR values

Very similar plots for the case of phase noise in scenario 2 were generated (not shown for space limitations), where we consider the AWGN as thermal noise and phase noise as distortion.Analogous to the nonlinear channel, a large amount of phase noise creates very asymmetric covariances,which become the dominate source of error for sufficiently high SNR.

We remark that this analysis is ideal in the sense that the reduced channel model perfectly represents the received symbols.In a practical system,the bivariate Gaussian is an approximation of the effects of several communication components.We examine this approximation in more detail in the Appendix.In the next sections,we demonstrate that the superior performance of the proposed demapper is maintained for practical systems with non-Gaussian PDFs.

## 4.2 Bit error rates

We have shown a substantial gain in the maximum achievable rate when operating in a distortion dominated regime,where the symbol noise varies across the constellation.In this section, we examine how this gain translates to system performance by computing the bit error rate (BER) for different coding schemes.

As an initial experiment, we compute the BER using the proposed and standard demappers to make hard decisions about the transmitted bits. The BER in Fig.7 is for an uncoded system under scenario 1 with a nonlinear amplifier at input power of -5 and -3 dB for two different constellations. The proposed demapper incorporating symbol covariances lowers the uncoded BER in distortion dominated regions,when the SNR is high.The BER increases for a denser constellation (e.g.,128-APSK) or a higher level of distortion (input power of -3 dB). It is also clear that an“error floor”exists for each scheme,due to the fixed level of distortion.

![](images/a02a7136c379faf5323db22577bfe641efeb6bfa5730aa9f4a943b1042cd3b33.jpg)  
Fig.7 Uncoded BER.Bit error rate (BER) of uncoded transmission for the standard (dashed line) and proposed (solid line) demapper for a nonlinear amplifier under different input powers and modulation schemes

The uncoded simulations reenforce the common theme that demapping using the symbol covariance is advantageous for high SNR when the system is dominated by distortion. However, when error-correction is used, the threshold of the code also plays a significant role.Figure 8 illustrates the BER of a coded system for the same setup as Fig.7.Notice that there is minimal improvement in the BER for 64-ASPK modulation with coding,despite a large reduction in BER for the uncoded case.To explain this,imagine decoding with a hard decision demapper. Although the proposed demapper reduces the errors at high SNR,the code can already correct for this number of errors (in the order of $1 0 ^ { - 2 } )$ ，so further reduction is unnecessary.In other words,the information gain from the proposed demapper occurs at SNR values above the threshold of the code. Conversely, higher order schemes, such as 128-APSK, inherently require a higher SNR to achieve the same level of error, so the proposed demapper becomes beneficial. Thus, the performance of the coded system will be substantially improved for 128-APSK modulation with covariance-based demapping,as shown in Fig. 8.

![](images/173d2053f2e3196f7b490adfd0b2ab0a0c88d331baaa8a2b5bba782eeb40620a.jpg)  
Fig.8 Coded BER. Bit error rate (BER) using SCCC and turbo decoding for the standard (dashed line) and proposed (solid line) demapper for a nonlinear amplifier under different input powers and modulation schemes

The performance of the entire system with the proposed demapper depends on the modulation scheme, level of distortion,and the SNR threshold of the code. Figure 9 presents the required SNR to achieve a BER of $1 0 ^ { - 6 }$ when error-correction is used for the nonlinear amplifier in scenario 1.As the nonlinear distortion increases,the covariance-based demapper provides more accurate L values,which improves the decoder performance so it can operate at reduced SNR compared to the traditional demapper. The reduction in SNR is more pronounced as the spectral efficiency increases，e.g.，by increasing the code rate or modulation order. This highlights the interplay between the quality of the demapper output and the errors after decoding.It is also worth noting that the required SNR increases smoothly with the distortion level,which acts to balance the increased uncertainty due to nonlinear distortion by reducing the uncertainty due to thermal noise.

![](images/b12b5769c7c4567f603e3283fa302817978afcca974bec42ba5096aba15e3bc3.jpg)  
Fig.9 SNR threshold. Required SNR to achieve a BER of $1 0 ^ { - 6 }$ with coding using the standard (dashed line) and proposed (solid line) demapper for a nonlinear amplifier with different distortion levels

Figure 10 plots the required SNR to achieve a BER of $1 0 ^ { - 6 }$ for a coded system with phase noise,described in scenario 2.When we consider the phase noise as a distortion, separate from thermal noise,all the trends above are maintained.This demonstrates the utility of the proposed demapper for any system that can be modeled with data-dependent noise.

## 4.3Effect of the number of pilot symbols

The robustness of the demapper to imperfect mean and covariance estimates is investigated by varying the number of pilot symbols.We calculated the SNR required to achievea BER of $1 0 ^ { - 6 }$ with a varying number of pilots for the coded system with the nonlinear amplifier in scenario 1.Figure 11 demonstrates that increasing the number of pilots leads to improved performance until the required SNR reaches a plateau,at which point further improvements in the mean and covariance estimates do not improve the BER performance.For 128-APSK modulation,more pilots are required to reach optimal performance,due to the increased number of parameters to be estimated.Apart for a very low number of pilots,the performance is relatively stable and a graceful performance degradation is observed for decreasing number of pilots,demonstrating a reasonable robustness to inaccurate covariance estimation.

## 4.4 Iterative demapping and decoding

In this section, we demonstrate that the proposed demapper can also benefit applications with iterative demap-ping and decoding [7]. Iterative demapping methods are strongly dependent on the chosen bit labeling，e.g.，a Gray mapping exhibits little performance gain with joint demapping and decoding [37]. To provide a suitable example,we consider a coded system with phase noise described in scenario 2,with a 128-QAM constellation and a randomly generated bit labeling.With this bit labeling,the demapper will benefit from a priori information passed back from the decoder each iteration. We use the EXIT chart [36] to visualize iterations between the demapper and decoder in Fig.12. The simulation was conducted close to the threshold of the turbo code,with an $E _ { s } / N _ { 0 }$ of 25 dB,and phase noise of -43 dBc/Hz at a frequency offset of 1oo Hz. The standard demap-per generates less accurate L values,and consequently, the mutual information captured in the EXIT function is lower. This results in the iterative receiver terminating when the demapper's EXIT function intersects with that of the decoder (Fig.12a). The proposed demapper, on the other hand,hasa higher EXIT function,which allows for successful decoding using the a priori information generated from previous iterations (Fig.l2b).Successful decoding is achieved after two iterations.It is interesting to note that the turbo code is suboptimal in this example and below the maximum achievable rate,which could be obtained by designing a code/decoder to match the EXIT function of the demapper [38]. Nonetheless,this example demonstrates a clear advantage of the proposed demapper for iterative demapping and decoding.As with all joint demapping approaches, however, the performance gain will depend on the bit labeling and the particular coding scheme.

![](images/2e9e2c2551e70a4ed317a29c58669756a788fefca9e00023adfa9bb1fedb061b.jpg)  
Fig.10 SNR threshold. Required SNR to achieve a BER of $1 0 ^ { - 6 }$ with coding using the standard (dashed line) and proposed (solid line) demapper for different levels of receiver phase noise.The figure displays the phase noise level at 10o Hz from the carrier

![](images/e3cdafc305fda76e6062c8263b7026016f03a2d6a88407b9651b1b26ce5a9b32.jpg)  
Fig.11 Varying number of pilots. Required SNR to achieve a BER of $1 0 ^ { - 6 }$ with coding using the proposed demapper for a varying number of pilot symbols for a nonlinear amplifier under different input powers and modulation schemes

## 4.5Computational complexity

The proposed demapper using a bivariate Gaussian model requires more computation than the standard demapper using a circularly symmetric Gaussian model. The likelihood computation in (1O) requires a squared Mahalanobis distance of the form $( y - \mu ) ^ { T } \Sigma ^ { - 1 } ( y - \mu )$ . Assuming precomputed constants,the likelihood calculation requires seven multiplications.For a circularly symmetric Gaussian,this reduces to a Euclidian distance and the likelihood requires four multiplications.However, the extra computational cost must be placed in context of the overall demapper and the receiver in general.

![](images/12ae2bb4bec4be46bebb22eb751d83388b7810f4582eacbff2a4c6ad5468676e.jpg)

![](images/19628cf8314d12d1f409f5eb90d3886bf63b3a6044ebc2345f5017494b252765.jpg)  
Fig.12IterativedmapingEXIhartandcalculatedectoryforiterativeemapingnddecoingusigthetadardemappdte proposedemapperfora64-QAMsystemwithphasenoise.TheincreasedEXIfunctionforteproposeddemapperalowsiterationsbetweenthe turbo decoder and the demapper to achieve successful decoding

We conducted performance tests for our MATLAB implementation using both models,and there was less than 1% increase in execution time for demapping of 100 frames using the bivariate Gaussian model compared to the circularly symmetric Gaussian model. The cost of the extra multiplications is not significant compared to the other calculations required for demapping, e.g., the products and exponentials in (9). The demapper also represents a fraction(< 2%) of the computational cost for the whole receiver module,where the turbo decoder consumes much more of the execution time.This demonstrates that the improved performance of the proposed demapper is at the expense of only a mild increase in computation.

## 5Conclusions

This paper has presented a new demapper based on the symbol mean and covariance at each constellation point.The proposed demapper improves performance when the communication link is dominated by asymmetric distortions as opposed to thermal noise.The demapper is optimal since it can attain the maximum theoretical rate given by the data-dependent channel model. Depending on the coding scheme and level of distortion, substantial reductions were demonstrated in the SNR required for near error-free transmission in practical systems.

## Appendix

The proposed demapper works on the assumption that the conditional PDF for each constellation point is adequately represented by a bivariate Gaussian of the inphase and quadrature components. In this section，we explore this assumption in more detail. We approach this investigation from the perspective of model selection [39],which addresses the question of whether a bivariate Gaussian is a “better”model than a circularly symmetric Gaussian. We use the Akaike information criterion (AIC) to compare the two models [39]. The AIC provides a trade-off between the goodness of fit of a model and the number of parameters in the model.

![](images/1a4450ebfc3201ffef47d64393d2564278698880aa2459cc1b62603e8f367e7b.jpg)  
Fig.13 Goodness of fit.The true PDF (left),bivariate Gaussian fit (middle),and circularly symmetric Gaussian fit (right).A constellation point from the third ring (bottom) and fourth ring (top) of a 64-APSK constellation under nonlinear amplification with an input power of -3 dB relative to amplifier saturation. Corresponding values of Akaike information criterion (AlC) are displayed for each model (scaled by $1 0 ^ { - 7 } ) ,$ where lower values representa preferred model

Figure 13 depicts the true PDF using a histogram of $1 0 ^ { 8 }$ simulated symbols partitioned into $1 0 ^ { 4 }$ bins.These symbols are used to fit a bivariate Gaussian model and a circularly symmetric Gaussian model,and the AIC for each model is displayed. The bivariate Gaussian model provides a better fit (lower AIC) than the circularly symmetric version even after penalizing the extra degrees of freedom. The bivariate Gaussian model had a lower AIC for all points in the constellation although the difference between the models is smaller for points in the inner rings since these points have less distortion.For example,the AIC for a constellation point in the outer ring is $- 2 . 6 1 \times 1 0 ^ { 7 }$ for the bivariate Gaussian compared $\mathrm { t o } - 2 . 2 6 \times 1 0 ^ { 7 }$ for the circularly symmetric Gaussian.

It is important to consider that our ultimate goal of modeling the PDF is to efficiently compute likelihoods to provide to the decoder. In addition to fitting the true PDF better, the results in this manuscript demonstrate that L values from the bivariate Gaussian model enable more accurate decoding than the standard circularly symmetric Gaussian.

## Abbreviations

AIC:Akaike information criterion; APP:A posteriori probability; APSK: Amplitude and phase-shift keying; AWGN: Additive white Gaussian noise; BER: Bit error rate; EM: Expectation-maximization; EXIT: Extrinsic information transfer; GMM: Gaussian mixture model; NMSE: Normalized mean squared error; OFDM: Orthogonal frequency division multiplexing; PDF: Probability density function; QAM: Quadrature amplitude modulation; SNR: Signal-to-noise ratio

## Funding

This research was supported under Australian Research Council's Linkage Projects funding scheme (project number LP140101010)with industry partners Thales Alenia Space and Thales Australia.Azam Mehboob is a recipient of an Australian Government RTP Scholarship.

## Ethics approval and consent to participate

Not applicable.

## Authors'contributions

The authors have contributed jointly to allparts on the preparation of this manuscript,and all authors read and approved the final manuscript.

## Competing interests

The authors declare that they have no competing interests.

## Publisher's Note

Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Received: 28 January 2018 Accepted: 27April 2018

Published online: 16 May 2018

## References

1.G Karam, H Sari,A data predistortion technique with memory for QAM radio systems.IEEE Trans. Commun.39(2),336-344 (1991)

2.FM Ghannouchi,O Hammi,M Helaoui, Behavioral Modeling and Predistortion of Wideband Wireless Transmitters.(Wiley,Chichester, UK,2015)

3.B Ng, C-t Lam, D Falco,Turbo frequency domain equalization for single-carrier broadband wireless systems.IEEE Trans.Wirel.Commun. 6(2),759-767 (2007)

4．H Bolcskei, MlMO-OFDM wireless systems: basics,perspectives,and challenges.IEEEWirel.Commun.13(4),31-37 (2006)

5．E Biglieri,JProakis,S Shamai,Fading channels: information-theoretic and communications aspects.IEEE Trans.Inf.Theory.44(6),2619-2692 (1998)

6.RGGallager,Principles of Digital Communication.(Cambridge University Press, New York,2008)

7．Sten Brink,JSpeidel,R-H Yan,in IEEEGlobal Communications Conference (GLOBECOM).Iterative demapping and decoding for multilevel modulation (IEEE, Sydney,1998),pp.579-584

8.X Li,JA Ritcey,Bit-interleaved coded modulation with iterative decoding using soft feedback. Electron.Lett.34(10),942-943 (1998)

9. MC Valenti,S Cheng, Iterative demodulation and decoding of turbo-coded M-ary noncoherent orthogonal modulation.iEEE J.Sel. Areas Commun.23(9),1739-1747 (2005)

10.R Yen,P Diament, M Teich, Channel capacity and maximum-likelihood detection for atmospherically disturbed binary photocounting communications.IEEE Trans.Inf.Theory.18(2),302-304 (1972)

11.F Schreckenbach,N Gortz,J Hagenauer,G Bauch, Optimization of symbol mappings for bit-interleaved coded modulation with iterative decoding. IEEE Commun.Lett.7(12),593-595 (2003)

12.Q Xie,ZWang,Z Yang,Simplified soft demapper for APSK with product constellation labeling.IEEE Trans.Wirel. Commun.11(7),2649-2657 (2012)

13.R De Gaudenzi, M Luise,Analysis and design of an all-digital demodulator for trellis coded 16-QAM transmission over a nonlinear satellite channel. IEEETrans. Commun.43(2-4),659-668 (1995)

14.CE Burnet,Mitigation of adverse efects in the nonlinear satelite channel for 16QAM transmission.PhD thesis.(University of South Australia,2006)

15.G Dong,YPan,N Xie,CVaranasi,T Zhang,Estimating information-theoretical NAND flash memory storage capacity and its implication to memory system design space exploration.IEEE Trans. Very Large Scale Integr.(VLSl) Syst.20(9),1705-1714 (2012)

16.M Safari,in 2015 IEEE International Conference on Communication Workshop (ICCW).Eficient optical wireless communication in the presence of signal-dependent noise (IEEE,London,2015),pp.1387-1391

17.K-P Ho,JM Kahn, Electronic compensation technique to nitigate nonlinear phase noise.J.Light.Technol.22(3),779-783 (2004)

18.T Sakamoto,A Chiba,T Kawanishi,in Conference on Lasers and Electro-Optics Europeand 12th European Quantum Electronics Conference, CLEO EUROPE/EQEC2011.Nonlinear distortion of 16QAM constellations in intradyne coherent receiver,(Munich,2011),p.1

19.M Mondell,R Urbanke,SH Hassani,in 52nd Annual Allerton Conference on Communication, Control,and Computing.How to achieve the capacity of asymmetric channels,(Monticello,2014),pp.789-796

20.E Casini, R De Gaudenzi,A Ginesi, DVB-S2 modem algorithms design and performance over typical satelite channels.Int. J. Satell. Commun. Netw. 22(3),281-318 (2004)

21．N Kelly,M Allegue-Martinez, P-D Arapoglou,A Zhu, Bandwidthconstrained digital pre-compensation technique for multi-carrier satellite communications.Int.J.Satel.Commun.Netw.34(2),171-194 (2015)

22.A Ghorbani,M Sheikhan,in Sixth International Conference on Digital Processing of Signals in Communications.The effect of solid state power amplifiers (SSPAs) nonlinearities on MPSK and M-QAM signal transmission (IET,Loughborough,1991),pp.193-197

23．L Ding,GT Zhou, DR Morgan,Z Ma,JS Kenney,J Kim, CR Giardina, A robust digital baseband predistorter constructed using memory polynomials.IEEE Trans. Commun.52(1),159-165 (2004)

24.NJ Kasdin,Discrete simulation of colored noise and stochastic processes and 1/fα power law noise generation.Proc.IEEE.83(5),802-827(1995)

25.G Colavolpe,A Barbieri,G Caire,Algorithms for iterative decoding in the presence of strong phase noise.IEEE J.Sel.Areas Commun.23(9), 1748-1757 (2005)

26.Q Zou,A Tarighat, AH Sayed, Compensation of phase noise in OFDM wireless systems.IEEE Trans.Signal Process.55(11),5407-5424 (2007)

27.JSchäfer, K Strimmer,A shrinkage approach to large-scale covariance matrix estimation and implications for functional genomics.Stat. Appl. Genet. Mol. Biol.4(1),1-32 (2005)

28.ZZhu,AK Nandi,MWAslam,in IEEE Military Communications Conference, MILCOM 2013.Approximate centroid estimation with constellation grid segmentation for blind M-QAM classification (IEEE, San Diego,2013), pp.46-51

29.AP Dempster,NM Laird, DB Rubin, Maximum likelihood from incomplete data via the EM algorithm.J.R.Stat. Soc.Ser. B Methodol.39(1),1-38 (1977)

30.CM Bishop,Pattern Recognition and Machine Learning.(Springer, New York,2006)

31.The Consultative Committee for Space Data Systems (CCSDS), Flexible advanced coding and modulation scheme for high rate telemetry applications.Technical Report 131.2-B-1 (2012)

32.C Eun, EJ Powers,A new volterra predistorter based on the indirect learning architecture.IEEE Trans. Signal Process.45(1),223-227(1997)

33.European Telecommunications Standards Institute,Second generation framing structure,channel coding and modulation systems for Broadcasting, Interactive Services, News Gathering and other broadband satellite applications: part I: S2-extensions (DVB-S2X).Technical Report A83-2 (2014)

34.European Telecommunications Standards Institute, Implementation guidelines for the second generation system for Broadcasting, Interactive Services,News Gathering and other broadband satellite applications: part I: S2-Extensions (DVB-S2X).Technical Report A171-2 (2015)

35.MF Huber,T Bailey,H Durrant-Whyte, UD Hanebeck,in 2008 IEEE International Conference on Multisensor Fusion and Integration for Intelligent Systems.On entropy approximation for Gaussian mixture random vectors (IEEE,Seoul, Korea,2008),pp.181-188

36.A Ashikhmin,G Kramer,S ten Brink, Extrinsic information transfer functions: model and erasure channel properties.IEEE Trans.Inf.Theory. 50(11),2657-2673 (2004)

37.S ten Brink, Convergence of iterative decoding.Electron.Lett.35(10),806 (1999)

38.G Lechner,JSayir,ILand,in 2006 IEEE International Symposium on Information Theory. Optimization of LDPC codes for receiver frontends (IEEE,Seattle,2006),pp.2388-2392

39.KP Burnham,DR Anderson, Model Selection and Multimodel Inference: a Practical Information-theoretic Approach,2nd edn.(Springer,New York, 2002)

## Submit your manuscript to a SpringerOpen journal and benefit from:

Convenient online submission

■ Rigorous peer review

Open access: articles freely available online

→ High visibility within the field

Retaining the copyright to your article

Submit your next manuscript at V springeropen.com
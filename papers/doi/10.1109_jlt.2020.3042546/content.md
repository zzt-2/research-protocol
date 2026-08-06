JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1629 

# An Optimum Signal Detection Approach to the Joint ML Estimation of Timing Offset, Carrier Frequency and Phase Offset for Coherent Optical OFDM 

Xinwei Du _, Member, IEEE_ , Tianyu Song _, Member, IEEE_ , Yan Li , Ming-Wei Wu _, Member, IEEE_ , and Pooi-Yuen Kam _, Member, IEEE_ 

**_Abstract_ —Coherent orthogonal frequency-division multiplexing (OFDM) is one of the prime digital modulation techniques for present and future generations of wireless and optical communications. Accurate synchronization is the main obstacle to the implementation of a reliable OFDM receiver. We propose here a joint maximum likelihood (ML) estimator for the timing offset (TO), carrier frequency offset (CFO), and carrier phase offset (CPO) for coherent optical OFDM (CO-OFDM) motivated by the theory of ML signal detection. Our approach starts conceptually with the idea of first computing** **_L_ replicas of the original OFDM spectrum, where** **_L_ is a power of two and is assumed sufficiently large. This is done by padding (** **_L −_ 1)** **_N_ zeros to the end of the** **_N_ received noisy OFDM samples, where** **_N_ is the number of OFDM subcarriers. By computing the** **_LN_ -point discrete Fourier transform (DFT) of these** **_LN_ time samples, we get** **_L_ replicas of the DFT of the original OFDM spectrum, where each replica corresponds to the DFT for one hypothesized value of the CFO and the set of possible CFO values is** **_{l/L}_**<sup>**_L_**</sup> **_l_ =0**<sup>**_−_1.Weselectthe**</sup> **most probable replica by choosing the one that is at the minimum Euclidean distance from the original OFDM spectrum, which leads to a matched-filtering (MF) operation in the frequency domain in either a blind or a data-aided manner. Building on this MF concept, we then develop a joint ML estimator of the TO and CPO for each hypothesized value of the CFO. The novelty here is that the TO and the CPO are estimated efficiently as the frequency and phase of a complex sinusoid observed in noise, via either a time-domain or a** 

Manuscript received November 21, 2019; revised April 13, 2020, July 3, 2020, and September 14, 2020; accepted November 20, 2020. Date of publication December 4, 2020; date of current version March 16, 2021. This work was supported in part by UIC Start-up Research Fund under Grant R72021107, in part by NSFC under Grant 61571316 and Grant 61971372, and in part by HK RGC GRF under Grant 15200718. _(Corresponding author: Tianyu Song.)_ 

Xinwei Du is with the Division of Science and Technology, BNUHKBU United International College, Zhuhai 519087, China (e-mail: xinweidu@uic.edu.cn). 

Tianyu Song was with the Department of Electrical and Computer Engineering, National University of Singapore, Singapore 117583, Singapore. He is now with Huawei Technologies, Shenzhen 518129, China (e-mail: song.tianyu@u.nus.edu). 

Yan Li is with the School of Electronics and Information Technology, Sun Yat-Sen University, Guangzhou 510275, China (e-mail: liyan329@mail.sysu.edu.cn). 

Ming-Wei Wu is with the School of Information and Electronic Engineering, Zhejiang University of Science and Technology, Hangzhou 310023, China (e-mail: mingweiwu@ieee.org). 

Pooi-Yuen Kam is with the School of Science and Engineering, Chinese University of Hong Kong, Shenzhen 518172, China, and also with the Department of Electrical and Computer Engineering, National University of Singapore, Singapore 117583, Singapore (e-mail: pykam@cuhk.edu.cn). Color versions of one or more figures in this article are available at https: //doi.org/10.1109/JLT.2020.3042546. Digital Object Identifier 10.1109/JLT.2020.3042546 

**frequency-domain approach. The resulting joint CFO, CPO, and TO estimator is simpler than existing estimators, both conceptually and in implementation. A much simpler sequential approach in which we first decide on the CFO and then perform a joint TO and CPO estimation is also proposed. The performance loss of this sequential approach compared to the optimum joint approach is small at high signal-to-noise ratio (SNR). We obtain the performance of all our estimators via simulations, and show that they perform better when compared with the existing well-known estimators. Finally, we derive the Cramér–Rao lower bounds (CRLB) on the performance of our estimators, and show via simulations that our estimators for high SNR attain these performance lower bounds.** 

**_Index Terms_ —Carrier frequency offset, carrier phase offset, matched filter, maximum likelihood estimation, orthogonal frequency-division multiplexing (OFDM), timing offset.** 

## I. INTRODUCTION 

OHERENT optical orthogonal frequency-division multi- **C** plexing (CO-OFDM) has attracted much research attention due to its high spectral efficiency and its robustness to the chromatic dispersion (CD) and polarization mode dispersion (PMD)[1].InaCO-OFDMsystem,aserialhigh-ratedatastream is split into multiple parallel data streams with lower speed, each of which is modulated onto orthogonal subcarriers. The subcarriers are orthogonally overlapping with one another, leading to high spectral efficiency. However, synchronization errors in timing, frequency and phase can introduce both inter-symbol interference (ISI) and inter-carrier interference (ICI) that lead to severe performance degradation. The timing offset (TO) is caused by the propagation delay or the sample timing offset (frequency difference / phase offset) between the transmitter and receiver, and the carrier frequency offset (CFO) is induced by the frequency offset between the transmitter and receiver laser. The existence of a carrier phase offset (CPO) due to phase noise in the transmitter and receiver oscillators also causes signal constellation rotations in the subcarriers that can lead to bit error rate (BER) performance degradation. Therefore, achieving reliable synchronization is a major challenge for CO-OFDM systems. 

Many approaches for CO-OFDM synchronization are available in the literature by now. The most promising approach to 

0733-8724 © 2020 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1630 

the design of synchronization algorithms for any digitally modulated signal is to treat the TO, CFO and CPO as unknown nonrandomparameters,andapplythetheoryofmaximumlikelihood (ML) estimation [2]–[7]. However, when applied to OFDM, this approach has turned out to be analytically intractable so far, and no solution is yet available that leads to a simple practical implementation. This is because these references, by and large, rely on solving the highly nonlinear likelihood equations that result from setting to zero the derivatives of the likelihood function with respect to each of these parameters. Various other synchronization approaches that may not be optimum with respect to any statistical criterion have also appeared. We present here a survey of the principal techniques available that are more commonly used and whose performance will form the benchmarks for comparison with the ML estimators we will derive. References [5], [8]–[18] have proposed methods to estimate the TO and CFO either jointly or independently. In [8], Schmidl and Cox proposed a training symbol-based method, by designing the first OFDM symbol with two identical halves and calculating the timing metric to estimate the TO. However, there is a plateau in the timing metric, whose length is equal to the length of the cyclic prefix (CP). When the signal-to-noise ratio (SNR) is low, the existence of the plateau can cause large timing estimation errors. To decrease the uncertainty of TO estimation, in [9], the authors modified Schmidl’s method by dividing the training symbol into four identical parts, in which the first two parts have the same sign while the other two parts also have the same sign that are opposite to that of the first two parts. The resulting timing metric has a sharper roll-off, but still has a large timing-estimation error variance especially in ISI channels since there are two high side-lobes in the timing metric. In [10], Park utilized the conjugate symmetric sequence to design the training symbol structure, which leads to an even sharper peak, but the large side-lobes still exist which will affect the estimation accuracy significantly when the SNR is low. The OFDM signal is most sensitive to CFO, since the CFO causes the loss of orthogonality between the subcarriers, which introduces ICI to the system. The CFO normalized by the OFDM subcarrier spacing comprises an integral part and a fractional part. The work of [8] estimates the fractional part of the CFO by taking the correlation between the two identical halves in the training symbol and computing the phase of the correlation. However, the estimation of the integral part requires an exhaustive search, which leads to a high computational complexity. To ensure the CFO estimation stability under poor SNR conditions, in [12], the training symbol design is done in the frequency domain, and contains several data blocks. The CFO estimate is obtained via a two-step iterative operation in order to achieve better CFO estimation accuracy. In general, the data-aided (DA) approaches are easy for implementation; however, they require the insertion of a pilot symbol before each OFDM frame, which decreases the effective data transmission bit rate. Blind (BL) approaches can avoid this problem, and are common in applications. A deterministic blind approach in [13] makes use of a cost function that the authors approximated by a cosine function. The CFO estimate is obtained by solving three equations in the nonlinear cosineformatthatareobtainedfromthreetestvaluesgivenbythe 

received signal samples. This approach is simple, but is sensitive to the SNR. Severe CFO estimation performance degradation may appear at low SNR. 

Although one can propose various synchronization techniques [15]–[18], we feel that ultimately, the most reliable approach is to apply ML estimation theory. Our novel conceptual approach here begins by computing the OFDM spectrum at multiple hypothesized values of the CFO from the received noisy signal samples. The received time-domain signal of _N_ samples is first zero-padded to the length of _LN_ by padding ( _L −_ 1) _N_ zeros to the end of the signal. After performing the _LN_ -point DFT, the spectrum obtained contains _L_ noisy replicas of the original OFDM spectrum, each replica corresponding to one possible value of the CFO. The ML estimation of the CFO now amounts to a minimum-error-probability decision on which replica of the computed spectrum contains the original OFDMspectrum.Fromfirstprinciplesincommunicationtheory, the optimum decision is the one at the minimum Euclidean distance from the original OFDM spectrum, and the search for this optimum leads to a matched-filtering (MF) operation in the frequency domain. The MF concept obviates the need to solve a complicated likelihood equation, i.e., the equation obtained by equating to zero the derivative of the likelihood function with respect to the CFO. Solving the likelihood equation is the main obstacle so far in applying the ML principle to CFO estimation for CO-OFDM. The on-line implementation of the MF approach isefficientandconceptuallysimple.BothDAMLandBLMLestimation of CFO are achievable via the MF concept, and we will show that the estimation error variance of the DA ML estimator asymptotically reaches the Cramér-Rao lower bound (CRLB) as SNR increases, i.e., the estimator is asymptotically efficient. 

Building on the MF concept, we develop a joint ML estimator for the CFO, CPO and the TO of an OFDM signal. For each discrete hypothesized value of the CFO, the receiver computes the joint ML estimates of the CPO and TO. The key novelty here is that we compute the latter joint estimates as the ML estimates of the frequency and phase of a complex sinusoid of constant amplitude observed in additive white Gaussian noise (AWGN). These ML estimates can be computed explicitly via the time-domain estimator in our work in [19], or the frequencydomain technique in [20] that involves a search for the peak of a periodogram. The MF CFO estimator coupled with the novel ML CPO and TO estimator leads to a much simpler receiver than existing ones. To reduce the implementation complexity, we propose a suboptimum sequential approach in which we first obtain the ML CFO estimate, followed by the joint ML estimation of CPO and TO corresponding to the CFO estimate obtained. The performance loss of this sequential approach compared to the optimum joint approach is small at high SNR. We obtain the performance of all our estimators via simulations, and show that they perform better when compared with the existing well-known estimators mentioned above. Finally, we derive the CRLBs on the performance of our estimators, and show via simulations that our estimators for high SNR attain these performance lower bounds. 

The paper is organized as follows. Section II introduces the signal model. The proposed joint ML parameter estimator is 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1631 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 



Fig. 1. Schematic diagram of a coherent OFDM system. S/P: serial to parallel, (I)DFT: (inverse) discrete Fourier transform, CP: cyclic prefix, DAC: digital to analog converter, IQ Mod.: IQ modulator. The value of _Nt_ is equal to _N_ plus the length of CP. 

derived in Section III. Section IV shows a sequential parameter estimator with much simpler implementation. Section V derives the performance bounds. Section VI provides the simulation results and the discussion of the performance comparison. Finally, Section VII concludes the paper. 

## II. SIGNAL MODEL 

The schematic diagram of a CO-OFDM system is shown in Fig. 1. According to Fig. 1, the _n_ -th received time-domain OFDM sample _r_ ( _n_ ) after removing the CP, with the appearance of TO, CFO and carrier phase noise (CPN), can be expressed as [1], [5]: 



where we have _n_ = 0 _,_ 1 _, . . . , N −_ 1. Term _N_ is the number of subcarriers, _x_ ( _n_ ) is the _n_ -th transmitted OFDM sample, which is obtained by taking the _N_ -point inverse discrete Fourier transform(IDFT)ofthedataspectrum _{X_ ( _k_ ) _}_<sup>_N_</sup> _k_ =0<sup>_−_1,where</sup><sup>_X_(</sup><sup>_k_)</sup> is the data on the _k_ -th subcarrier and can be expressed as [1]: 



Note that the TO denoted by _τ_ is in the units of sample period ( _Ts_ ) which is assumed to be within the range of [0 _, N −_ 1]. Term _h_ ( _n_ ) is the channel impulse response, which in general represents the dispersive channel, including the CD and PMD. Term _w_ ( _n_ ) is the _n_ -th complex additive white Gaussian noise (AWGN) sample with mean 0 and variance _σ_<sup>2</sup> , and _⊗_ denotes the convolution operation. Term _ϵ_ is the normalized CFO which is equal to the value of actual CFO normalized by the OFDM subcarrier spacing, and can be divided into an integral part and a fractional part. The carrier phase, represented by _θ_ ( _n_ ), is a 

Wiener process modelled by [1]: 



The carrier phase is noisy or randomly time-varying, consisting of the sum of a constant term _θ_ 0 and a sequence _{ν_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1</sup> of independent and identically distributed Gaussian random variables, each with mean zero and variance _σp_<sup>2= 2</sup><sup>_π_Δ</sup><sup>_νTs_. The</sup> constant term _θ_ 0 is the CPO that is normally thought of as the common phase error, and the sequence _{θ_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1is the CPN.</sup> In order to illustrate clearly our conceptually novel joint ML estimation approach, we have to somewhat limit the complexity of our system model. That way, it is analytically tractable, and leads to explicit theoretical results that provide a practical implementation. We first assume the channel is non-dispersive so that the channel impulse response is just an impulse, i.e., _h_ ( _n_ ) = _δ_ ( _n_ ). This assumption also means that the nonlinearities and dispersion that includes CD and PMD in the optical channel have been totally compensated and removed by optical means. This assumption has been commonly used in the recent literature [16], [21]–[23]. 

In addition, we assume in the estimator derivation that the CPN variance _σp_<sup>2iszero,andthereforethecarrierphaseisa</sup> constant and equal to the CPO _θ_ 0. This assumption is commonly used in practice [24], [25], because tracking a time-varying phase introduces much more analytical difficulties. Later, we will use simulations to show the estimation performance with the appearance of CPN. The theoretical development incorporating on the dispersive channel and the phase noise will be considered in our future work. Here we focus on the estimation of CFO, CPO and TO, which are all assumed to be constant. Then based on these assumptions, the signal model in (1) can be simplified to: 



Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1632 

In addition, in order to cope with the TO estimation range of [0 _, N −_ 1], we assume that the first two OFDM symbols are pilot symbols which are known to the receiver, and the second OFDM symbol is identical to the first. Assume without loss of generality that the pilot symbols are _M_ PSK modulated, so that they have the constant amplitude, i.e., _|X_ ( _k_ ) _|_<sup>2</sup> = _A_ . 

The time-domain SNR _γt_ is defined as: 



where _Ex_ denotes the average energy per transmitted sample in the time domain, i.e., _Ex_ = _E_ [ _|x_ ( _n_ ) _|_<sup>2</sup> ]. In Appendix A, we will show that the time-domain SNR is the same as the frequencydomain SNR, _γf_ , defined as: 



where _Es_ denotes the average energy per subcarrier, i.e, _Es_ = _E_ [ _|X_ ( _k_ ) _|_<sup>2</sup> ], where _k_ = 0 _,_ 1 _, . . . , N −_ 1. Term _σW_<sup>2isthevari-</sup> ance of _W_ ( _k_ ), where _{W_ ( _k_ ) _}_<sup>_N_</sup> _k_ =0<sup>_−_1isthefrequency-domain</sup> AWGN that results from performing the _N_ -point DFT of the time-domain AWGN, i.e., _{w_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1.WeshowinAppendix</sup> A that: 



Thus, we get: 



From here on, we denote the SNR as _γ_ . 

## III. JOINT MAXIMUM LIKELIHOOD PARAMETER ESTIMATION 

## _A. Overall General Approach_ 

The optimum approach for estimating the CFO, CPO and TO is to design a joint ML estimator of all the parameters based on the observations of the OFDM samples over one symbol interval. This subsection will explain the general principle of the joint ML parameter estimator. 

Since _{w_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1isasequenceofindependent,identi-</sup> cally distributed, complex, AWGN, the likelihood function _p_ ( _{r_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1</sup><sup>_|τ, ϵ, θ_) can be written as:</sup> 



The ML estimates (ˆ _τ,_ ˆ _ϵ, θ_<sup>ˆ</sup> ) of the parameters ( _τ, ϵ, θ_ ) are the values which jointly maximize the likelihood function, i.e.: 



Thus the ML estimates (ˆ _τ,_ ˆ _ϵ, θ_<sup>ˆ</sup> ) are the solutions of (11), which are shown as follows: 





It is obvious from the literature [24], [26] that it is analytically difficult even if not impossible to obtain explicit solutions of the three equations in (11). Thus, we propose here an alternative approach for joint estimation of CFO, CPO and TO, by using the communication theoretic concept of viewing the ML estimator as the minimum-error-probability signal detector. Supposing the signal samples after removing the CP given in (4) have been received. We pad ( _L −_ 1) _N_ zeros at the end of the _N_ received samples, so that we get a sequence of _LN_ samples _{rLN_ ( _n_ ) _}_<sup>_LN_</sup> _n_ =0<sup>_−_1, which can be expressed as:</sup> 



Here, we call _L_ as the zero-padding factor, which is a power of 2. Then by taking the _LN_ -point DFT of _rLN_ ( _n_ ), we obtain the noisy received OFDM symbol with CFO at _LN_ discrete frequency points, i.e., _{ LN_<sup><u>2</u></sup><sup>_<u>π</u>k}_</sup> _k_<sup>_LN_</sup> =0<sup>_−_1.Thereceivedsampleon</sup> the _k_ -th frequency _RLN_ ( _k_ ) in the frequency domain, for each _k_ = 0 _,_ 1 _, . . . , LN −_ 1, can be written as: 



where we have _WLN_ ( _k_ ) =<sup>�</sup><sup>_N_</sup> _n_ =0<sup>_−_1</sup><sup>_w_(</sup><sup>_n_)</sup><sup>_e−j_</sup><sup><u>2</u></sup> _LN_<sup>_<u>πkn</u>_</sup> _._ Next, we de- 



where _k_ = 0 _,_ 1 _, . . . , LN −_ 1. Actually, term _{XLN_ ( _k_ ) _}_<sup>_LN_</sup> _k_ =0<sup>_−_1</sup> is the _LN_ -point DFT of the zero-padded _LN_ -point time-domain samples _{{x_ ( _n − τ_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1</sup><sup>_,_0</sup><sup>_, . . . ,_0</sup><sup>_}_.Basedon(13)andthe</sup> DFT property that a time shift in the time domain causes a phase shift in the frequency domain, and vice versa, (13) can be written as: 



First, we think of the calculated spectrum of _LN_ samples in (15) as being made up of _L_ sets where the _l_ -th set _Sl_ is given by: 



This set _Sl_ is the spectrum that corresponds to the hypothesized value ˜ _ϵl_ for the CFO, which can be expressed as: 



Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1633 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 



Fig. 2. Schematic diagram the joint MF ML parameter estimator, with the assumption that _τ ∈_ [0 _, N −_ 1] and the first two OFDM symbols are known and identical to each other. 

For simplicity, we first assume that _L_ is sufficiently large so that the actual CFO is equal to one of the hypothesized values in _{ϵ_ ˜ _l}_<sup>_L_</sup> _l_ =0<sup>_−_1.Thefinesearchwillbeintroducedlater.Notethat</sup> for each set _Sl_ , the set of noise samples, _Wl_ = _{WLN_ ( _k_ ) _, k_ = _l, l_ + _L, . . . , l_ + ( _N −_ 1) _L}_ , is a set of AWGN samples. It is easy to show that the elements in _Wl_ are mutually independent of one another, each with mean 0 and variance _σW_<sup>2=</sup><sup>_Nσ_2.</sup> However, considering all the elements in _{WLN_ ( _k_ ) _}_<sup>_LN_</sup> _k_ =0<sup>_−_1, the</sup> noise samples are not all independent of one another [27]. The hypothesized values of CFO in (17) are actually the possible radian frequencies of the CFO, thus the corresponding possible values of the normalized CFO are _{ϵl_ = _l/L}_<sup>_L_</sup> _l_ =0<sup>_−_1, and</sup> we have _l_ = _ϵlL_ . In the subset _Sl_ given in (16), the _m_ -th element at frequency point _k_ = _l_ + _mL_ is given by: 

_RLN_ ( _k_ ) _|k_ = _l_ + _mL_ = _RLN_ ( _ϵlL_ + _mL_ ) 



Here, by defining 



the _l_ -th set _Sl_ in (16) can be rewritten as: 



For further simplification, we define: 



Since for each _l_ , _{WLN_ ( _ϵlL_ + _mL_ ) _}_<sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1isactuallyan</sup><sup>_N_-</sup> sample complex AWGN in the index _m_ , with each element having mean 0 and variance _Nσ_<sup>2</sup> , and each sample can be written as _V_ ( _m_ ) _∼CN_ (0 _, Nσ_<sup>2</sup> ). Then, (18) can be further simplified as: 



where we have _m_ = 0 _,_ 1 _, . . . , N −_ 1 and _l_ = 0 _,_ 1 _, . . . , L −_ 1. Equation (22) gives the model of the _m_ -th element in the _l_ -th set _Sl_ in (16). 

The schematic diagram of the joint ML parameter estimator is shown in Fig. 2. The received _LN_ -point spectrum _{RLN_ ( _k_ ) _}_<sup>_LN_</sup> _k_ =0<sup>_−_1</sup> is first demultiplexed into _L_ sets, where the input to the _l_ -th branch in the figure is the _l_ -th set _Sl_ , which corresponds to the hypothesized CFO _ϵl_ . In the _l_ -th branch, if the hypothesis that _ϵ_ = _ϵl_ is correct, (22) can be expressed as: 



where based on (14), we have: 



since the first two OFDM symbols are identical, the TO _τ_ is a circular shift of _{x_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1.Term</sup><sup>_X_(</sup><sup>_m_)istheDFTofthe</sup> transmitted samples which is defined in (2). Thus, (23) can be further simplified to: 



The result in (25) shows that if the hypothesis _ϵ_ = _ϵl_ is correct, then the _l_ -th signal set _Sl_ = _{RLN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1wouldconsistof</sup> the signal _{X_ ( _m_ ) _e_<sup>_−j_[</sup><sup><u>2</u></sup><sup>_<u>πmτ</u>_</sup> _N −θ_ ] _}Nm−_ =01<sup>plus AWGN</sup><sup>_{V_(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1.</sup> Since all the hypotheses _{ϵ_ = _ϵl}_<sup>_L_</sup> _l_ =0<sup>_−_1are assumed equally likely,</sup> it is well known from communication theory that the most likely hypothesis is that _ϵ_ = _ϵl_ for which the Euclidean distance between the _l_ -th signal set _Sl_ and the desired signal _{X_ ( _m_ ) _}_<sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1</sup> is a minimum. This Euclidean distance is given by: 



where R _{·}_ means taking the real part. We note that our decision problem here involves only one message, namely, _{X_ ( _m_ ) _}_<sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1,and</sup><sup>_L_possiblenoisyreceivedsignals,namely,</sup> 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1634 

_Sl, l_ = 0 _, . . ., L −_ 1. The problem is to determine the most likely received signal. In the common receiver decision problem, there is only one noisy received signal and multiple possible messages from which the receiver picks one as the decision. The conceptual difference between the two problems is small. Another point to note is that the Euclidean distance in (26) also depends on _τ_ and _θ_ , and has to be minimized with respect to these two parameter. As can be seen from (22) and (26), term � _Nm−_ =01<sup>_|R_</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_|_2providesnoinformationabout</sup><sup>_ϵ_.Thus,it</sup> can be discarded. Term<sup>�</sup><sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1</sup><sup>_|X_(</sup><sup>_m_)</sup><sup>_|_2isaconstantbecause</sup> the data is modulated onto _M_ PSK. Even for _M_ QAM, this is a constant for a given OFDM spectrum, and contains no information about _ϵ_ , thus can also be discarded. Therefore, the ML estimator chooses the hypothesis _ϵ_ = _ϵl_ that maximizes the term: 



As shown in Fig. 2, the receiver generates the sequence _{R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1foreachsignalset</sup><sup>_Sl, l_= 0</sup><sup>_,_1</sup><sup>_, . . . , N−_1,</sup> where 



If the hypothesis that _ϵ_ = _ϵl_ is correct, we then have from (23) that 



where the phase of _X_ ( _m_ ) is removed. Since _X_ ( _m_ ) is _M_ PSK modulated, its amplitude is a constant, i.e, _|X_ ( _m_ ) _|_<sup>2</sup> = _A_ . Thus (29) can be further written as: 



Here we have _W_ ( _m_ ) = _V_ ( _m_ ) _X_<sup>_∗_</sup> ( _m_ ), where _{W_ ( _m_ ) _}_<sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1is</sup> complex AWGN with each _W_ ( _m_ ) _∼CN_ (0 _, ANσ_<sup>2</sup> ). At this point, we consider minimizing the Euclidean distance in (26) with respect to _τ_ and _θ_ by maximizing _C_ ( _l_ ) in (27). 

In (30), by regarding the index _m_ as the ‘time’ index, the signal _{R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1for the</sup><sup>_l_-th hypothesized value of CFO</sup> in (30) can be seen as the samples of a complex single sinusoid observed in AWGN, with the frequency of _−_ 2 _πτ/N_ , phase _θ_ and constant amplitude _A_ . Thus, the joint estimation of _τ_ and _θ_ corresponding to the _l_ -th hypothesized value of the CFO reduces to the estimation of the parameters of a single sinusoid in noise. This estimation can be realized by either the ‘time-domain’ approach in [19] or ‘frequency-domain’ approach in [20]. We will show the details of the approaches in the next subsection. For the _l_ -th hypothesized value of CFO, based on (30), we can obtain the joint ML estimates of TO and CPO, i.e., (ˆ _τ |ϵl , θ_<sup>ˆ</sup> _|ϵl_ ). Then (ˆ _τ |ϵl , θ_<sup>ˆ</sup> _|ϵl_ ) is used for compensating the corresponding set _{R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1. The</sup><sup>_m_-th element of the compensatedsignal</sup> at _l_ -th branch can be expressed as: 



where we have _m_ = 0 _,_ 1 _, . . . , N −_ 1 and _l_ = 0 _,_ 1 _, . . . , L −_ 1. As can be seen from (30) and (31), if the hypothesized CFO _ϵl_ is 

equal to the exact value of the CFO, and if the estimates of TO ˆ and CPO are very accurate, i.e., _ϵl_ = _ϵ_ , _τ |ϵl_ = _τ_ and _θ_<sup>ˆ</sup> _|ϵl_ = _θ_ , then _Z_<sup>(</sup><sup>_l_)</sup> ( _m_ ) is a constant observed in AWGN, i.e.: 



Term _WR_ ( _m_ ) is the real part of _W_ ( _m_ ), which is real AWGN, i.e., _WR_ ( _m_ ) _∼N_ (0 _,_<sup>_<u>AN</u>_</sup> 2<sup>_σ_2). Following (27), we take the sum-</sup> mation of _Z_<sup>(</sup><sup>_l_)</sup> ( _m_ ) over _m_ , then find the set of _{ϵl,_ ˆ _τ |ϵl , θ_<sup>ˆ</sup> _|ϵl }_<sup>_L_</sup> _l_ =0<sup>_−_1</sup> that gives the best match. The matched signal _C_ ( _l_ ) can be written as: 



In (33), when there is no AWGN, there will be a single peak with amplitude of _AN_ at _l_ = _ϵL_ . 

Note that (30)-(33) hold if and only if _ϵl_ matches with _ϵ_ . Otherwise, _XLN_ [( _ϵl − ϵ_ ) _L_ + _mL_ ] will not match with _X_ ( _m_ ), so that we cannot get a constant phase, and the phase after the correlation in (29) is time-varying and unknown. Specifically, if _ϵl_ is not equal to the actual CFO _ϵ_ , the constellation phase removal step in (28) will become: 



where we have 



The detailed derivation of the expression for _A_<sup>(</sup><sup>_l_)</sup> ( _m_ ) is shown in Appendix B. By comparing (34) and (30), it can be observed that the only difference is the amplitude. In (30), the amplitude is a realconstant _A_ ,whilein(34),i.e.,inthecasewhere _ϵl_ isnotequal to the actual CFO _ϵ_ , the amplitude is _A_<sup>(</sup><sup>_l_)</sup> ( _m_ ) _e_<sup>_−j_[</sup> 2 _π_ <u>(</u> _ϵNl−ϵ_ <u>)</u> _τ_ ] which is complex, depends on _ϵ_ and _τ_ , and varies with the ‘time-index’ _m_ . To our knowledge, there is no existing technique to estimate _τ_ and _θ_ accurately for a single sinusoid with an unknown time-varying amplitude and phase. All existing methods, such as those in [19], [20], will generate very inaccurate estimates due to the phase disturbances caused by the mismatch. Thus, the joint ML parameter estimator works in favour of the correct set that corresponds to the actual CFO. 

In addition, in (34), even if TO and CPO are perfectly compensated, the final correlator output signal is still smaller than in the case of _ϵl_ = _ϵ_ . Here, based on (31) and (B.4), and supposing there is no AWGN, the correlator output signal can be expressed as: 



which is obviously less than _AN_ . 

Finally, the joint ML parameter estimates (ˆ _ϵ,_ ˆ _τ, θ_<sup>ˆ</sup> ) can be obtained by finding the index<sup>ˆ</sup> _l_ which gives the best match in the 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1635 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 

sense of maximizing _{C_ ( _l_ ) _}_<sup>_L_</sup> _l_ =0<sup>_−_1, i.e.:</sup> 



Then we have: 



In the next subsection, we will show how to do the joint ML estimation of _τ_ and _θ_ for each hypothesized value of CFO. 

## _B. Joint ML Estimation of to and CPO_ 

_1) ‘frequency-Domain’ Approach:_ To estimate the TO and the CPO, here we follow the approach in [20]. In the case of _ϵl_ = _ϵ_ , by regarding the index _m_ as the ‘time’ index, and taking the _N_ -point DFT of the ‘time-domain’ samples _{R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1</sup> in (30), we introduce another frequency index _ν_ , and compute the spectrum as: 



where we have _ν_ = 0 _,_ 1 _, . . . , N −_ 1 and _WF_ ( _ν_ ) = � _Nm−_ =01<sup>_W_(</sup><sup>_m_)</sup><sup>_e−j_2</sup><sup>_πmν/N_.</sup> 

As can be seen in (39), if _ϵl_ is equal to _ϵ_ , in the absence of noise, we can get a single peak of the amplitude spectrum at the frequency of _ν_ = _−τ_ , which is equal to _AN_ . Thus, the ML estimates of the TO and CPO, i.e., _τ_ ˆ _F |ϵl_ = _ϵ_ and _θ_<sup>ˆ</sup> _F |ϵl_ = _ϵ_ , can be obtained by searching for the frequency index _ν_ that maximizes _|RF_ ( _ν_ ) _|_ , and the phase of the peak is the estimated CPO, i.e., 



Since _τ_ is an integer, when SNR is low, the estimation error variance of _τ_ may become large. To improve the estimation accuracy, as was done in [20], we pad _L_<sup>_′_</sup> ( _N −_ 1) zeros after _{R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1where</sup><sup>_L′_isthecorrespondingzero-padding</sup> factor, then perform the _L_<sup>_′_</sup> _N_ -point DFT as was done in (39). Similar to our MF ML CFO estimator, a fine search is required as shown later in (48). Reference [20] has indicated that the zero-padding rate of four for the coarse search is enough to get a good estimation performance. 

However, in the case that the hypothesized CFO _ϵl_ is not equal to the exact value of CFO, i.e., _ϵl_ = _ϵ_ , when performing 

the _N_ -point DFT as in (39), we have: 



By taking the absolute value of _RF_ ( _ν_ ) _|ϵl_ = _ϵ_ , we can obtain from the detailed calculation of (41) in (B.4) that: 



It can be observed from (41) that if _ϵl_ = _ϵ_ , we will obtain a broadened spectrum. Also, comparing (42) with (39) that has a single peak at the frequency _ν_ = _−τ_ , the amplitude _|RF_ ( _ν_ ) _|ϵ_ ˆ= _ϵ|_ is just the amplitude of AWGN. Therefore, we can obtain the single peak if and only if _ϵl_ = _ϵ_ . 

_2) ‘Time-Domain’ Approach:_ As mentioned above, the joint estimation of TO and CPO can also be realized in the ‘time domain’. In [19], the frequency and phase of a complex single sinusoid with constant amplitude are obtained by solving the likelihood function. Explicit analytical results are given in [15, Eq. (16) and (17)]. Here, in the case of _ϵl_ = _ϵ_ , by applying our previous ML approach in [19], the estimation of TO and CPO reduces directly to calculating the frequency and phase of a sinusoid, respectively. The corresponding analytical results of _τ_ ˆ _T |ϵl_ = _ϵ_ and _θ_<sup>ˆ</sup> _T |ϵl_ = _ϵ_ are expressed in (43) and (44), as shown at the bottom of this page. In addition, it is obvious that when _ϵl_ = _ϵ_ , using (43) and (44) will lead to very inaccurate results since _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_|ϵ_</sup> _l_<sup>=</sup><sup>_ϵ_is a</sup><sup>_ϵ_-dependent term, as can be seen from</sup> (34). As can be seen in (43) and (44), since the actual phase data sample is obtained from the principal argument of _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_),</sup> which is within the interval [ _−π, π_ ), phase unwrapping is required to generate ∠ _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_). Here, we utilize the differential</sup> phase unwrapping method proposed in [28], to unwrap the phase ∠ _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_) into the correct range. To unwrap the phase,</sup> we first calculate the phase difference between two adjacent samples, i.e., Δ( _m_ ) = arg[ _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_+ 1) ˜</sup><sup>_R_</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_∗_].Thefirst</sup> data sample at time _m_ = 0, is an observation on the phase _φ_ alone. If _−π ≤ R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(0)</sup><sup>_≤π_,thenasequenceofangledata</sup> _{ψ_ ( _m_ ) _}_<sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1can be computed as:</sup> 





Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1636 





In order to obtain more accurate observation data, the phase of _R_ ˜ _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_) is collected by unwrapping arg</sup><sup>_{R_˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}_to within</sup> a 2 _π_ -interval centered around the computed value _ψ_ ( _m_ ), i.e., the value of ∠ _R_<sup>˜</sup> _LN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)chosenistheonelyingintheinter-</sup> val [ _ψ_ ( _m_ ) _− π, ψ_ ( _m_ ) + _π_ ), where _m_ = 0 _,_ 1 _, . . . , N −_ 1. The necessary condition for a good performance of this phase unwrapping operation is that Δ( _m_ ) satisfies [28]: 



_3) Discussion of the ‘Time-Domain’ and ‘FrequencyDomain’ Approaches:_ The ‘frequency-domain’ approach is conceptually easy to implement, and the ML estimation of TO and CPO does not involve the phase unwrapping issues. However, a search is required, and to get accurate estimation result, zero-padding needs to be performed which enlarges the number of searches and increases the complexity. Moreover, the probability of obtaining a local optimum result increases with the decrease of SNR. 

The ‘time-domain’ approach gives explicit analytical expressions of the TO and CPO ML estimates without exhaustive search, and has much lower complexity compared with the ‘frequency-domain’ method. However, the ‘time-domain’ approach needs to perform phase unwrapping, and it is worth noting that at low SNR, both ‘time-domain’ and ‘frequencydomain’ methods show estimation performance degradation. 

## _C. Fine Search_ 

Since we assume that the actual CFO is equal to one of the hypothesized values in (17), to get accurate estimation performance of CFO, TO and CPO, the zero-padding factor _L_ has to be sufficiently large, which may lead to a high computational complexity. To ensure both the estimation accuracy and low complexity, here we propose a scheme that involves a one-step fine search of the CFO, followed by a recalculation of joint ML estimates of TO and CPO. 

Based on (33), the fine search is realized by using a numerical method, i.e., the secant method [20]. The fine search problem becomes locating the zero point in _C_<sup>_′_</sup> ( _l_ ) with _C_<sup>_′′_</sup> ( _l_ ) _<_ 0. Here term _C_<sup>_′_</sup> ( _l_ ) and _C_<sup>_′′_</sup> ( _l_ ) represent the first order and second order differentiation of _C_ ( _l_ ) given in (27), respectively. The gradient calculation of a discrete signal is defined in the same way as MATLAB does, i.e.: 



If _C_<sup>_′_</sup> (<sup>ˆ</sup> _l_ ) _>_ 0, then the index of the actual peak, denoted by<sup>˜</sup> _l_ , is on the right hand side of<sup>ˆ</sup> _l_ . On the other hand, if _C_<sup>_′_</sup> (<sup>ˆ</sup> _l_ ) _<_ 0,<sup>˜</sup> _l_ is on the left hand side. Therefore, the final estimated peak index of _C_<sup>_′_</sup> ( _l_ ) by using the secant method is given by [20]: 



Then based on (48), the final ML estimate of CFO can be expressed as: 



After obtaining _ϵ_ ˆ, we first do the CFO compensation, then calculate _τ_ ˆ and _θ_<sup>ˆ</sup> by either the ‘time-domain’ [19] or the ‘frequency-domain’ [20] approach. 

Based on the above analysis, we can easily conclude that the proposed joint ML approach has full CFO estimation range, TO estimation range of [0 _, N −_ 1], and CPO estimation range of [ _−π, π_ ). For CFO estimation, to obtain the fractional part, we just take the value of _l_ from 0 to _L −_ 1 with the step of 1. To obtain the integral part, then the value of _l_ should be taken from 0 to ( _L −_ 1) _N_ , with the step of _N_ . 



Since for each hypothesized value of CFO, the joint MF ML parameter estimator needs to search for all the possible values of _τ_ and _θ_ , and the fine search step needs to be performed, the resulting implementation complexity will be high. Here we further develop a sequential approach which is suboptimal and proposed for arriving at a much simpler implementation. The schematic diagram of the sequential MF ML estimator is shown inFig.3.Inoursequentialapproach,theMLCFOestimateisfirst obtained by taking the sum of the magnitudes of the received signal set _{RLN_<sup>(</sup><sup>_l_)(</sup><sup>_m_)</sup><sup>_}N_</sup> _m_<sup>_−_</sup> =0<sup>1in(22),oneforeachhypothesized</sup> value _ϵl_ of _ϵ_ , i.e., 



Assume that the noise term _V_ ( _m_ ) is small or negligible, and we have: 



As can be seen in (50) and (51), the absolute value operation can filter out the effect of phase caused by TO and CPO, and when _ϵl_ = _ϵ_ , _CS_ ( _l_ ) can reach the maximum without knowing the information of the transmitted spectrum. Thus, the CFO estimate can be finally obtained by finding the one which achieves the 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1637 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 



Fig. 3. Schematic diagram of the sequential MF ML estimator. 

best match: 



Based on the estimated CFO _ϵ_ ˆ _S_ obtained in (52), we can use either the ‘time-domain’ approach [19] or the ‘frequencydomain’ approach [20] to obtain the ML estimates of TO and CPO jointly. One can see from the above development based on (50) and (51) that the sequential approach should work well at high SNR, and this is borne out by our simulation studies presented later in the paper. The sequential approach here forms the foundation of the approach we proposed earlier in [14]. 

In the sequential approach, since we utilize only the amplitude information of the spectrum for CFO estimation, the modulation format of _M_ QAM will show a CFO estimation error variance worse than that of _M_ PSK. This is because the _M_ PSK modulated data symbols have the same amplitude, whereas the _M_ QAM modulated data symbols have multi-level amplitudes, which may cause severe estimation error at low SNR. Therefore, the first two pilot OFDM symbols are modulated as _M_ PSK format to ensure the CFO estimation performance. 

In order to get accurate CFO estimation performance, the zero-padding factor needs to be large enough. To ensure a low complexity and a good estimation performance, similar to what has been done in Section III-C, a fine search needs to be performed as (48) and (49) show. 

## V. PERFORMANCE BOUNDS 

To evaluate the estimation performance of the proposed algorithms, for the CFO estimation, we compared the proposed methods with Schmidl’s [8] method with respect to the inverse estimation error variance (IEEV). For the timing offset estimation, we compare the ‘time-domain’ and ‘frequency-domain’ algorithms with Schmidl’s [8], Minn’s [9], and Park’s [10] algorithms. 

The estimation error variance is commonly used to measure the estimation accuracy. For _ϵ_ , _τ_ and _θ_ , the corresponding 





Fig. 4. Simulation setup of a CO-OFDM system. AWG: Arbitrary Waveform Generator; EDFA: Erbium-Doped Fiber Amplifier; SSMF: Standard Single Mode Fiber; OBPF: Optical Band-Pass Filter. 

In Appendix C, we derive the following CRLBs on these variances: 



where the definition and expression of terms _P, S_ and _Q_ are shown in (C.6) and (C.8). 

In addition, to evaluate the TO estimation performance, we also introduce the probability of correct timing estimation, which is computed as: 



The number of timing estimates made is 100000, to ensure reliable estimation of the probability. 

## VI. SIMULATION RESULTS AND DISCUSSION 

## _A. System Setup_ 

We refer to the transmitter and receiver block diagram of our CO-OFDM system shown in Fig. 1 and the setup in Fig. 4. The simulations are carried out through MATLAB and VPI TransmissionMaker 9.1. The length of serial input data bits is 2<sup>17</sup> _−_ 1 and the number of data subcarriers is 256, which is the same as the DFT/IDFT size. The first two pilot symbols are modulated onto 16-PSK, while the payload data can be 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1638 



Fig. 5. IEEV of CFO vs. _γ_ with _ϵ_ = 0 _._ 3 _, τ_ = 10, and _θ_ = _π/_ 4. 



Fig. 6. IEEV of CFO vs. _γ_ with _ϵ_ = 0 _._ 3 _, τ_ = 10, and _θ_ = _π/_ 4 under the CLW of 50 kHz, 100 kHz and 200 kHz. 

modulated onto any modulation format. In our simulations, the payload data is under 16-QAM modulation. A cyclic prefix of 32 samples is added before each OFDM symbol and there are 128 OFDM symbols in total. The sample rate of the arbitrary waveform generator (AWG) is 25 GSa/s. In VPI simulations, the laser is working at 1550 nm, with the linewidth of 100 kHz and launch power of _−_ 2 dBm. After transmitting through the standard single mode fiber (SSMF) with the dispersion factor of 16 ps/nm/km, the signal is received by a balanced receiver and converted to digital by passing through the ADC with the sample rate of 50 GSa/s. In the digital signal processing procedure at the receiver side, we first downsample the received signal by using a median filter, and in our proposed MF ML algorithms, the zero-padding factor is selected to be 8 for CFO estimation, and 4 for the ‘frequency-domain’ approach for joint ML estimation of TO and CPO. For laser phase noise compensation in Fig. 4, we use the pilot-assisted algorithm [29], with 5 pilot subcarriers. Besides, there are 5 OFDM symbols used for channel estimation. Thus,thenetdatarateintheVPIsimulationis25GSa/s _×_ log2 16 bits/sample _×_<sup><u>121</u></sup> 128<sup>_×_</sup><sup><u>256</u></sup> 288<sup>_×_</sup><sup><u>251</u></sup> 256<sup>_≈_82</sup><sup>_._4Gbps.Notethatthere-</sup> sults in subsections A through F are obtained using MATLAB simulations, while those in subsection G are obtained using VPI TransmissionMaker simulations. 

To discuss the simulation results clearly, here we use abbreviations of the methods, defined as: JF/SF: <u>joint/sequential</u> ML estimator by the ‘frequency-domain’ approach, and JT/ST: <u>joint/sequential</u> ML estimator by the ‘time-domain’ approach. For the CFO estimation by the sequential method, we denote it as ‘sequential’ for simplicity. 

## _B. Effects of SNR and CPN on CFO Estimation_ 

Fig. 5 shows the CFO estimation performance of the proposed methods and Schmidl’s algorithm [8] versus SNR. The IEEV of the JT method deviates from the inverse CRLB (ICRLB) when SNR is smaller than 9 dB, while that of the JF method always reaches the ICRLB. At low SNR, the phase unwrapping error accumulates and leads to the degradation of the final estimation performance. For the sequential estimator, to get rid of the phase effect caused by TO, it utilizes the amplitude information only 



Fig. 7. IEEV vs. _ϵ_ with under _γ_ = 10 dB and _γ_ = 20 dB. 

for CFO estimation. Compared with the proposed joint ML estimator, the sequential method is suboptimal, thus its IEEV cannot reach the ICRLB. 

In Fig. 6, in the presence of CPN, all the algorithms show performance degradation. However, the JF method always performs the best. The IEEV of the sequential method gradually converges to that of JF method with the increase of SNR. Under large CLW and high SNR, the sequential method outperforms Schmidl’s method. This is mainly because Schmidl’s method takes the correlation between the two identical halves in the time domain, and utilizes the phase information. Since the CPN is a Wiener process, the calculated phase after correlation actually includes the accumulated phase noise, which can lead to severe CFO estimation performance degradation at a high laser linewidth. However, the proposed methods perform well at the frequency domain, where the CPN after DFT, is composed of a common phase error (CPE) and an ICI part. When the CPN variance is small, the ICI part is commonly regarded as AWGN [1]. 

The IEEV performance versus different CFO values is shown in Fig. 7. The proposed methods have full CFO estimation range, 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1639 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 



Fig. 8. IEEV of TO vs. _γ_ with _ϵ_ = 0 _._ 3 _, τ_ = 10, and _θ_ = _π/_ 4. 

i.e., the integral part of CFO estimation range of [0 _, N −_ 1], and the fractional part of CFO estimation range of [ _−_ 0 _._ 5 _,_ 0 _._ 5). Since Schmidl’s method can only estimate the fractional part of CFO, here in Fig. 7, we only investigate the CFO range of [ _−_ 0 _._ 5 _,_ 0 _._ 5). It can be observed clearly that the IEEV of the proposed algorithms are transparent to the CFO values, and the performance of the joint method is the optimum, which is consistent with Fig. 5. 

## _C. Effects of SNR on to Estimation_ 

Fig. 8 shows the IEEV performance of the proposed methods versus SNR. The IEEV performance of TO of the JF and SF methods can achieve the ICRLB when SNR is higher than 2 dB. The SF method performs worse at lower SNR, because the CFO estimation error affects the estimation accuracy of TO, which is consistent with Fig. 5. The proposed JT and ST methods can perform well when SNR is higher than 10 dB, but due to the error caused by the phase unwrapping algorithm at low SNR, their IEEV degrades severely. 

## _D. Timing Metrics_ 

The timing metrics of the proposed JF/SF, Schmidl’s, Minn’s and Park’s methods are shown in Fig. 9, with _τ_ = 10, under the case of CFO and CPO totally compensated. As can be seen from Fig. 9, the timing metric of Schmidl’s method has a plateau that is equal to the length of CP, which causes severe timing estimation error at low SNR. Minn’s and Park’s methods solve this problem, and Park’s method has a sharper peak than Minn’s method. However, both Minn’s and Park’s methods have large side lobes which may cause severe timing estimation error because of leading to the wrong peak at low SNR. Compared with these algorithms, the timing metric of the proposed JF/SF method shows a clear and sharp peak without any side lobes. 

## _E. Probability of Correct Timing Estimation_ 

The timing estimation performance comparison of the proposedandconventionalmethodsisshowninFig.10,withrespect to the probability of correct timing estimation. In this simulation, 



Fig. 9. Timing metrics of JF/SF, Schmidl’s, Minn’s and Park’s methods, with _τ_ = 10, _ϵ_ = 0 and _θ_ = 0. 



Fig. 10. Probability of correct timing estimation, with _τ_ = 10. 

we assume the CFO has been totally compensated. For the SF and ST methods, we choose the nearest integer of the TO estimates as the estimation. In Fig. 10, Schmidl’s method shows the worst timing estimation performance, because the plateau in the timing metric leads to its sensitivity to the AWGN, and causes severe performance degradation. In addition, since the timing metric of Park’s method has a sharper main peak than that of Minn’s method, the probability of correct timing estimation of Park’s method is higher than that of Minn’s method, especially at low SNR. 

TheSFmethodshowsthebesttimingestimationperformance, with the timing estimation accuracy of 1 at even _−_ 10 dB SNR. The ST method performs a little worse than Park’s method at low SNR. There are two main reasons. First, the phase unwrapping algorithm is sensitive to the AWGN. Second, the TO estimate is obtained from the analytical result shown in (43), in which the TO related radian frequency is calculated first, then multiply by _N/_ 2 _π_ to get the final estimate. The multiplication step enlarges the small error and causes fluctuations around the actual TO, thus decreasing the probability of timing estimation. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1640 



Fig. 11. IEEV of CPO vs. _γ_ with _ϵ_ = 0 _._ 3 _, τ_ = 10, and _θ_ = _π/_ 4. 



Fig. 12. BER vs. OSNR in back to back transmission, with the CFO of 30 MHz and the CLW of 200 kHz. 

## _F. Effect of SNR on CPO Estimation_ 

Fig. 11 shows the IEEV of the proposed methods vs. SNR. The IEEV of the JF method can always reach the ICRLB, while that of the JT method reaches the ICRLB when SNR is higher than 9 dB. At low SNR, the JT method shows performance degradation due to the error caused by the phase unwrapping algorithm. The IEEV of the sequential method cannot reach the ICRLB since the CFO estimation step is suboptimal, whose accuracy will affect the estimation of TO and CPO. The result in Fig. 11 is consistent with that of Fig. 5. 

## _G. BER Performance and Nonlinearities Tolerance_ 

The final BER performance of the proposed algorithms and Schmidl’s method versus OSNR is investigated by using VPI TransmissionMaker, which is shown in Fig. 12, with the CFO of 30 MHz and the combined laser linewidth of 200 kHz, in a back to back transmission scenario. From Section VI. D, we can observe that the timing metric plateau of Schmidl’s method can lead to severe degradation on the timing estimation accuracy in a noisy and dispersive channel, thus causing the degradation of BER performance. Therefore, in this simulation, we correct the 



Fig. 13. BER vs. various transmission distances, with the CFO of 30 MHz and the CLW of 200 kHz, at the OSNR of 20 dB. 

timing estimation error of Schmidl’s method, in order to show a clear performance comparison of the CFO estimation. It can be observed from Fig. 12 that the BER performance of the proposed algorithms can always converge to the coherent bound, which is obtained by directly using the actual CFO value for compensation. Schmidl’s algorithm performs a little worse, but the BER difference between these algorithms is not obvious. This is because the residual CFO can be compensated and corrected by the phase noise compensation algorithm that follows the joint MF ML estimation and compensation algorithm, as shown in Fig. 4. 

We also investigate the CD and fiber nonlinearities tolerance of the proposed algorithms. Fig. 13 shows the BER performance after transmitting through various fiber lengths with the CFO of 30MHzandtheCLWof200kHz,attheOSNRof20dB.Itcanbe clearly observed that with CD compensation [30], the proposed JF method shows the best performance, while Schmidl’s method shows the worst. However, without the CD compensation, after a 100 km transmission, the BER of JF method is the highest, while the SF method is the lowest. This is because the data-aided algorithms such as JF and Schmidl’s methods depend highly on the transmitted data. With the appearance of fiber nonlinearities, the pilot symbols used for CFO estimation have already been severely distorted, thus leading to a poor BER performance. However, the proposed SF method estimates the CFO, TO and CPO in a sequential manner, in which the CFO estimation is achieved in a blind manner by utilizing only the amplitude information, and thus it shows the best tolerance of CD and fiber nonlinearies. Therefore, we can easily conclude that the proposed MF ML algorithms are applicable to real long-haul optical fiber transmissions. 

Inordertoinvestigatetheperformanceofproposedalgorithms in detail, we further plot the Q factor versus launch power, which is shown in Fig. 14. It can be seen that for 480 km transmission, the optimum launch power of the proposed algorithms is _−_ 1 dBm, while that of Schmidl’s method is 1 dBm. This illustrates that Schmidl’s method performs better under highly nonlinear transmission than JF and SF methods. The performance of proposed algorithms is worse than Schmidl’s method when the 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1641 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 

TABLE I 

COMPLEXITY COMPARISON 

lower complexity than the frequency-domain method. Because the time-domain method utilizes the analytical results while the frequency-domain method needs to perform the _N_ -point FFT and a fine search. We should point out that our proposed methods not only have lower complexity, but also can achieve the joint estimation of CFO, TO and CPO, while Schmidl’s method can only estimate the TO and CFO. 

## VII. CONCLUSION 

Fig. 14. Q factor versus launch power after 480 km transmission, with CD compensation. 

power is above 1.2 dBm. However, when the Q factor is below 13.5 dB, the corresponding BER is above 1E _−_ 3, which will become even worse at a higher power level. When the launch power is lower than 1.2 dBm, the proposed algorithms show obvious performance advantage compared with Schmidl’s method. Therefore, although the performance of proposed algorithms degrades in highly nonlinear environments, in which case the BER is relatively high, the proposed algorithms show superior performance than Schmidl’s method under the condition of lower nonlinearity. In a real transmission, by using existing algorithms to compensate for the dispersion and nonlinearities, the proposed algorithms are able to tolerate the residual effect, which can be seen from the simulation results in Fig. 13 and Fig. 14. Thus, the proposed algorithms show the possibility for applying to higher speed systems. 

## _H. Complexity Comparison_ 

Table I shows the complexity comparison between the proposed and Schmidl’s methods. Some abbreviations are defined as: Freq./Time: frequency/time-domain approach, Mul.: multiplications, Add.: additions, Val.: values, Seq.: sequential method. Term _L_<sup>_′_</sup> is the zero-padding factor of JF/SF method. For the typical values in simulations, we have _L_ = 8 _, N_ = 256 and _L_<sup>_′_</sup> = 4. 

In Table I, the complexity of Schmidl’s method is the highest. This is because the timing estimation of Schmidl’s method requires searching for all the possible values, and calculating the timing metric within each search. The sequential method is simpler than the joint method, and the time-domain approach shows 

Based on the concept of optimum signal detection in AWGN, we developed a joint ML estimator of the CFO, CPO and TO in the frequency domain. The resulting receiver is straightforward to implement, although it can be computationally heavy. However, the theoretical analysis demonstrates how one can derive a suboptimum sequential estimator that first obtains an approximate ML estimate of the CFO, followed by joint ML estimation of the CPO and TO. The sequential estimator is much simpler computationally, and its performance loss is small compared to the performance of the optimum joint estimator at high SNR. Also, simulation results show that the estimation performance of the sequential approach is more robust to the CD and the fiber nolinearity. One should note the conceptual novelty of our approach here that is easy to understand and simple to implement compared to other existing approaches. The system model we picked here for our analysis may be simpler than that in other papers, for instance, [31]–[34], but we did this in order to make it easier for the reader to understand the principle of our approach. In a future report, we will extend our work to the case of channels with time and frequency dispersion. 

## APPENDIX A 

## DERIVATION OF THE RELATIONSHIP BETWEEN TIME-DOMAIN SNR AND FREQUENCY-DOMAIN SNR 

Since the _{w_ ( _n_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1isasequenceofindependent,iden-</sup> tically distributed, complex, AWGN random variables, then we can easily obtain that _σW_<sup>2=</sup><sup>_Nσ_2. The average energy per</sup> subcarrier _EX_ can be rewritten as: 



Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1642 



Sincethedataonthesubcarriers areindependent witheachother, and for _M_ -PSK and _M_ -QAM modulation, the constellation points are symmetric with equal probability, then we have: 



Thus, after the _N_ -point IDFT, we can obtain: 



As can be seen from Appendix A,<sup>�</sup><sup>_N_</sup> _n_ =0<sup>_−_1</sup><sup>_|x_(</sup><sup>_n_)</sup><sup>_|_2=</sup><sup>_NEx_,</sup> where we have _NEx_ = _Es_ and for _M_ PSK modulation, _Es_ = _A_ . Thus, (B.2) can be simplified to: 



In Section III-B, we take the _N_ -point DFT of _A_<sup>(</sup><sup>_l_)</sup> ( _m_ ) _e_<sup>_−j_2</sup><sup>_πmτ/N_</sup> , which can be calculated as: 

Then (A.1) can be simplified as: 



Finally, the frequency-domain SNR _γf_ is: 



## APPENDIX B EXPRESSION OF _A_<sup>_l_</sup> ( _m_ ) 

From (35), we can calculate _A_<sup>(</sup><sup>_l_)</sup> ( _m_ ) as: 





According to the cycle characteristics of DFT, (B.1) can be further calculated as: 





The third step of (B.4) is obtained based on the property of geometric progression [35], i.e.,<sup>�</sup><sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1</sup><sup>_e−j_2</sup><sup>_πm_</sup> _N_<sup><u>(</u></sup><sup>_τ_</sup><sup><u>+</u></sup><sup>_ν_</sup><sup><u>)</u></sup> = 1 _−_ <u>1</u> _−e_<sup>_−_</sup> _<u>e</u>_<sup>_j−_2</sup><sup>_jπ_2(</sup><sup>_πτ_(+</sup><sup>_τ_+</sup><sup>_ν_)</sup><sup>_ν/N_)= 0,andsimilarly,�</sup><sup>_N_</sup> _m_<sup>_−_</sup> =0<sup>1</sup><sup>_e−j_2</sup><sup>_πm_</sup><sup><u>(</u></sup><sup>_τ_</sup><sup><u>+</u></sup> _N_<sup>_ν_</sup><sup><u>+</u></sup><sup>_n−n_</sup><sup><u>1)</u></sup> = 0. This is because the terms _τ_ + _ν_ and _τ_ + _ν_ + _n − n_ 1 in the numerators are integers, then _e_<sup>_−j_2</sup><sup>_π_(</sup><sup>_τ_+</sup><sup>_ν_)</sup> and _e_<sup>_−j_2</sup><sup>_π_(</sup><sup>_τ_+</sup><sup>_ν_+</sup><sup>_n−n_1)</sup> are both equal to 1. 

## APPENDIX C 

## DERIVATION OF THE UNBIASED CRAMÉR-RAO LOWER BOUND 

Here, (ˆ _ϵ,_ ˆ _τ, θ_<sup>ˆ</sup> ) become asymptotically unbiased as SNR increases, that have been proved in [14], [20]. The unbiased CRLBs are the diagonal elements of the inverse of the Fisher information matrix _J_ , whose typical element is given by [20]: 





Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

1643 

DU _et al._ : OPTIMUM SIGNAL DETECTION APPROACH TO THE JOINT ML ESTIMATION OF TIMING OFFSET 

where we have **z** = [ _ϵ, τ, θ_ ]<sup>_T_</sup> , and the expectation is with respect to the likelihood function, i.e.: 



where we have 



After calculation, the Fisher information matrix _J_ can be obtained which is in (C.5), as shown at the bottom of the previous page. Then the inverse matrix _J_<sup>_−_1</sup> is expressed in (C.7), also shown at the bottom of the previous page. Finally, then bounds are given by 



where the expressions of _P, S_ and _Q_ are shown in (C.6) and (C.8). 

## REFERENCES 

- [1] W. Shieh and I. Djordjevic, _OFDM for Optical Communications_ . New York, NY, USA: Academic, 2009. 

- [2] A. J. Coulson, “Maximum likelihood synchronization for OFDM using a pilot symbol: Algorithms,” _IEEE J. Sel. Areas Commun._ , vol. 19, no. 12, pp. 2486–2494, Dec. 2001. 

- [3] D. D. Lin, R. A. Pacheco, T. J. Lim, and D. Hatzinakos, “Joint estimation of channel response, frequency offset, and phase noise in OFDM,” _IEEE Trans. Signal Process._ , vol. 54, no. 9, pp. 3542–3554, Sep. 2006. 

- [4] J.-J. Van de Beek, M. Sandell, and P. O. Borjesson, “Ml estimation of time and frequency offset in OFDM systems,” _IEEE Trans. Signal Process._ , vol. 45, no. 7, pp. 1800–1805, Jul. 1997. 

- [5] M. M. U. Gul, X. Ma, and S. Lee, “Timing and frequency synchronization for OFDM downlink transmissions using Zadoff–Chu sequences,” _IEEE Trans. Wireless Commun._ , vol. 14, no. 3, pp. 1716–1729, Mar. 2015. 

- [6] Y. Cao, W. Su, and S. N. Batalama, “A novel receiver design and maximum-likelihood detection for distributed MIMO systems in presence of distributed frequency offsets and timing offsets,” _IEEE Trans. Signal Process._ , vol. 66, no. 23, pp. 6297–6309, Dec. 2018. 

- [7] G. Miriyala, A. Kakumanu, M. Swapna, and P. S. Shankar, “Joint estimation of channel response, frequency offset and phase noise in OFDM systems,” in _Proc. IEEE 2nd Int. Conf. Intell. Comput. Control Syst._ , 2018, pp. 1299–1303. 

- [8] T. M. Schmidl and D. C. Cox, “Robust frequency and timing synchronization for ofdm,” _IEEE Trans. Commun._ , vol. 45, no. 12, pp. 1613–1621, Dec. 1997. 

- [9] H. Minn, M. Zeng, and V. K. Bhargava, “On timing offset estimation for OFDM systems,” _IEEE Commun. Lett._ , vol. 4, no. 7, pp. 242–244, Jul. 2000. 

- [10] B. Park, H. Cheon, C. Kang, and D. Hong, “A novel timing estimation method for OFDM systems,” _IEEE Commun. Lett._ , vol. 7, no. 5, pp. 239–241, May 2003. 

- [11] X. Zhou, K. Long, R. Li, X. Yang, and Z. Zhang, “A simple and efficient frequency offset estimation algorithm for high-speed coherent optical OFDM systems,” _Opt. Express_ , vol. 20, no. 7, pp. 7350–7361, 2012. 

- [12] J. Wu _et al._ , “A robust and efficient frequency offset correction algorithm with experimental verification for coherent optical OFDM system,” _J. Lightw. Technol._ , vol. 33, no. 18, pp. 3801–3807, 2015. 

- [13] H.-G. Jeon, K.-S. Kim, and E. Serpedin, “An efficient blind deterministic frequency offset estimator for OFDM systems,” _IEEE Trans. Commun._ , vol. 59, no. 4, pp. 1133–1141, Apr. 2011. 

- [14] X. Du, T. Song, and P.-Y. Kam, “Carrier frequency offset for COOFDM: The matched filter approach,” _J. Lightw. Technol._ , vol. 36, no. 14, pp. 2955–2965, 2018. 

- [15] X. Du, J. Zhang, Y. Li, C. Yu, and P.-Y. Kam, “Efficient joint timing and frequency synchronization algorithm for coherent optical OFDM systems,” _Opt. Express_ , vol. 24, no. 17, pp. 19 969–19 977, 2016. 

- [16] B. You _et al._ , “Joint carrier frequency offset and phase noise estimation based on pseudo-pilot in CO-FBMC/OQAM system,” _IEEE Photon. J._ , vol. 11, no. 1, pp. 1–11, Feb. 2019. 

- [17] K. Ren _et al._ , “A time and frequency synchronization method for COOFDM based on CMA equalizers,” _Opt. Commun._ , vol. 416, pp. 166–171, 2018. 

- [18] X. Du, P.-Y. Kam, and C. Yu, “Joint timing and frequency synchronization incoherentopticalOFDMsystems,” _FrontiersOptoelectron._ ,vol.12,no.1, pp. 4–14, 2019. 

- [19] H. Fu and P. Y. Kam, “MAP/ML estimation of the frequency and phase of a single sinusoid in noise,” _IEEE Trans. Signal Process._ , vol. 55, no. 3, pp. 834–845, Mar. 2007. 

- [20] D. Rife and R. Boorstyn, “Single tone parameter estimation from discretetimeobservations,” _IEEETrans.Inf.Theory_ ,vol.IT-20,no.5,pp. 591–598, Sep. 1974. 

- [21] L. Li, W. Yao, L. Han, and G.-J. Hu, “Timing synchronization algorithm based on FH sequence for coherent optical OFDM systems with carrier frequency offset,” _Optoelectron. Lett._ , vol. 15, no. 4, pp. 288–291, 2019. 

- [22] X. Fang, Y. Wang, D. Ding, and L. Zhang, “Pilot-aided phase noise suppression for coherent optical ofdm/oqam,” in _Proc. Asia Commun. Photon. Conf._ , 2019, paper M4A.107. 

- [23] J. Liu, Y. Wei, X. Zeng, J. Lu, S. Zhang, and M. Wang, “A novel joint timing/frequency synchronization scheme based on Radon–Wigner transform of LFM signals in CO-OFDM systems,” _Opt. Commun._ , vol. 410, pp. 744–750, 2018. 

- [24] H. Abdzadeh-Ziabari, W.-P. Zhu, and M. Swamy, “Joint maximum likelihood timing, frequency offset, and doubly selective channel estimation for OFDM systems,” _IEEE Trans. Veh. Technol._ , vol. 67, no. 3, pp. 2787–2791, Mar. 2018. 

- [25] H. Rahbari, M. Krunz, and L. Lazos, “Swift jamming attack on frequency offset estimation: The achilles’ heel of OFDM systems,” _IEEE Trans. Mobile Comput._ , vol. 15, no. 5, pp. 1264–1278, May 2016. 

- [26] O. H. Salim, A. A. Nasir, H. Mehrpouyan, W. Xiang, S. Durrani, and R. A. Kennedy, “Channel, phase noise, and frequency offset in OFDM systems: Joint estimation, data detection, and hybrid Cramer–Rao lower bound,” _IEEE Trans. Commun._ , vol. 62, no. 9, pp. 3311–3325, Sep. 2014. 

- [27] G. L. Stüber, _Principles of Mobile Communication_ . Berlin, Germany: Springer, 2001, vol. 2, pp. 231–343. 

- [28] H. Fu and P.-Y. Kam, “Phase-based, time-domain estimation of the frequency and phase of a single sinusoid in AWGN–the role and applications of the additive observation phase noise model,” _IEEE Trans. Inform. Theory_ , vol. 59, no. 5, pp. 3175–3188, May 2013. 

- [29] X. Yi, W. Shieh, and Y. Tang, “Phase estimation for coherent optical OFDM,” _IEEE Photon. Technol. Lett._ , vol. 19, no. 12, pp. 919–921, Jun. 2007. 

- [30] W. Shieh and C. Athaudage, “Coherent optical orthogonal frequency division multiplexing,” _Electron. Lett._ , vol. 42, no. 10, pp. 587–589, 2006. 

- [31] H. Abdzadeh-Ziabari, W.-P. Zhu, and M. Swamy, “Joint maximum likelihood timing, frequency offset, and doubly selective channel estimation for OFDM systems,” _IEEE Trans. Veh. Technol._ , vol. 67, no. 3, pp. 2787–2791, Mar. 2018. 

- [32] P.-S. Wang and D. W. Lin, “On maximum-likelihood blind synchronization over WSSUS channels for OFDM systems,” _IEEE Trans. Signal Process._ , vol. 63, no. 19, pp. 5045–5059, Oct. 2015. 

- [33] T. Fusco and M. Tanda, “ML-based symbol timing and frequency offset estimation for OFDM systems with noncircular transmissions,” _IEEE Trans. Signal Process._ , vol. 54, no. 9, pp. 3527–3541, Sep. 2006. 

- [34] X. Ma, H. Zhang, X. Yao, and D. Peng, “Pilot-based phase noise, IQ mismatch, and channel distortion estimation for PDM CO-OFDM system,” _IEEE Photon. Technol. Lett._ , vol. 29, no. 22, pp. 1947–1950, Nov. 2017. 

- [35] M. Hazewinkel, _Encyclopedia of Mathematics_ . Norwell, MA, USA: Kluwer Academic, 1994. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 39, NO. 6, MARCH 15, 2021 

1644 

**Xinwei Du** (Member, IEEE) received the B.Eng. degree from the Department of Communication and Information Engineering, University of Electronic Science and Technology of China, Chengdu, China, in 2014 and the Ph.D. degree in 2018 from the Department of Electrical and Computer Engineering, National University of Singapore, Singapore, supervised by Prof. P.-Y. Kam, Prof. Changyuan Yu, and Prof. Mohan Gurusamy. From 2018 to 2020, she was a Postdoctoral Fellow with the Hong Kong Polytechnic University, Hong Kong. In September 2020, she joined the Division of Science and Technology, BNU-HKBU United International College, Guangdong, China, as an Assistant Professor. Her research focuses on the carrier recovery and data detection algorithms for coherent wireless and optical OFDM systems, including nonlinearity compensation, frequency, and phase synchronization. 

**Tianyu Song** (Member, IEEE) was born in Wuchang, Heilongjiang, China, in 1989. He received the B.Eng. degree from Honors School, Harbin Institute of Technology, Harbin, China, in 2011, and the Ph.D. degree from the National University of Singapore, Singapore, in 2016, supervised by Prof. P.-Y. Kam. From 2009 to 2010, he was an Exchange Student with the Department of Electrical Engineering, Korea Advanced Institute of Science and Technology, Daejon, South Korea. His research interests include free space optical communications, optimal receiver design, and stochastic processes and algorithms. He was the recipient of the Best Paper Award at the IEEE/CIC ICCC2015. 

**Yan Li** was born in Fuyang, Anhui, China, in 1994. He received the B.Eng. degree from Nanjing University, Nanjing, China, in 2014 and the Ph.D. degree from the National University of Singapore, Singapore, supervised by Prof. P.-Y. Kam and Prof. C. Yu. From 2018 to 2019, he was a Research Assistant with Hong Kong Polytechnic University and worked on digital signal processing for optical fiber communication systems. In 2019, he joined the School of Electronics and Information Technology, Sun Yat-sen University, Guangzhou, China, as a Postdoctoral Researcher. His current research focuses on optical signal manipulation for high-speed communication systems. 

**Pooi-Yuen Kam** (Fellow, IEEE) was born in Ipoh, Malaysia. He received the S.B., S.M., and Ph.D. degrees in electrical engineering from the Massachusetts Institute of Technology, Cambridge, MA, USA, in 1972, 1973, and 1976, respectively. From 1976 to 1978, he was a member of the Technical Staff with Bell Telephone Laboratories, Holmdel, NJ, USA, where he was engaged in packet network studies. Since 1978, he has been a Professor with the Department of Electrical and Computer Engineering, National University of Singapore, where he was the Deputy Dean of Engineering and the Vice Dean for Academic Affairs of the Faculty of Engineering from 2000 to 2003. He spent the sabbatical year from 1987 to 1988 with the Tokyo Institute of Technology, Tokyo, Japan, under the sponsorship of the Hitachi Scholarship Foundation. In 2006, he was invited to the School of Engineering Science, Simon Fraser University, Burnaby, BC, Canada, as the David Bensted Fellow. He was a Distinguished Guest Professor (Global) with the Graduate School of Science and Technology of Keio University, Tokyo, Japan, from 2015 to 2017. He was a Visiting Professor with the Department of Electronic Engineering, Shanghai Jiao Tong University, Shanghai, China, in 2017, and a Visiting Professor with the University of Electronic Science and Technology of China, in 2018. Since 2019, he has been a Professor with the School of Science and Engineering, Chinese University of Hong Kong, Shenzhen, China. His research interests include communication sciences and information theory, and their applications to wireless and optical communications. Dr. Kam is a member of Eta Kappa Nu, Tau Beta Pi, and Sigma Xi. From 2011 to 2017, he was a Senior Editor of the _IEEE Wireless Communications Letters_ . From 1996 to 2011, he was the Editor for Modulation and Detection for Wireless Systems of the IEEE TRANSACTIONS ON COMMUNICATIONS. From 2007 to 2012, he was on the Editorial Board of PHYCOM, the _Journal of Physical Communications_ of Elsevier. He was a Co-Chair for the Communication Theory Symposium of IEEE Globecom 2014. He was elected a Fellow of the IEEE for his contributions to receiver design and performance analysis for wireless communications. He was the recipient of the Best Paper Award at the IEEE VTC2004-Fall, the IEEE VTC2011-Spring, the IEEE ICC2011, and the IEEE/CIC ICCC2015. He was on the IEEE Fellow Committee in 2016, 2017, and 2018, and on the IEEE Fellows Strategic Planning Subcommittee in 2018 and 2019. He was on the IEEE VTS Awards Committee in 2019 and 2020, and has been on the IEEE ComSoc Fellow Evaluation Committee since 2020. Since 2016, he has also been with Suzhou Research Institute, National University of Singapore Suzhou Research Institute Suzhou, China, where he is the Principal Investigator of a project on free-space optical communications funded by the National Natural Science Foundation of China. 

**Ming-Wei Wu** (Member, IEEE) received the B.E. (first class Hons.), M.E., and Ph.D. degrees in electrical engineering from the National University of Singapore, Singapore, in 2000, 2003, and 2011, respectively. From 2002 to 2004, she was a Research Engineer with the Institute for Infocomm Research, Singapore, and worked on Ethernet passive optical networks standardization and implementation. In 2004, she joined the School of Information and Electronic Engineering, Zhejiang University of Science and Technology, Hangzhou, China, as a Lecturer, and is currently a Professor. Her research interests include wireless communication, detection, estimation theory, and performance analysis. She is a Technical Program Committee Member for international communications conferences, including the IEEE ICC, the IEEE VTC, the IEEE Globecom, and the IEEE ICCC. She was the recipient of the Best Paper Award from the IEEE ICC2011, Kyoto, Japan. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 10:17:47 UTC from IEEE Xplore.  Restrictions apply. 


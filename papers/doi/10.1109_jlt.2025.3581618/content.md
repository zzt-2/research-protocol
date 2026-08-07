JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 43, NO. 17, SEPTEMBER 1, 2025 

8040 

# Preamble Design for Online IQ-Skew Estimation in Upstream 400G Coherent TFDM-PON 

Junhao Zhao , Yongzhu Hu , An Yan , Penghao Luo , Xuyu Deng , Renle Zheng, Boyu Dong , Zhongya Li , Aolong Sun , Yinjun Liu , Ouhan Huang , Sizhe Xing , Ziwei Li , Chao Shen , Jianyang Shi , Zhixue He , Nan Chi , and Junwen Zhang 

_**Abstract**_ **—An online calibration method based on burst-mode digital signal processing (DSP) is proposed to solve the transceiver In-phase and quadrature (IQ) skew problem in the upstream system of 400G time frequency division multiplexing passive optical network (TFDM-PON). In traditional coherent PON, IQ skew can cause image frequency crosstalk, which seriously affects the system performance, especially in the scenario of multi-user subcarrier power imbalance. By designing a training sequence that simultaneously enables frame detection, one-tap SOP estimation, timing recovery, and frequency offset estimation (FOE), the proposed scheme also achieves online estimation and compensation of transceiver IQ skew. The experiment verifies the effectiveness of this method in three typical subcarrier allocation scenarios (single ONU four subcarriers, dual ONU two subcarriers each, and asymmetric subcarrier allocation). The results show that the transceiver IQ skew estimation error can be controlled within** _**±**_ **0.3 ps, and the sensitivity of 400G TFDM-PON system with 16-QAM signal after** 

Received 6 April 2025; revised 25 May 2025 and 8 June 2025; accepted 16 June 2025. Date of publication 19 June 2025; date of current version 2 September 2025. This work was supported in part by the National Natural Science Foundation of China under Grant 62171137, in part by the Natural Science Foundation of Shanghai under Grant 24ZR1490500, and in part by Major Key Project PCL. _(Corresponding author: Junwen Zhang.)_ 

Junhao Zhao is with the Key Laboratory for Information Science of Electromagnetic Waves (MoE), Shanghai Engineering Research Center of LEO Satellite Communication and Applications, Shanghai Collaborative Innovation Center of LEO Satellite Communication Technology, Department of Communication Science and Engineering, Fudan University, Shanghai 200433, China, and also with Shanghai Innovation Institute, Shanghai 200433, China (e-mail: jhzhao22@m.fudan.edu.cn). 

Yongzhu Hu, An Yan, Penghao Luo, Xuyu Deng, Renle Zheng, Boyu Dong, Zhongya Li, Aolong Sun, Yinjun Liu, Ouhan Huang, Sizhe Xing, Ziwei Li, Chao Shen, and Jianyang Shi are with the Key Laboratory for Information Science of Electromagnetic Waves (MoE), Shanghai Engineering Research Center of LEO Satellite Communication and Applications, Shanghai Collaborative Innovation Center of LEO Satellite Communication Technology, Department of Communication Science and Engineering, Fudan University, Shanghai 200433, China (e-mail: huyz23@m.fudan.edu.cn; ayan22@m.fudan. edu.cn; phluo22@m.fudan.edu.cn; xydeng23@m.fudan.edu.cn; 24110720110 @m.fudan.edu.cn; bydong21@m.fudan.edu.cn; zhongyali20@fudan.edu.cn; alsun22@m.fudan.edu.cn; 23110720080@m.fudan.edu.cn; 23110720145@m. fudan.edu.cn; szxing21@m.fudan.edu.cn; lizw@fudan.edu.cn; chaoshen@ fudan.edu.cn; jy_shi@fudan.edu.cn). 

Zhixue He is with Pengcheng Lab, Shenzhen 518057, China (e-mail: hezhx01@pcl.ac.cn). 

Nan Chi and Junwen Zhang are with the Key Laboratory for Information Science of Electromagnetic Waves (MoE), Shanghai Engineering Research Center of LEO Satellite Communication and Applications, Shanghai Collaborative Innovation Center of LEO Satellite Communication Technology, Department of Communication Science and Engineering, Fudan University, Shanghai 200433, China, and also with Pengcheng Lab, Shenzhen 518057, China (e-mail: nanchi@fudan.edu.cn; junwenzhang@fudan.edu.cn). 

Color versions of one or more figures in this article are available at https://doi.org/10.1109/JLT.2025.3581618. Digital Object Identifier 10.1109/JLT.2025.3581618 

**compensation reaches** _**−**_ **28 dBm after 50-km fiber transmission. In addition, after calibrating the transceiver according to the estimated value of the proposed scheme, the sensitivity penalty of transceiver IQ skew under subcarrier power imbalance in 400G TFDM PON is explored. This work provides a feasible solution for online calibration of future high-speed coherent access networks.** 

_**Index Terms**_ **—400G TFDM PON, online IQ skew estimation, burst-mode upstream.** 

## I. INTRODUCTION 

HE Institude of Electrical and Electronics Engineers **T** (IEEE) and the International Telecommunication Union Standardization Sector (ITU-T) have proposed the standardization of high-speed passive optical network (PON) in the past few years [1].Theintensitymodulationanddirectdetection(IM/DD) technology is widespread deployed in commercial PON due to its simple deployment and low cost. However, the growing demands on high access rates and power budget are difficultly satisfied in IM/DD system. It is predictable that 100, 200G and even 400G access rates will be invested in future PON systems to meet the growing user demands. To achieve higher access rates and power budget, the coherent technology is gradually becoming the most promising candidate in future high-capacity access network [2], [3], [4], [5]. Compared to IM/DD system, the coherent system offers many advantages such as high sensitivity, channel selection, polarization multiplexing and multidimensional modulation. Recently, time frequency division multiplexing (TFDM) technology, which is based on digital subcarriers multiplexing (DSCM) technology, has been proposed to provide flexible bandwidth allocation and low-latency access in coherent PON. In TFDM PON, the data allocation is realized in both time domain and frequency domain. 100-Gb/s and 200-Gb/s TFDM PON systems with four subcarriers have been proposed in [6], [7], [8]. These researches indicate that TFDM PON has great potential in the next-generation access network. The upstream burst detection is a critical part in TFDM PON. As shown in Fig. 1, the optical line terminal (OLT) will receive the optical signals with multi-subcarriers from different optical network units (ONUs). These subcarriers from different ONUs are generally located in different frequencies and coupled together by a splitter. Therefore, these subcarriers have different optical power, clocks, state of polarization (SOP), carrier frequencies, phase noise and channel responses. These all need to be solved by burst-mode digital signals process (DSP). Many efforts have 

0733-8724 © 2025 IEEE. All rights reserved, including rights for text and data mining, and training of artificial intelligence and similar technologies. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

ZHAO et al.: PREAMBLE DESIGN FOR ONLINE IQ-SKEW ESTIMATION IN UPSTREAM 400G COHERENT TFDM-PON 

8041 

**==> picture [221 x 114] intentionally omitted <==**

## Fig. 1. The architecture of upstream coherent TFDM-PON. 

been contributed to the fast convergence of burst DSP [9], [10], [11]. 

Additionally, as signals bandwidth increases in TFDM-PON systems, the mirror frequency image crosstalk, which is caused by in-phase and quadrature (IQ) skew from coherent transceiver, is becoming severer. The image crosstalk is more complicated and serious in upstream TFDM PON. As shown in Fig. 1, the image crosstalk, which is caused together by Tx IQ skews from different ONUs and especially Rx IQ skew from OLT, always impair the symmetric subcarriers [12]. Considering the case mentioned above where the optical power between subcarriers is different, the image generated by the high-power subcarriers will cause more serious damage to the low-power subcarriers. The distortion of low-power subcarriers further affects the entire upstream TFDM PON. Compared to time-division multiplexing (TDM)-PON, TFDM-PON adopts intermediate-frequency subcarriers with wider bandwidths, making the system more sensitive to IQ skew. Consequently, TFDM-PON places more stringent requirements on the accuracy and robustness of IQ skew estimation algorithms. Moreover, the sources of IQ skew in TFDM-PON are inherently more complex. In TDM-PON, each time slot carries data from a single ONU, and any IQ skew observed at the receiver is attributed solely to transceiver impairments of that ONU. However, in TFDM-PON, multiple ONUs transmit simultaneously using different subcarriers, leading to inter-ONU image crosstalk. In such a scenario, conventional training sequences designed for TDM-PON systems are insufficient, as the superposition of training sequences from different ONUs can cause mutual interference and degrade estimation performance. In contrast, for DSCM systems typically operating in continuous mode with centrally generated subcarriers from a single transmitter. This configuration avoids inter-user crosstalk and simplifies IQ skew monitoring through centralized calibration. Additionally, power imbalance between ONUs further exacerbates the impact of IQ skew, as high-power subcarriers generate stronger image components that may overwhelm weaker subcarriers. This amplifies skew-induced distortion and poses greater challenges for accurate estimation and compensation. Therefore, specially designed training sequences are required to ensure accurate per-subcarrier IQ skew estimation in a burst-mode, multi-user scenario. 

Although the baud rate of the upstream in coherent PON systems is typically lower than that of the downstream, IQ skew 

remains a critical impairment in the TFDM-PON upstream due to several system-specific factors. First, TFDM-PON employs intermediate-frequency subcarriers that are several gigahertz offset from baseband, which increases the system’s susceptibility to IQ skew. In particular, the presence of symmetrical image components may lead to severe inter-subcarrier and inter-ONU crosstalk if not properly compensated. Second, as mentioned above, the burst-mode nature of the TFDM-PON upstream involves multiple ONUs transmitting asynchronously with different power levels, resulting in subcarrier-level power imbalance. This imbalance exacerbates the impact of image crosstalk, where strong signals from one ONU may dominate the IQ distortion experienced by a weaker subcarrier of another ONU. Together, these factors make accurate and low-overhead IQ skew estimation an essential requirement for reliable high-capacity upstream transmission in TFDM-PON systems. 

Therefore, it is necessary to estimate and compensate transceiver IQ skew in upstream TFDM PON. There have been many efforts devoted to the IQ skew estimation. In [13], [14], [15], the training sequences are repeated 4 times in the frequency domain and skew estimation is calculated by dividing the adjacent spectra. In [16], the inserted single frequency tone is used to estimate IQ skew. In [17], IQ skew estimation is based on the specially designed time-and-frequency interleaving tones. However, the training sequences in these works are only used to estimate IQ impairments. Previous research efforts have been predominantly concentrated on the downstream aspects of TFDM-based PON systems, with limited attention paid to the upstream segment. However, the critical impact of IQ skews in the upstream domain warrants further investigation due to their significant impact on system performances. Consequently, an efficient preamble, which is satisfied on-line skew estimation, compensation and various DSP function simultaneously, is urgently needed. 

In this work, we mathematically model and experimentally verify the impact of transceiver IQ skew in TFDM-PON upstream with four subcarriers from two ONUs. To address the impairments of IQskewandnot addadditional trainingsequence overhead, we combine the transceiver IQ skew estimation function with upstream burst-mode DSP for the first time. The proposed online IQ skew estimation scheme is designed to operate during normal upstream transmission, enabling continuous monitoring and compensation of IQ skew without introducing additional signal overhead. This transparent integration allows the receiver to maintain high signal integrity by tracking and correcting IQ skew, thereby minimizing the impact of skew on system performance. This work is an extension of the paper at OFC 2025, with some results discussed and presented during the conference [18]. In the expansion, three cases with transmitter (Tx) or receiver (Rx) IQ skew, four subcarriers from one ONU (Case 1), two subcarriers from two ONUs (Case 2), and three subcarriersfromONU1andonesubcarrierfromONU2(Case3) have been discussed. Thanks to accurate IQ skew compensation, the sensitivity penalty with IQ skew for three cases under subcarriers power imbalance can be discussed, which offer important guidance for the development of coherent 400G TFDM-PON 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 43, NO. 17, SEPTEMBER 1, 2025 

8042 

**==> picture [233 x 146] intentionally omitted <==**

## Fig. 2. The training sequences and burst-mode DSP. 

upstream systems. The main contributions of the work are as follows: 

- r In our proposed scheme, the transceiver IQ skew is online estimated by training sequences which are used for burst DSP. We realize online IQ skew estimation using 1024symbols training sequences with an 81.92-ns duration at 12.5 Gbaud per subcarrier. As a proof of concept, the transceiver IQ skew estimation error is within _±_ 0.3 ps which is no effect on sensitivity. 

- r We verify the feasibility of the proposed DSP scheme in a 400G TFDM-PON upstream system with four subcarriers from two ONUs. After IQ skew compensation, we successfully achieve _−_ 28-dBm sensitivity for 16-QAM signals 

While current ITU-T standardization efforts for very-highspeed passive optical networks (PONs) are focused on 200GPON [19], the 400G configuration explored in this work is intended as a forward-looking scenario to evaluate algorithm scalability and robustness. Importantly, the proposed IQ skew estimation algorithm is equally applicable to 200G PON systems and other coherent PON architectures with reduced subcarrier count or lower per-subcarrier bitrates. 

The remainder of the paper is organized as follows. In Section II, the burst-mode preamble design and corresponding DSP principle is introduced. In Section III, we introduce the experimental setups of 400G upstream TFDM PON. In Section IV, the experimental results and discussions are demonstrated to verify the performance of the proposed burst-mode DSP scheme. Finally, the paper is concluded in Section V. 

## II. PRINCIPLES 

In this section, we firstly introduce the proposed burst-mode preamble design and the corresponding DSP principles. Then the DSCM signal in TFDM-PON upstream affected by Tx and Rx IQ skews are analyzed. Finally, the principle of online IQ skew estimation is given. 

## _A. Preamble Design and Burst-Mode DSP_ 

Fig. 2 shows the proposed burst-mode preamble design and the burst-mode DSP. In the training sequence A (TS-A), real 

part is the sequence with period [1, _−_ 1] and image part is the sequence with period [1, 1, _−_ 1, _−_ 1], whose spectrums are tones at half of baud rate _f_ 1 and a quarter of baud rate _f_ 2. Specifically, the TS-A can be expressed as: 

**==> picture [223 x 14] intentionally omitted <==**

where _N_ is the length of the TS-A, _⌊·⌋_ denotes the floor function. TS-A is time interleaved in X and Y polarization. In X polarization, the zero sequence is followed by TS-A. In Y polarization, TS-A is followed by the zero sequence. The training sequence B (TS-B) with QPSK symbols is the same structure as above. In the payload, training sequence C (TS-C) with distributed QPSK pilot symbols are inserted for pilot-aided carrier phase recovery(CPR).Inburst-modeDSP,framedetection,transceiver IQ skew estimation, one-tap SOP estimation, timing recovery, and frequency offset estimation (FOE) are firstly realized by TS-A. After the frame synchronization based on TS-B, constant modulus algorithm (CMA) based on TS-B is used to achieve the fast convergence of channel estimation. Non-zero TS-A and TS-B respectively contain 512 and 128 symbols (total 1024 and 256 symbols). The training sequences per subcarrier contain a totalTSof1280symbols(102.4ns).Thepayloadcontains28560 symbols. Spaced QPSK pilot symbols TS-C are inserted into every48payloadsymbols,whichaccountedfor2.08%overhead. 

## _B. Tx/Rx IQ Skew Model in TFDM-PON Upstream_ 

In the practical TFDM-PON upstream coherent system, the baseband signals from different ONUs form a DSCM signal in OLT. In our model, we take the cases of two ONUs as an example. 

Considering four complex-valued baseband signals in pol. X or pol. Y from two ONUs which can be expressed as 

**==> picture [212 x 12] intentionally omitted <==**

where _xk_ ( _n_ ) are the baseband signals of four subcarriers. _xIk_ ( _n_ ) and _xQk_ ( _n_ ) are real and imaginary parts of them. In three cases, these signals are merged into a signal with DSCM. The DSCM signal from ONU _i_ can be expressed as 

**==> picture [197 x 24] intentionally omitted <==**

where _i_ = 1 _,_ 2 indicates ONU’s identity document (ID), and _Si_ is the set of subcarrier IDs allocated to ONU _i_ . 

r For Case 1, _S_ 1 = _{_ 1 _,_ 2 _,_ 3 _,_ 4 _}, S_ 2 = _∅_ r For Case 2, _S_ 1 = _{_ 1 _,_ 2 _}, S_ 2 = _{_ 3 _,_ 4 _}_ r For Case 3, _S_ 1 = _{_ 1 _,_ 2 _,_ 3 _}, S_ 2 = _{_ 4 _} wck_ = 2 _π[f] f[ck] s_[,] _[ f][ck]_[ are the carrier frequencies of DSCM,] _[ f][s]_[ is] the baud rate. When the real and imaginary parts are separated, (3) can also be expressed as 

**==> picture [216 x 86] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

ZHAO et al.: PREAMBLE DESIGN FOR ONLINE IQ-SKEW ESTIMATION IN UPSTREAM 400G COHERENT TFDM-PON 

8043 

where _xT xi,I_ ( _n_ ) and _xT xi,Q_ ( _n_ ) are the real and imaginary parts of _xT xi_ ( _n_ ). When these signals are input into transmitters, they will be impaired by Tx IQ skew _τT x,i_ , which is from ONU1 or 

**==> picture [216 x 11] intentionally omitted <==**

wheremodulation, the optical signal can be expressed as _NT x,i_ = _[τ][T x] Ts[,][i]_[,] _[T][s]_[is][the][symbol][period.][After][optical] 

**==> picture [195 x 11] intentionally omitted <==**

**==> picture [195 x 11] intentionally omitted <==**

where _wo_ 1 = 2 _π[f] f[o] s_[1][and] _[w][o]_[2][= 2] _[π][f] f[o] s_[2][,] _[f][o]_[1][ and] _[f][o]_[2][ arethecenter] frequency of optical carriers. 

After fiber transmission, the optical signals from different ONUs are frequency division multiplexed and are coupled with a local oscillator (LO) for coherent detection. The aggregated received optical signal can be expressed as 

**==> picture [198 x 12] intentionally omitted <==**

Assuming that the LO can be expressed as exp _{j_ [ _wLOn_ + _φ_ ( _n_ )] _}_ , where _wLO_ = 2 _π[f] f[LO] s_[,] _[f][LO]_[is][the][frequency][of][LO,] _φ_ ( _n_ ) is the phase noise from LO. After coherent detection, the received signal can be approximately expressed as 

**==> picture [213 x 12] intentionally omitted <==**

For all cases, the (20) can be expressed as 

**==> picture [252 x 11] intentionally omitted <==**

**==> picture [254 x 43] intentionally omitted <==**

**==> picture [251 x 30] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

where _xRx,I_ ( _n_ ) and _xRx,Q_ ( _n_ ) are the real and imaginary part of _xRx_ ( _n_ ). Δ _wi_ = 2 _π_[Δ] _f[f] s[i]_[,][ Δ] _[f][i]_[are the frequency offset of LO] and optical carrier _foi_ . When the received signal suffers the Rx IQ skew _τRx_ , it can be expressed as 

**==> picture [252 x 32] intentionally omitted <==**

## _C. Transceiver IQ Skew Estimation in TFDM-PON Upstream_ 

In this paper, the training sequence used in IQ skew estimation is TS-A. As mentioned above, TS-A from two ONUs can be expressed as 

**==> picture [217 x 11] intentionally omitted <==**

Substitute (16) into (13) and (14), the equation of TS-A with transceiver IQ skews can be expressed. In order to analyze the feasibility of the algorithm more concisely, we will extract a subcarrier for analysis. The subcarrier at receiver can be 

expressed as 

**==> picture [251 x 84] intentionally omitted <==**

**==> picture [251 x 11] intentionally omitted <==**

where Δ _wsub_ = 2 _π_[Δ] _[f] f[sub] s_ , Δ _fsub_ denotes the center frequency of subcarrier. Considered the Fourier transform of (17) and (18), they can be expressed as 

**==> picture [244 x 171] intentionally omitted <==**

where _N_ denotes the FFT size, Δ _ksub_ , _k_ 1, and _k_ 2 denote the discrete form of Δ _fsub_ , _f_ 1 and _f_ 2. _φ_ 1( _k_ ) and _φ_ 2( _k_ ) are the Fourier transform of cos _φ_ ( _n_ ) and sin _φ_ ( _n_ ). The _φ_ 1( _k_ ) and _φ_ 2( _k_ ) can be considered as _δ_ ( _k_ ) and 0 when laser linewidth is approaching 0. By extracting the tones in formulas (20) and (21), the transceiver IQ skews can be calculated through the Godard phase detector [17], [18]: 

**==> picture [248 x 149] intentionally omitted <==**

**==> picture [233 x 70] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 43, NO. 17, SEPTEMBER 1, 2025 

8044 

**==> picture [66 x 176] intentionally omitted <==**

**==> picture [39 x 32] intentionally omitted <==**

**==> picture [271 x 174] intentionally omitted <==**

**==> picture [66 x 176] intentionally omitted <==**

Fig. 3. Experimental setup and DSP. (a) Transmitter (Tx) DSP. (b) Subcarriers allocation of 3 cases. (c) & (d) The transmitted signal spectra with 0, 5, 10, 15-ps Tx IQ skew in Case 2 & 3. (e) Receiver (Rx) DSP. 

**==> picture [217 x 71] intentionally omitted <==**

where i = 1, 2, j = I, Q, _n_ 0 is the frequency points around tones. According to formulas (21) and (22), the transceiver IQ skew values are estimated. However, the accuracy of IQ skew estimation is related to the linewidth of laser and the location of tones is changed with frequency offset. Therefore, adding up the values of frequency points near the tones is to avoid the influence of linewidth and frequency offset. 

## III. EXPERIMENTAL SETUP AND DSP PROCEDURES 

Using the above burst-mode DSP based training sequences, we experimentally demonstrate the upstream burst signals detection in a 400G TFDM-PON, as illustrated in Fig. 3. Fig. 3(a) shows the Tx DSP. DSCM technology is used to generate TFDM signals. The 16QAM signal, which is mapped from input data, and training sequences together form burst frames. Tx IQ skew compensation is employed on the signals according to estimated Tx IQ skew. The subcarriers allocation of 3 cases is shown in Fig. 3(b). As shown in Fig. 3(c) and (d), the signals of Case 2 and Case 3 with 5-ps, 10-ps and 15-ps Tx IQ skews cause more serious image crosstalk than the signals without Tx IQ skew. Then, subcarrier power adjustment is performed to compensate the channel high-frequency attenuation. Subcarrier up-conversion and multiplexing are carried out according to the needs of each ONU. For each ONU, the signal is generated by 120-GSa/s digital-to analog converter (DAC) and modulated onto optical carrier by dual-polarization IQ modulator. The optical signals of two ONUs are amplified by an Erbium-doped optical fiber amplifier (EDFA). To emulate inter-ONU power imbalance in the upstream burst, variable optical attenuators (VOAs) are inserted before each ONU to independently adjust 

their transmitted optical powers. Then two optical signals are combined by a 3-dB coupler and launched into a 50-km standard single-mode fiber (SSMF). At receiver, a VOA is used to adjust receivedopticalpower(ROP).Thereceivedopticalsignal,which is coupled with a local oscillator (LO), is coherent detected in an integrated coherent receiver (ICR). Then the signals are captured by a 256-GSa/s analog-to-digital converter (ADC, Keysight UXR-0594BP). Fig. 3(e) shows the Rx DSP. The Rx IQ skew compensation is firstly employed on received signals. The burst signal recovery is employed after subcarrier separation and down-conversion. Finally, the recovered signals are sent for bit-error-rate (BER) calculation. 

## IV. EXPERIMENTAL RESULTS AND DISCUSSIONS 

In this section, we first discuss the feasibility of the proposed upstream online transceiver IQ skew estimation. Then, we test the system sensitivity after calibration and under different Tx and Rx IQ skews. Finally, we explore the sensitivity penalties caused by Tx and Rx IQ skews when the subcarriers power is imbalanced between ONUs. All the following results are tested after 50km fiber transmission and the results of X and Y polarization are averaged. 

## _A. Performance of Tx and Rx IQ Skew Estimation_ 

In our experiment, the performance of Tx/Rx IQ skew estimation under different non-zero training sequence length of TS-A are firstly discussed. Then, the Tx and Rx IQ skews are estimated 10 times to investigate the reliability of the proposed online IQ skew estimation scheme. The transceiver IQ skew estimation performance under different ROP is also evaluated to verify the feasibility of actual upstream transmission. Finally, the pre-set Tx and Rx IQ skews from _−_ 15 ps to 15 ps are estimated to ensure the large enough range which can be covered by the IQ skew estimation algorithm. 

Fig. 4(a) presents the estimation accuracy of Tx and Rx IQ skew under different non-zero TS-A training sequence lengths. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

8045 

ZHAO et al.: PREAMBLE DESIGN FOR ONLINE IQ-SKEW ESTIMATION IN UPSTREAM 400G COHERENT TFDM-PON 

**==> picture [493 x 242] intentionally omitted <==**

Fig. 4. (a) The estimated Tx/Rx IQ skew and absolute Tx/Rx IQ skew error under different non-zero training sequence length per subcarrier. (b) The estimated absolute Tx IQ skew in 10 tests. (c) The estimated absolute Rx IQ skew in 10 tests. (d) The estimated absolute Tx/Rx IQ skew under different ROP per subcarrier. (e) The estimated Tx IQ skew under different pre-set Tx IQ skew. (f) The estimated Rx IQ skew under different pre-set Rx IQ skew. 

The results are obtained by averaging ten repeated tests at the system sensitivity _−_ 28-dBm ROP level. It can be observed that when the training sequence length is 512 symbols, the estimation accuracy is very high. As the sequence length decreases, the accuracy gradually degrades. This is because shorter sequences result in reduced tone power in the frequency domain, making the estimation more susceptible to noise, thereby lowering overall precision. Based on the results shown in Fig. 4(a), we determine the optimal non-zero length of the TS-A training sequence to be 512 symbols, as it provides a good balance between estimation accuracy and overhead. Therefore, all subsequent tests presented – in Fig. 4(b) (f) are conducted using this configuration. 

To evaluate the stability and repeatability of the proposed IQ skew estimation scheme over time, we conduct ten repeated measurements, with each test performed at 30-second intervals under the same IQ skew condition. As shown in Fig. 4(b) and Fig. 4(c), all estimation results of pre-set _±_ 2.0 ps and _±_ 5.0 ps consistently fall within a _±_ 0.3 ps error range, demonstrating that each individual test remains highly accurate and stable despite temporal variations and potential burst-mode fluctuations. This confirms the robustness of the proposed method in practical burst-mode PON scenarios, where environmental or system-level variations may occur over time. 

Fig. 4(d) presents the estimated absolute Tx and Rx IQ skew values under different received optical power (ROP) levels per subcarrier. In our experiment, the system sensitivity for four subcarriers is _−_ 28 dBm, corresponding to _−_ 34 dBm per subcarrier. To verify the robustness of the proposed IQ skew estimation algorithm, we tested across a range of ROP values from _−_ 35 dBm to _−_ 31 dBm per subcarrier, covering the typical operational region around the sensitivity threshold. At each ROP 

level, ten estimation trials are conducted using the same method described in Fig. 4(b) and (c)—that is, one measurement every 30 seconds, and the final result is the average of ten tests. The estimated IQ skew values for both Tx and Rx IQ skew consistently fall within _±_ 0.3 ps of the pre-set values across the entire ROP range. These results demonstrate that the proposed IQ skew estimation algorithm remains accurate and stable across all practical ROP conditions, confirming its robustness and feasibility for real-world TFDM-PON deployment. The method maintains high estimation precision even near the system sensitivity limit, ensuring compatibility with burst-mode upstream reception scenarios. 

As shown in Fig. 4(e) and (f), the proposed estimation algorithm is evaluated across a wide range of pre-set Tx and Rx IQ skew values, from _−_ 15 ps to +15 ps, to verify its applicability under various transceiver impairment conditions. The tests are conducted at the system sensitivity ROP level, and each data pointrepresentstheaverageresultoftenrepeatedmeasurements. The estimation errors for both Tx and Rx IQ skews are consistently controlled within _±_ 0.3 ps, confirming the high accuracy of the proposed method. Moreover, the Tx IQ skew estimation remains robust even in the presence of a 5-ps Rx IQ skew, and vice versa, demonstrating that the estimation of one skew component is not significantly affected by the presence of the other. These results validate the feasibility and robustness of the proposed online IQ skew estimation scheme under burst-mode upstream DSP conditions and confirm its reliability over a wide range of practical operating scenarios. 

Based on the experimental results shown in Fig. 4(b) and (c), the maximum single-shot estimation error of the proposed IQ skew estimation scheme remains within _±_ 0.3 ps. In the other 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 43, NO. 17, SEPTEMBER 1, 2025 

8046 

**==> picture [496 x 133] intentionally omitted <==**

Fig. 5. (a) The BER performance in upstream transmission after Tx and Rx IQ skew compensation. (b) The sensitivity per subcarrier under different pre-set Tx IQ skew in three cases. (c) The sensitivity per subcarrier under different pre-set Rx IQ skew in three cases. 

subfigures of Fig. 4, the reported IQ skew estimation values are the averaged results over ten repeated measurements, which further improve the accuracy and stability of the estimation. In practical deployment, the estimated value can be selected either from a single measurement or as an average, depending on the system requirements and performance trade-offs. Additionally, the estimated Tx IQ skew values can be fed back to the ONU via the downstream control channel using standard management protocols, such as optical network terminal management and control interface (OMCI) [20] or operations, administration, and maintenance (OAM) [21]. Given the slow variation of IQ skew, such feedback can be performed at low update rates without burdening the system. 

## _B. Analysis of Coherent Transmission With Tx and Rx IQ Skew_ 

In the previous part, we have tested the performance of IQ skew estimation. In this section, we compensate for Tx and Rx IQ skew of transceiver based on the estimated values. After compensation, the receiver sensitivity of three cases is tested. At receiver, the OLT will receive the subcarriers from different ONUs and aggregate them together for coherent reception. The damage caused by Tx and Rx IQ skew to the signals will be quite severe. To evaluate the damage, we test the sensitivity per subcarrier under Tx or Rx IQ skew in three cases. 

Fig. 5(a) presents the BER performance of three cases under different total ROP after Tx and Rx IQ compensation. Under the BER threshold 2E-2, the sensitivities of Case 1, Case 2 and Case 3 are _−_ 28 dBm. Thanks to the power optimization of subcarriers,theaverageBERofsubcarriersfromdifferentONUs is almost the same. Therefore, the sensitivities per subcarrier of Case 1, Case 2 and Case 3 are _−_ 34 dBm. To explore the effect of Tx and Rx IQ skews on signals, Fig. 5(b) and (c) present the sensitivity per subcarrier under different pre-set Tx and Rx IQ skew in three cases. The pre-set Tx IQ skew is ranged from 0 ps to 1.8 ps. When 0.6-ps, 1.2-ps and 1.8-ps Tx IQ skews are compensated, about 0.5-dB, 2.0-dB and 4.5-dB sensitivity gain per subcarrier are obtained. The pre-set Rx IQ skew is ranged from 0 ps to 1.8 ps. When 0.6-ps, 1.2-ps and 1.8-ps Rx IQ skews are compensated, about 0.5-dB, 2.0-dB and 4.5-dB sensitivity gain per subcarrier are obtained. For the transmitted 

12.5 GBaud _×_ 4 16QAM signals, about _−_ 33.7-dBm sensitivity per subcarrier is obtained under effects of 0.3-ps Tx IQ skew or 0.3-ps Rx IQ skew. The sensitivity is almost the same as the case without transceiver IQ skew. Therefore, the sensitivity is almost unaffected after Tx and Rx IQ skew compensation, which are estimated by our proposed scheme. These experiment results further illustrate the necessity of the calibration process for high-speed coherent optical transmission systems and the effectiveness of our proposed online calibration method. 

## _C. System Performance Analysis With Tx and Rx IQ Skew When Subcarriers Power Is Imbalanced Among ONUs_ 

In the multi-user upstream scenario of 400G TFDM PON, power imbalance of subcarriers among different ONUs often occurs. It is instructive to investigate the sensitivity penalty with different transceiver IQ skew when there is power difference between subcarriers. Thanks to the proposed scheme that can accurately estimate transceiver IQ skew, in this section, we will discuss the impairments caused by transceiver IQ skew in the case of imbalanced subcarrier power. In this section, sensitivity penalty per subcarrier is defined as the increase in required ROP for the lowest-power subcarrier when impairments such as IQ skew and power imbalance are introduced. Specifically, the baseline sensitivity per subcarrier is calculated from the total receiver sensitivity in the ideal case (e.g., _−_ 28 dBm total ROP for four subcarriers corresponds to _−_ 34 dBm per subcarrier). The maximum tolerable power difference is defined as the largest power imbalance between subcarriers of the strongest andweakestONUsunderwhichtheworstsubcarriersstillsatisfy the BER threshold of 2E-2. 

In Case 2, the input optical powers of ONU 1 and ONU 2 are both 2 dBm when there is no power difference. The power difference between ONU 1 and ONU 2 is controlled by VOA. Fig. 6(a) and (b) present the sensitivity penalty per subcarrier versus power difference under different Tx and Rx IQ skews. When the power differences per subcarrier are 1, 2, 3, 4, and 5 dB, the sensitivity penalties per subcarrier without transceiver IQ skew are 0.7, 1, 1.5, 1.8, and 2.0 dB. In Case 3, the input optical powers of ONU 1 and ONU 2 are _−_ 1 dBm and 3.8 dBm respectively when there is no power difference. Considering the 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

ZHAO et al.: PREAMBLE DESIGN FOR ONLINE IQ-SKEW ESTIMATION IN UPSTREAM 400G COHERENT TFDM-PON 

8047 

**==> picture [241 x 383] intentionally omitted <==**

Fig. 6. (a) The sensitivity penalty per subcarrier versus power difference under different Tx IQ skews in Case 2. (b) The sensitivity penalty versus power difference per subcarrier under different Rx IQ skews in Case 2. 

worst case, we make the power of each subcarrier in ONU2 higher than that of ONU1. Fig. 7(a) and (b) present the sensitivity penalty per subcarrier versus power difference of ONU1 and ONU2 under different Tx and Rx IQ skews. When the power differences per subcarrier are 1, 1, 2, 3, 4 and 5 dB, the sensitivity penalties per subcarrier without transceiver IQ skew are 1.2, 2.3, 4.3, 6.3, and 9.0 dB. A noticeable sensitivity penalty per subcarrier is observed even when the IQ skew is set to zero. This degradation is primarily caused by the power imbalance between ONUs, which interacts with the limited resolution of the ADC at the receiver. As the power difference increases, the ROP required by the lowest-power subcarrier also increases to maintain BER performance. However, since only the total ROP of all four subcarriers from both ONUs can be adjusted at the receiver, increasing the total ROP to compensate for the weakest subcarrier inevitably results in excessive power for the stronger subcarriers. This compresses the ADC’s dynamic range and increases quantization noise, which disproportionately affects thelowest-powersubcarrier,leadingtoitsdegradedperformance 

**==> picture [241 x 392] intentionally omitted <==**

Fig. 7. (a) The sensitivity penalty per subcarrier versus power difference under different Tx IQ skews in Case 3. (b) The sensitivity penalty per subcarrier versus power difference under different Rx IQ skews in Case 3. 

even in the absence of IQ skew. A comparison between Case 2 (Fig. 6) and Case 3 further highlights the role of power configuration in system performance. Under the same per-subcarrier power difference between ONU 1 and ONU 2, the total ROP in Case 3 is higher, resulting in more severe ADC saturation effects and greater quantization noise. Consequently, Case 3 exhibits a sharper degradation trend, while Case 2 shows a more gradual decline in sensitivity. As the power difference increases, the impact of transceiver IQ skew on sensitivity becomes more severe due to the enhanced distortion effects on lower-power subcarriers. In Case 2, for the lower-power signals with 0.3-ps, 0.6-ps, 0.9-ps, and 1.2-ps Tx IQ skews, the maximum tolerable power differences per subcarrier are 4, 4, 3, and 2 dB, respectively, and the corresponding sensitivity penalties are 4.8, 6.9, 7.2, and 6.5 dB. The increasing sensitivity penalty reflects the growing difficulty in maintaining signal integrity as the skew increases, especially when combined with moderate power imbalance. For Rx IQ skews of 0.3 ps, 0.6 ps, 0.9 ps, and 1.2 ps, the maximum 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 43, NO. 17, SEPTEMBER 1, 2025 

8048 

tolerable power differences are 4, 3, 3, and 2 dB, with sensitivity penalties of 5.0, 4.0, 6.1, and 6.1 dB, respectively. In Case 3, where inter-ONU power imbalance is more severe, the system becomes even more sensitive to IQ skew. For signals with 0.3-ps, 0.6-ps, 0.9-ps, and 1.2-ps Tx IQ skews, the maximum tolerable power differences per subcarrier drop to 4, 3, 2, and 1 dB, respectively, with corresponding sensitivity penalties of 8.0, 7.8, 7.0, and 6.1 dB. These results indicate that in highly asymmetric power scenarios, even small IQ skew can significantly reduce the system’s tolerance margin. For Rx IQ skews of 0.3 ps, 0.6 ps, 0.9 ps, and 1.2 ps, the maximum tolerable power differences are 4, 3, 2, and 2 dB, and the sensitivity penalties are 8.0, 7.2, 5.9, and 7.0 dB, respectively. This degradation can be attributed to image crosstalk generated by high-power subcarriers, which is more pronounced due to their stronger spectral components. When the power of a low-power subcarrier is sufficiently reduced, the symmetric image spectrum originating from a high-power subcarrier may entirely overwhelm or distort the desired signal of the weaker subcarrier. This leads to severe performance degradation, particularly in burst-mode TFDM-PON systems with inter-ONU power imbalance, where image leakage becomes a dominant impairment that cannot be neglected. The presence of transceiver IQ skew significantly reduces the power difference tolerance of the lower-power subcarrier, thereby severely degrading the overall power budget of the system. In TFDM-PON, the inherent power imbalance among ONUs further amplifies the impact of IQ skew, underscoring the necessity for accurate and robust IQ skew estimation algorithms. Moreover, given the strict constraints on training sequence overhead in upstream burst-mode PON systems, the proposed IQ skew estimation scheme is designed to share the same training sequence as the burst-mode DSP, introducing no additional overhead. This joint design ensures both estimation accuracy and protocol efficiency, making it well-suited for practical implementation in high-speed coherent TFDM-PON networks. 

## V. CONCLUSION 

This paper integrates online transceiver IQ skew estimation with burst-mode DSP and successfully applies it to a 400G TFDM-PON upstream system. By optimizing the design of training sequences, high-precision IQ skew estimation (with an error of _±_ 0.3 ps) under a dual-ONU TFDM-PON upstream scenario is achieved. Experimental results show that the system sensitivity is significantly improved after compensation and it supports a reception performance of _−_ 34 dBm per subcarrier. Further analysis reveals that as the subcarrier power difference increase, uncompensated IQ skew leads to exacerbated sensitivity degradation, necessitating IQ skew compensation to enhance system tolerance. This solution provides critical technical support for transceiver IQ skew calibration in next-generation high-speed coherent PONs and can be extended to higher rates and complex modulation formats in the future. 

Future work will focus on the quantitative impact of laser linewidth and frequency drift on IQ skew estimation accuracy, particularly under burst-mode constraints, to further enhance the robustness of the proposed scheme in practical deployment 

scenarios. Additionally, although this work uses a 400G TFDMPON configuration as the baseline to evaluate the proposed IQ skew estimation scheme, the approach is also readily applicable to lower-rate systems such as 200 G TFDM-PON. In such a scenario, the system can maintain the same frequency-division multiplexing structure with four subcarriers, while reducing the modulation format from 16-QAM to QPSK on each subcarrier. Under this configuration, the impact of IQ skew is expected to be reduced but not eliminated. First, since the per-subcarrier baud rate remains constant, the spectral image crosstalk of IQ skew remains nearly unchanged. Second, the use of QPSK improves the system’s tolerance to IQ skew due to the lower constellation density, resulting in smaller penalties in terms of BER and receiver sensitivity. Finally, the proposed IQ skew estimation algorithm is independent of the payload modulation order and thus can be directly applied to 200G TFDM-PON without modification. Moreover, the improved skew tolerance in QPSK-based systems allows for further optimization, such as reducing the length of the TS-A training sequence to minimize overhead because of lower calibration accuracy requirements. 

## ACKNOWLEDGMENT 

The authors would like to thank Keysight Technologies for the testing equipment used in this paper. 

## REFERENCES 

- [1] D. Zhang, D. Liu, X. Wu, and D. Nesset, “Progress of ITU-T higher speed passive optical network (50G-PON) standardization,” _J. Opt. Commun. Netw._ , vol. 12, no. 10, pp. D99–D108, Oct. 2020, doi: 10.1364/ JOCN.391830. 

- [2] M. S. Faruk, X. Li, D. Nesset, I. N. Cano, A. Rafel, and S. J. Savory, “Coherent passive optical networks: Why, when, and how,” _IEEE Commun. Mag._ , vol. 59, no. 12, pp. 112–117, Dec. 2021, doi: 10.1109/ MCOM.010.2100503. 

- [3] J. Zhang and Z. Jia, “Coherent passive optical networks for 100G/ _λ_ -andbeyond fiber access: Recent progress and outlook,” _IEEE Netw._ , vol. 36, no. 2, pp. 116–123, Mar./Apr. 2022, doi: 10.1109/MNET.005.2100604. 

- [4] L. A. Campos, Z. Jia, H. Zhang, and M. Xu, “Coherent optics for access from P2P to P2MP [Invited],” _J. Opt. Commun. Netw._ , vol. 15, no. 3, pp. A114–A123, Mar. 2023, doi: 10.1364/JOCN.469869. 

- [5] J. Zhao et al., “Sensitivity-improved and dispersion-tolerant lite-coherent hybrid receiver for digital-analog radio-over-fiber mobile fronthaul,” _J. Lightw. Technol._ , vol. 43, no. 11, pp. 5067–5075, Jun. 2025, doi: 10.1109/JLT.2025.3550176. 

- [6] H. Zhang, Z. Jia, L. A. Campos, and C. Knittle, “Low-cost 100G coherent PON enabled by TFDM digital subchannels and optical injection locking,” 2023. 

- [7] J. Zhang, Z. Jia, H. Zhang, M. Xu, J. Zhu, and L. A. Campos, “Rateflexible single-wavelength TFDM 100G coherent PON based on digital subcarrier multiplexing technology,” in _Proc. Opt. Fiber Commun. Conf. Exhib._ , Mar. 2020, pp. 1–3. 

- [8] G. Li et al., “Burst-mode signal reception for 200G coherent time and frequency division multiplexing passive optical network,” _J. Lightw. Technol._ , vol. 43, no. 2, pp. 429–438, Jan. 2025, doi: 10.1109/JLT.2024.3431668. 

- [9] J. Zhang, Z. Jia, M. Xu, H. Zhang, and L. A. Campos, “Efficient preamble design and digital signal processing in upstream burst-mode detection of 100G TDM coherent-PON,” _J. Opt. Commun. Netw._ , vol. 13, no. 2, pp. A135–A143, Feb. 2021, doi: 10.1364/JOCN.402591. 

- [10] H. Wang et al., “Fast-convergence digital signal processing for Coherent PON using digital SCM,” _J. Lightw. Technol._ , vol. 41, no. 14, pp. 4635–4643, Jul. 2023, doi: 10.1109/JLT.2023.3243828. 

- [11] C. Zhu, N. Kaneda, and J. Lee, “Reception of burst mode high-order QAM signals with pilot-aided digital signal processing,” _presented at Opt. Fiber Commun. Conf._ , San Diego, CA, USA, 2018, Paper M1C.5, doi: 10.1364/OFC.2018.M1C.5. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 

ZHAO et al.: PREAMBLE DESIGN FOR ONLINE IQ-SKEW ESTIMATION IN UPSTREAM 400G COHERENT TFDM-PON 

8049 

- [12] T. Duthel et al., “DSP design for coherent optical point-to-multipoint transmission,” _J. Lightw. Technol._ , vol. 42, no. 3, pp. 1109–1118, Feb. 2024, doi: 10.1109/JLT.2023.3322076. 

- [13] W. Wang, Z. Wu, D. Zou, Q. Sui, C. Lu, and F. Li, “Training sequences design for simultaneously transceiver IQ skew estimation in coherent systems,” _J. Lightw. Technol._ , vol. 42, no. 15, pp. 5088–5098, Aug. 2024, doi: 10.1109/JLT.2024.3385422. 

- [14] W. Wang, Z. Wu, D. Zou, F. Li, and Z. Li, “A novel low complexity and precise transceiver IQ skew calibration method for single carrier coherent system,” _presented at Opt. Fiber Commun. Conf._ , San Diego, CA, USA, 2024, Paper Th2A.7, doi: 10.1364/OFC.2024.Th2A.7. 

- [15] W. Wang et al., “A low complexity coherent 16 _×_ 400 gbit/s 4SC16QAM DSCM system with precise transceiver IQ skew compensation and simplified equalization,” _presented at Opt. Fiber Commun. Conf._ , San Diego, CA, USA, 2024, Paper W1E.7, doi: 10.1364/OFC.2024. W1E.7. 

- [16] L. Fan, Y. Yang, Q. Zhang, S. Gong, Y. Jia, and Y. Yao, “Robust, inservice, and joint monitoring of a dual-polarization transceiver IQ skew for a coherent DSCM system without channel impairment compensation,” _Opt. Lett._ , vol. 49, no. 1, pp. 129–132, Jan. 2024, doi: 10.1364/OL.509308. 

- [17] J. Zhou et al., “IQ skew and imbalance estimation for coherent point-tomulti-point optical networks,” Apr. 2024, _arXiv:2401.17566_ . 

- [18] J. Zhao et al., “Preamble design for online IQ skew estimation in burstmode DSP for 400G coherent TFDM-PON upstream,” presented at Opt. Fiber Commun. Conf., San Francisco, CA, USA, 2025, Paper Tu2I.4. 

- [19] D. Nesset, “Progress on very high speed PON in ITU-T,” _presented at Opt. Fiber Commun. Conf._ , Los Angeles, CA, USA, 2025, Paper Th1J.5. 

- [20] International Telecommunication Union (ITU), “ONU Management and Control Interface (OMCI) specification,” _ITU-T Recommendation G.988_ , 4th ed., Geneva, Switzerland, Nov. 13, 2022, doi: 11.1002/1000/15125. 

- [21] International Telecommunication Union (ITU), “Operation, administration and maintenance (OAM) functions and mechanisms for ethernetbasednetworks,” _ITU-TRecommendationG.8013/Y.1731_ ,6thed.,Geneva, Switzerland, Jun. 13, 2023, doi: 11.1002/1000/15553. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 06,2026 at 15:23:09 UTC from IEEE Xplore.  Restrictions apply. 


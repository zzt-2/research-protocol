1 

## Discrete FRFT-Based Frame and Frequency Synchronization for Coherent Optical Systems 

Oluyemi Omomukuyo, Shu Zhang, Octavia Dobre, Ramachandran Venkatesan, and Telex M. N. Ngatched 

_**Abstract**_ **—A joint frame and carrier frequency synchronization algorithm for coherent optical systems, based on the digital computation of the fractional Fourier transform (FRFT), is proposed. The algorithm utilizes the characteristics of energy centralization of chirp signals in the FRFT domain, together with the time and phase shift properties of the FRFT. Chirp signals are used to construct a training sequence (TS), and fractional cross-correlation is employed to define a detection metric for the TS, from which a set of equations can be obtained. Estimates of both the timing offset and carrier frequency offset (CFO) are obtained by solving these equations. This TS is later employed in a phase-dependent decision-directed least-mean square algorithm for adaptive equalization. Simulation results of a 32-Gbaud coherent polarization division multiplexed Nyquist system show that the proposed scheme has a wide CFO estimation range and accurate synchronization performance even in poor optical signal-to-noise ratio conditions.** 

_**Index Terms**_ **—Chirp signals, coherent optical communication, fractional correlation, fractional Fourier Transform, frame synchronization, frequency offset estimation, optical fiber communication, training sequence.** 

## I. INTRODUCTION 

COHERENT optical technology has been actively investigated in recent years as a promising technique for next-generation high-capacity transport networks. Current state-of-the-art coherent optical systems utilize digital signal processing (DSP) to compensate for various linear impairments in optical transmission such as chromatic dispersion (CD) and polarization-mode dispersion (PMD). In addition, these systems support the use of a combination of multi-level modulation and polarization division multiplexing (PDM) to increase the number of transported bits. 

In digital coherent receivers, a static filter is usually employed for bulk CD compensation, while a set of adaptive finite-impulse-response (FIR) filters are used in performing polarization demultiplexing as well as to compensate for timevarying channel impairments such as PMD and the state of polarization [1]. Blind tap adaptation algorithms like the constant-modulus algorithm (CMA) and the multi-modulus algorithm (MMA) are commonly used to update the tap coefficients of the adaptive FIR filters. However, both CMA and MMA are disadvantaged by long convergence time and the singularity problem [2]. To avoid these problems, a 

training sequence (TS)-based phase-dependent decisiondirected least-mean square (DD-LMS) algorithm has been proposed [3]. The DD-LMS algorithm requires accurate frame synchronization to identify the TS prior to adaptive equalization. In addition, the carrier frequency offset (CFO) has to be estimated and compensated for. 

For the frame synchronization, the Schmidl and Cox’s algorithm [4] can be adapted for coherent optical single-carrier systems as demonstrated by Zhou in [5]. However, as shown in [6], the Schmidl and Cox’s algorithm yields frame synchronization errors under poor optical signal-to-noise ratio (OSNR) conditions. For the frequency synchronization, most of the existing methods in the literature depend on using either the _M_ -th power operation [7] or a TS [5] to remove the modulated data phase. Notwithstanding, the _M_ -th power operation is disadvantaged by large computational complexity, while the accuracy of the Zhou’s TS-based algorithm [5] degrades in poor OSNR conditions. A method which does not depend on removing the modulated data phase has been proposed in [8]. However, this method is not modulationformat transparent, and has a small CFO estimation range. 

In this letter, we propose an algorithm which utilizes fractional cross-correlation, together with the time and phase shift properties of the fractional Fourier transform (FRFT), to carry out joint frame and frequency synchronization. Recently, the FRFT has also been proposed for joint synchronization for coherent optical OFDM [9]. However, the method in [9], which utilizes only the FRFT time and phase shift properties, yields frame synchronization errors even in the absence of noise. In addition, this method has a CFO estimation range of ±4 GHz, and it needs the Schmidl and Cox’s algorithm to compute the CFO. The proposed scheme is robust to amplified spontaneous emission (ASE) noise, and has a wide CFO estimation range. The proposed technique is demonstrated by means of simulations in a 32-Gbaud 16-ary quadrature amplitude modulation (16-QAM) coherent PDM system. 

## II. OPERATION PRINCIPLE 

The FRFT is a generalization of the conventional Fourier transform through an angle parameter _ϕ_ and an order parameter _α_ [10]. For each value of _ϕ_ , the 𝛼th-order FRFT rotates a time-domain signal counterclockwise by _ϕ_ [11]. In general, we can relate _ϕ_ and _α_ as follows [10]: 

**==> picture [251 x 14] intentionally omitted <==**

2 

The 𝛼th-order FRFT of a signal 𝑓(𝑡) can be defined as [12]: 

**==> picture [252 x 50] intentionally omitted <==**

where 𝓕[𝜙] is the FRFT operator associated with angle _ϕ_ , and 𝐾𝜙(𝑡, 𝑢) is the transform kernel, defined in (3) for values of _ϕ_ that are not multiples of _π_ . There are several discrete computational algorithms for the FRFT, but in the proposed scheme, we make use of the algorithm in [10] because of its computational efficiency (𝑂(𝑁log𝑁)) for an _N_ -length signal. 

chirp signal 1, 𝑃1𝑏(𝑢) = 𝑟𝑥(𝑏𝑁𝑠 + 𝑢), 𝑟𝑥 represents the discrete received time-domain samples, 𝑏= 0,1, ⋯, 𝐵−1 is the block index, 𝑢= 0,1, ⋯, 𝑁𝑠 −1, 𝐴(𝑢) are the discrete samples corresponding to the transmitted chirp signal 1, and * is the complex conjugation operation. For each block 𝑏, the FRFT sample index, 𝑢̂1𝑏, where 𝑅1𝑏(𝑢) has its peak value is: 

**==> picture [252 x 10] intentionally omitted <==**

We select the specific block 𝑏[̂] at which the maximum value of the detection metric is obtained using the following rule: 

**==> picture [252 x 12] intentionally omitted <==**

The peak shift for chirp signal 1, ∆𝑛1, is then obtained as: 

## _A. Training Sequence Design_ 

The TS used to perform the joint synchronization is obtained from two discrete-time linear chirp signals with different chirp rates. For simplicity, we consider a finiteduration discrete-time linear chirp with zero initial phase and a center frequency of 0 Hz, which can be expressed as: 

**==> picture [252 x 11] intentionally omitted <==**

where 2𝛽 is the chirp rate, 𝑇 is the sampling period, and 𝑁𝑠 is the number of discrete samples. The optimum angle, 𝜙𝑜𝑝𝑡, at which the FRFT of the chirp signal yields an impulse is [13]: 

**==> picture [251 x 25] intentionally omitted <==**

In designing the TS, two different values of 𝜙𝑜𝑝𝑡 are selected, and the corresponding values of the chirp rates are obtained from (5). These chirp rates are then used in (4) to construct the actual chirp signals. Since the constellation points of the chirp signals lie in a unit circle, the chirp signals are “sliced” and converted into 4-QAM symbols using the method in [14]. 

At the receiver, the chirp signals are detected by performing the fractional cross-correlation of the received TS and the transmitted one. This operation yields two impulses whose peaks would shift by different amounts depending on the values of the frame offset and CFO. 

## _B. Joint Frame and Frequency Synchronization_ 

For each polarization, the received symbols are divided into 𝐵 blocks, each of length 𝑁𝑠. To detect chirp signal 1, for each block, we define a detection metric 𝑅1𝑏(𝑢), obtained from the fractional cross-correlation [11] of the block with the original transmitted chirp signal 1 as follows: 

**==> picture [251 x 20] intentionally omitted <==**

where 𝜙1′ = 𝜙1𝑜𝑝𝑡 + 𝜋2 ~~,~~ and 𝜙1𝑜𝑝𝑡 is the optimal angle for 

**==> picture [252 x 22] intentionally omitted <==**

where 𝑢̂1𝑏̂ is the value of 𝑢̂1𝑏 corresponding to block 𝑏[̂] . The peak shift for chirp signal 2, ∆𝑛2, is obtained in a similar manner. A time shift ∆𝑡 and phase shift ∆𝑓 of a signal in the time domain correspond to shifts of ∆𝑡cos 𝜙 and ∆𝑓sin 𝜙 in the FRFT domain, respectively [12]. We can then construct the following set of equations which governs the peak shifts: 

**==> picture [251 x 25] intentionally omitted <==**

The solution of (10) is: 

**==> picture [253 x 55] intentionally omitted <==**

The frame offset estimate, 𝜇̂, and the CFO estimate, 𝛾̂, are: 

**==> picture [252 x 38] intentionally omitted <==**

where round(∙) rounds towards the nearest integer, and 𝑅𝑠 is the symbol rate. As shown in (11) and (13), the frequency resolution of the CFO estimation, would depend on 𝑅𝑠⁄𝑁𝑠, 𝜙1𝑜𝑝𝑡, and 𝜙2𝑜𝑝𝑡. It can also be deduced from (10)-(13) that the CFO estimation range, 𝛾max, of the proposed algorithm is: 

**==> picture [256 x 35] intentionally omitted <==**

3 

**==> picture [464 x 180] intentionally omitted <==**

Fig. 1.  Simulation setup. C1: chirp signal 1. C2: chirp signal 2. Tr: Training symbols (inserted every 1000 data symbols). PRBS: pseudo-random binary sequence. TS: training sequence. RRC: root raised-cosine. DAC: digital-to-analog converter. IQ: in-phase/quadrature phase. PBS: polarization beam splitter. PBC: polarization beam coupler. WDM: wavelength division multiplexing. EDFA: Erbium-doped fiber amplifier. SSMF: standard single-mode fiber. OBPF: optical band-pass filter. ADC: analog-to-digital converter. CD: chromatic dispersion. LMS: least-mean square. CPR: carrier phase recovery. Inset (a): Frame structure. Inset (b):  Metric for both chirp signals using (6) for a 100-symbol frame offset and a 3-GHz CFO. 

## III. SIMULATION SETUP AND RESULTS 

To investigate the performance of the proposed scheme, a model of a 32-Gbaud coherent PDM Nyquist system, whose schematic is depicted in Fig. 1, is built using VPI TransmissionMaker. Five channels are simulated with a channel spacing of 32 GHz, and the performance is assessed on the central channel. The DSP at the transmitter and receiver is performed in MATLAB. Two independent pseudo-random binary sequences are generated for the two polarization branches. For each polarization, an identical TS, comprising two chirp signals with different chirp rates, is placed at the beginning of each frame to be transmitted to achieve the joint synchronization. An additional 24 training symbols are inserted every 1000 transmitted data symbols to track the dynamic channel behaviors. The frame structure is shown in inset (a) of Fig. 1. The symbols are upsampled to 2 samples/symbol, and digitally shaped using a 73-tap root raised-cosine (RRC) filter with a roll-off factor of 0.13. 

For each channel, the electrical signals from each polarization branch are fed to digital-to-analog converters, and then used to drive two null-biased I/Q modulators. The optical source to the I/Q modulators is a continuous wave laser with a linewidth of 100 kHz. The multiplexed PDM optical signal is launched into a transmission link consisting of 10 spans of standard single-mode fiber, with 80 km and a 16-dB gain erbium-doped fiber amplifier per span. At the receiver, the central channel is selected using a 0.4-nm optical band-pass filter, and coherently detected with a polarization-diversity optical hybrid. A laser with a linewidth of 100 kHz is used as the local oscillator. The coherently-detected signal is sampled by the analog-to-digital converters, and then processed by the matched RRC filters. An overlapped frequency-domain equalizer is used for CD compensation. After CD compensation and downsampling to 1 sample/symbol, joint synchronization is carried out using the proposed algorithm. 

The processing of the algorithm is carried out independently for each polarization. The TS is then used for polarization demultiplexing using the phase-dependent DD-LMS algorithm [3]. The DD-LMS algorithm is also used to estimate the carrier phase and for residual CFO compensation. 

For all simulation results, unless otherwise mentioned, the TS length is 1024, the frame offset is 100 symbols, the CFO is 3 GHz, and the OSNR is 10 dB. In addition, 1000 trial runs have been performed for each assessment. It is clear from (11) and (14) that the performance of the proposed scheme depends on the selection of appropriate values of the angle parameters 𝜙1𝑜𝑝𝑡 and 𝜙2𝑜𝑝𝑡 in the design of the TS. For the performance assessment, we have selected 𝜙1𝑜𝑝𝑡 = −𝜙2𝑜𝑝𝑡. 

Inset (b) of Fig. 1 shows that the metric for both chirp signals is impulse-shaped. Fig. 2 shows the frame synchronization performance as a function of 𝜙2𝑜𝑝𝑡. It is observed that the timing estimation error is minimum around 𝜙2𝑜𝑝𝑡 = 𝜋4⁄ . Consequently, we have carried out the simulations using this value of 𝜙2𝑜𝑝𝑡. Fig. 3 shows the impact of a variation of the TS length on the frame and frequency synchronization performance. It is observed that for a TS length of 1024, no timing estimation errors are observed, and the CFO estimation error is ~7 MHz. The frame synchronization performance is more robust than the frequency synchronization performance to further reduction in the TS length. With the above simulation parameters, 𝛾max, as obtained using (14), is ~±16.3 GHz. Fig. 4 shows that the proposed algorithm can comfortably estimate CFOs as high as ±5 GHz, with a maximum CFO estimation error of ~11 MHz obtained. In Fig. 5, the frame and frequency synchronization performance of the proposed algorithm is compared to the TSbased Schmidl-Cox’s [4] and the Zhou’s [5] algorithms, respectively, in the presence of varying levels of the OSNR. The proposed algorithm demonstrates superior robustness to ASE noise than both algorithms. 

4 

**==> picture [163 x 127] intentionally omitted <==**

Fig. 2.  Frame synchronization performance as a function of 𝜙2𝑜𝑝𝑡. 

**==> picture [168 x 129] intentionally omitted <==**

Fig. 3.  Frame and frequency synchronization performance as a function of the TS length. 

**==> picture [170 x 128] intentionally omitted <==**

Fig. 4. Mean of estimated CFO and mean of CFO estimation error as a function of the actual CFO. 

## IV. CONCLUSION 

A novel joint frame and frequency synchronization scheme based on the FRFT has been proposed for coherent optical PDM systems. The proposed scheme, which utilizes fractional cross-correlation, has been shown to be robust to ASE noise, with a wide CFO estimation range, greater than half the symbol rate. The FRFT angle parameter can be varied in the design of the TS in the scheme to increase the accuracy of the offset estimation. 

## REFERENCES 

- [1] S. J. Savory, “Digital coherent optical receivers: algorithms and subsystems,” _IEEE J. Sel. Topics Quantum Electron_ ., vol. 16, no. 5, pp. 1164-1179, Sep.-Oct. 2010. 

- [2] K. Kikuchi, “Performance analyses of polarization demultiplexing based on constant-modulus algorithm in digital coherent receivers,” _Opt. Exp_ ., vol. 19, no. 10, pp. 9868-9880, May 2011. 

**==> picture [171 x 281] intentionally omitted <==**

Fig. 5. Synchronization performance in the presence of ASE noise. (a) Frame synchronization. (b) Frequency synchronization. 

- [3] Y. Mori, C. Zhang, and K. Kikuchi, “Novel configuration of finiteimpulse-response filters tolerant to carrier-phase fluctuations in digital coherent optical receivers for higher-order quadrature amplitude modulation signals,” _Opt. Exp._ , vol. 20, no. 24, pp. 26236-26251, Nov. 2012. 

- [4] T. M. Schmidl and D. C. Cox, “Robust frequency and timing synchronization for OFDM,” _IEEE Trans. Commun_ . vol. 45, no. 12, pp. 1613-1621, Dec. 1997. 

- [5] X. Zhou, X. Chen, and K. Long, “Wide-range frequency offset estimation algorithm for optical coherent systems using training sequence,” _IEEE Photon. Technol. Lett_ ., vol. 24, no. 1, pp. 82-84, Jan. 2012. 

- [6] O. Omomukuyo _et al._ , “Joint timing and frequency synchronization based on weighted CAZAC sequences for reduced-guard-interval COOFDM systems,” _Opt. Exp._ , vol. 23, no. 5, pp. 5777-5788, Mar. 2015. 

- [7] A. Leven _et al_ ., “Frequency estimation in intradyne reception,” _IEEE Photon. Technol. Lett_ , vol. 19, no. 6, pp. 366-368, Mar. 2007. 

- [8] Y. Cao _et al_ ., “Frequency estimation for optical coherent MPSK system without removing modulated data phase,” _IEEE Photon. Technol. Lett_ , vol. 22, no. 10, pp. 691-693, May 2010. 

- [9] H. Zhou _et al_ ., “Joint timing and frequency synchronization based on FrFT encoded training symbol for coherent optical OFDM systems,” in _Proc. OFC_ , Mar. 2016, pp. 1-3, paper Tu3K.6. 

- [10] H. M. Ozaktas _et al_ ., “Digital computation of the fractional Fourier transform,” _IEEE Trans. Sig. Proc_ ., vol. 44, no. 9, pp. 2141-2150, Sep. 1996. 

- [11] O. Akay and G. F. B-Bartels, “Fractional convolution and correlation via operator methods and an application to detection of linear FM signals,” _IEEE Trans. Sig. Proc_ ., vol. 49, no. 5, pp. 979-993, May 2001. 

- [12] L. B. Almeida, “The fractional Fourier transform and time-frequency representations,” _IEEE Trans. Sig. Proc_ ., vol. 42, no. 11, pp. 3084-3091, Nov. 1994. 

- [13] C. Capus and K. Brown, “Short-time fractional Fourier methods for the time-frequency representation of chirp signals,” _J. Acoust. Soc. Amer_ ., vol. 113, no. 6, pp. 3253–3263, Jun. 2003. 

- [14] C. C. Do _et al_ ., “Data-aided chromatic dispersion estimation for polarization multiplexed optical systems,” _IEEE Photon. J_ ., vol. 4, no. 5, pp. 2037-2049, Oct. 2012. 


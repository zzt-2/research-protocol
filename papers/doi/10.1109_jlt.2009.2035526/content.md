JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

1121 

## Optimal Polarization Demultiplexing for Coherent Optical Communications Systems 

Ioannis Roudas, Athanasios Vgenis, Constantinos S. Petrou, Dimitris Toumpakaris, Jason Hurley, Michael Sauer, John Downie, Yihong Mauro, and Srikanth Raghavan 

_**Abstract—**_ **Spectrally-efficient optical communications systems employ polarization division multiplexing (PDM) as a practical solution, in order to double the capacity of a fiber link. Polarization demultiplexing can be performed electronically, using polarization-diversity coherent optical receivers. The primary goal of this paper is the optimal design, using the maximum-likelihood criterion, of polarization-diversity coherent optical receivers for polarization-multiplexed optical signals, in the absence of polarization mode dispersion (PMD). It is shown that simultaneous joint estimation of the symbols, over the two received states of polarization, yields optimal performance, in the absence of phase noise and intermediate frequency offset. In contrast, the commonly used zero-forcing polarization demultiplexer, followed by individual demodulation of the polarization-multiplexed tributaries, exhibits inferior performance, and becomes optimal only if the channel transfer matrix is unitary, e.g., in the absence of polarization dependent loss (PDL), and if the noise components at the polarization diversity branches have equal variances. In this special case, the zero-forcing polarization demultiplexer can be implemented by a 2 2 lattice adaptive filter, which is controlled by only two independent real parameters. These parameters can be computed recursively using the constant modulus algorithm (CMA). We evaluate, by simulation, the performance of the aforementioned zero-forcing polarization demultiplexer in coherent optical communication systems using PDM quadrature phase shift keying (QPSK) signals. We show that it is, by far, superior, in terms of convergence accuracy and speed, compared to conventional CMA-based polarization demultiplexers. Finally, we experimentally test the robustness of the proposed constrained CMA polarization demultiplexer to realistic imperfections of polarization-diversity coherent optical receivers. The PMD and PDL tolerance of the proposed demultiplexer can be used as a benchmark in order to compare the performance of more sophisticated adaptive electronic PMD/PDL equalizers.** 

_**Index Terms—**_ **Coherent communications, polarization demultiplexing, constant modulus algorithm.** 

Manuscript received January 30, 2009; revised May 27, 2009, July 12, 2009. First published November 03, 2009; current version published March 12, 2010. This work was supported in part by the European Social Fund and in part by the Greek Ministry of Development-GSRT. 

I. Roudas, A. Vgenis, C. S. Petrou, and D. Toumpakaris are with the Department of Electrical and Computer Engineering, University of Patras, Rio 26500, Greece (e-mail: roudas@ece.upatras.gr; vgenis@ece.upatras.gr; petrou@ece.upatras.gr; dtouba@ece.upatras.gr). 

J. Hurley, M. Sauer, J. Downie, Y. Mauro, and S. Raghavan are with Corning Inc., Corning, NY 14831 USA (e-mail: RaghavanS@corning.com). Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org. Digital Object Identifier 10.1109/JLT.2009.2035526 

## I. INTRODUCTION 

**R** ECENT progress in fast data acquisition, in combinationwith the decreasing cost of high-speed digital electronics, is currently rendering the digital implementation of coherent optical receiver functionalities commercially viable at symbol rates equal to 10 GBd and beyond [1]. A growing number of research papers focuses on the evaluation of the performance of digital signal processing (DSP) algorithms, which can successfully counteract various transmission impairments that typically affect the performance of coherent optical receivers (see tutorials [2], [3], and references therein). 

Among all transmission impairments, it would be difficult to overstate the importance of the impact of polarization effects on the performance of coherent optical receivers. For instance, random polarization rotations, caused by the birefringence of optical fibers, can be detrimental, since the states of polarization (SOPs) of the received optical signal and the local oscillator are not identical, as required. Polarization diversity [2], [3] is a practical means to detect all signal power, independent of the received SOP, by using a coherent optical receiver with two identical branches, one for the - and one for the -polarization component, respectively. The photocurrents at the output of the receiver branches must be appropriately combined using a two-input/one-output adaptive filter (electronic _polarization combiner_ ) [3], in order to retrieve all the information carried by the received signal. 

The increased complexity and cost of polarization-diversity coherent optical receivers can be better justified when simultaneous polarization division multiplexing (PDM) is used at the transmitter, in order to double the spectral efficiency of the optical communications system. In this case, the electronic polarization combiner, used in the single-channel case, is replaced by a two-input/two-output adaptive filter, which separates the PDM channels into their respective outputs (electronic _polarization demultiplexer_ ) [4]–[12]. In addition, by increasing the number of adaptive filter coefficients, the polarization demultiplexer can also perform equalization of the intersymbol interference caused by polarization mode dispersion (PMD), polarization dependent loss (PDL), residual chromatic dispersion and other effects [13]–[17]. 

There is no unanimous agreement in the optical communications community regarding the merit of different DSP algorithms for electronic polarization demultiplexing and equalization. For example, depending on their operating mode, proposed algorithms can be distinguished into two categories: i) Data-aided (requiring a training sequence to achieve convergence, e.g., [8]); and ii) Blind, either decision-directed 

0733-8724/$26.00 © 2010 IEEE Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1122 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

(employing estimates of the received symbols for adaptation, e.g., [13]) or based on other attributes of the received optical signal, which are affected by intersymbol interference, without attempting to recover the data. In the latter category, the constant modulus algorithm (CMA) [18]–[21] has been proposed for blind adaptive feed-forward polarization demultiplexers [10], [11] and equalizers [15]. The popularity of these CMA-based modules [22]–[24] is due to their low computational complexity and their robustness in the presence of intermediate frequency (IF) offsets and laser phase noise. The second feature allows for decoupling between polarization demultiplexing and carrier frequency/phase recovery, so the latter two impairments can be addressed by separate DSP modules. A disadvantage of CMA-based modules is their possible erroneous convergence to the same PDM channel [11], [12]. 

This article focuses on the issue of optimal polarization demultiplexing exclusively, in the absence of PMD. The purpose of the present study is the optimal design, using the maximumlikelihood criterion [25]–[27], of polarization-diversity coherent optical receivers, for the detection of polarization-multiplexed optical signals with orthogonal, albeit unknown, SOPs. In the absence of laser phase noise and IF offset, it is shown that simultaneous joint estimation of the symbols, over the two received orthogonal SOPs, yields optimal performance. In contrast, the commonly used zero-forcing polarization demultiplexer usually yields sub-optimal performance [26], [27]. The latter first employs an electronic polarization demultiplexer, in order to fully invert the Jones matrix of the optical fiber, followed by individual demodulation of the polarization-multiplexed tributaries. Jones matrix inversion can be achieved using a lattice adaptive filter with four complex taps [4]–[12]. Similar to [4], [11] we introduce constraints between the taps, in order to avoid convergence into the same PDM channel. The constraints take advantage of the fact that polarization rotations in optical fibers can be represented by unitary transformations. Then, the transfer matrix of the adaptive filter, in the absence of PMD and PDL, is expressed as a function of only two independent real parameters. These parameters can be estimated using either dataaided or blind channel estimation techniques. For their estimation, we use the CMA. We evaluate, by simulation, the performance of the proposed constrained CMA polarization demultiplexer in coherent optical communication systems using PDM quadrature phase shift keying (QPSK) signals. We show that it is, by far, superior, in terms of convergence accuracy and speed, compared to previously proposed, conventional CMAbased polarization demultiplexers [10]. A salient feature of the proposed constrained CMA polarization demultiplexer is that convergence is always guaranteed. Finally, we experimentally test the tolerance of the proposed constrained CMA polarization demultiplexer to realistic imperfections of polarization-diversity coherent optical receivers. 

Despite its apparent simplicity, the proposed constrained CMA electronic demultiplexer, can be used as a benchmark in order to compare the performance of more sophisticated adaptive electronic equalizers in the presence of PMD and PDL. Since it does not possess any PMD/PDL compensation capabilities, it can be used as a reference for the PMD and PDL tolerance of uncompensated coherent optical systems. 

It is worth mentioning at this point that our polarization demultiplexer is almost identical to the one proposed by Kikuchi in a recent paper [11]. The latter came to our attention only after the submission of our manuscript to the Journal of Lightwave Technology, by one of the reviewers. Despite their similarities, the two papers approach the issue of polarization demultiplexing from different angles. Kikuchi’s main goal was to elucidate the physics behind the operation of the CMA-based polarization demultiplexers. In contrast, in our paper, we first derive the optimal polarization demultiplexer’s structure, based on the maximum-likelihood criterion. Then, we prove that the performance of a zero-forcing polarization demultiplexer, in the absence of PMD and PDL, is optimal. Finally, we express the transfer matrix of the zero-forcing polarization demultiplexer, in the absence of PMD and PDL, as a function of only two real parameters (as opposed to two complex parameters in [11]), which are subsequently computed recursively using the CMA. 

The rest of this paper is divided into three major sections, namely, theoretical model (Section II), simulation results and discussion (Section III), and experimental validation (Section IV). In Section II, we develop an equivalent, discrete-time model of a representative coherent optical communications system, using matrix formulation. Then, we apply the maximum-likelihood criterion, in order to derive an optimal decision metric for the joint estimation of the symbols, over both received SOPs. Based on the optimal decision metric, it is shown that, under certain ideal conditions, a zero-forcing linear receiver yields optimal performance. The final part of Section II is devoted to the proposed constrained polarization demultiplexer and the application of CMA for the blind adaptive estimation of its adjustable parameters. In Section III, we evaluate, by simulation, the performance of the proposed constrained CMA polarization demultiplexer, in terms of convergence properties and error probability. Finally, in Section IV, we experimentally test the capability of the proposed constrained CMA polarization demultiplexer in separating 2 GBd PDM QPSK optical signals. The details of the theoretical calculations are presented in the Appendices. 

## II. THEORETICAL MODEL 

## _A. System Description_ 

Fig. 1 shows the block diagram of a PDM QPSK optical communications system with a polarization- and phase-diversity coherent optical receiver. The modules of the optical transmitter are shown in detail in Fig. 1(a). The optical signal from a CW semiconductor laser diode (SLD) is equally split and fed into two parallel quadrature modulators (QM). Two independent pseudo-random bit sequences (PRBS), at a bit rate 

each, are differentially encoded (DE) and transformed into pulse sequences, which, in turn, change the driving voltage of each QM. Two optical, differentially-encoded QPSK signals are generated, at a symbol rate each, at the output of the QMs. The two optical QPSK signals are superimposed with orthogonal SOPs, using two polarization controllers (PC) and 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

1123 

**==> picture [502 x 260] intentionally omitted <==**

Fig. 1. Block diagram of a representative coherent optical system. (a) PDM QPSK transmitter (Symbols: PRBS: Pseudo-random bit sequence, DE: Differential encoding and pulse shaping, SLD: Semiconductor laser diode, CPL: 3-dB coupler, QM: Quadrature modulator, PC: Polarization controller, PBC: Polarization beam combiner.); (b) Polarization- and phase-diversity coherent optical receiver (Symbols: OA: Optical preamplifier, BPF: Optical bandpass filter, PBS: Polarization beam splitter, LO: Local oscillator, BPD: Balanced photodetectors, LPF: Lowpass filter, ADC: Analog-to-digital converter, ASIC: application specific integrated circuit.); (c) ASIC architecture (Symbols: QI comp.: Quadrature imbalance estimation and compensation, Pol. DMUX: Polarization demultiplexer, DD: Differeny tial decoding, Demod.: Demodulation, BER: Bit error rate counter.); (d) Proposed constrained polarization demultiplexer (Symbols: (n) : output photocurrents, w ; k; l = 1; 2 : Complex taps, f^(n); ^"(n)g : Estimated azimuth and ellipticity). x (n) : input photocurrents, 

a polarization beam combiner (PBC), to form a PDM QPSK signal, which is transmitted through an optical fiber. 

The block diagram of an optical polarization- and phase-diversity digital coherent homodyne synchronous receiver is shown in Fig. 1(b). The optical receiver front-end is composed of an optical preamplifier (OA), an optical bandpass filter (BPF), a laser diode, acting as a local oscillator (LO), two polarization beam splitters (PBSs) with aligned principal axes, two 2 4 90 optical hybrids, and four balanced photodetectors (BPDs). The received optical signal is optically preamplified and filtered by the optical BPF, in order to reject the out-of-band amplified spontaneous emission (ASE) noise. The - and -polarization components of the received optical signal and the local oscillator are separately combined and detected by two identical phase-diversity receivers composed of a 2 4 90 optical hybrid and two BPDs each, at the upper and lower polarization branches, respectively. The photocurrents at the output of the four balanced detectors are low-pass filtered (LPF), sampled at integer multiples of the symbol period , using an analog-to-digital converter (ADC), and fed to an application specific integrated circuit (ASIC) for DSP. 

Fig. 1(c) shows the ASIC’s architecture. The four sampled photocurrents are processed in pairs. Each pair corresponds to the in-phase and quadrature components of the coherent beating between the received signal and the signal of the LO. Initially, the quadrature imbalance (QI) occurring at each phase-diversity receiver is estimated and corrected [28]–[31]. The two 

quadratures are then combined, via complex addition, to form discrete-time, scaled replicas of the received complex electric field vectors at the - and -polarizations, respectively. Subsequently, polarization demultiplexing is performed [4]–[12], possibly combined with transmission impairments equalization [13]–[17]. The block diagram of the proposed constrained CMA polarization demultiplexer is shown in Fig. 1(d). The polarization demultiplexer attempts to counteract the channel effect by forming a linear superposition of the photocurrents. It has two inputs and two outputs and is composed of four complex multipliers which are connected in a butterfly structure. The multipliers are iteratively adjusted, using the CMA. The rationale behind the structure of the proposed polarization demultiplexer is explained in detail in Section II-C. 

Referring back to Fig. 1(c), after polarization demultiplexing, the complex envelopes of the electric fields of the PDM QPSK tributaries are recovered separately, at the upper and lower branches of the ASIC. The non-zero IF offset, due to the carrier frequency difference between the transmitter and the local oscillator lasers, is estimated and removed, using a feed-forward carrier recovery algorithm [32], [33]. A feed-forward phase noise removal circuit estimates and removes laser phase noise, e.g., [34]. Subsequently, the two waveforms are demodulated independently. Each symbol sequence is recovered using a decision circuit, is differentially decoded and transformed into two bit sequences, which are used for error counting. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1124 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

## _B. Mathematical Formulation_ 

In this subsection, an equivalent, discrete-time model of the coherent optical system of Fig. 1 is derived. 

For mathematical convenience, an equivalent baseband representation [25] of the optical signals and components is used. In addition, the following notations are adopted: (i) To distinguish vectors from scalars, we identify vector quantities with boldface type; (ii) Matrices are also denoted by boldface type (the distinction should be clear from the context); and (iii) Dirac’s bra and ket vectors denote normalized Jones vectors [35]. 

It is assumed that the electric fields of the two QPSK modulated waveforms, at the output of the QM, have orthogonal polarizations and , respectively. It is also assumed that the optical fiber induces arbitrary, random, time-varying polarization rotations but maintains the orthogonality between the SOPs of the polarization multiplexed signals. After transmission through the optical fiber, at the output of the optical BPF, the electric field of the optical PDM QPSK signal can be written, in equivalent baseband notation, as 

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

where are the complex envelopes of the preamplified optical signals contaminated with ASE noise, and are the corresponding slowly-varying, normalized, Jones vectors along two arbitrary orthogonal SOPs, denoted by . Based on the assumption of SOP orthogonality, the inner product of the two Jones vectors must vanish, i.e., where is Kronecker’s delta. The complex envelopes of the electric fields in (1) can be written as 

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [12 x 9] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where are the average optical powers at each SOP, are the modulating signals, is the angular frequency offset from the channel’s nominal frequency, and is the phase noise of the received signal. The terms represent independent, identically distributed, complex ASE noise components in the two orthogonal SOPs, which follow Gaussian distribution with zero mean and variance . 

. The normalized Jones vectors can be expressed in rectangular coordinates as [36] 

**==> picture [4 x 24] intentionally omitted <==**

**==> picture [5 x 24] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

and 

**==> picture [4 x 24] intentionally omitted <==**

**==> picture [4 x 24] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [12 x 9] intentionally omitted <==**

where and are the angles corresponding to the s-SOP’s azimuth and ellipticity [36], respectively, and take values in the intervals [36]. 

In Appendix A, it is shown that an array of two complex photocurrents is generated at the output of the polarization- 

and phase-diversity coherent optical receiver, which, in the absence of phase noise, can be written as 

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where is the array of the two sampled modulating signals scaled by a multiplication factor, is the array of the total photocurrent noises, and is the transfer function of the transmission channel 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

The mean and covariance matrices of the sampled modulating signals are 

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

and 

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

respectively, where denotes expectation, denotes a diagonal matrix, dagger denotes the adjoint, i.e., conjugate transpose, matrix, and are the signal amplitudes at each receiver branch. 

The mean and covariance matrices of the total photocurrent noises are given by 

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

and 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

respectively, where are the variances of the photocurrent noise components at each receiver branch. 

It is straightforward to verify that belongs to the special unitary group SU(2), i.e., where denotes the 2 2 unit matrix, and where the operator denotes the determinant of a matrix. 

## _C. Optimal Receiver_ 

In Appendix B, using the maximum-likelihood criterion [25]–[27], we derive the decision metric of the optimal receiver for joint detection of PDM QPSK signals transmitted over the memoryless, discrete-time, two-input two-output (TITO) linear channel described by (5). 

It is shown that a sufficient statistic for estimating the transmitted symbols is the following (see (57) in Appendix B) 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

where denotes real part and is the joint, complex-symbol alphabet. We have dropped the time dependence of all matrices in order to avoid clutter. 

From (11), we observe that, prior to decision, the optimal receiver must form a linear superposition of the complex photocurrents 

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [12 x 8] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

(12) 

1125 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

where is the transfer matrix of a spatial electronic filter 

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [13 x 8] intentionally omitted <==**

Substitution of (12) into (11) leads to the concise decision rule 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [10 x 7] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

We conclude that, in the general case, when the total photocurrent noise is not spatially white, i.e., , the optimal receiver should perform the following steps: (i) spatial noise pre-whitening, i.e., multiplication by (ii) projection to 

and (iii) joint maximum-likelihood vector symbol estimation using the concise metric (14). This receiver is called the linear minimum mean squared error (MMSE) receiver [27]. 

## _D. Zero-Forcing Receiver_ 

In the special case when the noises at the two branches of the polarization diversity receiver have the same variance (i.e., the photocurrent noise is spatially white), the optimal receiver may use the simplified decision rule (see (61) in Appendix B) 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where the spatial electronic filter transfer matrix is now reduced to 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [12 x 8] intentionally omitted <==**

The above relationship indicates that the optimal receiver must use an electronic polarization demultiplexer, in order to fully invert the fiber Jones matrix. 

It would be instructive to gain some insight into why (16) is optimal. Assume that the receiver has perfect knowledge of the channel transfer matrix. According to (16), the receiver should set . Then, the output of the polarization demultiplexer is written as 

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

Since the multiplication with a matrix is a linear operation, the resulting noise is a complex Gaussian random vector. Using (9) and (10), for , we can calculate the mean and covariance matrices of 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

maximum likelihood detection, since the noises at the output branches of the polarization demultiplexer would be correlated (19) [27]. 

As shown in Appendix B, the decision rule (15) can be further reduced so that each element of can be individually estimated at each branch of the polarization-diversity receiver. Furthermore, the in-phase and quadrature components of are independently retrieved, by comparison to a zero threshold. 

Polarization demultiplexing, followed by separate detection of the two PDM channels, is a special case of a well-known receiver structure in the context of multiuser systems with space diversity, called _zero-forcing linear receiver, interference nuller_ , or _decorrelator_ [27]. It is worth noting that the proposed receiver is a direct extension to two dimensions of the maximal ratio combiner, used in single channel communications systems, with polarization-diversity coherent receivers [3]. In addition, the proposed polarization demultiplexer transfer matrix is the exact 2 2 equivalent of the matched filter transfer function [27], [11]. 

## _E. Estimation of Channel Transfer Matrix_ 

The zero-forcing receiver must calculate an estimate of the channel transfer matrix in (5) and set . From (3)–(4) and (6), we observe that the elements of are functions of only two independent parameters and . Therefore, one simply needs to calculate the estimates of the angles . Below, we show that this can be achieved blindly using the CMA. Its application on optical channel parameters estimation is a novel idea. Its adequacy, compared to other estimators [37], lies out of the scope of the present study. No claims about its optimality are made. Its adoption, as an appropriate scheme for the estimation of and can be justified by its tolerance to intermediate frequency offsets and laser phase noise, and its excellent bit error rate (BER) performance shown in Fig. 5(c). 

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

where the operator denotes the Hadamard matrix product [39], defined as the component-wise multiplication of two matrices 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

and 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [5 x 25] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

and 

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

We observe that the photocurrent noise statistics are preserved after the proposed polarization demultiplexer. This indicates that polarization demultiplexing can be achieved without penalty. However, were it not for the equality of the total photocurrent noise variances and the unitarity of the channel transfer matrix, the performance of the linear zero-forcing receiver would be suboptimal, compared to joint 

where are the total signal and noise powers at each branch of the polarization-diversity receiver. 

The cost function, which we seek to minimize, can be defined as the total mean-squared error 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

The instantaneous cost function can then be expressed in terms of as 

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1126 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

We define the auxiliary column vector with elements equal to the independent parameters 

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

Taking the derivative of the instantaneous cost function with respect to and using the chain rule, one finally obtains analytical expressions for 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [12 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [13 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

We define the gradient of the instantaneous cost function in the space of the independent variables 

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

The stochastic gradient algorithm for updating the adaptive filter coefficients is written [21], [25] 

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where is a positive real constant ( _step-size parameter_ ). Using periodic boundary conditions, the parameters and in (28) are confined within a unit cell, delimited by . 

It should be stressed that both the proposed constrained CMA polarization demultiplexer and its conventional counterpart suffer from output permutation and rotation ambiguities. The first type of ambiguity means that PDM channel ordering at the polarization demultiplexer outputs is unpredictable. The second type of ambiguity means that the recovered constellations might exhibit arbitrary rotations from their nominal position. In other words, both polarization demultiplexers cannot distinguish between the desired solution (in the absence of noise) 

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

and the undesired solution 

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

where , and are arbitrary phase rotations. The output permutation ambiguity can be addressed, for instance, by periodically transmitting channel identification training symbols (pilots) and by using a tracking scheme for their detection. 

The rotation ambiguity can be readily unraveled by the feedforward laser phase noise estimation circuit [34], which is assisted by differential coding and decoding of the transmitted symbols [3]. 

It is worth mentioning that a combination of data-aided and blind estimation of can be performed, as well. Since polarization rotations, due to fiber birefringence, are slow, in comparison with the symbol rate, they can be considered a quasi-static effect. Estimation of quasi-static effects can be performed in two 

**==> picture [247 x 183] intentionally omitted <==**

Fig. 2. Constellation diagrams for the x -polarization, at the output of the polarization diversity receiver, in the absence ((a), (b), (c)) and in the presence ((d), (e), (f)) of IF offset. (Conditions: Received SOP parameters: (a), (d) = " = 0 , (b), (e) = =3; " = 0 , and (c), (f) = " = =3 ). 

phases, i.e., training and tracking. During the training phase, a short training sequence, in conjunction with the least squares method [37], can be used to estimate . This method asymptotically yields the best linear unbiased estimate [37]. During the time intervals between transmitting consecutive training sequences, a blind estimation algorithm, e.g., [38], can be used for tracking and continuously updating the values of the adjustable parameters. The values provided by the training phase can be used as initial guesses for the recursion of the tracking algorithm. 

## III. SIMULATION RESULTS AND DISCUSSION 

In order to theoretically evaluate the performance of the proposed constrained CMA polarization demultiplexer and compare it with its conventional counterpart [10], we perform computer simulations of the coherent optical communication system shown in Fig. 1. We use ideal non-return-to-zero (NRZ) QPSK signals. The optical fiber is modeled simply as a polarization rotator with transfer matrix . The optical hybrids are considered ideal and all photodiodes are identical. All simulations are performed with initial guesses 

for the proposed constrained CMA polarization demultiplexer and for its conventional counterpart. Initially, the impact of polarization rotations on the constellation of received sampled complex photocurrents is investigated. We distinguish two cases, in the absence and in the presence of phase noise and IF offset, respectively. First, the ideal constellation is shown as a reference (Fig. 2(a), black (red) crosses). Due to cross-polarization interference, received constellations consist of 16 points, Fig. 2(b), (c). This occurs because the mixing matrix creates all possible combinations of two constellations of four points each. Depending on the specific values of , some of the constellation points may overlap. In the presence of IF offset, constellation points rotate either clockwise or counterclockwise, producing up to four concentric circles with unequal radii, as shown in Fig. 2(e)–(f). 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

1127 

**==> picture [247 x 85] intentionally omitted <==**

Fig.and ellipticity3. (a) Three-dimensional ;^ ^" . (Symbols: A,plot ofB: Globalthe costminima withinfunction vs. estimated azimuththe unit cell, Rectangle: Unit cell), (b) Corresponding contour plot of the cost function on the Poincaré sphere for the proposed constrained polarization demultiplexer. (Sym-bols: White (red) point (A): Minimum at ^ = "^ = =6 ). (Conditions: Received SOP parameters: = " = =6 ). (Color coding: Black (blue) areas: Small values of the cost function, White (red) areas: Large values of the cost function). 

We proceed with exploring the performance surface as a function of the proposed demultiplexer adjustable parameters. Fig. 3(a), (b) show three-dimensional and Poincaré sphere-contour plots, respectively, of the instantaneous cost function vs. , in the absence of noise, for . Time averaging of the cost function , over 500 consecutive symbols, is performed instead of ensemble averaging. In Fig. 3(a), we observe that, within the limits of the unit cell, denoted by a rectangle, there are two global minima . In Fig. 3(b), these minima correspond to two antipodal points on the Poincaré sphere. The minimum at the point (also denoted by a (white) red point on the Poincaré sphere), corresponds to the correct ordering of the output signals, whereas the other minimum at the point (not shown on the Poincaré sphere), results in a permutation of the output channels. Bisecting the line connecting the two minima on the Poincaré sphere with a perpendicular plane, divides the sphere into two hemispheres. The intersection of the plane, with the surface of the sphere, creates a rotated equator line, which corresponds to the ridge within the unit cell of Fig. 3(a). The hemisphere of each minimum in Fig. 3(b) corresponds to a valley within the unit cell of Fig. 3(a). The constrained CMA converges to the minimum lying in the same hemisphere as the initialization point . If the initial point lies exactly on the equator, in the presence of noise, the algorithm may converge to either minimum. 

Subsequently, we study the impact of ASE noise on the convergence behavior of the proposed constrained CMA polarization demultiplexer. We assume that the transmitted orthogonal SOPs are , corresponding to the Stokes vectors and , respectively. We also assume that the received SOPs have been rotated due to fiber birefrigence in relation to the transmitted ones, such that the s-SOP angles are . The polarization demultiplexer iteratively estimates the angles and restores the SOPs of the PDM QPSK signals back to their initial values. Fig. 4(a) shows the trajectories followed on the Poincaré sphere during restoration from to , both in the absence (black (unmarked) line) and in the presence of ASE noise (for two different values of the optical signal-to-noise ration (OSNR)). We observe that, in the absence of ASE noise, the restored SOP eventually 

**==> picture [247 x 126] intentionally omitted <==**

Fig. 4. (a) Trajectory of the estimated SOP at the output of the proposed constrained polarization demultiplexer. (Conditions: Received SOP parameters: = " = =6 , BPF bandwidth= 32R , LPF 3-dB bandwidth: B = 0:8R , LPF equivalent noise bandwidth: B = 1:04B , phase averaging block size = 10 symbols), (Symbols: Black (unmarked) line: Absence of noise, Red line (open circles): OSNR = 9 dB and, Blue line (crosses): OSNR = 7 dB) (b) Time evolution of the MSE for the x polarization for the proposed constrained (dotted line), and the conventional CMA-based (solid line), polarization demultiplexers, for the optimum step size = 0:1 . Averaging over 500 experiments is performed. (Conditions: Received SOP parameters: =4 and " = 0 ). 

**==> picture [239 x 98] intentionally omitted <==**

Fig. 5. Representative constellations of the received (blue (gray) points), equalized (red (black) points) and ideal ((green) crosses) signals for the x polarization, using (a) the proposed constrained polarization demultiplexer, and (b) the conventional CMA-based polarization demultiplexer; (c) BER vs. OSNR for the ideal (i.e., distortionless) case (blue (thick black) curve), and using the proposed constrained ((red) triangles), and the conventional CMA-based ((black) circles), polarization demultiplexer. Quadratic polynomial fitting is used, drawn as a dotted line (in red) for the proposed constrained and as a thin solid line (in black) for the conventional CMA-based polarization demultiplexer. (Conditions: Received SOP parameters: = =6 and " = =12 , BPF bandwidth = 32R , LPF 3-dB bandwidth: B = 0:8R , 4th-order Bessel LPF equivalent noise bandwidth: B = 1:04B , phase averaging block size = 10 symbols). 

coincides with the transmitted one, whereas, as the OSNR is reduced, the restored SOP fluctuates more significantly around the initially transmitted SOP. 

In Fig. 4(b), we compare the decay time of the error magnitude for the proposed constrained CMA polarization demultiplexer (dotted line), and the conventional one (solid line) [10]. More specifically, for both demultiplexer types, we plot the time evolution of the mean-squared error , for the -polarization, for the optimal value of the step-size parameter . We choose a maximal initial perturbation; that is to say, the initial point is selected adjacent to the rotated equator and within the appropriate hemisphere, in order to prevent output reversal. Ensemble averaging over 500 simulation runs is performed. The optimum step-size parameter is for both polarization and demultiplexers, providing fast convergence and negligible residual mean squared error (MSE). The constrained CMA polarization demultiplexer clearly exhibits 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1128 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

**==> picture [502 x 201] intentionally omitted <==**

Fig. 6. (a) Block diagram of the experimental setup (Symbols: ECL: External cavity laser, QM: Quadrature modulator, CPL: 3-dB coupler, PC: Polarization controller, PRBS: Pseudo-random binary sequence, RF Amp: Radio frequency amplifier, OF: Optical fiber, PBC: Polarization beam combiner, VOA: Variable optical attenuator, OA: Optical amplifier, Rx: Polarization- and phase-diversity coherent optical receiver, BPD: Balanced photodetector, DSO: Digital storage oscilloscope.); (b) Block diagram of the DSP modules used to analyze the experimental results. (Symbols: Sync. & Resampling: Quadrature and polarization time synchronization and resampling, SE dist: Single-ended distortion mitigation, FFFE: Feed-forward frequency estimation and removal, FFPE: Feed-forward phase estimation and removal, BER: Bit error rate tester.). 

superior performance, in terms of convergence speed. For example, for , the constrained CMA polarization demultiplexer requires less than 20 symbol intervals to minimize the MSE, whereas its conventional counterpart [10] requires more than 60 symbol intervals, i.e., it is more than three times slower. 

PRBSs. The optical signal at the output of the QM is split into two equal amplitude components, using a 3-dB coupler. One of the two components is delayed using approximately 8 m of optical fiber. Their SOPs are adjusted, using two PCs, so that they become aligned with the principal axes of the PBC. The PDM QPSK signal, at the output of the PBC, is amplified using a booster optical amplifier (OA1) and is subsequently transmitted through 100 km of LEAF[®] optical fiber. The latter, at 2 GBd, simply acts as a polarization rotator and attenuator. The received optical signal is preamplified and filtered in two stages, using two tunable fiber Bragg grating (FBG) filters. The first FBG filter has 0.6 nm bandwidth, in order to emulate a WDM DMUX. The second FBG filter has 0.25 nm bandwidth, in order to emulate the ASE noise-limiting filter, typically used after the optical preamplifier. As the optical field reaches the polarization- and phase-diversity coherent optical receiver, it is split using a PBS. The two polarization components are combined with the light of an ECL, acting as a LO. Local-oscillator-to-signal power ratio (LOSPR) was kept small due to limitations of the lasers used at the experiment. Two different optical hybrid technologies were used, namely, a bulk-component, 2 2 90 optical hybrid [40], and a commercially-available, integrated 2 4 90 optical hybrid [6]. At the output of the 2 2 90 optical hybrid, two, almost identical, 10-GHz bandwidth PDs are used. The integrated 2 4 90 optical hybrid is followed by two pairs of 40-GHz bandwidth BPDs. Finally, an 8-GHz electrical bandwidth, 40 GSa/s, real-time, sampling oscilloscope samples the photocurrents and stores the signals for off-line processing. An electrical spectrum analyzer, not shown in Fig. 6(a), is used for the manual adjustment of the transmitter and LO frequencies within MHz from each other. The duration of a single measurement is equal to 51.25 s. 

Fig. 5(a), (b) show representative input/output constellation diagrams, with ASE noise and zero IF offset, obtained by using the constrained CMA polarization demultiplexer and the conventional one, respectively. We assume that the received SOPs correspond to . We see that both polarization demultiplexers are able to transform the received spiral constellation (blue (gray) points) into four approximately circular points (in red (black)) that approach the transmitted constellation (green crosses). 

Fig. 5(c) shows BER curves, as a function of the OSNR, measured in a resolution bandwidth , (e.g., OSNR measured in 0.1 nm resolution bandwidth for GBd) for both polarization demultiplexers. The BER is calculated using Monte Carlo simulation. The red triangles correspond to the proposed constrained CMA polarization demultiplexer, the black circles correspond to the conventional CMA polarization demultiplexer, and the blue (thick black) curve corresponds to the ideal case, with no polarization rotations [2], [3]. Obviously, both polarization demultiplexers exhibit almost identical performance, with a negligible penalty relative to the ideal case at high OSNRs. 

## IV. EXPERIMENTAL VALIDATION 

In order to test the validity of the simplifying assumptions of the theoretical model presented in Section II, we performed a series of PDM QPSK experiments. The experimental set-up is shown in Fig. 6(a). 

Fig. 6(b) shows the block diagram of the DSP modules used to analyze the experimental results. First, we filter the translated spectrum using an LPF, in order to remove out-of-band noise. 

Light from an external cavity laser (ECL), acting as a transto analyze the experimental results. First, we filter the translated mitter, is QPSK modulated using a QM, driven by two 2 Gb/s spectrum using an LPF, in order to remove out-of-band noise. Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

1129 

Timing recovery is manually performed, in order to remove any differential delays between the signals, which are caused by optical and electrical path differences. Subsequently, signals are resampled to one sample per symbol. 

Distortion due to small LOSPR and single-ended detection at the 2 2 90 optical hybrid is first partly removed [41]. Inaccuracies in the bias voltages of the 2 4 90 optical hybrid, as well as non-optimal setting of the four PCs within the 2 2 90 optical hybrid, in conjunction with differences in the responsivity of the PDs, cause QI [29]. QI is a slowly varying impairment, essentially constant over the duration of a single measurement. Several methods have been proposed for QI estimation and compensation, both in optical communications [28]–[31], and in digital communications, e.g., [42]. Here we use the algorithm described in [29], [31]. After QI compensation, the PDM QPSK signals are fed into the proposed electronic polarization demultiplexer. After polarization demultiplexing, any residual IF is estimated and removed using a feed-forward frequency estimation algorithm [32], [33]. A feed-forward phase noise removal circuit estimates and removes laser phase noise [34]. Finally, the signal corresponding to each quadrature passes through a decision circuit. The symbol sequence for each PDM QPSK signal is recovered and is differentially decoded. Then, it is transformed into two bit sequences, which are compared to the transmitted ones in order to perform error counting. 

It is important to note that all DSP algorithms based on the assumption of the envelope constancy of QPSK signals, (i.e., [32]–[34]), cannot be applied prior to polarization demultiplexing. Otherwise, symbol errors occur due to the presence of multiple signal levels, caused by cross-polarization interference, as shown in Fig. 2. Therefore, residual IF estimation and phase noise estimation should be performed only _after_ the proposed constrained CMA polarization demultiplexer. The latter is insensitive to IF offset and laser phase noise, so their presence does not affect the correct estimation of the fiber transfer matrix parameters . 

Fig. 7 shows typical constellations for the -polarization (upper row) and -polarization (lower row), respectively, immediately after synchronization and downsampling (Fig. 7(a), (b)), at the input of the proposed polarization demultiplexer (Fig. 7(c), (d)), at the output of the proposed polarization demultiplexer (Fig. 7(e), (f)), and after the IF and phase noise removing circuits (Fig. 7(g), (h)). The scale of constellations (a)–(d) is different from the scale of constellations (e)–(g) because the samples are normalized to unit magnitude at the input of the polarization demultiplexer. The initial constellations shown in Fig. 7(a), (b) contain QI, as witnessed by their elliptical shape. The constellation of Fig. 7(a), corresponding to the 2 2 90 optical hybrid, has the form of eccentric ellipses, a shape due to the distortion introduced by single-ended detection, combined with small LOSPR. The QI compensated constellations of Fig. 7(c), (d), resemble the ones plotted in Fig. 7(e), (f). Concentric circles with unequal radii are a tell-tale sign of cross-polarization interference between the two PDM QPSK signals. Due to the presence of ASE noise, circles are transformed into thick rings, whose circumferences may overlap. The constellations at the output of the polarization demultiplexer, seen in Fig. 7(e), (f), are single circles, indicating that fiber transfer matrix inversion was successfully performed. The difference in sizes between the 

**==> picture [247 x 128] intentionally omitted <==**

Fig. 7. Typical constellation diagrams in the x polarization (upper row) and the y polarization (lower row). (a), (b) after synchronization and downsampling; (c), (d) after QI compensation; (e), (f) at the output of the proposed polarization demultiplexer; (g), (h) after the IF and phase noise removing circuits. (Conditions: R = 2 GBd). 

final - and -polarization constellations is primarily attributed to _polarization imbalance_ (not to be confused with QI) due to gain and phase differences between the two branches of the polarization-diversity receiver (see analysis in Appendix C). In addition, the two polarization tributaries that are combined at the PBC, may have slightly unequal average powers due to maladjustment of the PCs or the non-ideal power splitting ratio of the 3-dB coupler. Fig. 7(g), (h) show the final constellations. The impact of polarization imbalance is obvious since the recovered constellations have unequal radii. No errors occur during a single measurement (i.e., 100 000 symbols) in both branches of the polarization diversity receiver. 

Fig. 8(a) illustrates the time evolution of the estimates of the azimuth and ellipticity . A variable step-size is used. In order to bring the operating point near the optimum quickly we start with a relatively large value of . The value of is halved after 100 symbols and again after another 200 symbols, to avoid large baseline wander. We can see that while the ellipticity angle approaches its final value after fewer than 100 symbols, the azimuth requires around 200 symbols to do the same. The azimuth and ellipticity remain stable over the rest of the measurement, confirming that polarization rotations are a slowly varying effect. Fig. 8(b) shows the time evolution of the instantaneous squared error function for the -polarization , for both the proposed constrained CMA polarization demultiplexer and the conventional one. Curves have been smoothed by moving averaging for illustration purposes. The theoretically observed three-fold increase in convergence speed is hereby qualitatively confirmed, although the absolute time scales are different compared to Fig. 4(b). 

## V. SUMMARY 

This article addressed the optimal design, using the maximum-likelihood criterion, of polarization-diversity coherent optical receivers, for the detection of orthogonal polarization-multiplexed optical signals in the absence of PMD and PDL. It was shown that a zero-forcing linear receiver, performing polarization demultiplexing and individual demodulation of the demultiplexed tributaries, yields, under certain conditions, optimal performance. We showed that polarization demultiplexing can be performed using a lattice adaptive filter with four complex, mutually-dependent taps in the absence of PMD and PDL. The taps can be expressed as a function of 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1130 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

only two, independently-controlled real parameters. For their estimation, we used the CMA. We studied, by simulation, the performance of the proposed polarization demultiplexer in coherent optical communication systems, using PDM QPSK signals. We showed that it was, by far, superior, in terms of convergence speed, compared to a conventional, CMA-based polarization demultiplexer [10]. Apart from this difference, both polarization demultiplexers exhibited almost identical performance. Nevertheless, a salient feature of the proposed constrained CMA polarization demultiplexer is that it always achieves convergence, unlike its conventional counterpart, which occasionally gets caught in singularities. Both the proposed constrained CMA polarization demultiplexer and the conventional one suffer from output permutation and rotation ambiguities, but these problems can be remedied by other DSP techniques. Finally, we experimentally tested the tolerance of the proposed constrained CMA polarization demultiplexer to realistic imperfections of polarization-diversity coherent optical receivers. 

**==> picture [52 x 8] intentionally omitted <==**

In this Appendix, we model the polarization- and phase-diversity coherent receiver and derive the matrix equation (5). Our analysis is similar to the one by [2], [3] and is reported here for completeness. Relationship (1) is used as a starting point. 

The polarization-diversity coherent optical receiver splits the received complex electric field vector into its - and -polarization components and using a PBS with principal axes 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

The SOP at the output of the LO is assumed to be linear 45 . After a PBS with principal axes , at the input of each hybrid, the electric field of the LO can be written, in equivalent baseband notation, as 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 11] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

where and is the complex envelope of the local oscillator given by 

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

In (33), is the average optical power of the local oscillator, is the local oscillator’s angular frequency offset from the channel’s nominal frequency, and is the phase noise of the local oscillator. 

At the four outputs of an ideal, lossless, polarization-independent, 90 optical hybrid, we obtain (omitting the time dependence, for brevity) [43] 

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

where . In (35), are the responsivities of the photodiodes and the dagger denotes the adjoint, i.e., conjugate transpose, matrix. 

By substitution of (34) into (35), we obtain 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

where and denote the real and imaginary parts, respectively. 

In the case of identical photodiodes with responsivity equal to at the outputs of the balanced receivers, we obtain 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

where . 

After sampling at integer multiples of the symbol period , we can form the discrete-time complex photocurrents via complex addition 

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

where . 

By substitution of (31) and (32) into (38), we obtain 

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [9 x 11] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

where and the superscript denotes complex conjugation. 

We can define the column-vectors of the photocurrents , the modulating signals and the total photocurrent noise as (40) 

where include the contribution of ASE, shot, and thermal noises, and the superscript T denotes transposition. 

From (2), (39), we observe that the fiber-induced polarization rotation and the optoelectronic conversion, at the polarizationand phase-diversity coherent optical receiver, can be described as a matrix equation 

where . 

Neglecting, for the moment, the contribution of shot and thermal noises, which will be taken into account later on, the photocurrents, at the output of the photodiodes, are given by 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where is a multiplicative factor 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [11 x 13] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [10 x 11] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

1131 

**==> picture [217 x 237] intentionally omitted <==**

Fig. 8. (a) Time evolution of the estimates of the s-SOP angles ^ and "^ computed by the proposed constrained polarization demultiplexer. For visualization purposes, we have removed the unit cell angle restrictions. (b) Time evolution of the squared error function for the x -polarization e (n); for the proposed polarization demultiplexer and the conventional CMA-based one. Curves are smoothed by two hundred-points moving averaging. (Symbols: Dotted lines: Initial convergence step = 0:05 , Solid lines: Initial convergence step = 0:5 ). 

respectively, where is the variance of the total photocurrent noise components at the two receiver branches. 

In the general case, when the modulating signal amplitudes and the noise variances at the two receiver branches are not identical, (41) can be rewritten, with some abuse of notation, as 

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

where we scale so that 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 9] intentionally omitted <==**

**==> picture [10 x 7] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

and 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

where denotes diagonal matrix, are the modulating signal amplitudes, and are the total photocurrent noise variances at the two branches of the polarization diversity receiver, respectively. 

## APPENDIX B 

This Appendix provides a detailed derivation of the optimal receiver for joint detection of PDM QPSK signals transmitted over a memoryless, discrete-time, two-input two-output (TITO) linear channel, based on the maximum-likelihood criterion [25]–[27]. 

As a starting point for the derivation, we use the matrix equation (48) 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

In the above, is the IF offset and is the total laser phase noise. 

**==> picture [6 x 5] intentionally omitted <==**

In (41), we also defined the transfer function of the transmission channel as a 2 2 matrix 

**==> picture [5 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

It is straightforward to verify that belongs to the special unitary group SU(2), i.e., and , where denotes the 2 2 unit matrix and the operator denotes the determinant of a matrix. 

For ideal NRZ QPSK modulation, the sampled modulating signals take equiprobable discrete complex values where . Consequently, the mean and covariance matrices of the modulating signals are 

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

and 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

respectively, where denotes expectation. 

From the properties of ASE, shot, and thermal noises, the mean and covariance matrices of the total photocurrent noise are given by 

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

and 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

The optimal maximum-likelihood receiver estimates the vector by maximizing the metric [26], 

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where is the conditional probability of the observed vector given that the transmitted vector was and is the joint, complex-symbol alphabet. We have dropped the time dependence of all matrices in order to avoid clutter. 

Using (51), the above relationship can be rewritten as 

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where is the joint probability density function (pdf) of the complex Gaussian random variables , with zero mean given by (46) and covariance matrix given by (50) [25], [26] 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [11 x 13] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

Since is a decreasing function of the argument of the exponential, the maximization in (53) is equivalent to minimizing the Euclidean distance 

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

Expanding the distance metric yields 

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

(56) 

1132 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

The first term is independent of and, can be ignored. Thus, a sufficient statistic for estimating the transmitted symbols is the following 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

In the special case when the noises at the two branches of the polarization diversity receiver have the same variance (i.e., the photocurrent noise is spatially white), the covariance matrix of the total photocurrent noise is given by (47). By substitution of (47) into (56), and taking into account that is unitary, the distance metric is simplified 

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

## APPENDIX C 

In this Appendix, we examine how the equivalent channel formalism can be modified, in order to accommodate PDL and polarization imbalance at the polarization-diversity receiver. It is shown that both effects result in a perturbation transfer matrix that creates additional cross-polarization interference. 

Consider a partial polarizer with eigenaxes in Jones space denoted by the vectors . The corresponding eigenaxes in Stokes space are denoted by . The transmittances associated with these eigenaxes are , respectively. Both the eigenaxes and the transmittances are independent of frequency. . 

The Jones matrix of the partial polarizer, in the absence of birefringence, is written as [44], [45] 

**==> picture [11 x 13] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [11 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

or, equivalently, 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

Using the expansion of the projection coefficient in Pauli spin matrices (relation [3.9] of [35]), the Jones matrix of the partial polarizer can be expressed in the alternative form 

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

Since only the first term of (59) depends on the candidate symbol vector the optimal receiver simply needs to minimize the metric 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [4 x 11] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

We observe that it is sufficient to estimate each element of individually, at each branch of the polarization-diversity receiver, using the metric 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

where is the complex symbol alphabet of each polarizationmultiplexed tributary. Furthermore, expanding the above relationship into its quadrature components, it follows that it is sufficient to choose the real and imaginary parts of each symbol independently at each branch of the phase-diversity receiver, in order to minimize the metric 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

To summarize, the above analysis indicates that the optimal receiver is reduced to a zero-forcing linear receiver [26], [27]. The latter first uses an electronic polarization demultiplexer with transfer matrix . Subsequently, the in-phase and quadrature components of the symbols, at the two outputs of the polarization demultiplexer, can be independently detected, by comparing each individual quadrature component to a zero threshold. 

In conclusion, the proposed constrained CMA polarization demultiplexer is optimal, when the photocurrent noise is spatially white. In this case, the joint maximum-likelihood receiver and the zero-forcing linear receiver are equivalent. 

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [11 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where is the 2 2 identity matrix, is the Pauli spin vector [35], and we defined the average amplitude attenuation coefficient and the differential amplitude attenuation coefficient as 

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [10 x 13] intentionally omitted <==**

**==> picture [11 x 13] intentionally omitted <==**

**==> picture [5 x 11] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

The electric field of the optical PDM QPSK signal at the input of the PDL is given by relationship (1). The electric field of the optical PDM QPSK signal at the output of the partial polarizer can be written, in the absence of noise, as 

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [11 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

Then (41) can be rewritten, in the absence of noise, as 

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where we defined the perturbation transfer matrix 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [17 x 9] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

As a sanity check, we observe that the second term of (69) becomes negligible for , i.e., when . 

The zero-forcing polarization demultiplexer must calculate an estimate of the total channel transfer matrix and set . The independent parameters of are the azimuth and the ellipticity of the input SOP , the azimuth and the ellipticity of the PDL eigenaxis , and the PDL parameters . 

In summary, the description of the perturbation matrix would require four additional control parameters. The total channel matrix requires six independent control parameters. Still, the current approach is advantageous compared to the CMA, which requires control of eight independent real parameters 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

ROUDAS _et al._ : OPTIMAL POLARIZATION DEMULTIPLEXING 

1133 

for polarization demultiplexing. Increasing the dimensionality of the independent parameter space will obviously slow down the search for the global optimum of the transfer function. On the other hand, conventional CMA-based demultiplexers are not only slow but also suffer from singularities. Their large number of independent parameters increases the number of degrees of freedom and the effects that can be accommodated, at the expense of execution speed and perhaps convergence altogether. 

It is instructive to estimate the impact of PDL and of polarization imbalance on the performance of the proposed constrained polarization demultiplexer, which possesses a unitary transfer matrix. Since the addition of two unitary matrices is not a unitary matrix, the total channel transfer matrix 

is not unitary. As a result, the product of the total channel transfer matrix with the unitary transfer matrix of the proposed constrained polarization demultiplexer is not a unit matrix. Consequently, the transmitted constellations cannot be not fully detangled. 

The output of the polarization demultiplexer can be written, in the absence of noise, as 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

where are the transfer matrices of the channel and the perturbation after polarization demultiplexing, which can be written 

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [12 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [10 x 7] intentionally omitted <==**

**==> picture [12 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

The action of the polarization demultiplexer is to rotate the principal axes of the receiver PBS in order to match the Jones vectors of the received polarization tributaries. It is straightforward to show that 

**==> picture [4 x 24] intentionally omitted <==**

**==> picture [4 x 24] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

and 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

where are estimates of the Jones vectors of the received polarization tributaries. 

Assuming that the presence of the perturbation transfer matrix does not drastically change the estimate of CMA, we can postulate that after convergence, . Since and [35], where is the Stokes vector of the s-SOP and are a right handed orthogonal set in Stokes space, 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [9 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 9] intentionally omitted <==**

**==> picture [9 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

where 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

The first term in (75) indicates that the polarization tributaries can be essentially recovered but they are distorted (i.e., the constellations have different size, differing by in radius). This distortion is an artifact induced by the assumption of the unitarity of the polarization demultiplexer’s transfer matrix. The second term in (75) indicates that there is a residual cross-polarization interference due to the anti-diagonal transfer matrix in (76). This interference term is relatively small since its magnitude depends on the differential amplitude attenuation . 

Finally, it is worth noting that the polarization imbalance at the polarization-diversity receiver is the electronic domain equivalent of using a partial polarizer in the optical domain. Its impact can be accounted for by substituting the polarizer’s transmission parameters with the photodiode responsivities and the polarizer eigenaxis in Stokes space by . 

## ACKNOWLEDGMENT 

The authors would like to thank Prof. G. Moustakides and Mr. V. U. Prabhu, Department of Electrical and Computer Engineering, University of Patras, Greece, for stimulating discussions on estimation theory, and the anonymous reviewers for their helpful comments and suggestions. 

## REFERENCES 

- [1] H. Sun, K.-T. Wu, and K. Roberts, “Real-time measurements of a 40 Gb/s coherent system,” _Opt. Exp._ , vol. 16, no. 2, pp. 873–879, Jan. 2008. 

- [2] E. Ip, A. P. T. Lau, D. J. F. Barros, and J. M. Kahn, “Coherent detection in optical fiber systems,” _Opt. Exp._ , vol. 16, no. 2, pp. 753–791, Jan. 2008. 

- [3] K. Kikuchi, “Coherent optical communication systems,” in _Optical Fiber Telecommunications_ , I. P. Kaminow, T. Li, and A. E. Willner, Eds. San Diego, CA: Academic, 2008, pp. 95–129, vol. VB, ch. 3. 

- [4] M. Tseytlin, O. Ritterbush, and A. Salamon, “Digital, endless polarization control for polarization multiplexed fiber-optic communications,” in _Proc. OFC 2003_ , Atlanta, GA, Mar. 2003, paper MF83. 

- [5] S. Calabro, T. Dullweber, E. Gottwald, N. Hecker-Denschlag, E. Mullner, B. Opitz, G. Sebald, E. Schmidt, B. Spinnler, C. Weiske, and H. Zech, “An electrical polarization-state controller and demultiplexer for polarization multiplexed optical signals,” in _Proc. 29th Eur. Conf. Optical Communication (ECOC)_ , Rimini, Italy, Sept. 2003, vol. 4, pp. 950–951. 

- [6] R. Noé, “Phase noise tolerant synchronous QPSK/BPSK basebandtype intradyne receiver concept with feedforward carrier recovery,” _J. Lightw. Technol._ , vol. 23, no. 2, pp. 802–808, Feb. 2005. 

- [7] R. Noé, “PLL-free synchronous QPSK polarization multiplex/diversity receiver concept with digital I & Q baseband processing,” _IEEE Photon. Technol. Lett._ , vol. 17, no. 4, pp. 887–889, Apr. 2005. 

- [8] Y. Han and G. Li, “Coherent optical communication using polarization multiple-input-multiple-output,” _Opt. Exp._ , vol. 13, no. 19, pp. 7527–7534, Sept. 2005. 

- [9] M. T. Core, “Cross polarization interference cancellation for fiber optic systems,” _J. Lightw. Technol._ , vol. 24, no. 1, pp. 305–312, Jan. 2006. 

- [10] A. Leven, N. Kaneda, and Y.-K. Chen, “A real-time CMA-based 10 Gb/s polarization demultiplexing coherent receiver implemented in an FPGA,” in _Proc. OFC/NFOEC 2008_ , Anaheim, CA, Feb. 2008, paper OTuO2. 

- [11] K. Kikuchi, “Polarization-demultiplexing algorithm in the digital coherent receiver,” in _Proc. IEEE LEOS Summer Topicals_ , Acapulco, Mexico, Jul. 2008, paper MC2.2. 

- [12] H. Zhang, Z. Tao, L. Liu, S. Oda, T. Hoshida, and J. C. Rasmussen, “Polarization demultiplexing based on independent component analysis in optical coherent receivers,” in _Proc. 34th Eur. Conf. Optical Communication (ECOC)_ , Brussels, Belgium, Sept. 2008, paper Mo.3.D.5. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 

1134 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 28, NO. 7, APRIL 1, 2010 

- [13] D. E. Crivelli, H. S. Carter, and M. R. Hueda, “Adaptive digital equalization in the presence of chromatic dispersion, PMD, and phase noise in coherent fiber optic systems,” in _Proc. IEEE Global Telecommun. Conf. (GLOBECOM)_ , Dallas, TX, Nov. 2004, vol. 4, pp. 2545–2551. 

- [14] E. Ip and J. M. Kahn, “Digital equalization of chromatic dispersion and polarization mode dispersion,” _J. Lightw. Technol._ , vol. 25, no. 8, pp. 2033–2043, Aug. 2007. 

- [15] S. J. Savory, “Digital filters for coherent optical receivers,” _Opt. Exp._ , vol. 16, no. 2, pp. 804–817, Jan. 2008. 

- [16] C. Laperle, B. Villeneuve, Z. Zhan, D. McGhan, H. Sun, and M. O’Sullivan, “WDM performance and PMD tolerance of a coherent 40 Gbit/s dual-polarization QPSK transceiver,” _J. Lightw. Technol._ , vol. 26, no. 1, pp. 168–175, Jan. 2008. 

- [17] C. R. S. Fludger, T. Duthel, D. van den Borne, C. Schulien, E. D. Schmidt, T. Wuth, J. Geyer, E. De Man, G. D. Khoe, and H. de Waardt, “Coherent equalization and POLMUX-RZ-DQPSK for robust 100-GE transmission,” _J. Lightw. Technol._ , vol. 26, no. 1, pp. 64–72, Jan. 2008. 

- [18] D. Godard, “Self-recovering equalization and carrier tracking in two dimensional data communication systems,” _IEEE Trans. Comm._ , vol. 28, no. 11, pp. 1867–1875, Nov. 1980. 

- [19] J. R. Treichler and M. G. Larimore, “New processing techniques based on the constant modulus adaptive algorithm,” _IEEE Trans. Acoust., Speech, Signal Process._ , vol. ASSP-33, no. 2, pp. 420–431, Apr. 1985. 

- [20] C. R. Johnson Jr., P. Schniter, T. J. Edres, J. D. Behm, D. R. Brown, and R. A. Casas, “Blind equalization using the constant modulus criterion: A review,” _Proc. IEEE_ , vol. 86, no. 10, pp. 1927–1950, Oct. 1998. 

- [21] S. Haykin _, Adaptive Filter Theory_ , 3rd ed. Englewood Cliffs, NJ: Prentice-Hall, 1996. 

- [22] J. Renaudier, G. Charlet, M. Salsi, O. B. Pardo, H. Mardoyan, P. Tran, and S. Bigo, “Linear fiber impairments mitigation of 40-Gbit/s polarization-multiplexed QPSK by digital processing in a coherent receiver,” _J. Lightw. Technol._ , vol. 26, no. 1, pp. 36–42, Jan. 2008. 

- [23] X. Zhou, J. Yu, D. Qian, T. Wang, G. Zhang, and P. Magill, “8 114 Gb/s, 25-GHz-spaced, polmux-RZ-8PSK transmission over 640 km of SSMF employing digital coherent detection and EDFA-only amplification,” in _Proc. OFC 2008_ , San Diego, CA, Feb. 2008, paper PDP6. 

- [24] P. J. Winzer and A. J. Gnauck, “112-Gb/s polarization-multiplexed 16-QAM on a 25-GHz WDM grid,” in _Proc. 34th Eur. Conf. Optical Communication (ECOC)_ , Brussels, Belgium, Sept. 2008, paper Th.3.E.5. 

- [25] J. Proakis _, Digital Communications_ , 4th ed. New York: McGrawHill, 2000, pp. 177–178. 

- [37] S. M. Kay _, Fundamentals of Statistical Signal Processing: Estimation Theory_ . Englewood Cliffs, NJ: Prentice Hall, 1993. 

- [38] E. Karami, “Tracking performance of least squares MIMO channel estimation algorithm,” _IEEE Trans. Commun._ , vol. 55, no. 11, pp. 2201–2209, Nov. 2007. 

- [39] R. A. Horn and C. R. Johnson _, Topics in Matrix Analysis_ . Cambridge, U.K.: Cambridge Univ. Press, 1991, ch. 5. 

- [40] L. G. Kazovsky, L. Curtis, W. C. Young, and N. K. Cheung, “All-fiber 90 optical hybrid for coherent communications,” _Appl. Opt._ , vol. 26, no. 3, pp. 437–439, Feb. 1987. 

- [41] X. Zhou, J. Yu, D. Qian, T. Wang, G. Zhang, and P. D. Magill, “High-spectral-efficiency 114-Gb/s transmission using PolMux-RZ8PSK modulation format and single-ended digital coherent detection technique,” _J. Lightw. Technol._ , vol. 27, no. 3, pp. 146–152, Feb. 2009. 

- [42] M. Valkama, M. Renfors, and V. Koivunen, “Advanced methods for I/Q imbalance compensation in communication receivers,” _IEEE Trans. Signal Proc._ , vol. 49, no. 10, pp. 2335–2344, Oct. 1998. 

- [43] D. Hoffmann, H. Heidrich, G. Wenke, R. Langenhorst, and N. K. Cheung, “Integrated opticseight-port 90 hybrid on LiNbO ,” _J. Lightw. Technol._ , vol. 7, no. 5, pp. 794–798, May 1989. 

- [44] N. Gisin, “Statistics of polarization dependent losses,” _Opt. Commun._ , vol. 114, no. 5–6, pp. 399–405, 1995. 

- [45] I. Roudas and N. Antoniades, “Performance outages in CWDM optical networks due to the polarization-dependent gain of semiconductor optical amplifiers,” _IEEE Photon. Technol. Lett._ , vol. 18, no. 1, pp. 48–50, Jan. 2007. 

**Ioannis Roudas,** photograph and biography not available at the time of publication. 

**Athanasios Vgenis,** photograph and biography not available at the time of publication. 

**Constantinos S. Petrou,** photograph and biography not available at the time of publication. 

- [26] J. R. Barry, E. A. Lee, and D. G. Messerschmitt _, Digital Communication_ , 3rd ed. Norwell, MA: Kluwer, 2003. 

- [27] D. Tse and P. Viswanath _, Fundamentals of Wireless Communication_ . Cambridge, U.K.: Cambridge Univ. Press, 2005, Section 3.3.3. 

- [28] H. Sun and K.-T. Wu, “Method for Quadrature Phase Angle Correction in a Coherent Receiver of a Dual-Polarization Optical Transport System,” U.S. Patent 6 917 031, Jul. 12, 2005. 

- [29] I. Roudas, M. Sauer, J. Hurley, Y. Mauro, and S. Raghavan, “Compensation of coherent DQPSK receiver imperfections,” in _Proc. IEEE LEOS Summer Topicals_ , Portland, OR, July 2007, paper MA3.4. 

**Dimitris Toumpakaris,** photograph and biography not available at the time of publication. 

**Jason Hurley,** photograph and biography not available at the time of publication. 

- [30] I. Fatadin, S. Savory, and D. Ives, “Compensation of quadrature imbalance in an optical QPSK coherent receiver,” _IEEE Photon. Technol. Lett._ , vol. 20, no. 20, pp. 1733–1735, Oct. 2008. 

- [31] C. S. Petrou, A. Vgenis, A. Kiourti, I. Roudas, J. Hurley, M. Sauer, J. Downie, Y. Mauro, and S. Raghavan, “Impact of transmitter and receiver imperfections on the performance of coherent optical QPSK communication systems,” in _Proc. LEOS 2008_ , Newport Beach, CA, Nov. 2008, paper TuFF3. 

- [32] H. Meyr, M. Moeneclaey, and S. Fechtel _, Digital Communication Receivers: Channel Estimation and Signal Processing_ . New York: Wiley, 1998, ch. 8. 

- [33] M. Morelli and U. Mengali, “Feedforward frequency estimation for PSK: A tutorial review,” _Eur. Trans. Telecommun._ , vol. 9, no. 2, pp. 103–116, Mar./Apr. 1998. 

- [34] A. Viterbi and A. Viterbi, “Nonlinear estimation of PSK-modulated carrier phase with application to burst digital transmission,” _IEEE Trans. Inf. Theory_ , vol. IT-29, no. 4, pp. 543–551, Jul. 1983. 

- [35] J. P. Gordon and H. Kogelnik, “PMD fundamentals: Polarization mode dispersion in optical fibers,” _PNAS_ , vol. 97, no. 9, pp. 4541–4550, Apr. 2000. 

- [36] S. Huard _, Polarization of Light_ . New York, NY: Wiley, 1997. 

**Michael Sauer,** photograph and biography not available at the time of publication. 

**John Downie,** photograph and biography not available at the time of publication. 

**Yihong Mauro,** photograph and biography not available at the time of publication. 

**Srikanth Raghavan,** photograph and biography not available at the time of publication. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:55 UTC from IEEE Xplore.  Restrictions apply. 


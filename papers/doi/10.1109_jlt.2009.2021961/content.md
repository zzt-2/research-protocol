JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 15, AUGUST 1, 2009 

3042 

## Blind Equalization and Carrier Phase Recovery in a 16-QAM Optical Coherent System 

Irshaad Fatadin _, Member, IEEE_ , David Ives, and Seb J. Savory _, Member, IEEE_ 

_**Abstract—**_ **Blind equalization and carrier phase recovery in a simulated 14 Gbaud 16-QAM optical coherent system are investigated. Equalization techniques to compensate for linear transmission impairments are presented using the constant modulus algorithm (CMA), the recursive least-squares (RLS)-CMA, and the radius directed equalization (RDE). With 7 T/2-spaced taps, the RDE and the RLS-CMA can compensate up to 1000 ps/nm of CD in the 16-QAM coherent system with performances comparable to the decision-directed (DD) equalizer. We show that the RDE is a promising technique for blind equalization in a 16-QAM coherent system with lower complexity than the RLS-CMA. Blind carrier phase recovery is investigated in a decision-directed-mode. We show that the blind carrier phase recovery algorithm can recover the Square-16-QAM constellation for laser beat linewidths of** 10 4 **in a polarization-multiplexed (POLMUX) 16-QAM coherent system with the RDE algorithm giving better overall performance than the CMA when compensating for CD and differential group delay (DGD). Finally, the dynamical characteristics of the equalizers to track endless polarization rotations are discussed. With the adaptation parameters optimized, the equalizers can track angular rate of rotation** 10[5] **rad/s.** 

_**Index Terms—**_ **Blind equalization, carrier phase recovery, coherent communications, QAM.** 

## I. INTRODUCTION 

HE limitations of spectrum allocation have renewed **T** interest in the spectrally efficient quadrature amplitude modulation (QAM) format. Optical multilevel modulation [1]–[3] can significantly increase spectral efficiency by reducing the symbol rate. However, the performance of -ary QAM can seriously be degraded due to intersymbol interference (ISI) as the number of levels increases. The effect of ISI is to cause the eye to close, thereby reducing the margin for amplified spontaneous emission (ASE) noise to cause errors. Equalization to suppress ISI in multilevel modulation should, therefore, be performed to achieve reliable performance [4]. 

Coherent demodulation gives a representation of the optical field in the electrical domain. This allows electronic equalization to compensate for linear transmission impairments and also 

Manuscript received December 02, 2008; revised March 10, 2009. First published May 05, 2009; current version published July 22, 2009. This work was supported by the U.K. Government Department for Innovation, Universities and Skills (DIUS). 

I. Fatadin and D. Ives are with the National Physical Laboratory, Teddington, Middlesex, TW11 0LW, U.K. (e-mail: irshaad.fatadin@npl.co.uk; david.ives@npl.co.uk). 

S. J. Savory is with the Optical Networks Group, UCL Electronic and Electrical Engineering, University College London, Torrington Place, London, WC1E 7JE, U.K. (e-mail: ssavory@ee.ucl.ac.uk). Digital Object Identifier 10.1109/JLT.2009.2021961 

to operate as a polarization demultiplexer to separate the convoluted signals that were transmitted in the two orthogonal polarization orientations. A fractionally spaced equalizer (FSE) can compensate for an arbitrary amount of chromatic dispersion (CD) and polarization-mode dispersion (PMD) in an optical coherent system provided sampling is performed above the Nyquist rate [5]. Among the many equalization techniques proposed in the literature beginning with Sato [6], the constant modulus algorithm (CMA) [7] is a well-known algorithm for blind equalization in wireless communication that does not require any training sequence for the start-up period or restarting after system breakdown. 

Blind equalization using the CMA can be applied in 16-QAM optical coherent system to compensate for linear transmission impairments. While the CMA error criterion is optimal for PSK signals, it may not be optimal for Square-16-QAM constellations in the sense that the error is not minimized even when the equalizer has fully converged [8]. This can lead to noise enhancement after equalization even in the absence of distortions [9]. In practice, after initial convergence, when the “eye is open,” the CMA-based equalizer can be switched to the classical decision directed (DD) mode to improve performance of the system. In this work, we investigate the performance of the radius directed equalization (RDE) [8] when compensating up to 1000 ps/nm of CD in a 16-QAM coherent system. Equalization using the recursive least-squares (RLS)-CMA is also investigated when compensating for CD and is shown to outperform the performance of the CMA equalizer. The RDE and the DD algorithms were found to give similar performances as the RLS-CMA algorithm with lower computational complexities when compensating up to 1000 ps/nm of CD in the 16-QAM coherent system. The RDE presented in this paper is a generalization of the CMA algorithm for QAM signals and was found to outperform the CMA in the 16-QAM coherent system which does not present a constant modulus. 

High performance carrier recovery is also an essential part of any coherent QAM receiver. In contrast to -PSK modulation where the phases are equally spaced and the modulation can be removed by taking the th power, the phase distances for Square-16-QAM are not equal and, hence, alternative approaches are required. In [10], carrier phase estimation (CPE) for laser beat linewidths of was performed by partitioning the constellation points into different groups. A similar technique has also been applied to estimate frequency offset [11] for Square-16-QAM constellations. However, this approach neglects symbols on the middle ring of the constellation for Square-16-QAM and hence requires large block lengths. As such, the required linewidths of the transmit laser and the 

0733-8724/$26.00 © 2009 IEEE Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

FATADIN _et al._ : BLIND EQUALIZATION AND CARRIER PHASE RECOVERY IN A 16-QAM OPTICAL COHERENT SYSTEM 

3043 

LO are still stringent. In [12], CPE for was achieved with a decision-directed soft-decision phase estimator employed. In [9] an improved algorithm for CPE in 16-QAM has been reported by modifying the approach in [10]. The linewidths of the laser and the LO were 1 MHz in a 100 Gbit/s 16-QAM coherent system. In this paper, we discuss a digital phase estimation appropriate for 16-QAM constellation using a blind carrier recovery algorithm. We show that the technique can estimate phase fluctuations for laser beat linewidths of in a polarization-multiplexed (POLMUX) 16-QAM coherent system. 

The paper is organized as follows. Blind equalization using the CMA, RLS-CMA, DD and the RDE are discussed in Section II. Compensation of CD using 7 T/2-spaced taps is discussed in Section III. Simulation results confirmed that the RDE leads to enhanced performance compared to the CMA. Blind carrier phase recovery in a decision-directed-mode is discussed in Section IV. Equalization in a POLMUX-16-QAM system is presented in Section V. The dynamical characteristics of the equalizers to track endless polarization rotations are also presented. We conclude our work in Section VI. 

## II. BLIND EQUALIZATION 

## _A. CMA Algorithm_ 

Amongst a number of blind equalizer schemes that have been introduced, the CMA algorithm proposed by Godard [13], also developed independently by Treichler _et al._ [14], is now well accepted and has been proposed for many applications, including the equalization of QAM systems. The cost-function of the CMA is of the form 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

where indicates statistical expectation and is the equalizer output. is the constant depending only on the input data symbol, . It is defined as [13] 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

The CMA is a blind algorithm that adapts the filter coefficients of the equalizer to reduce ISI of the received signal. Let denote the impulse response of the equalizer, we obtain the equalizer output as 

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

where is the equalizer tap weights vector, and is the equalizer input data vector. is the length of the equalizer tap weights, superscript stands for the transpose of a vector and is the complex conjugate transpose. The tap weights vector is adapted using the stochastic gradient algorithm [7] 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

(4) 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

TABLE I RLS-CMA ALGORITHM 

**==> picture [223 x 127] intentionally omitted <==**

where is the step size parameter and is the error signal given by 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

The CMA algorithm minimizes the error power between the equalizer output and a constant. Clearly, for PSK signals, this criterion is optimal in the sense that for perfect equalization, the error, , as the symbols all lie on a ring. 

## _B. RLS-CMA Algorithm_ 

The RLS-CMA optimization technique is discussed in this section. It is well known that adaptation algorithms based on the RLS technique generally have faster convergence rate than stochastic gradient descent (SGD) algorithms [15]. The cost function for the RLS-CMA algorithm is given by [16] 

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

where is the forgetting factor, and . The derivation of the cost function for the RLS-CMA assumes a stationary or slowly varying environments and its performance to track endless polarization rotations will be discussed in Section V. The RLS-CMA algorithm is updated according to the set of equations given in Table I where denotes complex conjugate and is the complex conjugate transpose. As discussed in [16], the RLS-CMA with offers the best convergence property and is the value chosen in our simulation. The output of the equalizer is then given by 

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where is the equalizer tap weights vector and is the equalizer input data vector. 

## _C. DD and RDE_ 

Since the 16-QAM constellation does not present a constant modulus as shown in the inset of Fig. 1, we discuss the DD and the RDE as alternative algorithms to CMA-based equalizers that can improve the steady-state performance. Whilst the DD is based on the symbol position closest to the equalizer output 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 15, AUGUST 1, 2009 

3044 

**==> picture [493 x 110] intentionally omitted <==**

Fig. 1. Simulation setup for 16-QAM optical coherent system. PSF: Pulse shaping filter. DSP: Digital Signal Processor. 

to update the equalizer weights, the RDE is based on the nearest symbol radius where the 16-QAM constellation presents three possible radii. 

_1) Decision-Directed:_ The error signal in the CMA equalizer after convergence can be minimized by switching over to a conventional DD algorithm to improve the steady-state performance, i.e., convergence speed and output error levels, when the eye pattern of the equalizer output is opened to some extent by the equalizer. According to Macchi and Eweda [17], an open-eye condition can be expressed as 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

where is the minimum distance between the symbols in the constellation. In this work, we investigated equalization on the detected 16-QAM signals using the DD without preconvergence with the CMA when compensating for CD up to 1000 ps/nm. The tap weights for the decision directed least-mean-square (DD-LMS) algorithm are updated as [15] 

**==> picture [12 x 10] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [246 x 212] intentionally omitted <==**

Fig. 2. Simulated back-to-back performance of 16-QAM coherent system compared with theory. 

where , with being the decision value using a standard rectilinear grid of decision regions in the constellation. 

electrical signals to give equally spaced constellation points for the 16-QAM optical coherent system. Since, rectangular pulses have a very broad frequency spectrum, due to the sharp transitions at the pulse edges, we considered a truncated Nyquist pulse using raised-cosine filtering to reduce the bandwidth of the pulse in the simulation. The in-phase (I) and quadrature (Q) signals were filtered using square-root raised cosine pulse shaping. The 16-QAM data was then transmitted over the fiber and subsequently ASE noise was loaded before the detector with a 50-GHz optical filter. We split the task of the pulse shaping equally between the transmitter and the receiver with the roll-off factor, . We, therefore, employed the square-root of the raised-cosine filter response at both the transmitter and the receiver. The product of the two filter responses led to an overall raised-cosine response having low ISI. At the receiving end, the in-phase and quadrature signals detected at the coherent receiver were analog-to-digital (A/D) converted with 6-bit resolution and then processed by the equalizers with 7 T/2-spaced taps. A 5th order low pass Bessel filter with a 3-dB bandwidth of 80% the symbol-rate was also included in the simulation as the antialiasing filter [5]. 

_2) Radius Directed Equalization:_ For QAM signals, an alternative error criterion is based on the error between the equalizer output and the nearest constellation radius. Compared to the CMA equalizer, the RDE also improved the steady-state performance for the 16-QAM signals as discussed in Section III. The RDE optimization is based on the equalizer output and the nearest constellation radius. The error criterion for the RDE is as 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

where is the radius of the nearest constellation symbol for each equalizer output. The tap weights for the RDE are then updated as given in (9) for the DD-LMS algorithm. 

## III. COMPENSATION OF CD 

Blind equalization using the algorithms presented in Sec3-dB bandwidth of 80% the symbol-rate was also included in tion II to compensate for CD in a 14 Gbaud 16-QAM optical the simulation as the antialiasing filter [5]. coherent system is discussed below. The simulation setup for The back-to-back performance of our simulated 16-QAM the coherent system under investigation is shown in Fig. 1. The transmission system with Gray coding is shown in Fig. 2 along 16-QAM constellation diagram was obtained using four-level with the expected theoretical curve. Fig. 3 shows the OSNR Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

3045 

FATADIN _et al._ : BLIND EQUALIZATION AND CARRIER PHASE RECOVERY IN A 16-QAM OPTICAL COHERENT SYSTEM 

**==> picture [247 x 176] intentionally omitted <==**

Fig. 3. Compensation of CD using the CMA, RLS-CMA, DD, and the RDE. 

**==> picture [241 x 101] intentionally omitted <==**

Fig. 4. BER performance with different number of bits resolution in A/D. (OSNR = 18 dB ) . 

penalty at a BER of when compensating up to 1000 ps/nm of CD using the CMA, RLS-CMA, DD and RDE. Improved performance was obtained with the RLS-CMA over the CMA equalizer which can achieve lower mean square error (MSE) than the CMA in the steady-state at the expense of an increased computational overhead needed to solve the RLS step at each iteration shown in Table I. The BER performance for different number of bits resolution in the A/D is shown in Fig. 4 for the case of the RLS equalizer. A resolution of 6 bits was found to be sufficient to give reliable estimation of the BER performance for the equalizers considered in this paper. 

We also investigated the performance improvement that can be achieved by applying the DD and the RDE algorithms. The RDE uses the error between the equalizer output modulus and the nearest symbol radius to update the equalizer tap weights. Fig. 3 shows the OSNR penalty when using the DD and the RDE to compensate up to 1000 ps/nm of CD. Similarly, the DD and the RDE optimization processes gave better performances than the CMA for the 16-QAM constellation. Performances comparable to the RLS-CMA were obtained for DD and RDE algorithms as seen in Fig. 3. For the RLS-CMA algorithm the computational complexity was of the order of compared to for the other equalizers, where is the length of the equalizer tap weights. The time to convergence (TTC) for the different equalizers are shown in Fig. 5(a) and (b), at an OSNR of 18 and 20 dB, respectively, with 500 ps/nm of CD. Better steady-state performances were obtained for the RLS-CMA, RDE and the DD as opposed to the CMA. 

**==> picture [247 x 342] intentionally omitted <==**

Fig. 5. Time to convergence of the different equalizers for 500 ps/nm of CD. (a) OSNR = 18 dB and (b) OSNR = 20 dB. 

**==> picture [184 x 84] intentionally omitted <==**

Fig. 6. Decision-directed (DD) carrier phase recovery. 

## IV. CARRIER PHASE RECOVERY ALGORITHM 

High performance carrier recovery is an essential part of any coherent QAM receiver. A carrier phase recovery algorithm suitable for Square-16-QAM constellations is investigated below. The block diagram of combined blind equalization and DD carrier tracking is illustrated in Fig. 6. The DD carrier recovery loop uses the error between the output of the equalizer and the corresponding decision. The phase updating rule is given by [18] 

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

where is the step-size parameter and is the error signal given by 

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

(12) 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 15, AUGUST 1, 2009 

3046 

**==> picture [247 x 168] intentionally omitted <==**

Fig. 7. Phase error standard deviation for different values of . (OSNR = 18 dB ) . 

**==> picture [247 x 257] intentionally omitted <==**

Fig. 8. Performance of carrier phase estimation with = 0:1 for different values of T . is the combined linewidths of the transmit laser and the LO. 

where is the equalized output with phase error correction and is the estimation of by a decision device. The laser phase noise in our simulation was modeled as the Wiener process 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [10 x 23] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [247 x 251] intentionally omitted <==**

Fig. 9. (a) Carrier phase fluctuations and (b) recovered carrier phase for T = 10 . (OSNR = 18 dB ) . 

**==> picture [247 x 271] intentionally omitted <==**

Fig. 10. (a) Carrier phase fluctuations and (b) recovered carrier phase for T = 10 . (OSNR = 18 dB ) . 

where is the instantaneous phase and is the fre. Fig. 8 shows the BER performance when quency noise. In Fig. 7, we investigated the standard deviation using the carrier phase recovery algorithm discussed above with of the phase error between the actual carrier phase fluctuations to compensate for different values of . The and the recovered phase for different values of and laser OSNR penalty was found to be less than 2 dB at a BER = beat linewidths, , where is the combined linewidths with . Fig. 8 shows an error floor for of the transmit laser and the LO. With , the car. The phase fluctuations and the recovered carrier phase rier phase recovery algorithm can recover beat linewidths of for laser beat linewidths of and are shown in Figs. 9 Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

FATADIN _et al._ : BLIND EQUALIZATION AND CARRIER PHASE RECOVERY IN A 16-QAM OPTICAL COHERENT SYSTEM 

3047 

**==> picture [338 x 102] intentionally omitted <==**

Fig. 11. Computational framework for the carrier phase recovery algorithm. 

**==> picture [247 x 156] intentionally omitted <==**

Fig. 12. Convergence for CMA and RDE algorithms with CD = 500 ps/nm and T = 10 . (OSNR = 22 dB ) . 

and 10, respectively. Fig. 9 shows that the estimated carrier phase using algorithm (11) closely tracked the expected phase fluctuations due to the laser phase noise. It is interesting to note that in (11) no nonlinear operation is required as with the th-power scheme [9], [10]. Also, no phase unwrapping was performed when using the above DD carrier tracking algorithm. However, the above technique was found to be inappropriate to track phase fluctuations for as seen in Fig. 10. The computational framework for the carrier phase recovery algorithm which is based on the feed-forward control scheme is shown in Fig. 11. We also investigated the performance of combined blind equalization and DD carrier tracking as shown in Fig. 12 with the CD set to 500 ps/nm and . Fig. 12 compares the performance of the system at an OSNR of 22 dB when using the CMA and the RDE algorithms for blind equalization. The RDE was found to outperform the CMA due to its better steady-state performance and lower ISI at convergence consistent with the results obtained in Section III. 

**==> picture [161 x 80] intentionally omitted <==**

Fig. 13. Equalizer for POLMUX-16-QAM optical coherent system. 

**==> picture [182 x 174] intentionally omitted <==**

Fig. 14. (a) Unequalized output in a POLMUX-16-QAM optical coherent system. (b) Equalization with RDE before carrier phase recovery. Recovered signals for (c) X - and (d) Y -Polarizations. (OSNR = 22 dB ) . 

structure as shown in Fig. 13 to reproduce the inverse Jones matrix [20]. The outputs of the equalizer are given by 

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [18 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

## V. EQUALIZATION IN A POLMUX-16-QAM COHERENT SYSTEM 

With a symbol rate of 14 Gbaud, a POLMUX-16-QAM optical coherent system allows transmission at a data rate of 112-Gb/s [19] which is appropriate for 100-Gb/s Ethernet (100 GE) with the necessary overheads for forward error correction (FEC). Equalization in a POLMUX system can be accomplished by a bank of FIR filters arranged in a butterfly 

for the - and the -polarizations, respectively. The filter coefficients can then be adapted as discussed in Section II to compensate for linear transmission impairments and to recover the polarization multiplexed data. An example where the RDE blind algorithm has been applied to a POLMUX-16-QAM optical coherent system to compensate for CD and differential group delay (DGD) is shown in Fig. 14. The taps of the FIR filter were T/2-spaced and 7 taps were implemented in the simulation. The gain coefficients of the taps were initialized with the center taps 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 15, AUGUST 1, 2009 

3048 

**==> picture [243 x 137] intentionally omitted <==**

Fig. 15. Compensation of CD using CMA and RDE in a POLMUX-16-QAM optical coherent system with = 45 , = 50 ps and T = 10 . (OSNR = 22 dB ) . 

of and set to unity and updated accordingly. The frequency response of the fiber with CD and DGD was included in the simulation using 

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where and are the GVD parameter and the length of the fiber, respectively, is the angle between the reference polarization and the principal states of polarization (PSP) of the fiber, and is the DGD between the PSPs. Fig. 14(a) shows the unequalized constellation diagram of the received signals with a CD of 500 ps/nm, (worst case), and a DGD of 50 ps where the eye is completely closed. The laser beat linewidths, , was set to in the POLMUX-16-QAM coherent system. Fig. 14(b) shows the recovered signal after convergence at an OSNR of 22 dB with the RDE algorithm before carrier phase recovery. Fig. 14(c) and (d) shows the derotated symbols - after employing the carrier-recovery algorithm (11) for the and the -polarizations, respectively. Carrier phase recovery can, thus, successfully be achieved in a POLMUX-16-QAM coherent system with . The performance of the RDE algorithm is compared with the CMA in Fig. 15 for different amount of accumulated CD. As it can be seen, the RDE was found to outperform the CMA when compensating for CD and DGD in the presence of phase noise. 

Finally, we investigated the dynamical characteristics for different equalizers by simulating an endless polarization rotations with the Jones matrix 

**==> picture [7 x 24] intentionally omitted <==**

**==> picture [6 x 24] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [17 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [244 x 359] intentionally omitted <==**

Fig. 16. Tracking performance for different equalizers with the adaptation parameters (a) and (b) . ( ! = 100 krad = s and OSNR = 20 dB). 

**==> picture [247 x 180] intentionally omitted <==**

Fig. 17. Dynamic response for different equalizers with endless polarization rotations. (OSNR = 20 dB ) . 

where is the angular rate of rotation. Fig. 16 shows the tracking performance for different equalizers with the adaptation parameters and at an OSNR of 20 dB and set to 100 krad/s. Fig. 17 shows the dynamical characteristics of the different equalizers with 3 taps in the butterfly FIR filter. The algorithms were able to track angular frequencies 

rad/s. The performance for the CMA was found to be better than the RLS-CMA for krad s. This could be due to the derivation of the RLS-CMA cost function [16] being based on the assumption of a stationary or slowly varying signal environments. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 

FATADIN _et al._ : BLIND EQUALIZATION AND CARRIER PHASE RECOVERY IN A 16-QAM OPTICAL COHERENT SYSTEM 

3049 

## VI. CONCLUSION 

Blind equalization and carrier phase recovery in a simulated 14 Gbaud 16-QAM coherent system have been investigated. Equalization to suppress ISI in multilevel modulation formats is necessary to improve performance of the transmission system together with a high performance carrier recovery. The CMA, RLS-CMA, DD and the RDE equalization techniques to compensate up to 1000 ps/nm of CD have been investigated in the 16-QAM coherent system. The RLS-CMA can achieve lower MSE than the CMA in the steady-state at the expense of an increased computational complexity. The RDE can give similar performance as the RLS-CMA with lower complexity. Blind carrier phase recovery has also been investigated in a decision-directed-mode for a Square-16-QAM constellation. We showed that the carrier phase recovery algorithm can successfully recover laser beat linewidths of in a POLMUX-16-QAM optical coherent system with the RDE being a promising equalization technique to compensate for linear transmission impairments. Finally, the dynamical characteristics for different equalizers to track endless polarization rotations were compared. 

## REFERENCES 

- [1] S. Walklin and J. Conradi, “Multilevel signaling for increasing the reach of 10 Gb/s lightwave systems,” _J. Lightw. Technol._ , vol. 17, no. 11, pp. 2235–2248, Nov. 1999. 

- [2] J. Kahn and K.-P. Ho, “Spectral efficiency limits and modulation/detection techniques for DWDM systems,” _IEEE J. Sel. Topics Quant. Electron._ , vol. 10, pp. 259–272, 2004. 

- [3] N. Kikuchi, K. Sekine, and S. Sasaki, Multilevel Signalling for HighSpeed Optical Transmission, 2006, paper Tu3.2.1. 

- [4] N. Kikuchi, “Intersymbol interference (ISI) suppression technique for optical binary and multilevel signal generation,” _J. Lightw. Technol._ , vol. 25, no. 8, pp. 2060–2068, Aug. 2007. 

- [5] E. Ip and J. M. Kahn, “Digital equalization of chromatic dispersion and polarization mode dispersion,” _J. Lightw. Technol._ , vol. 25, no. 8, pp. 2033–2043, Aug. 2007. 

- [6] Y. Sato, “A method of self-recovering equalization for multilevel amplitude-modulation systems,” _IEEE Trans. Commun._ , vol. COM-23, no. 6, pp. 679–682, Jun. 1975. 

- [7] C. R. Johnson, P. Schniter, T. J. Endres, J. D. Behm, D. R. Brown, and R. A. Casas, “Blind equalization using the constant modulus criterion: A review,” _Proc. IEEE_ , vol. 86, no. 10, pp. 1927–1950, Oct. 1998. 

- [8] M. J. Ready and R. P. Gooch, “Blind equalization based on radius directed adaptation,” in _Proc. ICASSP_ , Apr. 1990, vol. 3, pp. 1699–1702. 

- [9] H. Louchet, K. Kuzmin, and A. Richter, “Improved DSP algorithms for coherent 16-QAM transmission,” presented at the ECOC 2008, Brussels, Belgium, 2008, paper Tu.1.E.6. 

- [10] M. Seimetz, “Laser linewidth limitations for optical systems with highorder modulation employing feed forward digital carrier phase estimation,” presented at the OFC/NFOEC, 2008, paper OTuM2. 

- [11] M. Seimetz, “Performance of coherent optical square-16-QAM-systems based on IQ-transmitters and homodyne receivers with digital phase estimation,” presented at the Nat. Fiber Optic Engineers Conf., Anaheim, CA, 2006, paper NWA4. 

- [12] E. Ip and J. M. Kahn, “Feedforward carrier recovery for coherent optical communications,” _J. Lightw. Technol._ , vol. 25, no. 9, pp. 2675–2692, Sep. 2007. 

- [13] D. Godard, “Self-recovering equalization and carrier tracking in two-dimensional data communication systems,” _IEEE Trans. Commun._ , vol. 28, no. 11, pp. 1867–1875, Nov. 1980. 

- [14] J. R. Treichler and B. G. Agee, “A new approach to multipath correction of constant modulus signals,” _IEEE Trans. Acoust., Speech, Signal Process._ , vol. ASSP-31, no. 4, pp. 459–472, Apr. 1983. 

- [15] J. G. Proakis _, Digital Communications_ , 4th ed. New York: McGrawHill, 2001. 

- [16] Y. Chen, T. Le-Ngoc, B. Champagne, and X. Changjiang, “Recursive least squares constant modulus algorithm for blind adaptive array,” _IEEE Trans. Signal Process._ , vol. 52, no. 5, pp. 1452–1456, May 2004. 

- [17] O. Macchi and E. Eweda, “Convergence analysis of self-adaptive equalizers,” _IEEE Trans. Inf. Theory_ , vol. 30, no. 3, pp. 161–176, Mar. 1984. 

- [18] G. Picchi and G. Prati, “Stop-and-go decision-directed algorithm,” _IEEE Trans. Commun._ , vol. 35, no. 9, pp. 877–887, Sep. 1987. 

- [19] P. J. Winzer and A. H. Gnauck, “112-Gb/s polarization-multiplexed 16-QAM on a 25-GHz WDM grid,” presented at the ECOC, Brussels, Belgium, 2008, paper Th.3.E.5. 

- [20] S. J. Savory, “Digital filters for coherent optical receivers,” _Opt. Exp._ , vol. 16, no. 2, pp. 804–817, 2008. 

**Irshaad Fatadin** (M’02) received the B.Sc. degree (hons.) in physics from the University of Delhi, Delhi, India, in 2000, and the M.Phil. degree in microelectronic engineering and semiconductor physics from the University of Cambridge, Cambridge, U.K., in 2002. 

He joined the National Physical Laboratory, Middlesex, U.K., in 2002. His research and development interests include the areas of coherent optical communication systems, advanced modulation formats, optical waveguides, photonic integration, and numerical simulation of optoelectronic devices. 

Mr. Fatadin is a Chartered Engineer and member of the IOP and IEEE Lasers and Electro-Optics Society. 

**==> picture [73 x 91] intentionally omitted <==**

- **David Ives** was born in Burnham-on-Crouch, U.K., in 1967. He received the B.Sc. degree in physics from Birmingham University, Birmingham, U.K., in 1988. He is a Senior Research Scientist in the Photonics 

- Group at the National Physical Laboratory, Middlesex, U.K. His research and development interests include the areas of optical fiber measurement and characterization, optical fiber test equipment characterization, and numerical simulation of optical communication systems. 

Mr. Ives is a Chartered Physicist, U.K., and 

member of the IOP. 

**==> picture [73 x 91] intentionally omitted <==**

**Seb J. Savory** (M’07) received the M.A., M.Eng., and Ph.D. degrees in engineering from the University of Cambridge, Cambridge, U.K. and the M.Sc. (Maths) degree from the Open University, U.K. His interest in optical communications began in 1991, when he joined Standard Telecommunications Laboratories, Harlow, U.K. (now Nortel), prior to being sponsored though his undergraduate and postgraduate studies by Nortel. On completion of the Ph.D. degree in 2000, he joined Nortel’s Laboratories as a full-time Senior Research Engineer, working 

on digital signal processing and advanced optical transmission systems. In 2005, he joined the Optical Networks Group at University College London (UCL), U.K., where he held a Leverhulme Trust Early Career Fellowship from 2005–2007, being appointed to a lectureship in 2007. His current research is focused on advanced optical transmission systems including digital coherent transmission systems and advanced modulation formats. 

Dr. Savory is a Chartered Engineer and member of the Institute of Engineering and Technology, U.K. He is a member of the Photonics Society and the Signal Processing Society, an Associate Editor for IEEE PHOTONICS TECHNOLOGY LETTERS, and serves on the technical program committee of OFC/NFOEC, ECOC, and the IEEE LEOS annual meeting. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 18:00:03 UTC from IEEE Xplore.  Restrictions apply. 


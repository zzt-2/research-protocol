

## DSP for coherent single-carrier receivers 

### Citation for published version (APA): 

Kuschnerov, M., Hauske, F. N., Piyawanno, K., Spinnler, B., Al Fiad, M. S. A. S., Napoli, A., & Lankl, B. (2009). DSP for coherent single-carrier receivers. Journal of Lightwave Technology, 27(16), 3614-3622. https://doi.org/10.1109/JLT.2009.2024963 

### DOI: 

10.1109/JLT.2009.2024963 

Document status and date: Published: 01/01/2009 

### Document Version: 

Publisher’s PDF, also known as Version of Record (includes final page, issue and volume numbers) 

### Please check the document version of this publication: 

• A submitted manuscript is the version of the article upon submission and before peer-review. There can be important differences between the submitted version and the official published version of record. People interested in the research are advised to contact the author for the final version of the publication, or visit the DOI to the publisher's website. 

- The final author version and the galley proof are versions of the publication after peer review. 

- The final published version features the final layout of the paper including the volume, issue and page numbers. 

Link to publication 

#### General rights 

Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognise and abide by the legal requirements associated with these rights. 

- Users may download and print one copy of any publication from the public portal for the purpose of private study or research. 

- You may not further distribute the material or use it for any profit-making activity or commercial gain 

- You may freely distribute the URL identifying the publication in the public portal. 

If the publication is distributed under the terms of Article 25fa of the Dutch Copyright Act, indicated by the “Taverne” license above, please follow below link for the End User Agreement: 

www.tue.nl/taverne 

#### Take down policy 

If you believe that this document breaches copyright please contact us at: 

openaccess@tue.nl 

providing details and we will investigate your claim. 

Download date: 05. Aug. 2026 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 16, AUGUST 15, 2009 

3614 

# DSP for Coherent Single-Carrier Receivers 

Maxim Kuschnerov _, Student Member, IEEE_ , Fabian N. Hauske _, Member, IEEE_ , Kittipong Piyawanno, Bernhard Spinnler, Mohammad S. Alfiad _, Student Member, IEEE_ , Antonio Napoli, and Berthold Lankl _, Member, IEEE_ 

**_Abstract—_ In this paper, we outline the design of signal processing (DSP) algorithms with blind estimation for 100-G coherent optical polarization-diversity receivers in single-carrier systems. As main degrading optical propagation effects, we considered chromatic dispersion (CD), polarization-mode dispersion (PMD), polarization-dependent loss (PDL), and cross-phase modulation (XPM). In the context of this work, we developed algorithms to increase the robustness of the single DSP receiver modules against the aforesaid propagation effects. In particular, we first present a new and fast algorithm to perform blind adaptive CD compensation through frequency-domain equalization. This low complexity equalizer component inherits a highly precise estimation of residual dispersion independent from previous or subsequent blocks. Next, we introduce an original dispersion-tolerant timing recovery and illustrate the derivation of blind polarization demultiplexing, capable to operate also in condition of high PDL. At last, we propose an XPM-mitigating carrier phase recovery as an extension of the standard Viterbi–Viterbi algorithm.** 

**_Index Terms—_ Blind adaptation, carrier phase recovery, coherent detection, digital receiver, equalization, fiber optic communication, timing recovery.** 

### I. INTRODUCTION 

IGITAL SIGNAL PROCESSING (DSP) algorithms for **D** blind coherent fiber optic receivers can be derived from their wireless communication counterparts. However, modifications and further developments are necessary and inevitable considering the special nature of the fiber channel. Although the algorithms have to be as simple as possible to enable high-speed processing, the channel impulse response that can arise in the fiber channel differs from typical wireless systems and can be significantly longer. Since the variations in the fiber channel are very slow compared to the symbol rate, adaptation speed is of less concern, so that blind adaptation can be used. 

Chromatic dispersion (CD) is typically compensated for by a finite impulse response (FIR) butterfly structure [1]. In case of large accumulated CD in uncompensated links, the equalization of CD and PMD can be performed in two steps, first compensating for the static dispersion [2]. Here, the equalizer 

Manuscript received January 15, 2009; revised May 11, 2009. First published June 10, 2009; current version published July 24, 2009. 

M. Kuschnerov, K. Piyawanno, and B. Lankl are with the University of the Federal Armed Forces, Munich, 85577 Neubiberg, Germany (e-mail: maxim.kuschnerov@unibw.de; Kittipong.piyawanno@unibw.de; berthold.lankl@unibw.de). 

F. N. Hauske is on the leave from the University of the Federal Armed Forces, Munich, 85577 Neubiberg, Germany (e-mail: fabian.hauske@unibw.de). 

B. Spinnler and A. Napoli are with Nokia Siemens Networks, Munich 81379, Germany (e-mail: bernhard.spinnler@nsn.com; antonio.napoli@nsn.com). 

M. S. Alfiad is with COBRA institute, Eindhoven University of Technology, Eindhoven 5612AZ, The Netherlands (e-mail: m.s.alfiad@tue.nl). 

Digital Object Identifier 10.1109/JLT.2009.2024963 



Fig. 1. Polarization-diversity coherent receiver front-end. 

usually cannot be properly adapted using standard adaptation algorithms due to the severity of the distortion. In various investigations based on measured data, the filtering function for the CD compensation was either _a priori_ known or no information on the blind adaptation scheme with an appropriate analysis was given [2]. 

Next, a correction of the timing frequency and phase offset is necessary before the FIR butterfly filter. Conventional timing recovery algorithms cited in [1] and [3] lack a high dispersion tolerance that is usually required in optically compensated systems, thus creating a possible bottleneck in the receiver design. 

Contrary to wireless communication using polarization multiplexing [4], where the absolute signal polarization only slightly deviates from the original axes of the transmitter, the polarization evolution in typical fibers is arbitrary. Coherent receivers therefore require either a polarization control to align the signal and the local oscillator (LO), or polarization diversity reception, where the cross-polarization interference can be compensated for in the digital domain. Modifications to blind equalizer adaptation algorithms are required to achieve the demultiplexing of the two polarizations. 

Finally, XPM has been identified as the major limitation in the multichannel transmission of quaternary phase-shift keying (QPSK) over legacy systems with ON–OFF keying (OOK) neighbors [6], [7]. XPM can be mitigated in the carrier phase recovery averaging over only a small number of taps due to the rapid XPM-induced phase fluctuations [8]. 

This paper presents solution concepts for all of the above mentioned problems of DSP algorithm design, emphasizing the subcomponent interaction, and is structured as follows. Section II provides an overview on the coherent optical receiver, while Section III introduces the frequency-domain equalizer as the first component of the digital receiver and presents a blind CD estimation algorithm. Sections IV and V present the timing recovery and the blind polarization demultiplexing, respectively. Section VI deals with the XPM-mitigating carrier phase recovery. Finally, Section VII draws the conclusions. The digital signal processing principles will be mainly demonstrated on single-carrier polarization-multiplexed (PolMux) QPSK, 

0733-8724/$25.00 © 2009 IEEE 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

3615 

KUSCHNEROV _et al._ : DSP FOR COHERENT SINGLE-CARRIER RECEIVERS 



Fig. 2. Digital signal processing in a blind coherent digital receiver. 



Fig. 3. Chromatic dispersion compensation using (a) time-domain filtering and (b) frequency-domain filtering. 

although they can as well be applied to higher order modulation formats. 

### II. BLIND COHERENT RECEIVER DESIGN 

A typical coherent receiver front-end employing polarization diversity is shown in Fig. 1 [1]. After a polarization-beam splitter, the two orthogonal polarizations are mixed with a local oscillator in two 90 optical hybrids and sampled in an analog-to-digital converter (ADC) after the automatic gain control (AGC). Depending on the distortion-tolerance requirements, the ADC can sample with one or two samples per symbol. While a twofold oversampling makes it possible to fully equalize the signal, symbol-rate sampling can be employed in lower complexity systems with a limited dispersion tolerance [9]. The local oscillator can be controlled via low-bandwidth feedback from the receiver to achieve a rough frequency alignment, while a precise digital carrier frequency acquisition continuously tracks the remaining frequency and phase offset in the electrical domain. Further digital signal processing is required in order to compensate for linear distortion, mitigate nonlinear transmission effects, and demultiplex both polarizations. 

In the following, the signals in the four real-valued tributaries will be described in complex vector notation form leading to 





































































Here, , , is the complex symbol vector at the time instant consisting of one sample for Nyquist rate sampling or two samples for twofold oversampling. A typical blind receiver block diagram is shown in Fig. 2. 

The receiver employs frequency-domain equalization (FDE) to compensate for the bulk of accumulated chromatic disper- 

sion. Then, the signal is retimed, demultiplexed, and equalized in a butterfly FIR filter. Finally, the constellation diagram is derotated in the carrier frequency and phase recovery. Throughout this paper, a 35-GHz, second-order optical Gauss filter and a 19.6-GHz fifth-order electrical Bessel filter were assumed. 

### III. DISPERSION COMPENSATION 

### _A. Filter Design_ 

Coherent transmission systems can be operated either on optically compensated links with dispersion-compensating fiber (DCF), or over fully uncompensated links with no DCFs in place. In the latter case, system installation can be made more cost-efficient and tolerant to nonlinearities [10]. If dispersion compensation is performed in front of the timing recovery and the other processing blocks in the receiver, the subsequent algorithms can remain identical for compensated and uncompensated transmission with similar residual dispersion requirements. 

Dispersion can either be compensated using time-domain (TDE) [2] or frequency-domain equalization [11]. Fig. 3 shows the equalizer structures for TDE and FDE equalization. 

The filter choice between TDE and FDE mainly depends on the maximum dispersion in the channel and the resulting filter length. Fig. 4 compares the equalization complexity for 43- and 112-Gb/s PolMux-QPSK receivers [11]. Here, a FIR butterfly with five taps (43 Gb/s) and nine taps (112 Gb/s) was assumed, in order to compensate for PMD and low-pass filtering. The filter length is set to a maximum of 1-dB required OSNR penalty for the given chromatic dispersion. While the CD compensating filters were assumed nonadaptive for the computation, the timedomain butterfly filter was adapted using the least-mean square algorithm (LMS) [12]. Fig. 4 shows that FDE achieves a break- 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 16, AUGUST 15, 2009 

3616 



Fig. 4. Filtering complexity for 43- and 112-Gb/s PolMux-QPSK versus chromatic dispersion [11]. 

TABLE I 

COMPARISON OF DATA-AIDED AND BLIND ADAPTATION 



even over TDE starting at 11 000 ps/nm in 40 G systems and at 2000 ps/nm in 100-G systems. 

Another possibility for dispersion compensation is infinite impulse response (IIR) filtering, where the required tap number is lower as for FIR filters [13]. However, the inherent feedback of IIR equalizers makes this approach virtually impossible to implement in high-speed applications with parallelized signal processing. In the following, dispersion estimation will be demonstrated on the example of FDE, although it can as well be applied to time-domain filters. 

### _B. Dispersion Estimation_ 

The receiver must be able to estimate the chromatic dispersion at system startup and continuously monitor it during transmission. Ideally, the estimation is performed in the dispersioncompensating device, independently of the follow-up DSP, thus increasing the startup speed of the receiver. 

If the dispersion is to be estimated, one can distinguish between data-aided and blind estimation algorithms. The pros and cons for each are listed in Table I. 

In addition to these arguments, one has to add that there is only one unknown parameter in the second-order approximation of the chromatic dispersion transfer function, which can be analytically described by 





































where is the transmission distance, is the dispersion parameter, is the carrier wavelength, is the speed of light, and 



Fig. 5. Minimum-search frequency-domain equalizer, identical for both polarizations i = x; y . 

TABLE II 

COMPUTATION OF THE NORMALIZATION CONSTANTS R [b] 



is the angular frequency. Clearly, the equation, which describes a parabolic phase transfer function, has only one degree of freedom, so that a fully adaptive estimation is not justified under these conditions. 

In the following, a blind estimation algorithm first introduced in [14] will be presented that restricts the equalizer solutions to the inverse of the dispersion transfer function from (2), thus stabilizing the equalizer convergence. The presented minimumsearch algorithm is nondata aided and works prior to the timing recovery. Given a minimum and a maximum dispersion in the channel, predefined CD-values are loaded in the filter as shown on Fig. 5. 

The proposed minimum search algorithm uses an error criterion that was derived from Godard’s CMA [15]. It employs a cost function working on the twofold oversampled signal given by 









































where are the normalization constants of the odd and the even samples for , and is index of the fast Fourier transform (FFT)-block. In order to account for the changing timing phase due to the timing frequency offset between the transmitter and receiver oscillators, the normalization constant is determined separately for every FFT signal block. They are computed from the mean power for the odd and even samples after equalization given by 







































where is the number of symbols equalized per each FFT. Here, a simple case differentiation of the power ratio for each FFT-block is sufficient to give optimum results regardless of return-to-zero (RZ) or nonreturn-to-zero (NRZ) pulse shaping. It is given in Table II. 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

3617 

KUSCHNEROV _et al._ : DSP FOR COHERENT SINGLE-CARRIER RECEIVERS 



Fig. 6. Estimation example for a preloaded CD value of 120 000 ps/nm for 112-Gb/s PolMux-QPSK. The initial scan is performed in steps of CD = 200 ps/nm. 

In the following, the parameters have been optimized using RZ-pulse shaping with the constraint of a minimum estimation error. They are set to , , , and with the signal power in each polarization normalized to half the total signal power. 

For every value of chromatic dispersion, the total cost function is given by 













































, with symbols used for the cost function of each CD value. The minimum of indicates the correct value of chromatic dispersion. After a rough scan with a large , the dispersion values around the minimum can be scanned at a higher resolution improving the estimation precision. An exemplary estimation of the optimum filter value with a rough scan is given in Fig. 6. 

The main limiting parameter for the proposed algorithm is PMD, since this effect is not modeled in the transfer function , deteriorating the estimation. Fig. 7 shows the standard deviation of the estimator versus the mean DGD for 112-Gb/s polarization multiplexed QPSK and 16 quadrature amplitude modulation (QAM). Here, a maximum dispersion of 48 000 ps/nm was computed from the 3-dB penalty limit of the required OSNR at BER for an FFT size of 1024 symbols, where half of the samples were used for overlap. In general, the overlap size should be larger than the length of the channel impulse response. An average over eight FFT blocks was used for the cost function computation at each CD value. 



Although the computation of was optimized for RZ-QPSK, NRZ-QPSK as well as 16-QAM also perform similarly. With varying FFT sizes, the estimation performance remains virtually the same, if the identical number of symbols is used for the computation of , and and are appropriately scaled with the FFT size. 

The required tap number of the subsequent FIR butterfly filter is governed by the mean DGD and the maximum residual CD after the dispersion compensating block. The proposed algorithm avoids an additional FFT for feedback that is inevitable in standard adaptive FDE [16]. Furthermore, it is not significantly affected by nonlinearities as demonstrated by measurements in 



Fig. 7. Estimation performance versus mean DGD (full-order PMD) for RZ and NRZ pulse shaping of 112-Gb/s PolMux-QPSK (OSNR = 14 dB) and PolMux-16 QAM (OSNR = 17 dB). 



Fig. 8. General timing recovery block diagram. 

[17]. After the dispersion estimation at the startup of the transmission, tracking is possible estimating the residual CD from the taps of the FIR butterfly equalizer [18]. 

### IV. TIMING RECOVERY 

The task of the timing recovery is to correct for the timing phase and frequency offset between the transmitter and receiver clocks. The timing error can be corrected in a feedforward structure, e.g., using the square timing recovery [19], where an interpolation to four samples per symbol is required. If two samples per symbols are used, an early–late phase error indicator can be derived using, e.g., the Gardner algorithm [20]. The phase error is then typically fed into a second-order phase-locked loop (PLL). The correction of the timing phase is performed either in the digital domain via an interpolator, as shown in Fig. 2, or directly in the ADC. 

Fig. 8 shows a general block diagram of a timing recovery. After prefiltering the signal, the timing phase error is detected using the known algorithms and then typically averaged in a postfilter. 

Depending on the residual estimation error of the electrical CD compensation or on the residual dispersion in optically compensated systems, a certain dispersion tolerance of timing recovery algorithms can be desired. Conventional timing recovery algorithms rely on the filtering of the spectral line at the symbol rate after the squaring of the signal. With increasing dispersion, the spectrum clock line disappears as shown in Fig. 9, so that no reliable timing phase error can be generated. 

Since chromatic dispersion has an all-pass character, theoretically, a prefilter can be designed that perfectly recovers the spectral line. However, such a filter would have to be adaptive, introducing further complexity to the receiver. In [21] a simple, suboptimal prefilter was introduced that increases the tolerance 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 16, AUGUST 15, 2009 

3618 



Fig. 9. Spectrum of the absolute square of a 112-Gb/s PolMux-QPSK signal after low-pass filtering for several values of chromatic dispersion. The spectral clock line is at 28 GHz. 



Fig. 10. Absolute value of the prefilter transfer function H for several filter lengths N . 



of the timing recovery up to arbitrary values of chromatic dispersion. The filter is given by 



















where is the filter length index, is the number of filtered symbols, and for twofold oversampling. The resulting filter is a band-pass around the Nyquist frequency. Increasing the filter length , the band-pass of the filter can be decreased, thus lowering interfering beat terms at the symbol rate after signal squaring. The filtering requires only adders and can be performed separately on the odd and even samples of the signal with filter length to further reduce complexity, which will be assumed in the following. The transfer function value is shown in Fig. 10 for several realizations of . 



The minimum required length for the timing recovery prefilter is defined by the signal spread due to chromatic dispersion, similar to FIR filter length requirements for equalization. The dispersion tolerance of the timing recovery will be demonstrated using the timing detector presented in [21]. The performance of the histogram timing recovery can be verified against the modified Cramer–Rao bound (MCRB), which is the lower bound on the normalized estimation variance and given by 

































Fig. 11. Estimator performance versus chromatic dispersion for various prefilter lengths N , L = 1000 , and 112-Gb/s PolMux-QPSK at OSNR = 15 dB. 

with 











































for pulse-amplitude modulation, where is the symbol duration, is the averaging length of the postfilter, and is the spectrum of the signal pulse shape. Fig. 11 shows the estimator variance versus chromatic dispersion for several prefilter lengths. 

In a back-to-back configuration with zero dispersion and no prefiltering, the estimator performance is very close to the MCRB. The maximum dispersion that can be tolerated in this case is around 300 ps/nm. The dispersion tolerance requirement in optically compensated systems is usually higher, and in the case that the previously presented electrical dispersion compensation was used, the estimation precision can deteriorate for high PMD. In order to remove the timing recovery bottleneck, the prefilter can be introduced, clearly increasing the dispersion tolerance a the cost of a back-to-back degradation. A similar performance as in back-to-back configurations without prefiltering can be achieved, if the averaging length of the filter is increased, thus lowering the overall response bandwidth. 

### V. BLIND POLARIZATION DEMULTIPLEXING 

Polarization multiplexing in the fiber optic channel is a principle that has been used in radio transmission since the 1980s [4]. The optic channel is a special case of the more general multiple-input–multiple-output (MIMO) systems, widely applied in space-division multiplexing. Polarization demultiplexing is one of the most interesting problems of coherent receiver design. 

The CMA is a popular choice for approximate channel acquisition that can be followed by the LMS for tracking purposes. If no known training symbols are available at the receiver, translating the CMA from a single-input–single-output (SISO) channel to a 2 2 MIMO equalizer [26], as shown in Fig. 3, results in the possibility of the degenerate one-to-many output problem. 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

3619 

KUSCHNEROV _et al._ : DSP FOR COHERENT SINGLE-CARRIER RECEIVERS 



Fig. 12. Comparison of the equalizer failure probability with a degenerate solution for pure CMA/LMS and with an added constraint of a unitary PMD matrix versus PDL for 112-Gb/s PolMux-QPSK, CD = 1000 ps/nm and OSNR = 14 dB. A 15-tap T/2 filter is used for equalization. 

In [2] and [22], the PMD-matrix constraint was imposed on the equalizer filter taps, using the unitary properties of the fiber channel transfer function given by 













































with being the PMD transfer matrix with . Although this approach works well as long as the matrix is unitary, once significant PDL is present in the channel, the transfer function loses its previously described characterization and the probability of a degenerate equalizer solution increases as shown in Fig. 12, with the identical polarization appearing at both outputs of the equalizer. Here, one can distinguish between a best and a worst case in terms of performance, depending on the input polarization into the PDL element at the beginning of the transmission [5]. For a given channel realization, the equalizer converged using CMA/LMS with the constraint of (9). In the degenerate case of the same polarization at both equalizer outputs, a convergence failure was counted. Since the degenerate convergence is a random process that depends on the transmitted signal, noise, distortion, as well as the update speed of the equalizer, a convergence failure probability was evaluated over 

Other solutions for the demultiplexing problem have been demonstrated for one-tap filters only [23], or have not been fully commented upon [5]. In [24], a semiblind approach is described, where one polarization is adapted blindly and the other one afterwards with the help of the extracted training symbols from the first polarization, presumably using higher layer information bits. Introducing training symbols in all polarizations might seem as the most elegant solution [25]. However, it comes at the cost of signal overhead, so that a fully blind approach might be preferred for 100-G QPSK systems. 

The problem of blind source separation based on the CMA has been widely covered in wireless literature [27], [28]. While the CMA is able to achieve optimal equalization using second- 



Fig. 13. Required OSNR penalty versus PDL, at 1000-ps/nm CD, 30-ps mean DGD (full-order PMD), and 15 taps of a T/2-spaced butterfly FIR and 112-Gb/s PolMux-QPSK. 

order statistics in combination with oversampling, MIMO systems require higher order statistics [29], and independent-component analysis (ICA) in order to achieve blind source separation, as introduced by [30] for fiber optic systems and one-tap filtering. While [30] uses an ICA cost function different from the CMA or LMS, the source separation method described in [28] has the advantage that it can be added on top of the existing CMA/LMS algorithms, thus leading to virtually identical convergence and tracking properties in most cases as standard CMA algorithms. It is given by 









































































where is the expectation value. Here is the cross-correlation function between polarization and defined as 



























and and are integers that depend on the channel delay spread. By minimizing the cross-correlation between the channels, both sources can be separated in presence of PDL. Fig. 13 evaluates the performance of the algorithm versus PDL for simulations of 112-Gb/s PolMux-QPSK using a 15-tap T/2 fractionally spaced FIR butterfly with worst case distortions of 1000 ps/nm and 30-ps mean DGD (full-order PMD). Even in this case, where the channel memory length begins to exceed the number of equalizer taps, the theoretical performance can approximately be achieved for PDL ranging from 0 to 10 dB. 

After initial convergence with the CMA, faster convergence can be reached by switching to the LMS, especially if significant PDL is present. However, the LMS algorithm is decision directed, requiring a prior correction of the carrier phase and frequency offset. 



The mixing with the local oscillator introduces a frequency and phase offset, identical in both polarizations, leading to a 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 16, AUGUST 15, 2009 

3620 



Fig. 14. Block diagram of the JP V&V carrier phase estimator for the x -polarization with LMS equalization. 



Fig. 15. Block diagram of the JP carrier phase estimator for the x -polarization with CMA equalization. 

rotating constellation diagram. Feedback or feedforward algorithms can be used to compensate for the LO phase offset [31]. While the LO-phase recovery should have a rather low bandwidth in order to minimize noise influence, a second high-bandwidth component can be employed to mitigate for nonlinearities, if SPM and XPM are the main limiting effects over amplified spontaneous emission (ASE) and the LO phase noise. If the coherent polarization multiplexed channel is transmitted in overlay to legacy OOK channels, the resulting cross-phase modulation (XPM) can be effectively compensated using the phase recovery [8]. Here, the th power Viterbi-and-Viterbi (V&V) algorithm was used for phase offset estimation [32] by reducing the averaging length for the feedforward structure down to 2–5 symbols. The estimator is given by 













































where is a weighting factor, and have to be chosen according to the required tap number. In AWGN systems, can be optimized depending on the signal-to-noise ratio [33]. However, in the case of OOK-neighbor limited transmission, an optimization of did not yield significant improvements for the low tap numbers in contrast to . Inevitable cycle slips were mitigated using differential precoding of the phase-modulated signal. 

Standard implementations of the V&V algorithm, as used in [8], process each polarization independently and do not make use of the phase correlation between the two polarizations. The joint-polarization (JP) algorithm [34] is an extension of the standard V&V algorithm, making use of the correlated carrier phase information in both polarizations. In case that the carrier in both 



Fig. 16. Comparison of the JP and single-polarization V&V phase-recovery performance versus transmission distance for varying input power. 



Fig. 17. Performance versus coupling factor at 1900 km for various input powers per channel. 

polarizations is synchronous, e.g., when using the LMS algorithm for tracking in the equalizer, the phase offset information in the two polarizations can be simply superpositioned, as shown in Fig. 14. 

Note that the feedforward structure requires phase unwrapping, introducing feedback [31]. If, however, the equalization is performed using the CMA only, the carriers in the two polarizations are typically asynchronous, requiring feedback as shown in Fig. 15. 

Fig. 16 shows the performance of the JP phase recovery compared to V&V for the measurements as described in [8] with a 43-Gb/s PolMux-NRZ-QPSK channel and nine copolarized 10.7-Gb/s NRZ-OOK neighbors at arbitrary orientation to the QPSK channel on the 50-GHz ITU grid. Timing recovery and equalization were performed using methods introduced before. The LO phase and frequency offset was corrected using a PLL as outlined in Fig. 2 for LMS adaptation as in Fig. 14. CMA-only adaptation with a phase recovery as in Fig. 15 led to identical BER. The phase was averaged over three taps in each polarization, giving the best overall performance. 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

3621 

KUSCHNEROV _et al._ : DSP FOR COHERENT SINGLE-CARRIER RECEIVERS 

The performance gain is significant for input powers up to 4 dBm per channel and saturates due to high XPM at 2 dBm for the given transmission distances. Fig. 17 shows the influence of XPM on the optimum coupling factor that decreases for higher input power due to different nonlinear phase shifts in both polarizations [36]. 

The correlation of the phases in the two polarizations decreases with high XPM, and a near-optimum performance can be reached with a constant both for CMA and LMS implementations [34]. These improvements lead to a significant increase of the ASE noise tolerance, as demonstrated in [7]. 

### VII. CONCLUSION 

This contribution outlined the design of the key DSP algorithms for fiber optic coherent receivers. A blind stable dispersion estimation algorithm for arbitrarily large dispersion was presented in combination with frequency-domain equalization. The following timing recovery with prefiltering can be designed to tolerate any residual dispersion requirements, which is not possible using conventional algorithms, thus removing a critical bottleneck in receiver design. After the correction of the timing phase and frequency, the proposed equalization cost function can be used to derive polarization demultiplexing tolerant to PDL under worst case linear distortions and avoiding degenerate equalizer solutions. Finally, a JP version of the V&V algorithm for the carrier phase recovery was presented, further increasing the nonlinear tolerance in legacy channels with OOK-neighbors. 

### ACKNOWLEDGMENT 

The authors would like to thank D. van den Borne, T. Wuth, E.-D. Schmidt, T. Duthel, C. Fludger, F. Bondoux, and E. Gourdon for all the valuable discussions and their contribution to this work. 

### REFERENCES 

- [1] C. R. S. Fludger, T. Duthel, D. van den Borne, C. Schulien, E.-D. Schmidt, T. Wuth, J. Geyer, E. De Man, G.-D. Khoe, and H. de Waardt, “Coherent equalization and POLMUX-RZ-DQPSK for robust 100-GE transmission,” _J. Lightw. Technol._ , vol. 26, no. 1, pp. 64–72, Jan. 2008. 

- [2] S. J. Savory, G. Gavioli, R. I. Killey, and P. Bayvel, “Digital filters for coherent optical receivers,” _Opt. Exp._ , vol. 15, no. 5, pp. 2120–2126, 2007. 

- [3] H. Sun, K.-T. Wu, and K. Roberts, “Real-time measurements of a 40 Gb/s coherent system,” _Opt. Exp._ , vol. 16, no. 2, pp. 873–879, 2008. 

- [4] B. Lankl, J. A. Nossek, and G. Sebald, “Cross-polarization interference cancellation in the presence of delay effects,” in _Proc. Int. Conf. Commun._ , 1988, pp. 1355–1361. 

- [5] T. Duthel, C. R. S. Fludger, J. Geyer, and C. Schulien, “Impact of polarization-dependent loss on coherent POLMUX-NRZ-DQPSK,” in _Proc. Opt. Fiber Commun. Conf._ , San Diego, CA, 2008, OThU5. 

- [6] O. B. Pardo, J. Renaudier, H. Mardoyan, P. Tran, G. Charlet, and S. Bigo, “Investigation of design options for overlaying 40 Gb/s coherent PDM-QPSK channels over a 10 Gb/s system infrastructure,” in _Proc. Opt. Fiber Commun. Conf._ , San Diego, CA, 2008, OTuM5. 

- [7] T. J. Xia, G. Wellbrock, D. Peterson, W. Lee, M. Pollock, B. Basch, D. Chen, M. Freiberger, M. Alfiad, H. de Waardt, M. Kuschnerov, B. Lankl, T. Wuth, E. D. Schmidt, B. Spinnler, C. J. Weiske, E. de Man, C. Xie, D. van den Borne, M. Finkenzeller, S. Spaelter, M. Rehman, J. Behel, M. Chbat, and J. Stachowiak, “Multi-rate (111-Gb/s, 2 43-Gb/s, and 8 10.7-Gb/s) transmission at 50- GHz channel spacing over 1040-km field-deployed fiber,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, Th.2.E.2. 

- [8] D. van den Borne, C. R. S. Fludger, T. Duthel, T. Wuth, E.-D. Schmidt, C. Schulien, E. Gottwald, G. D. Khoe, and H. de Waardt, “Carrier phase estimation for coherent equalization of 43-Gb/s POLMUX-NRZ-DQPSK transmission with 10.7 Gb/s NRZ neighbors,” in _Proc. Eur. Conf. Opt. Commun._ , Berlin, Germany, 2007, We.7.2.3. 

- [9] T. Duthel, C. Fludger, C. Schulien, D. van den Borne, G.-D. Khoe, H. d. Waardt, E.-D. Schmidt, E. d. Man, and T. Wuth, “Impairment tolerance of 111 Gbit/s POLMUX-RZ-DQPSK using a reduced complexity coherent receiver with a T-spaced equaliser,” in _Proc. Eur. Conf. Opt. Commun._ , Berlin, Belgium, 2007, vol. 1, pp. 53–54. 

- [10] V. Curri, P. Poggiolini, A. Carena, and F. Forghieri, “Dispersion compensation and mitigation of nonlinear effects in 111-Gb/s WDM coherent PM-QPSK systems,” _IEEE Photon. Technol. Lett._ , vol. 20, no. 17, pp. 1473–1475, Sep. 2008. 

- [11] B. Spinnler, F. N. Hauske, and M. Kuschnerov, “Adaptive equalizer complexity in coherent optical receivers,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, We.2.E.4. 

- [12] B. Widrow and M. E. Hoff Jr., “Adaptive switching circuits,” _IRE WESCON Conv. Rec._ , pt. 4, pp. 96–104, 1960. 

- [13] G. Goldfarb and G. Li, “Chromatic dispersion compensation using digital IIR filtering with coherent detection,” _IEEE Photon. Technol. Lett._ , vol. 19, no. 13, pp. 969–971, Jul. 2007. 

- [14] M. Kuschnerov, F. N. Hauske, K. Piyawanno, B. Spinnler, A. Napoli, and B. Lankl, “Adaptive chromatic dispersion equalization for nondispersion managed coherent systems,” in _Proc. Opt. Fiber Commun. Conf._ , San Diego, CA, 2009, OMT1. 

- [15] D. N. Godard, “Self-recovering equalization and carrier tracking in two-dimensional data communication systems,” _IEEE Trans. Commun._ , vol. COM-28, no. 11, pp. 1867–1875, Nov. 1980. 

- [16] N. Benvenuto and G. Cherubini _, Algorithms for Communications Systems and their Applications_ . New York: Wiley, 2002. 

- [17] M. S. Alfiad, D. van den Borne, S. Jansen, T. Wuth, M. Kuschnerov, A. Napoli, and H. de Waardt, “Transmission of 11 111 Gb/s POLMUX-RZ-DQPSK over 2000 km of LEAF w/wo optical dispersion compensation,” in _Proc. Opt. Fiber Commun. Conf._ , San Diego, CA, 2009, OThR4. 

- [18] F. N. Hauske, J. Geyer, M. Kuschnerov, K. Piyawanno, B. Lankl, T. Duthel, C. R. S. Fludger, D. van den Borne, E.-D. Schmidt, and B. Spinnler, “Optical performance monitoring from FIR filter coefficients in coherent receivers,” in _Proc. Opt. Fiber Commun. Conf. 2008_ , San Diego, CA, Feb. 2008, OThW2. 

- [19] M. Oerder and H. Meyr, “Digital filter and square timing recovery,” _IEEE Trans. Commun._ , vol. COMM-36, no. 5, pp. 605–612, May 1988. 

- [20] F. M. Gardner, “A BPSK/QPSK timing-error detector for sampled receivers,” _IEEE Trans. Commun._ , vol. COMM-34, no. 5, pp. 423–429, May 1986. 

- [21] M. Kuschnerov, F. N. Hauske, K. Piyawanno, B. Spinnler, E.-D. Schmidt, and B. Lankl, “Joint equalization and timing recovery for coherent fiber optic receivers,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, Mo.3.D.3. 

- [22] L. Liu, Z. Tao, W. Yan, S. Oda, T. Hoshida, and J. C. Rasmussen, “Initial tap setup of constant modulus algorithm for polarization de-multiplexing in optical coherent receivers,” in _Proc. Opt. Fiber Commun. Conf._ , San Diego, CA, 2009, OMT2. 

- [23] M. El-Darawy, T. Pfau, C. Wördehoff, B. Koch, S. Hoffmann, R. Peveling, M. Porrmann, and R. Noé, “Real-time 40 krad/s polarization tracking with 6 dB PDL in digital synchronous polarization multiplexed QPSK receiver,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, We.3.E.4. 

- [24] H. Sun and K. T. Wu, “Equalization Strategy for Dual-Polarization Optical Transport System,” U.S. Patent 7,315,575 B2, 2008. 

- [25] C. Bontu, M. O’Sullivan, K. B. Roberts, H. Sun, and K. T. Wu, “Polarization compensation in a coherent optical receiver,” Int. Publ. Numb. WO 2007/045072 A1. 

- [26] S. J. Savory, “Digital filters for coherent optical receivers,” _Opt. Exp._ , vol. 16, no. 2, pp. 804–817, 2008. 

- [27] C. B. Papadias and A. Paulraj, “A space-time constant modulus algorithm for SDMA systems,” in _Proc. IEEE/VTS 46th Veh. Conf._ , Atlanta, GA, Apr. 1996, pp. 86–90. 

- [28] A. J. Paulraj and C. B. Papadias, “Space-time processing for wireless communications,” _IEEE Signal Process. Mag._ , vol. 14, no. 6, pp. 49–83, Nov. 1997. 

- [29] S. Haykin _, Unsupervised Adaptive Filtering_ . New York: Wiley, 2000, vol. 2, Blind Deconvolution. 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 

JOURNAL OF LIGHTWAVE TECHNOLOGY, VOL. 27, NO. 16, AUGUST 15, 2009 

3622 

- [30] H. Zhang, Z. Tao, L. Liu, S. Oda, T. Hoshida, and J. C. Rasmussen, “Polarization demultiplexing based on independent component analysis in optical coherent receivers,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, Mo.3.D.5. 

- [31] H. Meyr, M. Moeneclaey, and S. A. Fechtel _, Digital Communication Receivers_ . New York: Wiley, 1998. 

- [32] A. J. Viterbi and A. M. Viterbi, “Nonlinear estimation of PSK-modulated carrier phase with applications to burst digital transmission,” _IEEE Trans. Inf. Theory_ , vol. IT-29, no. 4, pp. 543–551, Jul. 1983. 

- [33] E. Ip and J. M. Kahn, “Feedforward carrier recovery for coherent optical communications,” _J. Lightwave Technol._ , vol. 25, no. 9, pp. 2675–2692, Sep. 2007. 

- [34] M. Kuschnerov, D. van den Borne, K. Piyawanno, F. N. Hauske, C. R. S. Fludger, T. Duthel, T. Wuth, J. C. Geyer, C. Schulien, B. Spinnler, E.-D. Schmidt, and B. Lankl, “Joint-polarization carrier phase estimation for XPM-limited coherent polarization-multiplexed QPSK transmission with OOK-neighbors,” in _Proc. Eur. Conf. Opt. Commun._ , Brussels, Belgium, 2008, Mo.4.D.2. 

- [35] X. Zhou, J. Yu, and P. Magill, “Cascaded two-modulus algorithm for blind polarization demultiplexing of 114-Gb/s PDM-8-QAM optical signals,” in _Proc. Opt. Fiber Commun. Conf. 2009_ , San Diego, CA, 2009, OWG3. 

- [36] G. P. Agrawal _, Nonlinear Fiber Optics_ . New York: Academic, 2001. 



**Maxim Kuschnerov** (S’05) was born in Kiev, Ukraine, in 1980. He received the Dipl.-Ing. degree in electrical engineering from the Technical University of Munich, Munich, Germany, in 2006. In 2004–2005, he was a visiting student at the City College of New York and graduated from the Center for Digital Technology and Management (CDTM), Munich, Germany, in 2004. In 2007 he joined the Institute for Communications Engineering of the University of the Federal Armed Forces, Munich, Germany, and is working towards the Ph.D. degree 

in cooperation with Nokia Siemens Networks. 

His research focuses on digital signal processing for optical transmission systems. 



**Fabian N. Hauske** (M’09) was born in Munich, Germany, in 1977. He received the Dipl.-Ing. degree in electrical engineering from the Munich University of Technology, Munich, Germany, in 2003. From 2000 to 2001, he was a visiting student at the University of Nottingham, U.K. Since 2003, he has been with the Institute for Communications Engineering, University of the Federal Armed Forces, Munich, working towards the Dr.-Ing. degree in collaboration with Nokia Siemens Networks GmbH & Co. KG. 

In 2003, he carried out research at the Fuijtsu Laboratories, Ltd., Kawasaki, Japan, within the scope of his diploma thesis. His fields of interest cover digital signal processing algorithms for equalization and optical performance monitoring for next generation optical transmission systems. 



**Kittipong Piyawanno** was born in Thailand in 1980. He received the Dipl.-Ing. degree in electrical engineering and information technology from the University of the Federal Armed Forces, Munich, Germany, in 2007, where he is currently working towards the Ph.D. degree in collaboration with Nokia Siemens Networks (previously Siemens AG), Munich, Germany. 

His focus is on digital carrier frequency and phase recovery with advanced modulation formats. 



**Bernhard Spinnler** was born in Erlangen, Germany, in 1968. He received the Dipl.-Ing. degree in communications engineering from the University of Erlangen-Nürnberg, Germany, in 1994 and the Dr.-Ing. degree with a thesis on noncoherent detection of continuous phase modulation in 1997. Since 1997, he worked on low-complexity modem design of wireless radio relay systems at Siemens AG, Information and Communication Networks. In 2002, he joined the optical networks group of Siemens Corporate Technology which later merged into Nokia Siemens Networks. There he is working on robust and tolerant design of optical communications systems. His interests focus on advanced modulation, forward error correction, and equalization. 



**Mohammad S. Alfiad** (SM’05) was born in Zarqa, Jordan, in 1982. He received the M.Sc. in broad band telecommunication (cum laude) from Eindhoven University of Technology, Eindhoven, The Netherlands, in 2007. His M.Sc. thesis research was conducted at Siemens AG, Munich, Germany. Currently, he is working towards the Ph.D. at the Eindhoven University of Technology in cooperation with Nokia Siemens Networks, Munich, Germany. 

His research focuses on digital signal processing and 100-Gb/s Ethernet for long-haul fiber-optic trans- 

mission systems. 



**Antonio Napoli** was born in Cossato, Italy, in 1974. He received the M.S. degree in electronics engineering and the Ph.D. degree with a dissertation on electronic equalization for advanced modulation formats from Politecnico di Torino, Torino, Italy, in 2002 and 2006, respectively. During his studies, he was a visiting student at the Technical University Wien, Universitat Politecnica de Catalunya, and University College London. In 2006, he joined the R&D of Siemens which later merged into Nokia Siemens Networks, where he is 

working on digital signal processing algorithms for optical communications systems. His interests cover the areas of digital signal processing, advanced modulation formats, forward error correction, and equalization. 



**Berthold Lankl** (M’82) was born in Tirschenreuth, Bavaria, in 1959. He received the Dipl.-Ing. degree in electrical engineering from the Technical University of Munich, Munich, Germany, in 1983 and the Dr.Ing. degree from the University of the Federal Armed Forces, Munich, Germany, in 1989. 

From 1983 to 2001, he worked at the Transmission Systems Division of Siemens AG, Munich, Germany, particularly in the development of radio relay systems. From 2001 to 2003, he was responsible for a research department in the field of optical communications. Since October 2003, he has been a Full Professor of Communications Engineering at the University of the Federal Armed Forces, Munich, Germany. Dr. Lankl is a member of Verband der Elektrotechnik, Elektronik und Informationstechnik e.V. (VDE) and Informationstechnische Gesellschaft im VDE (ITG). 

Authorized licensed use limited to: Eindhoven University of Technology. Downloaded on October 12, 2009 at 06:00 from IEEE Xplore.  Restrictions apply. 


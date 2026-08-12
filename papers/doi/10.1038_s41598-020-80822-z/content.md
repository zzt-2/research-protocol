www.nature.com/scientificreports 



# **OPEN Reduced sampling rate Kalman filters for carrier phase and frequency offset tracking in 200 Gbps 16 QAM coherent communication system** 

**Srishti Sharma**<sup>*</sup> **& Pradeep Kumar Krishnamurthy** 

**We propose 1 state and 2 state multi-step Kalman filters (MKFs) to estimate and compensate CFO, LPN and NLPN in long-haul coherent fiber-optic communication systems. The proposed filters generate state estimates once every** **_m_ symbols and therefore operate at a reduced sampling rate compared to conventional KFs that perform symbol by symbol processing. No computations are performed to obtain phase estimates of the intermediate** **_m_** − **1 samples; instead, the present and previous estimates are averaged and used to derotate the intermediate** **_m_** − **1 samples which are then demodulated to recover the transmitted symbols. This reduces the computational load on the receiver DSP. Further, in order to improve estimation accuracy, we adaptively vary the process noise covariance** **_Q_ . Simulation results of 200 Gbps PDM 16 QAM system over 12 spans shows that the proposed 1 state MKF can reduce the sampling rate requirement by a factor of** **_m_** = **20 with Q-factor degradation of 1.32 dB compared to single-step KF at linewidth of 100 kHz. The 2 state MKF tracks PN and CFO with a maximum step size of** **_m_** = **10 for a CFO of 100 MHz at linewidth of 100 kHz. We also study the dynamic performance of the proposed algorithms by applying step change to CFO. The 2 state MKF with adaptive** **_Q_ is able to track a step change of 400 MHz of CFO with** **_m_** = **1 and 3 with high estimation accuracy but slower convergence time compared to the non-adaptive 2 state MKF. Finally, we study the computational requirements of the proposed MKFs and show that they offer significant reduction in computations compared to single-step KF thus making the proposed filters suitable for hardware implementation.** 

Carrier synchronization is essential to demodulation of advanced modulation formats such as quadrature amplitude modulation (QAM) in high-data rate coherent optical communication  links<sup>1</sup> . By carrier synchronization we mean that the effects of carrier frequency offset (CFO) between transmitter laser and receiver local oscillator (LO) laser and phase noise (PN) due to lasers (both transmit and LO) and nonlinear phase noise arising out of the interaction of amplified spontaneous emission (ASE) noise and Kerr nonlinearity in the fiber are estimated and compensated by the receiver. CFO and PN cause the received constellation to rotate from its original position . thereby making it impossible to demodulate the received symbols correctly unless these effects are  compensated<sup>2</sup> . CFO is estimated by techniques such as time-domain differential phase method and blind frequency  search<sup>3–5</sup> Estimation techniques such as Viterbi-Viterbi method, blind phase search, Barycenter algorithm, and QPSK partitioning are used to estimate carrier phase after adapting them to the higher-order QAM  formats<sup>6–8</sup> . While these techniques maintain spectral efficiency of the transmission system as pilot symbols are not required for phase estimation, they are computationally expensive. Further, the phase estimation accuracy is limited by the quantization of test phases in BPS type algorithms which in turn limits the linewidth tolerance of the algorithm. The accuracy can be improved by employing additional stages and carrying out maximum likelihood phase estimation at the expense of increased computational complexity of the algorithm. Note that residual CFO affects the performance of the phase estimation algorithms. Once initial CFO and phase estimates are available, decision-directed feedback phase estimation can be advantageously employed for tracking residual CFO and 

Center for Laser and Photonics, Indian Institute of Technology Kanpur, Kanpur, Uttar Pradesh, India.<sup>*</sup> email: srishtis@iitk.ac.in 

**Scientific Reports** |         (2021) 11:1991 

| https://doi.org/10.1038/s41598-020-80822-z 

1 

www.nature.com/scientificreports/ 

phase  errors<sup>9,10</sup> . It is possible to combine both blind and feedback based techniques into a two-stage carrier recovery algorithm in which the coarse CFO is estimated first using blind CFO estimator and the residual CFO and PN are estimated using a feedback based algorithm in the second stage. However, this introduces additional computational load on the receiver DSP. 

It is also possible to perform joint estimation of CFO and PN instead of estimating them separately. Kalman filter (KF)<sup>11</sup> and its variants such as  extended<sup>2,12</sup> and unscented Kalman  filters<sup>13</sup> have been demonstrated for joint estimation of CFO and PN. While they are in general superior over blind carrier recovery algorithms, they suffer from high computational complexity as they typically perform symbol by symbol state estimation. Moreover, symbol by symbol processing requires many computations per state estimation which introduces high latency in processing the symbols. This, combined with the sampling rate constraints of the CMOS  ADCs<sup>8,14</sup> , makes it difficult to employ KFs in real-time processing. One method to overcome this problem is to employ block estimation techniques. Block  KF<sup>15</sup> and unscented KF  algorithms<sup>13</sup> have been proposed for joint estimation of CFO and carrier phase offset but do not perform well when laser and nonlinear phase noise is present in the received symbols. Moreover, these techniques are not studied for dynamic CFO estimation in which CFO changes suddenly to a new value during the transmission due to network issues. In this case, it is necessary that the carrier recovery algorithm converges to the correct value of CFO as quickly as possible which requires the study of tracking time of these algorithms. Finally, we note that the KF performance is sensitive to values of process noise covariance ( _Q_ ) and measurement noise covariance ( _R_ ). The estimation accuracy can be improved if _Q_ and _R_ can . be estimated either before filter begins operation or adaptively during the filter  operation<sup>16</sup> 

In this paper, we propose 1 state and 2 state multi-step Kalman filters (MKFs) for carrier recovery in 16 QAM 200 Gbps polarization division multiplexed coherent optical communication systems. In MKF, the state is updated once every _m_ symbols in contrast to symbol by symbol state update of a conventional Kalman filter. The m − 1 intermediate samples are discarded during phase estimation; instead they are derotated by the phase estimate obtained by averaging the current and previous MKF output. The derotated samples are then demodulated to recover the transmitted symbols. The 2 state MKF allows simultaneous estimation of CFO and phase noise which helps to lower the accuracy requirements of any CFO estimator that precedes MKF. We also show that the MKF algorithm requires only a few pilot symbols to track frequency and phase. In our simulations, only 20 pilot symbols were used in the training phase of the MKF algorithm. This does not affect the spectral efficiency of the transmission system as the training symbols is a negligible fraction of the total transmitted symbols. Further, we adaptively vary the process noise covariance _Q_ to improve the estimation accuracy of the MKF. Updating _m_ the filter equations every step significantly reduces the computational load on the receiver DSP and makes it possible to use KF techniques in practical implementation of carrier recovery for coherent communications. 

The rest of the paper is organized as follows. In “Principle of 1 and 2 state multi-step Kalman filters” section, we describe the 1 and 2 state MKFs with adaptive Q. In “System model” section, we describe the simulation model of 200 Gbps 16 QAM coherent optical link. In “Results and discussion” section, we study performance of proposed MKFs in terms of maximum step size for given CFO and PN, maximum linewidth tolerance, and tracking time of dynamic CFO. We study dynamic CFO tracking performance of the proposed filters and show that the tracking time depends on the locations at which the CFO changes during transmission. We show that the filter converges rapidly when CFO change occurs during the initial transmission of symbols compared to the change occurring during the later part of the transmission. In “Computational complexity of MKFs” section, we compute the computational efficiency of MKF. Finally, in “Conclusion” section, we conclude by summarizing our results. 

## **Principle of 1 and 2 state multi-step Kalman filters** 

Carrier synchronization in coherent optical communications involves estimation and tracking of both carrier frequency offset and phase noise of the lasers. In addition, during transmission, the symbols are affected by nonlinear phase which consists of average phase shift due to self phase modulation (SPM) and stochastic phase noise due to the interaction of ASE noise of the amplifiers and the Kerr nonlinearity of the fiber. sation on The _k_ th received sample after polarization mode dispersion (PMD) and chromatic dispersion (CD) compen-xˆ or yˆ polarizations is given by 



where �k = ωk + ψk<sup>PN</sup> + ψk<sup>SPM</sup> + ψk<sup>NLPN</sup> , sk is the transmitted complex symbol, ωk = 2πk�f is the phase error due to CFO ( �f ) of the local oscillator, ψk<sup>SPM</sup> = 2γ PinLeff Ns is the average phase due to SPM, ψk<sup>PN is phase</sup> rotation due to PN, ψk<sup>NLPN</sup> is phase due to NLPN, γ is fiber nonlinear coefficient, Pin is input launch power, Leff is effective length of the fiber and nk is ASE noise due to the inline optical amplifier which is modelled as zeromean Gaussian random variable. In Eq. (1) we have modeled laser phase noise as discrete-time Wiener process with ψk<sup>PN</sup> = ψk<sup>PN</sup> −1<sup>+ δψ</sup> k<sup>PN in which δψ</sup> k<sup>PN is the zero mean Gaussian random variable with variance 2π�νTs ,</sup> where �ν is the laser linewidth and Ts is the symbol  duration<sup>17</sup> . 

In the following subsections we propose a 1 state MKF to track and estimate only laser phase noise and a 2 state MKF to jointly track and estimate PN and CFO. 

**1 state MKF.** The state-space model of 1 state MKF to estimate phase �k is given by the following equations. 



**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

2 

www.nature.com/scientificreports/ 



**Figure 1.** Principle of multi-step Kalman filter algorithm. Here _m_ denotes the step size of the filter. 





The equations for error covariance estimate _P_ and Kalman gain _K_ are given by 





where _m_ is the step size (≥ 1) , _P_ is the error covariance, vk is zero mean Gaussian distributed noise of covariance _Q_ , and _R_ is the covariance of measurement noise. In the above equations superscript ‘ _p_ ’ indicates predicted value and ‘ _c_ ’ indicates corrected value. To initialise phase estimation, MKF is first operated in the data aided mode and then switched to the decision directed mode. 

Figure 1 shows operation of the MKF algorithm with step-size _m_ . The phase �k<sup>c is used to estimate the phase</sup> �<sup>c</sup> k+m<sup>using Kalman filter equations. The samples rk+1 , rk+2,..., rk+m−1 are derotated by the average of the phases</sup> �<sup>c</sup> k<sup>and �</sup> k<sup>c</sup> +m<sup>as shown in Fig. 1.</sup> 

**2 state MKF.** The state space model for 2 state MKF is given by 









**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

3 

www.nature.com/scientificreports/ 



(6h) 

where Kk is the Kalman gain, _A_ is state 2 × 2 transition matrix given by [1m; 01]<sup>T</sup> and Pk is error covariance matrix. Just like 1 state MKF, in the above equations also, the superscript ‘ _c_ ’ and ‘ _p_ ’ indicates corrected value and predicted value of the concerned variable. _Q_ and _R_ are the covariance matrix of process and measurement noise respectively. s1k = rke<sup>(−j�p)</sup> and s2k is obtained from s1k after decision. δ� and δω are the residual for the total phase error and the phase error due to CFO. In the non-adaptive versions of 1 state and 2 state MKFs, we keep the covariance matrices _Q_ and _R_ constant throughout the filter operation. 

**Adaptation of** **_Q_ .** In MKF, tracking capability and accuracy of the filter is sensitive to the value of the _Q_ matrix. A poor choice of _Q_ causes the filter to diverge thereby degrading its performance.  In<sup>16</sup> authors proposed an innovations based approach to adaptively change _Q_ during filter operation in order to increase accuracy of ˆ state estimation. The innovation vector is given by δrk = rk −ˆrk , where rk is the k<sup>th</sup> predicted symbol. In this paper we apply this approach to our 2 state MKF. Q<sup>ˆ</sup> k , the innovation based approach estimate of _Q_ at _k_ th symbol time can be calculated as given in Eq. (7). 



where _E_ [.] is the expectation operator. To solve Eq. (7), the expectation operator is approximated by the time average value of δrkδrk<sup>T</sup> .  In<sup>18</sup> , a forgetting factor β is proposed to obtain the average value of δrkδrk<sup>T</sup> over time. Therefore _Q_ in Eq. (6c) can be adapted with the symbol time giving Qk. 



The forgetting factor controls the performance of the filter in terms of convergence speed and estimation accuracy. 

## **System model** 

In this section we describe the simulation setup of 200 Gbps polarization division multiplexed (PDM) 16 QAM single-channel coherent communication system as shown in Fig. 2 to characterize the performance of the filters described in “Principle of 1 and 2 state multi-step Kalman filters” section. At the transmitter, two symbol sequences d1(k) and d2(k) of length 10,000 each are generated and are mapped onto a square 16 QAM constelcal I/Q modulator. A polarization beam combiner (PBC) is used to combine the modulated symbols of lation. These complex symbols are then passed to the rectangular pulse shaper. These rectangular pulses in electrical domain are then modulated onto the yˆ polarizations to form the complex data stream to be transmitted. The complex symbols are then transmitted xˆ and yˆ polarizations of optical carrier at 1550 nm using an opti-xˆ and over an optical fiber link consisting of Ns = 12 spans with each span comprising SSMF and inline optical amplifier to compensate for span losses. We model the propagation of the symbols by coupled nonlinear Schrodinger equation (CNLSE) which includes CD, PMD and SPM effects. In each span, fiber is divided into small sections and in each section CNLSE is numerically solved using split step Fourier method (SSFM). In order to model the effects of PMD, we consider each section of the fiber as a waveplate and using Jones matrix formalism we write the transmission matrix of the i<sup>th</sup> waveplate as given in Eq. (9). 



where � = ω�τi in which �τi is differential group delay (DGD) of i<sup>th</sup> waveplate and ω is the angular frequency. φ and θ are the elevation and azimuthal angle on the Poincare  sphere<sup>19</sup> . 

Each span consists of 80 km of SSMF giving a total of 960 km propagation. The SSMF parameters are: loss coefficient α = 0.2 dB/km, dispersion coefficient Ds = 17 ps/nm-km, Kerr nonlinear coefficient γ = 1.3/W/km and PMD coefficient Dp = 0.1 ps/ ~~√~~ km . Each span of fiber is divided into 40 waveplates which are simulated using an open source software  Optilux<sup>24</sup> and transmission of symbols through waveplates is governed by Eq. (9). An inline optical amplifier of gain and noise figure of 16 dB and 5 dB respectively compensates for the span losses and adds ASE noise power within 0.1 nm reference bandwidth. We set β = 0.88. 

At the receiver, xˆ and yˆ polarizations are separated using PBS which are then coherently demodulated using the local oscillator and coherent receiver. PMD and CD are jointly compensated using the vector form of digital back propagation (DBP). The resulting complex symbols are passed to MKF for further processing. Performance is analysed in terms of Q-factor, calculated using EVM method given by the following  equations<sup>20,21</sup> . 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

4 

www.nature.com/scientificreports/ 



**Figure 2.** Simulation setup for 200 Gbps 16 QAM coherent optical communication system. SMF, single mode fiber; OA, optical amplifier; ADC, analog to digital convertor; EDC, electronic dispersion compensation; PMDC, polarisation mode dispersion compensation. PBS and PBC, polarisation beam splitter and combiner; MKF, multi-step Kalman filter. 



**Figure 3.** Constellation diagrams of the received signal on xˆ -polarisation before and after 1 state MKF at Pin = 1 dBm, Ns = 12 spans, δν = 100 kHz. ( **a** ) PDM-16-QAM before 1 state MKF, ( **b** ) PDM-16-QAM after 1 state MKF for m = 1 , ( **c** ) m = 10 , ( **d** ) m = 20. 





## **Results and discussion** 

**Performance analysis of 1 state MKF.** In this section we discuss the performance of 1 and 2 state MKFs described in “Principle of 1 and 2 state multi-step Kalman filters” section. First we consider the 1 state MKF. For this, we set CFO to zero. Figure 3a shows the received constellation after CD and PMD compensation. The received symbols are processed by 1 state MKF to estimate and compensate phase noise. Figure 3b,c,d show the constellations of the received signal after 1 state MKF processing with m = 1, 10 and 20 respectively. We observe that after MKF processing the constellations return to their original positions apart from the spread of symbols due to ASE noise. 

Figure 4 shows the Q-factor curves as a function of launch powers for different step sizes of MKF. From Fig. 4 we can observe that for _m_ = 10 and 20 , the Q-factor penalty is 0.68 dB and 1.32 dB at 1 dBm launch power when compared to the linear step KF. Since CFO is zero, the cycle slip in phase tracking is reduced and hence the Q factor is high even for large values of step-size _m_ . This shows that phase can be estimated at the receiver using MKF with reduced sampling rate and a small penalty in the Q-factor value thus reducing the number of computations in comparison to the linear KF. For benchmark, we also compare the performance of 1 step MKF to the results of QPSK partitioning  scheme<sup>22</sup> . We see that MKF outperforms the QPSK partitioning method. At lower launch powers, the QPSK partitioning scheme performance is closer to MKF; however, at higher launch powers, MKF performs significantly better over the QPSK partitioning algorithm even for step size as large as m = 20 . Thus, when the CFO is already estimated, say, as part of a multistage carrier recovery algorithm the residual time-varying phase noise can be tracked with reduced computational requirements by employing MKF with large step sizes. 

Figure 5 shows the Q-factor variation with the number of spans to characterize long haul performance of the system. We calculated the Q-factor for various linewidths to determine the linewidth tolerance of the system under consideration. We found that for zero CFO, MKF shows a linewidth tolerance of 1 MHz before the performance deteriorates. Increasing the laser linewidth from 100 kHz to 1 MHz reduces Q-factor by ≈ 1.53 dB 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

5 

www.nature.com/scientificreports/ 



**Figure 4.** Q-factor versus launch power curve for 1 state MKF for �ν = 100 kHz and 12 spans for different step sizes. 



**Figure 5.** Q-factor versus no. of spans curve for 1 state MKF for �ν = 100 kHz and launch power of 1 dBm. For reference, Q-factor corresponding to the BER of 10<sup>−3</sup> is shown. 

at launch power of 1 dBm. We see that performance of 1 state MKF is better than QPSK partitioning scheme over 40 spans. 

**Performance analysis of 2 state MKF.** Figure 6a shows the received constellation after CD and PMD compensation. This is then processed by the 2 state MKF for phase noise and CFO estimation and compensation. Figure 6b,c,d show the constellations of the received signal after 2 state MKF processing with m = 1, 5 and 10 respectively. We note that increasing the value of _m_ increases the distortion in constellations . However, the constellation and the resulting BER is within the FEC limit for _m_ as large as 10. 

Figure 7 shows the Q-factor versus launch power curve for three different CFO values and for three different step sizes for δν = 100 kHz. We see that for m = 1 , Q factor for CFO of 100 MHz and 1 GHz overlap each other indicating the suitability of 2 state MKF for estimation and tracking of CFO and phase noise. For m = 3 and 5, 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

6 

www.nature.com/scientificreports/ 



**Figure 6.** Constellation diagrams of the received signal on xˆ-polarisation before and after 2 state MKF at Pin = 0 dBm, Ns = 12 spans, �ν = 100 kHz. ( **a** ) PDM-16-QAM before 2 state MKF, ( **b** ) PDM-16-QAM after 2 state MKF for m = 1 ( **c** ) m = 5 , ( **d** ) m = 10. 



**Figure 7.** Q-factor versus launch power curve for 2 state MKF for �ν = 100 kHz and 12 spans for different CFO values and step sizes ( _m_ ). 

and CFO of 100 MHz, the performance of the 2 state MKF reduces compared to m = 1 case. However, the Q factor still remains significantly higher than the FEC limit as shown in Fig. 7. However at higher launch powers ( > 2 dBm) MKF with m = 5 does not track CFO and phase noise as the deviation in the total actual phase and estimated phase increases due to CFO and NLPN. 

Figure 8 shows the long haul performance of the 2 state MKF for 100 MHz at m = 1 and 5 and for CFO = 1 GHz at m = 1 . At CFO as high as 1 GHz the proposed system can be operated upto 20 × 80 km. For CFO = 100 MHz the linear KF can go upto 30 spans but as we increase the step size the Q-factor values drops and the span over which data can be transmitted reduces. It can be attributed to the fact that the increase in step size decreases the symbol rate which in turn increases the overall phase rotation due to CFO. 

Figure 9 shows the Q-factor values achieved for the various step sizes and various frequency offsets for 100 kHz laser linewidth. From the figure, we see that 2 state MKF with m = 1 performs better than the other values of _m_ for CFO in the range of 100 MHz to 1 GHz. For 100 MHz frequency offset step size upto 10 can be achieved with approximately 2.5 dB degradation in Q-factor value. We next varied the CFO from 100 MHz to 1.2 GHz. As seen from Fig. 9, for CFO > 1 GHz only m = 1 can be achieved. 

Figure 10 summarises the maximum step size _m_ that can be achieved for the frequency offsets in the range 100 MHz to 1 GHz. For CFO ≤ 1 GHz, m is greater than 1, i.e. allowing the carrier recovery with reduced numm = 10 can ber of samples thereby increasing the computational efficiency. For 100 MHz CFO, step size up to be achieved. 

Figure 11 shows Q-factor versus launch power curve for 2 state MKF for three different values of m and Ns = 3 spans. The results are compared with the block estimation based Kalman filter for carrier  recovery<sup>15</sup> . For the system model proposed in Fig. 2 we simulated the block based Kalman filter for laser linewidth of 1 kHz and CFO of 100 MHz. Filter proposed  in<sup>15</sup> can track low laser linewidths and can reach the transmission distance 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

7 

www.nature.com/scientificreports/ 



**Figure 8.** Q-factor versus no. of spans curve for 2 state MKF for �ν = 100 kHz and launch power of 1 dBm. 



**Figure 9.** Q-factor versus step size of 2 state MKF for �ν = 100 kHz and different frequency offsets for Pin = 0 dBm. For reference, Q-factor corresponding to 10<sup>−3</sup> BER is shown. 

of 320 km. On the contrary, the proposed 2 state Kalman filter can track laser linewidths upto 100 kHz over the transmission distance of 960 km. 

**Dynamic frequency estimation.** Figure 12 shows the tracking capability of the 2 state MKF with adaptive _Q_ for the dynamic frequency offset case with m = 1 and 3 compared with the 2 state MKF with constant _Q_ over 12 span transmission link. The conventional MKF shows quick convergence but its accuracy is poor. On the other hand, the tracking capability of the MKF with adaptive _Q_ is comparatively low but its estimation accuracy is better. This result is in agreement to the performance of the adaptive Kalman filter (AKF) proposed in<sup>18</sup> for B2B system. Poor tracking capability of the filter can be attributed to the choice of β . A small value of β reduces the convergence speed and the filter exhibits sluggish response in case of suddenly changing frequency offsets. On the other hand, larger values of β gives rapid convergence but causes large dependence of _Q_ on the innovation vector which can cause the filter to diverge. For m = 3 system shows degradation in the tracking of 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

8 

www.nature.com/scientificreports/ 



**Figure 10.** Maximum achievable step size for various frequency offsets for 2 state MKF. 



**Figure 11.** Q-factor versus launch power curve for 2 state MKF for CFO = 100 MHz and 3 spans. For 2 state MKF �ν = 100 kHz, For block estimation of KF �ν = 1 kHz. 

frequency offset. This degradation can be reduced by detecting the symbols which are affected and then applying the cycle slip mitigation  techniques<sup>23</sup> . 

This dynamic behaviour in CFO is modeled as a step change in CFO by 0.5 GHz. We denote the step change in CFO during the initial part of transmission by step I and by step II, the step change in CFO during the later part of transmission. This allows us to bring out the effect of accumulated residual phase and frequency errors on the tracking ability for step change in CFO as described next. Exponential curve fit is done for step I and step II in Fig. 12 and rise time and fall times are computed. Rise time ( tr ) is defined as number of symbols required to go from 100 MHz to 95% of 500 MHz and fall time ( tf ) as 500 MHz to 95% of 100 MHz. Rise times and fall times for step m = 1 and 3 are tabulated in Table 1. From the values in Table 1, we can conclude that the tracking of CFO for step I is better than step II. This can be attributed to the fact that the rotation of constellation points at the step II symbol range is greater than step I symbol range thereby affecting the rise and fall of CFO with respect to the symbols hence affecting the convergence time. The proposed scheme shows the degradation in tracking of CFO for m = 3 compared to 1. But this degradation can be reduced by considering the final value of CFO after transition and then again applying the phase recovery scheme to all the symbols under transition. 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

9 

www.nature.com/scientificreports/ 



**Figure 12.** Tracked CFO by 2 state MKF with constant _Q_ and adaptive _Q_ for ( **a** ) m = 1 and ( **b** ) m = 3. 



<!-- Start of picture text -->
Step size  Step size<br>Step no. (m = 1) (m = 3)<br>(tr) (tf ) (tr) (tf )<br>Step I 140 277 112 376<br>Step II 415 539 486 523<br><!-- End of picture text -->

**Table 1.** Rise times and fall times for step change in CFO. 

|**Operation**|**1 state MKF**|**2 state MKF**|
|---|---|---|
|State prediction|1 RA|3 RA, 1 RM|
|Error covariance prediction|1 RA|2 MM, 1 MA|
|Kalman gain update|1 RA, 1 RM|1 MA, 3 MM, 1 MI|
|Error covariance update|1 RA, 2 RM|1 MA, 2MM|
|Measurement update|1 CM, 1 RM, 2 RA, 1 LUT|1 CM, 8 RM, 1 MA, 2 MM, 2 LUT|
|Averaging|1 RA|1 RA|
|CPE correction|1 CM|1 CM|



**Table 2.** Computational complexity for 1 state and 2 state MKF. RA, real addition; RM, real multiplication; MM, matrix Multiplication; MA, matrix addition; MI matrix inversion; CM complex multiplication; LUT lookup table. 

## **Computational complexity of MKFs** 

In this section, we analyze the computational complexity of the proposed 1 state and 2 state MKFs in terms of total number of real additions, real multiplicaions and lookup tables (LUTs) required for implementation of the algorithm. Each real addition (RA) requires a real adder and real multiplication (RM) requires a real multiplier. We take RA, RM, and LUT as one unit of operation. The following rules govern the total number of real additions and real multiplications required for each operation. 

1. Each matrix addition requires 4 RAs. 

2. Each matrix inversion requires 6 RMs and 1 RA. 

3. Each matrix multiplication requires 4 RAs and 8 RMs. 

4. Each complex multiplication requires 3 RAs and 4 RMs. 

5. The arg(), tan<sup>−1</sup> () operations requires a LUT. 

The number of operations of 1 state and 2 state filters for each iteration are summarized in Table 2. From the entries in Table 2 and the rules given above we find that the 1 state MKF requires a total of 13 RAs, 12 RMs and 1 LUT. Similarly, the 2 state MKF requires a total of 66 RAs, 97 RMs and 2 LUTs. 

The MKF reduces the computational complexity in comparison to the single-step Kalman filters by reducing the total number of computations by the factor of _m_ : 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

10 

www.nature.com/scientificreports/ 

1 −<sup>1</sup> � m � (11) 

### Reduction in no. of computations = Number of computations × Total number of symbols × 

For example, the 2 state MKF with m = 5 for 10,000 transmitted symbols, reduction in RMs= 97 × 10, 000 × �1 −<sup><u>1</u></sup> 5 � = 776000 compared with single-step KF. 

## **Conclusion** 

In this paper, we proposed 1 state and 2 state MKF for carrier tracking and estimation with reduced sampling rate requirements in 200 Gbps 16 QAM coherent transmission system and verified its performance with numerical simulations. Simulations are carried for long haul system (960 km) taking CD, PMD and nonlinearity in account. 1 state MKF is concerned with tracking for PN and NLPN. Simulation results show that MKF with _m_ upto 20 can be used with ≤ 1.5 dB loss and results are found to perform better than QPSK partioning scheme. Also, maximum laser linewidth tolerance limit of the proposed 1 state MKF is found to be 1 MHz. 2 state MKF is concerned with joint mitigation of PN, NLPN, and CFO upto 1 GHz for m ≥ 1 . Proposed algorithm outperforms block based estimation using Kalman filter in terms of Q-factor values and number of spans transmission. Also, 2 state MKF was adapted in terms of _Q_ so as to improve the estimation accuracy of CFO and results are found in agreement to the adaptive Kalman filter proposed in literature. Tracking performance for dynamic CFO was analysed for 2 state MKF, it was observed that 2 state MKF gives reduced jitter with adaptive _Q_ in comparison to constant _Q_ . Finally, we studied the computational complexity of the proposed 1 and 2 state MKF and computed the reduction in computations with slight degradation in performance. Our proposed filters use the linear Kalman filter resulting in significant computational advantage compared to nonlinear Kalman filters such as EKF and UKF thus making it suitable for joint mitigation of PN, NLPN, and CFO in high-rate high-modulation order coherent communication systems. 

Received: 14 September 2020; Accepted: 28 December 2020 



## **References** 

1. Ip, E., Lau, A. P. T., Barros, D. J. & Kahn, J. M. Coherent detection in optical fiber systems. _Opt. Express_ **16** , 753–791 (2008). 2. Li, L. _et al._ A joint recovery scheme for carrier frequency offset and carrier phase noise using extended Kalman filter. _Opt. Fiber Technol._ **36** , 438–446 (2017). 

3. Leven, A., Kaneda, N., Koc, U. V. & Chen, Y. K. Frequency estimation in intradyne reception. _IEEE Photon. Technol. Lett._ **19** , 366–368 (2007). 

4. Hoffmann, S. _et al._ Frequency and phase estimation for coherent QPSK transmission with unlocked DFB lasers. _IEEE Photon. Technol. Lett._ **20** , 1569–1571 (2008). 

5. Zhou, X. _et al._ 64-Tb/s, 8 b/s/Hz, PDM-36QAM transmission over 320 km using both pre- and post-transmission digital signal processing. _J. Lightw. Technol._ **29** , 571–577 (2011). 

6. Dris, S. et al. M-QAM carrier phase recovery using the viterbiviterbi monomial-based and maximum Likelihood Estimators. In _2013 Optical Fiber Communication Conference and Exposition and the National Fiber Optic Engineers Conference (OFC/NFOEC)_ , 1–3 (IEEE, 2013). 

7. Wang, Y., Serpedin, E. & Ciblat, P. Optimal blind carrier recovery for MPSK burst transmissions. _IEEE Trans. Commun._ **51** , 1571–1581 (2003). 

8. Faruk, M. S. & Savory, S. J. Digital signal processing for coherent transceivers employing multilevel formats. _J. Lightwave Technol._ **35** , 1125–1141 (2017). 

9. Benani, A. M. & Gagnon, F. Comparison of carrier recovery techniques in M-QAM digital communication systems. In _2000 Canadian Conference on Electrical and Computer Engineering. Conference Proceedings_ , 73–77. vol. 1 (2000). 

10. Barry, J. R. & Kahn, J. M. Carrier synchronization for homodyne and heterodyne detection of optical quadriphase-shift keying. _J. Lightwave Technol._ **10** , 1939–1951 (1992). 

11. Jain, A. & Krishnamurthy, P. K. Phase noise tracking and compensation in coherent optical systems using Kalman filter. _IEEE Commun. Lett._ **20** , 1072–1075 (2016). 

12. Jain, A., Krishnamurthy, P. K., Landais, P. & Anandarajah, P. M. EKF for joint mitigation of phase noise, frequency offset and nonlinearity in 400 Gb/s PM-16-QAM and 200 Gb/s PM-QPSK systems. _IEEE Photonics J._ **9** , 1–10 (2017). 

13. Jignesh, J., Corcoran, B. & Lowery, A. Parallelized unscented Kalman filters for carrier recovery in coherent optical communication. _Opt. Lett._ **41** , 3253–3256 (2016). 

14. Pfau, T. et al. Towards real-time implementation of coherent optical communication. _2009 Conference on Optical Fiber Communication_ , 1–3 (2009). 

15. Inoue, T. & Namiki, S. Carrier recovery for M-QAM signals based on a block estimation process with Kalman filter. _Opt. Express_ **22** , 15376–15387 (2014). 

16. Akhlaghi, S., Zhou, N. & Huang, Z. Adaptive adjustment of noise covariance in Kalman filter for dynamic state estimation. _2017 IEEE Power & Energy Society General Meeting_ , 1–5 (2017). 

17. Seimetz, M. _Transmitter design in high-order modulation for optical fiber transmission_ Vol. 143, 14–16 (Springer, Berlin, 2009). 18. Xiang, Q., Yang, Y., Zhang, Q., Cao, J. & Yao, Y. Adaptive and joint frequency offset and carrier phase estimation based on Kalman filter for 16 QAM signals. _Opt. Commun._ **430** , 336–341 (2019). 

19. Zhou, X. & Xie, C. _Polarization and Nonlinear Impairments in Fiber Communication Systems in Enabling Technologies for High Spectral-Efficiency Coherent Optical Communication Networks_ 201–210 (Wiley, Hoboken, 2016). 

20. Zhang, F. _et al._ Experimental comparison of different BER estimation methods for coherent optical QPSK transmission systems. _IEEE Photonics Technol. Lett._ **23** , 1343–1345 (2011). 

21. Schmogrow, R. _et al._ Error vector magnitude as a performance measure for advanced modulation formats. _IEEE Photonics Technol. Lett._ **24** , 61–63 (2012). 

22. Fatadin, I., Ives, D. & Savory, S. J. Laser linewidth tolerance for 16-QAM coherent optical systems using QPSK partitioning. _IEEE Photonics Technol. Lett._ **22** , 631–633 (2010). 

23. Taylor, M. G. Phase estimation methods for optical coherent detection using digital signal processing. _J. Lightwave Technol._ **27** , 901–914 (2009). 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

11 

www.nature.com/scientificreports/ 

24. Serena, P., Bertolini, M. & Vannucci, A. Optilux toolbox. Available at optilux.sourceforge.net/Documentation/optilux-doc.pdf (2009). 

## **Author contributions** 

Both S.S. and P.K. did the theoretical analysis. S.S. simulated the system and P.K. analysed the results. Both authors reviewed the manuscript. 

## **Competing interests** 

The authors declare no competing interests. 

## **Additional information** 

**Correspondence** and requests for materials should be addressed to S.S. 

**Reprints and permissions information** is available at www.nature.com/reprints. 

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

**Open Access** This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creat iveco mmons .org/licen ses/by/4.0/. 

© The Author(s) 2021 

**Scientific Reports** |         (2021) 11:1991  | 

https://doi.org/10.1038/s41598-020-80822-z 

12 


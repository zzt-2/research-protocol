**Adaptive Rate/Power Control With ML-Based Channel Prediction for Optical Satellite Systems** 

## Correspondence 

**Free-space optical (FSO)-based satellite communications, due to extremely high data rates and global coverage capability, have recently drawn substantial research attention. The adverse issues on FSObased satellite links, including atmospheric turbulence and pointing error, pose various challenges in designing and deploying such systems. Nevertheless, recent efforts in error control design focusing on adaptation-based mitigation techniques face practical restrictions due to the outdated feedback channel state information (CSI) caused by long-distance/high-latency satellite links. This article addresses the design of an adaptive rate/power control scheme using machine learning (ML)-aided channel prediction for FSO-based satellite systems. Notably, we employ the echo state network (ESN) model, an efficient form of recurrent neural network, for channel prediction. The design proposal facilitates the concurrent control of data rate and satellite’s transmitted power for each equal-duration channel state, leveraging accurately predicted CSI. The average required transmitted power and energy efficiency performance metrics are analytically derived. Numerical results demonstrate the severe impact of outdated CSI on the performance of FSO-based satellite systems and highlight the necessity of our design proposal. Moreover, we confirm the effectiveness of the ESN model for FSO channel prediction by comparing its performance with other ML approaches in terms of predicted accuracy and complexity.** 

## I. INTRODUCTION 

Recent years have witnessed the growing trend to provide Internet services from low earth orbit (LEO) satellites [1]. The revolutionary impact of thousands of LEO satellites in projects, such as SpaceX’s Starlink, Amazon’s Kuiper, Telesat, and OneWeb, has triggered a surge in global mega satellite-constellation development [2]. On the other hand, free-space optical (FSO) communication has gained renown for providing high-speed data services over long distances without depleting radio frequency (RF) resources [3]. Leveraging the recent progress in satelliteaccess Internet and full-fledged hardware facilitating FSO technology, FSO-based LEO satellite communication has emerged as a potential solution for diverse applications, e.g., vertical fronthaul/backhaul networks, last-mile access 

Manuscript received 8 August 2023; revised 1 January 2024 and 19 April 2024; accepted 16 May 2024. Date of publication 21 May 2024; date of current version 11 October 2024. 

DOI. No. 10.1109/TAES.2024.3403809 

Refereeing of this contribution was handled by Mohamed S. Alouini. 

This work was supported by the Japan Society for the Promotion of Science Grants-in-Aid for Scientific Research under Grant 21K11870 and Grant 23K19124. 

Authors’ address: Tinh V. Nguyen, Hoang D. Le, and Anh T. Pham are with the School of Computer Science and Engineering, University of Aizu, Aizuwakamatsu 965-8580, Japan, E-mail: (tinh.nv310300@gmail.com;hoangle@u-aizu.ac.jp;pham@u-aizu.ac.jp). _(Corresponding author: Hoang D. Le)_ . 

0018-9251 © 2024 IEEE 

IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS VOL. 60, NO. 5 OCTOBER 2024 

7498 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

of the Internet of Vehicles (IoV), and quantum key distributions [4]. However, the impact of atmospheric turbulence and pointing errors on FSO links significantly degrades system performance, necessitating extensive research efforts [5]. 

_Related works:_ Extensive research endeavors have been steered to discover efficient mitigation techniques for FSObased LEO satellite systems [3]. These studies primarily focused on: 1) physical-layer (PHY) solutions, e.g., hybrid FSO/RF scheme [5], adaptive transmission [6], and intelligent-reflecting-surface-aided relays [7], and 2) linklayer solutions, e.g., hybrid automatic repeat request [8]. A promising and viable approach to further improve the system performance is the joint design between the adaptive transmission scheme with other mitigation techniques, which has recently gained considerable attention [4], [6], [7], [8]. Using the adaptive transmission scheme, the transmitter adaptively selects the appropriate PHY parameters, such as data rate, coding rate, and transmitted power, to maintain the quality of service (QoS) requirements over time-varying turbulence channels [9], [10], [11], [12], [13], [14]. Notably, Perlot and de Cola [9] investigated the throughput performance of optical LEO satellite-to-ground systems using adaptive rate transmissions. Spellmeyer et al. [10] analyzed the performance of multirate differential phase-shift keying schemes for optical satellite systems. The performance of optical LEO satellite systems using adaptive pulse position modulation was investigated in [11]. Geisler et al. [12] conducted an experiment to demonstrate the feasibility of employing adaptive modulation (AM) and coding rate schemes for coherent optical LEO satellite systems. German researchers presented the implementation of adaptive rate schemes, where LEO satellites adjust the data rate according to elevation and channel conditions [13]. Most recently, the novel architecture to implement variable data rate schemes in the hardware efficiently was introduced in [14].Inthiswork,theauthorsaimedtoachievethehighest symbol rate allowed by the link budget in each sector of the satellite pass by repeating/spreading the data symbols while keeping the targeted chip rate. 

_Motivation:_ Existing works on FSO-based LEO satellite systems using adaptive transmission schemes also leave some open challenges and issues for future research. _First_ , the aforementioned studies primarily focused on the design of data rate adaptation based on a fixed transmitted power selected for the worst case channel conditions. Using a constant transmitted power over time-varying turbulence channels leads to low achievable energy efficiency, which is especially critical for satellite communications. Rate adaptation in conjunction with transmitted power control can take advantage of favorable channel conditions, resulting in considerable enhancement in energy efficiency without sacrificing the desired QoS, e.g., targeted bit error rate (BER) [15]. It is worth noting that the design of joint rate and power adaptation has been extensively investigated for FSO-based terrestrial systems [16], [17], [18]. In these studies, the transmitted power was adjusted in the order of bit duration to strictly maintain the targeted BER. This, 

TABLE I 

Literature Comparison on Optical LEO Satellite Systems Using Adaptive Transmission Schemes 

**==> picture [227 x 70] intentionally omitted <==**

nonetheless, poses challenges in practical systems due to feedback delays and hardware limitations, particularly in long-distance satellite communications. Therefore, a proper adaptive rate/power control design for optical LEO satellite systems is required. 

_Regarding the second concern_ , the existing design of adaptive transmission schemes for FSO-based LEO satellite systems was based on the assumption of perfect channel state information (CSI). In practice, the CSI tends to be outdated, especially in optical satellite systems. Unlike FSO-based terrestrial systems,[1] this issue becomes critical due to inherent high feedback latency in long-distance LEO satellite communications, i.e., a few milliseconds. This delay is much longer than the LEO satellite channel coherence time, which is typically shorter than 1 ms, as reported in [22]. Such outdated CSI, indeed, substantially deteriorates the performance of optical satellite systems using adaptive transmission schemes [23]. Therefore, it becomes crucial and imperative to devise an efficient channel prediction for accurately acquiring the up-to-date CSI over time-varying FSO channels. Our initial report in [24] confirmed the effectiveness of machine learning (ML)-based echo state network (ESN) for FSO channel prediction. The ESN model, an efficient recurrent neural network (RNN), constructs random recurrent connections within its hidden layer and utilizes a straightforward linear regression algorithm for training the output layer [25]. This model overcomes the limitations of traditional RNNs, i.e., elevated computational complexity and slow convergence, making it a potential candidate for channel prediction [26]. To our knowledge, the design of adaptive rate/power control with ML-based channel prediction is not available in the literature on FSO-based LEO satellite systems. 

_Contributions:_ The primary objective of this article is to present the efficient design of adaptive rate/power control with ML-based channel prediction for FSO-based LEO satellite-assisted vehicular networks. A comparison between our study and the literature is depicted in Table I. In summary, the key contributions of this article are outlined as follows. 

1In FSO-based terrestrial systems, the impact of outdated CSI is not significant. This is because the link distance is a few kilometers, in which the delay ofCSIestimation based on thefeedback channelisshortenough [19], [20]. On the other hand, thanks to the terrestrial channel reciprocal characteristics, the CSI can be estimated for transmitting channels using the received CSI [21]. 

CORRESPONDENCE 

7499 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [223 x 219] intentionally omitted <==**

Fig. 1. FSO-based satellite-to-UAV system block diagram. 

- _C_ 1: It is a design of an efficient adaptive modulation and power (AMP) control scheme for FSO-based LEO satellitesystems.Particularly,weintroducethesuboptimal adaptive modulation and power (SAMP) scheme, enabling the LEO satellite to adjust the rate and power in the fixed equal-time slots. The design proposal guarantees a targeted achievable rate requested by the user while minimizing power consumption. 

- _C_ 2: Unlike the single-output ESN channel prediction model reported in [24] and [26], we present a multistep-prediction ESN, where the predicted CSI effectively overcomes the induced feedback delay. Moreover, a comprehensive comparison with stateof-the-art ML-based channel prediction models in terms of accuracy, computational time, and energy efficiency performance is also included. 

- _C_ 3: We provide insightful numerical results into the detailed impacts of turbulence channel conditions andtheoutdatedCSIontheperformanceofourproposed rate/power adaptation system. In addition, we conduct the simulations to verify the correctness of the model and analysis. 

The rest of this article is organized as follows. The system and channel models are described in Section II. Section III presents our proposed adaptive rate with a power control scheme and derives performance metrics, including average transmitted power and energy efficiency. Numerous numerical results and discussions are given in Section IV. Finally, Section V concludes this article. 

## II. SYSTEM AND CHANNEL MODELS 

## A. System Description 

Fig. 1 illustrates an FSO transmission from an LEO satellite to an unmanned aerial vehicle (UAV), e.g., for vertical backhaul solutions or IoV applications. A joint 

power and rate adaptation scheme is employed at the PHY layer. This aims to satisfy a specific data rate demand from the UAV with minimum power consumption under various practical constraints. For the adaptive rate transmission, we adopt the subcarrier _K_ -ary quadrature amplitude modulation ( _K_ -QAM) scheme with a fixed symbol rate of _Rs_ for _M_ possible transmission modes. The transmission bit rate varies for each transmission mode and is given as _Rb_ = _Rs_ log2( _K_ ) (bits/s), where _K_ is the constellation size. Let _**h**_ **[∗]** = { _h_ 1[∗] _[<][ h]_ 2[∗] _[<]_[ · · ·] _[ <][ h] M_[∗] _[<][ h] M_[∗] +1[=][ ∞}][ be the] switching thresholds for _M_ different transmission modes, _**h**_ = { _h_ 1 _< h_ 2 _<_ · · · _< hN < hN_ +1 = ∞} be the switching thresholds for _N_ channel states, and _h_ is the instantaneous channel gain, i.e., the CSI. The _i_ th transmission mode is selected if _hi_[∗][≤] _[h][ <][ h] i_[∗] +1[, and the current channel is said to] be in the _j_ th state if _h j_ ≤ _h < h j_ +1, where _i_ ∈{1 _,_ 2 _, . . ., M_ } and _j_ ∈{1 _,_ 2 _, . . ., N_ }. To avoid a high BER, the system falls into outage mode (no transmission) when the channel is in bad condition, i.e., _h < h_ 1 = _h_ 1[∗][. The selection of the trans-] mission mode thresholds _**h**_ **[∗]** and channel state thresholds _**h**_ can be found in Section III. 

On the other hand, the data bursts are transmitted in the equal duration of channel states. Each channel state is designed to cover a data burst transmission, in which its duration, denoted as _Tb_ , is chosen to be shorter than the channel coherence time. This guarantees that the channel remains stable during a transmission. Here, both data rate and transmitted power are changed for each channel state using different transmission modes. At the UAV-based receiver side,[2] we employ an ESN-based prediction model whose purpose is to forecast the future CSI from several historical values. It is then fed back to the LEO satellite’s transmitter. Based on this predicted CSI, the adaptive transmission controller decides the proper channel state and transmission mode of the system. It sends a control signal to the QAM modulator and the erbium-doped fiber amplifier (EDFA)[3] to select the proper constellation size and amplifier gain for the subsequent burst transmission. 

## B. FSO Channel Model 

For the FSO link between the LEO satellite and the UAV, we consider three major impairments,[4] i.e., atmospheric attenuation _h_ l, atmospheric turbulence _ha_ , and pointing 

2The CSI is estimated at the UAV, which is then fed back to the satellite via feedback links, which could be an FSO or RF link. In FSO-based LEO satellite systems, the feedback delay (a few milliseconds) is much longer than the channel coherence time (typically shorter than 1 ms), leading to the outdated CSI [22]. Here, the imperfect CSI due to other sources, e.g., channel estimation and quantization errors, is beyond the scope of this study and can be further investigated in our future work. 3The typical time scale needed for changing EDFA gains is in the order of tens up to hundreds of microseconds [27], [28]. These values are, nevertheless, much smaller than the channel coherence time and the considered time slot (orders of milliseconds). Therefore, the EDFA delay does not have a significant impact on our considered system and thus can be ignored. 4As reported in [29, Sec. 2.1], the Doppler effect can be ignored as its maximum value is within the capability of the current receiver design for FSO-based satellite systems. 

7500 

IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS VOL. 60, NO. 5 OCTOBER 2024 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

error _h_ p. The composite channel coefficient is expressed as _h_ = _hah_ l _h_ p. 

1) _Atmospheric Attenuation and Turbulence:_ The molecular absorption and aerosol scattering suspended in the air significantly decrease received signal power. This is described by the Beer–Lambert law as _h_ l = exp (− _σ_ ( _Ha_ − _H_ U)sec( _ξ_ )), where _σ_ is the attenuation coefficient related to the visibility _V_ , while _Ha, H_ U, and _ξ_ are the atmospheric altitude, UAV’s altitude, and zenith angle, respectively [29, eq. (3)]. 

On the other hand, the atmospheric turbulence phenomenon causes the scintillation effect, resulting in signal power fluctuations at the UAV’s detector. The UAVs considered in this article are drones, which operate within 1 km of the earth’s surface. As a result, the turbulence strength for the LEO satellite-to-UAV optical links is usually weak [29]. The intensity fluctuations can be well described by a lognormal model, i.e., [8, eq. (6)] 

**==> picture [227 x 31] intentionally omitted <==**

where _σ_ R[2][is the Rytov variance determined as [][4][, eq. (15)]] 

**==> picture [229 x 27] intentionally omitted <==**

where _k_ wave = 2 _π/λ_ istheopticalwavenumbercorresponding to the optical wavelength _λ_ , and _Ha_ is the atmospheric altitude. Also, _Cn_[2][(] _[h]_[)][ is given by the Hufnagel–Valley model] _h_ as [3] _Cn_[2][(] _[h]_[)][=][0] _[.]_[00594(] _[v]_[wind] 27[)][2][(10][−][5] _[h]_[)][10][ exp(][−] 1000[)][+] 2 _._ 7 × 10[−][16] exp(− 1500 _h_[)][ +] _[ C] n_[2][(0) exp(][−] 100 _[h]_[)][, where] _[C] n_[2][(0)][ is] the ground-level turbulence and _v_ wind is the rms wind speed. In addition, the aperture averaging effect demonstrates that an increase in the receiver aperture size leads to a decrease in power fluctuations caused by atmospheric turbulence. The aperture averaging factor, denoted as _AA_ , is given as [29, eq. (9)] 

**==> picture [233 x 34] intentionally omitted <==**

where _da_ is the aperture diameter, _σ_ I[2][is][the][scintillation] index [3], and _�_ is found in [29, eq. (10)]. 

2) _UAV Hovering-Induced Misalignment:_ The misalignment between the center of the satellite’s beam footprint and that of the UAV’s detector is due to: 1) the satellite’s vibration and the UAV’s hovering at their own fixed positions and 2) the UAV’s operation within the satellite’s wide beam coverage. 

The generalized misalignment model is reported in [29, Sec. 2.4]. The total radial displacement due to UAV hovering and satellite vibrations is given as _**r**_ = ( _rx, ry_ ), where _rx_ ∼ _N_ ( _μx, σx_[2][)][and] _[r][y]_[∼] _[N]_[ (] _[μ][y][, σ]_[ 2] _y_[)][.][Here,] _[r][x]_[and] _[r][y]_[are] two independent Gaussian random variables with different nonzero means ({ _μx, μy_ }) and variances ({ _σx_[2] _[, σ]_[ 2] _y_[}][).] Therefore, _**r**_ follows Beckmann distribution, which is accurately approximated by a modified Rayleigh distribution [4, 

eq. (17)], i.e., 

**==> picture [190 x 27] intentionally omitted <==**

where _σm_[2][=] � 3 _μ_[2] _x[σ] x_[ 4][+][3] _[μ]_[2] _y_ 2 _[σ] y_[ 4][+] _[σ] x_[ 6][+] _[σ] y_[ 6] �1 _/_ 3 is the approximated jitter variance. 

Considering the Gaussian beam profile, the fraction of received power at the UAV’s detector is given as [19, eq. (9)] 

**==> picture [167 x 32] intentionally omitted <==**

where _A_ 0 = [erf( _v_ )][2] is the fraction of collected power at _r_ = 0, erf(·) is the error function, _v_ = 2√ ~~√~~ _π_ 2 _dωaz_[is][the][ratio] between the aperture diameter and the beamwidth. In ad√ _π_ erf( _v_ ) dition, _ω_ zeq[2][=] _[ ω] z_[2] 2 _v_ exp(− _v_[2] )[is][the][equivalent][beamwidth,] where _ωz_ is the effective beamwidth at distance _L_ , given as _ωz_ = _ω_ 0�( _�_[2] 0[+] _[ �]_[2] 0[)(1][ +][ 1] _[.]_[625] _[σ]_[ 12] R _[/]_[5] ),where _ω_ 0 = _πθ_[2] _[λ]_[is] the beamwidth at _L_ = 0, with _θ_ being the divergence angle. Also, _�_ 0 = 1 − _F[L]_ 0[,][where] _[F]_[0][is][the][radius][of][curvature,] while _�_ 0 = _k_ wave2 _Lω_ 0[2][and] _[ �]_[1][=] _�_[2] 0 _�_[+] 0 _[�]_[2] 0[.] From (4) and (5), the probability distribution function (PDF) of _hp_ is derived as [29, eq. (15)] 

**==> picture [202 x 30] intentionally omitted <==**

where _Am_ = _A_ 0 exp( _ϕ_[1] _m_[2][−] 2 _ϕ_ 1 _x_[2][−] 2 _ϕ_ 1 _y_[2][−] 2 _σμx_[2] _ϕ_[2] _x x_[2][−] 2 _σμy_[2] _ϕ_[2] _y y_[2][)][and] _ϕm_ = _[ω]_ 2 _σ_[ze] _m_[q][, with] _[ ϕ][x]_[=] _[ω]_ 2 _σ_[ze] _x_[q][and] _[ ϕ][y]_[=] _[ω]_ 2 _σ_[ze] _y_[q][the jitter variances] in the _x_ and _y_ directions, respectively. 3) _Composite Channel Statistical Model:_ The composite PDF of the channel gain _h_ = _hah_ l _h_ p is derived as [8, eq. (12)] 

**==> picture [237 x 38] intentionally omitted <==**

_h_ where _Z_ = log( _Amhl_[)][ +] _[ μ]_[with] _[μ]_[ =][ 0] _[.]_[5] _[σ]_[ 2] R[(1][ +][ 2] _[ϕ] m_[2][)][.][The] cumulative distribution function of _h_ is given as [29, eq. (34)] 

**==> picture [222 x 55] intentionally omitted <==**

C. ESN-Based Channel Prediction 

1) _Multistep-Prediction ESN:_ The multiple-input– multiple-output ESN structure is illustrated in Fig. 2. Particularly, the model consists of three different layers, i.e., an input layer [1; _**x**_ ( _n_ )] ∈ R[(] _[M]_[+][1)][×][1] , a hidden layer (reservoir) _**r**_ ( _n_ ) ∈ R _[L]_[×][1] , and an output layer _**y**_ ( _n_ ) ∈ R _[N]_[×][1] . The input layer is connected to the hidden reservoir by an input weight matrix _**W** i_ ∈ R _[L]_[×][(] _[M]_[+][1)] , while the neurons in the reservoir are mutually connected by an internal sparse matrix _**W**_ ∈ R _[L]_[×] _[L]_ . The updated and output equations are typically 

7501 

CORRESPONDENCE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [237 x 106] intentionally omitted <==**

Fig. 2. Multiple-input–multiple-output ESN model. 

**==> picture [200 x 10] intentionally omitted <==**

**==> picture [200 x 25] intentionally omitted <==**

where _**r**_ **˜** ( _n_ ) is the updated state of _**r**_ ( _n_ ), [·; ·] is the vertical matrix concatenation, _α_ ∈ (0 _,_ 1] is the leaking rate, and _**W**_ o ∈ R _[N]_[×][(1][+] _[M]_[+] _[L]_[)] is the output weight matrix. 

2) _Channel Prediction Process:_ We first prepare the dataset for training and testing the model. At discrete time _n_ , _M_ data samples are regarded as the input data, while the output is defined as the next _N_ channel gain samples as 

**==> picture [224 x 25] intentionally omitted <==**

**==> picture [18 x 10] intentionally omitted <==**

where _τs_ denotes the sampling interval. Then, we start training the model to obtain the output weight matrix, as follows. 

_Step 1:_ Randomly generate _**W** i_ and _**W**_ between 0 and 1. Then, take _M_ consecutive channel gain as the input vector _**x**_ ( _n_ ); the state of the internal neurons _**r**_ ( _n_ ) is updated based on (10). The first _Ni_ samples are used to initialize the reservoir state. The collected states are stored in a matrix _**X**_ ∈ R[(1][+] _[M]_[+] _[L]_[)][×][(] _[N][t]_[−] _[N][i]_[+][1)] , given as 

**==> picture [187 x 13] intentionally omitted <==**

where _**Z**_ ( _n_ ) = [1; _**x**_ ( _n_ ); _**r**_ ( _n_ )], and _Nt_ is the number of training samples. The corresponding target output matrix is _**Y**_ ∈ R _[N]_[×][(] _[N][t]_[−] _[N][i]_[+][1)] , given by 

**==> picture [237 x 68] intentionally omitted <==**

_Step 2:_ Based on _**X**_ and _**Y**_ , the output weight matrix can be obtained by using ridge regression as 

**==> picture [177 x 15] intentionally omitted <==**

where _β_ is the regularization coefficient and _**I**_ is the identity matrix. 

Finally, after obtaining the output weight matrix _**W**_ o, at discrete time _n_ , _N_ future CSI _**y**_ ( _n_ ) can be predicted based on _M_ input samples _**x**_ ( _n_ ) according to (9)–(12). 

## III. ADAPTIVE TRANSMISSION SCHEMES 

In our adaptive system, the modulation size _K_ and transmitted power _Pt_ adaptively vary according to the channel conditions. This aims to satisfy an achievable rate ~~_τ_~~ requested from the UAV with minimum power consumption and meet practical constraints, i.e., targeted outage probability (Prout _,_ tar), targeted BER (BERtar), and maximum transmitted power ( _P_ t _,_ max). The optimization problem is formulated as 

**==> picture [213 x 25] intentionally omitted <==**

**==> picture [198 x 25] intentionally omitted <==**

**==> picture [191 x 10] intentionally omitted <==**

**==> picture [205 x 10] intentionally omitted <==**

**==> picture [193 x 10] intentionally omitted <==**

We focus on two adaptive schemes: 1) _ideal optimal AMP_ [16], and 2) _our proposed SAMP_ . Hereinafter, the modulationsizeandtransmitpoweraredenotedasfunctions of the channel coefficient _h_ , i.e., _K_ ( _h_ ) and _Pt_ ( _h_ ), respectively. 

## A. AMP Scheme 

In this ideal approach, the QAM constellation size _K_ is discretely selected from _**K**_ = { _K_ 1 _, K_ 2 _, . . ., KM_ }, while the transmitted power _Pt_ is continuously varied according to the channel conditions. Since _K_ takes discrete values, the optimization stated in (16) is an integer programming [16]. To simplify it, we divide the channel gains _h_ into subintervals, so-called transmission thresholds _**h**_[∗] . Each interval corresponds to one modulation size _Ki_ . Let _**Pr**_ = { _Pr,_ 1 _, Pr,_ 2 _, . . ., Pr,M_ } be the received power thresholds based on _**K**_ that guarantees BERtar; the optimal transmitted power can be expressed as 

**==> picture [230 x 26] intentionally omitted <==**

where _h_ 1[∗][is the outage threshold.] From (16c), _h_ 1[∗][can be obtained by keeping the outage] probability equal to Prout _,_ tar, i.e., 

**==> picture [189 x 26] intentionally omitted <==**

The optimization problem is now reduced to determine the optimal transmission thresholds _**h**_[∗] and is written as 

**==> picture [213 x 66] intentionally omitted <==**

**==> picture [194 x 11] intentionally omitted <==**

7502 IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS VOL. 60, NO. 5 OCTOBER 2024 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

## **Algorithm 1:** AMP Scheme. 

**Input:** ~~_τ_~~ , Prout _,_ tar, _**Pr**_ , _**K**_ , _h_ **Output:** _Pt_ ( _h_ ), _K_ ( _h_ ), _**h**_ **[∗] Step 1:** Given Prout _,_ tar, compute _h_ 1[∗][from][ (18)] **Step 2:** Given ~~_τ_~~ , compute _**h**_ **[∗]** from (20) **Step 3: if** _h_ ≥ _h_ 1[∗] **[and]** _[ h] i_[∗][≤] _[h][ <][ h] i_[∗] +1 **[then] 3.1:** Allocate optimal transmit power _Pt_ ( _h_ ) = _[P] h[r][,][i]_ **3.2:** Choose modulation order _Ki_ **else** Outage mode occurs, and the system is halted **end if** 

LEMMA 1 An optimum set of channel coefficient _**h**_[∗] can be derived as 

**==> picture [227 x 25] intentionally omitted <==**

where _ζ_ is the Lagrange multiplier, which is obtained from 

**==> picture [225 x 67] intentionally omitted <==**

PROOF It is solved by using the Lagrangian method provided in Appendix A. ■ 

The summary of the AMP is given in Algorithm 1. 

REMARK 1 The AMP scheme theoretically requires the transmittedpowertocontinuouslyadaptitsvalueinasinglebit duration. This, however, poses critical challenges in FSO-based satellite communications due to high feedback delays and low channel coherence time. 

## B. Proposed SAMP Scheme 

In this scheme, the transmitted power is selected from a list of discrete values _**P** t_ = [ _Pt,_ 1 _, Pt,_ 2 _, . . ., Pt,N_ ]. As mentioned in Section II, data are transmitted in fixed-time bursts. For each burst transmission, we need to determine the appropriate transmitted power _Pt, j_ , _j_ ∈{1 _,_ 2 _, . . ., N_ } and constellation size _Ki_ , _i_ ∈{1 _,_ 2 _, . . ., M_ }. To do so, we partition the thresholds into two types of subintervals, i.e., mode thresholds _**h**_[∗] and channel state thresholds _**h**_ . Each modulation scheme _Ki_ represents a transmission mode, while each transmitted power _Pt, j_ corresponds to a channel state. 

REMARK 2 To implement the SAMP scheme, we need to: 1) find _**h**_[∗] and _**h**_ and 2) determine the relation between these thresholds. Here, _**h**_[∗] can be obtained by solving the optimization problem stated in (19). Meanwhile, to find _**h**_ , we need to design a channel state model to effectively facilitate the system operation over the time-varying turbulence channels. 

**Algorithm 2:** Channel State Threshold Determination. 

**Input:** _h_ 1[∗] **Output:** _**h** , N_ **Step 1:** Set _h_ 1 = _h_ 1[∗][, and] _[j]_[=][ 2] **Step 2: while** true **do** 

**2.1:** Search _h j_ that satisfies _t j_ = _Tb_ , where _t j_ is given in (22) **2.2: if** _h j_ − _h j_ −1 ≤ _ϵ_ th **then** _h j_ = INF Break **end if 2.2:** Set _j_ = _j_ + 1 **end while Step 3:** Set _N_ = _j_ − 1 

1) _Channel State Model:_ In our system, the data are transmitted in bursts within the fixed-time slots of _Tb_ . As a result, we divide the channel into nonoverlapping states defined by a range of channel coefficients. The selection of this range satisfies the condition that the intervals of all channel states are equal to _Tb_ and shorter than the channel coherence time. The interval of the _i_ th state, _t i_ , depends on the statistical characteristic of the channel, which is given as [8, eq. (15)] 

**==> picture [182 x 26] intentionally omitted <==**

where Pr _j_ = _Fh_ ( _h j_ +1) − _Fh_ ( _h j_ ) is the probability of the _i_ th channel state. Also, LCR( _h_ th) is the level crossing rate at a certain threshold of _h_ th given as [30, (37)] 

**==> picture [230 x 78] intentionally omitted <==**

where _η_[2] = 2 _σm_[2][|] _[�]_[2][ −] _[�]_ 4[2][|][,][with] _[�]_[and] _[�]_[being][found] in [30], and _b_ = 2 _πσc_[2][with] _[ σ][c]_[=] ~~√~~ 2 ln 2 _fc_[;] _[f][c]_[ is the 3-dB cutoff] frequency. Also, _wk_ and _xk_ are, respectively, the weight factor and the _k_ th zero of the Laguerre polynomials found in [31, Tab. 25.9], and _J_ is the number of Gauss–Laguerre approximation orders. 2) _SAMP Algorithm:_ To determine channel state thresholds _**h**_ , we use the same approach stated in [8]. Specifically, we set the first threshold _h_ 1 to be equal to _h_ 1[∗][to keep] Prout _,_ tar, and the channel state interval _t j_ to be equal to the burst duration _Tb_ . In this way, all threshold levels { _hi_ } _[N] i_ =[+] 1[1] are determined. The detailed approach is summarized in Algorithm 2, where _ϵ_ th is the gap threshold between two consecutive channel states. 

7503 

CORRESPONDENCE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

**Algorithm 3:** Relation Vector Determination. 

**Input:** _**h**_[∗] , _**h**_ **Output:** _**A**_ **Step 1:** Set _j_ = 1 **Step 2: while** _j_ ≤ _N_ **do 2.1:** Find _i, i_ ∈{1 _,_ 2 _, . . ., M_ }, such that _h j_ ≥ _hi_[∗] **and** _h j < hi_[∗] +1 **2.2:** Set _A j_ = _i_ **2.2:** Set _j_ = _j_ + 1 **end while** 

## **Algorithm 4:** SAMP Scheme. 

**Input:** ~~_τ_~~ , Prout _,_ tar, _**Pr**_ , _**K**_ , _h_ **Output:** _Pt_ ( _h_ ), _K_ ( _h_ ), _**h**_ **[∗]** , _**h**_ , _**A**_ , _**Pt**_ **Step 1:** Given Prout _,_ tar, compute _h_ 1[∗][from][ (18)] **Step 2:** Given ~~_τ_~~ , compute _**h**_ **[∗]** from (20) **Step 3:** Compute _**h**_ according to Algorithm 2 **Step 4:** Compute _**A**_ by assigning the transmission modes to channel states according to Algorithm 3 **Step 5:** Compute _**P** t_ from (24) **Step 6: if** _h_ ≥ _h_ 1 **and** _h j_ ≤ _h < h j_ +1 **then 6.1:** Choose transmit power _Pt, j_ **6.2:** Choose modulation order _KA j_ **else** Outage mode occurs, and the system is halted **end if** 

When all channel states and transmission modes are determined, the next step is to find the relation between these thresholds. Let _**A**_ = [ _A_ 1 _, A_ 2 _, . . ., AN_ ], where _A j_ is the transmission mode of the _j_ th channel state. In general, one channel state interval is usually smaller than that of a transmission mode. If the mode _i_ covers all the channel state _j_ , we assign _A j_ = _i_ . Otherwise, if the channel state _j_ belongs to two or more transmission modes, the lowest mode is selected to guarantee the condition (16d), i.e., BER( _h_ ) ≤ BERtar. 

Based on the relation vector _**A**_ found in Algorithm 3, the transmitted power _Pt, j_ used for the _j_ th channel state, _j_ ∈{1 _,_ 2 _, . . . , N_ }, can be expressed as 

**==> picture [145 x 26] intentionally omitted <==**

The summary of the SAMP is given in Algorithm 4. 

## C. Performance Analysis 

1) _Average Required Transmitted Power:_ It is defined as the minimum transmitted power to maintain a particular requested rate ~~_τ_~~ under predetermined constraints on Prout _,_ tar, BERtar, and _Pt,_ max. 

LEMMA 2 The closed-form expression of required transmit power for the AMP scheme can be expressed as 

**==> picture [229 x 77] intentionally omitted <==**

**==> picture [241 x 48] intentionally omitted <==**

On the other hand, the average transmitted power of the SAMP scheme can be computed as 

**==> picture [202 x 70] intentionally omitted <==**

2) _Energy Efficiency:_ It is defined as the ratio between the average number of successfully received data bits within a burst duration and the average energy consumption for a burst transmission. It is, then, given as ~~_η_~~ EE = _E b/_ ( _Pt_ × _Tb_ ) _,_ where _E b_ is the average number of correctly received data bits within a burst duration. For the AMP scheme, it can be determined as 

**==> picture [240 x 79] intentionally omitted <==**

In the case of the SAMP scheme, _E b_ is computed as 

**==> picture [241 x 82] intentionally omitted <==**

where BER _j_ = � _hhj j_ +1 BER _j_ ( _h_ ) _fh_ ( _h_ ) _dh_ is the average BER of the _j_ th channel state. Here, BER _j_ ( _h_ ) is the instantaneous −3 _Pt_[2] _, j[h]_[2] BER given as BER _j_ ( _h_ ) = 0 _._ 2 exp( 2 _σn_[2] ( _KA j_ −1)[)][,][where] _[σ][n]_[is] the standard deviation of the Gaussian noise. 

## IV. NUMERICAL RESULTS AND DISCUSSIONS 

This section presents and discusses the performance of our proposed SAMP scheme in terms of energy efficiency. The effectiveness of the proposed design is also highlighted by comparing its performance with the conventional AM 

7504 

IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS VOL. 60, NO. 5 OCTOBER 2024 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

TABLE II 

System Parameters 

**==> picture [202 x 370] intentionally omitted <==**

Fig. 3. Average required transmit power versus requested rate for different adaptive transmission schemes. 

scheme [6] and ideal AMP scheme [16]. Moreover, the energy efficiency performance in the case of outdated CSI and predicted CSI using ML-based channel prediction models is also investigated. Monte Carlo simulations are performed to verify the analytical results. In addition, we adopt a set of constellation sizes _**K**_ = {4 _,_ 8 _,_ 16 _,_ 32 _,_ 64 _,_ 128}. Other parameters used in this article, unless otherwise noted, are given in Table II. It is worth noting that most of parameters from Table II are adopted from [4], [30], and [32]. 

## A. Average Transmitted Power and Energy Efficiency 

First, we quantitatively highlight the effectiveness of the proposed SAMP scheme by investigating the required transmitted power to satisfy a particular rate, as depicted in Fig. 3. For the sake of comparison, in addition to the ideal AMP scheme [16], we consider the AM scheme, in which the transmitted power is fixed, and the constellation size is varied during the transmission [6]. Also, different satellite’s zenith angles, i.e., _ξ_ = 50[◦] and 60[◦] , are considered. As expected, the performance of the proposed SAMP is close to that of the ideal AMP scheme. Moreover, this scheme 

**==> picture [238 x 140] intentionally omitted <==**

Fig. 4. Energy efficiency versus zenith angle for different requested rates. (a) ~~_τ_~~ = 0 _._ 6 Gb/s. (b) ~~_τ_~~ = 1 Gb/s. (c) ~~_τ_~~ = 1 _._ 2 Gb/s. 

**==> picture [238 x 152] intentionally omitted <==**

Fig. 5. Energy efficiency versus UAV’s initial displacement for different adaptive transmission schemes. (a) _θ_ jt = 11 _._ 15 _μ_ rad. (b) _θ_ jt = 20 _._ 07 _μ_ rad. 

**==> picture [202 x 131] intentionally omitted <==**

Fig. 6. Energy efficiency in the presence of outdated CSI. 

also exhibits a significant performance enhancement at the cost of high complexity compared to the conventional AM scheme. For example, when _ξ_ = 50[◦] and requested rate = 1 Gb/s, the required power gap between AM and AMP/SAMP is approximately 0.85 dB. It is because the system can utilize joint AMP control to save power consumption. From this figure, the analytical results closely follow simulated ones, which validates the correctness of the model and analysis. 

Fig. 4 analyzes the energy efficiency of different adaptive transmission schemes over a range of satellite’s zenith 

7505 

CORRESPONDENCE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [390 x 117] intentionally omitted <==**

Fig. 7. Comparison of MAE, computational time, and energy efficiency performance for different channel prediction models. 

angles. Also, different UAV’s requested rates are considered, i.e., 0.6, 1, and 1.2 Gb/s. As seen, when the satellite’s zenith angle increases, the energy efficiency performance experiencesaconsiderabledrop.Thisisbecausethesatellite needs more power to maintain the QoS requirements, i.e., the requested rate and targeted outage probability, with higher atmospheric attenuation and stronger turbulence. In addition, when the requested rate by the UAV increases, energy efficiency decreases. In other words, there is a tradeoff between the throughput and energy efficiency of the system. For example, to offer a double requested rate, i.e., from 0.6 to 1.2 Gb/s, the system needs to sacrifice approximately 0.2 Gb/J in energy efficiency. This tradeoff comes from the fact that the power required to achieve a higher rate is on a larger scale than the increase in the rate itself. 

Next, Fig. 5 analyzes the energy efficiency for different adaptive transmission schemes. Also, different pointing error conditions are considered, i.e., UAV’s radial displacement as well as satellite vibration. As evident, an increase in the UAV’s positions from the center of the beam footprint results in a significant decrease in energy efficiency, due to the beam spreading loss. For the AMP and SAMP schemes, energy efficiency is reduced by 200 Mb/J when the UAV is at 50 m from the beam center. Moreover, the severity of pointing error caused by satellite vibration jitter angle has a noticeable effect on energy efficiency due to frequent signal fluctuations. For instance, when the jitter angle varies from _θ_ jt = 11 _._ 15 _μ_ rad to _θ_ jt = 20 _._ 07 _μ_ rad, energy efficiency decreases approximately 40 Mb/J. 

## B. Effects of Outdated and Predicted CSI 

We now evaluate the system performance in the presence of outdated CSI with the channel prediction model. For the purpose of simulation and data source limitation, we adopt the channel data obtained from an FSO channel measurement [33]. We use two real-time FSO channel datasets corresponding to _σ_ R[2][=][ 0] _[.]_[0075][ and] _[ σ]_ R[ 2][=][ 0] _[.]_[1020][.] 

Fig. 6 investigates energy efficiency in the presence of delayed CSI for AMP and SAMP schemes. In this article, we assume that the delay time of the CSI is equal to _nTb_ , _n_ ∈ N, so that each burst transmission is only covered by a specific CSI. Obviously, the delayed CSI leads to a substantial degradation in energy efficiency. Moreover, as the 

**==> picture [134 x 108] intentionally omitted <==**

Fig. 8. Energy efficiency with predicted and outdated CSI. 

**==> picture [188 x 140] intentionally omitted <==**

Fig. 9. Energy efficiency and MAE versus the number of predicted steps for the ESN model. 

power is continuously varied in the optimal AMP scheme, it becomes more susceptible to imperfect CSI, leading to lower energy efficiency compared to the SAMP scheme. In addition, for the SAMP scheme, energy efficiency under stronger turbulence condition ( _σ_ R[2][=][ 0] _[.]_[1020][) is higher than] that under weaker condition ( _σ_ R[2][=][ 0] _[.]_[0075][).][This][occurs] because the interval between two consecutive channel state thresholds becomes narrower when the channel gets better. Consequently, it is more likely that the delayed state is different from the actual one, leading to high degradation in energy efficiency. 

7506 

IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS 

VOL. 60, NO. 5 OCTOBER 2024 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [215 x 107] intentionally omitted <==**

Fig. 10. Energy efficiency with outdated CSI and corresponding multistep predicted CSI. (a) _σ_ R[2][=][ 0] _[.]_[0075][. (b)] _[ σ]_ R[ 2][=][ 0] _[.]_[1020] 

Next, we adopt a support vector machine (SVM) [34] and three different types of RNN, i.e., ESN [24], [26], long short-term memory (LSTM) [35], and gated recurrent unit (GRU) [36], for channel prediction. The total number of data samples is 837 500 with the sampling interval of 1 ms. For each iteration, we use 7500 samples for training and the next 2500 samples for testing the models. The numbers of inputunits,hiddenneurons,andoutputunitsforRNN-based schemes are 20, 50, and 1, respectively. Meanwhile, the type of SVM is epsilon-SVR, the epsilon in the loss function is 0.01, and the kernel type is the radial basis function with the gamma value of 2.8. All simulations are performed in a Windows 11, AMD CPU Ryzen 7-5800H with 16.0 GB of RAM. 

As shown in Fig. 7, the RNN-based prediction models outperform SVM in terms of mean absolute error (MAE) and energy efficiency, which confirms their effectiveness in processing the time-series data. In addition, the ESN model offers very close performance compared to LSTM and GRU while requiring much smaller training time thanks to its simple structure. This is an essential factor to consider since the FSO channel coherence time is in the order of milliseconds. Therefore, we select the ESN as the most potential prediction scheme to investigate the system’s performance in this article. 

In Fig. 8, we quantitatively compare the system’s energy efficiency performance with perfect, predicted, and delayed CSI. As can be seen, in both cases of the channel, the system with predicted CSI offers very close energy efficiency compared to the system with perfect CSI. Furthermore, using predicted CSI provides a considerable performance enhancement in comparison with delayed CSI. In particular, energy efficiency when the ESN model is utilized is improved by approximately 110 Mb/J ( _σ_ R[2][=][ 0] _[.]_[1020][)][and] 160 Mb/J ( _σ_ R[2][=][ 0] _[.]_[0075][) compared to the 1-ms-delay CSI.] 

Next, we investigate the performance of the multistepprediction ESN, in which the model predicts multiple future values from the previous ones, so that the predicted CSI totally overcomes the induced feedback delay. This is necessarily important for long-distance FSO-based satellite communications. In general, when increasing the number of predicted steps, there are an upward trend in the MAE 

and an inverse trend for energy efficiency, as illustrated in Fig. 9. In addition, the ESN seems to perform better when _σ_ R[2][=][ 0] _[.]_[1020][,][which][results][in][a][lower][MAE.][It][is] worth noting that energy efficiency under weaker turbulence ( _σ_ R[2][=][ 0] _[.]_[0075][)][suffers][from][a][considerable][decrease] compared with stronger turbulence due to higher MAE and narrower channel state thresholds. 

Finally, Fig. 10 compares the energy efficiency performancewithoutdatedCSIandpredictedCSI.Weassumethat using _n_ -step prediction could completely overcome _n_ ms of delay. As can be seen from the figure, energy efficiency with multistep prediction still experiences a significant improvement over that with outdated CSI, especially when _σ_ R[2][=][ 0] _[.]_[1020][.][This][confirms][that][the][channel][prediction] model is necessarily important for our AMP control system. 

## V. CONCLUSION 

This article has introduced the design of the SAMP scheme with ML-based channel prediction. This scheme was confirmed to be more suitable for FSO-based LEO satellite communication systems than the conventional optimal ones. We analytically studied the system’s average transmitted power and energy efficiency with different adaptive schemes and CSI conditions. There are several remarkable findings from the obtained results, as follows. 

- 1) The proposed SAMP scheme exhibited a substantial performance enhancement at the cost of high complexity compared with the conventional AM scheme. Moreover, this scheme also offered very close performance compared with the ideal AMP. In the case of imperfect CSI, the ideal one was more susceptible to delayed feedback, leading to a considerable degradation of energy efficiency. 

- 2) The ESN-based prediction model was utilized to cope with delayed CSI, thanks to its high accuracy and simple structure. A comprehensive comparison among different ML-based prediction models was also provided. 

- 3) By using predicted CSI, the system experienced a considerable energy efficiency enhancement in comparison with delayed CSI. This highlighted the effectiveness of using ESN-based channel prediction for our proposed optical satellite system using adaptive transmission schemes. 

Finally, Monte Carlo simulations further confirmed the correctness of the derived analytical results. 

In addition, the study in this article envisions several future research directions, as follows. 

- 1) Since this study focused on imperfect CSI due to the delayed feedback only, other impairment sources, such as channel estimation and quantization errors, would be an extended direction. 

- 2) Another interesting future direction would be an investigation into the support of multiple UAVs, where each UAV suffers from different channel conditions. 

7507 

CORRESPONDENCE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

In this scenario, designing an efficient resource allocation scheme that satisfies the QoS of each UAV while maintaining the fairness among them becomes a challenging problem. 

## APPENDIX A 

## SOLVING THE OPTIMIZATION PROBLEM OF (19) 

We use the Lagrange method to solve the optimization problem stated in (19), which can be formulated as 

**==> picture [219 x 84] intentionally omitted <==**

where ( _ψ_ 1 _, ψ_ 2 _, . . ., ψM_ ) and _ζ_ are the Lagrange multipliers. Using the Karush–Kuhn–Tucker conditions [37], the optimal transmission thresholds _**h**_[∗] , the corresponding Lagrange multipliers ( _ψ_ 1 _, ψ_ 2 _, . . ., ψM_ ), and _ζ_ must satisfy the following conditions: 

**==> picture [225 x 37] intentionally omitted <==**

**==> picture [226 x 26] intentionally omitted <==**

To simplify the optimization problem, we assume that _h_ 1[∗] _[<] h_ 2[∗] _[<]_[ · · ·] _[ <][ h] M_[∗][.][Therefore,][from][(30b)][and][(30c)][,] _[ψ][i]_[=][ 0][.] By substituting (29) into (30a) and after some mathematical manipulations, the thresholds _**h**_[∗] can be derived as in (20). 

We now confirm the accuracy of the abovementioned assumption. When all thresholds are determined, let us define the vector _**ϵ**_ = [ _ϵ_ 1 _, . . ., ϵM_ −1], whose each element is computed as 

**==> picture [231 x 52] intentionally omitted <==**

The assumption is valid if all the elements of _**ϵ**_ are positive. Here, the values of _ϵi_ only depend on the outage probability, received power threshold _Pr,i_ , and modulation size _Ki_ . As a result, a set of QAM constellation sizes and the outage probability are selected properly to guarantee the assumption. In the numerical results, we show that all the elements of _**ϵ**_ are positive. 

APPENDIX B DERIVATION OF (25) 

The average transmitted power for the AMP is given as 

**==> picture [131 x 30] intentionally omitted <==**

**==> picture [204 x 74] intentionally omitted <==**

_h_ Let _y_ = log( _Amhl_[)][ +] _[ μ]_[;][then,] _[h]_[ =] _[ A][m][h][l]_[ exp (] _[y]_[ −] _[μ]_[)][,] _[dh]_[ =] _Amhl_ exp ( _y_ − _μ_ ) _dy_ . Integral in (32) is rewritten as 

**==> picture [221 x 86] intentionally omitted <==**

where _yi_ = log( _A[h] mi_[∗] _hl_[)][ +] _[ μ]_[and] _[y][i]_[+][1][=][ log(] _A[h] mi_[∗] + _h_ 1 _l_[)][ +] _[ μ]_[.][Us-] ing [38, eq. (06.27.21.0011.01)], the integral in (33) is solved. After several mathematical manipulations, we complete the proof. 

## **TINH V. NGUYEN** 

**==> picture [150 x 34] intentionally omitted <==**

## REFERENCES 

- [1] J. Khalife and Z. Z. M. Kassas, “Performance-driven design of carrier phase differential navigation frameworks with megaconstellation LEO satellites,” _IEEE Trans. Aerosp. Electron. Syst._ , vol. 59, no. 3, pp. 2947–2966, Jun. 2023. 

- [2] D. Zhou, M. Sheng, J. Li, and Z. Han, “Aerospace integrated networks innovation for empowering 6G: A survey and future challenges,” _IEEE Commun. Surv. Tut._ , vol. 25, no. 2, pp. 975–1019, Second Quarter 2023. 

- [3] H. Kaushal and G. Kaddoum, “Optical communication in space: Challenges and mitigation techniques,” _IEEE Commun. Surv. Tut._ , vol. 19, no. 1, pp. 57–96, First Quarter 2017. 

- [4] H. D. Le, H. D. Nguyen, C. T. Nguyen, and A. T. Pham, “FSO-based space-air-ground integrated vehicular networks: Cooperative HARQ with rate adaptation,” _IEEE Trans. Aerosp. Electron. Syst._ , vol. 59, no. 4, pp. 4076–4091, Aug. 2023. 

- [5] R. Swaminathan et al., “HAPS-based relaying for integrated spaceair-ground networks with hybrid FSO/RF communication: A performance analysis,” _IEEE Trans. Aerosp. Electron. Syst._ , vol. 57, no. 3, pp. 1581–1599, Jun. 2021. 

- [6] T. V. Nguyen, H. D. Le, N. T. Dang, and A. T. Pham, “On the design of rate adaptation for relay-assisted satellite hybrid FSO/RF systems,” _IEEE Photon. J._ , vol. 14, no. 1, Feb. 2022, Art. no. 7304211. 

- [7] T. V. Nguyen, H. D. Le, and A. T. Pham, “On the design of RIS-UAV relay-assisted hybrid FSO/RF satellite–aerial–ground integrated network,” _IEEE Trans. Aerosp. Electron. Syst._ , vol. 59, no. 2, pp. 757–771, Apr. 2023. 

- [8] H. D. Le and A. T. Pham, “On the design of FSO-based satellite systems using incremental redundancy hybrid ARQ protocols with rate adaptation,” _IEEE Trans. Veh. Technol._ , vol. 71, no. 1, pp. 463–477, Jan. 2022. 

- [9] N. Perlot and T. de Cola, “Throughput maximization of optical LEOground links,” _Proc. SPIE_ , vol. 8246, 2012, Art. no. 82460V. 

- [10] N. W. Spellmeyer et al., “A multi-rate DPSK modem for free-space laser communications,” _Proc. SPIE_ , vol. 8971, 2014, Art. no. 89710J. 

7508 IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS VOL. 60, NO. 5 OCTOBER 2024 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 

- [11] A. Shrestha and D. Giggenbach, “Variable data rate for optical lowearth-orbit (LEO) downlinks,” in _Proc. ITG-Symp. Photon. Netw._ , 2016, pp. 1–5. 

- [12] D. J. Geisler, C. M. Schieler, T. M. Yarnall, M. L. Stevens, B. S. Robinson, and S. A. Hamilton, “Demonstration of a variable datarate free-space optical communication architecture using efficient coherent techniques,” _Opt. Eng._ , vol. 55, no. 11, pp. 1–12, Nov. 2016. 

- [13] J. Pacheco-Labrador, A. Shrestha, J. C. R. Molina, and D. Giggenbach, “Implementation of variable data rates in transceiver for freespace optical LEO to ground link,” _Proc. SPIE_ , vol. 11532, 2020, Art. no. 115320J. 

- [14] P.-D. Arapoglou, G. Colavolpe, T. Foggi, N. Mazzali, and A. Vannucci, “Variable data rate architectures in optical LEO direct-to-earth links: Design aspects and system analysis,” _J. Lightw. Technol._ , vol. 40, no. 16, pp. 5541–5556, Aug. 2022. 

- [15] A.Goldsmith andS.-G.Chua,“Variable-ratevariable-powerMQAM for fading channels,” _IEEE Trans. Commun._ , vol. 45, no. 10, pp. 1218–1230, Oct. 1997. 

- [16] M. Karimi and M. Uysal, “Novel adaptive transmission algorithms for free-space optical links,” _IEEE Trans. Commun._ , vol. 60, no. 12, pp. 3808–3815, Dec. 2012. 

- [17] H. Safi, A. A. Sharifi, M. T. Dabiri, I. S. Ansari, and J. Cheng, “Adaptive channel coding and power control for practical FSO communication systems under channel estimation error,” _IEEE Trans. Veh. Technol._ , vol. 68, no. 8, pp. 7566–7577, Aug. 2019. 

- [18] D. Chen, Y. Cao, Y. Liu, Y. Gao, and F. Ai, “Performance analysis of adaptive transmission based on power control over atmosphere composite channel,” _Opt. Eng._ , vol. 62, no. 3, pp. 1–13, Mar. 2023. 

- [19] A. A. Farid and S. Hranilovic, “Outage capacity optimization for free-space optical links with pointing errors,” _J. Lightw. Technol._ , vol. 25, no. 7, pp. 1702–1710, Jul. 2007. 

- [20] I. S. Ansari, F. Yilmaz, and M.-S. Alouini, “Performance analysis of free-space optical links over Málaga ( _M_ ) turbulence channels with pointing errors,” _IEEE Trans. Wireless Commun._ , vol. 15, no. 1, pp. 91–102, Jan. 2016. 

- [21] J. H. Shapiro and A. L. Puryear, “Reciprocity-enhanced optical communication through atmospheric turbulence—Part I: Reciprocity proofs and far-field power transfer optimization,” _J. Opt. Commun. Netw._ , vol. 4, no. 12, pp. 947–954, Dec. 2012. 

- [22] F. Moll, “Experimental analysis of channel coherence time and fading behavior in the LEO-ground link,” in _Proc. IEEE Int. Conf. Space Opt. Syst. Appl._ , 2014, pp. 1–7. 

- [23] W. Jiang and H. D. Schotten, “Deep learning for fading channel prediction,” _IEEE Open J. Commun. Soc._ , vol. 1, pp. 320–332, 2020. 

   - [25] X. Na, W. Ren, M. Liu, and M. Han, “Hierarchical echo state network with sparse learning: A method for multidimensional chaotic time series prediction,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 34, no. 11, pp. 9302–9313, Nov. 2023. 

   - [26] Y. Zhao, H. Gao, N. C. Beaulieu, Z. Chen, and H. Ji, “Echo state network forfastchannelprediction in Ricean fading scenarios,” _IEEE Commun. Lett._ , vol. 21, no. 3, pp. 672–675, Mar. 2017. 

   - [27] A. Srivastava and Y. Sun, “Erbium-doped fiber amplifiers for dynamic optical networks,” in _Guided Wave Optical Components and Devices_ ,B.P.Pal,Ed.,Burlington,NJ,USA:Academic,2006,ch.12, pp. 181–203. 

   - [28] “DTS0161—Super-fast auto gain controlled erbium doped fiber amplifier (EDFA).” Accessed: Apr. 15, 2024. [Online]. Available: https://www.ofcconference.org/library/exhibits/OFC/2021/pdfs/ 579321-pb-productBrochure6.pdf 

   - [29] H. D. Le and A. T. Pham, “Level crossing rate and average fade durationofsatellite-to-UAVFSOchannels,” _IEEEPhoton.J._ ,vol.13, no. 1, Feb. 2021, Art. no. 7901514. 

   - [30] P. V. Trinh et al., “Experimental channel statistics of drone-to-ground retro-reflected FSO links with fine-tracking systems,” _IEEE Access_ , vol. 9, pp. 137148–137164, 2021. 

   - [31] M. Abramowitz and I. Stegun, _Handbook of Math. Functions With Formulas, Graphs, and Math. Tables_ , 9th ed. Gaithersburg, MD, USA: U.S. Dept. Commerce, Nat. Bureau Standards Technol., 1972. 

   - [32] M. Toyoshima, “Recent trends in space laser communications for small satellites and constellations,” _J. Lightw. Technol._ , vol. 39, no. 3, pp. 693–699, Feb. 2021. 

   - [33] A. Mostafa and S. Hranilovic, “Channel measurement and Markov modeling of an urban free-space optical link,” _J. Opt. Commun. Netw._ , vol. 4, no. 10, pp. 836–846, Oct. 2012. 

   - [34] C.-H.Wu,J.-M.Ho,andD.Lee,“Travel-timepredictionwithsupport vector regression,” _IEEE Trans. Intell. Transp. Syst._ , vol. 5, no. 4, pp. 276–281, Dec. 2004. 

   - [35] Y. Zhang, R. Xiong, H. He, and M. G. Pecht, “Long short-term memory recurrent neural network for remaining useful life prediction of lithium-ion batteries,” _IEEE Trans. Veh. Technol._ , vol. 67, no. 7, pp. 5695–5705, Jul. 2018. 

   - [36] A. B. Adege, H.-P. Lin, and L.-C. Wang, “Mobility predictions for IoT devices using gated recurrent unit network,” _IEEE Internet Things J._ , vol. 7, no. 1, pp. 505–517, Jan. 2020. 

   - [37] S. Boyd and L. Vandenberghe, _Convex Optimization_ . Cambridge, U.K.: Cambridge Univ. Press, 2004. 

   - [38] _Mathematica, Version 13.3_ , W. R. Inc., Champaign, IL, USA, 2023. [Online]. Available: https://www.wolfram.com/mathematica 

- [24] T. V. Nguyen, H. D. Le, and A. T. Pham, “Echo state network for turbulence-induced fading channel prediction in free-space optical systems,” in _Proc. IEEE World Symp. Commun. Eng._ , 2022, pp. 47–52. 

7509 

CORRESPONDENCE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30,2026 at 07:31:59 UTC from IEEE Xplore.  Restrictions apply. 


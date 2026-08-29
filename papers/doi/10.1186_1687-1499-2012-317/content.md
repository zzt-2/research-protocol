Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

## **RESEARCH** 

## **Open Access** 

## A comparison between APSK and QAM in wireless tactical scenarios for land mobile systems 

Marco Baldi[1*] , Franco Chiaraluce[1] , Antonio de Angelis[2] , Rossano Marchesani[2] and Sebastiano Schillaci[2] 

## **Abstract** 

We evaluate the performance of APSK modulation for wireless systems and compare it with the performance of more conventional QAM systems. In previous literature, the analysis of APSK has been mainly focused on the AWGN channel. This channel model provides useful insights when APSK is used in satellite systems, while it is important to consider more complex channel models for its use in terrestrial wireless applications. In particular, we consider wireless tactical scenarios for land mobile systems, that are of interest for military applications, and provide several numerical examples. First, we explore the effects on the total degradation of the reduced PAPR, typical of APSK, also taking into account the nonlinearity of HPAs and the need to use adaptive predistortion. Then, the bit error rate performance is assessed by simulation, for some typical multipath scenarios with decision feedback equalization, also including the presence of turbo channel coding. Our analysis shows that APSK can be a valid alternative to QAM in all cases in which the nonlinear effects due to HPAs cannot be neglected. 

## **Introduction** 

Mobile radio systems require highly bandwidth-efficient modulation schemes, because of the limited resources of the available radio spectrum. Such a requirement becomes particularly stringent in tactical scenarios needing high capacity communication links. 

Since a long time, quadrature amplitude modulation (QAM) and amplitude-phase shift keying (APSK) modulation [1] have been considered valuable candidates for saving bandwidth while preserving good error rate performance [2]. The benefits and drawbacks of APSK and QAM have already been assessed and compared, but only focusing on additive white Gaussian noise (AWGN) and fading channels. In [3], for example, by assuming a modulation order _M_ = 16 (that is a typical value we consider too), it was verified analytically that QAM can outperform APSK under Rayleigh fading conditions. On the other hand, in [4] it was shown that, in peak power limited Gaussian complex channels, APSK considerably outperforms QAM in terms of mutual information, particularly for the cases 

*Correspondence: m.baldi@univpm.it 

1Dipartimento di Ingegneria dell’Informazione, Universit`a Politecnica delle Marche, via Brecce Bianche 12, 60131 Ancona, Italy Full list of author information is available at the end of the article 

of _M_ = 16 and _M_ = 64. Mutual information provides the maximum transmission rate (in bits per channel use) at which error-free transmission is possible with a given signal set. Therefore, maximization of the channel mutual information is a very effective criterion to optimize the APSK constellation for any signal-to-noise ratio (SNR) operating point. Following such a criterion, some optimized APSK signal sets were presented in [5], with error performance close to QAM. Differential amplitudephase shift keying (DAPSK) has also been proposed to simplify demodulation. The performance of DAPSK has been determined [6], also over frequency-selective Rician fading channels [7], and in comparison with QAM [8]. 

Whilst it seems rather difficult to claim that APSK outperforms QAM in ideal conditions, the scenario can change when considering the impact of nonlinearities. In fact, in this case, APSK can benefit of its low peak-toaverage power ratio (PAPR): a modulation with low PAPR is more suitable for transmission when using power amplifiers with nonlinear characteristic, like traveling wave tube amplifiers (TWTAs), onboard of satellites, or solid state power amplifiers (SSPAs), on handheld devices for tactical applications. In particular, this feature allows operating with a smaller back-off, thus increasing the energy 

© 2012 Baldi et al.; licensee Springer. This is an Open Access article distributed under the terms of the Creative Commons Attribution License (http://creativecommons.org/licenses/by/2.0), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited. 

Page 2 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

efficiency of the system [9]. Dually, once having fixed the working point on the amplifier characteristic, the low PAPR allows minimizing many effects of nonlinear distortion, like warping, clustering and spectral regrowing, which is caused by intermodulation products and is responsible for adjacent channel interference (ACI) [10]. 

Many techniques, often adaptive [11], have been proposed in the past to compensate for nonlinear effects. In order to assess the best solution, an important issue concerns complexity. Among the most efficient schemes, an approach with very low complexity is the adaptive memoryless predistortion of the constellation. This method exploits a feedback mechanism between the amplifier output and the modulator, whose goal is to make the constellation actually transmitted as close as possible to the ideal constellation. On the other hand, in the presence of high power amplifiers (HPAs) and square root raised cosine (SRRC) filters, the AWGN channel can be modeled in the aggregate as a nonlinear channel with memory. So, a memoryless approach can compensate for warping but not for clustering, i.e., there is residual nonlinear intersymbol interference (ISI). Other approaches are available that, taking into account the channel memory, also reduce the nonlinear ISI. However, they are based on the solution of _M_[2] _[Q]_[+][1] equations, where _Q_ is the finite number of symbols considered for approximating the memory of the channel (for memoryless systems _Q_ = 0). So, even for very small values of _M_ and _Q_ , the complexity of these methods becomes rapidly too high [12], most of all for the implementation on low-power resource-limited field programmable gate arrays (FPGA). 

Recently, APSK has been proposed in the framework of the DVB-S2 standard [13] and its performance has been widely investigated over the AWGN channel, by considering typical satellite scenarios, also in the presence of HPAs. Moreover, several different adaptive techniques to compensate for nonlinear effects have been studied, and the improvements achievable by adding turbo channel codes have also been estimated [11,14]. 

On the contrary, the performance of APSK over multipath wireless channels, in the presence of typical HPAs for handheld devices, has not been assessed yet. In the considered scenario, modulations like Gaussian minimum shift keying (GMSK) and quadrature phase shift keying (QPSK), that are used for cellular systems (GSM and UMTS), exhibit spectral efficiencies that are generally unsatisfactory to realize high capacity links. Some recent standards, like 3GPP long term evolution (LTE) or WiMax, exploit multi-carrier modulations, like orthogonal frequency-division multiplexing (OFDM) or orthogonal frequency-division multiple access (OFDMA), which are robust against multipaths but show high PAPR, and hence low energy efficiency in the presence of nonlinear amplifiers. 

Starting from these premises, the object of this article is to discuss the performance of single carrier APSK modulation in land mobile systems and to compare it with that of a QAM having the same value of _M_ . In particular, we deepen and extend some results recently presented in [15]. As a favorite testbed, we consider the possible use of APSK in handheld high capacity tactical radio systems. This has guided the choice of some simulation variables, in particular: channel parameters, such as the maximum Doppler shift and the power delay profile (PDP), and code parameters, such as the code rate _R_ . Our starting point is the analysis carried out for the satellite channel, but performance is then assessed in land mobile scenarios. We discuss the additional problems caused by these channels, including techniques to solve them. The multipath fading, in particular, is compensated by using robust equalization at the receiver side, e.g., decision feedback equalization with filter coefficients adapted using a least mean square (LMS) algorithm. This algorithm has low computational complexity, which makes it suitable for implementation on resource-limited handheld tactical devices. We also estimate the degradation due to a typical SSPA with nonlinear characteristic, in the presence of adaptive predistortion. 

The performance analysis is most developed by simulations. This is a rather classical approach for this kind of problems, where the theoretical framework usually relies on a number of previous results (concerning modeling of the channel and the devices) that are suitably combined to describe the specific scenario. Our aim is to apply such consolidated models taking into account the peculiarities of the tactical radio scenarios, most of them being relevant to the used range of frequencies (in the VHF/UHF band). Our analysis aims at showing that, in this context, APSK can be advantageous with respect to more conventional modulation schemes, like QAM. 

The article is organized as follows. In Section ‘Overview of tactical scenarios’, a short overview of the concept of tactical scenario is given. In Section ‘System model’, we describe the model adopted for the analysis and the system components (transmitter, channel, receiver). In Section ‘PAPR and adaptive predistortion’, we discuss the PAPR and the effects of adaptive predistortion on the warping and clustering phenomena. In Section ‘Performance of APSK in multipath scenarios ’, several simulation results are provided and discussed, for timeinvariant channels as well as in the presence of fading, also considering the performance improvement due to the inclusion of a turbo channel code. In Section ‘Combined effect of multipath and nonlinearity’, the two threats are jointly considered. Finally, Section ‘Conclusion’ reports some conclusive remarks. 

Page 3 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

## **Overview of tactical scenarios** 

Tactical scenarios are of interest in military missions, and are characterized by some peculiarities, which distinguish them from conventional civil scenarios. Some of these peculiarities are discussed next. Although many of them are not essential for the subsequent analysis, all they help to understand the complexity of the considered communication system, and justify the need for more and more 

The usual frequency band for communications in tactical scenarios is the 225–400 MHz band, reserved for military use. At these frequencies, it is difficult to achieve data rates higher than 1 Mbps. A further feature of tactical scenarios is the presence of a hierarchical organization of the nodes. Since tactical scenarios reflect tactical operations, nodes are often organized in squads, platoons, companies, battalions and brigades. Each hierarchical level can be characterized differently in terms of mobility and link capacity, thus leading to rather heterogeneous networks. 

There are two main tactical scenarios which are used as a reference: on the move (OTM) and at the halt (ATH). In OTM scenarios the operation mode is that of a multi-hop ad-hoc network that is selforganizing and self-healing, and where nodes are mobile. 

The whole network is moving and no base stations are deployed. An example of OTM network may be military units (e.g., battalions) moving from an area to another. During the movement, troops can communicate within the OTM network. When a unit arrives at the operation area, ATH networks are deployed, which also involve semi-fixed or fixed nodes. Connections can be done through radio access points (RAP) exploiting high-gain mast antennas. 

As mentioned, OTM scenarios are characterized by the fact that nodes are mobile. This mobility results in the following general requirements: 

- dynamic network topology maintenance (fast network splitting/merging); 

- automatic and rapid attachment/detachment to the network; 

- dynamic radio resource allocation (whatever traffic source is constant or variable); 

- dynamic intra/inter network routing. 

An example of OTM scenario is shown in Figure 1; in this case, the network fulfills squads, platoons and companies communication needs. Obviously, similar scenarios 

**==> picture [468 x 313] intentionally omitted <==**

**Figure 1 Example of OTM scenario.** 

Page 4 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

**==> picture [342 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
GeneratorPacket FEC Turboencoder mappingSymbol ModulatorComplex Up-sampling SRRC Filter<br>HPA<br>Adaptive Pre-<br>Distortion<br>Channel<br>FEC Turbo<br>BER Soft bit Down-<br>decoder DFE SRRC Filter<br>Evaluation detection sampling<br>(BCJR)<br>**----- End of picture text -----**<br>


**Figure 2 System block diagram.** 

can also involve battalions and brigades, that represent the highest hierarchical level. 

These scenarios lead to different coverage requirements as well as different network configurations. The class of services is also dependent on the specific scenario. Concerning mobility, there are two main models used in tactical scenarios: the Gaussian Markov mobility (GMM) and group mobility. Speeds have a very variable range since we can consider both soldiers moving by foot and vehicles moving on the ground. The choice of the model is of great importance, since it is possible to verify that performance can drastically change as a result of changing the mobility model simulated [16]. 

This wide set of possibilities and requirements demands for suitable transmission techniques to be implemented in land mobile systems. Simple solutions are important for coping with the resource-limited hardware and assuring high reliability. On the other hand, achieving a high link capacity and, at the same time, a high bandwidth efficiency becomes a mandatory requirement. 

A futher requirement is obviously transmission security, which falls outside the scope of this paper. However, a careful choice of the transmission technique may also be useful from the security standpoint [17]. 

## **System model** 

A schematic representation of the communication system we consider is shown in Figure 2. This scheme will be used in the following for the performance assessment; this justifies the presence of the block for the bit error rate (BER) evaluation. The role of the other blocks will be explained next. 

The APSK constellation consists of the superposition of two concentric PSK constellations, that are characterized by different energy. An example, referred to the DVB-S2 standard, is shown in Figure 3. 

**==> picture [220 x 72] intentionally omitted <==**

where _N_ is the number of concentric rings ( _N_ = 2 for the 4+12-APSK shown in Figure 3), _ni_ is the number of points in the _i_ th PSK ( _i_ = 1, 2, _. . ._ , _N_ ), _ri_[2][is the energy of the] _[ i]_[th] subset of signals, and _ϑi_ its phase offset. 

In comparison with a QAM constellation having the same number, _M_ , of symbols, APSK is characterized by a smaller number of amplitude levels, and this allows 

**==> picture [235 x 257] intentionally omitted <==**

**----- Start of picture text -----**<br>
0010<br>1010<br>1110 C 1 0110<br>C<br>2<br>1111 0011 0111<br>1011<br>0<br>1101 1001 0101<br>0001<br>1100 0100<br>1000<br>0000<br>0<br>In-Phase (I-Channel)<br>Figure 3 Example of APSK constellation.<br>Quadrature (Q-Channel)<br>**----- End of picture text -----**<br>


Page 5 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

achieving a lower PAPR. For a fixed value of _M_ , the constellation can be optimized through the minimization of a suitably defined cost function, or, equivalently, through the maximization of a quantity related to the cost function. Common criteria for this purpose consist in maximizing the minimum Euclidean distance (MED) or the mutual information [14]. 

As an example of practical interest, in this article we consider the 4 + 12-APSK constellation suggested in [13], whose parameters are optimized under the MED criterion ( _r_ 2 _/r_ 1 = 2.7, _ϑ_ 2 − _ϑ_ 1 = 0). We remind that the choice of having a larger number of points in the outer ring allows maximizing the conversion efficiency of the HPA, since the mean transmitted power tends to be close to the peak level. In this article, a pseudo-Gray labeling, of the type shown in Figure 3, is used for the 4 + 12-APSK constellation. The 16-QAM constellation we compare with adopts a Gray labeling. As well known, these mapping strategies minimize the bit error rate for a given value of the symbol error rate. However, it must be said that the discussion about optimal mapping, as well as de-mapping (that has an impact on the computational complexity) is still open, and some variants have been proposed in the literature (see [18,19], for example). 

At the transmitter (TX) side, an SRRC filter is adopted, with a roll-off factor _ρ_ . The complex envelope of the signal can be written as: 

**==> picture [220 x 29] intentionally omitted <==**

where _an_ ∈ C is the _n_ th transmitted symbol and _p(t)_ determines the pulse shape. _Ts_ is the symbol duration, whose inverse is the symbol rate _Rs_ . Before entering the channel, _s(t)_ is amplified by the HPA, which makes the overall channel nonlinear. For simulation purposes, the latter is modeled through a memoryless nonlinearity described by the so-called amplitude modulation to amplitude modulation (AM/AM) and amplitude modulation to phase modulation (AM/PM) conversion functions [20]. The output of the nonlinearity is then expressed as _s_ HPA _(t)_ = _F(_ | _s(t)_ | _)e[j][(]_[∠] _[s][(][t][)]_[+] _[�(]_[|] _[s][(][t][)]_[|] _[))]_ , where, following [21], we have defined _F(A)_ and _�(A)_ as the AM/AM and AM/PM characteristics of the amplifier for a signal with instantaneous signal amplitude _A_ . Common expressions for _F(A)_ and _�(A)_ can be found in the literature [22,23]. In particular, for a typical SSPA equipping handheld devices, 

**==> picture [171 x 59] intentionally omitted <==**

for AM/AM and AM/PM, respectively. The four parameters appearing in Equations (3) and (4) (i.e., _γ_ , _δ_ , _αp_ and _βp_ ) are determined from measured AM/AM and AM/PM curves, taken from a real 1 W SSPA used for handheld devices. In particular, following a best fit approach which minimizes the mean squared error (MSE) between the analytical and measured data, one finds: _γ_ = 1.99, _δ_ = 2.15, _αp_ = 0.14 and _βp_ = 0 [21]. The corresponding AM/AM and AM/PM characteristics are shown in Figure 4, where the mean input and output powers are normalized to the corresponding saturation levels. As it is expected for SSPAs, even near saturation, phase degradation is rather small, while the main distortion affects the amplitude. 

The output of the HPA is then given as input to the adaptive predistortion block. This has been implemented by following the memoryless approach proposed in [11]; details are omitted for the sake of brevity, but can be found in the quoted reference. 

In order to describe the effects of the multipath fading, we have considered the discrete paths model whose channel impulse response (baseband equivalent) can be written as: 

**==> picture [220 x 31] intentionally omitted <==**

In (5), _P_ is the number of paths and _τi(t)_ is the propagation delay along the _i_ th path; moreover: 

**==> picture [214 x 12] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

where _αi(t_ , _τ)_ is the attenuation along the _i_ th path (that can be described through a statistical distribution, as Rice or Rayleigh), _ϕi(t_ , _τ)_ is a random phase shift, and _fc_ is the carrier frequency. The channel has been simulated 

**==> picture [235 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 15<br>-5 10<br>-10 5<br>-15 0<br>-20 -18 -16 -14 -12 -10 -8 -6 -4 -2 0 2<br>normalized mean input power [dB]<br>Figure 4 AM/AM and AM/PM characteristics for the considered<br>SSPA.<br>**----- End of picture text -----**<br>


Page 6 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

by using the statistical model based on the sum of sinusoids (SoS) [24], which derives from the well-known Jakes model. Before entering the receiver section, white Gaussian thermal noise is added, characterized by a two-sided power spectral density equal to _N_ 0 _/_ 2. 

At the receiver (RX) side, we have an SRRC filter equal to that at the TX. Perfect carrier synchronization is assumed to allow ideal coherent demodulation. Very efficient algorithms have been proposed in the past for such purpose [25]. The output of the RX filter is sampled at the symbol time and then sent to a decision feedback equalizer (DFE) [26]. The coefficients of the DFE are adapted through the LMS algorithm. According to the proposed solution, equalization is performed in the time domain. Alternatively, frequency domain equalizers, e.g., iterative block decision feedback equalizers, could be used as well, with some expected advantage in terms of reduced complexity [27]. 

According to Figure 2, forward error correction (FEC) can also be included. Actually, in Section ‘Performance of APSK in multipath scenarios’, simulations considering the use of turbo channel codes [28] will be presented. In such case, the encoder of a binary turbo code is added at the TX, before the bit to symbol mapping (i.e., according to a “pragmatic” approach), while, at the RX, a decoder based on the BCJR algorithm is inserted after the decision device. The turbo code we consider is that included in the UMTS standard [29]. It is composed of two recursive systematic convolutional (RSC) encoders with constraint length 4, concatenated in parallel. The feedforward generator is 15 and the feedback generator is 13 (in octal notation). The code bits for the two encoders are alternatively punctured to achieve the desired code rate _R_ = 1 _/_ 2. Decoding has been implemented in Matlab[©] , by using the algorithm presented in [30]. The UMTS code is worldwide, and its performance has been widely investigated. So, in our opinion, it is a valid candidate for the use in tactical radio systems. 

## **PAPR and adaptive predistortion** 

By observing the modulated signal (2) within the finite interval [ 0, _T_ ], the PAPR is defined as follows [9]: 

**==> picture [220 x 28] intentionally omitted <==**

We have chosen an observation time corresponding to a frame of 1024 modulated symbols, that is a reasonable value for the applications of interest, and considered SRRC filters with different values of the roll-off factor. It is known [31] that the roll-off factor has a significant impact on the PAPR value. In our simulation, we have considered a filter with 17 fractionally spaced taps, at a sampling rate 

**==> picture [214 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
5.0<br>4.5<br>4.0<br>3.5<br>3.0<br>0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0<br>ρ<br>SRRC<br>**----- End of picture text -----**<br>


**Figure 5 Contribution of the SRRC to the PAPR, for different** 

of four samples per symbol. The assumption of a so short filter is justified by the need to ensure an acceptable complexity on board of a low-power handheld radio with high capacity (1 Mbps). As a drawback, the behavior of such a filter can be rather poor at small values of _ρ_ , but this can be compensated, for example by adding further filtering at the analog front-end. 

The contribution of the SRRC filter to the PAPR is shown in Figure 5. The total PAPR can be obtained from this figure by adding 1.05 dB, for the APSK, and 2.55 dB, for the QAM, that are the constant contributions due to the constellation. Some numerical values are reported in Table 1. It must be said that a further reduction in the PAPR value could be achieved, at least in principle, by using peak envelope control algorithms, like trellis shaping (TS) [32] or magnitude modulation (MM) [33]. These techniques, however, introduce additional complexity that, particularly for TS, may be unacceptable for the considered applications. 

The parameter chosen to evaluate the performance in the presence of nonlinear effects is the _total degradation_ (TD). Given the output back-off (OBO) of the system (that is, the reduction in the transmitted power that is necessary to minimize the effect of the intermodulation products), the TD is defined, in dB, as: 

**==> picture [220 x 11] intentionally omitted <==**

**Table 1 PAPR in 4 + 12-APSK and 16-QAM, for different** 

|**Modulation**|**_ρ_ = 0.1**|**_ρ_ = 0.3**|**_ρ_ = 0.5**|
|---|---|---|---|
|16-QAM|7.2 dB|6.3 dB|5.7 dB|
|4+12-APSK|5.7 dB|4.8 dB|4.2 dB|



Page 7 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

**==> picture [204 x 168] intentionally omitted <==**

**----- Start of picture text -----**<br>
9<br>8<br>7<br>6<br>5<br>4<br>3<br>4+12-APSK, ( E b / N 0 ) lin = 10.95 dB<br>2 16-QAM, ( E b / N 0 ) lin  = 10.50 dB<br>1<br>1 2 3 4 5 6 7 8 9<br>OBO [dB]<br>**----- End of picture text -----**<br>


**Figure 6 Total degradation with 4 + 12-APSK and 16-QAM, assuming** _**ρ**_ **= 0.3 and BER = 10[-3] .** 

where _(Eb/N_ 0 _)_ OBO is the signal-to-noise ratio per bit required to achieve a desired BER value in the real system, while _(Eb/N_ 0 _)_ lin is the signal-to-noise ratio per bit required to have the same performance in an ideal (linear) system. The simulated TD in the case of _ρ_ = 0.3 is shown in Figure 6, for BER = 10[−][3] , and in Figure 7, for BER = 10[−][5] . The optimal working point corresponds to the minimum of each curve and, from the figures, we see that the minimum is lower for the APSK system than for the QAM system. Such result is not surprising since, for both systems, the TD value depends on the PAPR value: a smaller PAPR corresponds to a smaller TD. Moreover, the optimal working point of APSK corresponds to a smaller back-off, which allows improving the energy efficiency of the system. 

**==> picture [202 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
10<br>9<br>8<br>7<br>6<br>5<br>4<br>3 4+12-APSK, ( E b / N 0 ) lin = 14 dB<br>2 16-QAM, ( E b / N 0 ) lin = 13.4 dB<br>1<br>1 2 3 4 5 6 7 8 9<br>OBO [dB]<br>**----- End of picture text -----**<br>


**Figure 7 Total degradation with 4 + 12-APSK and 16-QAM, assuming** _**ρ**_ **= 0.3 and BER = 10[−][5] .** 

The effect of a nonlinear power amplifier on the transmitted constellation is essentially described by the warping and clustering phenomena observed at the output of the amplification process [21]. 

The constellation warping, which is due to the gain compression of the amplifier operated near saturation, refers to the situation where the points on the inner ring, i.e. with lower energy, are more amplified than the points on the outer ring, which have higher energy (an example is shown in Figure 8): as a result, the constellation collapses towards the outer ring, and this is due to the AM/AM characteristic. Moreover, the outer ring is phase shifted with respect to the inner ring, because of the AM/PM distortion, and the performance can be severely degraded. 

In addition, as we see from Figure 8, each point is spread in a cloud centered around the effective “warped” constellation: we refer to this effect as clustering, and it is equivalent to have ISI in the received signal. This phenomenon is essentially due to the memory effect of the overall nonlinear channel composed by the pulse shaping filter, the memoryless nonlinearity and the matched filter at the receiver, as the presence of the nonlinearity, although instantaneous[a] , makes the cascade between the pulse shaping filter and the matched receiver to be not compliant with the Nyquist ISI criterion. For such reason, we define this type of interference in the received signal as nonlinear ISI. Modeling the power amplifier as a pure nonlinearity without memory implies that the amplifier behavior is frequency independent, i.e., it does not exhibit a filtering action on the amplified signal. This assumption is realistic when dealing with SSPAs whose passband is much larger than the modulated signal bandwidth. However, since the required transmission rates are continuously increasing (so that the signal bandwidth becomes larger and larger as well), improved HPA 

**==> picture [214 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.5<br>1<br>0.5<br>0<br>-0.5<br>-1<br>-1.5<br>-1.5 -1 -0.5 0 0.5 1 1.5<br>In-Phase<br>Quadrature<br>**----- End of picture text -----**<br>


**Figure 8 Effect of saturation on APSK constellation without predistortion.** 

Page 8 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

models are needed, which also take into account the memory effect of the amplifier itself [21]. 

There is another important phenomenon in the frequency domain that is due to the presence of nonlinear amplification: the output signal spectrum is affected by the so-called “spectral regrowth” effect [21]. 

This phenomenon is shown in Figure 9, for different values of the input back-off (IBO); it must be noted that IBO →∞ corresponds to the linear behavior. Spectral regrowth is due to the intermodulation products associated to the nonlinearity, i.e., to the fact that the output signal spectrum contains frequency components which are absent in the original input signal spectrum, outside of its original bandwidth. This kind of distortion brings to the adjacent channel interference, an undesired effect which degrades the transmission of other users on adjacent channel bandwidths. 

Digital memoryless (or static) symbol time predistortion is a method for reducing the undesired effects of nonlinear amplification. Since it considers only the current symbol, it does not compensate for clustering (due to the memory effect) but only for warping. On the other hand, it has significantly lower computational complexity with respect to methods with memory, or dynamic; the latter, in fact, are commonly based on the solution of _M_[2] _[Q]_[+][1] equations, so that their complexity increases exponentially with the memory _Q_ of the predistortion process. 

The considered approach works on the downsampled signal at the symbol time, rather than at the digital-toanalog converter (DAC) sample rate, that is, at the lowest possible sampling rate within the receiver chain. On the other hand, working on the downsampled, i.e., aliased, signal, it is not possible to control the entire transmitted spectrum, that prevents from reducing the spurious frequency components originated from the nonlinearity. 

**==> picture [215 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
IBO = 0 dB IBO = 3 dB<br>2 2<br>1 1<br>0 0<br>-1 -1<br>-2 -2<br>-2 -1 0 1 2 -2 -1 0 1 2<br>In-Phase In-Phase<br>IBO = 6 dB IBO = 12 dB<br>2 2<br>1 1<br>0 0<br>-1 -1<br>-2 -2<br>-2 -1 0 1 2 -2 -1 0 1 2<br>In-Phase In-Phase<br>Quadrature Quadrature<br>Quadrature Quadrature<br>**----- End of picture text -----**<br>


**Figure 10 APSK constellation with predistortion.** 

In fact, changing only the constellation points positions does not modify the shape of the power spectral density of the modulated signal, which is [34]: 

**==> picture [220 x 23] intentionally omitted <==**

where _P(f )_ is the Fourier transform of the pulse shape and _σa_[2][is][the][variance][of][the][information][sequence][{] _[a][n]_[}][.] As a consequence, to change the constellation points positions does not compensate for the frequency nonlinear distortion induced by the amplifier. Figures 9 and 10 (the latter to be compared with Figure 11, where predistortion has not been applied) confirm that the memoryless approach compensates only for the warping of the constellation points, and the residual nonlinear ISI degrades performance near saturation. 

**==> picture [483 x 209] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 IBO = 0 dB IBO = 3 dB<br>IBO = 0 dB 2 2<br>IBO = 1 dB<br>-10 IBO = 3 dB 1 1<br>IBO = 6 dB<br>IBO = 12 dB 0 0<br>-20 IBO →∞<br>-1 -1<br>-30<br>-2 -2<br>-2 -1 0 1 2 -2 -1 0 1 2<br>In-Phase In-Phase<br>-40 IBO = 6 dB IBO →∞<br>2 2<br>-50 1 1<br>-60 0 0<br>-1 -1<br>-70<br>-20 -10 0 10 20 -2 -2<br>-2 -1 0 1 2 -2 -1 0 1 2<br>Frequency [MHz] In-Phase In-Phase<br>Figure 9 Spectral regrowth effect. Figure 11 APSK constellation without predistortion.<br>Quadrature Quadrature<br>PSD [dB/Hz]<br>Quadrature Quadrature<br>**----- End of picture text -----**<br>


Page 9 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

The adaptive predistortion method can be implemented off-line through an iterative LMS algorithm [25]. More precisely, _S_ blocks of _W_ symbols are observed at the output of the matched filter and, for each of them, the center _cn_ of the cluster _In_ (for the _n_ th constellation point) is computed according to the following expression: 

**==> picture [220 x 28] intentionally omitted <==**

where _Mn_ is the number of symbols, in the _s_ th block, _(s_ = 1, _. . ._ , _S)_ belonging to _In_ . Then, denoting by _a_[pre] _n[(][s][)]_ the predistorted _n_ th constellation point at step _s_ , the following equations are applied: 

**==> picture [186 x 12] intentionally omitted <==**

**==> picture [162 x 10] intentionally omitted <==**

where _an_ is the ideal constellation point, _μ_ is the LMS step size parameter and _en(s)_ is the error signal at the end of the _s_ th block. As we see from Figure 12, this type of predistortion allows transmitting at saturation without the warping 

## **Performance of APSK in multipath scenarios** 

In this section, we introduce the effects of multipath fading. It is intuitively reasonable that the BER performance in this kind of scenario depends on the PDP, that is, the distribution of the power levels among the paths. Performance is also affected by the ability of the LMS algorithm, used for computing the DFE coefficients, to track the channel variations. 

In our analysis, the number of DFE coefficients has been set equal to 15, for the feedforward filter, and to 7, for the feedback filter. The number, _P_ , of channel paths simulated is three and four. In the latter case, the fourth path is outside the span of the DFE, thus allowing to evaluate the 

**==> picture [214 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.5<br>1<br>0.5<br>0<br>-0.5<br>-1<br>-1.5<br>-1.5 -1 -0.5 0 0.5 1 1.5<br>In-Phase<br>Quadrature<br>**----- End of picture text -----**<br>


**Figure 12 Effect of saturation on APSK constellation with predistortion.** 

sensitivity of the system on rare or unexpected multipath components that, as such, have not been considered, in advance, in the design. More precisely, in (5), we have set: _τ_ 0 = 0, _τ_ 1 = _Ts_ , _τ_ 2 = 2 _Ts_ , _τ_ 3 = 8 _Ts_ . As the effect of the HPA nonlinearity can be taken into account through the TD parameter, with the aim to study separately the phenomena, fading effects are investigated by assuming that the amplifier works in linear regime. The way to use TD in the complete system (i.e., in the presence of multipath and nonlinearity) will be discussed in Section ‘Combined effect of multipath and nonlinearity’. 

## **Channel without fading** 

Let us suppose that the channel is time-invariant. We wish to study the robustness of the DFE against multipaths within the span of the feedback filter; so, we have set _P_ = 3. Assuming the power on the first path as a reference, the power on the other paths has been progressively increased. Some examples of PDPs are considered in Figure 13, which shows the channel transfer functions within the Nyquist interval (only positive frequencies are plotted). We see that, for increasing power levels, the transfer function tends to have, as expected, a null in the frequency range of interest. As it is known, this is the situation where the DFE outperforms classical equalization approaches based on the inversion of the equivalent channel filter (like zero-forcing equalizers). The BER performance achievable with APSK, in comparison with that of QAM, is shown in Figure 14 for the considered power delay profiles. Although the BER curves could be plotted as functions of the classical signal-to-noise ratio (i.e., the ratio between the transmitted power and the noise power), we prefer to use the signal-to-noise ratio per bit, since it is more meaningful and coherent with the definition (8) of total degradation. From the figure, we see that 

**==> picture [214 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
5<br>0<br>-5<br>PDP = [0 -20 -20]<br>PDP = [0 -10 -20]<br>-10<br>PDP = [0 -6 -12]<br>PDP = [0 -3 -6]<br>PDP = [0 -2 -4]<br>-15<br>0 0.1 0.2 0.3 0.4 0.5<br>Nyquist interval (f × Ts)<br>Power [dB]<br>**----- End of picture text -----**<br>


**Figure 13 Multipath channel transfer functions for different power levels.** 

Page 10 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

**==> picture [235 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3<br>10<br>4+12-APSK PDP=[0 -20 -20]<br>10-4 16-QAM PDP=[0 -20 -20]<br>4+12-APSK PDP=[0 -10 -20]<br>10-5 16-QAM PDP=[0 -10 -20]<br>4+12-APSK PDP=[0 -6 -12]<br>10-6 16-QAM PDP=[0 -6 -12]<br>4+12-APSK PDP=[0 -3 -6]<br>-7 16-QAM PDP=[0 -3 -6]<br>10<br>4+12-APSK PDP=[0 -2 -4]<br>-8 16-QAM PDP=[0 -2 -4]<br>10<br>0 2 4 6 8 10 12 14 16 18 20<br>Eb/N0 [dB]<br>Figure 14 Simulated BER performance of APSK and QAM in<br>multipath channels with different power levels.<br>BER<br>**----- End of picture text -----**<br>


the APSK modulation shows a loss of about 0.5 dB, at BER = 10[−][5] , with respect to QAM. Thanks to the presence of the DFE, the performance remains acceptable even for the most critical channel (at BER = 10[−][5] , the gap between the curves is smaller than 4 dB), and no _error floor_ appears, which could be due to irreducible ISI. 

The situation is rather different in the presence of the fourth path, that is out-of-span and, hence, unexpected. In Figure 15, we have fixed a very small power in the second and third paths (−20 dB, with respect to the first path), while the power on the fourth path has been progressively increased by steps of 2 dB. Through a comparison with Figure 14, we see that, even for a power of −20 dB, at BER = 10[−][3] , there is a loss of about 1.5 dB with respect to the ideal condition (i.e., the case with three paths). The curves for a power of −14 dB exhibit a BER floor just in the neighborhood of 10[−][3] , and, for signal-to-noise ratios greater than about 20 dB, the performance significantly degrades. These results confirm the need to properly model the channel, in such a way as to avoid the appearance of unexpected path contributions. 

## **Channel with fading** 

In the previous section, the channel was assumed to be time-invariant. Obviously, this condition does not apply to mobile systems, so it will be removed in this section. 

Since we are studying mobile scenarios, it is necessary to take into account the Doppler shift. By considering a VHF/UHF carrier at 400 MHz (which is a typical value in the considered wireless tactical applications) and a relative speed between TX and RX of about 80 km/h, i.e., a moderate vehicular velocity, the maximum Doppler shift _fD_ is in the order of 25 Hz. Correspondingly, the coherence time 

**==> picture [214 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3 4+12-APSK 4th: -20 dB<br>10 16-QAM 4th: -20 dB<br>4+12-APSK 4th: -18 dB<br>16-QAM 4th: -18 dB<br>10-4 4+12-APSK 4th: -16 dB<br>16-QAM 4th: -16 dB<br>4+12-APSK 4th: -14 dB<br>-5 16-QAM 4th: -14 dB<br>10<br>0 2 4 6 8 10 12 14 16 18 20<br>Eb/N0 [dB]<br>BER<br>**----- End of picture text -----**<br>


**Figure 15 Simulated BER performance of APSK and QAM for different power levels of the fourth path.** 

is about 0.04 s. In high capacity networks, it is reasonable to assume slow fading, i.e., the channel remains in static conditions for several consecutive symbols, which implies to have a normalized fade rate due to terminals motion _fDTs <<_ 1. More precisely, we set _fDTs_ = 5 · 10[−][6] . This yields an uncoded bit rate equal to 20 Mbps, which means to have 10 Mbps information bit rate when a rate-1 _/_ 2 turbo code is applied. Both these cases will be considered in the following. By assuming a roll-off _ρ_ = 0.3, the required bandwidth at radio frequency equals 6.5 MHz. 

A first goal is to estimate the impact of applying the UMTS punctured turbo code (but other coding options are obviously acceptable). Figure 16 shows the average BER, with and without channel coding, in a single path scenario where a line of sight (LOS), unfaded component 

**==> picture [214 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3<br>10<br>-4<br>10<br>-5 4+12-APSK uncoded<br>10 16-QAM uncoded<br>4+12-APSK Turbo coded<br>-6 16-QAM Turbo coded<br>10<br>0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16<br>Eb/N0 [dB]<br>BER<br>**----- End of picture text -----**<br>


**Figure 16 Average BER on a single path fading channel with LOS (Rice fading), with and without the application of a turbo code.** 

Page 11 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

exists between TX and RX, as it can occur in a rural area with no obstacles. In this case, |˜ _α_ 0 _(t_ , _τ)_ | has a Rice distribution with parameter _K_ , set equal to 10 dB in the simulations, which represents the power ratio between the unfaded (LOS) component and the faded components in that path. In this figure, and the following ones of the same type, averaging has been done within a typical observation time of 1 s. This obviously limits the minimum simulated BER to values that, however, are significant enough for the considered tactical radio applications. 

Figure 16 evidences the improvement achievable by using the turbo code: at BER = 10[−][3] , the simulated coding gain is about 4 dB for QAM and about 4.8 dB for APSK. In this scenario, an error floor effect appears in the BER curves, due to the random frequency modulation caused by the Doppler spread [26]. Obviously, the channel code cannot eliminate such BER floor, which depends on the value of _fD_ and appears, for the considered example, around BER = 10[−][5] . 

As expected, the situation is more critical in the presence of multipaths: Figure 17 shows the average BER, for the APSK and QAM systems, by considering, for the first path, the same Rice fading as in Figure 16, but with the addition of the second and third paths, for which |˜ _αi(t_ , _τ)_ |, _i_ = 1, 2, has a Rayleigh distribution. Different PDPs are also considered, and no channel code is applied. In this scenario, the error floor due to the random frequency modulation caused by the Doppler spread is around 10[−][4] for the most favorable case and around 10[−][3] for the least favorable case (among the considered ones). 

Now let us consider the first path without the unfaded component, i.e., without LOS visibility between TX and RX. The BER curves are shown in Figure 18. In this case, it is more meaningful to plot the cumulative distribution 

**==> picture [214 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3<br>10<br>4+12-APSK PDP = [0 -10 -20]<br>16-QAM PDP = [0 -10 -20]<br>10-4 4+12-APSK PDP = [0 -6 -12]<br>16-QAM PDP = [0 -6 -12]<br>4+12-APSK PDP = [0 -3 -6]<br>-5 16-QAM PDP = [0 -3 -6]<br>10<br>0 2 4 6 8 10 12 14 16 18<br>E /N<br>b 0<br>BER<br>**----- End of picture text -----**<br>


**Figure 17 Average BER on a three-path fading channel with LOS along the first path (Rice fading).** 

**==> picture [214 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>4+12-APSK PDP = [0 -10 -20]<br>16-QAM PDP = [0 -10 -20]<br>4+12-APSK PDP = [0 -6 -12]<br>16-QAM PDP = [0 -6 -12]<br>-1 4+12-APSK PDP = [0 -3 -6]<br>10 16-QAM PDP = [0 -3 -6]<br>-2<br>10<br>-3<br>10<br>0 2 4 6 8 10 12 14 16 18<br>E /N<br>b 0<br>BER<br>**----- End of picture text -----**<br>


**Figure 18 Average BER on a three-path fading channel without LOS (Rayleigh fading).** 

function (CDF) of the BER: it expresses the probability that the BER is smaller than a prefixed value BER0, for a given signal-to-noise ratio. The BER is evaluated over a set of frames during which the channel can be assumed to be static, that is, within a time interval not longer than the channel coherence time, and its probability distribution is determined. This performance measure is directly related to the outage probability, expressing the probability that the channel shows a deep fade which severely = degrades the BER performance [35]. The CDF for PDP [ 0, −3, −6] dB, considering different values of the signalto-noise ratio, is shown in Figure 19: the probability to have BER _<_ BER0 = 10[−][3] , at _Eb/N_ 0 = 14 dB, is about 0.35 for QAM and about 0.28 for APSK, while it becomes greater than 0.56, for both systems, at _Eb/N_ 0 = 20 dB. Similar evaluations for PDP =[ 0, −20, −20] dB (i.e., the 

**==> picture [214 x 165] intentionally omitted <==**

**----- Start of picture text -----**<br>
1<br>0.9<br>0.8<br>0.7<br>0.6 16-QAM E b /N 0 =10 dB<br>0.5 4+12-APSK E b /N 0 =10 dB<br>0.4 16-QAM Eb/N0=12 dB<br>4+12-APSK Eb/N0=12 dB<br>0.3 16-QAM Eb/N0=14 dB<br>0.2 4+12-APSK E b /N 0 =14 dB<br>0.1 16-QAM E b /N 0 =20 dB<br>4+12-APSK Eb/N0=20 dB<br>0  -3 -2 -1 0<br>10 10 10 10<br>BER<br>0<br>)Pr(BER < BER0<br>**----- End of picture text -----**<br>


**Figure 19 CDF of the BER for the Rayleigh fading with PDP = [ 0, −3, −6] dB.** 

Page 12 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

channel is much less disturbed) would provide a probability in the order of 0.9 for _Eb/N_ 0 = 14 dB and a greater value for _Eb/N_ 0 = 20 dB. Hence, the CDF permits us to verify explicitly the expected result, i.e., that the probability of a fade is greater for the more disturbed channel. To draw the same conclusion from the average BER curves of Figure 18 is not possible. 

The fade probability can be significantly reduced by using the turbo code. Figure 20 shows the CDF for the least disturbed scenario (among those we have considered), assuming _Eb/N_ 0 = 8 dB. At such signal-tonoise ratio, the probability that the uncoded system has BER _<_ 10[−][3] is negligible, while it grows up to nearly 0.9 after using the turbo code, that is a strong performance improvement. 

Similarly to Section ‘Channel without fading’, another topic we discuss is the sensitivity of the equalization process on the presence of multipath components that are out of the span of the feedback filter in the DFE. In Figure 21, the mean transmitted power along the second and third paths have been set to −20 dB, while that on the fourth path has been progressively increased. We observe that, when the power on the fourth path changes from −30 dB to −20 dB, the BER floor grows from about 10[−][5] to about 10[−][3] . Further increasing the unequalized path power makes the system useless. Even adding the turbo code is not effective in this case: as shown in Figure 22, the signal-to-noise ratios involved are smaller but, for a nonnegligible power level on the unexpected path (i.e., −10 dB and −15 dB), a high BER floor remains. 

At the end of this section, we observe that, in all our simulations, the BER performance of the 4+12-APSK system is quite similar to that of the 16-QAM system. So, we can conclude that no significant loss appears when using 

**==> picture [214 x 165] intentionally omitted <==**

**----- Start of picture text -----**<br>
1<br>0.9<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2 4+12-APSK uncoded<br>16-QAM uncoded<br>0.1 4+12-APSK turbo coded<br>16-QAM turbo coded<br>0  -3 -2 -1 0<br>10 10 10 10<br>BER<br>0<br>)0<br>Pr(BER < BER<br>**----- End of picture text -----**<br>


**Figure 20 CDF of the BER for the Rayleigh fading with PDP =[ 0, −20, −20] dB, at** _**Eb/N**_ **0 = 8 dB, including the presence of the turbo code.** 

**==> picture [214 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3 4+12-APSK 4th: -30 dB<br>10 16-QAM 4th: -30 dB<br>4+12-APSK 4th: -20 dB<br>16-QAM 4th: -20 dB<br>10-4 4+12-APSK 4th: -15 dB<br>16-QAM 4th: -15 dB<br>4+12-APSK 4th: -10 dB<br>-5 16-QAM 4th: -10 dB<br>10<br>0 2 4 6 8 10 12 14 16 18 20<br>Eb/N0 [dB]<br>BER<br>**----- End of picture text -----**<br>


**Figure 21 Simulated BER performance for different power levels of the fourth path.** 

this modulation scheme in multipath fading channels in place of the square QAM scheme. Taking into account the benefits shown by the APSK system, for example in terms of total degradation, this suggests that APSK represents an efficient solution for the use in the considered tactical radio framework. 

## **Combined effect of multipath and nonlinearity** 

The object of this section is twofold. On one hand, we provide an example of simulation of the entire system, i.e., in the presence of both nonlinearity and multipath. On the other hand, we show how the previous analysis, that considered these impairments separately, can be used to provide a meaningful estimate of the whole performance. 

**==> picture [214 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
0<br>10<br>-1<br>10<br>-2<br>10<br>-3 4+12-APSK 4th: -30 dB<br>10 16-QAM 4th: -30 dB<br>4+12-APSK 4th: -20 dB<br>16-QAM 4th: -20 dB<br>10-4 4+12-APSK 4th: -15 dB<br>16-QAM 4th: -15 dB<br>4+12-APSK 4th: -10 dB<br>-5 16-QAM 4th: -10 dB<br>10<br>0 1 2 3 4 5 6 7 8 9 10<br>Eb/N0 [dB]<br>BER<br>**----- End of picture text -----**<br>


**Figure 22 Simulated BER performance for different power levels of the fourth path in the presence of the turbo code.** 

Page 13 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

It must be said that the following considerations hold under the assumptions to be far away from the error floor and that both the residual nonlinearity and multipath are not negligible. If these hypotheses are not satisfied, a more involved analysis is necessary that, however, is outside the goals of this article. 

Let us suppose that the target BER is 10[−][3] , such that the optimal working point for the HPA can be obtained from Figure 6, that is, OBO = 2 dB for 4 + 12-APSK and OBO ≈ 3.1 dB for 16-QAM. First of all, we wish to check that the DFE is basically ineffective against the residual nonlinearity, and, hence, the latter can be obtained from Figure 6, as the difference TD − OBO. For this purpose, we have simulated the linear system and the nonlinear one in the presence of the DFE with _ρ_ = 0.3. The results are reported in Figure 23. Obviously, the considered values of OBO are optimal for the case of BER = 10[−][3] , while they should be changed for different BER values (see Figure 7 for BER = 10[−][5] ). From the figure we see that, as expected, in spite of the optimization, the curve for the nonlinear system exhibits a penalty of about 1 dB for the 4 + 12-APSK constellation and about 0.7 dB for the 16QAM constellation. These values correspond, with very good approximation, to the gap between the value of TD and the point TD = OBO in Figure 6. Hence, it is confirmed that such residual nonlinearity is well estimated through the TD analysis, while it remains the same after introduction of the DFE. 

Then, the simulation has been repeated by introducing a three paths profile with PDP =[ 0, −3, −6] dB. This way, the system simultaneously includes nonlinearity and multipath. The performance of the complete system is also shown in Figure 23. 

**==> picture [206 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
100<br>4+12-APSK, lin.<br>16-QAM, lin.<br>4+12-APSK, nonlin. only<br>10-1 16-QAM, nonlin. only4+12-APSK, nonlin. + mp<br>16-QAM, nonlin. + mp<br>10-2<br>10-3<br>10-4<br>0 2 4 6 8 10 12 14 16 18 20<br>Eb/N0   [dB]<br>**----- End of picture text -----**<br>


**Figure 23 Performance in the presence of nonlinearity, with and without multipath, by assuming the optimum OBO value at BER** = **10[-3] .** A DFE with _ρ_ = 0.3 is applied. The linear channel is used as a reference. 

From Figure 14, we know that the loss due to multipath is about 3 dB at BER = 10[−][3] . From Figure 23, we see that the total loss of the system when both the nonlinearity and the multipath are present is about 5 dB; we observe that this total penalty can be obtained by linearly summing the loss due to the residual nonlinearity and the multipath. Explicitly, in fact, we have 10 log10 �10[1] _[/]_[10] + 10[3] _[/]_[10][�] = 5.12 dB for the 4 + 12APSK and 10 log10 �10[0.7] _[/]_[10] + 10[3] _[/]_[10][�] = 5.01 dB for the 16-QAM, respectively. 

Based on this and other simulations we have developed in similar conditions, we can conjecture that the residual nonlinearity and multipath can be considered independent, and a reliable approximation of the total loss can be obtained by linearly summing the two contributions. A formal demonstration of this result could be obtained by studying the distribution of the residual nonlinearity (a uniform distribution is expected, but this shall be proved). On the contrary, we have verified that the approximation cannot be used neither when the BER is close to the error floor, as expected, nor when one of the two contributions is very small, as obvious. In the latter case, in fact, only one loss is relevant, and there is no need to combine them. 

## **Conclusion** 

This article provides a performance assessment of the APSK modulation in high data rate wireless tactical networks for land mobile scenarios, and a comparison with conventional square QAM. Assuming a modulation order of 16 as a test case, we have compared 4+12-APSK and 16QAM, in terms of both average and instantaneous BER, in a number of different conditions: in time-invariant and slow fading channels, with and without the application of a turbo channel code, in land mobile scenarios with and without a LOS component. Attention has also been devoted to the impact of unexpected paths, that are not taken into account in the equalizer design. 

In general, the APSK solution has shown a very limited power loss with respect to QAM, and even some advantage, in the considered scenarios, when turbo coding is used. This can make 4 + 12-APSK preferable to 16-QAM when the nonlinearities due to HPAs, e.g., typical SSPAs for handheld devices, are taken into account. In particular, we have shown that, when using adaptive predistortion, APSK allows reducing the output back-off, at the optimal working point, by about 1 dB, with a similar improvement on the total degradation. 

Obviously, high order modulation schemes are much more sensitive to channel conditions, especially when affected by fading. However, when a LOS component is present, these modulation schemes are advantageous because they allow to reach higher bit rates, thus increasing the number of applications. So, a possible use of APSK in land mobile tactical scenarios is for vehicular 

Page 14 of 14 

Baldi _et al. EURASIP Journal on Wireless Communications and Networking_ 2012, **2012** :317 http://jwcn.eurasipjournals.com/content/2012/1/317 

applications, where more favorable propagation conditions (in particular, a high probability to have the LOS component) can make the improvement achievable even greater than for handheld devices. 

Further study will concern the implementation of this system on an FPGA hardware architecture, in such a way as to evaluate the complexity issues as well. 

## **Endnote** 

> aMore precisely, a pure memoryless nonlinearity cannot introduce distortion in the phase of the input signal: for this reason, in the literature, when describing an HPA with AM/AM and AM/PM curves, the model is said to be quasi-memoryless [20]. 

## **Competing interests** 

The authors declare that they have no competing interests. 

## **Acknowledgements** 

This study was supported in part by the MIUR project “ESCAPADE” (Grant RBFR105NLC) under the “FIRB - Futuro in Ricerca 2010” funding program. 

## **Author details** 

1Dipartimento di Ingegneria dell’Informazione, Universit`a Politecnica delle Marche, via Brecce Bianche 12, 60131 Ancona, Italy.[2] Thales Italia, Via Enrico Mattei 20, 66100 Chieti Scalo, Italy. 

Received: 11 April 2012 Accepted: 1 October 2012 Published: 19 October 2012 

## **References** 

1. MC Thomas, MY Weidner, SH Durrani, Digital amplitude-phase keying with _M_ -ary alphabets. IEEE Trans. Commun. **22** (2), 168–180 (1974) 

2. M Baldi, F Chiaraluce, G Cancellieri, Finite-Precision Analysis of Demappers and Decoders for LDPC-coded M-QAM Systems. IEEE Trans. Broadcast. **55** (2), 239–250 (2009) 

3. F Adachi, M Sawahashi, Performance analysis of various 16 level modulation schemes under Rayleigh fading. Electron Lett. **28** (17), 1579–1581 (1992) 

4. RR M¨uller, U Wachsmann, JB Huber, in _Proc. IEEE International Symposium on Information Theory (ISIT 1997)_ . Multilevel coding for peak power limited complex Gaussian channels, (Ulm, Germany, 1997) p. 103 

5. KP Liolis, R De Gaudenzi, N Alagha, A Martinez, A Guill´en i F`abregas, _Amplitude Phase Shift Keying Constellation Design and its Applications to Satellite Digital Video Broadcasting_ , (2010). http://www.intechopen.com 

6. YC Adachi, AR Nix, JP McGeehan, Analysis of 16-APSK modulation in AWGN and Rayleigh fading channel. Electron Lett. **28** (17), 1608–1610 (1992) 

7. TT Tjhung, F Adachi, KH Tan, On the diversity reception of narrowband 16 star-QAM in fast Rician fading. IEEE Trans. Veh. Technol. **46** (4), 923–932 (1997) 

8. Y Ma, QT Zhang, R Schober, S Pasupathy, Diversity reception of DAPSK over generalized fading channels. IEEE Trans. Wirel. Commun. **4** (4), 1834–1846 (2005) 

9. HG Myung, DJ Goodman, _Single Carrier FDMA: a New Air Interface for Long Term Evolution_ . (Wiley, New York,2008) 

10. GE Corazza, _Digital Satellite Communications_ . (Springer, New York,2007) 11. L Giugno, M Luise, V Lottici, Adaptive pre- and post-compensation of nonlinear distortions for high-level data modulations. IEEE Trans. Wirel. Commun. **3** (5), 1490–1495 (2004) 

12. G Karam, H Sari, A data predistortion technique with memory for QAM radio systems. IEEE Trans. Commun. **39** (2), 336–344 (1991) 

13. ETSI EN 302 307 V121: Digital Video Broadcasting (DVB); Second Generation Framing Structure, Channel Coding, and Modulation Systems for Broadcasting, Interactive Services, News Gathering and Other Broadband Satellite Applications (2009) 

14. R de Gaudenzi, A Guill´en i F`abregas, A Martinez, Turbo coded APSK modulations design for satellite broadband communications. Int. J. Satellite Commun. Network. **24** , 261–281 (2006) 

15. M Baldi, F Chiaraluce, A de Angelis, R Marchesani, S Schillaci, in _Proc. 16th IEEE Symposium on Computers and Communications (ISCC’11)_ . Performance of APSK modulation in wireless tactical scenarios for land mobile systems, (Corfu, Greece, 2011) pp. 591–596 

16. T Camp, J Boleng, V Davies, A survey of mobility models for ad hoc network research. Wirel. Commun. Mob. Comput. **2** (5), 483–502 (2002) 

17. M Baldi, M Bianchi, F Chiaraluce, in _Proc. IEEE Information Theory Workshop (ITW 2010)_ . Non-systematic codes for physical layer security, (Dublin, Ireland, 2010) pp. 1–5 

18. JH Kim, CS Sin, SU Lee, JH Kim, in _Proc 6th International Conference on Information Communication and Signal Processing (ICICS 2007)_ . Improved performance of APSK modulation scheme for satellite system, (Singapore, 2007) 

19. P Ali, F Hussain, J Jeong, in _Proc. 3th International Conference on Convergence and Hybrid Information Technology (ICCIT 2008)_ . A new demapping technique for 16-APSK modulation for digital video broadcasting in AWGN channel, (Busan, South Korea, 2008). pp. 9–12 

20. MC Jeruchim, P Balaban, KS Shanmugan, _Simulation of Communication Systems: modeling, methodology and techniques_ , 2nd edn. (Kluwer Academic Press, New York,2002) 

21. G Albertazzi, GE Corazza, A Vanelli-Coralli, S Cioni, M Iubatti, M Neri, R Pedone, M Villanti, Performance evaluation of APSK modems. Tech. rep. ARCES - Thales Italia Partnership (2003) 

22. C Rapp, in _2nd European Conference on Satellite Communications_ . Effects of HPA - Nonlinearity on a 4-DPSK/OFDM signal for a digital sound broadcasting system, (Li`ege, Belgium, 1991) pp. 179–184 

23. AA Saleh, Frequency - independent and frequency - dependent nonlinear models of TWT amplifiers. IEEE Trans. Commun. **29** (11), 1715–1720 (1981) 

24. YR Zheng, C Xiao, Simulation models with correct statistical properties for Rayleigh fading channels. IEEE Trans. Commun. **51** (6), 920–928 (2003) 

25. R De Gaudenzi, A Guill´en i F`abregas, A Martinez, Performance analysis of turbo-coded APSK modulations over nonlinear satellite channels. IEEE Trans. Wirel. Commun. **5** (9), 2396–2407 (2006) 

26. TS Rappaport, _Wireless Communications_ . (Prentice Hall, Upper Saddle River,2001) 

27. N Benvenuto, S Tomasin, Block iterative DFE for single carrier modulation. Electron Lett. **38** (19), 1144–1145 (2002) 

28. C Berrou, A Glavieux, Near optimum error correcting coding and decoding: Turbo-codes. IEEE Trans. Commun. **44** (10), 1261–1271 (1996) 

29. 3GPP: 3GPP TS 25.212; 3rd Generation Partnership Project; Technical Specification Group Radio Access Network; Multiplexing and Channel Coding (FDD). 9.1.0 (2009) 

30. MC Valenti, J Sun, The UMTS turbo code and efficient decoder implementation suitable for software-defined radios. Int. J. Wirel. Inf. Netws. **8** (4), 203–215 (2002) 

31. S Daumont, B Rihawi, Y Lout, in _Proc. 3rd International Symposium on Communications, Control, and Signal Processing (ISCCSP 2008)_ . Root-raised cosine filter influences on PAPR distribution of single-carrier signals, (Malta, 2008). pp. 841–845 

32. M Tanahashi, H Ochiai, Near constant envelope trellis shaping for PSK signaling. IEEE Trans. Commun. **57** (2), 450–458 (2009) 

33. M Gomes, V Silva, F Cercas, M Tomlinson, in _Proc. IEEE International Conference on Communications (ICC 2010)_ . Analytical analysis of polyphase magnitude modulation method’s performance, (Cape Town, South Africa, 2010) 

34. JG Proakis, M Salehi, _Communication Systems Engineering_ . (Prentice Hall, Upper Saddle River,2002) 

35. N Benvenuto, G Cherubini, _Algorithms for communication systems and their applications_ . (Wiley, New York,2002) 

doi:10.1186/1687-1499-2012-317 

**Cite this article as:** Baldi _et al._ : A comparison between APSK and QAM in wireless tactical scenarios for land mobile systems. _EURASIP Journal on Wireless Communications and Networking_ 2012 **2012** :317. 


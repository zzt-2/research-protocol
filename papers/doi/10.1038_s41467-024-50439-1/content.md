https://doi.org/10.1038/s41467-024-50439-1 



### Article 

# Overcoming laser phase noise for low-cost coherent optical communication 

Received: 15 December 2023 Accepted: 9 July 2024 Check for updates 





Xiansong Fang<sup>1,4</sup> , Yixiao Zhu 2,4 , Xiang Cai<sup>1</sup> , Weisheng Hu<sup>3</sup> , Zhixue He<sup>3</sup> , Shaohua Yu 1,3 & Fan Zhang1,3 

Artificial-intelligence-generated content has driven explosive data traffic growth in data-center interconnects. Traditional direct detection solutions struggle with limited spectral efficiency and distance, prompting the shift to coherent optics for cost-sensitive short-reach links. One specific challenge is integrating low-cost lasers while overcoming severe phase noise on high-order modulation formats. Here, we propose a residual carrier modulation scheme for precise and efficient carrier frequency and phase recovery. The residual optical carrier can continuously track phase fluctuations without redundancy compared with discrete time-domain pilots, and address the digital-to-analog convertor resolution reduction issue of frequency-domain digital pilots. In proof-of-concept experiments, we transmit a net 1-Tb/s probabilistic-shaped 256-ary quadrature amplitude modulated (PS-256-QAM) signal using a 3 MHz distributed feedback (DFB) laser. Our scheme improves bitrate by 41% compared to conventional time-domain pilots, achieving a record laser linewidth sum and symbol duration product of 6.89 × 10<sup>−5</sup> . This approach supports MHz linewidth DFB lasers in low-cost coherent optical communications. 

The modern information society relies on the optical fiber infrastructure, which is responsible for >99% of global data transmission and exchange. As the era of emerging artificial intelligence-generated content (AIGC) unfolds, significant volumes of data are generated at the cloud side and distributed to end-users. Consequently, there is evident traffic growth in the short-reach scenarios (Fig. 1a), including data-center interconnects<sup>1,2</sup> and fiber-wireless access networks<sup>3,4</sup> . Different from long-haul transmission<sup>5,6</sup> , short-reach scenarios have abundant fiber resources, allowing for massively parallel deployment<sup>7,8</sup> . Hence, there is a stringent requirement for costeffective transceivers, particularly the laser source. 

The optical transmission systems can be divided into two categories: direct detection and coherent detection<sup>9</sup> . The traditional direct detection solution employs only one-dimensional power detection, whereas coherent detection can fully utilize the phase and polarization diversity based on a reference laser, namely the local oscillator (LO). 

However, as the signal laser and LO originate from different sources, the phase noise becomes a critical impairment for coherent receivers<sup>10</sup> . Theoretically, laser phase noise is modeled as a Wiener process<sup>11</sup> , and its variance is determined by the product of the symbol duration and the linewidth sum of signal laser and LO. 

As the Ethernet interface is speeding up from 800GbE to 1.6TbE and beyond, the adoption of multi-level modulation formats emerges as a promising solution to overcome the bandwidth limitation of optoelectronic devices and components<sup>12</sup> . For decades, intensitymodulation with direct detection (IM-DD) scheme in Fig. 1b has dominated optical interconnects, thanks to its cost and simplicity advantages. However, the square-law detection of the photodiode imposes fundamental restrictions. More specifically, the line rate is mainly limited by amplitude-only one-dimensional modulation, and the distance is hindered by the fiber chromatic dispersion-induced power fading effect, primarily due to the loss of phase information<sup>13</sup> . 

> 1State Key Laboratory of Advanced Optical Communication Systems and Networks, Frontiers Science Center for Nano-optoelectronics, School of Electronics, Peking University, Beijing 100871, China.<sup>2</sup> State Key Laboratory of Advanced Optical Communication Systems and Networks, Department of Electronic Engineering, Shanghai Jiao Tong University, Shanghai 200240, China.<sup>3</sup> Peng Cheng Laboratory, Shenzhen 518055, China.<sup>4</sup> These authors contributed equally: Xiansong Fang, Yixiao Zhu. e-mail: yixiaozhu@sjtu.edu.cn; fzhang@pku.edu.cn 

Nature Communications |  (2024) 15:6339 

1 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
a Data-center interconnect Mobile fronthaul Passive optical network<br>AI<br>b c IQ Mod. Fiber d<br>Laser MZM Fiber PD Laser Laser IQ Mod. Fiber<br>I<br>I Q ICR I<br>Q ICR<br>APC<br>LO<br>f f f f f f f f f<br>IM-DD Self-Coherent Detection Intradyne Coherent Detection<br>e 10-kHz Linewidth 100-kHz Linewidth 1-MHz Linewidth<br>��� ��� ���<br>��� ��� ���<br>��� ��� ���<br>� � �<br>���� ���� ����<br>� � � � � � � � � � � � � � �<br>��������� ��������� ���������<br>w/o CPR w/ CPR w/o CPR w/ CPR w/o CPR w/ CPR<br>�� �� ��<br>��� ��� ���<br>� � �<br>� � �<br>�� �� ��<br>��� ��� ���<br>� � �<br>� � �<br><!-- End of picture text -->

Fig. 1 | Conventional optical transmission structures and the phase noise challenge for low-cost lasers in coherent detection. a Short-reach optical transmission applications, encompassing data-center interconnects, mobile fronthaul, and passive optical networks. AI artificial intelligence. b The architecture of intensity-modulation with direct detection (IM-DD) scheme. DFB laser distributed feedback laser, MZM Mach-Zehnder modulator, PD photodiode. c The architecture of self-coherent schemes. IQ Mod. in-phase/quadrature (IQ) modulator, APC 

automatic polarization controller, ICR integrated coherent receiver. d The architecture of the intradyne coherent detection scheme. ECL external cavity laser, LO local oscillator. e The numerically simulated phase fluctuation and constellations of the intradyne coherent detected signal with laser linewidth sum of 10 kHz, 100 kHz, and 1 MHz. CPR carrier phase recovery, w/o without, w/ with. Here the CPR refers to the conventional time-domain pilot enabled phase recovery. The simulation is based on a 45-Gbaud 64-ary quadrature amplitude modulation (64-QAM) signal. 

To extend the spectral efficiency and distance, self-coherent schemes are also potential candidates<sup>14,15</sup> . As illustrated in Fig. 1c, an optical carrier co-propagates with the information-bearing signal through an additional dimension, such as the spatial dimension in selfhomodyne architecture. The optical carrier serves as a remote LO for signal recovery. With accurate optical path matching between the fiber pair<sup>16</sup> , the laser phase noise can be mostly canceled. Nevertheless, remote LO halves the average spectral efficiency per fiber, and the randomly varying polarization state of the remote LO requires sophisticated endless polarization controllers<sup>15</sup> or complementary branches<sup>17</sup> in the receiver structure. 

Moreover, the intradyne coherent receiver in Fig. 1d is widely deployed in long-haul and metro networks. It has the merit of superior receiver sensitivity, 4-dimensional modulation, and efficient digital compensation of channel impairments. Equipped with the highbandwidth in-phase/quadrature (IQ) modulator<sup>18</sup> , capacity-approaching probabilistic shaping (PS) technique<sup>19</sup> , and precise in-phase/quadrature imbalance correction<sup>20</sup> , state-of-the-art coherent systems have stridden over 2 Tb/s data rate in a single channel<sup>21</sup> , or surpassed the spectral efficiency of 20 bit/s/Hz<sup>22</sup> leveraging kHz-level narrow linewidth lasers. However, when migrating to the cost-sensitive scenarios, distributed feedback (DFB) lasers with several MHz linewidth are preferred, making it difficult to recover high-order modulation formats. 

The laser phase noise is one of the foremost impairments in coherent receivers, which stems from the unpredictable phase fluctuations between signal and LO lasers. As depicted in Fig. 1e, such phase noise causes a random and time-varying rotation on the signal constellation, where a larger linewidth corresponds to greater phase ambiguity. To combat this problem, commercial coherent optical transponders use carrier phase recovery (CPR) in the digital domain. This technique estimates the phase noise by transmitting receiverknown symbols as pilot symbols, and then inversely rotates the neighboring payloads<sup>23</sup> . Notably, the frame redundancy inevitably leads to the sacrifice of spectral efficiency. More importantly, with MHz-class linewidth lasers, the relative phase fluctuates rapidly over time, making it no longer a reliable estimation of adjacent symbols. Alternatively, a radio-frequency (RF) pilot tone-based phase recovery technique<sup>24,25</sup> is proposed, but it consumes precious quantization bits of DACs, enhancing the quantization noise and degrading signal SNR. Although an optical generation of pilot tone has been demonstrated with OFDM modulation<sup>26</sup> , OFDM is much more susceptible to phase noise due to its longer symbol duration. Besides, the potential broad application of optical pilot tone in modern optical communication remains unexplored. Furthermore, overcoming phase noise in highorder modulation standard coherent systems with low-cost lasers has not yet been demonstrated. 

Nature Communications |  (2024) 15:6339 

2 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
I<br>DSP<br>Q SSMF ICR (CPR)<br>DFB laser IQ Mod. LO<br>Power Time Time<br>CPR<br>Bias (TP)<br>Tx  Rx<br>Null point Freq. Laser Laser Freq.<br>f f<br>0 0<br>Power Time Noise Time<br>CPR<br>Bias (RCM)<br>Above null point Freq. Freq.<br>f f<br>0 0<br><!-- End of picture text -->



<!-- Start of picture text -->
1 2<br>0 � f f<br><!-- End of picture text -->



<!-- Start of picture text -->
1 2<br>0 f<br><!-- End of picture text -->



<!-- Start of picture text -->
1 2<br>0 f<br><!-- End of picture text -->



<!-- Start of picture text -->
0 f<br><!-- End of picture text -->

Fig. 2 | Concept of the proposed residual carrier modulation (RCM) scheme. a The architecture of low-cost standard coherent transceivers using distributed feedback (DFB) laser at the transmitter and receiver. IQ Mod. in-phase/quadrature modulator, SSMF standard single-mode fiber, LO local oscillator, ICR integrated coherent receiver. The comparison of b conventional time-domain pilot (TP) and c the proposed RCM enabled carrier phase recovery (CPR). The constellation diagrams and optical spectra at the transmitter, the received electrical spectra, and 

constellation diagrams after phase recovery are shown. The direct current (DC) bias of modulators is plotted on the left of the transmitter spectra. Freq. frequency, Tx transmitter, Rx receiver. d The digital signal processing procedure for the residual carrier modulation to recover the phase. Δf is the estimated frequency offset value. �f g<sup>*</sup> denotes the complex conjugate operation. FOE frequency offset estimation, LPF low-pass filter. e The frame structure of the time-domain pilot-based CPR. f The principle of frequency-domain pilot tone-based CPR. 

In this work, we present a residual carrier modulation (RCM) technique integrated with subcarrier multiplexing to achieve high-speed and high spectral efficiency in modern coherent optical communication systems using low-cost, large linewidth lasers. Our quantitative evaluation demonstrates the advantage of our phase tracking method over conventional time-domain and frequency-domain pilot techniques. We also showcase its potential in diverse scenarios such as data-center interconnects and fiber-wireless access networks. By slightly adjusting the bias point of the IQ modulator, we introduce the residual carrier that originates from the identical laser source as the signal. This approach enhances the tracking ability of phase noise by facilitating the beating between the signal and residual carrier in the digital domain. For the data-center interconnect scenario, we achieve net single-channel 1.0-Tb/ s PS-256-QAM signal transmission over 80-km standard single-mode fiber (SSMF) using a 3-MHz linewidth laser. For high-capacity transmission, the residual carrier introduces negligible optical signal-to-noise ratio (OSNR) reduction and is well-suited for 16 × 900-Gb/s wavelengthdivision-multiplexed (WDM) data-center interconnects using transceiver laser with both 1-MHz linewidths. For the fiber-wireless access network scenario, we report high-fidelity analog radio-over-fiber fronthaul 

delivering 512-QAM signals, leading to a >2-Tb/s common public radio interface (CPRI)-equivalent rate within only 18.85-GHz optical bandwidth. The proposed methodology integrates the concept of selfhomodyne detection with the conventional intradyne coherent system, thus significantly relaxing the hardware requirement. This reshapes various short-reach optical communications in the age of artificial intelligence. 

## Results 

#### Phase recovery using residual carrier modulation 

In the standard intradyne coherent architecture (Fig. 2a), the utilization of a low-cost DFB laser can cause severe phase noise due to the rapid and independent phase fluctuations between the signal laser and LO. The conventional approach inserts time-domain pilot (TP) symbols periodically between the blocks of payload symbol to probe the phase rotation (Fig. 2e). However, for lasers with a large linewidth, the recovered constellation diagrams are still blurred as the TP struggles to track rapid phase changes (Fig. 2b). Figure 2c illustrates the concept of residual carrier modulation. At the transmitter, the IQ modulator operates at a bias point slightly deviated from the null point, 

Nature Communications |  (2024) 15:6339 

3 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
a SP IQ Mod.1 optical link<br>CUT CH1 CH2 electrical link<br>λ<br>100-kHz ECL/1-MHz DFB/ (120 GSa/s)AWG PBC ... ... λ ... ... λ<br>3-MHz DFB<br>CH3 CH4 80-km SSMF<br>SP IQ Mod.2<br>Loading channels<br>ECL #1 CH1 CH2 EDFA EDFA OBPF 90°<br>ECL #2 EA WSS 100-kHz ECL/ Optical Hybrid<br>SP IQ Mod.3<br>1-MHz DFB/<br>ECL #15 PDM-E EDFA 3-MHz DFB LO<br>... ... BPD<br>λ λ<br>b c<br>−10 w/o carrier 0<br>w carrier<br>−20<br>−30<br>−40<br>−50 −60<br>1552.4 1552.7 1553.0 1553.3 1553.6 −90 −45 0 45 90 −2 −1 0 1 2<br>Frequency (GHz) Frequency (GHz)<br>Wavelength (nm)<br>GSa/s)<br>RTO<br>(256<br>... PM-OC<br>)Bm )B<br>(d (d<br>re re<br>Pow Pow<br><!-- End of picture text -->

Fig. 3 | Residual carrier modulation-enabled terabit coherent transmission system with high-order modulation formats. a The experimental setup of 16-channel wavelength-division multiplexed (WDM) probabilistic-shaped 256-ary quadrature amplitude-modulation (PS-256-QAM) signals. CUT channel under test, ECL external cavity laser, DFB distributed feedback laser, CH channel, PM-OC polarization-maintaining optical coupler, SP IQ Mod. single-polarization in-phase/ quadrature modulator, PBC polarization beam combiner, EA electrical amplifier, 

PDM-E polarization-division-multiplexing emulator, EDFA erbium-doped fiber amplifier, SSMF standard single-mode fiber, WSS wavelength-selective switch, OBPF optical band-pass filter, LO local oscillator, BPD balanced photodetector, RTO real-time oscilloscope. b The measured optical spectra of the channel under test with or without the residual carrier. w/ with, w/o without. c The received electrical spectrum after frequency offset removal. 

generating a residual optical carrier for frequency and phase recovery. To cut off the crosstalk from the signal band, we propose the integration of dual-band subcarrier modulation (SCM)<sup>27</sup> to reserve a narrow guard band. After beating with the LO at the receiver, the residual carrier becomes the same blurred as the signal bands. Nonetheless, we leverage it for phase recovery. It should be noted that the frequency offset prevents the residual carrier from being blocked in the receiver analog circuit. As depicted in Fig. 2d, we initially remove the frequency offset by identifying the peak in the electrical spectrum and downconvert the signal and residual carrier to the baseband. A digital lowpass filter (LPF) is then employed to extract the residual carrier. The signal and residual carrier are subsequently beaten in the digital domain to simultaneously eliminate the two components of phase noise, as elaborated in Eq. (1). 



Here φ<sup>0</sup> S<sup>and φ0</sup> RC<sup>represent the phase of the digital signal and residual</sup> carrier after signal-LO beating. φS, φLO and φRC denote the phase of the optical signal, LO, and residual carrier, respectively. Similar to the concept of self-homodyne detection, the signal and the residual carrier originate from the same laser and traverse the same optical path. One essential difference is that the beating of the signal and residual carrier is accomplished in the digital domain, relaxing the hardware requirement. Additionally, residual carrier modulation eliminates the frame redundancy and offers modulation format transparent signal processing. 

In contrast to the traditional pilot-based phase recovery method, our approach offers substantial improvements. The TP-based phase 

recovery, involving the insertion of uniformly distributed time-domain pilot symbols at the transmitter as in Fig. 2e, aids in phase tracking at the receiver after channel equalization. However, it is not optimal from the point of the entire mathematical system model. In the coherent system, the transmitted signal first undergoes distortion due to fiber channels and is subsequently influenced by phase noise at the receiver. Therefore, in the absence of the mathematical commutative property, compensating for phase noise should precede the application of the channel equalizer to mitigate inter-symbol interference (ISI)<sup>10</sup> . An alternative phase recovery scheme involves utilizing a RF pilot tone<sup>24,25</sup> , as depicted in Fig. 2f. This method introduces a frequency-domain RF tone in the digital signal processing (DSP) stage before the digital-toanalog converter (DAC) at the transmitter. Filtering the pilot tone at the receiver also allows for phase noise mitigation. Nevertheless, a drawback lies in the RF pilot tone’s occupation of the precious effective number of bits (ENOB), thereby amplifying quantization noise. 

#### Experimental setup of low-cost coherent system 

Figure 3 a illustrates a 16-channel WDM high-speed coherent transmission system with different laser linewidth configurations. For the channel under test (CUT), we employ a 100 kHz external cavity laser (ECL), 1-MHz DFB laser, or 3 MHz DFB laser as the signal laser source to evaluate transmission performance under varying phase noise conditions, respectively. A 120-GSa/s arbitrary waveform generator (AWG) with 45 GHz 3-dB bandwidth generates the eletrical 2 × 45-GBaud PS-256-QAM signal. We use two single-polarization IQ modulators to realize polarization-division-multiplexing (PDM). Both modulators are biased slightly above the null point to introduce the residual optical carrier. The transmitted optical spectrum of the CUT seeded by a 3 MHz linewidth DFB laser is depicted in Fig. 3b. For the loading 

Nature Communications |  (2024) 15:6339 

4 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
ii<br>NGMI Limit<br><!-- End of picture text -->



<!-- Start of picture text -->
i CSPR = -23.4dB ii CSPR=-3.4dB<br><!-- End of picture text -->



<!-- Start of picture text -->
i<br>CSPR = -23.4 dB<br> CSPR = -13.4 dB<br>CSPR = -3.4 dB<br><!-- End of picture text -->



<!-- Start of picture text -->
iv<br><!-- End of picture text -->



<!-- Start of picture text -->
NGMI Limit<br><!-- End of picture text -->

Fig. 4 | Parameter optimization of residual carrier modulation in singlechannel net 1.0-Tb/s PS-256-QAM transmission. a The measured normalized generalized mutual information (NGMI) for different carrier-to-signal power ratios (CSPR) in the single-channel back-to-back (BTB) scenario. b The transmitted optical spectra with a CSPR of -23.4 dB, -13.4 dB and -3.4 dB, respectively. All the spectra are in 0.02 nm resolution. c The constellation diagrams with a CSPR of -23.4 dB and -3.4 dB. d The measured NGMI for different digital low-pass filter (LPF) bandwidths 

channels, we combine 15 external cavity lasers with 125 GHz spacing using a polarization-maintaining optical coupler. Then, they are fed into another IQ modulator and passed through a split-anddecorrelation-based emulator. The CUT and loading channels are boosted by two erbium-doped fiber amplifiers (EDFA), respectively. We set a programmable wavelength-selective switch to combine and flatten the wavelength channels simultaneously. The WDM superchannel is transmitted through up to 80-km standard single-mode fiber (SSMF). 

At the receiver, we use another laser with a linewidth ranging from 100 kHz–3 MHz as the LO. An optical band-pass filter (OBPF) selects the desired channel. After intradyne coherent detection, the 256 GSa/s real-time oscilloscope (RTO) captures the electrical waveforms for offline digital signal processing. Figure 3c shows the received electrical spectrum after frequency offset removal. For comparative analysis, we also implement the conventional time-domain pilot-based phase recovery method. An equivalent net bitrate is maintained by adopting 

with different signal (Tx) and local oscillator (Rx) lasers with a CSPR of -11.4dB. The configuration includes 3 MHz Tx with 100 kHz Rx, 1 MHz Tx with 1 MHz Rx, and 100 kHz Tx with 100 kHz Rx. Tx, transmitter; Rx, receiver. e The recovered phase for different symbol indexes with a low-pass filter bandwidth (BW) of 180 MHz and 1080 MHz for 3 MHz Tx and 100 kHz Rx lasers. f The measured NGMI for different launch powers in a single-channel 80 km transmission scenario with 3 MHz Tx and 100 kHz Rx lasers with a CSPR of -11.4dB. 

a single-band 90-Gbaud signal with the same modulation format. Detailed descriptions of the digital signal processing stacks are provided in the Methods section. 

#### RCM-enabled 1-Tb/s single-channel transmission with a 3-MHz DFB laser 

In this study, we assess the transmission penalty using the generalized mutual information (GMI), a key metric representing the maximum achievable data throughput for a bit-wise decoder<sup>28</sup> . Notably, the GMI is dependent on the modulation format. After normalization, the normalized GMI (NGMI) becomes a modulation-independent metric for predicting transmission performance after the forward-error correction (FEC), with an abundant NGMI threshold. Therefore, we also use the NGMI to provide the error-free net data rate after FEC. Here, the NGMI threshold is set at 0.857 with a corresponding code rate of 0.826<sup>29</sup> . In the single-channel scenario, we choose a source entropy (maximum achievable GMI) of 13.92 bits per four-dimensional 

Nature Communications |  (2024) 15:6339 

5 

Article 

https://doi.org/10.1038/s41467-024-50439-1 

(4-D) symbol (6.96 bits in each polarization) for evaluation. For WDM transmission, a source entropy of 12.82 bits/4D-symbol is selected. 

A high-quality residual carrier is paramount to achieve optimal digital beating of residual carrier and signal for accurate phase noise cancellation. This entails maintaining an appropriate carrier-to-signal power ratio (CSPR) and ensuring a suitable filter bandwidth to preserve the integrity of the residual carrier. We first optimize the parameters of RCM in the single-channel back-to-back scenario. We choose a digital Gaussian filter to extract the residual carrier. As shown in Fig. 4a, a CSPR of -11.4 dB is sufficient, ensuring that the phase information remains untainted by noise or interference. Since the power of the residual carrier is much smaller than the signal, the reduction in the effective optical signal-to-noise ratio is less than -0.3 dB (see Supplementary Note 5), which can be ignored. The measured transmitted optical spectra are shown in Fig. 4b. Subsequently, we delve into an assessment of the low-pass filter (LPF) bandwidth for the extraction of the residual carrier. The measured NGMI for different 3 dB bandwidths of LPF is illustrated in Fig. 4d, considering different laser configurations. To streamline the statement, if not specified, the received LO laser is a 100 kHz ECL. The results highlight the necessity for an adequate LPF bandwidth tailored to the laser linewidth, ensuring the filtration of phase information without introducing excessive noise. As revealed in Fig. 4e, oversized bandwidth introduces high-frequency noise or signal bands that affect the phase information similarly to modulation. Conversely, undersized bandwidths yield overly smoothed results, causing the loss of precise phase change information. With these above optimized parameters, the signal is transmitted over an 80 km fiber link. Figure 4f demonstrates the measured NGMI for different launch powers in the single-channel 80 km SSMF transmission with 3 MHz signal and 100 kHz LO lasers. The optimal launch power is 3 dBm and we obtained an NGMI above the NGMI limit of 0.857. Therefore, the net data rate is 1.0 Tb/s (See methods for the net bitrate calculation of PS signals) considering the FEC overhead with a record laser linewidth sum and symbol duration product of 6.89 × 10<sup>−5</sup> (ref. 30). 

#### Performance of RCM under different laser linewidth configurations 

In this study, we conduct a comprehensive evaluation of the performance of RCM and conventional TP-enabled phase recovery. Firstly, we assess the performance of RCM and TP-enabled phase recovery in simulations where the sole impairment is phase noise. Figure 5a illustrates the phase noise-induced penalty in the required OSNR for the NGMI limit of 0.857 as a function of different linewidth sum and symbol duration product Δf × Ts. The modulation format is PS-256QAM with an entropy of 13.92 bits/4D-symbol. This result emphasizes a significant enhancement achieved by the RCM scheme. The RCM scheme surpasses the upper limit of the TP method and makes it possible for an application of low-cost lasers with linewidth exceeding megahertz. Specifically, for an OSNR penalty of 1 dB, the RCM scheme enhances the maximum tolerable Δf × Ts value by an order of magnitude compared to the TP method, which means the acceptable transceiver laser linewidth sum can be increased from 100 kHz to 1 MHz for the 45-Gbaud PS-256-QAM signal. 

In our proof-of-concept single-channel experiments, the NGMI with different received OSNR values at the back-to-back scenario is measured, as shown in Fig. 5b. We observe that the combination of 1 MHz and 3 MHz linewidth signal lasers with a 100 kHz LO incurs OSNR penalties of 0.82 dB and 2.05 dB, respectively, compared to the 100 kHz linewidth ECL. These penalties are quite close to the simulation result in Fig. 5a, where the 1 MHz and 3 MHz lasers bring OSNR penalties of 0.5 dB and 1.25 dB, respectively. Besides, as the phase noise is related to the laser linewidth sum of signal and LO lasers, the exchange of signal and LO lasers will not bring OSNR penalty at the back-to-back case, as shown in the 3 MHz Tx laser or 3 MHz Rx laser curves in Fig. 5b. 

Figure 5c demonstrates the phase recovery performance of the conventional TP scheme. Although the gross GMI will improve and saturate as the increase of pilot ratio, a significant gap is observed when substituting the signal laser from 100-kHz ECL to 3 MHz DFB. Moreover, regarding the net GMI excluding the pilot overhead, the penalty is even greater. Specifically, the net GMI penalty is 3.13 bits/4Dsymbol. However, for the residual carrier modulation, this penalty is only 0.17 bits/4D-symbol. For the same data rate PS-256-QAM signal with the 3 MHz signal laser and 100 kHz LO, the RCM improves the net GMI from 8.39 bits/4D-symbol to 11.85 bits/4D-symbol compared to TP-based phase recovery, corresponding to 41.2% enhancement in the net bitrate. The recovered constellations with RCM and TP schemes are shown in Fig. 5e. A significant signal quality improvement can be obtained by the RCM, especially for the 3 MHz linewidth case. Figure 5f compares the phase recovery performance of the proposed RCM and RF pilot tone-based phase recovery. The measured NGMI is presented for the same data rate PS-256-QAM signal, using a 3 MHz signal laser and a 100 kHz LO at the back-to-back scenario with varying receiver-side pilot tone-to-signal power ratios (PTSPR). Receiver-side PTSPR denotes the measured power ratio between the pilot tone and signal in the electrical domain. As RF pilot tone scheme can also track phase continuously, at moderate pilot tone power levels (approximately −20 dB PTSPR), it exhibits comparable performance to RCM. However, as the RF pilot tone occupies the DAC quantization bits, further increasing its power leads to enhanced quantization noise, thereby degrading NGMI performance. In contrast, RCM scheme can further improve performance by increasing the PTSPR. The peak GMI performance difference between the two schemes is 0.45 bits/4D-symbol (See Supplementary Note 7). Notably, our experiment utilized DACs with 8 bits vertical resolution and an effective number of bits (ENOB) of about 5.5 bits (Keysight 8194A). In practical scenarios with lower DAC resolution, the advantage of RCM would be even more pronounced. 

To evaluate the performance of RCM after transmission, we show the measured GMI of different transceiver laser configurations after single-channel 80 km fiber transmission in Fig. 5d. For a fair comparison, the OSNR values of the transmitted signal are fixed at 40 dB in all the laser configurations. It can be observed that the exchange of the signal laser and LO with different linewidths, while maintaining the same laser linewidth sum and symbol duration product, will not introduce obvious performance variation. The slight degradation when the linewidth of the LO laser is larger is attributed to the equalization-enhanced phase noise (EEPN)<sup>31</sup> . 

#### The 16-channel WDM Transmission using low-cost DFB transceiver lasers 

Traditional self-coherent schemes typically necessitate a high CSPR, commonly around 10 dB<sup>32–34</sup> , to mitigate the signal-signal beating interference (SSBI) as a perturbation. However, this prerequisite imposes limitations on the number of signal channels and, consequently, the overall system capacity in a WDM transmission due to the restricted output power of EDFAs<sup>35</sup> . In contrast, the RCM method only requires a typical CSPR value below -10 dB, thereby addressing this limitation. In this study, we assess the WDM transmission performance of RCM to reveal its advantages. The transmitted signal is PS-256-QAM with an entropy of 12.82 bits/4D-symbol. Figure 6a shows the measured NGMI of the 9<sup>th</sup> channel as a function of the launch power per channel, employing signal and LO lasers of 100-kHz ECL or 1-MHz DFB. The GMI reduction associated with 1 MHz transceiver lasers, as compared to 100-kHz transceivers, is merely 0.065 bits per 4D-symbol. The optimal launch power is identified as 1 dBm per channel after an 80 km 16-channel WDM transmission. This analysis reveals a trade-off between the SNR and fiber nonlinearity. In comparison to singlechannel transmission with 1 MHz transceiver lasers, the WDM setup introduces a GMI degradation of only 0.352 bits/4D-symbol 

Nature Communications |  (2024) 15:6339 

6 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



Fig. 5 | Simulation and experimental results of the single-channel probabilisticshaped 256-ary quadrature amplitude-modulation (PS-256-QAM) signal under different transceiver laser setup. a The optical signal-to-noise ratio (OSNR) penalty for different linewidth sum and symbol period product Δf × Ts with conventional time-domain pilot (TP) enabled phase recovery and residual carrier modulation (RCM) under simulation. b The measured normalized generalized mutual information (NGMI) versus the OSNR for different signal (Tx) and local oscillator (Rx) lasersusing RCM in the back-to-back experiment. Tx, transmitter; Rx, receiver. c The measured generalized mutual information (GMI) for the different pilot ratios of the TP-based phase recovery with 100 kHz, 1 MHz, and 3 MHz linewidth signal lasers in the back-to-back experiment at an OSNR of 41 dB. The results 

of RCM are also plotted for comparison. The gross rate and net rate respectively denote the GMI that includes pilot overhead and the GMI that excludes pilot overhead. w, with. d The measured GMI for different signal and local oscillator lasers with RCM at a transmitted OSNR of 40 dB in the 80 km transmission experiment. e The recovered PS-256-QAM constellation for 100 kHz and 3 MHz signal laser with 100 kHz local oscillator using RCM scheme or TP-based phase recovery at an OSNR of 41 dB. LW linewidth, 4D 4-dimensional. f The measured NGMI using RCM or radio-frequency (RF) pilot tone for phase recovery under different receiver-side pilot tone to signal power ratio (PTSPR) with 3 MHz signal laser and 100 kHz local oscillator laser. The receiver-side PTSPR denotes the measured power ratio between the pilot tone and signal in the electrical domain. 

(See Supplementary Note 6). The recovered constellations at the optimal launch power are shown in Fig. 6b. 

Figure 6c illustrates the transmitted optical spectrum of the WDM system. The WDM channels are labeled from channel (CH) 1 to CH 16, arranged from low to high frequency. With RCM-based phase recovery, the 16 channels achieve an average NGMI of 0.90, as depicted in Fig. 6d. All channels are well above the NGMI limit of 0.857 after 80-km SSMF transmission. The net bitrate is 903.2 Gb/s/λ and the aggregated 

capacity adds up to 14.45 Tb/s (16λ × 903.2 Gb/s/λ). The results indicate the feasibility of RCM for low-cost and high-capacity data-center interconnects exceeding 10 Tb/s. 

#### RCM-enabled high-fidelity fiber-wireless access network with 512-QAM signal 

Apart from data-center interconnects, fiber-wireless access networks become increasingly popular in short-reach scenarios. In such 

Nature Communications |  (2024) 15:6339 

7 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
a<br>c<br>-20<br>-40<br>NGMI Limit<br>-60<br>�� �� 192.0 192.5 193.0 193.5 194.0 194.5<br>Frequency (THz)<br>b<br>d 0.92<br>0.88<br>NGMI Limit<br>0.84<br>0.80<br>Tx: 100 kHz linewidth Tx: 1 MHz linewidth 0 2 4 6 8 10 12 14 16<br>Rx: 100 kHz linewidth Rx: 1 MHz linewidth Channel Index<br>)m<br>B<br>d<br>( r<br>e<br>w<br>o<br>P<br>IM<br>G<br>N<br><!-- End of picture text -->

Fig. 6 | Experimental results of 16λ × 903.2-Gb/s/λ wavelength-divisionmultiplexed (WDM) transmission enabled by residual carrier modulation. The modulation format is probabilistic-shaped 256-ary quadrature amplitudemodulation (PS-256-QAM) with an entropy of 12.82 bits/4D-symbol. a The measured normalized generalized mutual information (NGMI) as a function of different launch power per channel at the 9th channel. The linewidth of signal and lasers are 

both 100 kHz or 1 MHz. Tx transmitter, Rx receiver. b The recovered constellations at the optimum launch power for transceiver lasers with different linewidths. c The measured optical spectrum of the transmitted 16-channel WDM signal with a 0.02 nm resolution. d The measured NGMI for all 16 channels. The results are well above the NGMI limit of 0.857. 

networks, fronthaul plays a crucial role in seamlessly connecting mobile and optical communications. The wireless waveforms are distributed from the centralized unit (CU) or distributed unit (DU) to the radio units (RUs) through optical fibers, as depicted in Fig. 7a. The analog radio-over-fiber (RoF) technique, which directly modulates the original wireless signal onto the optical carrier, is promising thanks to its high spectral efficiency and simplicity. As wireless communications are moving towards 1024-QAM, the transceiver distortion and laser phase noise in fronthaul hinder the adoption of high-order modulation format beyond the 64-QAM. 

In this study, we demonstrate the application of the RCM technique for mitigating phase noise in analog RoF for fronthaul. As illustrated in Fig. 7a and b, we separate the left sideband (LSB) and right sideband (RSB) for the downlink and uplink, respectively. Such configuration not only separates the transmitter IQ imbalance-induced crosstalk, but also avoids the backward scattering for bi-directional transmission. Therefore, the SNR bottleneck is considerably alleviated for the analog RoF transmission of high-order modulation formats. The residual carrier, when beaten with the LO, serves for phase recovery, as depicted in the electrical spectra in Fig. 7c. With these impairments mitigated, the SNR can reach 30.8 dB at symbol rate of 17 Gbaud, satisfying the 29.1 dB SNR requirement of the 256-QAM format, as shown in Fig. 7d. This corresponds to an over 2 Tb/s/λ CPRIequivalent rate<sup>36,37</sup> using only an 18.85 GHz optical bandwidth. The SNR gradually degrades with symbol rate, attributed to increased in-band noise and bandwidth limitation. Figure 7e demonstrates the bit-error rate (BER) versus the modulation formats from 128-QAM to 512-QAM at 17 Gbaud. Even for the 512-QAM signal, the BER is well below 1 × 10<sup>−2</sup> . The receiver sensitivity is evaluated to be around -18 dBm at the 15.3% open forward error correction (O-FEC) threshold of 1.8 × 10<sup>−2</sup> for the 512-QAM format, as shown in Fig. 7f. Finally, we assess a 12-channel WDM transmission over 10 km SSMF in Fig. 7g. The BER values of all channels in both the downlink and uplink are well below the O-FEC threshold. Therefore, we successfully demonstrate the transmission of 25.1-Tb/s (12λ × 2.089 Tb/s/λ) aggregated CPRI-equivalent rate and 512- 

QAM signals over 10-km SSMF. Besides, the linewidth is 100 kHz for both signal and LO lasers, corresponding to a record linewidth sum and symbol duration product of 1.18 × 10<sup>−5</sup> for 512-QAM format. By comparing the recovered constellations, the residual carrier modulation-based recovery effectively eliminates the phase blur, particularly for high-order formats, showcasing superior performance compared to the time-domain pilot-based scheme. 

## Discussion 

In summary, our study introduces a pioneering approach to recover the carrier phase by utilizing the residual carrier for beating the carrier and signal in the digital domain, in contrast to the optical beating used in self-coherent systems. This diverges fundamentally from traditional phase recovery methods employed in coherent optical communication systems. The deliberately preserved optical carrier serves as a crucial link connecting the signal phase with the carrier phase contaminated by the phase noise. This innovation enables the utilization of low-cost DFB lasers for conventional intradyne coherent transceivers. The elimination of external cavity lasers has the potential to significantly reduce costs by orders of magnitude. 

Compared to conventional time-domain pilot-aided carrier phase recovery, RCM enhances the tolerable product of linewidth sum and symbol duration (Δf × Ts) by more than an order of magnitude<sup>21,22,38–41</sup> , which facilitates the deployment of low-cost DFB lasers with linewidth exceeding MHz for short-reach coherent transceivers. In the proof-ofconcept experiments, we demonstrate the net 1.0 Tb/s/λ 256-QAM signal transmission with a 3 MHz DFB laser using the RCM scheme, showing a 41% bitrate improvement compared to the time-domain pilot for phase recovery. As shown in Fig. 8a, we have set a record for the product of linewidth sum and symbol duration Δf × Ts with a net bitrate beyond 1 Tb/s. 

Compared to conventional self-coherent architecture, RCM can significantly reduce the operating carrier-to-signal power ratio by around 20 dB. Therefore, the bottleneck of restricted channels for WDM transmission in self-coherent systems no longer exists. We 

Nature Communications |  (2024) 15:6339 

8 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
a<br>CU/DU Downlink ... ...<br>f<br>RU #1 RU #2 RU #3 ... RU #N Uplink ... ...<br>f<br>b -20 c Downlink<br>0<br>-40<br>-20<br>-60<br> Downlink<br>-40<br>-20<br>0 Uplink<br>-40<br>-20<br>-60<br>Uplink<br>193.2 193.4 193.6 193.8 -40<br>-32 -16 0 16 32<br>Frequency (THz)<br>Frequency (GHz)<br>d 32 e 10 -2<br> Downlink<br>30  Uplink 10 -3 iii<br>SNR Limit<br>28<br>ii<br>10 -4<br>26 i<br>24 10 -5  Downlink<br> Uplink<br>22 10 -6<br>16 20 24 28 32 36 128 256 512<br>Symbol Rate (GBaud) QAM Order<br>f 3×10 -2 g 2×10 -2<br>15.3% O-FEC 15.3% O-FEC<br> Downlink 10 -2<br>10 -2  Uplink<br>iv<br> Downlink<br> Uplink<br>2×10 -3 2×10 -3<br>-18 -15 -12 -9 -6 -3 0 3 1 2 3 4 5 6 7 8 9 10 11 12<br>ROP (dBm) Channel Index<br>i 128-QAM SC  ii 256-QAM SC  iii 512-QAM SC  iv 512-QAM WDM (CH3)<br>RCM-based<br>carrier recovery<br>TP-based<br>carrier recovery<br>)<br>( rBdmew ( S)BdD<br>o P<br>P<br>)( rBdPmeow )( SBdDP<br>)B<br>( dRN REB<br>S<br>R R<br>E E<br>B B<br><!-- End of picture text -->

Fig. 7 | Experimental demonstration of residual carrier modulation (RCM) for high-fidelity 512-ary quadrature amplitude-modulation (512-QAM) fiberwireless access networks. a The conceptional illustration of the fronthual connecting the centralized unit (CU) or distributed unit (DU) to the radio units (RUs). The proposed residual carrier-based bi-directional transmission with separate sidebands is illustrated on the right. b The measured optical spectra of the 12-channel 17-Gbaud 512-QAM signal for the downlink and uplink with the left sideband and right sideband. The channels are labeled from CH1 to CH12, arranged from low frequency to high frequency. CH, channel. c The received electrical 

spectra of the central 6th channel for the downlink and uplink. d The recovered signal-to-noise ratio (SNR) versus the symbol rate with 512-QAM at a single channel back-to-back scenario. e The measured bit-error rate (BER) for different modulation formats from 128-QAM to 512-QAM for single-channel 17-Gbaud signal at back-toback. f The measured BER versus received optical power (ROP) with 17-Gbaud 512-QAM signal at single channel back-to-back scenario. g The measured BER for all the 12 WDM channels after 10 km transmission with 17-Gbaud 512-QAM. The insets show the corresponding recovered constellations with residual carrier modulation or time-domain pilot-based (TP) carrier recovery. SC, single channel. 

Nature Communications |  (2024) 15:6339 

9 

Article 

https://doi.org/10.1038/s41467-024-50439-1 



<!-- Start of picture text -->
(Hz)<br>This work<br>Δf ×T<br><!-- End of picture text -->



<!-- Start of picture text -->
(Hz)<br>This work<br>Δf ×T<br><!-- End of picture text -->



<!-- Start of picture text -->
b<br><!-- End of picture text -->



<!-- Start of picture text -->
a<br><!-- End of picture text -->

information rate (IR) per 4D symbol versus the product of laser linewidth sum and symbol duration Δf × Ts. In this work, we report high-order 512-QAM transmission using transceiver lasers with both 100 kHz linewidths. 4D 4-dimensional. 

Fig. 8 | State-of-the-art results. a The net bitrate versus the product of laser linewidth sum and symbol duration Δf × Ts. In this work, we achieve net 1.0-Tb/s PS256-QAM single-channel transmission with a 3-MHz linewidth laser. b The 

demonstrate 16λ × 903.2-Gb/s PS-256-QAM signal transmission over 80 km SSMF using a 1 MHz DFB laser pair as the transceiver laser source, showing only mild performance degradation compared to single-channel transmission. 

To accommodate the phase noise challenge in analog radio-overfiber systems, RCM provides an efficient solution to increase the SNR ceiling in conventional intradyne coherent systems<sup>22,38,39,42–46</sup> . We demonstrate high-fidelity analog RoF signal transmission with a 512-QAM format, which is also based on a record linewidth sum and symbol duration of 1.18 × 10<sup>−5</sup> , as depicted in Fig. 8b. 

The proposed RCM demonstrates a low-cost short-reach solution with minimal hardware complexity, uncompromised effective optical signal-to-noise ratio, and precise modulation-format-transparent phase tracking performance. Beyond its application in optical communication, the concept of residual carrier modulation may find its potential application in various areas such as precision measurement, continuous variable quantum key distribution, frequency-modulated continuous wave Lidar, and other sensing systems. 

## Methods 

#### Detailed experimental setup and DSP stacks for PS-256-QAM transmission 

At the transmitter, the WDM channels are composed of 15 ECLs for loading channels and one laser for the channel under test (CUT). The channel spacing is kept at 125 GHz. As the wavelength of the 1 MHz and 3 MHz DFB lasers is not tunable, we assess the performance of all the WDM channels by periodically changing the wavelength of the loading channels, which alternates the relative position of the CUT to the whole WDM spectrum. The linewidth measurement result is provided in Supplementary Note 1. The baseband PS-256-QAM signal with two subcarriers (45 GBaud × 2) is generated by an arbitrary waveform generator (AWG), with a 3 dB bandwidth of 45 GHz and a sampling rate of 120 GSa/s. All of the three IQ modulators have a 3-dB bandwidth of around 27 GHz. The modulators are biased slightly deviating from the null point (See Supplementary Note 10 for details on the bias control method). Then for the CUT, the signal on two polarizations is individually modulated and combined through the polarization beam combiner (PBC). The loading channels are jointly modulated with another modulator with the conjugate output of the AWG to generate different signals. It was evaluated both in a back-to-back configuration and with 80-km standard single-mode fiber. 

At the receiver, the signal after the optical band-pass filter is sent to the optical 90<sup>∘</sup> hybrid followed by balanced photodiodes (BPDs) with 70 GHz 3 dB bandwidth. It is subsequently sampled by a 256 GSa/s real-time oscilloscope with 59-GHz bandwidth. A detailed singlechannel experimental setup is also depicted in Supplementary Note 2, Fig. S2a. 

The DSP stack is shown in Supplementary Note 2, Fig. S2b. At the transmitter, the data is mapped to 40960 PS-256-QAM symbols first, 

which is framed by a 4352-symbol preamble for synchronization and channel equalization. After up-sampling, the signal is pulse-shaped with a roll-off factor of 0.05. Then the signal is re-sampled to match the sampling rate of AWG. Subsequently, a dual-band subcarrier modulation is conducted with an optimized guard band interval of 2.0 GHz. A linear pre-emphasis is applied to compensate for the transmitter bandwidth limitation. 

At the receiver, the captured signal is first re-sampled to 4 samples-per-symbol (SPS). Then a chromatic dispersion compensation (CDC) is employed for 80 km SSMF transmission. Subsequently, the frequency offset estimation (FOE) and carrier phase recovery are completed with the aid of residual carrier, as shown in Supplementary Note 2, Fig. S2c. After frame synchronization, the channel equalization is performed by 3rd-order Volterra nonlinear equalizer (VNLE). The 1st, 2nd, and 3rd-order memory length of the VNLE is optimized to 161, 41, and 11, respectively. After subcarrier demultiplexing and down-sampling to 1 SPS, we use the blind phase search (BPS) algorithm<sup>47</sup> to finely correct the residual phase fluctuation within ± 5. 3<sup>∘</sup> . Then the GMI or NGMI is calculated as the performance metric. 

#### Calculation of net bitrate with the PS signal 

Assume a concatenated FEC with a total code rate Rc of 0.826 is used, the threshold of NGMI is 0.857. Then the net bitrate (NBR) of PS-MQAM per subcarrier in dual polarization can be calculated as 



Here H is the source entropy for 2-dimensional symbols and B is the baud rate. For 45-Gbuad dual-subcarrier PS-256-QAM signal with a source entropy of 13.92 bits/4D-symbol. The net bit rate is 1.0 Tb/s ( = 2 × 2 × ½13:92=2 �ð1 � 0:826Þ × log2256� × 45 Gb=s). For the WDM channels with an entropy of 12.82 bits/4D-symbol, the net bit rate is 903.2 Gb/s ( = 2 × 2 × ½12:82=2 �ð1 � 0:826Þ × log2256� × 45 Gb=s). 

#### The detailed experimental setup and DSP for front-haul transmission 

Figure S4 in Supplementary Note 4 provides a detailed illustration of the experimental setup. At the transmitter, we use a 1550 nm external cavity laser (ECL) with 100 kHz linewidth as an optical source of the channel under test (CUT). The 17-Gbaud LSB/RSB 512-QAM signal is generated by a 120-GSa/s AWG and then modulated through a 27 GHz 3 dB bandwidth IQ modulator. The bias is deviated from the null point to introduce a residual carrier with ~ -15 dB carrier-to-signal power ratio. For the loading channels, 11 ECLs spacing at 50 GHz are combined and fed into IQ modulator 2 simultaneously. The CUT and loading channels are respectively amplified, polarization division multiplexed and combined using a wave-shaper. After 10 km SSMF transmission, an optical band-pass filter is placed to select the desired 

Nature Communications |  (2024) 15:6339 

10 

Article 

https://doi.org/10.1038/s41467-024-50439-1 

wavelength. The demultiplexed signal is intradyne coherent detected with a 100-kHz local oscillator. After four 70 GHz BPDs detection, the electrical waveform is captured by a 128-GSa/s real-time oscilloscope for offline DSP. 

In the transmitter-side DSP, 32768 512-QAM symbols are mapped from binary bits, which is framed by a 3072-symbol preamble for synchronization and channel equalization. After up-sampling, rootraised cosine shaping is conducted with a roll-off of 0.1. Then the sequence is digitally up-converted for LSB and RSB modulation, in which a 1 GHz guard band is reserved for the residual carrier. After resampling to AWG sampling rate, linear pre-emphasis is applied to improve the bandwidth response. In the receiver-side DSP, we first emulate a DC block by subtracting the average value from the photocurrents of the in-phase/quadrature on X and Y polarizations. Then the detected waveform is 3 times re-sampled, frequency and phase recovered by the residual carrier, synchronized, and equalized based on the preamble. The multi-input multi-output (MIMO) equalizer has 3-order sparse Volterra kernels with lengths of (81, 11, 11). We use the blind phase search algorithm to finely correct the residual phase noise within ±8<sup>∘</sup> . 

## Data availability 

The data that support the plots within this paper and other findings of this study are available on Zenodo database [https://doi.org/10.5281/ zenodo.12513545]. All other data used in this study are available from the corresponding authors upon request. 

## Code availability 

The codes that support the findings of this study are available from the corresponding authors upon request. 

## References 

1. Zhou, X., Ryohei, U. & Hong, L. Beyond 1 Tb/s intra-data center interconnect technology: IM-DD OR coherent? J. Light. Technol. 38, 475–484 (2019). 

2. Rizzo, A. et al. Massively scalable Kerr comb-driven silicon photonic link. Nat. Photon. 17, 781–790 (2023). 

3. Pizzinat, A., Chanclou, P., Saliou, F. & Diallo, T. Things you should know about fronthaul. J. Light. Technol. 33, 1077–1083 (2015). 

4. Liu, X. Enabling optical network technologies for 5G and beyond. J. Light. Technol. 40, 358–367 (2022). 

5. Temprana, E. et al. Overcoming Kerr-induced capacity limit in optical fiber transmission. Science 348, 1445–1448 (2015). 

6. Liu, X., Chraplyvy, A. R., Winzer, P. J., Tkach, R. W. & Chandrasekhar, S. Phase-conjugated twin waves for communication beyond the Kerr nonlinearity limit. Nat. Photon. 7, 560–568 (2013). 

7. Jørgensen, A. et al. Petabit-per-second data transmission using a chip-scale microcomb ring resonator source. Nat. Photon. 16, 798–802 (2022). 

8. Liu, J. et al. 1-Pbps orbital angular momentum fibre-optic transmission. Light Sci. Appl. 11, 1–11 (2022). 

9. Kikuchi, K. Fundamentals of coherent optical fiber communications. J. Light. Technol. 34, 157–179 (2016). 

10. Colavolpe, G., Foggi, T., Forestieri, E. & Secondini, M. Impact of phase noise and compensation techniques in coherent optical systems. J. Light.Technol. 29, 2790–2800 (2011). 

11. Mengali, U. Synchronization Techniques for Digital Receivers 1997th edn, Vol. 520 (Kluwer Academic/Plenum Publishers, 1997). 

12. Chen, X. et al. Single-wavelength and single-photodiode 700 Gb/s entropy-loaded PS-256-QAM and 200-GBaud PS-PAM-16 transmission over 10 km SMF. Eur. Conf. Optic. Commun. https://doi. org/10.1109/ECOC48923.2020.9333201 (2020). 

13. Zhong, K. et al. Digital signal processing for short-reach optical communications: a review of current technologies and future trends. J. Light. Technol. 36, 377–400 (2018). 

14. Morsy-Osman, M. et al. DSP-free ‘coherent-lite’ transceiver for next generation single wavelength optical intra-datacenter interconnects. Opt. Express 26, 8890–8903 (2018). 

15. Gui, T. et al. Real-time demonstration of 600 Gb/s DP-64QAM SelfHomodyne coherent bi-direction transmission with un-cooled DFB laser. In Optical Fiber Communication Conference, Th4C–3 (Optica Publishing Group, 2020). 

16. Zhou, X., Gao, Y., Huo, J. & Shieh, W. Theoretical analysis of phase noise induced by laser linewidth and mismatch length in selfhomodyne coherent systems. J. Light. Technol. 39, 1312–1321 (2020). 

17. Ji, H. et al. Photonic integrated self-coherent homodyne receiver without optical polarization control for polarization-multiplexing short-reach optical interconnects. J. Light. Technol. 41, 911–918 (2023). 

18. Xu, M. et al. High-performance coherent optical modulators based on thin-film lithium niobate platform. Nat. Commun. 11, 3911 (2020). 

19. Cho, J. & Winzer, P. J. Probabilistic constellation shaping for optical fiber communications. J. Light.Technol. 37, 1590–1607 (2019). 

20. Kawai, A., Nakamura, M., Kobayashi, T. & Miyamoto, Y. Digital fourdimensional transceiver IQ characterization. J. Light. Technol. 41, 1389–1398 (2023). 

21. Nakamura, M. et al. Over 2-Tb/s net bitrate single-carrier transmission based on >130-GHz-bandwidth InP-DHBT baseband amplifier module. In European Conference and Exhibition on Optical Communication Th3C–1 (Optica Publishing Group, 2022). 

22. Chen, X., Cho, J., Adamiecki, A. & Winzer, P. 16384-QAM transmission at 10 GBd over 25-km SSMF using polarization-multiplexed probabilistic constellation shaping. In European Conference on Optical Communications (ECOC) https://doi.org/10.1049/cp.2019. 1030 (IET, 2019). 

23. Magarini, M. et al. Pilot-symbols-aided carrier-phase recovery for 100-G PM-QPSK digital coherent receivers. IEEE Photon.Technol. Lett. 24, 739–741 (2012). 

24. Morsy-Osman, M., Zhuge, Q., Chagnon, M., Xu, X. & Plant, D. V. Experimental demonstration of pilot-aided polarization recovery, frequency offset and phase noise mitigation. In Optical Fiber Communication Conference/National Fiber Optic Engineers Conference, OTu3I–6 (IEEE, 2013). 

25. Jansen, S. L., Morita, I., Schenk, T. C., Takeda, N. & Tanaka, H. Coherent optical 25.8-Gb/s OFDM transmission over 4160-km SSMF. J. Light. Technol. 26, 6–15 (2008). 

26. Jansen, S. L., Morita, I. & Tanaka, H. Experimental demonstration of 23.6-Gb/s OFDM with a colorless transmitter. In OptoElectronics and Communications Conference (OECC), PD1–5 (IEEE, 2007). 

27. Welch, D. et al. Point-to-multipoint optical networks using coherent digital subcarriers. J. Light. Technol. 39, 5232–5247 (2021). 

28. Alvarado, A., Agrell, E., Lavery, D., Maher, R. & Bayvel, P. Replacing the soft-decision FEC limit paradigm in the design of optical communication systems. J. Light. Technol.33, 4338–4352 (2015). 

29. Yamazaki, H. et al. Net-400-Gbps PS-PAM transmission using integrated AMUX-MZM. Opt. Express 27, 25544–25550 (2019). 

30. Fang, X. et al. Net 1-Tb/s/lambda PS-256-QAM coherent transmission with a 3-MHz DFB laser enabled by residual carrier modulation. In European Conference on Optical Communication (ECOC), Th–C–1–8 (IEEE, 2023). 

31. Shieh, W. & Ho, K.-P. Equalization-enhanced phase noise for coherent-detection systems using electronic digital signal processing. Opt. Express 16, 15718–15727 (2008). 

32. Mecozzi, A., Antonelli, C. & Shtaif, M. Kramers–Kronig coherent receiver. Optica 3, 1220–1227 (2016). 

33. Chen, X. et al. 218-Gb/s single-wavelength, single-polarization, single-photodiode transmission over 125-km of standard singlemode fiber using Kramers-Kronig detection. In Optical Fiber Communication Conference, Th5B–6 (Optica Publishing Group, 2017). 

Nature Communications |  (2024) 15:6339 

11 

Article 

https://doi.org/10.1038/s41467-024-50439-1 

34. Shieh, W., Sun, C. & Ji, H. Carrier-assisted differential detection. Light Sci. Appl. 9, 18 (2020). 

35. Le, S. T., Aref, V., Schuh, K. & Tan, H. N. Power-efficient singlesideband transmission with clipped iterative SSBI cancellation. J. Light. Technol. 38, 4359–4367 (2020). 

36. Common Public Radio Interface (CPRI). Specification, V6.1. http:// www.cpri.info/downloads/CPRI_v_6_1_2014-07-01.pdf (2013). 

37. Liu, X., Zeng, H., Chand, N. & Effenberger, F. Efficient mobile fronthaul via DSP-based channel aggregation. J. Light. Technol. 34, 1556–1564 (2016). 

38. Nakamura, M. et al. Net-bit rate of >562-Gb/s with 32-GBaud probabilistically constellation-shaped 1024QAM signal based on entropy and code-rate optimization. In European Conference on Optical Communication (ECOC) We3C–5 (IEEE, 2022). 

39. Nakamura, M., Kobayashi, T., Hamaoka, F. & Miyamoto, Y. High information rate of 128-GBaud 1.8-Tb/s and 64-GBaud 1.03-Tb/s signal generation and detection using frequency-domain 8 × 2 MIMO equalization. In Optical Fiber Communication Conference Th1F–2 (Optica Publishing Group, 2022). 

40. Olsson, S. L. et al. Record-high 17.3-bit/s/Hz spectral efficiency transmission over 50 km using probabilistically shaped PDM 4096QAM. In Optical Fiber Communication Conference Th4C–5 (Optica Publishing Group, 2018). 

41. Okamoto, S. et al. Experimental and numerical comparison of probabilistically shaped 4096 QAM and a uniformly shaped 1024 QAM in all-Raman amplified 160 km transmission. Opt. Express 26, 3535–3543 (2018). 

42. Olsson, S. L. et al. Probabilistically shaped PDM 4096-QAM transmission over up to 200 km of fiber using standard intradyne detection. Opt. Express 26, 4522–4530 (2018). 

43. Chen, X. C., Chandrasekhar, S., Cho, J. & Winzer, P. Transmission of 30-GBd polarization-multiplexed probabilistically shaped 4096QAM over 50.9 km SSMF. Opt. Express 27, 29916–29923 (2019). 

44. Terayama, M., Okamoto, S., Kasai, K., Yoshida, M. & Nakazawa, M. in Optical Fiber Communication Conference 1–3 (Optica Publishing Group, 2018). 

45. Beppu, S., Kasai, K., Yoshida, M. & Nakazawa, M. 2048 QAM (66 Gbit/ s) single-carrier coherent optical transmission over 150 km with a potential SE of 15.3 bit/s/Hz. Opt. Express 23, 4960–4969 (2015). 

46. Wang, Y., Okamoto, S., Kasai, K., Yoshida, M. & Nakazawa, M. Singlechannel 200 Gbit/s, 10 Gsymbol/s-1024 QAM injection-locked coherent transmission over 160 km with a pilot-assisted adaptive equalizer. Opt. Express 26, 17015–17024 (2018). 

47. Pfau, T., Hoffmann, S. & Noe, R. Hardware-efficient coherent digital receiver concept with feedforward carrier recovery for M-QAM constellations. J. Light. Technol. 27, 989–999 (2009). 

## Acknowledgements 

This work was supported by National Natural Science Foundation of China (62271010, F.Z.; U21A20454, F.Z.; 62001287, Y.Z.) and the major key project of Peng Cheng Laboratory (F.Z.). This work was also supported by High-performance Computing Platform of Peking University. 

We would like to thank Prof. Xiaopeng Xie and Dr. Chenbo Zhang from Peking University for providing the 3-MHz DFB laser and the helpful discussion. We also thank Prof. Dan Lu and Mr. Hao Song from Institute of Semiconductors, Chinese Academy of Sciences for their assistance with the laser linewidth measurement. 

## Author contributions 

X.F., Y.Z. and F.Z. conceived the concept of residual carrier modulation. X.F. and Y.Z. performed the experiment and analyzed the results. X.F., Y.Z. and F.Z. wrote the manuscript. X.C., W.H., Z.H. and S.Y. participated in preparing the manuscript and contributed to the discussions. All authors reviewed and revised the paper. F.Z. supervised the work. 

## Competing interests 

X.F. and F.Z. have filed a patent application on the residual carrier modulation method for laser phase noise compensation: CN202410809830.2, filed 21 June 2024. The remaining authors declare no competing interests. 

## Additional information 

Supplementary information The online version contains supplementary material available at https://doi.org/10.1038/s41467-024-50439-1. 

Correspondence and requests for materials should be addressed to Yixiao Zhu or Fan Zhang. 

Peer review information Nature Communications thanks Hiroyuki Takahashi, and the other anonymous reviewer(s) for their contribution to the peer review of this work. A peer review file is available. 

Reprints and permissions information is available at http://www.nature.com/reprints 

Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/ licenses/by/4.0/. 

© The Author(s) 2024 

Nature Communications |  (2024) 15:6339 

12 


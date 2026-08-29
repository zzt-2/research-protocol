2022 IEEE International Conference on Space Optical Systems and Applications (ICSOS) 

# Low-power-consumption coherent receiver architecture for satellite optical links 

A.W. Bernini, M. J. Fice, K. Balakier Department of Electronic and Electrical Engineering University College London (UCL) London, United Kingdom (UK) _Alexis.bernini.19@ucl.ac.uk_ 

_**Abstract**_ **— As the demand for satellite data transmission increases, higher capacity optical links need to be developed to allow satellites to be connected directly to ground stations (GST). The advantages of Low Earth Orbit (LEO) direct-toEarth links are smaller latency when compared to relay systems using Geostationary Orbit (GEO) satellites, i.e. LEO-to-GEO and GEO-to-GST, and an increased available bandwidth offered by the optical spectrum with respect to radio frequency (RF) which allows for much higher link capacity. The increase in data rate of optical satellite to ground links towards 100 Gbps will require implementing optical coherent transceivers with capability to compensate for Doppler shift and atmospheric channel impairments. An important figure of merit which needs to be carefully considered in a satellite system is the equipment power consumption. The power consumption of coherent receivers used for terrestrial applications is closely related to the bit rate, with a receiver back-end digital signal processing being responsible for the vast majority of the power consumed.** 

**In this paper we propose a hybrid approach to signal processing consisting of simplified digital and analogue elements allowing for significant power reduction. Moreover, one of the attractive aspects of the proposed approach is that it does not require an increased complexity for an increase in baud rate. It will be discussed that the analogue approach to the frequency and phase recovery would allow a saving of approximately 40% to 50% of power on the overall DSP block at baud rates between 10 Gbaud and 100 Gbaud.** 

## _**Keywords—digital signal processing, optical injection phaselock loop (OIPLL), power consumption, low-earth orbit (LEO) satellites, coherent detection**_ 

## I. INTRODUCTION 

Power consumption is one of the key aspects to consider when designing a communication system, and has been subject to multiple studies which aim to reduce the impact of active components in the communication link [1]–[4]. The amount of power that these consume influences the choices that are made throughout the design, such as the modulation format, baud rate, and constellation size [5]. Satellite systems are under significant pressure when it comes to power consumption, especially when dealing with small platforms in the LEO orbit. The current satellite optical communication systems rely on analogue amplitude modulation to simplify the receiver end as much as possible. Employing a coherent detection system would introduce more complexity, but can also allow an increase in the number of bits transmitted per symbol. With the advent of coherent detection, transceivers have been able to transmit both in-phase and quadrature components, therefore the available throughput is significantly increased, allowing much higher spectral efficiencies to be reached [6]. This approach has been used in long-reach and data-centre optical fibre communications. The key element which allows complex constellations to be decoded is the digital signal processing (DSP) at the receiver end, which unfortunately becomes one of the main power 

drawing elements in the whole communication chain [7]. In order to recover the signal in a fibre link, the elements of the DSP are the following: chromatic dispersion (CD) compensation, timing recovery, polarisation mode dispersion (PMD) compensation, carrier recovery, and decoding [7], [8]. All of these processes are carried out in the digital domain, hence analogue-to-digital converters (ADC) need to be in place per quadrature and per polarisation. For a full dualpolarisation (DP), in-phase and quadrature decoder (IQ decoder), four ADCs are required. The key reason why the DSP block consumes a high amount of power, approximately 420 mW/Gbit/s [9], is that the power is linearly dependent on the energy per bit (for each IC technological node), hence, a higher data rate translates linearly into a higher power consumption of the DSP block. 

The aim of this paper is to provide a concept for a powerefficient satellite communication system. Satellite links are not subject to some of the distortions experienced in optical fibre systems. Namely, CD and PMD effects are negligible, which allows the DSP block to be simplified [10], [11]. In order to further reduce the complexity of the DSP block we are investigating an analogue Optical Injection Phase-Lock Loop (OIPLL) [12] to operate in place of the digital carrier recovery component. The advantage of an analogue approach to signal processing (phase and frequency recovery) is that the power consumption does not depend on data rate as long as the used modulation format allows for a residual reference tone required by the OIPLL. It will be demonstrated that even after simplifying the DSP block, the OIPLL-based system allows a significant amount of power to be saved. In the next sections, the Doppler shift effect on the signal will be discussed, followed by an analysis of the power consuming elements in OIPLL and DSP systems respectively. 

II. DOPPLER SHIFT 

The Doppler shift consists of a frequency change in a received signal due to the relative velocity between two objects. In satellite free-space coherent communications this has a strong impact on performance, as, ideally, the receiver local oscillator should operate at the same frequency as the incoming signal. The LEO-to-Ground link adds another element of complexity to the system, as the satellite’s position with respect to the ground station is varying. 

The Doppler shift for various LEO scenarios has been studied in several publications. For the purposes of this discussion, the findings from [13] will be considered. 

As shown in Figure 1, and summarized in Table I, the Doppler shift range for LEO satellites does not significantly change with the orbit height. For a satellite orbiting at 160 km 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:24 UTC from IEEE Xplore.  Restrictions apply. 

149 

978-1-6654-3439-3/22/$31.00 ©2022 IEEE 

2022 IEEE International Conference on Space Optical Systems and Applications (ICSOS) 

**==> picture [502 x 182] intentionally omitted <==**

_Figure 1 -Doppler Shift (a) and Rate of Change (b) over time for multiple LEO orbit heights_ 

from Earth, the Doppler shift is ±4.89 GHz, whereas for a 1000 km orbit it is ±4.08 GHz. 

On the other hand, when considering the rate of change of frequency, at 1000 km orbit height the maximum rate is 29 MHz/s, whereas at 160 km it is 237 MHz/s, an eight times faster rate of change. 

_Table I.  Doppler shift parameters for various orbit heights_ 

|**Orbit**<br>**height**<br>**(km)**|**Velocity**<br>**(m/s)**|**View time**<br>**(min)**|**Max Doppler**<br>**Shift (GHz)**|**Max Rate**<br>**of Change**<br>**(MHz/s)**|
|---|---|---|---|---|
|**160**|7341|6.180|±4.862|237.2|
|**500**|7090|12.84|±4.4081|55.6|
|**1000**|6882|17.60|±4.0535|29.8|



III. POWER CONSUMPTION OF DIGITAL AND HYBRID COHERENT RECEIVER 

In order to compensate for the Doppler shift at the receiver side, analogue and digital approaches can be used. For the analogue compensation, an Optical Injection Phase-Lock Loop (OIPLL) will be considered, whereas for the DSP approach, a pilot aided and a data-based algorithm will be discussed. 

## _A. Hybrid Coherent Receiver_ 

The OIPLL combines an Optical Phase Lock Loop (OPLL) with Optical Injection Locking (OIL), providing the frequency tracking and phase locking of the OPLL together with the narrow linewidth and phase noise figure of OIL [13]. The configuration for the OIPLL which is going to be considered for this application has been explained in detail  in [12] and is shown in Figure 2. The current receiver breadboard was designed based on discrete components without low power consumption as a feature, hence, by designing the OIPLL in more integrated form an improved power consumption figure could be achieved. Moreover, as the OIPLL in our current experimental setup is not integrated: additional circuitry is inserted into the design to maintain the fibre paths in the two arms of the receiver at the same length; the path length control is represented with dashed lines to distinguish it from the OIPLL in dotted lines. For the 

purposes of power calculations these will be omitted, as ideally the OIPLL would be integrated on a photonic integrated circuit (PIC) for deployment, removing the need for the fibre path-length control. 

The complexity added to the receiver due to the analogue feedback  loop only comes from the loop filter and optical circulator. This assumption can be made as the other elements composing the receiver would be there in case of analogue or digital receiver, for instance, the LO laser, 90-degree hybrid, and electrical amplifiers. 

The loop filter power consuming elements are mainly the operational amplifiers which compose it. The supply voltage for those, in our implementation, is ±15V, and the current draw for the two supply rails has been measured in a worst case scenario, i.e. when the control signal coming from the PLL filter is at its 

**==> picture [244 x 109] intentionally omitted <==**

_Figure 2 - OIPLL architecture_ 

maximum correction. Depending on the polarity of the feedback signal, one of the supplies would experience a current draw of 28.5 mA, whereas the other rail would experience a current draw of 17.2 mA. The power for the two is then calculated to be 0.685 W. As discussed in [13], [14], the Doppler shift in a satellite link can be compensated by an OIPLL. Their calculations show that the doppler shift they manage to compensate is ±7.5GHz, which is more than the maximum ±5.5GHz calculated for the LEO-to-ground system discussed in the previous section. 

Another important observation is that given its analogue construction, the OIPLL’s power consumption is not dependent on the data rate being transmitted; increasing or 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:24 UTC from IEEE Xplore.  Restrictions apply. 

150 

2022 IEEE International Conference on Space Optical Systems and Applications (ICSOS) 

decreasing the transmitted information would consume the same amount of power at the receiver side. 

## _B. Digital Coherent Receiver_ 

As discussed in [7], DSP is the main power consuming element in the communication chain; this becomes an issue when deploying a coherent communication system. For ground links, it has been shown that the power consumption increases with distance, mainly due to chromatic dispersion and polarisation mode dispersion compensation [6]. In satellite communications, none of fibre dispersion compensations are required. The atmosphere’s effect on an optical carrier is very different than the one of a fibre optic cable [15]. 

In [7], a thorough analysis of the power consumption of the various elements composing a ground fibre optic link is described, considering both QPSK and 16-QAM modulation formats, and for various fibre distances. It has been shown that the main power-hungry component in the whole physical communication chain is the digital signal processing chip. For example, in a 2,400 km dual-polarisation QPSK (DPQPSK) system, the DSP consumes 56.3% of the energy per bit of the whole system (transmitter, link amplifiers, and receiver). This quantity translates to power by multiplying it by the data rate of the link. It is therefore intuitive that, as the trend of communications is to increase the possible data rate, this quantity can become an enormous issue. 

The various elements which compose the DSP are: encoding (at the transmitter), pulse shaping, chromatic dispersion compensation, timing recovery, polarisation mode dispersion compensation, carrier recovery, and decoding. The two most power-consuming components, as discussed by [7], are chromatic dispersion compensation and polarisation mode dispersion compensation [16]. As discussed before, these are not a factor in satellite communication, hence, these two can be directly cut out of the DSP, saving about 57% of the energy consumed by the DSP block. 

## _1) Frequency Offset Estimation Algorithms_ 

Any Frequency Offset Estimation (FOE) algorithm would be required to compensate for the Doppler shift caused by the movement of the satellite with respect to the OGS. The maximum shift they should be able to compensate is ±4.9GHz. 

There are multiple algorithms that have been shown to allow for carrier recovery in the DSP block. For the purposes of this discussion, only the ones with a bandwidth large enough to accommodate the full Doppler shift will be considered. The two algorithms selected for this discussion are described in detail in [17], [18]. 

It should be noted that these algorithms operate for intradyne Doppler shift, that is, for Doppler shift which is smaller than the signal bandwidth. This is mainly because of the sampling frequency of the ADCs. Hence, the transmit signal baudrate should be more than 5 Gbaud for those to work. 

The power consumption of the above algorithms could not be found in the literature, hence, an estimation based on the FastFourier Transform (FFT) and other DSP operations has been made. 

The estimation range of the method presented in [17] is dependent on the sampling rate, covering the frequency span 

between -Fs/2 and +Fs/2, where Fs is the sample rate of the ADCs employed at the receiver. 

The FOE algorithm discussed in [18] is constructed by taking into consideration spectral asymmetry. This is the shift of the spectrum with respect to baseband due to the up-conversion to the Doppler shift frequency. This is performed by taking the FFT of the incoming signal and calculating the power of the spectrum above and below zero. This method allows to estimate the Doppler shift up to 1GHz of precision, allowing for coarse correction of the Doppler shift. This approach needs to be combined with a carrier recovery algorithm to correct for the remaining shift. The length of the FFT used to compensate for the shift was set to 128 bits. 

The common element in these two algorithms is the need for a carrier recovery block further down the DSP line. This block would take care of multiplying the signal by the carrier offset, practically down-converting it to its baseband equivalent. If a numeric controlled oscillator (NCO) was to be used, these two methods would become similar to a CD compensation algorithm, as discussed in the next section. Therefore, the power consumed by the above could be approximated to the one being consumed by CD compensation. 

## _2) CD Power Consumption_ 

The basic element of the FOE algorithms discussed in the previous section is the FFT. The FFT is defined by two main parameters: the block size and sampling rate. These together allow to identify the frequency bandwidth of the DSP, and the resolution. 

Depending on the implementation of the FFT, the platform and technology on which it is deployed – i.e. FPGA, ASIC, etc. -, and other specific details, the power consumed is not trivial to calculate. A thorough calculation element by element of the FFT power is beyond of the scope of this paper; instead, the aim here is to obtain an estimate of the power consumption, rather than a value for a specific implementation. 

In [7], the FFT algorithm was designed to minimise power consumption for a specific FIR filter response, composed of approximately 1100 taps. In their findings, it was estimated that the energy per bit for CD compensation on a 2400 km, PM-QPSK system would consume 162 pJ/bit for a 40 nm ASIC, and 81 pJ/bit for a 20 nm. This value is generated from equation (1): 

**==> picture [169 x 23] intentionally omitted <==**

where, _nsa_ is the oversampling ratio, ∑𝐸𝑐 𝑜𝑝,𝑐𝑁𝑜𝑝,𝑐 represents the energy consumption estimate from the operations carried out in the DSP element for CD, _R_ is the rate of the code being used, in this case 0.83 LPDC code, _Nn_ is the number of multiplexed lines going into the FFT block, and _M_ is the constellation size. 

This energy-per-bit values for PM-QPSK can therefore be corrected for a DP-BPSK transmission system by multiplying the value by 2, as can be seen from (1). The energy consumption for DP-BPSK would then be 324 pJ/bit, translating to an approximate power consumption of 3.24 W at 10 Gbit/s. The FFT size for the above calculations is set to give a minimum power consumption given the number of 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:24 UTC from IEEE Xplore.  Restrictions apply. 

151 

2022 IEEE International Conference on Space Optical Systems and Applications (ICSOS) 

taps on the FIR filter. More recent technology in semiconductor manufacturing allows to reduce the minimum feature size from the discussed 40 nm down to 5 nm, with associated reduction in power consumption. 

## IV. DISCUSSION 

Figure 3 represents a comparison between the power consumed by the DSP-based 40nm CMOS and the OIPLLbased hybrid satellite coherent receiver systems. The dependency on the data rate comes from the inclusion of the carrier and timing recovery algorithms in the receiver. For the purposes of the calculations, the energy per bit consumption for the various elements of the DSP are the ones calculated by [7], and summarised in Table II. In order to allow a comparison between the OIPLL power consumption and that of the DSP, the power consumed by the former has been divided by the 10 Gbit/s data rate, so that the result would be the energy consumed per bit. It can be seen that the OIPLL would allow a saving of approximately 40% of the power when compared to the DSP approach at 10 Gbit/s. Following the same calculations, the power savings at 100 Gbit/s would be 49%. The DSP approach could still be less power hungry at low data rates. Figure 4 represents a comparison between the power consumption of a ground fibre link, a satellite link with DSP, and the satellite link with the OIPLL. Here the power consumed by the OIPLL is calculated as previously discussed, resulting in a non-zero intercept on the power axis. It can be seen that for data rates below 2.2 Gbit/s, the DSP approach would consume less power. It should be noted that this graph does not take into consideration an eventual flattening of the curve to a minimum power consumption that the platform on which the DSP was built might have. 

**==> picture [248 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
Energy per bit consumed at<br>10Gbit/s<br>1000<br>800<br>600<br>400<br>200<br>0<br>DSP DP-BPSK DSP DP-BPSK OIPLL DP-BPSK<br>satellite satellite<br>CD Compensation PMD compensation<br>Timing recovery Carrier recovery<br>Decoding OIPLL<br>Doppler Compensation<br>Energy per bit [pJ/bit]<br>**----- End of picture text -----**<br>


_Figure 3 - Energy per bit of DSP and OIPLL_ 

**==> picture [263 x 162] intentionally omitted <==**

_Figure 4 - Comparison of power consumption between ground link (blue), satellite link with DSP (orange), and satellite link with analogue OIPLL (yellow)_ 

Another element which can be compensated in analogue domain is timing recovery. This is not a feature of the OIPLL, but it could be implemented together with the latter [19], removing the need for any DSP if the link budget was to be strong enough as to remove the need for FEC. 

_Table II - Energy Per Bit Consumption_ 

|DSP Element|Energy per Bit – 40nm<br>CMOS[pJ/Bit]|
|---|---|
|CD Compensation for 2400 km|324|
|Timing Recovery|104|
|Decoding|172|
|PMD Compensation|246|
|Carrier Recovery|46|



## V. CONCLUSION 

The power consumption of a satellite optical coherent receiver is of great importance in the power budget. A comparison between analogue (OIPLL based) and digital (DSP based) signal processing has been presented. At baud rates greater than 2.2 Gbaud, the analogue approach would consume a smaller amount of power. At 10 Gbaud and 100 Gbaud, the analogue-based system would allow savings at the receiver of respectively 40% and 49% of power for a DP-BPSK system. Moreover, an increase in data rate or different constellation sizes would not require a redesign of the frequency and phase recovery subsystems if those were to be implemented using an OIPLL, as long as a reference tone is present. 

## ACKNOWLEDGMENT 

This research work has been supported by the UK Engineering and Physical Sciences Research Council (EPSRC) through Doctoral Training Partnerships (DTP) (EPSRC Reference: EP/R513143/1) and PICSat (EPSRC Reference: EP/S000976/1). 

## REFERENCES 

[1] A. Simsek _et al._ , “Evolution of Chip-Scale Heterodyne Optical Phase-Locked Loops Toward Watt Level Power Consumption,” _J. Light. Technol._ , vol. 36, no. 2, pp. 258–264, 2018, doi: 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:24 UTC from IEEE Xplore.  Restrictions apply. 

152 

2022 IEEE International Conference on Space Optical Systems and Applications (ICSOS) 

10.1109/JLT.2017.2758744. 

- [2] J. L. Wei, Q. Cheng, R. V Penty, I. H. White, and D. G. Cunningham, “Analysis of complexity and power consumption in DSP-based optical modulation formats,” _Advanced Photonics for Communications,_ 2014, doi: 10.1364/sppcom.2014.sm2d.5. 

- [3] E. Cianca _et al._ , “Softwarization and Virtualization as Enablers for Future EHF/FSO High Throughput Satellites,” _2018 IEEE Glob. Commun. Conf. GLOBECOM 2018 - Proc._ , 2018, doi: 10.1109/GLOCOM.2018.8647698. 

- [4] T. Kupfer, A. Bisplinghof, T. Duthel, C. Fludger, and S. Langenbach, “Optimizing power consumption of a coherent DSP for metro and data center interconnects,” _2017 Optical Fiber Communications Conferencce and Exhibition, OFC 2017 - Pocceedings,_ 2017. 

- [5] C. Christopoulos and A. Wright, “Digital communications,” in _Electrical Power System Protection_ , McGraw-Hill, 2008. 

- [6] K. Kikuchi, “Fundamentals of coherent optical fiber communications,” _J. Light. Technol._ , vol. 34, no. 1, pp. 157–179, 2016, doi: 10.1109/JLT.2015.2463719. 

- [7] B. S. G. Pillai _et al._ , “End-to-end energy modeling and analysis of long-haul coherent transmission systems,” _J. Light. Technol._ , vol. 32, no. 18, pp. 3093–3111, Sep. 2014, doi: 10.1109/JLT.2014.2331086. 

- [8] S. J. Savory, “Digital coherent optical receivers: Algorithms and subsystems,” _IEEE J. Sel. Top. Quantum Electron._ , vol. 16, no. 5, pp. 1164–1179, Sep. 2010, doi: 10.1109/JSTQE.2010.2044751. 

- [9] X. Zhang, X. Yi, X. Liu, and P. J. Winzer, “100G transport systems: technology bench-mark testing in China and evolution to Terabit/s interfaces,” _China Commun._ , vol. 10, no. 4, pp. 19–30, 2013, doi: 10.1109/CC.2013.6506925. 

- [10] K. Elayoubi, “Study of communications channels for optical links through the atmosphere,” Ph.D dissertation, Université de Toulouse,  2019. 

   - [12] M. J. Fice, A. Chiuchiarelli, E. Ciaramella, and A. J. Seeds, “Homodyne coherent optical receiver using an optical injection phase-lock loop,” _J. Light. Technol._ , vol. 29, no. 8, pp. 1152–1164, 2011, doi: 10.1109/JLT.2011.2115993. 

   - [13] Y. Shoji, M. J. Fice, Y. Takayama, and A. J. Seeds, “A pilot-carrier coherent LEO-to-ground downlink system using an optical injection phase lock loop (OIPLL) technique,” _J. Light. Technol._ , vol. 30, no. 16, pp. 2696–2706, 2012, doi: 10.1109/JLT.2012.2204037. 

   - [14] T. Ando, E. Haraguchi, K. Tajima, Y. Hirano, T. Hanada, and S. Yamakawa, “Optical homodyne BPSK receiver with Doppler shift compensation for LEO-GEO optical communication,” _Pacific Rim Conf. Lasers Electro-Optics, CLEO - Tech. Dig._ , pp. 59–60, 2013, doi: 10.1109/CLEOPR.2013.6600348. 

   - [15] H. Kaushal and G. Kaddoum, “Optical Communication in Space: Challenges and Mitigation Techniques,” _IEEE Communications Surveys and Tutorials_ . 2017, doi: 10.1109/COMST.2016.2603518. 

   - [16] A. A. M. Saleh, “An Investigation of Laser Wave Depolarization Due to Atmospheric Transmission,” _IEEE J. Quantum Electron._ , vol. 3, no. 11, pp. 540–543, 1967, doi: 10.1109/JQE.1967.1074404. 

   - [17] D. Zhao, L. Xi, X. Tang, W. Zhang, Y. Qiao, and X. Zhang, “Digital pilot aided carrier frequency offset estimation for coherent optical transmission systems,” _Opt. Express_ , vol. 23, no. 19, p. 24822, 2015, doi: 10.1364/oe.23.024822. 

   - [18] J. C. M. Diniz _et al._ , “Simple feed-forward wide-range frequency offset estimator for optical coherent receivers,” _Opt. InfoBase Conf. Pap._ , vol. 19, no. 26, pp. 323–328, 2011, doi: 10.1364/oe.19.00b323. 

   - [19] R. Kamran _et al._ , “Demonstration of a low-power, local-oscillatorless, and DSP-free coherent receiver for data center interconnects,” _Appl. Opt._ , vol. 59, no. 7, p. 2031, Mar. 2020, doi: 10.1364/ao.383185. 

- [11] S. F. Clifford, “Polarization and Angle-of -Arrival Fluctuations,” _IEEE Transacctions  on Antennas and Propagation,_ Vol.. 15, no. 3, pp.  416-421, 1967. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:52:24 UTC from IEEE Xplore.  Restrictions apply. 

153 


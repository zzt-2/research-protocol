# Bit-Interleaved LDPC-Coded Modulation with Iterative Demapping and Decoding 

Qiuliang Xie, Kewu Peng, Jian Song and Zhixing Yang 

Tsinghua National Laboratory for Information Science and Technology (TNList) Department of Electronic Engineering, Tsinghua University, Beijing 100084, China Email: xql06@mails.tsinghua.edu.cn 

_**Abstract**_ **— Bit-interleaved coded modulation (BICM) is a suboptimal scheme from the average mutual information (AMI) point of view due to independent demapping. However, this AMI loss can be neglected for signal constellations with Gray mapping at high coding rates. AMI of amplitude-phase shift keying (APSK) constrained additive white Gaussian noise (AWGN) channel is provided in this paper, which shows that the BICM scheme has considerable loss with APSK constellations since no Gray mapping exists. Bit-interleaved low-density parity-check (LDPC) coded modulation (BILCM) is an excellent scheme and has been employed in many broadcasting and communication systems, however, such scheme also suffers from the independent demapping loss. Therefore, BILCM with iterative demapping and decoding (BILCM-ID) is proposed in this paper to overcome such loss. Simulation results show that the BILCM-ID scheme outweighs BILCM scheme by about 0.5 and 0.3 dB over AWGN channel for 32-APSK constellation at coding rates 2/3 and 4/5, respectively.** 

## I. INTRODUCTION 

Bit-interleaved coded modulation (BICM), which consists of a coding, bit-wise interleaving and constellation mapping, was first proposed by Zehavi [1]. Studies show that BICM is much better than trellis coded modulation (TCM) and symbolinterleaved coded modulation (SICM) under fading channels, but a little worse than TCM under additive white Gaussian noise (AWGN) channel [1]. BICM _with iterative decoding_ (BICM-ID) was first described by Li _et al._ [2], [3], and Brink [4] who named it _iterative demapping_ independently. This BICM-ID scheme can approach the performance of Turbo-TCM over AWGN channel, but it mainly employs traditional convolutional codes and focuses on the constellation mapping (also often called labeling), which greatly affects the error performance [3], [5]–[7]. However, such BICM-ID systems have high error floor and do not take advantages over BICM with excellent channel codes from the viewpoint of error performance or implementation complexity. 

Low-density parity-check (LDPC) codes were first described by Gallager [8], and re-discovered by Mackay [9]. In this paper, bit-interleaved LDPC-coded modulation with iterative demapping and decoding (BILCM-ID) is studied using amplitude-phase shift keying (APSK) constellations, which have been employed by DVB-S2 [10]. As pointed out by Goff [11] and Caire [12], there is very little average mutual information (AMI) loss for traditional M phase shift keying (M-PSK) or M quadrature-amplitude modulation (MQAM) constellations in BICM systems, when Gray mapping 

is employed. However, only pseudo-Gray mapping exists for APSK constellations. Therefore, BICM schemes with APSK lead to more AMI loss than those with traditional MPSK or MQAM. Fortunately such AMI loss can be regained via iterative demapping and decoding. 

BILCM-ID is different from traditional BICM-ID with convolutional codes. The later treats the constellation mapping as the inner code and expects it to transfer more information between bits within the same symbol, and hence Gray mapping becomes the worst one. The former, however, expects to regain the AMI loss due to independent demapping, and Gray mapping maximize the AMI in the first iteration, therefore it is the best one, again. Such Gray mapping has one additional advantage that the receiver can treat the system both as BILCM or BILCM-ID, and thereby only Gray or pseudo-Gray mapping is considered in this paper. 

The rest of this paper is organized as follows. Section II gives the system model describing how BILCM-ID works. Section III discusses the AMI of constellation-constrained AWGN channel, where APSK-constrained AMIs for both BICM and BICM-ID are provided. Section IV deals with BILCM-ID system, where the iterative demapping algorithm and simulation results are presented. Finally, conclusions are drawn in Section V. 

## II. SYSTEM MODEL 

The transmitter and receiver modules of BILCM-ID are depicted in Fig. 1. The transmitter of BILCM-ID is the same as that of BILCM, where the source bits _sk_ are encoded, interleaved and mapped (with Gray or pseudo-Gray mapping) to constellation symbols _xk_ , which are then transmitted to the channel. However, unlike in the receiver of BILCM, the decoder’s soft output is fed back to the soft demapper in the receiver of BILCM-ID to achieve the iterative demapping and decoding gain. 

## III. AMI OF BICM-ID SYSTEM 

An information-theoretical view of BICM-ID system is given in this section. First, the AMI of constellationconstrained AWGN channel and the definition of APSK constellation are presented. Then the AMI of APSK-constrained AWGN channel is obtained via numerical calculation, based on which quantitative AMI loss due to independent demapping in BICM system can be obtained. 

> Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:25 UTC from IEEE Xplore.  Restrictions apply. 978-1-4244-2517-4/09/$20.00 ©2009 IEEE 

1 

**==> picture [248 x 123] intentionally omitted <==**

**----- Start of picture text -----**<br>
sk LDPC bk Constellaion<br>�<br>Encoder Mapping xk<br>noise channel<br>s ˆ k LDPC Lk � [��] Soft<br>Decoder Demapper<br>a priori<br>� L-value<br>**----- End of picture text -----**<br>


Fig. 1. Transmitter and receiver modules of BILCM-ID. 

## _A. AMI of Constellation-Constrained AWGN Channel_ 

We now consider the discrete-time memoryless complex AWGN channel modeled as _y_ = _x_ + _n_ , where _x_ denotes the input complex signal, _n_ denotes the complex Gaussian noise with zero mean and variance of _σ_[2] _/_ 2 = _N_ 0 _/_ 2 for each real and imaginary part, and _y_ denotes the corresponding output. Following the definitions given in [13], AMI of AWGN channel when the input signals _x_ are constrained by a specific elementary constellation _χ_ (assuming _x_ takes on _χ_ with equal probability), can be evaluated as (e.g., [12], [13]) 

**==> picture [203 x 26] intentionally omitted <==**

where E denotes expectation, and _m_ = log2( _|χ|_ ) where _|χ|_ denotes the size of signal set _χ_ . The AMI _C_ defined in (1) is called _Coded Modulation (CM) Capacity_ in [12] since it is the maximum transmission rate (in bits/channel use), at which error-free transmission is possible with such signal set. 

In a BICM system, however, since each bit level is demapped independently, the AMI is reduced to [12] 

**==> picture [215 x 32] intentionally omitted <==**

where _χ_[(] _i[b]_[)] denotes the subset of _χ_ whose corresponding _i_ -th bit is _b_ ( _b ∈{_ 0 _,_ 1 _}_ ). Similar to the definition above, we call the AMI defined in (2) the _BICM Capacity_ . 

According to the data-processing theorem in information theory, it can be easily proved that _C_[ˆ] _≤ C_ which shows the sub-optimality of BICM schemes. However, BICM-ID schemes are optimal because the bit-levels are not demapped independently but are fed back to assist demapping other bits within the same symbol. 

## _B. APSK Constellations_ 

Since the AMIs of traditional constellations such as 8PSK, 16QAM and 64QAM have already been discussed carefully in many literatures [11], [12], with which BICM only lose just a little when Gray mapping is employed, we will mainly focus our attentions on the constellations that Gray mapping does not exist, e.g., 16APSK and 32APSK. For the reason of comparison, 8PSK with Gray mapping is also discussed in this paper. 

**==> picture [235 x 203] intentionally omitted <==**

Fig. 2. (4+12)16APSK and (4+12+16)32APSK constellation with pseudoGray mapping. Mapping for (4+12)16APSK in brackets (). 

TABLE I 

PARAMETERS OF 16 AND 32-APSK CONSIDERED IN THIS PAPER. 

|Constellation|_r_2_/r_1|_r_3_/r_1|_θ_1|_θ_2|_θ_2|
|---|---|---|---|---|---|
|(4+12) 16APSK|2.7|N/A|_π/_4|_π/_12|N/A|
|(4+12+16) 32APSK|2.8|5.3|_π/_4|_π/_12|_π/_16|



An _M_ -APSK constellation consists _nR_ concentric rings, each with uniformly spaced PSK points [14]. The signal set is given by 

**==> picture [243 x 93] intentionally omitted <==**

where _nl_ , _rl_ and _θl_ denote the number of points, the radius and the phase shift of the _l_ -th ring, respectively. 

The 16 and 32-APSK constellations with pseudo-Gray mapping are depicted in Fig. 2, and parameters of them are listed in Table I. The optimal parameters of such constellations vary with different coding rates [14], but in this paper, such parameters are fixed for the simplicity of discussions. 

## _C. Numerical Results_ 

The BICM and CM capacities of 8PSK under AWGN channel are depicted in Fig. 3, and those of 16 and 32-APSK with parameters listed in Table I are shown in Fig. 4. From these two figures we can see that the gap between BICM and CM capacities varies with different coding rates and constellation orders. For example, such gap is less than 0.02 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:25 UTC from IEEE Xplore.  Restrictions apply. 

2 

**==> picture [42 x 40] intentionally omitted <==**

**==> picture [245 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
check node<br>LDPC<br>girth-4<br>bit node<br>BICM-ID<br>symbol node<br>**----- End of picture text -----**<br>


Fig. 5. Tanner Graph of BILCM-ID where bit-interleaving is restricted within one LDPC codeword. 

In BICM-ID systems, the soft output (usually the loglikelihood ratio (LLR) of each bit) from the soft decoder is fed back to assist demapping. The soft demapping algorithm with LLR values feedback can be simply derived as follows, 

Fig. 3. BICM and CM capacity versus signal-to-noise ratio (SNR, SNR = _Es/σ_[2] = _Es/N_ 0) for 8PSK over AWGN channel. 

**==> picture [84 x 160] intentionally omitted <==**

Fig. 4. BICM and CM capacity versus SNR for 16 and 32APSK over AWGN channel. 

**==> picture [241 x 165] intentionally omitted <==**

where _f_ ( _β, j_ ) denotes the _j_ -th bit ( _j_ = 1 _, · · · , m_ ) corresponding to symbol _β_ , _L_ ( _Bj_ ) = log( _P_ ( _Bj_ = 0) _/P_ ( _Bj_ = 1)) denotes the LLR metric of the _j_ -th bit, _p_ ( _y|X_ = _β_ ) denotes the probability density function (PDF) of the received signal _Y_ with transmitted symbol _β_ , and 

**==> picture [183 x 23] intentionally omitted <==**

dB when coding rate is 0.8 (at the capacity of 2.4 bits/channel use) for 8PSK, but about 0.3 dB when coding rate is 0.4 (at the capacity of 1.2 bits/channel use). On the other side, at the coding rate of 0.8, the gap for 8PSK is less than 0.02 dB, while it is about 0.18 dB for 16APSK (at the capacity of 3.2 bits/channel use) and 0.41 dB for 32APSK (at the capacity of 4 bits/channel use). Therefore, it can be concluded that such gap decreases as the coding rate increases, and increases as the constellation order increases, and Gray mapping makes such gap ignorable at high coding rates. 

## IV. BILCM-ID SYSTEM 

## _A. Soft Demapping with a Priori Knowledge_ 

Since the gaps between CM and BICM capacities can not be neglected for APSK constellations, iterative demapping is presented here to regain such loss. 

It is notable that the demapping algorithm expressed in (4) is exactly the same as that derived by [4], while here the derivation of (4) is much more straightforward and reveals physical insights. Assuming _L_ ( _bj_ ) = 0, which denotes that no priori information is used, then (4) degenerates to the traditional independent demapping algorithm. 

## _B. The Tanner Graph of BILCM-ID_ 

It is well-known that an LDPC code can be represented by a Tanner Graph. Similarly, since bits corresponding to the same symbol also have some constraints, BICM-ID also can be represented by a Tanner Graph. Therefore, BILCM-ID can be represented by Fig. 5, and the iterative demapping procedure can be regarded as the message passing between the bit nodes and symbol nodes back and forth. 

It can be observed from this Tanner Graph that there are no cycles between the symbol nodes and the bit nodes since 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:25 UTC from IEEE Xplore.  Restrictions apply. 

3 

**==> picture [148 x 114] intentionally omitted <==**

Fig. 6. BER of BILCM and BILCM-ID 8PSK with 2/5 and 4/5 coding rates. AWGN channel. 

**==> picture [182 x 133] intentionally omitted <==**

**==> picture [32 x 36] intentionally omitted <==**

Fig. 7. BER of BILCM and BILCM-ID 16APSK with 2/5 and 4/5 coding rates. AWGN channel. 

each symbol node connects to different bit nodes, however, there will be some short girth (the minimum length of the cycles) such as girth-4 in the BILCM-ID system at a large probability if the interleaver is restricted within one LDPC codeword. Just as the performance is affected by short cycles in an LDPC code, these short cycles in BILCM-ID will also affect the error performance, especially at low coding rates where there are more check nodes and hence easier to form cycles. On the other hand, by observing (4), the LLR values of each bits corresponding to the same symbol are assumed to be independent, while in practice the cycles will make them related to each other and affect the error performance consequently. 

## _C. Simulation Results_ 

The bit error rate (BER) performance of BILCM-ID over AWGN channel are depicted from Fig. 6 to Fig. 8 for 8PSK, 16APSK and 32APSK, respectively. The BER performance 

**==> picture [82 x 98] intentionally omitted <==**

**==> picture [48 x 47] intentionally omitted <==**

Fig. 8. BER of BILCM and BILCM-ID 32APSK with 2/5 and 4/5 coding rates. AWGN channel. 

of BILCM and the Shannon limits for these constellation mappings are also provided as the references. Here LDPC codes of rate 2/5 and 4/5 length 64800 bits from DVB-S2 are employed. In this simulation, there are totally 8 demapping iterations each iteration the LDPC decoder iterates 50 times, and BILCM system only takes 50 iterative decoding using the standard LLR-BP algorithm. Bit-interleaving is restricted within one LDPC codeword. The Shannon limits are obtained based on the AMIs shown in Fig. 3 and 4, which are named _CM or BICM-ID limit_ for BILCM-ID system and _BICM limit_ for BILCM system. 

According to these figures, there are some iterative gain for any constellation any coding rate. Except for 8PSK with 4/5 coding rate where both the capacity gap and iterative gain can be neglected because of the Gray mapping and high coding rate, for other constellations or coding rates, there are about 0.15 to 0.2 dB iterative gains, while the corresponding gaps between the CM limits and BICM limits are much larger than 0.2 dB. For example, although there is about a 0.74 dB gap between CM limit and BICM limit for 32APSK 2/5 coding rate, a 0.41 dB gap between them for 32APSK 4/5 coding rate, there are still only about 0.15 to 0.2 dB iterative gains. A possible reason for this phenomenon is that the short cycles greatly affect the error performance, which makes the _L_ ( _Bj_ )s in (4) not independent. Therefore, since bit-interleaving between multiple codewords and high coding rates can reduce the short cycles in a large probability, better error performance can be expected. 

The BER performances of 32APSK coding rate 2/3 and 4/5 with different interleaving size are shown in Fig. 9 and Fig. 10. From these figures, we can see that another 0.1 to 0.15 dB can be gained compared with that bit-interleaving restricted within one codeword. Comparing with the original BILCM 32APSK system, BILCM-ID can obtain about 0.5 and 0.3 dB over AWGN channel at coding rate 2/3 and 4/5, respectively, when the interleaving size is increased to 8-codeword. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:25 UTC from IEEE Xplore.  Restrictions apply. 

4 

**==> picture [66 x 40] intentionally omitted <==**

BILCM system, BILCM-ID system can obtain considerable iterative gain in the case of large constellation and long interleaving size. For instance, for 32APSK and 8-codeword interleaving, BILCM-ID system can obtain about 0.5 and 0.3 dB over AWGN channel compared with BILCM system at coding rates 2/3 and 4/5, respectively. 

Another advantage of BILCM-ID is that the transmitter in it is exactly the same with that in BILCM because they both employ Gray or pseudo-Gray mapping, and therefore BILCMID is compatible with the existed BILCM system. That is, better error performance can be achieved by increasing the complexity of the detection algorithm. However, since the algorithm provided in this paper is much more complicated than that of BILCM system, some simplification work still needs to be done. 

Fig. 9. BER of BILCM and BILCM-ID 32APSK with 2/3 coding rate, where BILCM-ID( _m_ ) denotes that the bit-interleaving is restricted within _m_ codewords. AWGN channel. 

**==> picture [69 x 47] intentionally omitted <==**

## ACKNOWLEDGMENT 

This work was supported by “Multistandard integrated network convergence for global mobile and broadcast technologies” (MING-T, FP6 STREP Contract Nr.045461). 

## REFERENCES 

- [1] E. Zehavi, “8-PSK trellis codes for a Rayleigh channel,” _IEEE Trans. Commun._ , vol. 40, no. 5, pp. 873–884, May 1992. 

- [2] X. Li and J. A. Ritcey, “Bit-interleaved coded modulation with iterative decoding using soft feedback,” _Electronics Letters_ , vol. 34, no. 10, pp. 942–943, May 1998. 

- [3] X. Li, A. Chindapol, and J. A. Ritcey, “Bit-interleaved coded modulation with iterative decoding and 8PSK signaling,” _IEEE Trans. Commun._ , vol. 50, no. 8, pp. 1250–1257, 2002. 

- [4] S. T. Brink, J. Speidel, and R.-H. Yan, “Iterative demapping and decoding for multilevel modulation,” in _Globecom ’98_ , 1998, pp. 579– 584. 

- [5] A. Chindapol and J. A. Ritcey, “Design, analysis, and performance evaluation for BICM-ID with square QAM constellations in Rayleigh fading channels,” _IEEE J. Select. Areas Commun._ , vol. 19, pp. 944–957, May 2001. 

Fig. 10. BER of BILCM and BILCM-ID 32APSK with 4/5 coding rate, where BILCM-ID( _m_ ) denotes that the bit-interleaving is restricted within _m_ codewords. AWGN channel. 

## V. CONCLUSIONS 

The AMI of constellation-constrained AWGN channel is discussed in this paper, especially for APSK constellations that have been employed by DVB-S2 but without Gray mapping exist. Analysis show that the gaps between BICM capacities and CM capacities can not be neglected for 16 or 32 APSK constellations with pseudo-Gray mapping. Numerical results show that at 4/5 coding rate, such gap is about 0.18 dB for 16APSK and about 0.41 dB for 32APSK. For 32APSK, such gap is up to 0.6 dB at 2/3 coding rate and 0.71 dB at 2/5 coding rate. Therefore, although the combination of low coding rate and large constellation may not be used in practice, the gap for high coding rate and high order constellation can not be neglected, either. 

- [6] X. Qi, S. Zhou, M. Zhao, and J. Wang, “Design of constellation labelling maps for iteratively demapped modulation schemes based on the assumption of hard-decision virtual channels,” _IEE Proc.-Commun._ , vol. 152, no. 6, pp. 1139–1148, Dec. 2005. 

- [7] N. H. Tran and H. H. Nguyen, “Signal mappings of 8-ary constellations for bit interleaved coded modulation with iterative decoding,” _IEEE Trans. on Broadcasting_ , vol. 52, no. 1, pp. 92–99, Mar. 2006. 

- [8] R. G. Gallager, “Low-density parity-check codes,” _IRE Trans. Inform. Theory_ , no. 18, pp. 21–28, Jan. 1962. 

- [9] D. J. C. MacKay, “Good error correcting codes based on very sparse matrices,” _IEEE Trans. Inform. Theory_ , vol. 45, pp. 399–431, Mar. 1999. 

- [10] _Digital Video Broadcasting (DVB); Second generation framing structure, channel coding and modulation systems for Broadcasting, Interactive Services, News Gathering and other broadband satellite applications_ , ETSI Std. EN 302 307, V1.1.2, 2006. 

- [11] S. Y. Goff, “Signal constellations for bit-interleaved coded modulation,” _IEEE Trans. Inform. Theory_ , vol. 49, no. 1, pp. 307–313, Jan. 2003. 

- [12] G. Caire, G. Taricco, and E. Biglieri, “Bit-interleaved coded modulation,” _IEEE Trans. Inform. Theory_ , vol. 44, no. 3, pp. 927–946, May 1998. 

- [13] E. Biglieri, _Coding for Wireless Channels_ . Springer Science+Business Media, Inc., 2005. 

- [14] R. D. Gaudenzi, A. G. i Fabregas, and A. Martinez, “Performance analysis of Turbo-coded APSK modulations over nonlinear satellite channels,” _IEEE Trans. Wireless Commun._ , vol. 5, no. 9, pp. 2396–2407, Sept. 2006. 

To regain the capacity loss due to independent demapping, BILCM-ID system is proposed in this paper. Comparing with 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:25 UTC from IEEE Xplore.  Restrictions apply. 

5 


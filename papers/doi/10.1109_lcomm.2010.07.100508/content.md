667 

IEEE COMMUNICATIONS LETTERS, VOL. 14, NO. 7, JULY 2010 

## Adaptive-Normalized/Offset Min-Sum Algorithm 

## Xiaofu Wu, Yue Song, Ming Jiang, and Chunming Zhao 

_**Abstract**_ **—An adaptive-normalized/offset min-sum (AN-/AOMS) algorithm for decoding low-density parity-check (LDPC) codes is proposed. Unlike the normalized/offset min-sum (NMS/OMS) algorithm, the normalization/offset factor is adaptively adjusted according to the state of check nodes in each iteration. Simulation results show that the proposed AN-/AOMS algorithm can perform better than the NMS/OMS algorithm while still preserving the low complexity of the min-sum algorithm.** 

_**Index Terms**_ **—Decoding, min-sum algorithm, low-density parity-check (LDPC) codes.** 

## I. INTRODUCTION 

TERATIVE decoding of low-density parity-check (LDPC) **I** codes has received much attention in recent years ( [1]– [5], and references therein). The standard sum-product (SP) algorithm can achieve excellent performance but often with heavy implementation complexity [1]. In particular, the SP algorithm requires to estimate the signal-to-noise ratio (SNR), which is undesirable in practice. The min-sum (MS) algorithm , as an approximation to the SP algorithm, performs worse than the SP algorithm. However, the MS algorithm has the advantage of both low implementation complexity and no requirement for SNR estimation. 

The sub-optimality of the MS algorithm in performance comes from the overestimation of the message at check nodes. Therefore, the improvement can be achieved with a normalization or offset operation at check nodes. The resulted algorithm is the normalized MS (NMS) or the offset MS (OMS) algorithm [3], [5], which has received much interest in practice. In this paper, we propose an adaptive-normalized/offset minsum (AN-MS/AO-MS) algorithm, which can further improve the performance of the NMS/OMS algorithm. 

Let _𝐶_ be a ( _𝑁, 𝐾_ ) LDPC code of block length _𝑁_ and dimension _𝐾_ , which has a parity-check matrix _𝐻_ = [ _ℎ𝑚,𝑛_ ] of _𝑀_ rows, and _𝑁_ columns. Let _𝑅𝑐_ = _𝐾/𝑁_ denote its code rate. Consider now that the LDPC coded bits are BPSK 

Manuscript received March 30, 2010. The associate editor coordinating the review of this letter and approving it for publication was V. Stankovic. 

This work was supported in part by the National High Technology Research and Development Program (863 program) of China under Grant 2009AA01Z235, by the National Science Foundation of China under Grant 60972060, and by the Research Fund of National Mobile Communications Research Laboratory, Southeast University (No. 2010A10). 

X. Wu is with the Nanjing Institute of Communications Engineering, PLA Univ.of Sci. & Tech., Nanjing 210007, China. He is also with the National Mobile Commun. Research Lab., Southeast Univ., Nanjing 210096 (e-mail: xfuwu@ieee.org). 

Y. Song is with the PLA Univ. of Sci. & Tech., Nanjing 210007, China (e-mail: echoyuesong@163.com). 

M. Jiang and C. Zhao are with the National Mobile Commun. Research Lab., Southeast University, Nanjing 210096, China (e-mail: _{_ jiang ming, cmzhao5 _}_ @seu.edu.cn). 

Digital Object 10.1109/LCOMM.2010.07.100508 

modulated, and further transmitted over an additive white Gaussian noise (AWGN) channel. Let **c** = ( _𝑐_ 1 _, 𝑐_ 2 _, ⋅⋅⋅ , 𝑐𝑁_ ) _[𝑇]_ be a column vector of size _𝑁_ , which denotes a codeword of _𝐶_ . It is mapped to **x** = ( _𝑥_ 1 _, 𝑥_ 2 _, ⋅⋅⋅ , 𝑥𝑁_ ) _[𝑇]_ by _𝑥𝑛_ = 2 _𝑐𝑛 −_ 1 before transmission. At the receiver, we get the received vector **y** = ( _𝑦_ 1 _, 𝑦_ 2 _, ⋅⋅⋅ , 𝑦𝑁_ ) _[𝑇]_ , where 

**==> picture [192 x 10] intentionally omitted <==**

and _𝑣𝑛_ is the additive white Gaussian noise with zero mean and variance _𝜎_[2] = (2 _𝑅𝑐𝐸𝑏/𝑁_ 0) _[−]_[1] . 

We denote the set of bits that participate in check _𝑚_ by _𝒩_ ( _𝑚_ ) = _{𝑛_ : _ℎ𝑚,𝑛_ = 1 _}_ . Similarly, we denote the set of checks in which bit _𝑛_ participates as _ℳ_ ( _𝑛_ ) = _{𝑚_ : _ℎ𝑚,𝑛_ = 1 _}_ . We denote by _𝒩_ ( _𝑚_ ) _∖𝑛_ as the set _𝒩_ ( _𝑚_ ) with bit _𝑛_ excluded and by _ℳ_ ( _𝑛_ ) _∖𝑚_ as the set _ℳ_ ( _𝑛_ ) with check _𝑚_ excluded. The row vectors of the parity-check matrix _𝐻_ can be enumerated as **h** _[𝑇] 𝑚_[= (] _[ℎ][𝑚,]_[1] _[,][ ⋅⋅⋅][, ℎ][𝑚,𝑁]_[)] _[, 𝑚]_[= 1] _[,]_[ 2] _[,][ ⋅⋅⋅][, 𝑀]_[.] 

The rest of the letter is organized as follows. In sectionII, the AN-MS/AO-MS algorithm is presented. Section-III discusses the simulation results and Section-IV concludes the letter. 

## II. ADAPTIVE-NORMALIZED/OFFSET MIN-SUM ALGORITHM 

## _A. Motivation_ 

In this section, we based on the NMS/OMS algorithm to make a further improvement. We notice that the decoding iteration can terminate immediately if all the checks are satisfied. However, if this is not the case, there should be some check nodes which are checked in error. For a check node which is checked in error, there must exist at least one variable node which passes the wrong message to this check node. By the rule of min-sum algorithm, the messages updated at this check node are not reliable and preferable to be suppressed. 

Based on this observation, we propose an adaptivenormalized/offset min-sum algorithm. For this new NMS/OMS algorithm, the normalization/offset factor at a check node can be adjusted according to the state of this check node in each iteration. Here, the state of a check node is defined as the check-sum of the incoming messages. 

The following notations concern message-passing algorithms running on the Tanner graph of an LDPC code, and will be used throughout the paper. 

- _𝛾𝑛_ : a priori information of the variable node _𝑛_ in the form of log-likelihood ratio (LLR), 

- _𝛾_ ˜ _𝑛_ : a posteriori information (LLR) of the variable node _𝑛_ , 

- _𝛼𝑛,𝑚_ : the variable-to-check message from _𝑛_ to _𝑚_ , 

- _𝛽𝑚,𝑛_ : the check-to-variable message from _𝑚_ to _𝑛_ , 

- _𝜇_ : the normalized factor at check node, 0 _< 𝜇<_ 1, 

1089-7798/10$25.00 _⃝_ c 2010 IEEE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:00 UTC from IEEE Xplore.  Restrictions apply. 

668 

IEEE COMMUNICATIONS LETTERS, VOL. 14, NO. 7, JULY 2010 

- _𝜂_ : the suppressed factor at check node, 0 _< 𝜂<_ 1, 

- _𝜖_ : the offset value at check node, _𝜖>_ 0, 

- _𝜚_ : the multiplicative factor relative to the offset value, 0 _< 𝜚<_ 1. 

## _B. AN-MS Algorithm_ 

- S1: Initialization: 

**==> picture [188 x 47] intentionally omitted <==**

- S2: Hard decision: 

**==> picture [51 x 11] intentionally omitted <==**

**==> picture [60 x 11] intentionally omitted <==**

output **z** and terminate the decoding; 

S3: Check node processing: 

**==> picture [222 x 24] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

**==> picture [125 x 23] intentionally omitted <==**

**==> picture [149 x 11] intentionally omitted <==**

S5: A posteriori information: 

**==> picture [166 x 25] intentionally omitted <==**

S6: Variable node processing: 

**==> picture [154 x 10] intentionally omitted <==**

Go to step S2. 

In practice, the decoding is often forced to terminate if the maximum allowable number of decoding iterations is completed. By combining (2) and (3), the update rule for the check node which is checked in error can be written as 

**==> picture [242 x 24] intentionally omitted <==**

where _𝜈_ = _𝜇 ⋅ 𝜂_ . For ease of implementation, it is natural to employ two normalization factors at check nodes, one is _𝜇_ and the other is _𝜈_ = _𝜇 ⋅ 𝜂_ . 

Compared to the original NMS algorithm [5], the step S4) is new. It should be mentioned that the normalization factor appears multiplying while it appears dividing in [3], [5]. The use of multiplying factors may facilitate the implementation. Furthermore, the normalization factors may vary with the iteration number as commented in [5] and for simplicity we keep them fixed. For choice of normalization factors _𝜇_ and _𝜈_ , there is unfortunately no analytical results currently. Hence, we have to resort to tedious simulations. 

## _C. AO-MS Algorithm_ 

The AO-MS algorithm is almost the same as that of the AN-MS algorithm except the check node processing in steps S3) and S4), which can be stated as follows. If ( **h** _[𝑇] 𝑚[⋅]_ **[z]**[ == 0] mod 2), the message at check node _𝑚_ is updated as 

**==> picture [223 x 53] intentionally omitted <==**

However, if ( **h** _[𝑇] 𝑚[⋅]_ **[z]**[ == 1][mod][2)][,][the][offset][factor] _[𝜖]_[in][(7)] is replaced by _𝜍_ = (1 + _𝜚_ ) _⋅ 𝜖_ with _𝜚_ denoting a suppression factor. 

Compared to the NMS algorithm, the main shortage of the OMS algorithm is the difficulty in determining the value of offset _𝜖_ , which depends on the practical channel model and often requires the estimation of signal amplitude and noise variance. The density evolution approach for determining the offset value shown in [5] assumes that the channel model takes the form of 2 _𝜎_[2] _[ 𝑦][𝑛]_[with respect to the channel model (1), which,] in fact, requires to estimate the ratio of signal amplitude to noise variance. 

For the proposed AO-MS algorithm, the optimal value of _𝜖_ depends on the channel model just like the OMS algorithm. However, it is shown by extensive simulations that the optimal value of _𝜚_ is independent of the channel model. 

## _D. Computational Complexity_ 

Compared to the NMS/OMS algorithm, increase in computational complexity for the AN-/AO-MS algorithm can be well expected. In general, there are two aspects for additional complexity. One of which is the decision of the state of check nodes, and the other is the use of two normalization/offset factors, i.e., ( _𝜇, 𝜈_ ) or ( _𝜖, 𝜍_ ). 

For deciding the state of check nodes, it requires to compute the check-sum for each check node. Clearly, the amount of XOR operations for computing all check-sums is finally equal to the number of 1’s in _𝐻_ minus the number of rows in _𝐻_ . 

If the dynamic early termination of decoding as shown in Step S2) is used for both the NMS/OMS and the AN-MS/AOMS algorithms, the decision of the state of check nodes should be performed at each iteration for both algorithms. Hence, the check-sum operation at each iteration incur no additional implementation complexity. Therefore, the use of two normalization/offset factors dominates the additional computational complexity. 

For an ASIC implementation of the AN-/AO-MS algorithm, we argue that the adaptive use of two kinds of normalization/offset factors does not incur much more computational complexity. In fact, the multiplicative operation can be equivalently implemented as the series of both addition and shift operations. For example, the multiplication of _𝑥_ with 0.875 can be implemented as 0 _._ 875 _× 𝑥_ = _𝑥/_ 2 + _𝑥/_ 4 + _𝑥/_ 8, which includes three shift operations and two additions. Hence, when the value of the normalization factor switches from one to another, the group of shift coefficients changes accordingly in implementation. Therefore, the AN-MS algorithm requires two groups of shift coefficients, which are adaptively switched 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:00 UTC from IEEE Xplore.  Restrictions apply. 

669 

WU _et al._ : ADAPTIVE-NORMALIZED/OFFSET MIN-SUM ALGORITHM 

**==> picture [245 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
10−1<br>NMS<br>AN−MS<br>OMS<br>AO−MS<br>10−2 SP<br>10−3<br>10−4<br>10−5<br>10−6<br>10−7<br>0.75 0.8 0.85 0.9 0.95 1 1.05 1.1 1.15<br>Eb/N0, dB<br>Bit Error Rate<br>**----- End of picture text -----**<br>


Fig. 1. Bit error rate of the rate-1/2 DVB-S2 LDPC code with various decodings. 

**==> picture [245 x 194] intentionally omitted <==**

**----- Start of picture text -----**<br>
10−1<br>NMS<br>AN−MS<br>OMS<br>AO−MS<br>SP<br>10−2<br>10−3<br>10−4<br>10−5<br>10−6<br>2.1 2.15 2.2 2.25 2.3 2.35 2.4 2.45 2.5 2.55 2.6<br>Eb/N0, dB<br>Bit Error Rate<br>**----- End of picture text -----**<br>


Fig. 2. Bit error rate of the rate-3/4 LDPC code with various decodings. 

according to the state of check nodes. Hence, there is minor increase in memory and control logic for the AN-MS algorithm compared to the NMS algorithm. For the AO-MS algorithm, two offset factors ( _𝜖, 𝜍_ ) are also adaptively switched according to the value of check-sum at each check node, and the amount of increase in complexity is also minor compared to the OMS algorithm. 

## III. SIMULATION RESULTS 

To show the potential use of the AN-/AO-MS algorithm, we consider a long rate-1/2 LDPC code employed in digital video broadcasting standard for the second generation satellite applications (DVB-S2). For this long DVB-S2 LDPC code, its codeword length is 64800 and its performance can be very close to the Shannon limit (0.18 dB). The bit-error-rate (BER) performance of the DVB-S2 LDPC code under the NMS, the OMS, the AN-MS and the AO-MS decodings is shown in Fig. 1 with fixed-point simulations. The number of maximum allowable decoding iterations is 50. For fixed-point 

implementation of various iterative decoders, both the received samples and the passing messages along edges are quantized to 8 bits and two-phase decoding is employed. The SP algorithm with floating-point simulations is also shown. With 8-bit quantization, we observe little performance loss compared to the floating-point simulations. The normalization factor for the NMS algorithm is 27 _/_ 32 = 1 _/_ 2 + 1 _/_ 4 + 1 _/_ 16 + 1 _/_ 32. The normalizer factors ( _𝜇, 𝜈_ ) are set to be (27 _/_ 32 _,_ 3 _/_ 4) for the AN-MS algorithm. The offset factor for the OMS algorithm is 8 _/_ 50 and the offset factors ( _𝜖, 𝜍_ ) = (8 _/_ 50 _,_ 12 _/_ 50) for the AOMS algorithm. With a scaling factor of 50 for multiplying the channel model of (1), the offset factors can be well represented as integers in fixed-point environments. It is shown that the AN-MS algorithm has about 0.15 dB improvement compared to the NMS algorithm while the the AO-MS algorithm has about 0.1 dB improvement compared to the OMS algorithm. Both the AN- and AO-MS algorithms have about 0.1 dB loss compared to the SP algorithm. This improvement is observed at the BER of about 10 _[−]_[6] . 

We also consider a rate-3/4 irregular quasi-cyclic LDPC code of codeword length 8064. The degree profile of rate-3/4 LDPC code can be described as _𝜆_ ( _𝑥_ ) = 125 _[𝑥]_[+] 24[7] _[𝑥]_[2][+] 24[7] _[𝑥]_[6][ and] _𝜌_ ( _𝑥_ ) = _𝑥_[14] . The size of sub-matrix is 112. Fig. 2 shows the BER performance under various decodings. The normalization factors for the NMS and the AN-MS algorithms take the same values as that employed in DVB-S2 LDPC codes. The offset factor for the OMS algorithm is 4 _/_ 50 and the offset factors ( _𝜖, 𝜍_ ) = (4 _/_ 50 _,_ 6 _/_ 50) for the AO-MS algorithm. The number of maximum decoding iterations is set to be 60. It is shown in Fig. 2 that the proposed AN-/AO-MS algorithm performs very close to the SP algorithm. 

Finally, it should be noted that various normalization/offset factors are determined by limited simulations and there are still room for optimizing them by extensive simulations. 

## IV. CONCLUSION 

We have proposed an adaptive-normalized/offset min-sum decoding algorithm for LDPC codes. Compared to the NMS/OMS decoding, the proposed AN-/AO-MS decoding can achieve better performance with a minor increase in complexity. Therefore, we can expect that it is very competitive in practice. Compared to the AO-MS algorithm, the AN-MS algorithm does not require to estimate the signal-to-noise ratio for parameter optimization, which is welcome in practice. 

## REFERENCES 

- [1] Y. Kou, S. Lin, and M. Fossorier, “Low-density parity-check codes based on finite geometries: a rediscovery and more,” _IEEE Trans. Inf. Theory_ , vol. 47, pp. 2711–2736, Nov. 2001. 

- [2] M. Fossorier, M. Mihaljevic, and H. Imai, “Reduced complexity iterative decoding of low density parity check codes based on belief propagation,” _IEEE Trans. Commun._ , vol. 47, pp. 673–680, May 1999. 

- [3] J. Chen and M. P. Fossorier, “Near optimum universal belief propagation based decoding of low density parity check codes,” _IEEE Trans. Commun._ , vol. 50, pp. 406–414, Mar. 2002. 

- [4] M. R. Yazdani, S. Hemati, and A. H. Banihashemi, “Improving belief propagation on graphs with cycles,” _IEEE Commun. Lett._ , vol. 8, pp. 57–59, Jan. 2004. 

- [5] J. Chen and M. P. Fossorier, “Density evolution for two improved bpbased decoding algorithms of LDPC codes,” _IEEE Commun. Lett._ , vol. 6, pp. 208–210, May 2002. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:56:00 UTC from IEEE Xplore.  Restrictions apply. 


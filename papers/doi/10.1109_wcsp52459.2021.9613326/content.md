# Lowering the Error Floor of Quantized NR LDPC Decoders by a Post-Processing on Trapping Sets 

Hai He[1] , Ming Jiang[1][,][2] , Mingyang Zhu[1] , Chunming Zhao[1][,][2] 

> 1National Mobile Communications Research Laboratory, Southeast University, Nanjing 210096, China 

> 2The Purple Mountain Laboratories, Nanjing, China 

Email: {haihe seu, jiang ming, zhumingyang, cmzhao}@seu.edu.cn 

Abstract—This paper presents a novel two-stage quantized iterative decoder to lower the error floor for new radio lowdensity parity-check (NR LDPC) codes. In the first stage, quantized normalized min-sum (NMS) decoding algorithm is used to guarantee the performance of waterfall region. The second stage is executed if the syndrome reaches the specific criterion about the number of unsatisfied check constraints. The cyclicshifting CRC detection (CSCD) and syndrome assistant CSCD (SA-CSCD) algorithm designed to flip the error bits in possible positions based on the error patterns and the base graph (BG) to lower the error floor. Simulation results show that the proposed algorithm can effectively lower the error floor of NR LDPC while maintaining an acceptable complexity. 

Index Terms—LDPC codes, error floor, quantized decoder, min-sum algorithm 

## I. INTRODUCTION 

Low-density parity-check (LDPC) codes, proposed by Robert. G. Gallager in early 1960s’ [1] and later rediscovered by D. J. C. Mackay [2], have been widely used in communication systems. Due to the sparsity of parity-check matrices, belief propagation (BP) has been proposed to achieve capacityapproaching performance for LDPC codes. The normalized min-sum (NMS) and offset min-sum (OMS), as reducedcomplexity approximate versions for the BP algorithm, are hardware-friendly algorithms achieving ultra-high throughput. Due to their capacity-approaching performance and highthroughput implementation, quasi-cyclic (QC) LDPC codes [3], which have the architectures of block-parallel, have been accepted by 3GPP as the channel coding scheme for the 5G new radio [4] (NR) uplink and downlink shared channels. 

However, the performance degradation of LDPC codes in the high SNR region, called error floor, limits the applications of LDPC codes in high-speed and ultra-reliability scenarios. Richardson used the notion of trapping sets (TSs) [5], defined as the relatively small set of variable nodes leading to the error floor, to explain the phenomenon. The TS structures depend on not only transmission channels but also decoding algorithms. In practice, the quantizers used for the channel output and the message passing in the iterative decoders degrade error floor. 

Several research efforts about the design of LDPC codes have been devoted to lower the error floor. In [6], QC protograph codes are constructed by the careful selection of edge permutation shifts for the vulnerable subgraphs of the protograph whose inverse image can be short cycles with low 

extrinsic message degree values. Low error-floor irregular QCLDPC codes are constructed in [7] through the proper selection of cyclic permutation shifts within the exponent matrix to avoid any instance of leafless elementary trapping sets within a targeted set of structures. However, for an existing LDPC code such as the LDPC code in 5G standard, we can not modify its structure thus the only way to lower the error floor is to improve the decoding algorithm for specific TSs. 

Apart from designing LDPC codes, many improved decoding algorithms have been proposed to lower the error floor. An iterative decoding algorithm based on backtracking and a post-processing algorithm using message biasing scheme are introduced in [8] and [9] which boost the reliabilities of messages from unsatisfied checks and weakens the reliabilities of messages from the satisfied checks. Another effective error floor lowering technique for QC-LDPC codes was proposed in [10], where a post-processing is performed on specifically attenuated soft information when the decoding fails. 

In this paper, we propose a two-stage quantized decoding algorithm to lower the error floor for NR LDPC codes with base graph (BG) 2, which usually supports short-blocklength LDPC codes with relatively low code rates. In the first stage, a conventional quantized NMS decoding scheme is used to guarantee the performance in waterfall region. If the decoder declares a failure, the cyclic-shifting CRC detection (CSCD) and syndrome assistant CSCD (SA-CSCD) algorithm, designed to flip the bits in specific positions based on the error patterns, will be carried out as a post-processing in the second stage to lower the error floor. Here, the error patterns are collected by Monte-Carlo simulations and analyzed according to their TS structures. Due to the consideration of complexity, we set a criterion based on the number of unsatisfied paritycheck equations which enables the implementation of the second stage. The simulation results show that our approach can significantly lower the error floor by about one order with a reasonable complexity. 

## II. NR LDPC CODES AND TRAPPING SETS 

An LDPC code can be defined by a sparse parity-check matrix (PCM) denoted by H which has N columns and M rows corresponding to N coded bits and M parity-check constraints, respectively. In most practical applications, QCLDPC codes can be constructed by base matrices (BMs) or BGs, and are very efficient for encoder/decoder hardware 

978-1-6654-0785-4/21/$31.00 ©2021 IEEE Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:55:41 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [187 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
2<br>4<br>6<br>7<br>8<br>6 16 17 18<br>**----- End of picture text -----**<br>


Fig. 1. The partial structure of BG2 for a rate-1/2 short LDPC code, nb = 22 (circle marked) and mb = 12 (square marked). 

implementations. Each non-empty entry in a BG is substituted by a square Z × Z cyclic permutation matrix (CPM) with a specific shifting value, while each empty entry is replaced by a zero matrix (ZM). 

NR LDPC codes, which are QC-LDPC codes described by BG1 and BG2 in NR standard, consist of a highest-rate part and an incremental redundancy part. For example, the numbers of rows and columns of BG2 are mb = 42 and nb = 52, respectively, while those of highest-rate part in BG2 are only 4 and 14, where the number of columns for information bits is kb = 6∼10. The numbers of coded bits, parity-check constraints and information bits of an NR LDPC code can be calculated by the parameters of BG and the lifting size Z, M = mb × Z, N = nb×Z and K = kb×Z. Fig. 1 shows the partial structure of BG2 for a rate-1/2 short LDPC code as an example, nb = 22 and mb = 12, where dark blue sub-blocks and the light blue ones are correspond to the non-empty CPMs in highest-rate part and incremental redundancy part, respectively. Here, we use circles and squares to represent variable nodes (columns) and check nodes (rows) of BG2, where the number in circle or square represents the index of column or row. In the following discussion, we focus on the NR LDPC codes given by BG2 denoted by (nb, mb, Z), which are suitable candidates for lowrate and short blocklength transmission in uRLLC scenario. 

Considering the (22, 12, 96) NR LDPC code as an example, we carry out simulations over additive white Gaussian noise (AWGN) channel with quantized NMS decoding. The cyclic redundancy check (CRC) codes are used for error detection in NR and a decoding success is declared only when the decoded information bits satisfy the CRC constraint. The maximum number of iterations is set to 100 and the normalized factor is optimized to guarantee good waterfall performance. Moreover, the layered schedule is employed to speed up the convergence. In addition, a (24, 12, 80) LDPC code in WiMAX standard is selected for comparison. The simulation results in Fig. 2 show that the NR LDPC code performs not well in highSNR regions and an error floor is exhibited. At the Eb/N0 of 3.4 dB, we obtain one hundred decoding errors selected from 1.82 × 10[8] decoding trials, where the FER is 5.47 × 10[−][7] . The patterns of most decoding failures only consist of few error bits and can be regarded as dominant TSs. 

**==> picture [201 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [0]<br>NR LDPC,NMS<br>NR LDPC,NMS,TS groups<br>10 [−1] WiMAX LDPC,NMS<br>10 [−2]<br>10 [−3]<br>10 [−4]<br>10 [−5]<br>10 [−6]<br>1.00 1.25 1.50 1.75 2.00 2.25 2.50 2.75 3.00<br>Eb/N0(dB)<br>FER<br>**----- End of picture text -----**<br>


Fig. 2. FER performances of NMS decoder for (22, 12, 96) NR LDPC code (black line) and (24, 12, 80) WiMAX LDPC code (red line). The blue line is the error rate caused by the considering TS groups of NR LDPC code. 

TABLE I 

STATISTIC OF ERROR PATTERNS AND OFFSET PATTERNS FOR (22, 12, 96) NR LDPC CODE 

|error pattern Ψ|offset pattern P|number|
|---|---|---|
|[ 3 ]|[ 0 ]|13|
|[ 6 ]|[ 0 ]|61|
|[ 8 ]|[ 0 ]|16|



A TS [5] is defined as a small set of variable nodes associated with the error bits, which makes the decoder be “trapped” and can no longer correct these error bits. From the perspective of BG, a typical (a, b) TS is a set of a variable nodes from a columns and b ≥ 0 odd-degree check nodes from b rows neighboring in the subgraph of BG. Specifically, the TSs with small size a give major contributions to error floors. For QC-LDPC codes, if an (a, b) TS is identified, other Z − 1 isomorphic TSs can be found by cyclically shifting the variable nodes in the TS. In later, a TS group is used to represent these Z isomorphic TSs constructed by cyclic shifting. 

Most of decoding errors we collected at high SNR can be classified into several major TS groups and the positions of error information bits can be derived according to the indices of unsatisfied parity-checks and the structures of TS groups. To describe the relationship between TS groups and decoding error floor, we define the error pattern Ψ = [Ψ0, Ψ1, ..., ΨV−1] of size V, which records the indices of the columns corresponding to error information bits in the BG, and the offset pattern P = [P0, P1, ..., PV−1], where Pi is the relative error positions in 0∼Z - 1 for the variable node Ψi. Further, we define the check node error pattern Φ = [Φ0, Φ1, ..., ΦC−1] for a TS group, where C is the size of Φ, recording the indices of error check nodes in highest-rate part of BG, and the offset pattern Q = [Q0, Q1, ..., QC−1] from check node perspective, where Qi is the relative unsatisfied position in 0∼Z - 1 for the check node Φi. We can calculate one set of possible positions of error information bits R = [R0, R1, ..., RV−1] by 

**==> picture [215 x 11] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:55:41 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [101 x 100] intentionally omitted <==**

**----- Start of picture text -----**<br>
2<br>4 8 18<br>6<br>6 7<br>16 17<br>**----- End of picture text -----**<br>


Fig. 3. A (4, 2) TS group of (22, 12, 96) NR LDPC code 

A TS group consists of Z isomorphic TSs thus Ψ (or Φ) contains Z positions of error information bits (or check equations), where other Z − 1 positions can be obtained by cyclic shifting. In particular, if the offset pattern P corresponding to one TS group only has one entry, the value of this entry can be set in range of 0∼Z − 1 with same mean and is set as 0 in this paper. 

We can correct decoding errors according to the error patterns and offset patterns. Ri Analyzing one hundred decoding errors of (22, 12, 96) NR LDPC code and counting the error patterns and offset patterns as shown in Table I, we find that the error information bits mainly locate at the 3rd, 6th and 8th variable nodes in BG2. For example, Fig. 3 shows a (4, 2) TS group which is high related to the 6th variable node, where red circles (squares) represent the variable nodes (check nodes) contain error information bits (unsatisfied parity-checks) and the blue circles (squares) represent no error bits (all satisfied parity-checks). According to our definition, the TS group is related to Ψ = [6] and P = [0] and one set of the possible positions of error information bits can be calculated by R = [R0] = [(Ψ0−1)×Z+P0] = [(6−1)×96+0] = [480], while other sets of possible error positions can be obtained by cyclic shifting of R in the range of (480, 575]. 

From Fig. 1, we find that three information variable nodes shown in Table I only have two ’1’ entries in the highestrate part, while other information variable nodes are at least with degree three. We also show the FER performance which only considers the decoding errors caused by these three TS groups in Fig. 2. It can be seen that these three TS groups almost determine the error 

The error patterns in Table I can be identified by the paritycheck constraints. Moreover, some error patterns satisfying all parity-check equations can be detected through the CRC test. For example, we find that the error pattern [1, 2, 3, 6, 7, 8] is a valid codeword in the simulation of the (17, 7, 224) NR LDPC code. 

## III. AN EFFICIENT POST PROCESSING ON TS GROUP 

Consider the binary phase shift keying (BPSK) transmission over an AWGN channel. A codeword c = [c0, c1, ...cN −1] is mapped to x = [x0, x1, ..., xN −1] by xi = 1 − 2ci. y = [y0, y1, ..., yN −1] is the received sequence, where yi = xi + ni and ni is an independent Gaussian random variable with mean 

ˆ zeroˆ and varianceˆ ˆ σ[2] . The sequence c = [ˆc0, ˆc0, ..., ˆcN −1] and b = [ˆb0, b0, ..., bK−1] are the output of a quantized NMS decoder of LDPC codes and the decoded information bits including CRC bits, respectively. In our simulations, a 5-bit uniformly quantized layered NMS decoder is implemented. 

The first stage of our scheme is just the conventional NMS decoding. If the decoded information bits b[ˆ] satisfy the CRC test, the iterative decoding will be early stopped and a decoding success is declared. Otherwise, the secondstage post-processing is employed, where the syndrome s is ˆ calculated by s = Hc[T] . Then we get the number of the unsatisfied check nodes as ||s||, where ||·|| is the norm of a vector. Since we only consider the decoding errors caused by the small TS groups that are the most harmful errors in the error floor region, the decoding errors with ||s|| > 10 are discarded. 

In the second stage, a simple post-processing scheme called CSCD is applied. The error patterns Ψ s and offset patterns Ps have been collected by Monte-Carlo simulations. Total v TS groups are considered to be corrected and {R0, ..., Rv−1} are used to describe different sets of possible error information bits’ positions which belong to different error patterns. Each set of possible positions Ri of size Vi is calculated by Eq. (1). We flip the bits at these positions by 

**==> picture [239 x 16] intentionally omitted <==**

where b[ˆ] is the output sequence of decoded information bits from the first stage. Because each error pattern represents a TS group, we can get other sets of possible error information bits’ positions R′ by cyclic shifting the values of R for total Z times and 

**==> picture [219 x 14] intentionally omitted <==**

where z = 1, .., Z − 1, i = 0, .., v − 1 and j = 0, ..., Vi − 1. These estimated information sequences are tested by CRC and the second stage will stop early if one sequence satisfies CRC test. The CSCD algorithm is described in detail by Algorithm 1. Although Algorithm 1 has triple loops, the number of the error patterns v is limited and the specific criterion is used to guarantee a controllable complexity. 

Further, most decoding errors collected in the error floor region do not satisfy the parity-check of the LDPC code, thus we can directly correct some decoding errors by their syndromes. When the decoded sequence only has one error bit in the related variable node of TS, the syndrome is significantly influenced by the error bit. Combining the syndrome and BG structure, we can accurately locate to the position of the error bit but need more storage resource to record the error patterns Φs and offset patterns Qs of check nodes. Obviously the numbers of check node error patterns and offset patterns are both equal to v. Simulation results show that most of decoded sequences have one error bit in highest-rate part at high SNR region. More error bits cause the larger number of unsatisfied parity-checks, so our proposed criterion can ignore this complex scenario. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:55:41 UTC from IEEE Xplore.  Restrictions apply. 

Algorithm 1 cyclic-shifting CRC detection (CSCD). 

**==> picture [230 x 215] intentionally omitted <==**

**==> picture [255 x 246] intentionally omitted <==**

## TABLE II 

ERROR PATTERNS AND OFFSET PATTERNS OF CSCD FOR NR LDPC WITH K = 3840, RATE = 1/4,1/2,2/3 

|variable nodes<br><br>|variable nodes<br><br>|variable nodes<br><br>|variable nodes<br><br>|
|---|---|---|---|
|error pattern<br>|offset pattern<br>|error pattern<br>|offset pattern<br>|
|[3,8]<br>|[0,8]<br>|[3,6,7,8]<br>|[103,0,8,95]<br>|
|[3,8]<br>|[57,0]<br>|[3,6,7,8]<br>|[34,0,323,46]<br>|
|[3,8]<br>|[0,12]<br>|[3]<br>|[0]<br>|
|[3,6]<br>|[103,0]<br>|[6]<br>|[0]<br>|
|[3,6]|[34,0]|[8]|[0]|
|[3,6]|[74,0]|[6,8]|[0,46]|
|[3,6,7]|[0,350,289]|[6,8]|[0,95]|
|[3,6,7]|[103,0,8]|[3,6,8]|[0,232,327]|



After the first stage, the syndrome can be calculated by Hcˆ[T] , where cˆ represents the decoded sequence of the first stage decoding. Then non-zero elements of syndrome which belong to highest-rate part are defined as error check positions denoted by S = {i|si > 0}. Calculate indices of rows Φ[ˆ] = [ Φ[ˆ] 0, Φ[ˆ] 1, ..., Φ[ˆ] C] and offset Q[ˆ] = [ Q[ˆ] 0, Q[ˆ] 1, ..., Q[ˆ] C] of S by 

**==> picture [207 x 28] intentionally omitted <==**

If ′Φ[ˆ] is equal to one of the collected syndrome patterns Φs, Φto ,Q[ˆ] weandcanQdirectly′ by get the position of the error bit according 

**==> picture [240 x 13] intentionally omitted <==**

′ ′ ′ where Ψ and P are corresponding to Φ . We call the method as SA-CSCD which is described in Algorithm 2. SA-CSCD can be thought as the supplement of CSCD and significantly reduce the complexity of CSCD by using small storage resource. 

## TABLE III 

ERROR PATTERNS AND OFFSET PATTERNS OF SA-CSCD FOR NR LDPC WITH K = 3840, RATE = 1/4,1/2,2/3 

|variable nodes|variable nodes|check nodes|check nodes|
|---|---|---|---|
|error pattern|offset pattern|error pattern|offset pattern|
|[3]|[193]|[1,4]|[27,18]|
|[6]|[170]|[2,4]|[78,98]|
|[8]|[15]|[2,4]|[212,281]|



## IV. RESULTS 

In this section, we give some simulations on our proposed method including CSCD and SA-CSCD for NR LDPC codes. We present simulation results of different NR LDPC codes which have different lengths of information bits (including 3840, 1440 and 960) and different rates (including rate-2/3, rate-1/2 and rate-1/4). We discuss the simulation results of BP decoding, quantized NMS decoding and our proposed two-stage quantized decoding. The BP decoding, quantized NMS decoding and the first stage of our algorithm are carried out by layered scheduling, where the maximum number of iterations is set to 100. The 5-bit uniform quantization scheme is implemented, and the saturation level of the quantization scheme is optimized by Monte-Carlo simulations. 

Fig. 4 shows the simulation results of NR LDPC with K = 3840. For rate-1/4, rate-1/2 and rate-1/3, the normalized factors are set as 0.875, 0.875 and 0.9375, respectively. The error patterns and offset patterns are provided in Table II and Table III. This table lists all TS groups, but we can choose part of these to simulate according to code rates. Simulation results show that the gap between BP decoding and quantized NMS decoding decreases with the increasing of rate and the gap is about 0.1∼0.4dB at the waterfall region. But the performances of error floor don’t have significant 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:55:41 UTC from IEEE Xplore.  Restrictions apply. 

**==> picture [201 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [0]<br>10 [−1]<br>10 [−2]<br>10 [−3]<br>10 [−4]<br>10 [−5]<br>10 [−6] (17,7,384),rate-2/3<br>(22,12,384),rate-1/2<br>(42,32,384),rate-1/4<br>10 [−7]<br>−1.0 −0.5 0.0 0.5 1.0 1.5 2.0 2.5 3.0<br>Eb/N0(dB)<br>FER<br>**----- End of picture text -----**<br>


Fig. 4. FER performance of BP decoding (red line), quantized NMS decoding (black line) and quantized NMS decoding with our post-processing (blue line) for the (nb, mb, 384) NR LDPC with information length K = 3840. 

**==> picture [201 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [0]<br>10 [−1]<br>10 [−2]<br>10 [−3]<br>10 [−4]<br>10 [−5]<br>10 [−6] (17,7,144),rate-2/3<br>(22,12,144),rate-1/2<br>(42,32,144),rate-1/4<br>10 [−7]<br>−1.0 −0.5 0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5<br>Eb/N0(dB)<br>FER<br>**----- End of picture text -----**<br>


Fig. 5. FER performance of BP decoding (red line), quantized NMS decoding (black line) and quantized NMS decoding with our post-processing (blue line) for the (nb, mb, 144) NR LDPC with information length K = 1440. 

**==> picture [201 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [0]<br>(17,7,96),rate-2/3<br>(22,12,96),rate-1/2<br>10 [−1] (42,32,96),rate-1/4<br>10 [−2]<br>10 [−3]<br>10 [−4]<br>10 [−5]<br>10 [−6]<br>10 [−7]<br>−1 0 1 2 3 4<br>Eb/N0(dB)<br>FER<br>**----- End of picture text -----**<br>


Fig. 6. FER performance of BP decoding (red line), quantized NMS decoding (black line) and quantized NMS decoding with our post-processing (blue line) for the (nb, mb, 96) NR LDPC with information length K = 960. 

relation with rate, where the rate-1/2 NR LDPC code has the worst error floor. The error floor of quantized NMS decoding is about FER of 10[−][3] ∼10[−][4] . Our proposed methods, which are post-processing methods and don’t influence the 

waterfall performance, lower error floor about 1/2∼1/10 and the performance substantially improves with the increase of code rate. 

Fig. 5 compares the FER of three different decoding schemes for NR LDPC codes with K = 1440. The error floors of the these codes all occur at FER of 10[−][3] with quantized NMS decoding. And our proposed post-processing can efficiently lower the error floor to FER of 10[−][4] . At low FER, two-stage decoder can achieve about 0.3 dB gain over the quantized NMS algorithm. Fig. 6 plots results of different decoders for NR LDPC with K = 960. Similar to the results of longer NR LDPC codes, our method can noticeably lower the error floor by an order of magnitude. 

## V. CONCLUSION 

In this paper, a TS-based post-processing for quantized iterative decoder is proposed to lower the error floor of NR LDPC codes. The TS information for quantized decoding are collected by Monte-Carlo simulations and analyzed according to the BG structure. Our proposed post-processing will be performed when the first-stage decoding fails. Two simple methods, CSCD and SA-CSCD, can be used in the postprocessing. The provided simulation results show that our proposed scheme can efficiently lower the error floor of quantized decoders for NR LDPC codes. 

## ACKNOWLEDGEMENT 

This work was supported by the National Natural Science Foundation of China under Grant 61771133 and the Jiangsu Province Basic Research Project under Grant BK20192002. 

## REFERENCES 

- [1] R. G. Gallager, “Low density parity-check codes,” IRE Trans. Inf. Theory, vol. IT-8, no. 1, pp. 21–28, Jan. 1962. 

- [2] D. J. C. MacKay, “Good error-correcting codes based on very sparse matrices,” IEEE Trans. Inf. Theory, vol. 45, no. 2, pp. 399–431, Mar. 1999. 

- [3] Y. Kou, S. Lin and M. P. C. Fossorier, “Low-density parity-check codes based on finite geometries: a rediscovery and new results,” IEEE Trans. Inf. Theory, vol. 47, no. 7, pp. 2711–2736, Nov. 2001. 

- [4] 3GPP, “3rd generation partnership pProject; Technical specification group radio access network; NR; Multiplexing and channel coding (Release 15),” 3GPP TS 38.212 V15.5.0, Mar. 2019. 

- [5] T. Richardson, “Error floors of LDPC codes,” in Proc. 2003 Annu. Allerton Conf., pp. 1426—1435. 

- [6] R. Asvadi, A. H. Banihashemi and M. Ahmadian-Attari, “Design of finite-length irregular protograph codes with low error floors over the binary-input AWGN channel using cyclic liftings,” IEEE Trans. Commun., vol. 60, no. 4, pp. 902–907, April 2012. 

- [7] B. Karimi and A. H. Banihashemi, “Construction of irregular protograph-based QC-LDPC codes with low error floor,” IEEE Trans. Commun., vol. 69, no. 1, pp. 3–18, Jan. 2021. 

- [8] J. Kang, Q. Huang, S. Lin and K. Abdel-Ghaffar, “An iterative decoding algorithm with backtracking to lower the error-floors of LDPC codes,” IEEE Trans. Commun., vol. 59, no. 1, pp. 64–73, January 2011. 

- [9] Z. Zhang, L. Dolecek, B. Nikolic, V. Anantharam and M. J. Wainwright, “Lowering LDPC error floors by postprocessing,” in proc. 2008 IEEE Globecom Conf., pp. 1–6. 

- [10] H. Lee, P. Chou and Y. Ueng, “An effective low-complexity errorfloor lowering technique for high-rate QC-LDPC codes,” IEEE Commun. Lett., vol. 22, no. 10, pp. 1988–1991, Oct. 2018. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:55:41 UTC from IEEE Xplore.  Restrictions apply. 


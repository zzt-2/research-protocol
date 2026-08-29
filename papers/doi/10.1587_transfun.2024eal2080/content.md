IEICE TRANS. FUNDAMENTALS, VOL.E108–A, NO.6 JUNE 2025

878

## <u>LETTER</u>

# **Reliability-List-Based Check-Belief Propagation Decoding of LDPC Codes**<sup>**∗**</sup>

**Zhe LIU**<sup>†a)</sup> **, Wu GUAN**<sup>†b)</sup> **, Ziqin YAN**<sup>†c)</sup> **,** **_and_ Liping LIANG**<sup>†d)</sup> **,** **_Nonmembers_**

**SUMMARY** Reliability-based belief propagation (RBP) decoding algorithms are used to decode low-density parity-check (LDPC) codes. However, due to the reliability of comparing and sorting in traditional algorithms, conventional RBP decoders significantly lose in resource consumption. This letter presents an enhanced reliability list-based check-belief propagation (RL-CBP) algorithm. The RL-CBP algorithm reduces computational complexity by scheduling a concise list of check-beliefs. Moreover, the list is applied for comparisons and selections of check-beliefs. The selected checkbelief transforms the decoding message between edges; all check-beliefs are iteratively enlarged according to the reliabilities, and high-performance decoding will be achieved. The simulation results and analyses show that the proposed method achieves a reliability-list gain compared with the checkbelief propagation (CBP) algorithm but consumes much fewer calculations than the traditional RBP algorithm.

**_key words:_** _belief propagation (BP), check-belief, low-density parity-check (LDPC) codes, reliability-list, scheduling_

### **1. Introduction**

Since LDPC codes were rediscovered in the 1990s, various low-complexity iterative decoding algorithms have been proposed to balance the performance and complexity of LDPC decoding [1]. The flooding belief propagation (FBP) algorithm is the fundamental decoding algorithm for LDPC code [2], and most decoding algorithms for LDPC code are proposed based on the BP decoding algorithm. It updates all the variable nodes simultaneously using the previously generated check-to-variable (C2V) and then updates all the check nodes simultaneously using the previously generated variable-to-check (V2C). To reduce the complexity, various simplified FBP algorithms are presented, such as the minsum [3], normalized min-sum algorithms [4]. A shuffled version of the belief propagation (SBP) algorithm is proposed to provide a good trade-off between error performance and complexity for decoding LDPC codes [5]. To speed up the LDPC decoding process, layered belief-propagation (LBP) has been proposed to converge faster than the traditional flooding schedule while allowing parallel decoding of

Manuscript received September 17, 2024. Manuscript revised December 1, 2024. Manuscript publicized December 19, 2024.

†School of Integrated Circuits, Beijing University of Posts and Telecommunications, Beijing, 100876, China.

> ∗This work was supported by the National Natural Science Foundation of China (Grant No. 62271069). a) E-mail: liu_zhe@bupt.edu.cn

b) E-mail: guanwu@bupt.edu.cn (Corresponding author) c) E-mail: yzqqqaqq@bupt.edu.cn d) E-mail: liangliping@bupt.edu.cn DOI: 10.1587/transfun.2024EAL2080

LDPC codes [6]. The LBP method calculates the checkbelief propagation in rows or columns to get the check-belief propagation of every node [7], resulting in improved data through rate in decoding. The above non-dynamic message updating strategies only update and propagate messages in predetermined orders. However, although the non dynamic message updating strategies have improved performance compared with the FBP algorithm, applying the latest updating message to the following message update process is still impossible. A kind of BP decoding algorithm based on a reliability scheduling method is presented called residual BP (RBP) to lessen the number of iterations ulteriorly [8]. The decoding algorithms need to speed up the convergence and reduce the cost of the average calculation in each message update process [9]. The FBP and LBP methods require many registers to store V2C and C2V messages, increasing decoding complexity and power consumption.

The check-belief propagation (CBP) decoding method has been presented to reduce decoding complexity [10]. It transfers check-belief message between two check-nodes via only one variable node; compared with other LDPC decoding methods, the CBP renews check-belief propagation through two nodes, which eliminates accumulations and multiplications in the process of LDPC decoding. However, the CBP algorithm cannot take advantage of the reliability of the check nodes.

In order to improve the propagation rate of checkbeliefs, the RBP algorithms need to compare the value of all residuals to choose the edges corresponding to the maximum residual for priority decoding. However, the comparisons of residuals lead to increasing resource consumption. To improve convergence, various modified residualbased algorithms including node-wise RBP (NW-RBP) [11], silent-variable-node-free RBP (SVNF-RBP) [12], residualdecaying-based RBP (RD-RBP) [13], and conditional innovation based RBP (CI-RBP) [14] were presented. Aiming to tackle the problem of large amount of residual comparisons, the reliability-list-based check-belief propagation is proposed to decrease the number of comparisons for checkbeliefs, which can reduce the decoding complexity with little performance loss.

### **2. Preliminaries**

A binary ( _N_ , _K_ ) LDPC code with rate _R_ = _K_ / _N_ is defined by a code graph _G_ = ( _V_ , _C_ , _E_ ), where _V_ , _C_ , and _E_ represent the set of variable-nodes, check-nodes, and edges, respectively.

Copyright © 2025 The Institute of Electronics, Information and Communication Engineers

LETTER

879

The set _V_ contains _N_ variable nodes, and there are _M_ = _N_ − _K_ check nodes in _C_ . Let _N_ (v) and _N_ ( _c_ ) denote the adjacent check-nodes of variable-node v and adjacent variable-nodes of check-node _c_ , respectively. The symbols _N_ (v)\ _c_ and _N_ ( _c_ )\v denote the set _N_ (v) except for check-node _c_ and the set _N_ ( _c_ ) except for variable-node v, respectively.

### 2.1 CBP Decoding

In previous decoding methods such as BP and LBP, the V2C and C2V messages are produced in the cumulative calculations of contiguous nodes, enlarging the decoding complexity.

In order to solve this problem, CBP decoding exchanges each message of LDPC codes between two check nodes. The



where _Sc_ i is the parity check corresponding to check-node _c_ i. Let _Y_ be the signal received.

The check-belief represents the probability that the parity-check of the check node is satisfied. The check-belief is a positive value if the parity-check is satisfied.

The process of the CBP algorithm can be summarized as follows.

For each check-node _c_ i, the updating of check-belief is recursively. The latest updated adjacent check-node of variable-node va is presented as _c_ j.

Calculate the updating message of check-belief from check-node _c_ j to variable-node va (B2V) following (2)



where





Corresponding messages for variable-node va (V2C) updates following (5) and the update of posterior information generates as (6).



Update the V2C message to check-belief (C2B) following (7).



where _n_ = 0, 1,. . ., | _N_ ( _c_ i)| − 1, | _N_ ( _c_ i)| is the number of elements in set _N_ ( _c_ i), and





In order to make all the parity-checks satisfied, every

check-belief is enlarged by iteration in a serial recursive order. The CBP algorithm propagates check-belief with no cumulative calculations, which causes a low decoding performance loss.

### 2.2 RBP Decoding

The basic idea of RBP decoding is to adopt a dynamic scheduling strategy, using residuals as a measurement and prioritizing the update for the message of the highest residuals. In the RBP algorithms, the residual is defined as the degree of deviation before and after a message update process. The message transition of RBP is exchanged in descending order of extrinsic information value between edges [15]. The RBP algorithm performs a better convergence than FBP and LBP due to the application of the informed dynamic scheduling strategy [16].

The C2V residual is generated by the magnitude difference between the current C2V message _R_ ci →va and the precomputed message _R_ c<sup>pre</sup> i →va<sup>.</sup>



The RBP schedules the edge with the maximum C2V residual to be updated, and each updated C2V message is propagated to its adjacent nodes. In this way, the message of check-node is promoted from all the adjacent nodes renewal, which results in a significantly increasing convergence speed. However, the V2C and C2V processes collect messages from all the neighboring nodes, which increases the calculation complexity of decoding.

### **3. Reliability-List-Based CBP Decoding**

### 3.1 Reliability-List-Based Check-Belief Scheduling

In CBP decoding, it updates the check-belief for all check nodes. However, the check-belief of some nodes will become stable after a certain number of updates, so it is a waste of resources and may introduce unreliable information. To improve the performance of CBP, residuals are used to select the check-node with higher extrinsic information. Meanwhile, a small reliability list is adopted to reduce the number of check-nodes involved in the residual comparisons. This filters out some check-beliefs that have become stable and accelerated the transmission of newly updated reliable messages to a certain extent. In general, we summarize the decoding process of RL-CBP into two steps:

- 1) Scheduling decoding the maximum reliability checknode in the reliability list

- 2) Update the reliability list

The RL-CBP decoding process is shown in Fig. 1. In this process, firstly, the C2V message _L_ c<sup>ne</sup> i →<sup>w</sup> va<sup>isupdated</sup> from the a posterior check-belief Ωci . Secondly, the corresponding posterior information Λ<sup>ne</sup> va<sup>w</sup> of variable-node va is updated. Thirdly, the variable node va sends a new V2C message _L_ v<sup>ne</sup> a →<sup>w</sup> c j<sup>to the check node</sup><sup>_c_j.Then, the check node</sup>

IEICE TRANS. FUNDAMENTALS, VOL.E108–A, NO.6 JUNE 2025

880





**Fig. 1** Reliability-list-based check-belief scheduling.

_c_ j updates its check-belief Ω<sup>ne</sup> c j<sup>w</sup> in a recursive way. Finally, renew the reliability list if the absolute value of the new reliability _R_ v<sup>ne</sup> a<sup>w</sup> is higher than the minimum absolute value of check-belief in the list, update check-beliefs and reliabilities for all check nodes connected to the variable-node va except _c_ i, and update reliability and check-belief of checknode until all variable nodes connected to the check-node _c_ i are traversed.

The reliability value of the check-node _c_ j is calculated

by:



Based on the above process, the proposed RL-CBP method is summarized by using the pseudocode shown in Algorithm 1. The stopping criteron for RL-CBP is either all the check-beliefs satisfying positive values or the reaching of a predefined maximum number of iterations. The initialization of Algorithm 1 is based on the binary phase shift keying (BPSK) modulated additive white Gaussian noise (AWGN) channel.



### 3.2 Choice of for List Parmeters

We will find an appropriate size for the reliability list by balancing error rate and convergence speed. Too few check nodes in the list may cause a loss of decoding messages and prevent successful decoding. An excessive number of check nodes stored in the list will increase the complexity of calculation and cause difficulties for hardware implementation.

**Fig. 2** Performance comparisons of the proposed RL-CBP methods with the reliability list for different lengths. (a) Length-2048 irregular codes. (b) Length-8192 irregular codes.



The error rate performance and the convergence speed of the RL-CBP algorithm for different sizes of the reliability list under different irregular LDPC codes are shown in Fig. 2 and Fig. 3. The regular (3, 6) LDPC codes and irregular LDPC codes under degree distributions (λ( _x_ ) = 0.45 _x_ + 0.3708 _x_<sup>2</sup> + 0.0307 _x_<sup>3</sup> + 0.1485 _x_<sup>11</sup> , ρ( _x_ ) = 0.5467 _x_<sup>4</sup> + 0.4533 _x_<sup>5</sup> ) are applied in simulation [17]. The progressive edge growth (PEG) algorithm is used to construct the LDPC codes. In addition, the code rate of LDPC codes is set as 1/2, the simulation employs LDPC codes with code lengths of 2048 and 8192, and the maximum number of iterations is 50.

We can see that the error rate performs best when the _L_ total equals 64. Meanwhile, we can see that the convergence has little increase when _L_ total is bigger than 64. Con-

**Fig. 3** Iteration performance comparisons of the RL-CBP methods for Length-2048 irregular codes and Length-8192 irregular codes.

LETTER

881

**Table 1** Total complexity.









**Fig. 4** Performance comparisons of the BP, LBP, RBP, CBP, and the proposed RL-CBP methods. (a) Length-2048 irregular codes. (b) Length2048 regular codes.



**Fig. 6** Convergence performance comparisons of the FBP, LBP, RBP, CBP, and the proposed RL-CBP methods. (a) Length-2048 codes. (b) Length-8192 codes.



**Fig. 5** Performance comparisons of the BP, LBP, RBP, CBP, and the proposed RL-CBP methods. (a) Length-8192 irregular codes. (b) Length8192 regular codes.

### to RBP.

The average number of iterations is simulated to measure the convergence speed for LDPC decoding. The simulation results for the regular and irregular codes are shown in Fig. 6. We find that the proposed RL-CBP has twice the convergence speed compared to CBP, a similar convergence speed as RBP, and it reaches a lower BER than FBP and LBP under the same number of iterations. The proposed RL-CBP method can combine the advantages of both CBP and RBP approaches. The transform of the decoding message is processed between edges with no cumulative calculation. Furthermore, a limited list of reliabilities is proposed for the reliability comparing, reducing the comparisons for each reliability value in decoding.

sidering the cost of resource consumption, the _L_ total is selected as 64 for RL-CBP in this letter.

### **4. Simulation Results**

In this section, the performances of the traditional algorithms, the CBP algorithm, and the proposed RL-CBP algorithm are analyzed, the setting of simulation parameters is same as Sect. 3.2.

### 4.1 Error Correction Performance

Figure 4 and Fig. 5 illustrate the error correction performance of the different decoding algorithms for both irregular and regular LDPC codes in the AWGN channel. When the 2048 irregular code is used, and the BER approaches 10<sup>−5</sup> , RLCBP can obtain a coding gain of approximately 0.06 dB over CBP 0.11 dB over LBP, 0.16 dB over FBP, and is very close

### 4.2 Calculation Complexity

In this subsection, we analyze the decoding complexity for the proposed RL-CBP algorithms according to the number of message updates in each iteration and the calculations required for each message update. Let _d_ v<sup>iand</sup><sup>_d_j</sup> c<sup>denotethe</sup> average degrees of variable and check nodes, respectively. The calculation complexities of different BP decoding algorithms are shown in Table 1. The data for FBP, LBP, RBP and CBP in the table are from [10].

- a) Updates in Each Iteration: For each check-belief renewed process in the proposed strategy, there are _d_ c<sup>j</sup> B2V updates, _d_ c<sup>jV2Cupdates,</sup><sup>_d_j</sup> c<sup>C2Bupdates,and</sup> _M_ · _L_ · ( _d_ v − 1) updates of comparison, where _L_ is the short for _L_ total.

- b) Calculation in Each Update: In the proposed RL-CBP method, one product exists in the update process of B2V, two sums (including substrates) in the V2C up-

IEICE TRANS. FUNDAMENTALS, VOL.E108–A, NO.6 JUNE 2025

882

   - date process, one product in the C2B update, and one comparison for the update of the reliability list.

- c) Total complexity: We set the convergence speed of decoding as 1/4 for RBP and RL-CBP to obtain the total complexity. From Table 1, there are much less comparisons in RL-CBP than in RBP. Hence, the complexity of the proposed decoding strategy is much smaller than that of RBP.

### **5. Conclusion**

In this letter, we propose a decoding method of sequence scheduling based on the reliability list in sequence order. It propagates check-belief between edges selected from the small list and reduces the computational complexity. This reduces comparisons in scheduling, and significantly improves the efficiency of the decoding process. Simulation and analysis results show that the proposed algorithm has little performance loss compared with the previous reliability-based algorithms and consumes much fewer comparisons than the traditional RBP algorithms.

#### **References**

- [1] N. Wiberg, H. Loeliger, and R. Kotter, “Codes and iterative decoding on general graphs,” European Transactions on Telecommunications, vol.6, no.5, pp.513–525, 1995.

- [2] D.J. MacKay and R.M. Neal, “Near Shannon limit performance of low density parity check codes,” Electronics Letters, vol.33, no.6, pp.457–458 1997.

- [3] J. Zhao, F. Zarkeshvari, and A.H. Banihashemi, “On implementation of min-sum algorithm and its modifications for decoding low-density parity-check (LDPC) codes,” IEEE Trans. Commun., vol.53, no.4, pp.549–554, 2005.

- [4] J. Chen, A. Dholakia, E. Eleftheriou, M.P. Fossorier, and X.Y. Hu, “Reduced-complexity decoding of LDPC codes,” IEEE Trans. Commun., vol.53, no.8, pp.1288–1299, 2005.

   - [6] D.E. Hocevar, “A reduced complexity decoder architecture via layered decoding of LDPC codes,” IEEE Workshop on Signal Processing Systems, 2004, SIPS 2004, pp.107–112, 2004.

   - [7] H. Li, H. Ding, L. Zheng, Z. Lei, H. Xiong, and T. Wang, “An efficient scheduling scheme for layered belief propagation decoding of regular LDPC codes,” 2016 8th International Congress on Ultra Modern Telecommunications and Control Systems and Workshops (ICUMT), pp.397–400, Oct. 2016.

   - [8] A.I.V. Casado, M. Griot, and R.D. Wesel, “Informed dynamic scheduling for belief-propagation decoding of LDPC codes,” 2007 IEEE International Conference on Communications, pp.932–937, June 2007.

   - [9] D.-D. Yan, X.-K. Fan, Z.-Y. Chen, and H.-Y. Ma, “Low-loss belief propagation decoder with Tanner graph in quantum error-correction codes,” Chinese Physics B, vol.31, no.1, 010304, 2022.

   - [10] W. Guan and L. Liang, “Check-belief propagation decoding of LDPC codes,” IEEE Trans. Commun., vol.71, no.12, pp.6849–6858, Dec. 2023, doi: 10.1109/TCOMM.2023.3308155.

   - [11] A.I.V. Casado, M. Griot, and R.D. Wesel, “LDPC decoders with informed dynamic scheduling,” IEEE Trans. Commun., vol.58, no.12, pp.3470–3479, Dec. 2010

   - [12] H.-C. Lee, Y.-L. Ueng, S.-M. Yeh, and W.-Y. Weng, “Two informed dynamic scheduling strategies for iterative LDPC decoders,” IEEE Trans. Commun., vol.61, no.3, pp.886–896, March 2013.

   - [13] H. Zhang and S. Chen, “Residual-decaying-based informed dynamic scheduling for belief-propagation decoding of LDPC codes,” IEEE Access, vol.7, pp.23656–23666, 2019.

   - [14] T.C.-Y. Chang, P.-H. Wang, J.-J. Weng, I.-H. Lee, and Y.T. Su, “Belief-propagation decoding of LDPC codes with variable node– centric dynamic schedules,” IEEE Trans. Commun., vol.69, no.8, pp.5014–5027, Aug. 2021, doi: 10.1109/TCOMM.2021.3078776.

   - [15] Q. Zhu and L.-N. WU, “Low-complexity check-node-based serial scheduling belief propagation for LDPC codes,” Journal of Signal Processing, vol.29, no.5, pp.550–556, 2013.

   - [16] R. Yuan, T. Xie, and Z. Wang, “A reliability profile based lowcomplexity dynamic schedule LDPC decoding,” IEEE Access, vol.10, pp.3390–3399, 2022.

   - [17] H.-Y. Kwak, J.-S. No, and H. Park, “Design of irregular SC-LDPC codes with non-uniform degree distributions by linear programming,” IEEE Trans. Commun., vol.67, no.4, pp.2632–2646, April 2019, doi: 10.1109/TCOMM.2018.2889850.

- [5] J. Zhang and M. Fossorier, “Shuffled belief propagation decoding,” Conference Record of the Thirty-Sixth Asilomar Conference on Signals, Systems and Computers, 2002, Pacific Grove, CA, USA, vol.1, pp.8–15, 2002, doi: 10.1109/ACSSC.2002.1197141.

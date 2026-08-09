Hindawi Publishing Corporation EURASIP Journal on Wireless Communications and Networking Volume 2009, Article ID 821819, 9 pages doi:10.1155/2009/821819

## _Research Article_ **A Practical Scheme for Frequency Offset Estimation in MIMO-OFDM Systems**

## **Michele Morelli, Marco Moretti, and Giuseppe Imbarlina**

_Dipartimento di Ingegneria dell’Informazione, University of Pisa, Via Caruso 16, 56122 Pisa, Italy_

Correspondence should be addressed to Marco Moretti, marco.moretti@iet.unipi.it

Received 27 June 2008; Revised 3 October 2008; Accepted 25 December 2008

Recommended by Mounir Ghogho

This paper deals with training-assisted carrier frequency offset (CFO) estimation in multiple-input multiple-output (MIMO) orthogonal frequency-division multiplexing (OFDM) systems. The exact maximum likelihood (ML) solution to this problem is computationally demanding as it involves a line search over the CFO uncertainty range. To reduce the system complexity, we divide the CFO into an integer part plus a fractional part and select the pilot subcarriers such that the training sequences have a repetitive structure in the time domain. In this way, the fractional CFO is efficiently computed through a correlation-based approach, while ML methods are employed to estimate the integer CFO. Simulations indicate that the proposed scheme is superior to the existing alternatives in terms of both estimation accuracy and processing load.

Copyright © 2009 Michele Morelli et al. This is an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.

## **1. Introduction**

Orthogonal frequency-division multiplexing (OFDM) is an attractive modulation technique for wideband wireless communications due to its robustness against multipath distortions and flexibility in allocating power and data rate over distinct subchannels. For these reasons, it is adopted in a variety of applications, including digital audio broadcasting (DAB), digital video broadcasting (DVB), and the IEEE 802.11a wireless local area network (WLAN) [1]. Combining OFDM with the multiple-input multiple-output (MIMO) technology is an effective solution to increase the capacity of practical commercial systems. The deployment of multiple antennas at both the transmitter and receiver ends can be exploited to improve reliability by means of space-time coding techniques and/or to increase the data rate through spatial multiplexing [2].

Similar to single-input single-output (SISO) OFDM, MIMO-OFDM is extremely sensitive to carrier frequency offsets (CFOs) induced by Doppler shifts and/or oscillator instabilities. The CFO destroys orthogonality among subcarriers and must be accurately estimated and compensated for to avoid severe error rate degradations [3]. While CFO recovery is a well-studied problem for single antenna systems, only few solutions are available for MIMO-OFDM.

A blind kurtosis-based scheme is presented in [4], while a method for jointly estimating the CFO and MIMO channel is derived in [5] by placing null subcarriers and pilot tones across adjacent OFDM blocks. Unfortunately, these methods are quite complex as they require a large-point discrete Fourier transform (DFT) operation and a computationally demanding line search. Furthermore, they provide the CFO estimate upon observation of several OFDM blocks, and accordingly, are not suited for packet-oriented applications, where synchronization must be completed shortly after the reception of a packet. In order to achieve fast timing and frequency recovery, training sequences with a periodic structure are commonly employed in SISO-OFDM systems [6–8]. Extending this approach to MIMO-OFDM, however, is not straightforward as signals emitted from different antennas give rise to multistream interference (MSI) at the receiver station, which may degrade the accuracy of the synchronization algorithms. The detrimental effect of MSI can be alleviated by a careful design of the MIMO preambles. For instance, in [9], it is shown that the performance of the least-squares (LSs) channel estimator is optimized if the training sequences at different TX branches are orthogonal and shift-orthogonal for at least the channel length. To meet such requirement, a time-orthogonal design is employed in [10], where different TX antennas transmit their preambles

EURASIP Journal on Wireless Communications and Networking

2

over disjoint time intervals. In this way, however, the preamble length grows linearly with the number of TX branches, thereby, increasing the system overhead. The use of chirp-like polyphase sequences is suggested in [11], while a training block composed of repeated PN sequences with good cross-correlation properties is employed in [12]. In both cases, the CFO estimate is obtained by cross-correlating the repetitive parts of the received preambles in a way similar to SISO-OFDM. This approach is also adopted in [13, 14], where the pilot sequences are obtained by repeating Chu or Frank-Zadoff codes with a different cyclic shift applied at each TX antenna. Alternative criteria for MIMO-OFDM preamble design can be found in [15, 16].

A subspace-based method for CFO estimation in MIMOOFDM has recently been proposed in [17]. In this scheme, pilot symbols at different transmit antennas are frequencydivision multiplexed (FDM) and placed over equally spaced subcarriers. The resulting preambles are characterized by an inherent periodic structure in the time domain which can be effectively exploited at the receiver to separate signals arriving from different TX antennas. This approach is reminiscent of the multiple-signal-classification (MUSIC)based frequency recovery scheme employed in [18] in the context of orthogonal frequency division multiple access (OFDMA). The main advantage with respect to [18] is that in [17], the CFO estimate is obtained with reduced complexity by looking for the roots of a real-valued polynomial function. A root-based approach is also adopted in [19] after writing the CFO metric in polynomial form.

In this paper, the repetitive slots-based CFO estimator discussed in [8] is extended to MIMO-OFDM transmissions. In order to enlarge the frequency acquisition range, however, we decompose the CFO into a fractional part plus an integer part. The fractional CFO is computed first by crosscorrelating the repetitive segments of the received preambles in a way similar to [8], while the integer CFO is subsequently estimated by resorting to maximum likelihood (ML) methods. This results into an algorithm of affordable complexity which can estimate large CFOs and whose accuracy attains the relevant Cramer-Rao bound (CRB).

The rest of this paper is organized as follows. Section 2 describes the system model and introduces basic notation. In Section 3, we review the joint ML estimation of the CFO and MIMO channel, while Section 4 is devoted to the training sequences design and CFO recovery scheme. Simulation results are presented in Section 5 and some conclusions are drawn in Section 6.

_Notation 1._ Matrices and vectors are denoted by boldface letters, with **W** _N_ and **I** _N_ being the DFT matrix and identity matrix of order _N_ , respectively. **A** _=_ diag _{a_ ( _n_ ); _n =_ 1, 2, _..._ , _N }_ denotes an _N × N_ diagonal matrix with entries _a_ ( _n_ ) along its main diagonal, while **B** _[−]_[1] is the inverse of a square matrix **B** . We use _E{·}_ , ( _·_ ) _[∗]_ , ( _·_ ) _[T]_ , and ( _·_ ) _[H]_ for expectation, complex conjugation, transposition, and Hermitian transposition, respectively. The notation _∥· ∥_ represents the Euclidean norm of the enclosed vector, while Re _{x}_ , _|x|_ , and arg _{x}_ stand for the real part, modulus, and principal argument of a complex number _x_ . Finally, [ **B** ] _k_ ,l

denotes the ( _k_ , l)th entry of a matrix **B** , while _λ_[�] is a trial value of the unknown parameter _λ_ .

## **2. System Model**

We consider a MIMO-OFDM system with _NT_ transmitting and _NR_ receiving antennas. We denote by _N_ the number of available subcarriers which are enumerated from _n =_ 0 to _n = N −_ 1 and call **c** _i =_ [ _ci_ (0), _ci_ (1), _..._ , _ci_ ( _N −_ 1)] _[T]_ the frequency domain pilot sequence at the _i_ th TX antenna. Before transmission, this sequence is converted in the time domain through an inverse discrete Fourier transform (IDFT) operation and a cyclic prefix (CP) of length _Ng_ is inserted to avoid inter-block interference (IBI). The signal emitted from the _i_ th TX branch arrives at the _m_ th RX antenna after propagating through a multipath channel with discretetime impulse response **h** _m_ , _i =_ [ _hm_ , _i_ (0), _hm_ , _i_ (1), _..._ , _hm_ , _i_ ( _L −_ 1)] _[T]_ , where _L_ is a design parameter that depends on the duration of the transmit/receive filters and on the channel delay spread. Since one single oscillator is used for frequency conversion at both ends of the wireless link, the same CFO is assumed for all transmit/receive antenna pairs. We denote by **x** _m =_ [ _xm_ (0), _xm_ (1), _..._ , _xm_ ( _N −_ 1)] _[T]_ the time domain samples available at the _m_ th RX antenna and define **Γ** ( _ν_ ) _=_ diag _{e[j]_[2] _[π][ν][k/N]_ ; 0 _≤ k ≤ N −_ 1 _}_ , where _ν_ is the frequency offset normalized by the subcarrier spacing. Assuming ideal timing recovery and _Ng ≥ L_ , we have

**==> picture [158 x 9] intentionally omitted <==**

where **n** _m_ is an _N_ -dimensional vector of AWGN samples with zero-mean and variance _σn_[2] , while **s** _m =_ [ _sm_ (0), _sm_ (1), _..._ , _sm_ ( _N −_ 1)] _[T]_ is the useful signal component, which is modeled as

**==> picture [151 x 28] intentionally omitted <==**

**==> picture [241 x 53] intentionally omitted <==**

In Section 3 we show how to exploit vectors _{_ **x** _m_ ; 1 _≤ m ≤ NR}_ for jointly estimating the CFO _ν_ and the MIMO channel **H** _= {_ **h** _m_ , _i_ ; 1 _≤ m ≤ NR_ , 1 _≤ i ≤ NT }_ . In doing so, we adopt the FDM training sequences suggested in [17], which optimize the performance of the LS channel estimator thanks to their shift orthogonality properties [9]. Such sequences are expressed by

**==> picture [227 x 35] intentionally omitted <==**

where _Q_ is a power of two not smaller than _NT_ , _{μi}_ are integer parameters satisfying 0 _≤ μ_ 1 _< μ_ 2 _< · · · < μNT < Q_ , and _di_ ( _n[′]_ ) _}_ are pilot symbols with constant modulus _|di_ ( _n[′]_ ) _| =_ ~~�~~ _Q/NT_ . In this way, the total energy allocated to training amounts to _ET = N_ and is equally split between the TX antennas.

EURASIP Journal on Wireless Communications and Networking

3

## **3. Maximum Likelihood Frequency Estimation**

Given the unknown parameters ( **H** , _ν_ ), from (1), it turns out that vectors _{_ **x** _m}_ are statistically independent and Gaussian distributed with mean **Γ** ( _ν_ ) **s** _m_ and covariance matrix _σn_[2] **I** _N_ . Hence, bearing in mind (2), the log-likelihood function (LLF) for ( **H** , _ν_ ) takes the form

**==> picture [207 x 47] intentionally omitted <==**

As a consequence of the FDM property of the employed training sequences, we observe that **A** _[H] i_ 1 **[A]** _[i]_ 2 _[=]_ **[F]** _[H] L_ **[C]** _[H] i_ 1 **[C]** _[i]_ 2 **[F]** _[L]_[is] the null matrix for any _i_ 1 _=/ i_ 2. Using this fact, after neglecting irrelevant terms independent of **H**[�] and � _ν_ , we may rewrite the LLF as

**==> picture [205 x 64] intentionally omitted <==**

� � where we have borne in mind that **Γ** _[H]_ ( _ν_ ) **Γ** ( _ν_ ) _=_ **I** _N_ . The joint ML estimate of the unknown parameters is the location where Λ1( **H**[�] , � _ν_ ) achieves its global maximum. After standard computations, the CFO estimate is found to be

**==> picture [159 x 16] intentionally omitted <==**

where

**==> picture [174 x 27] intentionally omitted <==**

and **LL** _[H]_ is the following Cholesky decomposition:

**==> picture [173 x 27] intentionally omitted <==**

In the sequel, we refer to (7) as the maximum likelihood frequency estimator (MLFE). The following remarks are in order.

- (1) Observing that **A** _[H] i_ **[A]** _[i][=]_ **[ F]** _[H] L_ **[C]** _[H] i_ **[C]** _[i]_ **[F]** _[L]_[with rank] _[{]_ **[F]** _[L][}][=] L_ and rank _{_ **C** _[H] i_ **[C]** _[i][}] = N/Q_ , it turns out that rank _{_ **A** _[H] i_ **[A]** _[i][} ≤]_[min] _[{][L]_[,] _[ N/Q][}]_[. Since] **[ A]** _[H] i_ **[A]** _[i]_[has dimen-] sions _L × L_ , a necessary condition for the existence of ( **A** _[H] i_ **[A]** _[i]_[)] _[−]_[1][in][the][right-hand-side][of][(][9][)][is][that] _[L][≤] N/Q_ . On the other hand, from (4), it follows that **A** _[H] i_ **[A]** _[i]_[has entries]

**==> picture [226 x 42] intentionally omitted <==**

and reduces to _N ·_ **I** _L_ if _L ≤ N/Q_ . In such a case, the frequency metric simplifies to

**==> picture [187 x 27] intentionally omitted <==**

- (2) By invoking the asymptotic efficiency property of the MLFE, the frequency estimate (7) is expected to be unbiased with an accuracy that approaches the corresponding CRB for large data records and sufficiently high signal-to-noise ratios (SNRs). Using the LLF in (5), it is found that [19]:

**==> picture [193 x 25] intentionally omitted <==**

where **y** _m =_ [ _ym_ (0), _ym_ (1), _..._ , _ym_ ( _N −_ 1)] _[T]_ is an _N_ - dimensional vector with entries

**==> picture [199 x 20] intentionally omitted <==**

## **4. Frequency Estimation with Reduced Complexity**

_4.1. Problem Formulation._ Direct maximization of _g_ (� _ν_ ) in (8) undertakes heavy computational burden. One possible way to reduce the system complexity is indicated in [19], where _g_ (� _ν_ ) is transformed into a real-valued polynomial function, and the CFO estimate is indirectly obtained by means of a polynomial rooting procedure. In this paper, we follow the alternative approach outlined in [8], by which a periodicity is first introduced in the MIMO training sequences, and CFO recovery is then accomplished by measuring the phase rotations between the repetitive parts of the received preambles. For this purpose, the sequences in (4) are modified so as to simultaneously satisfy the following constraints:

- (C1) pilot symbols are equipowered, equispaced in the frequency domain and modulate distinct subcarriers at different TX antennas according to the FDM principle;

- (C2) each vector **W** _[H] N_ **[c]** _[i]_[(] _[i][=]_[1, 2,] _[ ...]_[,] _[ N][T]_[)][of][time][domain] samples is obtained by the repetition of _R_ identical segments, where _R_ is some power of two.

Condition C1 implies that the _NT_ preambles remain shift-orthogonal in the time domain, which is desirable to enhance the accuracy of the channel estimates, while condition C2 facilitates CFO recovery by ensuring that the preambles are periodic with period _P = N/R_ .

To proceed further, let _Q_ be a power of two with _Q ≥ NT_ . Then, it can be easily shown that C1 and C2 are simultaneously met if pilot symbols at each TX antenna are equispaced in the frequency domain at a distance of _M = QR_

EURASIP Journal on Wireless Communications and Networking

4

subcarriers and their positions are shifted by _R_ subcarriers from one TX branch to the next. This amounts to putting

**==> picture [237 x 45] intentionally omitted <==**

where we set _|di_ ( _n[′]_ ) _| =_ � _M/NT_ to ensure that the total energy allocated to training is still _ET = N_ . It is worth observing that the use of time-repetitive FDM training sequences for MIMO-OFDM has also been suggested in [16] to make the CRB of the frequency estimates independent of the channel realization. However, our design (14) is more general as it applies to any triple � _N_ , _NT_ , _L_ ), whereas in [16], the number of subcarriers is constrained to be a multiple of _NT L_ . Recalling that in practical OFDM systems _N_ is always a power of two, it turns out that the sequence design in [16] can only be adopted on condition that both _NT_ and _L_ are powers of two.

As it is known, the use of OFDM preambles composed by _R_ repetitive slots restricts the acquisition range of the CFO estimator to _±R/_ 2 times the subcarrier spacing. To cope with such a drawback, we decompose _ν_ into a _fractional part_ , less than _R/_ 2 in magnitude, plus an _integer part_ which is multiple of _R_ . The normalized CFO is thus rewritten as

**==> picture [147 x 10] intentionally omitted <==**

where _η_ is an integer parameter referred to as the integer CFO (ICFO), while _ε_ is the fractional CFO (FCFO) and belongs to the interval ( _−_ 1 _/_ 2, 1 _/_ 2]. Since the transmitted preambles remain periodic after passing through the channel (apart from the presence of thermal noise and from a phase shift induced by the CFO), each vector of received time domain samples can be decomposed into _R_ segments **x** _m =_ [ **x** _m[T]_ (0), **x** _m[T]_ (1), _..._ , **x** _m[T]_ ( _R −_ 1)] _[T]_ , with

**==> picture [207 x 11] intentionally omitted <==**

In(16), **u** _m_ is a _P_ -dimensional vector with elements

**==> picture [200 x 12] intentionally omitted <==**

while _{_ **n** _m_ ( _r_ ); _r =_ 0, 1, _..._ , _R−_ 1 _}_ are statistically independent Gaussian vectors with zero-mean and covariance matrix _σn_[2] **I** _P_ .

_4.2. Estimation of the Fractional CFO._ Our first goal is the estimation of _ε_ based on the observations _{_ **x** _m}[N] m[R] =_ 1[.] Inspection of (16) reveals that this task is complicated by the presence of the nuisance vectors _{_ **u** _m}_ . One possible approach is to consider such vectors as deterministic but unknown parameters and proceed to the joint ML estimation _T_ of the parameter set ( **u** , _ε_ ), with **u** _=_[�] **u** _[T]_ 1 **[u]** _[T]_ 2 _· · ·_ **u** _[T] NR_ � . This approach has been used in [8] in the context of SISOOFDM, and its extension to MIMO transmissions leads to the following FCFO metric:

**==> picture [187 x 27] intentionally omitted <==**

where _Rm_ ( _r_ ) is the _rP_ —lag sample correlation function evaluated at the _m_ th RX branch, that is,

**==> picture [182 x 27] intentionally omitted <==**

The ML estimate of _ε_ is eventually found by locating the global maximum of _q_ ( _ε_ �). Unfortunately, no closed form solution is available except when _R =_ 2. The more general case can be approached by an exhaustive search over the � interval _ε ∈_ ( _−_ 1 _/_ 2, 1 _/_ 2] which may be cumbersome in practice. For this reason, we suggest a suboptimal but simpler procedure which develops in two steps. In the first step a coarse FCFO estimate is obtained as

**==> picture [241 x 58] intentionally omitted <==**

**==> picture [195 x 13] intentionally omitted <==**

where _Nm_ ( _r_ ) is a zero-mean disturbance term collecting signal _×_ noise and noise _×_ noise interactions. Inspection of (21) reveals that, in the absence of noise, the right-handside of (20) is just the true FCFO. In order to improve the estimation accuracy, _ε_ �[(] _[c]_[)] is refined in the second step by � looking for an estimate of the residual error Δ _ε = ε − ε_[(] _[c]_[)] . For this purpose, we let _R_[(] _m[c]_[)] ( _r_ ) _= Rm_ ( _r_ ) _e[−][j]_[2] _[π][ε]_[�][(] _[c]_[)] _[r]_ and rewrite (18) in the following form:

**==> picture [223 x 27] intentionally omitted <==**

� � � where we have defined Δ _ε = ε − ε_[(] _[c]_[)] and _ϕm_[(] _[c]_[)] ( _r_ ) _=_ arg _{R_[(] _m[c]_[)] ( _r_ ) _}_ . Setting to zero the derivative of (22) with respect to Δ _ε_ � and assuming that Δ _ε_ is small enough such that � � sin[ _ϕm_[(] _[c]_[)] ( _r_ ) _−_ 2 _π_ Δ _εr_ ] _≃ ϕm_[(] _[c]_[)] ( _r_ ) _−_ 2 _π_ Δ _εr_ , an estimate of Δ _ε_ can be computed in closed form as

**==> picture [197 x 28] intentionally omitted <==**

The final FCFO estimate is given by

**==> picture [146 x 11] intentionally omitted <==**

_4.3. Estimation of the Integer CFO._ If the normalized CFO is guaranteed to be less than _R/_ 2 in magnitude, the quantity _εR_ � can be regarded as an estimate of _ν_ . Otherwise, _ν_ is expressed as in (15), and an estimate of the integer offset _η_ must be found. This problem is now addressed using ML methods.

In order to compensate for the fractional offset _ε_ , the received samples at each RX branch are first counter-rotated at an angular speed 2 _πεR/N_ � . This produces the _NR_ vectors **z** _m =_ [ _zm_ (0), _zm_ (1), _..._ , _zm_ ( _N −_ 1)] _[T]_ , with

**==> picture [183 x 11] intentionally omitted <==**

EURASIP Journal on Wireless Communications and Networking

5

Substituting (1)-(2) into (25) and assuming ideal FCFO compensation, we obtain

_n[′] M_ + ( _i −_ 1) _R_ are the indices of the pilot subcarriers at the _i_ th TX antenna. Function _ψ_ ( _η_ �) can thus be rewritten as

**==> picture [432 x 56] intentionally omitted <==**

� where **n** _[′] m =_ **Γ** _[H]_ ( _εR_ ) **n** _m_ is the noise contribution, which is statistically equivalent to **n** _m_ . Vectors _{_ **z** _m}_ are next used to get the joint ML estimate of ( **H** , _η_ ). Bearing in mind (26), the corresponding LLF is found to be

Once the ICFO is obtained as indicated in (31), an estimate of the CFO is computed from (15) in the form

**==> picture [218 x 47] intentionally omitted <==**

**==> picture [147 x 11] intentionally omitted <==**

In the sequel, we refer to (35) as the reduced complexity frequency estimator (RCFE).

by which, maximizing with respect to **h**[�] _m_ , _i_ , we obtain

_4.4. Remarks._ (1) As mentioned previously, matrix **A** _[H] i_ **[A]** _[i]_[in] (28) is nonsingular provided that _L ≤ N/M_ . Such condition is more restrictive than the constraint _L ≤ N/Q_ that was found in the previous section for MLFE. In particular, recalling that _M = QR_ , it turns out that the maximum channel length that RCFE can manage is _R_ times smaller than for MLFE.

**==> picture [188 x 14] intentionally omitted <==**

Now, we observe that **A** _[H] i_ **[A]** _[i][=]_ **[ F]** _[H] L_ **[C]** _[H] i_ **[C]** _[i]_ **[F]** _[L]_[is an] _[ L][ ×][ L]_[ matrix] whose rank is not greater than min _{L_ , _N/M}_ . Hence, a necessary condition for the existence of ( **A** _[H] i_ **[A]** _[i]_[)] _[−]_[1][is][that] _L ≤ N/M_ . In such a case, if the pilot sequences are those defined in (14), we have **A** _[H] i_ **[A]** _[i][=][ N][ ·]_ **[I]** _[L]_[so that (][28][) simplifies] to

(2) Assuming for simplicity that the ICFO has been � perfectly estimated, from (35), it follows that _E{_ ( _ν − ν_ )[2] _} =_ � _R_[2] _· E{_ ( _ε − ε_ )[2] _}_ . Since parameters ( **u** , _ε_ ) are jointly estimated � through ML methods, we expect that _E{_ ( _ε − ε_ )[2] _}_ asymptotically approaches the corresponding CRB. The latter is provided in [8] and reads

**==> picture [174 x 20] intentionally omitted <==**

The concentrated likelihood function for _η_ is found by substituting (29) into the right-hand-side of (27). Neglecting irrelevant terms independent of _η_ �, we obtain

**==> picture [180 x 24] intentionally omitted <==**

where _σs_[2] denotes the average signal power at each RX branch, that is,

**==> picture [185 x 28] intentionally omitted <==**

**==> picture [176 x 28] intentionally omitted <==**

and the ML estimate of _η_ is computed as

**==> picture [167 x 18] intentionally omitted <==**

The frequency MSE is thus given by

**==> picture [192 x 24] intentionally omitted <==**

where _|η|_ max represents the largest expected value of _|η|_ , which is determined by the stability of the transmitter and receiver oscillators. Recalling that **A** _i =_ **W** _[H] N_ **[C]** _[i]_ **[F]** _[L]_[,][after] standard manipulations, we may put _ψ_ ( _η_ �) in the equivalent form

(3) The computational load of RCFE can be assessed as follows. Computing the correlations _{Rm_ ( _r_ ) _}[R] r=[−]_ 1[1][in][(][19][)] requires a total of 2( _R−_ 1)(2 _N −_ 1) real operations (additions plus multiplications) for each RX branch, while 8 _NR_ ( _R −_ 1) operations are needed to obtain Δ _ε_ � in (23). Quantities _Zm_ ( _n_ ) in (33) are computed through an _N_ -point DFT for each receiving antenna, with a corresponding complexity of 5 _NRN_ log2 _N_ . Finally, evaluating _ψ_ ( _η_ �) in (34) needs additional 8 _NLNT NR/M_ operations for each _η_ �. The overall complexity of RCFE is summarized in the first row of Table 1, where a distinction has been made between the FCFO and ICFO recovery tasks, and we have denoted by _Nη =_ 2 _|η|_ max + 1 the number of hypothesized ICFO values.

**==> picture [230 x 30] intentionally omitted <==**

where _{Zm_ ( _n_ ) _}_ is the repetition with period _N_ of the DFT of **z** _m_ , that is,

**==> picture [228 x 28] intentionally omitted <==**

On the other hand, from (14), we see that symbols _ci_ ( _n_ ) are different from zero only when _n = pi_ ( _n[′]_ ), where _pi_ ( _n[′]_ ) _=_

(4) Our FCFO recovery algorithm is an improved version of the correlation-based frequency estimator (CBFE)

EURASIP Journal on Wireless Communications and Networking

6

Table 1: Complexity of FCFO and ICFO estimation schemes.

||FCFO recovery|ICFO recovery|
|---|---|---|
|RCFE|2_NR_(_R −_1)(2_N_+ 3)|_NRN_(5 log2_N_+ 8_LNTNη/M_)|
|PBFE|4_NRNQ_+ 30(_Q −_1)3|_NRN_(5 log2_N_+ 4_NT_)|
|CBFE|4_NR_(3_N −_2_P −_1)||



proposed in [12]. Actually, both schemes employ training preambles composed by _R_ repetitive parts and operate in two � steps. A coarse estimate _ε_[(] _[c]_[)] is firstly computed by CBFE in a way similar to (20), and it is next refined by evaluating the quantity

**==> picture [180 x 27] intentionally omitted <==**

� � � The final CFO estimate is obtained as _ν_ CBFE _= R_ ( _ε_[(] _[c]_[)] + Δ _ε_ ), and its MSE is given by [12]

**==> picture [179 x 23] intentionally omitted <==**

Comparing this results with (38), we see that the loss (in dB) with respect to RCFE is 10 _·_ Log[4(1 _−_ 1 _/R_[2] ) _/_ 3], which approaches 1.25 dB for large values of _R_ . Furthermore, since no ICFO estimation is attempted in [12], the estimation range of CBFE is restricted to _|ν| ≤ R/_ 2, while RCFE can cope with CFOs as large as _±N/_ 2. The overall complexity of CBFE is shown in the third line of Table 1. Compared to FCFO recovery by means of RCFE, the computational saving of CBFE is in the order of _R/_ 3.

## **5. Simulation Results**

Computer simulations have been run to check and extend the analytical results of the previous sections. The simulation scenario is summarized as follows.

_5.1. Simulation Model._ The investigated MIMO-OFDM system has _N =_ 1024 subcarriers and operates in the 5 GHz frequency band. The signal bandwidth is 5 MHz, corresponding to a subcarrier distance of approximately 4 _._ 9 kHz. The sampling period is _Ts =_ 0 _._ 2 microsecond, so that the useful part of each OFDM block has length 0 _._ 205 millisecond. Each channel is characterized by _L =_ 12 independent Rayleigh fading taps with an exponentially decaying power delay profile

**==> picture [231 x 32] intentionally omitted <==**

In (41), the constant _σh_[2][is][chosen][such][that][the][channel] power is normalized to unity, that is, _E{∥_ **h** _m_ , _i∥_[2] _} =_ 1. A new channel snapshot is generated at each simulation run and kept fixed over the training period. Vectors **h** _m_ , _i_ are assumed to be statistically independent for different TX/RX antenna

**==> picture [231 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [−] [4]<br>NT =  3,  NR =  2<br>EMCB<br>10 [−] [5]<br>10 [−] [6]<br>0 3 6 9 12 15 18<br>SNR (dB)<br>RCFE<br>PBFE<br>CBFE<br>MSE<br>**----- End of picture text -----**<br>


Figure 1: MSE of the FCFO estimators versus SNR with _NT_ = 3 and _NR_ = 2.

pairs . The training sequences employed by RCFE are given in (14), where we have set _R =_ 8 and _Q =_ 4. In this way, each TX antenna transmits a total of 32 pilot symbols which are randomly taken from a QPSK constellation with power _|di_ ( _n[′]_ ) _|_[2] _=_ 32 _/NT_ . Parameters _NT_ and _NR_ are varied throughout simulations to assess their impact on the system performance.

Comparisons are made between RCFE, CBFE, and the polynomial-based frequency estimator (PBFE) proposed in [17]. This scheme employs the training sequences defined in (4) and performs initial ICFO recovery by maximizing the following cost function:

**==> picture [218 x 28] intentionally omitted <==**

� over the set _η ∈ {−Q/_ 2, _−Q/_ 2 + 1, _..._ , _Q/_ 2 _−_ 1 _}_ , with _{Xm_ ( _n_ ); 0 _≤ n ≤ N −_ 1 _}_ being the _N_ -point DFT of **x** _m_ . After ICFO compensation, the fractional CFO is eventually estimated by looking for the roots of a real-valued polynomial function that is obtained by applying the MUSIC principle. As mentioned in [17], the estimation range of PBFE is _|ν| ≤ Q/_ 2. Its computational requirement is mainly ascribed to the need for evaluating the correlation matrix of the received time domain samples and is summarized in the second row of Table 1.

_5.2. Performance Assessment._ Figure 1 compares the performance of the fractional CFO estimators in terms of their � MSE _E{_ ( _ν − ν_ )[2] _}_ versus the signal-to-noise ratio at each receiving antenna. The latter is defined as SNR _= σs_[2] _/σn_[2] , where _σn_[2] is the noise power, and _σs_[2] is given in (37). Marks indicate simulation results, while solid lines are drawn to

EURASIP Journal on Wireless Communications and Networking

7

**==> picture [231 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [−] [4]<br>RCFE<br>NR =  2<br>EMCB<br>10 [−] [5]<br>10 [−] [6]<br>0 3 6 9 12 15 18<br>SNR (dB)<br>NT =  2<br>NT =  3<br>NT =  4<br>MSE<br>**----- End of picture text -----**<br>


Figure 2: Accuracy of RCFE versus SNR with _NT=_ 2,3,4 and _NR=_ 2.

ease the reading of the graphs. The number of TX and RX antennas is _NT =_ 3 and _NR =_ 2, respectively. The same training sequences are used for both CBFE and RCFE, while PBFE employs the pilot design specified in (4) with _Q =_ 32 and _{μ_ 1, _μ_ 2, _μ_ 3 _} = {_ 0, 1, 5 _}_ . This means that the number of pilot symbols transmitted by each TX antenna is 32 for all the considered schemes. As suggested in [17], the pilot symbols _{di_ ( _n[′]_ ) _}_ for PBFE belong to a Chu sequence. The CFO is randomly generated at each simulation run with uniform distribution within the interval [ _−_ 0, 4; 0 _._ 4), which corresponds to having _η =_ 0 and _ε = ν/R_ . For the time being, we concentrate on the accuracy of the FCFO estimates and assume ideal ICFO recovery for both RCFE and PBFE. We use the average CRB to benchmark the performance of the considered schemes. The latter corresponds to the extended Miller and Chang bound (EMCB) [20] and is obtained by numerically averaging the right-hand-side of (12) with respect to the channel statistics. Inspection of Figure 1 reveals that RCFE outperforms the other schemes, and its accuracy is close to the EMCB at all investigated SNR values. As predicted by the theoretical analysis shown in (38) and (40), the loss of CBFE with respect to RCFE is approximately 1.25 dB. Looking at the system complexity, from Table 1, it turns out that in the considered scenario, RCFE requires a total of 57 500 operations for FCFO recovery, while PBFE and CBFE need 1 156 000 and 24 000 operations, respectively. Combining these figures with the results of Figure 1 indicates that RCFE is superior to PBFE in terms of both estimation accuracy and processing load, while CBFE is a valid solution when limiting the computational requirement is an issue of concern.

Figure 2 illustrates the impact of the number of transmit antennas _NT_ on the accuracy of RCFE. The simulation

**==> picture [231 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [−] [4]<br>RCFE<br>NT =  3<br>10 [−] [5]<br>EMCB<br>10 [−] [6]<br>0 3 6 9 12 15 18<br>SNR (dB)<br>NR =  2<br>NR =  3<br>NR =  4<br>MSE<br>**----- End of picture text -----**<br>


Figure 3: Accuracy of RCFE versus SNR with _NT=_ 3 and _NR=_ 2,3,4.

scenario is the same as in Figure 1, except that now _NT =_ 2, 3 or 4. As it is seen, the frequency MSE is virtually independent of _NT_ and the same occurs for the EMCB. Such behavior can be ascribed to the fact that signals emitted by different TX antennas combine incoherently at each RX branch, so that higher values of _NT_ do not result into a corresponding increase of the array gain. As it is known, array gain exploitation by means of multiple TX antennas requires channel knowledge at the transmitter in conjunction with suitable precoding techniques.

Figure 3 shows how the performance of RCFE is affected by the number _NR_ of receiving antennas. In such a case, _NT_ is fixed to three while _NR =_ 2, 3 or 4. As predicted by (38), the estimation accuracy improves with _NR_ , and this trend is also evident in the EMCB. The physical reason behind such SNR advantage is that the presence of multiple receiving antennas increases the length of the data record **x** _=_ [ **x** 1 _[T]_[,] **[ x]** 2 _[T]_[,] _[ ...]_[,] **[ x]** _N[T] R_[]] _[T]_ used for CFO recovery. This provides the system with an array gain of 10 _·_ Log( _NR_ ) dB.

The performance of the ICFO estimators is illustrated in � Figure 4 in terms of probability of failure _P f =_ Pr _{η =/ η}_ versus SNR. Comparisons are made between RCFE and PBFE using the same simulation setup of Figure 1. The RCFE � metric defined in (34) is evaluated for _η ∈{−_ 2, _−_ 1, 0, 1, 2 _}_ , while PBFE looks for the maximum of _ψ_ PBFE( _η_ �) over the set � _η ∈{−_ 16, _−_ 15, _..._ , 15 _}_ . In this way, the estimation range is _|ν| ≤_ 20 for RCFE and _|ν| ≤_ 16 for PBFE. As it is seen, for SNR _> −_ 10 dB, the best performance is obtained with RCFE. From Table 1, it follows that the total number of operations needed to get the CFO estimate � _ν_ is 1 283 000 for PBFE and 252 500 for RCFE, thereby leading to a reduction of the processing load by a factor greater than 5. It is fair to say, however, that the complexity of PBFE can be controlled by

EURASIP Journal on Wireless Communications and Networking

8

**==> picture [230 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 [0]<br>NT =  3,  NR =  2<br>10 [−] [1]<br>10 [−] [2]<br>10 [−] [3]<br>10 [−] [4]<br>− 18 − 15 − 12 − 9 − 6<br>SNR (dB)<br>RCFE<br>PBFE<br>P f<br>**----- End of picture text -----**<br>


Figure 4: Probability of failure versus SNR for RCFE and PBFE with _NT_ = 3 and _NR_ = 2.

a judicious design of parameter _Q_ . Specifically, decreasing _Q_ alleviates the computational requirement at the expense of a reduced CFO acquisition range.

## **6. Conclusions**

We have addressed the problem of training-assisted CFO recovery in MIMO-OFDM systems. To reduce the computational burden required by the exact ML solution, we have divided the CFO into a fractional part plus an integer part and have designed FDM pilot sequences that are periodic in the time domain. The fractional CFO is estimated in closed form by measuring the phase rotations between the repetitive parts of the received preambles, while the integer CFO is estimated in a joint fashion with the MIMO channel matrix by resorting to the ML principle. The proposed scheme has affordable complexity and exhibits improved performance with respect to existing alternatives. For these reasons, we believe that it provides an effective approach for frequency synchronization in beyond third generation (3G) wideband MIMO-OFDM transmissions.

## **References**

- [1] “Wireless LAN medium access control (MAC) and physical layer (PHY) specifications, higher speed physical layer extension in the 5 GHz band,” 1999.

- [2] G. L. St¨uber, J. R. Barry, S. W. Mclaughlin, Y. E. Li, M. A. Ingram, and T. G. Pratt, “Broadband MIMO-OFDM wireless communications,” _Proceedings of the IEEE_ , vol. 92, no. 2, pp. 271–294, 2004.

- [3] T. Pollet, M. van Bladel, and M. Moeneclaey, “BER sensitivity of OFDM systems to carrier frequency offset and Wiener phase noise,” _IEEE Transactions on Communications_ , vol. 43, no. 234, pp. 191–193, 1995.

- [4] Y. Yao and G. B. Giannakis, “Blind carrier frequency offset estimation in SISO, MIMO, and multiuser OFDM systems,” _IEEE Transactions on Communications_ , vol. 53, no. 1, pp. 173– 183, 2005.

- [5] X. Ma, M.-K. Oh, G. B. Giannakis, and D.-J. Park, “Hopping pilots for estimation of frequency-offset and multiantenna channels in MIMO-OFDM,” _IEEE Transactions on Communications_ , vol. 53, no. 1, pp. 162–172, 2005.

- [6] T. M. Schmidl and D. C. Cox, “Robust frequency and timing synchronization for OFDM,” _IEEE Transactions on Communications_ , vol. 45, no. 12, pp. 1613–1621, 1997.

- [7] M. Morelli and U. Mengali, “An improved frequency offset estimator for OFDM applications,” _IEEE Communications Letters_ , vol. 3, no. 3, pp. 75–77, 1999.

- [8] M. Ghogho, A. Swami, and P. Ciblat, “Training design for CFO estimation in OFDM over correlated multipath fading channels,” in _Proceedings of the 50th Annual IEEE Global Telecommunications Conference (GLOBECOM ’07)_ , pp. 2821– 2825, Washington, DC, USA, November 2007.

- [9] I. Barhumi, G. Leus, and M. Moonen, “Optimal training sequences for channel estimation in MIMO OFDM systems in mobile wireless channels,” in _Proceedings of the International Zurich Seminar on Broadband Communications: Accessing, Transmission, Networking_ , pp. 441–446, Zurich, Switzerland, February 2002.

- [10] A. van Zelst and T. C. Schenk, “Implementation of a MIMO OFDM-based wireless LAN system,” _IEEE Transactions on Signal Processing_ , vol. 52, no. 2, pp. 483–494, 2004.

- [11] A. N. Mody and G. L. St¨uber, “Synchronization for MIMO OFDM systems,” in _Proceedings of IEEE Global Telecommunicatins Conference (GLOBECOM ’01)_ , vol. 1, pp. 509–513, San Antonio, Tex, USA, November 2001.

- [12] C. Yan, S. Li, Y. Tang, and X. Luo, “Frequency synchronization in MIMO OFDM system,” in _Proceedings of the 60th IEEE Vehicular Technology Conference (VTC ’04)_ , vol. 3, pp. 1732– 1734, Los Angeles, Calif, USA, September 2004.

- [13] T. C. W. Schenk and A. van Zelst, “Frequency synchronization for MIMO OFDM wireless LAN systems,” in _Proceedings of the 58th IEEE Vehicular Technology Conference (VTC ’03)_ , vol. 2, pp. 781–785, Orlando, Fla, USA, October 2003.

- [14] J. Zheng, J. Han, J. Lv, and W. Wu, “A novel timing and frequency synchronization scheme for MIMO OFDM system,” in _Proceedings of the International Conference on Wireless Communications, Networking and Mobile Computing (WiCOM ’07)_ , pp. 420–423, Shanghai, China, September 2007.

- [15] H. Minn, N. Al-Dhahir, and Y. Li, “Optimal training signals for MIMO OFDM channel estimation in the presence of frequency offset and phase noise,” _IEEE Transactions on Communications_ , vol. 54, no. 10, pp. 1754–1759, 2006.

- [16] M. Ghogho and A. Swami, “Training design for multipath channel and frequency-offset estimation in MIMO systems,” _IEEE Transactions on Signal Processing_ , vol. 54, no. 10, pp. 3957–3965, 2006.

- [17] Y. Jiang, H. Minn, X. Gao, X. You, and Y. Li, “Frequency offset estimation and training sequence design for MIMO OFDM,” _IEEE Transactions on Wireless Communications_ , vol. 7, no. 4, pp. 1244–1254, 2008.

- [18] Z. Cao, U. Tureli, and Y.-D. Yao, “Deterministic multiuser carrier-frequency offset estimation for interleaved OFDMA uplink,” _IEEE Transactions on Communications_ , vol. 52, no. 9, pp. 1585–1594, 2004.

EURASIP Journal on Wireless Communications and Networking

9

- [19] Y. Jiang, X. You, X. Gao, and H. Minn, “MIMO OFDM frequency offset estimator with low computational complexity,” in _Proceedings of IEEE International Conference on Communications (ICC ’07)_ , pp. 5449–5454, Glasgow, Scotland, June 2007.

- [20] F. Gini and R. Reggiannini, “On the use of Cramer-Rao-like bounds in the presence of random nuisance parameters,” _IEEE Transactions on Communications_ , vol. 48, no. 12, pp. 2120– 2126, 2000.

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

997 

## The Multimodulus Blind Equalization and Its Generalized Algorithms 

Jian Yang _, Member, IEEE_ , Jean-Jacques Werner _, Fellow, IEEE_ , and Guy A. Dumont _, Fellow, IEEE_ 

_**Abstract—**_ **This paper presents a new blind equalization algorithm called multimodulus algorithm (MMA). This algorithm combines the benefits of the well-known reduced constellation algorithm (RCA) and constant modulus algorithm (CMA). In addition, MMA provides more flexibility than RCA and CMA, and is better suited to take advantage of the symbol statistics of certain types of signal constellations, such as nonsquare constellations, very dense constellations, and some wrong solutions.** 

_**Index Terms—**_ **Adaptive equalizer, blind equalization, carrierless amplitude and phase modulation, least mean square methods, quadrature amplitude modulation.** 

## I. INTRODUCTION 

HE CONCEPT of blind equalization has been known **T** since the publication of Sato’s original work on this subject, in 1975 [1]. Sato’s algorithm was subsequently generalized, and other types of blind equalization algorithms were proposed and analyzed [2]–[11]. In spite of all these early contributions of significance, until recently, blind equalization had only found limited applications. The renewed interest in this topic has been triggered by applications such as asynchronous transfer mode (ATM) local area network (LAN) and broadband access on copper in fiber-to-the-curb (FTTC) and very high-rate digital subscriber line (VDSL) networks, for which blind equalization provides major benefits [12]–[14]. 

We now briefly discuss one of these applications. The point-to-multipoint arrangement shown in Fig. 1 is used in FTTC networks, which provide broadband access to the home using standard unshielded twisted pair (UTP) telephone wiring in the network and coaxial cable, or UTP wiring in the home. Details on the characteristics of the communication link between the optical network unit (ONU) in the cable plant and the various set-top boxes and personal computers (PCs) in the home are given in [14] and will not be repeated here. The downstream channel, from the ONU to the home, uses a 51.84 Mb/s 16-carrierless amplitude and phase modulation (CAP) signal, which is broadcast to the various termination points inside the home. The upstream channel, from the home to the ONU, uses a 1.62 Mb/s quadrature phase-shift keying (QPSK) burst modem. Our interest here is in downstream 

Manuscript received March 30, 2001; revised December 17, 2001. The work of J. Yang and J.-J. Werner was supported by Bell Laboratories. This paper was presented in part at DSP97, Santorini, Greece, 1997. 

J. Yang is with Bell Laboratories, Holmdel, NJ 07733 USA (e-mail: yangj@lucent.com). 

J.-J. Werner (deceased) was with Bell Laboratories, Holmdel, NJ 07733 USA. 

G. A. Dumont is with the University of British Columbia, Vancouver, BC V6T 1Z4, Canada (e-mail: guyd@ppc.ubc.ca). Publisher Item Identifier S 0733-8716(02)05381-7. 

transmission. A simplified diagram showing the signal flow in the downstream direction is shown on the bottom right in the figure. Assume now, for example, that the two set-top boxes are operational and that the PC is suddenly turned on. The 16-CAP receiver in the PC needs to be trained before it can deliver valid data. Conceptually, this can be done in a variety of ways. 

- 1) The transmitter in the ONU could interrupt its transmission of data to the set-top boxes for some time interval and transmit instead a known training sequence for the receiver in the PC. Such an interruption of data transmission to the set-top boxes is obviously not desirable. 

- 2) The transmitter in the ONU could send a periodic training sequence, as is done in some broadcast applications, such as high definition television (HDTV). However, the overhead incurred with such an approach cannot be justified for the FTTC application considered here because of the small number of termination points in the home. 

- 3) The best solution is to blindly train the receiver that is being turned on. That is, the receiver is trained without the help of a known training sequence and uses instead the (unknown) sequence of data that is being sent to the other termination points in the home. 

The most complex and time-consuming task during blind startup of a receiver is the convergence of the equalizer, which is done with a blind tap updating algorithm. The two best known blind equalization algorithms for two-dimensional modulation schemes, such as quadrature amplitude modulation (QAM) and CAP, are the reduced constellation algorithm (RCA) and the constant modulus algorithm (CMA). RCA is very simple to implement, but does not provide reliable initial convergence. CMA provides reliable convergence, but increases the complexity of implementation of the receiver in steady-state operation because of the need to add a rotator at the output of the equalizer. 

The multimodulus algorithm (MMA) presented here combines the benefits of RCA and CMA. It provides reliable initial convergence and does not need the addition of a rotator in steady-state operation. The latter property seems to have been discovered independently in [15] and [16], [17]. In addition, MMA provides much more flexibility than RCA and CMA and is better suited to take advantage of the symbol statistics of certain types of signal constellations, such as nonsquare and very dense constellations [16]–[18]. RCA and CMA are not very effective in handling these types of signal constellations. MMA also suitable for CAP–QAM dual mode reception [19]. 

The rest of the material is organized as follows. A brief review of CAP transceivers and equalizer structures is provided in the next section. Various commonly used cost functions 

0733-8716/02$17.00 © 2002 IEEE 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

998 

**==> picture [367 x 210] intentionally omitted <==**

Fig. 1. Broadband access on copper in FTTC networks. 

and tap updating algorithms are discussed in Section III. In Section IV, we introduce the basic MMA algorithm for square signal constellations, and show how it can be modified to accommodate nonsquare constellations. Section V presents a generalized MMA (GMMA) algorithm, which is well suited to very dense signal constellations. The combined CMA–MMA and dual-mode CAP–QAM receiver will be presented in Sections VI and VII separately. The issue of convergence to wrong solutions during blind startup is discussed in Section VIII. Then experimental results obtained in the laboratory with a 51.84 Mb/s 16-CAP and other DSP setup are presented in Section IX. Finally, we summarize paper in Section X. 

## II. CARRIERLESS AM/PM MODULATION TRANSCEIVER 

## _A. Transceiver Structure_ 

CAP is a bandwidth-efficient two-dimensional passband transmission scheme, which is closely related to the more familiar QAM transmission scheme. The block diagram of a digital CAP transmitter is shown on the top of Fig. 2. The bit stream to be transmitted is first passed through a scrambler (not shown in the figure). The scrambled bits are then fed to an encoder, which maps blocks of bits into one of different complex symbols . A CAP line code that uses different complex symbols is called a -CAP line code. The two-dimensional display of the discrete values assumed by the symbols and is called a signal constellation. Examples of 16-CAP and 32-CAP signal constellations are shown in Fig. 3. After the encoder, the symbols and are fed to digital shaping filters. The outputs of the filter are subtracted and the result is passed through a digital-to-analog (D/A) converter, which is followed by an interpolating low-pass filter (LPF). The digital shaping filters and the D/A operate at a sampling rate where is a suitably chosen integer and is the symbol rate. 

**==> picture [252 x 205] intentionally omitted <==**

Fig. 2. A communication link using a CAP transceiver. (a) Transmitter structure. (b) Receiver structure. 

The signal at the output of the CAP transmitter in Fig. 2 can be written as 

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [7 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [4 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 4] intentionally omitted <==**

where is the symbol period, and are discrete multilevel symbols, which are sent in symbol period , and and are the impulse responses of in-phase and quadrature passband shaping filters, respectively, and form a Hilbert pair. Details on the design of the shaping filters can be found in [17]. 

The structure of a digital CAP receiver is shown on the bottom of Fig. 2. It consists of an analog-to-digital (A/D) converter followed by an adaptive equalizer. Examples of adaptive equalizer structures are given in the next section. The A/D operates at a sampling rate , which is typically the same as the 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

999 

**==> picture [247 x 128] intentionally omitted <==**

**==> picture [145 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) (b)<br>**----- End of picture text -----**<br>


Fig. 3. (a) 16-point signal constellation. (b) 32-point signal constellation. 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

vector of quadrature phase tap coefficients (2.5) 

where the superscript denotes vector transpose, and the subscript is a short notation for the symbol period . With , we have . The outputs and of the digital filters can then be written as (2.6) 

If we define the following complex equalizer output and complex tap vector : 

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

We can rewrite (2.6) in the more compact complex form 

sampling rate used for the D/A at the transmitter. The two outputs of the adaptive equalizers are sampled at the symbol rate and, in steady-state operation, the results are fed to a decision device followed by a decoder, which maps the symbols into bits. Let be the impulse response of the channel and let be some noise added to the CAP signal in the channel. The signal at the input of the CAP receiver can then be written as 

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

where denotes convolution, and and . It should be pointed out that and still form a Hilbert pair. Thus, the distortion introduced by the channel does not affect the generic form of the expression for a CAP signal that is given in (2.1). 

## _B. Adaptive Equalizer Structures_ 

A great variety of adaptive equalizer structures can be used for CAP signals. For example, all the types of equalizers that are used for QAM can be used for CAP as well. The difference between CAP and QAM is the way to implement. QAM requires a modulator/demodulator which is explicitly used in CAP within the passband shaping filters. CAP does not require the phase-recovery circuit that is usually used at the output of the equalizer in a QAM receiver. In this paper, we will only consider linear adaptive equalizers. Blind convergence of decision-feedback equalizers will be discussed in a forthcoming paper. 

A fractionally spaced linear equalizer (FSLE) that is particularly well suited to the applications considered here is the phase-splitting equalizer shown in Fig. 4 [20]. It consists of a parallel arrangement of two adaptive digital filters, which take their inputs directly from the A/D at the sampling rate and are implemented as finite-impulse-response (FIR) filters. In the steady-state mode of operation, the two outputs of the filters are sampled at the symbol rate , and are then fed to a decision device (slicer). Normally, is held. 

We now make the following definitions with respect to Fig. 4: 

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [209 x 9] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

vector of in-phase tap coefficients (2.4) 

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

## III. COST FUNCTIONS AND TAP UPDATING ALGORITHMS 

In most practical applications, the tap coefficients of an adaptive equalizer are adjusted by using a stochastic gradient algorithm, i.e., the complex tap vector is updated according to 

**==> picture [9 x 9] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [9 x 9] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where is a small number called step size and is the gradient of some cost function ( ) with respect to the tap vector . The subscript refers to the th tap updating iteration. For a convex cost function, the tap updating algorithm has converged when the gradient is zero, that is 

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Two main types of cost functions are used in practice. In one case, they are functions of the symbols used in the signal constellation, and in the other case they are functions of statistics of the symbols . These two cases are discussed in the next two sections. In the last section, we show how some of these algorithms can be used in a blind startup. 

## _A. Tap Updating Algorithms Based on Symbol Values_ 

Many modems use a known training sequence during initial startup, so that the receiver knows _a priori_ what sequence of complex symbols is sent by the transmitter. The adaptive equalizer can then be converged with a so-called ideal reference. In this case, the cost function that is usually used is the mean squared error (MSE) defined as 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [11 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

where is the complex output of the equalizers and denotes expectation. The tap updating algorithm in (3.1) then becomes the least-mean-square (LMS) algorithm. Practical implementations usually use the unaveraged gradient, so that the LMS algorithm for the two equalizers in Fig. 4 can be written as 

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where , and is the complex error in symbol period , as shown in Fig. 5. Let be the complex noise sample at the output of the equalizer after convergence, so that and . 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1000 

**==> picture [393 x 114] intentionally omitted <==**

Fig. 4. Structure of phase-splitting FSLE with decision devices. 

**==> picture [205 x 200] intentionally omitted <==**

Fig. 5. Error used for various types of tap updating algorithms. 

Thus, after convergence of the equalizer, the MSE in (3.3) is simply equal to the variance of the noise . Note that the above equalizer convergence is applied for a linear channel with required whiteness of source data. In addition, due to the limitation of some factors such as FIR filter length and adaptation parameters, the convergence of an adaptive equalizer always exists certain amount of excess mean square error and some misadjustment. 

In the steady-state mode of operation, the slicers in Fig. 4 make the right decisions most of the time by selecting the symbol which is the closest in Euclidean distance to the received sample . In this case, the known symbols can be replaced with the estimated (or sliced) symbols . The cost function that is then minimized is given by 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [11 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

and the tap updating algorithms are the same as in (3.4) except that replaces , as shown in Fig. 5. When these algorithms are used, the equalizer is said to be adapted in the decision-directed mode [21]. With this algorithm, the MSE reduces again to the variance of the noise at the output of the equalizer in the steady-state mode of operation. 

The MSE in (3.3) and (3.5) uses second-order statistics of the equalizer’s output samples. It can be shown that the use of second-order statistics only is generally not sufficient for the blind deconvolution of nonminimum-phase channels [22], [23]. 

For this reason, most blind equalization algorithms have cost functions which use cyclostationary second or higher order statistics (HOS) of the signals. However, the second-order cyclostationarity is extensively used in blind equalization just because of the convergence problems and larger variance associated with HOS. 

## _B. Tap Updating Algorithms Based on Symbol Statistics_ 

During initial convergence of an adaptive equalizer, it usually is not possible to use a decision-directed tap updating algorithm, because the slicers make too many errors. If no training sequence is available, then the equalizer has to be converged under so-called “blind” conditions. In this case, the cost function that is minimized does not depend on known or estimated symbols and , but on known statistics of the symbols . 

The simplest blind tap updating algorithm is the so-called _reduced constellation algorithm_ (RCA). The cost function minimized by RCA is the MSE with respect to a reduced number of symbol values, which usually are not a subset of the symbol values used in the signal constellation. When four symbol values are used, the cost function for RCA can be written as 

**==> picture [5 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

where is the complex signum function, and the constant is a function of the statistics of the symbols in the signal constellation. Closed-form expressions for are given in Appendix A. The quantity minimized by the RCA cost function is shown in Figs. 5 and 6(a). The tap updating algorithm for the equalizers in Fig. 4 is given by 

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Another well-known blind equalization algorithm is the _constant modulus algorithm_ (CMA), which minimizes the dispersion of the equalizer’s output samples around a circle, as shown in Fig. 6(b). The cost function for CMA is given by 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

Notice that this cost function uses fourth-order statistics of the signals. The corresponding tap updating algorithm for the two equalizers in Fig. 4 is given by 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Expressions relating the constant to the statistics of the symbols are given in Appendix A. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1001 

**==> picture [426 x 144] intentionally omitted <==**

**==> picture [363 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) (b) (c)<br>**----- End of picture text -----**<br>


Fig. 6. Principles of (a) RCA, (b) CMA, and (c) MMA. 

It is shown in [24] that the CMA cost functions in (3.8) is minimized when the channel is perfectly equalized (and noiseless) and the kurtosis of the complex symbols is negative, that is 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [15 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [10 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [25 x 10] intentionally omitted <==**

The condition on the right is satisfied for all signal constellations of practical interest. It should be pointed out that, even in the absence of noise, the minimum of the cost function is generally not equal to zero, except for 4-CAP. Closed-form expressions for the minimum values of the RCA, CMA, and MMA cost functions are derived in Appendix B. 

Both RCA and CMA are used in practice. However, these two blind equalization algorithms do not fully take advantage of the statistics of the set of symbols used in certain signal constellations, such as nonsquare and very dense constellations. The MMA algorithm described in the following sections is much more flexible in this regard. In addition, it is quite efficient in reducing occurrence of wrong solutions. This issue is discussed in detail in Section VIII. 

## _C. Blind Startup_ 

We now briefly discuss how the various tap updating algorithms can be incorporated in a typical blind startup of a receiver. Illustration of the procedure will be given in Section IX when we discuss experimental results. A typical blind startup of a receiver consists of the following three main sequential steps. 

- 1) Adjust the automatic gain control (AGC) and acquire timing (synchronize the receiver’s clock to the clock of the far-end transmitter). 

- 2) Adapt the tap coefficients of the equalizer with a blind equalization algorithm until the “eye” of the signal constellation is open. 

- 3) Switch to a decision-directed tap updating algorithm when the eye is open. 

The eye of the signal constellation is considered to be open when the slicer makes the right decisions “most of the time” or, equivalently, when the MSE measured across the slicer is small enough. A probability of symbol error of 10 is usually considered acceptable to guarantee a safe switch between the blind equalization and decision-directed tap updating algorithms. In real-time DSP prototype, when the measure of MSE or symbol 

error is not suitable, we observe experimentally and manually switch the equalizer from blind startup to LMS algorithm. 

**==> picture [70 x 8] intentionally omitted <==**

In this section, we discuss the simplest version of the MMA and its application to small and medium-sized ( ) square and nonsquare signal constellations. The generalization of the algorithm to dense constellations and other applications are presented in the next three sections. 

## _A. Square Constellations_ 

We first consider square constellations. The cost function minimized by MMA is then given by 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where is a positive integer. In practice, a value usually provides the best compromise between performance and complexity of implementation. This cost function is similar to the cost function for CMA in (3.8), except that the term is missing. As a result, the MMA cost function is not a truly two-dimensional cost function. It can be considered as the sum of two one-dimensional cost functions, which minimize the dispersion of the output samples and of the equalizer around separate straight contours (or moduli), as shown in Fig. 6(c). This should be more obvious if we rewrite (4.1) as 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where is the cost function for the in-phase samples and is the cost function for the quadrature samples . It is shown in Appendix C that a condition similar to (3.10) applies to the minimum of the MMA cost function, except that the condition applies independently to the real and imaginary symbols. For the symbols we have 

and (4.3) We now consider the phase-splitting equalizer in Fig. 4. Taking the gradient of and with respect to the tap vectors and , respectively, we get 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1002 

**==> picture [248 x 142] intentionally omitted <==**

Fig. 7. MMA moduli for 128-point signal constellation. 

The derivation of the expression for the constant is provided in Appendix A, where it is shown that 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

The equality on the right in (4.6) holds in the usual case where the symbols and have the same statistics. The stochastic gradient tap updating algorithms for the tap vectors and are given by the following expressions: 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where we have incorporated the factor in the step size . For , we get 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [25 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [25 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Similar to the conditions required for an adaptive updating algorithm, MMA is applied for a linear channel and requires the whiteness of the source data. 

nonsquare constellations, rather than the straight contours used for square constellations [see Fig. 6(c)]. The piecewise linear contours used for the 128-point constellation are shown on the left in Fig. 7. The dotted lines are used for the in-phase dimension and the solid lines are used for the quadrature dimension. 

The in-phase and quadrature cost functions for square constellations in (4.2) are modified as follows for nonsquare constellations having two different sets of statistics along each dimension: 

**==> picture [4 x 18] intentionally omitted <==**

**==> picture [4 x 18] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [84 x 74] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where is a constant that is a function of the signal constellation under consideration. Generalization to the case where there are more than two sets of statistics along each dimension is straightforward. Notice that two different constants are used in (4.12) and (4.13). We now show how these constants are computed for the 128-point constellation. 

The constants are always evaluated from the expression in (4.11), which requires the computation of the second- and fourth-order moments of the symbols. We now show how to compute , for example. We can compute this moment by considering the first quadrant only. Consider the subset of 24 complex symbols in this quadrant that applies to in Fig. 7. For these symbols 1, 3, 5, 7, 9, 11 and 1, 3, 5, 7 so that each value of occurs with probability 4/24 1/6. Similarly, the subset has 8 symbols for which 1, 3, 5, 7 and 9, 11 so that each value of occurs with probability 2/8 1/4. Thus, the variance of the symbols becomes 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [129 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [142 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

## _B. Nonsquare Constellations_ 

We now show how the MMA algorithm can be modified to take advantage of the statistics of the symbols used in nonsquare constellations. Fig. 7 shows a 128-point signal constellation, which is used to transmit blocks of 128 7 bits. This constellation is obtained from a square constellation with 12 12 144 points by removing the four outer points in each corner. We will assume that the symbol levels used along each dimension are taken from the set 1, 3, 5, 7, 9, 11 and that all the 128 complex symbols are sent with the same probability 1/128. In this case, the discrete values taken by the real and imaginary symbols and do not all have the same probability of occurrence. Specifically, the largest values 9, 11 occur less often than the smaller values 1, 3, 5, and 7. Thus, the statistics of the symbols and vary along their respective dimensions. 

MMA takes advantage of the variation of statistics along each dimension by using piecewise linear contours (or moduli) for 

Other moments for the symbols are computed in a similar fashion, and we find that the two moduli for the 128-point constellation are given by 9.2 and 6.1. The separate constant moduli for 32-CAP and 128-CAP are listed in Table II. A single modulus could also be used, but this would increase the probability of converging to the so-called 144-point wrong solution, which will be discussed in Section VIII. 

## V. GENERALIZED MMA (GMMA) 

The RCA and CMA blind equalization algorithms discussed previously are not very effective in providing a good eye opening when the number of different symbols in the signal constellation becomes very large. The basic MMA algorithm also has difficulties with very dense constellations, but, because of its flexibility, it can be modified to ease the eye opening of these constellations. This is achieved by dividing the complex plane of in-phase and quadrature output samples of the equal- 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1003 

izer into several disjoint regions, which all have their own cost functions and moduli. This modified MMA algorithm is called generalized MMA (GMMA). 

## _A. The Problem With Dense Constellations_ 

In this section, we provide a brief intuitive explanation of why RCA, CMA, and basic MMA have difficulties in opening the eye of very large signal constellations. From (3.7), (3.9), (4.7), and (4.8) we see that the stochastic gradient tap updating algorithms used for the phase-splitting equalizer, for example, all have the following generic form: 

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

where depends on the type of algorithm that is being used. Assume now that we are in steady-state and that the complex tap vector has converged in the mean, so that 

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Thus, in steady-state the mean of the correction term in the tap updating algorithm is zero, but its variance is generally not equal to zero. This results in tap fluctuations, which contribute tap adaptation noise to the output signal of the equalizer. When a decision-directed algorithm is used in steady-state operation, the quantity in the correction term becomes the error across the slicer, which is also equal to the noise at the output of the equalizer, as was shown in Section III-A. The magnitude of this noise is comparable to the magnitude of the additive noise in the channel, and is small compared with the spacing between the points in the signal constellation. Multiplication by the small step size further decreases the variance of the correction term. As a result, the tap fluctuations due to the adaptation algorithm are very small and do not contribute significantly to the MSE at the output of the equalizer. 

Assume now that we use RCA, for example. The quantity used in the correction term is then the error with respect to one of four points, as shown in Fig. 7. It should be apparent from the figure that this error cannot become small in steadystate operation, even in the absence of noise. It should also be apparent that the variance of increases compared with the squared distance between symbols when the number of points in the signal constellation is increased. This increases the tap fluctuations and associated tap adaptation noise, and makes it increasingly difficult to open the eye. The only way to keep the tap fluctuation noise low when is increased is to decrease the step size . However, this decreases the speed of convergence of the equalizer. In addition, finite precision effects become a factor in a practical implementation if is too small. It has been found that, for the applications discussed here, RCA, CMA, and basic MMA become impractical when 64, 128, and 256, respectively. 

Rather than decreasing the step size when is increased, one can, instead, try to keep the variance of the correction term small by keeping small. This is the approach that is used for GMMA. The idea is to divide the complex plane of equalizer output samples into smaller regions, which contain subsets of symbols of the main constellation. Each subset is then treated as a constellation with a reduced number of symbols, and 

**==> picture [216 x 199] intentionally omitted <==**

Fig. 8. GMMA sample subsets and moduli for 256-point signal constellation. 

has its own MMA cost function and modulus. With such an approach, the variance of and the corresponding tap adaptation noise remain manageable when the number of points in the main signal constellation increases. 

## _B. Principle of GMMA_ 

The principle of GMMA will be discussed with respect to the 256-point signal constellation shown in Fig. 8, where, for simplicity of notation, we are showing the in-phase dimension ( ) along the vertical axis and the quadrature dimension ( ) along the horizontal axis. We will again treat the in-phase and quadrature dimensions independently, as was done for the basic MMA. The dotted lines in the figure represent boundaries for various subsets of in-phase output samples of the equalizer. In this example, there are three subsets (1), (2), and (3), which include the symbol levels 1, 3, 5, 7 , 9, 11 , and 13, 15 , respectively. The solid lines represent the moduli, which are used for each subset, and we have 6.08, 10.25, and 14.17. Similar subsets and moduli are also defined for the quadrature samples . Multiple moduli (but not multiple sample subsets) had previously been used in [26] for a different cost function than the one proposed here. 

We now describe the GMMA tap updating algorithm as it applies to the in-phase tap vector of the phase-splitting equalizer shown in Fig. 4. The equation used for updating the tap vector is always the one given in (4.9). However, the value of the constant use in the computation is a function of the value of the in-phase sample . For example, if 8 12 in Fig. 8, then the modulus corresponding to this subset has to be utilized, i.e., 10.25. Similarly, when belongs to another subset, then the corresponding modulus has to be used in the computation of the tap updating algorithm in (4.9). 

## _C. Computation of the GMMA Design Parameters_ 

The definition of the various subsets of equalizer output samples and corresponding moduli used by GMMA is not straightforward, and has to be made carefully if one wants to get the benefits provided by this algorithm. Here, to address this problem, 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1004 

we present an iterative algorithm, which uses an equal energy type of principle and leads to a good choice of subsets of equalizer output samples and corresponding moduli. 

An ideal choice of sample subsets and moduli would guarantee that the tap fluctuation noise introduced by each subset is the same and is as low as possible. Practical designs, such as the one described below, can only approximate this ideal design. Rather than dealing directly with tap fluctuation noise, we will instead use a closely related quantity, which is the minimum of the MMA cost function. The main idea behind the iterative algorithm is to design sample subsets in such a way that this minimum is (roughly) the same for all the subsets. Assume now that we have in-phase subsets and that represents the th sample subset, which includes the subset of symbols . The cost function minimization is done with respect to each sample subset , i.e., we minimize 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

The minimum of this cost function is again obtained when or . If the minimum value of the cost function is the same for all the sample subsets, then the cost function of the dense constellation has the same minimum value. 

For simplicity, we will restrict our discussion of the iterative algorithm to square constellations, but it can also be used for nonsquare constellations. We will assume that the symbols and take values 1 3 2 1 , so that the maximum number of symbol levels (in magnitude) is . The expressions for the modulus and minimum of the MMA cost function for sample subset are the same as the ones used for basic MMA, except that they are only evaluated over the subset of symbols . The three main steps of the iterative algorithm are given below. 

- _Step 1:_ We first choose a targeted value for the minimum of the GMMA cost function, and we choose it in such a way that it corresponds to the minimum of a square constellation that is easily handled by basic MMA. For the 256-point constellation in Fig. 8, we have chosen 592, which is the minimum value of the MMA cost function for a 64-point constellation, as computed from (B-3) with 4. This choice also defines the design parameters for the first sample subset and we have 

**==> picture [9 x 8] intentionally omitted <==**

- (5.4) 

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

- _Step 2:_ We now outline the procedure used to find the design parameters of the second subset of samples . First, we define a square constellation 

- using a number of symbol levels . This signal constellation is obtained from the 64-point constellation by adding new symbol values, so that the symbols in the second subset take the following values . 

- Equation (B-9) in Appendix B gives a general expression for the minimum of the cost function of 

sample subset . Specializing (B-9) to the second sample subset, we get 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

There are two different ways to use this equation to find . One approach is to compute the cost function for various values of . The value of the cost function that is closest to the targeted 592 is obtained for 6, so that the design parameters for the second sample subset are 

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

   - The try-and-choose approach used above to determine the value of the parameter (or in general) is adequate for most practical applications, but is not very rigorous. A more systematic and mathematically pleasing approach is to replace the cost function on the left in 5.5 with its targeted value of 592 and then solve the equation for . This can be done with commercially available software packages. We find that the only solution that is in the desired range is 6.24, which has to be rounded to the closest integer, i.e., 6, for a practical implementation. 

- _Step 3:_ To get the design parameters for the third subset of samples, , we again use the procedure given in Step 2, except that the subscripts 2 and 3 replace the subscripts 1 and 2 in (B-9), respectively. We find that the design parameters for the third sample subset are 

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

The same procedure is then iterated until the computed is larger than the number of symbol levels used by the main constellation. For 256-CAP, this number is eight and the iterative algorithm stops after three subsets of samples have been defined. 

## VI. CMA–MMA 

Another generalized MMA is proposed in this paper, called CMA–MMA. Rather than to create new cost functions, the CMA–MMA jointly uses the two cost functions of CMA and MMA for in-phase and quadrature phase filters separately in a phase-splitting filter structure shown in Fig. 4. 

The main aspect of the algorithm of CMA–MMA introduces asymmetry into the tap updating algorithm of an equalizer, whereas other blind equalization algorithms use symmetrical algorithms for the two-filter equalizer. Referring to Fig. 4, the cost functions of CMA–MMA are proposed as 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

1005 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

The gradients of the cost functions derived from (6.1) and (6.2) as follows: 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Then we have the following stochastic gradient tap updating algorithms: 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

Note that the constants are different for two filters. For instance with 16-CAP, we use 3.6 for CMA and 2.86 for MMA. 

CMA–MMA algorithm jointly uses the CMA and MMA cost functions. Now we compare CMA–MMA and CMA. CMA is a truly two-dimensional (2-D) algorithm and CMA–MMA is a pseudo (2-D) algorithm. Due to the two-dimensional feature, both algorithms do not converge to diagonal solutions, which will be discussed in Section VIII. However, CMA–MMA rotates a constellation in a right position, but CMA remains the phase offset of the constellation. This means that CMA requires a rotator at blind startup and remains in steady-state, which results in an increase of complexity. 

The reason why CMA cannot rotate the constellation is discussed in [17]. Now, we show why CMA–MMA can rotate the constellations. Assume a rotated constellation by some angle , so that . The in-phase cost function is then given as 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

We want to show that this cost function takes its minimum value for 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

This is equivalent to the following in (6.7): 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

and 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [25 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

It is clear that the condition in (6.10) is true for any . We now simplify the conditions in (6.9). Equation (6.9) can be written 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [4 x 12] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [25 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [252 x 116] intentionally omitted <==**

Fig. 9. Dual-mode CAP–QAM receiver. 

So that (6.7) becomes 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [25 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

The quantity emphasized above is the negative of the so-called kurtosis. It can be shown that the kurtosis is always negative for typical signal constellation, so that this quantity is always positive, so that (6.8) is satisfied for any . 

CMA–MMA takes advantages of the strength of both CMA and MMA. CMA cannot rotate a constellation and MMA may converge to some wrong solutions. Without an additional cost, the new algorithm achieves more reliable convergence during initial startup. 

## VII. DUAL MODE CAP–QAM RECEIVER 

Recently, in some broadband excess standards require that the transmitter can use either CAP or QAM line codes [28]. The receiver, on the other hand, must accommodate both line codes, blindly startup, then blindly deciding which line code was sent, and finally decoding the sent symbols. In a straight forward way, we can use a parallel receiver, separately using CAP or QAM that may increase complexity. Another way to implement it is to start in CAP mode and switch to QAM mode if CAP mode does not produce satisfactory results. Now, we propose a dual-mode CAP–QAM receiver capable of demodulating both CAP and QAM-modulated data by using a single equalizer. In particular, this receiver applies to xDSL-type channels where no frequency offset is introduced. 

The detailed CAP and QAM transmitter can be found in [19]. The receiver structure of the dual-mode CAP–QAM is illustrated in Fig. 9. Now we propose a dual-mode CAP–QAM receiver for MMA. The MMA cost function for a CAP receiver is given as 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

If (7.1) is applied to the QAM signal in Fig. 3, the cost function needs to be adjusted as 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

We see from (7.2) that the constant needs to be computed for QAM receiver. Note that the computation of for the cost function in (7.1) with a CAP receiver can be found in Section IV 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1006 

and Appendix A. Now we derive the constant for QAM. The partial derivative of (7.2) for the in-phase dimension is given by 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

where is the carrier frequency and is the symbol period. With perfect equalization, or , (7.3) becomes 

From (7.8), we see that is a function of and with , this leads (7.8) become , which is the same as for MMA with a CAP receiver, see Appendix A. 

The constant can be computed from either (7.6) or (7.8), Because is dependent on , can be different even for the same constellation. For instance, for 16-QAM with 15.55 MHz and 25.92 MHz, we obtain . The following example computes the constant from (7.8) 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [11 x 4] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

Setting (7.4) to zero, we obtain 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

With the assumptions of , and , seeing in [17], (7.5) can be simplified in the steps shown in (7.6) at the bottom of the page. 

From (7.6), we see that for a QAM receiver, the constant is not only a function of the transmitted symbols, but also of the angle . Then the constant can be numerically computed from (7.6). It can also be expressed as a function of the symbol level number . The expression of for a standard MMA for CAP constellation can be found in Appendix A. We can rewrite (7.6) in as shown in (7.7) at the bottom of the page. Defining , (7.7) can be rewritten as 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

Above shows a basic dual-mode CAP–QAM blind equalizer. More developed algorithms of this type equalizer can be found in [19]. RCA and CMA can be also applied for CAP–QAM reception. However, for some applications, MMA achieves better performance. 

## VIII. CONVERGENCE TO WRONG SOLUTIONS AND INCOMPLETE SOLUTIONS 

One of the major problems with blind equalization is the possibility to converge the equalizer to so-called “wrong solutions.” These wrong solutions should be distinguished from the local minima discussed in [26]. When the equalizer converges to a local minimum, the cost function of the blind equalization algorithm is not minimized. Wrong solutions, on the other hand, can, potentially, minimize the cost function, as will be shown later. 

The probability of converging to a wrong solution during blind startup is a function of the type of blind equalization algorithm and equalizer structure being used. The characteristics of the channel can also be a major factor. Fig. 10 shows some 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1007 

**==> picture [248 x 194] intentionally omitted <==**

**==> picture [246 x 184] intentionally omitted <==**

Fig. 11. Rotated solutions obtained with CMA. 

Fig. 10. Wrong solutions obtained with RCA. 

wrong solutions, which were obtained in the laboratory with a phase-splitting equalizer when it was converged with RCA. 

In Fig. 10, the two solutions on the top were obtained with a 16-CAP transceiver using the 16-point constellation shown in Fig. 3(a) and the two solutions on the bottom were obtained with a 32-CAP transceiver using the 32-point constellation shown in Fig. 3(b). The _diagonal solution_ for 16-CAP that is shown on the top left is the most frequently observed wrong solution when RCA is used to blindly converge a phase-splitting equalizer. This solution occurs when the in-phase and quadrature filters of the equalizer synthesize the same transfer function. It should be pointed out that convergence to the diagonal solution is not possible with a cross-coupled equalizer. The two wrong solutions shown on the right produce signal constellations which are rotated by 45 with respect to the original constellation. This type of wrong solution can also be observed with the cross-coupled equalizer. Finally, the wrong solutions shown in Fig. 10 can also be obtained with MMA, but much less frequently than with RCA. 

CMA cannot converge a phase-splitting equalizer to the diagonal solutions shown on the left in Fig. 10. However, it systematically produces _rotated solutions,_ as shown in Fig. 11. This type of incomplete solution can be obtained with both phase-splitting and cross-coupled equalizers, or any other type of equalizer that uses CMA during blind startup. The use of differential coding can only correct 90 phase ambiguity wrong solutions, but it cannot converge an equalizer with arbitrary phase offset introduced in the channel. 

CMA produces these rotated solutions because it cannot compensate for a fixed phase offset introduced by the channel. Consider the CMA cost function in (3.8) and assume that the equalizer’s complex output samples are rotated by an angle . The cost function can then be written as 

**==> picture [5 x 25] intentionally omitted <==**

**==> picture [4 x 25] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

of the equalizer’s output samples can be obtained by rotating the complex tap vector , as should be apparent from (2.8). Thus, if the tap vector minimizes the CMA cost function when , then all its rotated versions also minimize the cost function and . RCA and MMA cannot produce rotated solutions with an arbitrary angle . However, they can, occasionally, produce the 45 rotation shown in Fig. 10. 

We conclude with one last type of wrong solution, which is the so-called _offset solution_ . This wrong solution is peculiar to the phase-splitting equalizer and can be observed with RCA, CMA, and MMA. It occurs when the in-phase and quadrature filters synthesize tap vectors which are offset in time by an integer number of symbol periods. Fig. 12 shows the effect of such a solution on a 128-point signal constellation. In this example, the transmitter uses the nonsquare 128-point signal constellation shown in Fig. 7. The signal constellation obtained at the output of the equalizer is shown in Fig. 12. This constellation is square and has 144 points instead of 128 points. To understand how this can happen, assume, for example, that the following successive real and imaginary symbols have been transmitted: and . If the equalizer had converged to the right solution, the complex outputs of the equalizer would be 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 10] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

and 

**==> picture [20 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [6 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

which correspond to valid points in the 128-point constellation. Assume now that the quadrature filter of the phase-splitting equalizer introduces a propagation delay that is one symbol period larger than the delay introduced by the in-phase filter. The complex output of the equalizer in symbol period will then be 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

**==> picture [6 x 9] intentionally omitted <==**

**==> picture [6 x 9] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [20 x 9] intentionally omitted <==**

Thus, the value of the CMA cost function is not affected by a rotation of the equalizer’s complex output samples . As a result, CMA cannot compensate for such a rotation. A rotation 

This is a corner point of the 144-point constellation and is not a valid symbol of the 128-point constellation. Offset solutions are easily detected with nonsquare constellations by simply looking 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1008 

**==> picture [204 x 204] intentionally omitted <==**

Fig. 12. 144-point offset solution for 128-CAP. 

at the signal constellation at the output of the equalizer. However, such a detection scheme is not possible when the signal constellation used at the transmitter is square. 

_Coping With Wrong Solutions:_ There are many techniques that can be used to handle wrong solutions during initial startup. One possibility is to monitor the bit stream at a higher layer and send a signal to the receiver if no valid data (such as ATM cells) are detected after a certain amount of time. The receiver can then initiate another blind startup of the equalizer with a new set of initial tap coefficients, for example. This process is repeated until proper convergence is achieved. This approach has been found useful in the applications discussed in [12] and [13], which have to deal with mild channel characteristics. The technique is somewhat less effective when the channel introduces very severe linear distortion. 

The rotated solutions obtained with CMA can be handled by using a rotator at the output of the equalizer. This rotator can be implemented as a carrier recovery loop of the type used for voiceband modems, for example [4], [19], and [27]. However, with such an approach, the rotator must be used all the time and must operate at the symbol rate in steady-state operation. This adds unnecessary complexity to the steady-state operation of the receiver when the rotator is not required for other purposes, such as tracking of frequency offset and carrier fluctuations introduced by the channel. The applications considered here do not have to deal with this kind of channel impairment. 

One way to handle wrong solutions is to modify the basic cost functions given in previous sections, and incorporate some constraints which do not allow the occurrence of wrong solutions. We provide one example here, which has been found to be effective in preventing the convergence of the phase-splitting equalizer to various wrong solutions, such as the diagonal solution. The constraint that is used is based on the fact that the impulse responses of the in-phase and quadrature filters of a phase-splitting equalizer form a Hilbert pair after convergence to the right solution. It is well known that functions that form a Hilbert pair are orthogonal and have the same energy. For a passband struc- 

ture, this leads to the following conditions on the tap vectors and : 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [200 x 12] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

We now make the following definitions: 

**==> picture [167 x 88] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

These quantities can be used to modify either the RCA, CMA, or MMA cost functions. For example, the MMA cost function in (4.1) is modified in the following way (with ): 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

and the tap updating algorithms in (4.9) and (4.10) become 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [7 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [23 x 39] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [7 x 10] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [4 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

where , , and are different step sizes, which are best determined empirically. 

Another way to handle wrong solutions is to use the CMA–MMA algorithm which is proposed in Section VI. Instead of modifying the cost functions, we simply use CMA for one channel and MMA for the other. This combined algorithm takes advantages of both CMA and MMA, where the former does not converge to diagonal solutions and the latter rotates the constellation to the right positions. 

## IX. EXPERIMENTAL RESULTS 

The experimental results presented in this paper were obtained in the laboratory with the setup pictured in Fig. 13. The transceiver prototype used in the experiments was initially developed to implement the 51.84 Mb/s 16-CAP transceivers used in the ATM LAN, and FTTC applications described in [12] and [14]. It has since been enhanced to accommodate other applications, such as the various CAP transceivers considered for VDSL and the 64-CAP transceiver specified for ATM LAN at 155.52 Mb/s [13]. The performance of the CAP transceivers has been evaluated in the laboratory with a variety of communication links using actual cables and connecting hardware. An example of such a cabling arrangement is the FTTC broadband access network shown in Fig. 1. 

The CAP receiver implemented in the prototype uses the phase-splitting equalizer shown in Fig. 4. This equalizer provides the best trade-off between complexity and performance in steady-state operation for the type of applications considered here. However, it is more prone to convergence to wrong solutions than some other equalizers, as was discussed in the previous section. The equalizer consists of three main hardware components, a FIFO that collects blocks of A/D samples, fast FIR filters that compute the equalizer outputs at the symbol rate , and a programmable digital signal processor (DSP) chip that can implement any of the tap updating algorithms discussed here. The tap updating algorithms are iterated in the DSP at a rate lower than . New tap coefficients are down- 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1009 

**==> picture [241 x 148] intentionally omitted <==**

Fig. 13. Laboratory experimental setup. 

**==> picture [250 x 189] intentionally omitted <==**

Fig. 14. CAP spectrum at the input and output of the channel. 

loaded from the DSP to the fast FIR filters when computation of the tap updating algorithm is completed. 

We now describe some experimental results obtained with the 51.84 Mb/s 16-CAP transceiver described in [14]. The upper trace in Fig. 14 shows the spectrum of the 16-CAP signal at the output of the transmitter. The lower trace shows the spectrum of the signal at the output of a VDSL communication link consisting of a 700 UTP loop with a 14 bridged tap. The deep notch in the spectrum is due to the bridged tap. RCA cannot blindly converge the equalizer in a reliable fashion with this type of channel impairment. Both CMA and MMA are much more effective in opening the eye. However, as was mentioned previously, CMA requires a rotator operating at the symbol rate at the output of the fast FIR filters in Fig. 13. Such a rotator has not been implemented in the prototype. 

For the equalizer with DSP setup shown in Fig. 13, we use 48 taps and initialize filter taps with the shaping filters of the transmitter. Fig. 15 shows the various steps of a blind startup obtained with MMA over a VDSL channel. The picture on the top left shows the signal constellation at the output of the equalizer before any tap adaptation has started, but after the AGC has settled. The signal constellation obtained after a couple of 

**==> picture [249 x 197] intentionally omitted <==**

Fig. 15. Main steps of a blind startup using MMA. 

**==> picture [252 x 87] intentionally omitted <==**

Fig. 16. 32-CAP and 36-point constellations. 

thousand tap updating iterations with MMA is shown on the top right. In real-time DSP setup, we just manually control the switch with observation. The picture on the bottom left shows the eye opening after about ten seconds. Note that due to the limitation of the DSP implementation, we can only record laboratory results within a few second duration. This eye opening is good enough to allow the receiver to switch from MMA to the LMS algorithm, which is done at this point. The LMS algorithm quickly tightens the dots and produces the steady-state signal constellation shown on the bottom right in the figure. 

We tested MMA with different lengths of equalizer. A minimum number of taps is required for a blind equalizer to obtain eye opening depending the applications. The equalizer used for 16-CAP may not long enough for 256-CAP. Initially, a blind equalizer can converge faster with fewer taps, but with higher error rate. After initial equalization, taps can be added to improve error performance. Using longer equalizer during blind startup will generate meaningless values for the extreme end taps. 

Fig. 16 shows the convergence for 32-point nonsquare constellation. Using piecewise multiple moduli in separate data spaces, MMA achieves better performance in terms of avoiding converging to wrong mapping solutions. The picture on the left shows the 32-point convergence when two moduli are used in MMA, and the picture on the right shows 36-point solution for 32-CAP. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1010 

**==> picture [418 x 192] intentionally omitted <==**

Fig. 17. Convergence performance with MMA and GMMA for 256-CAP. 

TABLE I 

MINIMUM VALUES OF THE COST FUNCTION FOR GMMA 

**==> picture [353 x 39] intentionally omitted <==**

Fig. 17 shows that the simulation results of comparing MMA and GMMA with the dense constellation of 256-CAP. As discussed in Section V, the use of multiple moduli gives better eye opening. Table I shows minimum values of the cost functions for 256 CAP when the separate data spaces are used. We see that the use of two moduli does not significantly reduce minimum cost functions. We use three moduli in this application. The computation of the three moduli can be found in Section V-C and illustrated in Fig. 8. Note that the subspace is divided after the AGC converges, i.e., with normalized gain. The picture on the left side shows the convergence with MMA and the picture on the right side shows that with GMMA. As shown in Fig. 17, GMMA exhibits better eye opening than MMA. By dividing complex plane into smaller regions, GMMA may increase the rate of wrong decisions if the decision which region to use is not correct. It is true that the equalizer will not converge if the probability of wrong decision is high. As discussed in Section III, the eye of the signal constellations is considered to be open when the slicer makes right decisions “most of time,” or when the MSE measured across the slicer is small enough. If subspaces are properly divided, the reduction of the minimum cost function helps equalizer decrease MSE. Simulation results show that with properly chosen parameters, GMMA can achieve better eye opening than MMA, particularly for some noisy channels. 

The various steps of blind startup with CMMA–MMA are illustrated in Fig. 18. CMA–MMA first converges to a constellation with a phase-offset, and then rotates to the right position. In this case, the convergence rate to a diagonal solution is tremendously reduced. In the laboratory experimental work, we tested CMA–MMA with various channel lengths of 20 ft, 150 ft, 300 ft, and 700 ft which introduce different phase-offset to the channel. A few hundreds of tests with those channels show no 

**==> picture [243 x 185] intentionally omitted <==**

Fig. 18. Convergence of MMA–CMA algorithm. 

convergence to diagonal solutions. At this point, CMA–MMA algorithm is more reliable than RCA and MMA. 

Experimental results for CAP–QAM are not covered in this paper. Interested readers can find detailed information in [19]. 

## X. SUMMARY 

In this paper, the multimodulus blind equalization algorithm and its generalized algorithms are presented. MMA combines the benefits of RCA and CMA algorithms that are used extensively in practical applications. MMA provides more flexibility than RCA and CMA. Along with GMMA and CMA–MMA, MMA exhibits the capability to handle nonsquare constellation, dense constellation and certain wrong 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1011 

solutions. MMA is also suitable in dual-mode CAP–QAM receiver. 

Computer simulations and laboratory experimental results are provided. The results support the theoretical analysis for MMA. MMA shows reduced rate of convergence to wrong mapping solutions. In addition, for 256-CAP, GMMA exhibits good eye opening due to the reduction of minimum value of the cost function. Without additional cost, CMA–MMA can be reliably used to avoid convergence to diagonal solutions. 

In the appendices, we calculate the constant modulus . The results provide a useful tool to analyze the cost function and performance. 

## APPENDIX A COMPUTATION OF THE CONSTANTS 

**==> picture [8 x 8] intentionally omitted <==**

This appendix presents the derivation of closed-form expressions for the various constants used in the RCA, CMA, and MMA algorithms. As will be shown, these expressions can be conveniently expressed as a function of the number of symbol levels (in magnitude) used along each dimension of the signal constellation. 

The general approach used to compute the constant will be explained for the MMA algorithm. The MMA cost function is given by 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

where and represent the equalizer’s output samples, and is a positive integer. For two-dimensional CAP systems, and represent the transmitted symbols for the in-phase and quadrature phase channels, respectively. When an equalizer converges, and , and the cost function becomes 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Assuming the same statistics for and , we have . In the following, only the analysis for the in-phase channel will be provided. The same analysis applies to the quadrature phase channel. For the in-phase dimension, the gradient of the cost function with respect to the real tap vector was previously given in (4.4) as 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Using the same method, we obtain the following expression for the constant used for CMA: 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

and for RCA, we get 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

_Square Constellations:_ The expressions derived previously for the constants are functions of the moments of the symbols and . These moments can be computed on an individual basis, although this can be tedious. For the usual case where the symbols have odd integer values it is possible to derive simple closed-form expressions for the constants as a function of the number of symbol levels. We will assume that the symbols take the following values , where indicates the number of symbol levels (in magnitude). The following summations can be found in [29], for example: 

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

These summations do not apply directly to sums of powers of odd integer, but can be used to derive closed-form expressions for these types of summations. For example, we can write 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [15 x 16] intentionally omitted <==**

**==> picture [14 x 16] intentionally omitted <==**

**==> picture [14 x 16] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

where the two sums in the middle have been evaluated from (A-8). Similar summation manipulations can be used for other sums of powers of odd integers, and we get 

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

The constant can now be evaluated by assuming perfect equalization, i.e., , and by setting the gradient to zero [2]–[4]. Also, if we assume that symbols in different symbol periods are uncorrelated, we get , where is a fixed vector whose entries are a function of the channel. We then get 

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [7 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

Solving for in (A-4), we get 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

For square constellations, the probability of occurrence of each symbol level is the same, i.e., , so that the moments of the symbol levels become 

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1012 

TABLE II 

THE CONSTANT R FOR BLIND EQUALIZATION ALGORITHMS 

**==> picture [319 x 66] intentionally omitted <==**

For CMA, the constant is a function of the moments of the complex symbols . Assuming that the symbols and are uncorrelated, it is easily verified that 

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Using the above results and , the constants for the three blind algorithms can be expressed in the following simple ways as a function of : 

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

For nonsquare constellations, MMA uses several moduli along each dimension. The various constants are then computed by evaluating the summations in (A-14) and (A-16) for various symbol subsets rather than the whole set of symbols. An example of the procedure is given in Section IV-B. 

The values of the constants for the RCA, MMA, and CMA are listed in Table II for square and nonsquare CAP applications. 

We can compute the minima of the CMA and RCA in a similar fashion, and we get 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

It should be pointed out that the CMA cost function in (B-4) is for both dimensions and that the MMA and RCA cost functions in (B-3) and (B-5) apply to one dimension only. Notice that the minimum of all three cost functions is zero for 1, which corresponds to 4-CAP. However, the minimum is nonzero when 1. 

The expressions for the modulus and cost function of the th in-phase sample subset used by GMMA are given by 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [22 x 9] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 18] intentionally omitted <==**

**==> picture [4 x 18] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [4 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

## APPENDIX B MINIMUM VALUES OF THE COST FUNCTIONS 

In this appendix, we derive closed-form expressions for the minimum values of the various cost functions. We will only consider square constellations. For the in-phase cost function of MMA, for example, we have 

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Using the value of in (A-19), we can rewrite the minimum of the cost function as follows: 

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [22 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Using the results in (A-16), (A-17), and (A-19) we then get 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where is the subset of symbols belonging to sample subset . These expressions are functions of the moments and , which can be written 

**==> picture [4 x 30] intentionally omitted <==**

**==> picture [4 x 30] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [8 x 4] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [22 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

where and are the number of symbol levels in the square constellations corresponding to sample subsets and , respectively. Using the results in (A-14) and (A-16) we get 

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

(B-9) 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

1013 

**==> picture [119 x 20] intentionally omitted <==**

when the gain of AGC and the initial values of the equalizer are properly chosen. It is easily verified that, with the constraint in (C-8), the following holds: 

The input and channel vectors are defined as follows: 

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

where is the number of samples. So the second-order expectation of the sample is 

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

and the equal sign holds if and only if the channel vector satisfies the ISI free condition in (C-5). 

The condition in (C-6) can be written as 

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

With the assumption that different symbols are uncorrelated we obtain 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [9 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [28 x 43] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

Replacing by its value and using (C-4) in (C-11), we can further simplify the equation to 

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

With a perfectly equalized channel and no ISI at the input of the slicer, the channel vector has only one nonzero entry equal to one and can be written as 

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

From the inequality in (C-9), we then have 

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [7 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

In order to show that minimization of the cost function results in zero ISI, we can show that 

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

and that the minimum is achieved when the channel vector satisfies (C-5). We now provide two such proofs, one for a constrained problem and one for a nonconstrained problem. A result which will be useful in the following analysis is: 

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [10 x 5] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 9] intentionally omitted <==**

**==> picture [6 x 9] intentionally omitted <==**

**==> picture [23 x 9] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 9] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

and equality can only hold if and only if the channel vector satisfies the ISI free condition in (C-5). 

_Unconstrained Problem:_ We now remove the constraint in (C-8) of keeping one entry of the channel vector equal to one. Using results given in [24], it is possible to show that 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

where and are called the kurtosis of the equalizer output samples and symbols, respectively. We can use (C-4) and (C-15) to solve for in (C-14), and we obtain 

Equality in (C-7) holds if and only if one the terms is nonzero and all the other terms are zero. 

_Constrained Problem:_ In this scenario, we assume that the channel vector can be written as 

**==> picture [7 x 6] intentionally omitted <==**

**==> picture [23 x 10] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [7 x 5] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [28 x 9] intentionally omitted <==**

Using (C-7) on the right side in (C-16), we obtain 

That is, one of the entries of the vector is constrained to remain equal to one, and the other entries can take any value. This assumption is a good approximation of what is done in practice 

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [28 x 10] intentionally omitted <==**

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 20, NO. 5, JUNE 2002 

1014 

Replacing by its value and using (C-15), the one-dimensional cost function of MMA in (4.7) can be written as 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [27 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

Using (C-17) in (C-18), we get 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [14 x 16] intentionally omitted <==**

**==> picture [14 x 16] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 31] intentionally omitted <==**

**==> picture [4 x 31] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [8 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [9 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [27 x 9] intentionally omitted <==**

Replacing in the above equation by its value on the right in (C-7), we have 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [5 x 13] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 7] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 30] intentionally omitted <==**

**==> picture [6 x 30] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [14 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [5 x 18] intentionally omitted <==**

**==> picture [5 x 18] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 18] intentionally omitted <==**

**==> picture [5 x 18] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [8 x 5] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 19] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [27 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

From (C-20), we conclude that the following holds: 

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 19] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [4 x 13] intentionally omitted <==**

**==> picture [27 x 10] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [6 x 7] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 5] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

if 

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [7 x 31] intentionally omitted <==**

**==> picture [6 x 31] intentionally omitted <==**

**==> picture [15 x 15] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [16 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [7 x 9] intentionally omitted <==**

**==> picture [8 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

(C-22) 

The left condition in (C-22) is always true. The right condition says that the kurtosis of the symbols has to be always negative. Equality can only hold if and in (C-20). From (C-7), this implies that only one can be nonzero and implies that the nonzero term has to be one, so that the channel vector has to have the ISI free form given in (C-5). 

To show that the kurtosis of the symbols used in typical signal constellation is always negative we can use the results obtained 

in Appendix A. The second- and fourth-order moments of the symbols are obtained from (A-14) and (A-16). Then, we have 

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [9 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 5] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [4 x 6] intentionally omitted <==**

**==> picture [27 x 10] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [5 x 8] intentionally omitted <==**

**==> picture [8 x 8] intentionally omitted <==**

**==> picture [9 x 6] intentionally omitted <==**

**==> picture [10 x 6] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

**==> picture [4 x 5] intentionally omitted <==**

It is obvious that the values in the brackets are always larger than zero for . As a result 

**==> picture [113 x 9] intentionally omitted <==**

**==> picture [10 x 8] intentionally omitted <==**

**==> picture [6 x 8] intentionally omitted <==**

**==> picture [7 x 7] intentionally omitted <==**

**==> picture [6 x 6] intentionally omitted <==**

**==> picture [6 x 4] intentionally omitted <==**

This completes the proof that minimization of the MMA cost function leads to ISI free output samples of the equalizer [17]. 

## ACKNOWLEDGMENT 

The authors would like to thank V. Lawrence for his support of this work, D. Harman and R. L. Cupo for their help with the experimental results, and L. M. Garth and K. Balemarthy for many useful comments on the material in this paper. 

## REFERENCES 

- [1] Y. Sato, “A method of self-recovering equalization for multilevel amplitude modulation systems,” _IEEE Trans. Commun._ , pp. 679–682, June 1975. 

- [2] R. D. Gitlin and J. J. Werner, “A “blind” equalizer tap adjustment algorithm for quadrature-amplitude modulation data transmission,” _Bell Laboratories Engineer’s Notes_ , Oct. 19, 1979. 

- [3] D. N. Godard and P. E. Thirion, “Method device for training an adaptive equalizer by means of an unknown data signal in a QAM transmission system,” U.S. Patent 4 227 152, Oct. 7, 1980. 

- [4] D. N. Godard, “Self-recovering equalization carrier tracking in two-dimensional data communications systems,” _IEEE Trans. Commun._ , vol. 28, pp. 1867–1875, Nov. 1980. 

- [5] A. Benveniste, M. Goursat, and G. Ruget, “Robust identification of a nonminimum phase system: Blind adjustment of a linear equalizer in data communications,” _IEEE Trans. Automat. Contr._ , vol. AC-25, pp. 385–399, Mar., 1980. 

- [6] J. R. Treichler and B. G. Agee, “A new approach to multipath correction of constant modulus signals,” _IEEE Trans. Acoustics, Speech, and Signal Processing_ , vol. ASSP-28, pp. 459–472, Apr. 1983. 

- [7] A. Benveniste and M. Goursat, “Blind equalizers,” _IEEE Trans. Commun._ , vol. 32, pp. 871–883, Aug. 1984. 

- [8] L. Hanzo, W. Webb, and T. Keller, _Single- and Multicarrier Quadrature Amplitude Modulation_ . New York: Wiley , 2000. 

- [9] C. R. Johnson, P. Schniter, T. J. Endres, J. D. Behm, D. Brown, and R. A. Casas, “Blind equalization using the constant modulus criterion: A review,” _Proc. IEEE_ , vol. 86, pp. 1927–1950, Oct. 1998. 

- [10] O. Shalvi and E. Weinstein, “Super-exponential methods for blind deconvolution,” _IEEE Trans. Inform. Theory_ , vol. 39, pp. 504–519, Mar. 1993. 

- [11] B. Jelonnek, D. Boss, and K. D. Kammeyer, “Generalized eigenvector algorithm for blind equalization,” _Elsevier Signal Processing_ , vol. 61, pp. 237–264, Sept. 1997. 

- [12] G.-H. Im, D. D. Harman, G. Huang, A. V. Mandzik, M.-H. Nguyen, and J. J. Werner, “51.84 Mb/s 16-CAP ATM-LN standard,” _IEEE J. Select. Areas Commun._ , vol. 13, pp. 620–632, May 1995. 

- [13] G.-H. Im and J. J. Werner, “Bandwidth-efficient digital transmission over unshielded twisted pair wiring,” _IEEE J. Select. Areas Commun._ , vol. 13, pp. 1643–1655, Dec. 1995. 

- [14] D. D. Harman, G. Huang, G.-H. Im, M.-H. Nguyen, J. J. Werner, and M. K. Wong, “Local distribution for IMIV,” _IEEE Multimedia_ , vol. 2, pp. 14–23, Fall 1995. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 

1015 

YANG _et al._ : THE MULTIMODULUS BLIND EQUALIZATION AND ITS GENERALIZED ALGORITHMS 

- [15] K. N. Oh and Y. O. Chin, “Modified constant modulus algorithm: Blind equalization and carrier phase recovery algorithm,” in _Proc. ICC ’95_ , Seattle, WA, June 18–22, 1995, pp. 498–502. 

- [16] J. Yang, J. J. Werner, and G. A. Dumont, “The multimodulus blind equalization algorithm,” in _in Proc. 13th Int. Conf. Digital Signal Processing_ , Santorini, Greece, July 2–4, 1997. 

- [17] J. Yang, “Multimodulus algorithms for blind equalization,” Ph.D. dissertation, University of British Columbia, Aug. 1997. 

- [18] J. J. Werner, J. Yang, and G. A. Dumont, “Blind equalization for broadband acess,” _IEEE Commun. Mag._ , vol. 37, pp. 87–93, Apr. 1999. 

- [19] L. Garth, J. Yang, and J. J. Werner, “Blind equalization algorithms for dual-mode CAP–QAM reception,” _IEEE Trans. Commun._ , vol. 49, pp. 455–466, Mar. 2001. 

- [20] K. H. Mueller and J. J. Werner, “A hardware efficient passband equalizer structure for data transmission,” _IEEE Trans. Commun._ , vol. COM-30, pp. 538–541, Mar. 1982. 

- [21] R. D. Gitlin, J. F. Hayes, and S. B. Weinstein, _Data Communications Principles_ . New York: Plenum Press, 1992. 

- [22] J. K. Tugnait, “Identification of linear stochastic systems via second and fourth-order cumulant matching,” _IEEE Trans. Inform. Theory_ , vol. 33, pp. 393–407, May 1987. 

- [23] S. Haykin, _Blind Deconvolution_ . Englewood Cliffs, NJ: Prentice-Hall, 1994. 

- [24] O. Shalvi and E. Weinstein, “New criteria for blind deconvolution of nonminimum phase systems (channels),” _IEEE Trans. Inform. Theory_ , vol. 36, pp. 313–320, Mar. 1990. 

**Jean-Jacques Werner** (F’92) was born on February 9, 1943, in Rountzheim in the Alsace region of France, and grew up in the nearby village of Hageneau. He received the engineering degree in electronics from the Institut National des Sciences Appliquees, Lyon, in 1965. He immigrated to Canada and received the Master’s degree, in 1967, from Laval University, Quebec, Canada. He subsequently moved to the United States and received the Sc.D. from Columbia University, NY, in 1973. He joined Bell Labs, Lucent Technologies (former AT&T), Holmdel, NJ, in 1973, where he immediately began making his notable contributions to both the theory and implementation of voiceband modems. He pioneered the use of software for real-time digital processing and conducted research in general areas of data communication, digital signal processing, and broadband access. His most outstanding contribution was the successful development of echo cancellation for full-duplex operation as is used in V.32 and V.34 modems. Over the course of his career, he has published extensively in archived journals and conferences and has been issued 45 patents. In addition, he has made several key contributions in areas of voice-band modems, DSL, and home-networks at various standards organizations. 

Dr. Werner, in recognition of his work, became a Fellow of the IEEE in 1992, and a Bell Labs Fellow in 1995. He was corecepient of two best paper awards, the 1996 Leonard G. Abraham Prize Paper Award and the best paper award at Interface 1984. 

- [25] W. A. Sethares, G. A. Rey, and C. R. Johnson, Jr., “Approaches to blind equalization of signals with multiple modulus,” in _Proc. IEEE Int. Conf. Acoustics, Speech, and Signal Processing_ , Glasgow, Scotland, May 23–26, 1989, pp. 972–975. 

- [26] Y. Li, J. K. Liu, and Z. Ding, “Length- and cost-dependent local minima of unconstrained blind channel equalizers,” _IEEE Trans. Signal Processing_ , vol. 44, pp. 2726–2735, Nov. 1996. 

- [27] N. K. Jablon, “Joint blind equalization, carrier recovery, and timing recovery for high-order QAM signal constellations,” _IEEE Trans. Signal Processing_ , vol. 40, pp. 1383–1398, June 1992. 

- [28] V. Oksman, Ed., _VDSL Draft Specification_ , June 1998, ANSI Standards Contribution T1E1.4/98 045R1. 

- [29] I. S. Gradshteyn and I. M. Ryzhik, _Table of Integrals, Series, and Products_ . New York: Academic, 1994. 

**Jian Yang** (M’98) received the M.S. and Ph.D. degrees in the department of electrical engineering from the University of British Columbia, Vancouver, BC, Canada, in 1992 and 1997, respectively. 

In 1995, she joined Bell Laboratories of Lucent Technologies, Holmdel, NJ, where she is currently a Member of the Technical Staff. From 1995 to 1999, she worked on the theory and practice of digital signal processing for communications, with applications to single and multicarrier (DMT) modulation, particularly using blind equalization techniques. Her research interests also include carrier detection, carrier and timing recovery, echo cancellation, and single/multirate adaptive filtering. She holds eight patents, mostly on blind equalization algorithms. She is currently working on wireless and fiber-optical communications, focusing on modulation, equalization, and echo cancellation. 

**Guy A. Dumont** (M’78–SM’84–F’99) received the Diplôme d’Ingénieur from ENSAM, Paris, France, in 1973, and the Ph.D. degree in electrical engineering from McGill University, Montreal, Canada, in 1977. From 1973 to 1974, and then again from 1977 to 1979, he worked for Tioxide France. From 1979 to 1989, he was with Paprican where he headed the Control Engineering Section, first in Montreal and then in Vancouver, BC, Canada. In 1989, he joined the Department of Electrical and Computer Engineering at the University of British Columbia, Vancouver, BC, Canada, where he is a Professor and leads the Process Control Group, and is currently Associate Dean of Applied Science. His current research interests are in adaptive control and filtering, distributed parameter system control, control loop performance monitoring, predictive control, with applications to the process industries, mainly pulp and paper, and more recently to biomedical engineering. 

Dr. Dumont was awarded the 1979 IEEE TRANSACTIONS ON AUTOMATIC CONTROL Honorable Paper Award; the 1985 Paprican Presidential Citation; the 1990 UBC Killam research Prize; the 1995 CPPA Weldon Medal; the 1998 Universal Dynamics Prize for Leadership in Process Control Technology; and the IEEE Control Systems Society 1998 Control Systems Technology Award. He is a Fellow of the BC Advanced Systems Institute, Vancouver, BC, Canada. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 29,2026 at 17:59:09 UTC from IEEE Xplore.  Restrictions apply. 


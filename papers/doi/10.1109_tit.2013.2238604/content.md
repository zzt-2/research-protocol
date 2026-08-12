IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3175 

# Phase-Based, Time-Domain Estimation of the Frequency and Phase of a Single Sinusoid in AWGN—The Role and Applications of the Additive Observation Phase Noise Model Hua Fu and Pooi-Yuen Kam _, Fellow, IEEE_ 

**_Abstract—_ This paper presents the theoretical foundation for time-domain, phase-based estimation of the frequency and phase of a single sinusoid in additive white Gaussian noise (AWGN), analogous to the theoretical foundation provided by Rife and Boorstyn for frequency-domain, Fourier-transform-based estimation. It is shown from the maximum** **_a posteriori_ probability (MAP) and the maximum likelihood (ML) estimation principles that with the additive observation phase noise (AOPN), due to the AWGN, being described by its** **_a posteriori_ distribution conditioned on the received signal magnitude, the received signal phase is a sufficient statistic for estimating the single-sinusoid angle parameters. Using a geometric approach, the exact statistical model for the AOPN is derived, where the** **_a posteriori_ probability density function (pdf) and the corresponding** **_a priori_ pdf are given by explicit, closed-form expressions that are valid for arbitrary signal-to-noise ratios (SNRs). The** **_a posteriori_ pdf is Tikhonov, and is of particular interest as it establishes the AOPN model for phase-based frequency/phase MAP/ML estimation in the time domain. It is further illustrated that the results derived can yield various AOPN models as special cases, and the underlying physical insights and interconnections that exist among these models are revealed. It is shown that the model derived by Tretter is an ultimate specialization in the high SNR limit of the AOPN models developed here. For high SNR, the** **_a posteriori_ Tikhonov pdf can be accurately approximated by a Gaussian distribution, which leads to the best linearized AOPN model. The applications of these AOPN models to the design of linear estimators, including the linear minimum mean square error (LMMSE) estimator, the linear minimum variance estimator, and the LMMSE implementation of the weighted phase averager are presented, and their estimation performances are compared through computer simulations, with the Cramer–Rao lower bound (CRLB) and the Bayesian CRLB as the benchmark. To facilitate estimator design, the** **_a priori_ statistical models of the frequency and phase are proposed from the information-theoretic perspective, and an improved phase unwrapping algorithm over that given by Fu and Kam is presented. It is shown that by incorporating all the information available in the AOPN, the estimation accuracy can be much improved.** 

### **_Index Terms—_ AOPN, frequency, linear estimator, phase, phasebased time-domain estimation, single-sinusoid, Tikhonov pdf.** 

Manuscript received March 13, 2011; revised April 30, 2012; accepted December 13, 2012. Date of publication January 09, 2013; date of current version April 17, 2013. This work was supported by the Singapore Ministry of Education Academic Research Fund Tier 2 under Grant MOE2010-T2-1-101. This paper was presented in part at the 2008 IEEE Vehicular Technology Conference. The authors are with the Department of Electrical and Computer Engineering, National University of Singapore, 117583 Singapore (e-mail: elefh@nus.edu.sg; elekampy@nus.edu.sg). 

Communicated by M. Lops, Associate Editor for Detection and Estimation. Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org. Digital Object Identifier 10.1109/TIT.2013.2238604 

## I. INTRODUCTION 

STIMATING the frequency and phase of a single si- **E** nusoid in additive white Gaussian noise (AWGN) is a classic problem of considerable research interest over the past several decades [1]–[26]. The most common approach is to model analytically the frequency and phase as unknown parameters over a closed interval with the physical interpretation given in [2], and apply the theory of maximum likelihood (ML) estimation [27]. However, due to the nonlinear nature of the problem, there is no explicit, closed-form mathematical expression for the absolute maximum of the likelihood function. As a result, several estimation algorithms were developed. One method is to locate the peak of the periodogram through a 1-D search. This has led to the well-known Fourier-transform (FT)-based frequency-domain solution via a coarse fast FT (FFT) followed by a fine numerical search [1]. In order to obtain better tradeoff between various estimator requirements, numerous refinements and improvements to this frequency-domain approach have been proposed in the literature; see, for example, [3]–[8] and their references. An alternative method, which is sometimes termed phase-based, time-domain estimation and the subject of this paper<sup>1</sup> , is to use the received signal phase which is expressed as the sum of the transmitted signal phase and an additive observation phase noise (AOPN), due to the AWGN, as the observation data sample to be fed into the estimator. For this method, modeling of the AOPN is a crucial issue. The first approximate AOPN model, which is valid only for high signal-to-noise ratio (SNR), was derived in [9] by Tretter through a purely mathematical approach. The resulting estimator has a linear regression implementation of the phase data that requires phase unwrapping [25], [26]. The work done in [9] is insightful and has inspired another large body of research. For instance, in order to avoid phase unwrapping, using the same approximate AOPN model as in [9], the weighted phase averager (WPA) estimator is proposed in [12], where the frequency estimate is obtained as a weighted sum of the differenced received signal phases acquired through a differential demodulation operation. Recently, an explicit, approximate, iterative, time-domain ML estimator was derived in [10]. The result shows how the magnitude and the phase of each received signal sample should be used in the estimation. 

> 1The focus of this paper is the AOPN model and its application to phasebased, time-domain estimation of the frequency and phase. Hence, the computational complexity comparison between the FFT-based frequency-domain approach and the phase-based time-domain approach is not addressed here, as such digression can lead us too far afield. 

0018-9448/$31.00 © 2013 IEEE Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3176 

A basic result of estimation theory [27] states that the ML estimator is asymptotically efficient, and for an efficient estimate, the ML estimate provides the unique solution. Therefore, if the peak of a periodogram [1] gives the FFT-based ML estimate via the frequency domain, a logical question is: what is the corresponding AOPN model that provides the phase-based ML estimate via the time domain? The answer to this question forms the main contribution of this paper. 

The aim of this paper is three-fold. First, under the unified framework of maximum _a posteriori_ probability (MAP) estimation which can be viewed as a regularization of ML estimation, we show that with the AOPN, due to the AWGN, being described by its _a posteriori_ distribution conditioned on the received signal magnitude, the received signal phase is a sufficient statistic for estimating the single-sinusoid angle parameters. By relating geometrically the AOPN with a Rician fading signal, the exact statistical model for the AOPN is derived, where the _a posteriori_ probability density function (pdf) conditioned on knowing the received signal magnitude is given by an explicit, closed-form expression that is valid for arbitrary SNR. The _a posteriori_ pdf obtained is Tikhonov, and is of particular importance as it provides _the answer_ to the aforementioned question (practically, the Tikhonov pdf has been widely used in modeling the statistics of the estimation error in frequency and phase tracking systems [28], [29]). As such, while Rife and Boorstyn [1] established the theoretical foundation for frequency-domain, FFT-based frequency and phase estimation of a single sinusoid, this paper provides the analogous theoretical foundation for time-domain, phase-based estimation. The corresponding exact _a priori_ pdf prior to receiving any data sample is also obtained in a similar way, and is related to the _a posteriori_ pdf through an approximation to the Tikhonov distribution at high SNR where the received signal magnitude information becomes irrelevant. Second, we illustrate that the results derived can yield various approximate AOPN models as special cases. In particular, for high SNR, the _a posteriori_ Tikhonov pdf can be accurately approximated by a Gaussian pdf, which provides a linearization to the phase-based observation data model, and gives the best linearized AOPN approximation so far. It is shown that the AOPN model in [9] is an ultimate specialization for the _a priori_ pdf derived here for high SNR. The underlying physical insights and interconnections that exist among these various AOPN models are revealed. Third, we adopt the linear minimum mean square error (LMMSE) and the linear minimum variance (LMV) criteria to demonstrate the applications of the various AOPN models developed to the design of linear estimators, and compare their performances through computer simulations. Since in the phase-based signal model, the data sample is a linear function of the parameters to be estimated, under the LMMSE and LMV criteria, we can readily design various kinds of linear estimators. We first develop the _a priori_ statistical model for the frequency and phase, and then, several linear estimators, including the LMMSE estimator and the LMMSE implementation of the WPA estimator, are presented. We show that by incorporating the information available in the AOPN, the estimation accuracy can be improved. Along with the estimator design, an improved phase unwrapping algorithm (over the one proposed in [10]) is presented, and its unwrapping performance is studied via simulations. 

This paper is organized as follows. The exact _a posteriori_ and _a priori_ AOPN models are derived in Section II. The AOPN approximations are presented in Section III. Applications to the design of linear estimators are presented in Section IV. Section V provides the simulation results and concludes this paper. 

## II. EXACT AOPN MODEL 

The aim is to recover accurately the unknown frequency and the unknown phase from the discrete-time, complex received signals , given by [1], [2] 



where is the transmitted signal amplitude, which is assumed to be known when necessary, the AWGN is a sequence of zero-mean, circularly symmetric, independent, identically distributed (i.i.d.), complex Gaussian random variables with covariance function , the sequence is assumed to be available from time . The moduloreduced and the moduloreduced are modeled as random parameters with pdf’s and over the interval . It is assumed that and are statistically independent of each other, and of the AWGN . The SNR is defined as . 

Fig. 1 gives a geometric representation of , , and in the in-phase-and-quadrature (I-Q) coordinate complex plane. The AWGN has been decomposed into two orthogonal components, namely, and , with being parallel to, and perpendicular to , and the two components are real-valued, i.i.d., Gaussian random variables each with mean zero and variance . It follows from Fig. 1 that in the I-Q coordinate system, the received signal phase can geometrically be represented as the sum of the transmitted signal phase and an AOPN component<sup>2</sup> , denoted here as , which is due to the AWGN , i.e., we have 



Note that in (2) represents the unwrapped received signal phase, which is obtained from the principal argument of by phase unwrapping. Comparing (2) with (1), we see that the nonlinear relationship between the data sample and the parameters and in (1) has been converted into a linear relationship between the data sample and and in (2). The goal of phase-based time-domain estimation is that instead of using , the received signal phase is exploited to recover and . Under the MAP criterion, a unified framework for parameter estimation, the estimates of and are the values that maximize the _a posteriori_ probability (APP) when in (1) is used, or the APP 

2In this paper, the definition of “phase noise” follows from [9, eq. (8)], that is, the quantities , , and represent the transmitted signal, the received signal, and the AWGN, respectively, whereas the quantities , , and represent the transmitted signal phase, the received signal phase, and the additive phase noise, respectively. In some literature, e.g., [30], the term “phase noise” refers to the rapid, random fluctuations in the oscillator’s frequency, caused by jitter. To avoid this terminology confusion, the quantity in (2) is referred to here as the additive observation phase noise, abbreviated as AOPN. This is because in estimation theory [27], the quantities in (1) and in (2) are usually referred to as the estimator observation (also called the estimator measurement). 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3177 



<!-- Start of picture text -->
.<br><!-- End of picture text -->

Fig. 1. Geometric representation of the received signal 

when in (2) is used. By solving the log-APP equation, it can be easily shown that the equivalence of linear model (2) to nonlinear model (1) under the MAP criterion is true if and only if it is true under the ML criterion. The likelihood function can be further evaluated by transforming from rectangular coordinates to polar coordinates , i.e., one has 





From (1), the quantity can be computed as , where is statistically identical to , as can be absorbed into without altering its statistical properties. Hence, statistically has no dependence on and (see also Fig. 1), and the pdf term in (3) can reduce to . Moreover, given and , the only randomness in is due to . Therefore, the conditional pdf in (3) will reduce to , where the subscript specifies that the pdf is that of the random variable . Accordingly, (3) can be expressed as 

First, it is seen from Fig. 1 that in the newly formed I’-Q’coordinate system, which is the I-Q-coordinate system rotated by the angle , the received signal in (1) can be rewritten as 



The magnitude and phase of in the I’-Q’-coordinate system are given, respectively, by 





Next, we interpret the received signal in (5) as a Rician fading signal with real-valued, constant mean . The joint pdf of and and the marginal pdf of in (6) are well known, and are given, respectively, by [27] 







Finally, using , we have 



where is only a function of . It follows from (3) and (4) that the equivalence of using to using for estimating and lies in specifying the conditional distribution , which in turn amounts to specifying the conditional pdf . We now derive 

. 





which is a Tikhonov pdf with mean zero, and depends on the transmitted signal amplitude , the AWGN variance , and the online received signal magnitude . The result (9) gives the statistical model for the AOPN in (2). In other words, 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3178 

the nonlinear model (1) of , and parameters and with AWGN , is tantamount to the linear model (2) of and and with AOPN governed by the Tikhonov conditional pdf (9). 

receiving the data. After receiving , the state of knowledge of the estimator concerning is changed, and all the information concerning is contained in the pdf (9). 

A further understanding on (9) and (13) can be gained in the high SNR regime. As SNR increases, becomes better and better approximated by for most times . Accordingly, the received signal magnitude information becomes less and less important, and the _a posteriori_ pdf (9) tends to , which reduces to the _a priori_ pdf , as is a constant quantity. Specifically, putting the approximation into (9), we have 

To understand this equivalence more clearly, we now consider the ML estimation of and . It can be shown that the likelihood equations obtained from (2) are identical to those from (1), provided that the AOPN in (2) is given as in (9). This means that using the received signals leads to the same ML estimates for and as using the received signal phases with received signal amplitudes incorporated in the AOPN model (9). This result, therefore, establishes the theoretical basis for phase-based estimation of the single-sinusoid angle parameters. Specifically, suppose that we want the estimates of and based on data samples , or equivalently, . In view of (9), the likelihood function in (2) is given by 





The result (14) provides actually the asymptotic pdf for the complex phasor perturbed by AWGN [31, eq. (3)], which is shown through a mathematical derivation [31, App. I] to be an approximation to the exact _a priori_ pdf (13) for small values of the variance . The derivation here of (14) from (9) presents an alternative approach, which is simpler. 





## III. APPROXIMATE AOPN MODELS 

The necessary conditions for the ML estimates of and are thus obtained as 

Analyses of the asymptotic behavior of the Tikhonov pdf’s (9) and (14) for large values of and can provide us several approximate models for the AOPN . For instance, by using the Jacobi–Anger formula: , it is shown that a Tikhonov pdf can be expressed by an _exact_ infinite Fourier series [28], i.e., (9) and (14) can be expressed, respectively, as 











In comparison with [10, eqs. (4) and (5)], it is seen that the loglikelihood equations (11) and (12) are identical to those obtained by using the likelihood function [10, eq. (2)]. 



We next examine more closely the relationship between the _a posteriori_ Tikhonov pdf of in (9) and the corresponding _a priori_ pdf, which can be obtained from (7) for as 

Alternatively, using the asymptotic expression: for large , and expanding the cosine function, , by a Taylor series, (9) and (14) can also be asymptotically _approximated_ , respectively, by 







where . The physical interpretation of the pdf’s (9) and (13) is as follows. Before receiving , based merely on knowing that is an AWGN and the SNR information , the estimator can gain some (18) knowledge on the AOPN . This knowledge is specified by the pdf (13) which depends exclusively on the SNR; without knowing the SNR, (13) is unknown. In other words, (13) provides the exact _a priori_ pdf of for arbitrary SNR before Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 



FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3179 

Clearly, if truncation is applied to the infinite series expressions (15)–(18), we can obtain numerous approximate models for the AOPN , depending on the degree of truncation. Among these approximate models, the Gaussian approximation is of particular interest. This is because under the ML estimation criterion, which is optimal in terms of the threshold SNR [1], the Gaussian approximation for the AOPN will lead to a linearization to the linear signal model (2), meaning that under the ML criterion, the estimates of and can be obtained analytically as a linear function of the observation data samples . In the sequel, we will use the Gaussian distribution to approximate the pdf’s (9) and (14), and compare the results obtained with those given in the literature. 

The first Gaussian linearized model for in (2) (referred to hereafter as Tretter’s AOPN model) is developed in [9] by a purely mathematical approach which involves two approximations. It is given by 

leads to a better estimation performance. An insight into this variance difference can be gained as follows. Recall from [10] and [11] that it is argued that, conditioning on , we have in (20), because the only randomness in is due to AWGN component with variance . However, it is seen from (6) that since and are correlated, knowing will provide partial information on , and this information will modify its variance. This means that conditioned on , the variance of in (20) is no longer . In fact, conditioned on , the quadrature noise in Fig. 1 is not Gaussian anymore. The exact conditional pdf in (20) can be derived as follows. First, it follows from (6) that the conditional pdf can be evaluated as (23) 



Here, the AOPN is approximated by a Gaussian random variable with mean zero and variance . Using a geometric approach, it is shown in [10] and [11] that (19) can be improved by introducing a new model for which involves only one approximation (referred to hereafter as the geometric AOPN model). It is given by 

where is Gaussian with , and is Rician given by (8). Next, conditioned on and in view of (6), in (23) can be obtained by first deriving the pdf of the random variable , where , and then evaluating the pdf of . The result is 





where, conditioned on the magnitude being known, the AOPN is a zero-mean, Gaussian random variable with variance . It is illustrated in [10] and [11] that the geometric AOPN model (20) can intelligently identify those observed instantaneous phase samples with large errors, and, thus, can improve the estimation performance. By dropping terms in the fourth and higher powers of in the exponents of (17) and (18), the Tikhonov pdf’s in (9) and in (14) reduce to the Gaussian pdf’s given, respectively, by 







Comparing (22) with (19), it is seen that the Gaussian approximation (22), which originates from the Tikhonov approximation (14) to the exact _a priori_ pdf (13) for high SNR, is the same as Tretter’s model (19). This means that Tretter’s model can only provide the estimator an approximation to our prior knowledge on the exact _a priori_ AOPN before is collected. The result (21) is more accurate than the geometric model (20), and gives the best linearized AOPN model so far. The difference lies in that the variance in (21) is , whereas in (20), it is . Simulation results will show that the model (21) (referred to hereafter as the best linearized AOPN model) 

Putting (8), (24), and into (23), we have 





Finally, noting that in (20), the exact conditional pdf is computed as 





which is more complicated than a Gaussian pdf. The asymptotic behavior of (26) for high SNR can be seen as follows through several approximation steps. First, at high SNR, is small so that can be approximated by . Second, for large values of , and . Then, we have 



Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3180 



Fig. 2. Underlying physical and pdf interconnections among the various AOPN models. 

Using the approximation , together with (27), one finally has 





which is identical to (21). This reveals that the exact pdf is asymptotically Gaussian. Although (26) is more accurate and gives the exact, closed-form expression for , in this paper, we keep the Gaussian approximation , for the AOPN model (20) due to its geometric simplicity. 

For easy reference, depending on the AOPN models used, the pdfs of in (2) are summarized in Table I. The underlying physical insights and interconnections that exist among the aforementioned AOPN models are illustrated in Fig. 2. It is seen that Tretter’s AOPN model provides an ultimate specialization for the various AOPN models for high SNR. 

## IV. APPLICATION TO THE DESIGN OF LINEAR ESTIMATORS 

In this section, we first develop _a priori_ statistical models for and , and then, adopt the LMMSE/LMV estimation criteria to demonstrate the application of the various AOPN models developed to the design of linear estimators. Along with the estimator design, an improved phase unwrapping algorithm is proposed and its performance is analyzed. 

that on the one hand, the uniform distribution for and gives the maximum entropy, , which represents the most prior ignorance of the estimator before time [32], while on the other hand, the variances, and , for the pdfs and that have entropy less than , must always be smaller than , the variance when and are uniform. It is known that subject to the conditions 

and , the Gaussian distribution provides the maximum entropy [32]. Thus, it would be reasonable to require and to have the following properties: 1) they satisfy the interval constraints and ; 2) for variances less than 

, they resemble the Gaussian distribution so that they not only model the _a priori_ statistical information on and , but also retain the maximum entropy; and 3) they converge to the uniform distribution as the variances approach . The Tikhonov pdf satisfies all these requirements. Without loss of generality, assuming that the _a priori_ mean values of and are zero, and can then be expressed as 







Following [28, eq. (4.39)], the corresponding variances and are given, respectively, by 

## _A. A Priori Statistical Models of and_ 

To obtain phase-based, time-domain estimates of and under the LMMSE criterion, we need their _a priori_ statistical (30) models, i.e., and in (2) should be available to the estimator prior to time . Here, we adopt the Tikhonov pdf The pdf’s and in (29) can model, via the paramto model and . The physical modeling of and coneters and , various degrees of prior knowledge of and fines them to within the finite interval [2]. This implies . Now, we see that in (2) is given as a linear sum Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 



The pdf’s and in (29) can model, via the parameters and , various degrees of prior knowledge of and . Now, we see that in (2) is given as a linear sum of 

FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3181 

TABLE I 

AOPN MODELS, pdf EXPRESSIONS, AND THE VARIANCES 



three Tikhonov random variables, and thus, due to the nonlinear nature of the problem, the estimate has no closed-form solution when the MAP criterion is used. However, under the LMMSE/LMV criterion, the linear model (2) can easily allow us to design an LMMSE/LMV estimator. This is because in designing an LMMSE/LMV estimator, only the variances of the Tikhonov random variables are needed. 

## _B. LMMSE Estimator_ 

In designing an LMMSE estimator, it is convenient to use a matrix–vector notation to describe (2). Without loss of generality, it is assumed that a fixed block of data samples is collected for the processing. We use to denote a vector holding , the unwrapped phase of ; to denote a vector holding the parameters to be estimated; and to denote a vector holding the AOPN components. Then, the linear signal model (2) can be expressed in matrix–vector notation as 



where is an constant matrix which depends on time index . The LMMSE criterion is concerned with determining the best approximation of that is a linear combination of , i.e., , and minimizes the cost function . The result is well known, and is given by 



where is the covariance matrix of ; is the covariance matrix of , given by . The corresponding MSE covariance matrix is given by 



Clearly, the elements of in (32) depend on the specific AOPN model since is determined by the variance , which has been summarized in Table I. 

## _C. Improved Phase Unwrapping Algorithm and Its Performance_ 

As pointed out in (2), since the actual phase data sample is obtained from the principal argument of which is within the interval , to generate , phase unwrapping is required. A simple, recursive phase unwrapping algorithm presented in [10] and [11] can be used in the LMMSE estimator (32). In this section, we propose a new, improved phase unwrapping algorithm, which, as will be shown by simulation in Section V, has a better unwrapping performance than that given in [10] and [11]. The algorithm works as follows. 

From (1) and (2), we have and . Thus, the phase difference between data samples and , denoted as , can be obtained as 



Here, is obtained in practice by projecting data sample onto and then taking the phase of the resulting complex quantity. The first data sample at time , given by , is an observation on the phase alone. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3182 

If , is equal to the principal argument of , i.e., we have 

approximation to (29) for and when the quantities and are high 





Then, in view of (34) and (35), a sequence of angle data can be computed as 



Now, and are given, respectively, by a sum of two and three zero-mean, independent Gaussian random variables. The probabilities and can then be computed as 









and the conditional probabilities and can be computed as 

Comparing (36) with (2), we see that can be retrieved from the computed angle data as they are mathematically identical. In other words, the moduloreduced should be _exactly_ equal to , the principal argument of . However, in practice, this may not be achievable. To obtain more accurate observation data, the phase of is collected by unwrapping to within a -interval centered around the computed value , i.e., the value of chosen is the one lying in the interval . This is done by adding multiples of to , when the absolute difference between and is greater than . The necessary conditions for a good performance of this phase unwrapping operation are that in (34) satisfies 



Several conclusions can be drawn from (39) and (40). First, the probabilities (39) and (40) depend on the online data . This means that the actual values of can provide us knowledge on where an unwrapping failure is more likely to occur. Second, in order to obtain an average probability versus the SNR , we need to average (39) and (40) over the Rician pdf (8). Third, it is seen from (36) that the algorithm is limited by the unwrapping failure propagation, since a particular failure at time point will affect all succeeding points is added to each of . 



and (35) is true. Clearly, the validity of these two conditions occur. Second, in order to obtain an average probability versus is expected to depend on the SNR as well as the values of the SNR , we need to average (39) and (40) over the Rician and , since a value of and close to is expected to lead pdf (8). Third, it is seen from (36) that the algorithm is limited easily, due to a small amount of AOPN, to the actual value by the unwrapping failure propagation, since a particular failure of in (37) and in (35) falling at time point will affect all succeeding points is added outside of the boundaries of the interval . When the to each of . conditions (35) and/or (37) are not satisfied, cannot be unwrapped correctly to and a phase unwrapping failure will occur. The probabilities that and lie outside _D. LMMSE Implementation of WPA Estimator and the_ the interval can be computed in two ways. First, they _Performance Improvement_ are computed as and . Phase unwrapping has been a very challenging problem phase extraction [25], [26]. Despite an enormous research effort, Second, in order to differentiate the effect of the SNR on no perfect phase-unwrapping solution has been obtained. phase unwrapping, which is our main concern, from that of avoid unacceptable performance degradation due to phase unthe values of and , they are evaluated as the conditional wrapping failure, the WPA estimator is proposed in [12] where probabilities and . the differenced received signal phase in (34) is used as the If the Tikhonov pdf’s (9) and (29) are used for and observation data sample. The WPA estimator formulated in [12] and , and will be, respectively, a sum of two adopted the same linearized AOPN model as in [9], i.e., it used and three Tikhonov random variables, whose distribution has Tretter’s model (19). This section revamps the study in [12] by no closed-form solution. To simplify the analysis, we use the developing an LMMSE implementation of the WPA estimator best linearized model (21) for and the following Gaussian and presents the application of the various AOPN models to its Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

Phase unwrapping has been a very challenging problem in phase extraction [25], [26]. Despite an enormous research effort, no perfect phase-unwrapping solution has been obtained. To avoid unacceptable performance degradation due to phase unwrapping failure, the WPA estimator is proposed in [12] where the differenced received signal phase in (34) is used as the observation data sample. The WPA estimator formulated in [12] adopted the same linearized AOPN model as in [9], i.e., it used Tretter’s model (19). This section revamps the study in [12] by developing an LMMSE implementation of the WPA estimator and presents the application of the various AOPN models to its 

FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3183 

design. As in [12], the parameter that we are interested in here is only the frequency , the phase being considered to be a nuisance parameter (since the differenced phase is used, the WPA estimator cannot estimate ). 

Suppose that a fixed block of data samples is collected for the processing. The inputs to be fed into the estimator are the phase differences , where is obtained via (34). Now, using the matrix–vector notation for a block of differenced phase data samples , we have 

If the approximate _a priori_ model (14) is used, we have 



If Tretter’s model (19) is used, we have 





where is an -dimensional column vector; is an -dimensional column vector with components all equal to 1, and is an -dimensional column vector with colored noise components given by . Note that if the AOPN models (19)–(21) are used, is a colored Gaussian vector. The LMMSE implementation of the WPA estimator is to find the estimate of which is a linear function of (i.e., , where is an -dimensional weighting row vector), and minimizes the MSE . The solution is given by 





where , and is the covariance matrix of the noise vector which has a tridiagonal form whose components depend on the specific AOPN model. The component can be evaluated as follows. If the exact _a posteriori_ model (9) is used, we have 



If the best linearized model (21) is used, we have 









If the geometric model (20) is used, we have 









We notice that the noise covariance matrix in (42) has the same feature as that of in (32), i.e., the diagonal elements of the covariance matrix for the AOPN models (9), (21), and (20) are inversely proportional<sup>3</sup> to some function of the data sample magnitude . This means that the estimator can use the online received magnitude information to identify those instantaneous received signal phase samples with higher noise variances. Accordingly, in the region of low SNR when large noise samples are more common, this feature can be exploited to indicate to the estimator the exact positions of the observation data samples which are less reliable, and, thus, should be weighted less in their contribution to the estimator. Indeed, we can even make use of this online information to improve the performance at low SNR by selectively dropping the most noisy data samples from the real-time estimation process. Using the estimator (42) as an illustration, this can be done in the following several ways. 

The first way is to drop those samples in a sequence of for which the AOPN components have larger variances. Since values of the diagonal elements of the covariance matrix at time point are associated with two successive received signal magnitudes at time points and , the samples to be dropped depend on , where denotes a mapping function that is dependent on the specific AOPN model. 

The second way is to first eliminate the noisy individual data samples before formulating the differenced phase data . For example, suppose that a sequence of received signal samples are collected and we know that is not reliable and should be excluded. Then, the sequence can be formulated as 





Comparing (48) with (34), we see that the two samples and in (34) have been replaced by one sample in (48). In this way, we prevent the sequence from being 

> 3For the exact _a posteriori_ Tikhonov model (9 <mark>)</mark> , it is seen from the numerical plot [28, Fig. 4.8] that the variance of a Tikhonov random variable with pdf is a monotonically increasing function of . 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3184 



Fig. 3. Performance comparison of the LMVE for different AOPN models with Algorithm 1 for phase unwrapping. 

disturbed too much by . In practice, in (48) is obtained by the operation 



from which we see that the variance of the AOPN is reduced by 3 dB, and as such the probability of phase unwrapping failure decreases. 

The third way is to revamp the modified WPA estimator proposed in [19]. The estimator in [19] is different from the WPA in that the average values of data samples are used to form the phase differences with the aim to lower the noise variance. However, since the overall SNR can be either enhanced or reduced depending on the actual value of frequency to be estimated, an estimation range has to be imposed. Unfortunately, unlike the estimators given in [15] and [16] to which [19] has been compared, the range limitation in [19] is due to SNR degradation, whereas in [15] and [16], it is due to phase unwrapping. In this aspect, the range limitation in [19] is mandatory. 

## V. SIMULATION RESULTS AND CONCLUSION 

Computer simulation is performed to compare the performance of the linear estimators developed. The number of simulation runs used to obtain each simulation data point is set to . We present only the simulation results for the frequency . The same conclusions can be drawn for the phase . The performance is measured by the inverse MSE, , achievable versus the SNR in a specified number of data samples if the LMMSE criterion is adopted, and by the inverse estimation error variance, 

, if the LMV criterion is used. As a basis for comparison, we also plot the inverse Cramer–Rao lower bound (ICRLB) and the inverse Bayesian CRLB (IBCRLB)[11]<sup>4</sup> . The BCRLB is given by 





and the CRLB is given by 

(50) Two phase unwrapping algorithms, i.e., Algorithm 1 presented in Section IV-C and Algorithm 2 in [10] and [11], are examined. Fig. 3 plots the computer simulation results of the variance under the LMV criterion for the various AOPN models with the number of the data samples . The actual values to be estimated are 1.0 and for and , respectively. Algorithm 1 which does not suffer from phase unwrapping failure propagation is assumed in the phase unwrapping operation. The LMV estimator (LMVE) is obtained from (32) as , which can be easily verified to be unbiased because the mean value is evaluated as 

. An estimate that is 

> 4Recent works in [33]–[35] show that for modulo-periodic parameter estimation (the frequency and phase are modulo-periodic parameter), the conventional MSE may not be an appropriate criterion and the standard CRLB and BCRLB may not be valid bounds. To find suitable performance criteria and bounds for modulo-periodic parameter estimation is a forefront of current research [33]–[35]. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3185 



Fig. 4. Performance comparison of phase unwrapping Algorithm 1 and Algorithm 2 for the LMVE. 

wrapping failure at time ). Since in practice the estimation errors and always exist in Algorithm 2, the performance of Algorithm 1 is superior to that of Algorithm 2. Figs. 5 and 6 present the simulation results of the LMMSE estimator (32) for the various AOPN models and the performance comparison of the two phase unwrapping algorithms, respectively. The _a priori_ values and in (29) are both set to 60, and . In Fig. 5, Algorithm 1 is used for phase unwrapping and in Fig. 6, the best linearized model and Tretter’s model are adopted. Under the LMMSE criterion , the expectation is taken over both and , and it follows from (49) that the quantity for also affects the MSE of . This means that in the simulations, both and should be generated randomly according to the Tikhonov pdf (29). Again, the results in Fig. 5 show that at high SNR, the LMMSE estimates can attain the BCRLB for all AOPN models. As SNR decreases, the exact _a posteriori_ model gives the best performance and Tretter’s model produces the worst. As in Fig. 3, the performance of the best linearized model is superior to that of the geometric model. The price we need to pay for this performance improvement is the additional complexity due to the fact that the transmitted signal amplitude must be known at the estimator (no knowledge of is required for Tretter’s model and the geometric model). Moreover, the conclusion on the performance comparison between phase unwrapping Algorithm 1 and Algorithm 2 for the LMMSE estimator under the same AOPN models in Fig. 6 is similar to that drawn in Fig. 4. 

unbiased and whose variance attains the CRLB is an efficient estimate [27]. It is seen from Fig. 3 that at high SNR, the LMV estimates are efficient for all AOPN models. As SNR decreases, the performance for Tretter’s model degrades fastest. At medium SNR, the exact _a posteriori_ model, the geometric model, and the best linearized model provide slightly different performances. As SNR decreases further, we see that the exact _a posteriori_ model outperforms the geometric model and the best linearized model. The results in Fig. 3 also confirm that the best linearized model gives further performance improvement over the geometric model, especially at low SNR. The estimation threshold SNR gain is about 1.0 dB. 

Fig. 4 gives the performance comparison of the two phase in the simulations, both and should be generated randomly unwrapping algorithms for the LMVE’s with , according to the Tikhonov pdf (29). Again, the results in Fig. 5 , and . The best linearized model and Tretter’s show that at high SNR, the LMMSE estimates can attain the model are assumed. It is seen that for the same AOPN model, BCRLB for all AOPN models. As SNR decreases, the exact _a_ Algorithm 1 performs better than Algorithm 2. The recursive _posteriori_ model gives the best performance and Tretter’s model prediction and updating feature of the phase unwrapping opproduces the worst. As in Fig. 3, the performance of the best eration in Algorithm 2 of [10] and [11] requires that no unlinearized model is superior to that of the geometric model. The wrapping failure occurs in the initial estimation step and the price we need to pay for this performance improvement is the initial estimates should be reasonably reliable. For instance, additional complexity due to the fact that the transmitted signal in estimating and , at least two data samples, namely, amplitude must be known at the estimator (no knowledge and are needed in of is required for Tretter’s model and the geometric model). the initial estimation step. Hence, correctly unwrapping Moreover, the conclusion on the performance comparison beand is a prerequisite. To improve the estimation accutween phase unwrapping Algorithm 1 and Algorithm 2 for the racy, more data samples have to be collected. However, this LMMSE estimator under the same AOPN models in Fig. 6 is will increase the probability for phase unwrapping failure in similar to that drawn in Fig. 4. the initial step, which in turn leads to unwrapping failure propFig. 7 gives the comparison of the inverse MSE between the agation (in Fig. 4, it is assumed that no unwrapping failure AOPN models for a particular sample value of with propagation occurs for either Algorithm 1 or Algorithm 2). and for the LMMSE implementation of the Moreover, poor estimates at time will degrade the prediction WPA estimator (42). The nuisance parameter is generated ranquality in the next step at time where the unwrapping domly within the interval . In accordance with [12] that interval for the motivation of using the WPA estimator is to avoid phase unis formulated (very poor estimates can even cause phase unwrapping, it is assumed here that the condition (34) is satisfied Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

Fig. 7 gives the comparison of the inverse MSE between the AOPN models for a particular sample value of with and for the LMMSE implementation of the WPA estimator (42). The nuisance parameter is generated randomly within the interval . In accordance with [12] that the motivation of using the WPA estimator is to avoid phase unwrapping, it is assumed here that the condition (34) is satisfied 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3186 



Fig. 5. Performance comparison of the LMMSE estimator for different AOPN models with Algorithm 1 for phase unwrapping. 



Fig. 6. Performance comparison of phase unwrapping Algorithm 1 and Algorithm 2 for the LMMSE estimator. 

for all . We see from Fig. 7 that at high SNR, the WPA to the lowest estimation threshold SNR. For example, its estiestimator for all AOPN models can attain the CRLB. As SNR mation threshold SNR is about 6.6 dB for . In compardecreases, however, the exact _a posteriori_ model is seen to lead ison with the WPA with Tretter’s model, the threshold SNR gain Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

FU AND KAM: PHASE-BASED, TIME-DOMAIN ESTIMATION OF THE FREQUENCY AND PHASE OF A SINGLE SINUSOID 

3187 



<!-- Start of picture text -->
and .<br><!-- End of picture text -->

Fig. 7. Performance comparison of the WPA estimators with the various AOPN models for 



is about 2.0 dB. Again, the results also show that at low SNR, the best linearized model provides better estimation accuracy than the geometric model. As discussed in Section IV-D, the online information that the diagonal elements of the matrix for the models (9), (20), and (21) depend on the received signal magnitudes and can indicate to the WPA the exact positions of the data samples that are less reliable, and one can improve the performance by selectively dropping the most noisy samples from the averaging process. The result is shown in Fig. 8 where the best linearized model is assumed. The performance of Tretter’s model is given for a comparison. A block of observations are obtained and the corresponding quantities which are proportional to the diagonal elements of in (44) are computed. The WPA estimator (42) is then implemented by using only 19, 17, and 15 components of after dropping one, three, and five samples of associated with the largest values of , respectively. From Fig. 8, we see that by dropping the data samples that are most perturbed by bad noise, the WPA with the best linearized model can lead to further performance improvement over that with Tretter’s model at low SNR. For instance, for , the SNR gain is up to 1.0 dB by dropping the three most noisy samples. As the SNR decreases, it can perform increasingly better than the WPA with Tretter’s model by dropping more and more noisy data samples. This suggests that if the _a priori_ information on the operating SNR region of the estimator is available, we can make use of Fig. 8 to specify the number of most noisy samples to drop to achieve the maximum performance gain. It can be verified that the summation of the weighting coefficients in is always equal to 1. To improve the performance, solutions must be sought to optimize the coefficients in such a way that the input from noisy samples is suppressed and that from the less noisy samples is increased, while the constraint 

Fig. 8. Performance comparison of the WPA estimator by dropping data samples with best linearized model for . 

on the unit sum remains satisfied. We can view the distribution of these coefficients as a weighting spectrum. The spectrum in [12, Fig. 1] is independent of the noise, whereas the spectra for the models (9), (20), and (21) can be adjusted through their dependence on the instantaneous noise samples, and one expects that the adjustment can help optimize the spectrum in the way as mentioned. The averaging nature of the WPA is such that the adjustment on the spectrum brought about by the different AOPN models should be as significant as possible. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 59, NO. 5, MAY 2013 

3188 

## REFERENCES 

- [1] D. C. Rife and R. R. Boorstyn, “Single-tone parameter estimation from discrete-time observations,” _IEEE Trans. Inf. Theory_ , vol. IT-20, no. 5, pp. 591–598, Sep. 1974. 

- [2] L. C. Palmer, “Coarse frequency estimation using the discrete Fourier transform,” _IEEE Trans. Inf. Theory_ , vol. IT-20, no. 1, pp. 104–109, Jan. 1974. 

- [3] Y. V. Zakharov, V. M. Baronkin, and T. C. Tozer, “DFT-based frequency estimators with narrow acquisition range,” in _Proc. Inst. Elect. Eng. Commun._ , 2001, vol. 148, pp. 1–7. 

- [4] S. Reisenfeld and E. Aboutanios, “A new algorithm for the estimation of the frequency of a complex exponential in additive Gaussian noise,” _IEEE Commun. Lett._ , vol. 7, no. 11, pp. 549–551, Nov. 2003. 

- [5] E. Aboutanios and B. Mulgrew, “Iterative frequency estimation by interpolation on Fourier coefficients,” _IEEE Trans. Signal Process._ , vol. 53, no. 4, pp. 1237–1242, Apr. 2005. 

- [6] E. Jacobsen and P. Kootsookos, “Fast, accurate frequency estimators,” _IEEE Signal Process. Mag._ , vol. 24, no. 3, pp. 123–125, May 2007. 

- [7] S. Provencher, “Estimation of complex single-tone parameter in the DFT domain,” _IEEE Trans. Signal Process._ , vol. 58, no. 7, pp. 3879–3883, Jul. 2010. 

- [8] C. Candan, “A method for fine resolution frequency estimation from three DFT samples,” _IEEE Signal Process. Lett._ , vol. 18, no. 6, pp. 351–354, Jun. 2011. 

- [9] S. A. Tretter, “Estimating the frequency of a noisy sinusoid by linear regression,” _IEEE Trans. Inf. Theory_ , vol. IT-31, no. 6, pp. 832–835, Nov. 1985. 

- [10] H. Fu and P. Y. Kam, “ML estimation of the frequency and phase in noise,” presented at the IEEE Global Telecommun. Conf., San Francisco, CA, USA, Nov. 2006, SPC09-2. 

- [11] H. Fu and P. Y. Kam, “MAP/ML estimation of the frequency and phase of a single sinusoid in noise,” _IEEE Trans. Signal Process._ , vol. 55, no. 3, pp. 834–845, Mar. 2007. 

- [12] S. Kay, “A fast and accurate single frequency estimator,” _IEEE Trans. Acoust., Speech, Signal Process._ , vol. 37, no. 12, pp. 1987–1990, Dec. 1989. 

- [13] H. Fu and P. Y. Kam, “Linear estimation of the frequency and phase of a noisy sinusoid,” in _Proc. IEEE Veh. Technol. Conf._ , Singapore, May 2008, pp. 1727–1731. 

- [24] H. Fu and P. Y. Kam, “Exact phase noise model for single-tone frequency estimation in noise,” _IET Electron. Lett._ , vol. 44, no. 15, pp. 937–938, Jul. 2008. 

- [25] J. M. Tribolet, “A new phase unwrapping algorithm,” _IEEE Trans. Acoust., Speech, Signal Process._ , vol. 25, no. 2, pp. 170–177, Apr. 1977. 

- [26] K. Steiglitz and B. Dickinson, “Phase unwrapping by factorization,” _IEEE Trans. Acoust., Speech, Signal Process._ , vol. 30, no. 6, pp. 984–991, Dec. 1982. 

- [27] H. L. Van Trees _, Detection, Estimation, and Modulation Theory: Part I_ . New York, NY, USA: Wiley, 1968. 

- [28] A. J. Viterbi _, Principles of Coherent Communication_ . New York, NY, USA: McGraw-Hill, 1966. 

- [29] M. K. Simon, S. M. Hinedi, and W. C. Lindsey _, Digital Communication Techniques_ . New York, NY, USA: Prentice-Hall, 1995. 

- [30] T. H. Lee and A. Hajimiri, “Oscillator phase noise: A tutorial,” _IEEE J. Solid-State Circuits_ , vol. 35, no. 3, pp. 326–336, Mar. 2000. 

- [31] H. Leib and S. Pasupathy, “The phase of a vector perturbed by Gaussian noise and differentially coherent receivers,” _IEEE Trans. Inf. Theory_ , vol. IT-34, no. 6, pp. 1491–1501, Sep. 1988. 

- [32] T. M. Cover and J. A. Thomas _, Elements of Information Theory_ . Hoboken, NJ, USA: Wiley, 2006. 

- [33] T. Routtenberg and J. Tabrikian, “Periodic CRB for non-Bayesian parameter estimation,” in _Proc. IEEE Int. Conf. Acoust., Speech Signal Process._ , May 2011, pp. 2448–2451. 

- [34] S. Basu and Y. Bresler, “A global lower bound on parameter estimation with periodic distortion functions,” _IEEE Trans. Inf. Theory_ , vol. 46, no. 3, pp. 1145–1150, May 2000. 

- [35] H. L. Van Trees and K. L. Bell _, Bayesian Bounds for Parameter Estimation and Nonlinear Filtering/Tracking_ . New York, NY, USA: Wiley, 2007. 

**Hua Fu** is with the Department of Electrical and Computer Engineering, National University of Singapore. His research interests include communication theory, wireless communication, detection, estimation and statistical signal processing in communication and radar, antenna array processing and 3GPP/3GPP2 CDMA wireless networks. 

- [14] B. C. Lovell and R. C. Williamson, “The statistical performance of some instantaneous frequency estimators,” _IEEE Trans. Signal Process._ , vol. 40, no. 7, pp. 1708–1723, Jul. 1992. 

- [15] M. P. Fitz, “Further results in the fast estimation of a single frequency,” _IEEE Trans. Commun._ , vol. 42, no. 234, pp. 862–864, Feb. 1994. 

- [16] M. Luise and R. Reggiannini, “Carrier frequency recovery in all-digital modems for burst-mode transmissions,” _IEEE Trans. Commun._ , vol. 43, no. 234, pp. 1169–1178, Feb.–Mar.–Apr. 1995. 

- [17] V. Clarkson, P. J. Kootsookos, and B. G. Quinn, “A analysis of the variance threshold of Kay’s weighted linear predictor frequency estimator,” _IEEE Trans. Signal Process._ , vol. 42, no. 9, pp. 2370–2379, Sep. 1994. 

- [18] P. Handel, “On the performance of the weighted linear predictor frequency estimator,” _IEEE Trans. Signal Process._ , vol. 43, no. 12, pp. 3070–3071, Dec. 1995. 

- [19] D. Kim, M. J. Narasimha, and D. C. Cox, “An improved single frequency estimator,” _IEEE Signal Process. Lett._ , vol. 3, no. 7, pp. 212–214, Jul. 1996. 

- [20] M. L. Fowler and J. A. Johnson, “Extending the threshold and frequency range for phase-based frequency estimation,” _IEEE Trans. Signal Process._ , vol. 47, no. 10, pp. 2857–2863, Oct. 1999. 

- [21] Z. Zhang, A. Jakobsson, M. D. Macleod, and J. A. Chambers, “A hybrid phase-based single frequency estimator,” _IEEE Signal Process. Lett._ , vol. 12, no. 9, pp. 657–660, Sep. 2005. 

- [22] H. Fu and P. Y. Kam, “Improved weighted phase averager for frequency estimation of single sinusoid in noise,” _IET Electron. Lett._ , vol. 44, no. 3, pp. 247–248, Jan. 2008. 

- [23] A. B. Awoseyila, C. Kasparis, and B. G. Evans, “Improved single frequency estimation with wide acquisition range,” _IET Electron. Lett._ , vol. 44, no. 3, pp. 245–247, Jan. 2008. 

**Pooi-Yuen Kam** (F’10) was born in Ipoh, Malaysia, and educated at the Massachusetts Institute of Technology, Cambridge, Mass., USA where he obtained the S. B., S. M., and Ph. D. degrees in electrical engineering in 1972, 1973, and 1976, respectively. 

From 1976 to 1978, he was a member of the technical staff at the Bell Telephone Laboratories, Holmdel, N. J., USA, where he was engaged in packet network studies. Since 1978, he has been with the Department of Electrical and Computer Engineering, National University of Singapore, where he is now a professor. He served as the Deputy Dean of Engineering and the Vice Dean for Academic Affairs, Faculty of Engineering of the National University of Singapore, from 2000 to 2003. His research interests are in the communication sciences and information theory, and their applications to wireless and optical communications. He spent the sabbatical year 1987 to 1988 at the Tokyo Institute of Technology, Tokyo, Japan, under the sponsorship of the Hitachi Scholarship Foundation. In year 2006, he was invited to the School of Engineering Science, Simon Fraser University, Burnaby, B.C., Canada, as the David Bested Fellow. 

Dr. Kam is a member of Eta Kappa Nu, Tau Beta Pi, and Sigma Xi. Since September 2011, he is a senior editor of the IEEE WIRELESS COMMUNICATIONS LETTERS. From 1996 to 2011, he served as the Editor for Modulation and Detection for Wireless Systems of the IEEE TRANSACTIONS ON COMMUNICATIONS. He also served on the editorial board of PHYCOM, the Journal of Physical Communications of Elsevier, from 2007 to 2012. He was elected a Fellow of the IEEE for his contributions to receiver design and performance analysis for wireless communications. He received the Best Paper Award at the IEEE VTC2004Fall, at the IEEE VTC2011-Spring, and at the IEEE ICC2011. 

Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on August 12,2026 at 03:35:47 UTC from IEEE Xplore.  Restrictions apply. 


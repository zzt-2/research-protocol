% ----------------------------- Description ----------------------------- %
% GB 2312 Encode
% Author:			Robin Hu
% 
% Create Date:		2023/05/16   20:09:49
% File Name:		Tx2Rx.m 
% Description:		收发一体
% 发送：信息生成 --> CRC16 --> LDPC --> 加扰 --> 加帧头 --> 符号映射 --> 量化 --> 成型 --> 发送
% 接收：匹配滤波 --> 定时同步 --> 均衡 --> 载波同步 --> 解映射 --> 帧同步(解相位模糊)
% ----------------------------------------------------------------------- %
close all
clear
clc


load('mat/ccsds_matrix.mat');
BitLen		= 7136;
ByteLen		= BitLen/8;
VaildPad	= ones(1, 16);
UnVaildPad	= 0*ones(1, 16);
Hexpadding	= "5A";
Vaild		= 0;
if(Vaild)
	BinData	= [VaildPad, randi([0, 1], 1, BitLen-16*2)];
else
	BinData	= [UnVaildPad, [repmat(de2bi(hex2dec(Hexpadding), 'left-msb', 8), 1, ByteLen-16/8*2)]];
end

% ---------------------------------- CRC16校验 --------------------------------- %
% g(x) = x^16 + x^15 + x^2 + 1
RegIni				= 1*ones(1, 16);
LenCRC				= length(BinData) + 16;
[CrcBin, CRCout]	= CRC16_0x1021(BinData, LenCRC, RegIni);

% ---------------------------------- LDPC编码 ---------------------------------- %
FrmBin			= [zeros(1, 18), CrcBin];
FrmBinEncode	= mod(FrmBin * G , 2);			% 编码结果
FrmBinEncode	= [FrmBinEncode(19:end), 0, 0];	% 丢掉前面18'd0，后面补2'd0
CheckCodeBin	= FrmBinEncode(end-1021:end);	% 校验位
CheckCodeHex	= dec2hex(bi2de(reshape([CheckCodeBin, 0, 0], 32, [])', 'left-msb'));

% ------------------------------------ 加扰 ------------------------------------ %
% 产生加扰序列 g(x) = x^15 + x^14 + 1
ShiftReg	= [1 0 0 1 0 1 0 1 0 0 0 0 0 0 0];
LenPN		= length(FrmBinEncode);
PnMsg		= zeros(1, LenPN);		% 产生 LenPN 长度的加扰移位数据
for k=1:LenPN
	PnMsg(k)	= xor(ShiftReg(14), ShiftReg(15));
	ShiftReg	= [PnMsg(k) ShiftReg(1:14)];
end

ScrBin			= double(xor(FrmBinEncode, PnMsg));
% ScrDec			= bi2de(reshape(ScrBin, 32, [])', 'left-msb');
% ScrHex			= lower([dec2hex(ScrDec), 10*ones(249, 1)]);


% ------------------------------------ 加帧头 ----------------------------------- %
FrmHead	= de2bi(hex2dec("1ACFFC1D"), 'left-msb', 32);
FrmUnip	= [FrmHead, ScrBin];	% 8192bit/帧
FrmBin	= FrmUnip;
save mat/FrmBin.mat FrmBin
FrmHex	= dec2hex(bi2de(reshape(FrmUnip, 32, [])', 'left-msb'));
LenFrm	= length(FrmUnip);
FrmBip	= 1 - 2*FrmUnip;									% 01映射
FrmNum	= 140;
FrmRep	= repmat(FrmUnip, 1, FrmNum);

% % ----------------------------------- 存一帧数据 ---------------------------------- %
% fid			= fopen('coe\Frame32bit.coe', 'wt');
% fprintf(fid, '%s\n', 'memory_initialization_radix	= 16;');
% fprintf(fid, '%s\n', 'memory_initialization_vector	=');
% FrmHexCoe	= [FrmHex, 10*ones(length(FrmHex), 1)];
% fprintf(fid, '%s', FrmHexCoe');
% fclose(fid);

% ----------------------------------- 星座映射 ----------------------------------- %
M				= 2^4;		% 星座图点数
alpha			= log2(M);	% bit/符号
ConstPlot		= 0;		% 是否画星座图
Mess			= bi2de(reshape(FrmRep, alpha, [])', 'left-msb');
MessMod			= ModCh(M, Mess, ConstPlot);	% 调制
scatterplot(MessMod);title('16APSK')
% ------------------------------------- 量化 ------------------------------------- %
QuantN			= 14;
MessModQuant	= MessMod * (2^(QuantN-1)-1);
% scatterplot(MessModQuant);title('量化数据')
% figure;plot(real(MessModQuant(1:10)));

% ------------------------------------ 成型 ------------------------------------ %
FsTx			= 8e9;
Rs				= 2e9;
OverSampleRate	= FsTx/Rs;	% 过采样倍数
span			= 4;		% 截断的符号范围 2^n 效果会较好
ShapCoe			= 0.25;		% 成型滤波器滚降系数
RcosFilterTx	= rcosdesign(ShapCoe, span, OverSampleRate, 'sqrt');
RcosFilterTx2	= [32, -32, -64, 128, 128, -256, -128, 1024, 2048, 1024, -128, -256, 128, 128, -64, -32, 32];	% 进行2^n近似/截断一点后性能没有明显下降或变化，但可以简化运算节约资源
RcosFilterTx4	= [32, 16, -32, -96, -64, 16, 128, 192, 128, -128, -256, -512, -128, 512, 1024, 1526, 2048, 1536, 1024, 512, -128, -512, -256, -128, 128, 192, 128, 16, -64, -96, -32, 16, 32];
if(OverSampleRate==2)	RcosFilterTx	= RcosFilterTx2;
else					RcosFilterTx	= RcosFilterTx4;
end
ShapSig			= conv(upsample(MessModQuant, OverSampleRate), RcosFilterTx, 'same');	% 成型滤波后的信号
% scatterplot(ShapSig);title('成型数据')
scatterplot(downsample(ShapSig, OverSampleRate, 0));title('成型数据')

% % ----------------------------------- 存ROM ----------------------------------- %
% DataLen			= 16*256*1;
% DataRom			= floor(ShapSig(1:DataLen));
% DataRomI		= real(DataRom)*2;
% DataRomQ		= imag(DataRom)*2;
% figure
% plot(DataRomI);hold on;plot(DataRomQ);hold on
% DataRomI(DataRomI<0)	= DataRomI(DataRomI<0) + 2^16;
% DataRomQ(DataRomQ<0)	= DataRomQ(DataRomQ<0) + 2^16;
% DataRomI1		= DataRomI;
% DataRomQ1		= DataRomQ;
% DataRomI1(DataRomI1>2^15)	= DataRomI1(DataRomI1>2^15) - 2^16;
% DataRomQ1(DataRomQ1>2^15)	= DataRomQ1(DataRomQ1>2^15) - 2^16;
% plot(repmat(DataRomI1, [10,1]));hold on;plot(repmat(DataRomQ1, [10,1]));legend('I', 'Q', 'I1', 'Q1')
% scatterplot(downsample(DataRomI1+1j*DataRomQ1, OverSampleRate, 0));title('成型数据')
% % HexRomI			= dec2hex(DataRomI);
% % HexRomQ			= dec2hex(DataRomQ);
% % HexRomI			= reshape(HexRomI', 4*16, [])';
% % HexRomQ			= reshape(HexRomQ', 4*16, [])';
% % HexRomIQ		= [HexRomI, HexRomQ, 10*ones(length(HexRomI), 1)];
% % switch(alpha)
% % 	case 2;	FileNameP0 = 'QP';
% % 	case 3;	FileNameP0 = 'D8P';
% % 	case 4;	FileNameP0 = 'D12AP';
% % 	case 5;	FileNameP0 = 'D32AP';
% % end
% % % FileNameP0		= 'coe\D32AP4G.coe';
% % FileName	= ['F:/PSKProject/PskSend216/Top.srcs/sources_1/CoeFile/', FileNameP0, num2str(Rs/1e9), 'G.coe'];
% % fid			= fopen(FileName, 'wt');
% % fprintf(fid, '%s\n', 'memory_initialization_radix	= 16;');
% % fprintf(fid, '%s\n', 'memory_initialization_vector	=');
% % fprintf(fid, '%s', HexRomIQ');
% % fclose(fid);

% ------------------------------------ 加噪 ------------------------------------ %
EbN0			= 55;						% 环路信噪比 单位：dB
% if(OverSampleRate==4);	EbN0	= EbN0 + 3;
% end
Rb				= Rs*alpha;					% 信息速率
B				= FsTx/2;					% 噪声带宽、信号带宽
SNR				= EbN0 + 10*log10(Rb/B);	% SNR = (Es*Rs)/(N0*B) = (Eb*alpha*Rs)/(N0*B)=Eb/N0*Rb/B
ShapSig			= awgn(ShapSig, SNR, 'measured');

% ------------------------------------ FFT ----------------------------------- %
fft1			= abs(fft(ShapSig));
LenFFT			= length(fft1);
figure;plot((-LenFFT/2:LenFFT/2-1)/LenFFT*FsTx, fftshift(fft1));title('成型频谱');xlabel('频率/Hz');ylabel('幅度')

% ----------------------------------- 加载波频偏 ---------------------------------- %
Fbias			= 1e6*1;
CarrySig		= ShapSig .* exp(1j*2*pi*(1:LenFFT)'/FsTx*Fbias + 2*pi*rand(1));
% CarrySig		= ShapSig;
% scatterplot(CarrySig);title('载波频偏数据')

% ----------------------------------- 采样率转换 ---------------------------------- %
FsRx1			= 5e9;	% AD采样率
RxSig1			= resample(CarrySig, FsRx1, FsTx);	% 多相滤波等效采样率	加时钟偏斜造成的定时误差
RxSig1			= resample(RxSig1, 40001, 40000);
FsRx2			= 4*Rs;	% 统一为4倍过采样
RxSig2			= resample(RxSig1, FsRx2, FsRx1);

% ----------------------------------- 匹配滤波 ----------------------------------- %
% MatchSig		= conv(ShapSig, RcosFilterTx, 'same');
RcosFilterRx	= rcosdesign(ShapCoe, span, floor(FsRx2/Rs), 'sqrt');
% RcosFilterRx	= rcosdesign(ShapCoe, span, 4, 'sqrt');

MatchSig		= conv(RxSig2, RcosFilterTx4, 'same');
% scatterplot(MatchSig);title('多相滤波')

% ------------------------------------------------------------------------------- %
%                                     定时同步                                     %
% ------------------------------------------------------------------------------- %
C1			= 1/2^5;
C2			= C1^2/2;
Amp			= max(abs(MatchSig));
DinInt		= downsample(MatchSig/Amp, 1);	% 行向量
Len1		= length(DinInt);
UpsampR		= FsRx2/Rs;			% 过采样倍数
eta			= zeros(Len1, 1);	% NCO输出
omega		= zeros(Len1, 1);	% NCO控制字
omega(1:2)	= 1/UpsampR;
eck			= zeros(Len1, 1);	% 定时误差
eckloop		= zeros(Len1, 1);	% 定时误差
muk			= zeros(Len1, 1);	% 最佳采样点位置 (0:1)
mk			= 0;
InterOne	= zeros(Len1, 1);	% 内插最佳采样点
InterHalf	= zeros(Len1, 1);	% 内插最佳采样点中间点
for n = 2: Len1-4*2
	eta(n+1)	= eta(n) - omega(n);
	if(eta(n+1) < 0)
		mk				= mk + 1;
		eta(n+1)		= eta(n+1) + 1;
		muk(n+1)		= eta(n)*UpsampR;
		InterOne(mk)	= InterpCubic(muk(n+1), DinInt(n-1: n+2));
		InterHalf(mk)	= InterpCubic(muk(n+1), DinInt(n+1: n+4));
		InterOne(mk+1)	= InterpCubic(muk(n+1), DinInt(n+3: n+6));
		eck(mk)			= PSKTimingErrDetector(InterOne(mk), InterHalf(mk), InterOne(mk+1));
		% 环路滤波器
		if (mk > 1)
			omega(n + 1) = (C1 + C2) * eck(mk) - C1 * eck(mk-1) + omega(n);
			eckloop(n+1) = (C1 + C2) * eck(mk) - C1 * eck(mk-1);
		else
			omega(n + 1) = (C1 + C2) * eck(mk)  + omega(n);
		end
	else
		omega(n + 1)	= omega(n);
		eckloop(n + 1)	= eckloop(n);
		muk(n + 1)		= muk(n);
	end
end
DoutInt	= InterOne(1:mk);
figure;
subplot(3,1,1);plot(muk(1:mk), 'b', 'LineWidth', 1);title('\mu_k');
subplot(3,1,2);plot(eck(1:mk), 'b', 'LineWidth', 1);title('eck');
subplot(3,1,3);plot(omega(1:mk), 'b', 'LineWidth', 1);title('\omega');
scatterplot(DoutInt(end/2:end), 1, 1, 'y.');title('定时同步');


% ------------------------------------ 加多径 ----------------------------------- %
DoutInt = DoutInt(end/4:end);
DoutMP	= DoutInt' + 0.5*circshift(DoutInt', 1);
% scatterplot(DoutMP);title('加多径')

% ------------------------------------------------------------------------------ %
%                                      均衡                                      %
% ------------------------------------------------------------------------------ %
L			= 20;	% 均衡器长度M=2*L+1
mu			= 4e-3;
R			= 1;
Amp1		= max(abs(DoutMP));
EqM			= 2*L;	% 实际均衡器长度等于M=2*L+1 
K			= length(DoutMP)-EqM+1;
uk			= zeros(EqM,K);
w			= [zeros(L,1);1;zeros(L-1,1)];
DoutEq		= zeros(1,K);
R			= 1;
DinCMA		= DoutMP/Amp1;	% 幅度归一化
e			= [];
w_detect	= [];
for k = 1:K
	uk(:,k)		= DinCMA(k:k+EqM-1);
	DoutEq(k)	= w'*uk(:,k);
	if(M==16)
		% if(abs(DoutEq(k))^2>((1/2.7)^2+1)/2)	% 半径阈值要小于中间值
		if(abs(DoutEq(k))^2>0.4)
			e(k) = DoutEq(k)*(1-abs(DoutEq(k))^2);
		else
			e(k) = DoutEq(k)*((1/2.7)^2-abs(DoutEq(k))^2);
		end
	elseif(M==32)
		% if(abs(DoutEq(k))^2>((2.6/4.6)^2+1)/2)
		if(abs(DoutEq(k))^2>0.5)
			e(k) = DoutEq(k)*(1-abs(DoutEq(k))^2);
		elseif(abs(DoutEq(k))^2>((1/4.6)^2+(2.6/4.6)^2)/2)
			e(k) = DoutEq(k)*((2.6/4.6)^2-abs(DoutEq(k))^2);
		else
			e(k) = DoutEq(k)*((1/4.6)^2-abs(DoutEq(k))^2);
		end
	else	% PSK 衡模
		e(k)	= DoutEq(k)*(R-abs(DoutEq(k))^2);
	end
	w			= w+mu*conj(e(k))*uk(:,k);
	w_detect(k)	= w(L+1,1);
end
figure;
subplot(2,1,1);plot(real(e));title('误差收敛曲线')
subplot(2,1,2);plot(real(w_detect));title('系数收敛曲线')
scatterplot(DoutEq(1*end/2:end));title('\fontsize{14} CMA 均衡后');


%%----------------载波同步------------------------------------------------------------------------
C1				= 1/2^7;
C2				= C1^2/2; 
C1_1			= C1/4;
C2_1			= C2/4;
Signal_Noise	= DoutEq/max(abs(DoutEq(end/2:end)));
N				= length(Signal_Noise);
Theta_M_Noisy	= zeros(1,N);


% %% 定义每一轮仿真的中间结果：
Theta_Out_1		= zeros(1,N);	% 锁相环1的输出相位。
PD_Out_1		= zeros(1,N);	% 锁相环1的鉴相器输出。
NCO_StepUp_1	= zeros(1,N);	% 锁相环1的NCO步进量（单位是弧度每采样点）。
%% PLL仿真
for n = 2:N
	% PLL1
	Theta_M_Noisy(n)	= atan2(imag(Signal_Noise(n)),real(Signal_Noise(n)));
	Theta_Out_1(n)		= mod(Theta_Out_1(n-1)+NCO_StepUp_1(n-1),2*pi);   
	
	%鉴相器（PhaseDetector_Quad）
	SampR = real(Signal_Noise(n)).^2+imag(Signal_Noise(n)).^2;
	if(M<16 || (SampR<=0.5 && M==16) || (SampR<=0.2 && M==32))  % 三个半径分别是0.14/1
		theta_e	= mod((Theta_M_Noisy(n)-Theta_Out_1(n)-pi/4)*4, 2*pi);
		if (theta_e>pi)
			PD_Out_1(n) = theta_e - 2*pi;
		else
			PD_Out_1(n) = theta_e;
		end

	else
		PD_Out_1(n) = PD_Out_1(n);
	end
	
	%环路滤波器（LoopFLT_v2）
	NCO_StepUp_1(n)	= (C1_1+C2_1)*PD_Out_1(n)-C1_1*PD_Out_1(n-1)+NCO_StepUp_1(n-1);
	NCO_StepUp_1(n)	= mod(NCO_StepUp_1(n),2*pi);
	if (NCO_StepUp_1(n)>pi)
		NCO_StepUp_1(n) = NCO_StepUp_1(n)-2*pi;
	end
	
end 
PLL_Out	= Signal_Noise(1:N).*exp(1j*(-Theta_Out_1(1:N)));
Carry	= exp(1j*(-Theta_Out_1(1:N)));
figure;plot(real(Carry));title('恢复载波')
scatterplot(PLL_Out(3*end/4:end));title('\fontsize{14} 载波同步')

% ------------------------------------ 解映射 ----------------------------------- %
SyncSig			= PLL_Out(end/4*3:end).*exp(1j*pi/4*6);
SyncSig			= SyncSig/max(abs(SyncSig));	% 归一化幅度
DemodSig		= DemodCh(SyncSig, M);
DemodBin		= reshape(de2bi(DemodSig, 'left-msb')', 1, []);
DemodBip		= 1 - 2*DemodBin;
DemodBip		= DemodBip(2/4*end:end);

% -------------------------------- 生成不同相位旋转的帧头 ------------------------------- %
HeadData_IQ			= MessMod(1:ceil(32/alpha));
HeadData_QI			= imag(HeadData_IQ) + 1j*real(HeadData_IQ);
if(M~=8)	% 除8PSK外其余均有4种相位模糊，不考虑IQ交错
	% ------------------------------------ IQ ------------------------------------ %
	HeadData_IQ0	= HeadData_IQ;
	HeadData_IQ1	= HeadData_IQ.*exp(1j*pi/2);
	HeadData_IQ2	= HeadData_IQ.*exp(1j*pi*2/2);
	HeadData_IQ3	= HeadData_IQ.*exp(1j*pi*3/2);

	Head_IQ0	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ0, M), 'left-msb', log2(M))', 1, []);
	Head_IQ1	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ1, M), 'left-msb', log2(M))', 1, []);
	Head_IQ2	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ2, M), 'left-msb', log2(M))', 1, []);
	Head_IQ3	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ3, M), 'left-msb', log2(M))', 1, []);

	Corr_IQ0	= conv(DemodBip, fliplr(Head_IQ0));
	Corr_IQ1	= conv(DemodBip, fliplr(Head_IQ1));
	Corr_IQ2	= conv(DemodBip, fliplr(Head_IQ2));
	Corr_IQ3	= conv(DemodBip, fliplr(Head_IQ3));

	% ------------------------------------ QI ------------------------------------ %
	HeadData_QI0	= HeadData_QI;
	HeadData_QI1	= HeadData_QI.*exp(1j*pi/2);
	HeadData_QI2	= HeadData_QI.*exp(1j*pi*2/2);
	HeadData_QI3	= HeadData_QI.*exp(1j*pi*3/2);

	Head_QI0	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI0, M), 'left-msb', log2(M))', 1, []);
	Head_QI1	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI1, M), 'left-msb', log2(M))', 1, []);
	Head_QI2	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI2, M), 'left-msb', log2(M))', 1, []);
	Head_QI3	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI3, M), 'left-msb', log2(M))', 1, []);

	Corr_QI0	= conv(DemodBip, fliplr(Head_QI0));
	Corr_QI1	= conv(DemodBip, fliplr(Head_QI1));
	Corr_QI2	= conv(DemodBip, fliplr(Head_QI2));
	Corr_QI3	= conv(DemodBip, fliplr(Head_QI3));
	figure;
	subplot(4,2,1);plot(Corr_IQ0);title('帧头相关-IQ-0相位')
	subplot(4,2,3);plot(Corr_IQ1);title('帧头相关-IQ-pi/2相位')
	subplot(4,2,5);plot(Corr_IQ2);title('帧头相关-IQ-pi相位')
	subplot(4,2,7);plot(Corr_IQ3);title('帧头相关-IQ-3pi/2相位')
	subplot(4,2,2);plot(Corr_QI0);title('帧头相关-QI-0相位')
	subplot(4,2,4);plot(Corr_QI1);title('帧头相关-QI-pi/2相位')
	subplot(4,2,6);plot(Corr_QI2);title('帧头相关-QI-pi相位')
	subplot(4,2,8);plot(Corr_QI3);title('帧头相关-QI-3pi/2相位')

	% ----------------------------------- 纠相位模糊 ---------------------------------- %
	[MaxVal, MaxIdx]	= max([max(Corr_IQ0), max(Corr_IQ1), max(Corr_IQ2), max(Corr_IQ3), max(Corr_QI0), max(Corr_QI1), max(Corr_QI2), max(Corr_QI3)]);
	switch MaxIdx
		case 1;	RxSig	= SyncSig;
		case 2;	RxSig	= SyncSig .* exp(-1j*pi/2*1);
		case 3;	RxSig	= SyncSig .* exp(-1j*pi/2*2);
		case 4;	RxSig	= SyncSig .* exp(-1j*pi/2*3);
		case 5;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig));
		case 6;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/2*1);
		case 7;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/2*2);
		case 8;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/2*3);
	end
	RxDemodSig			= DemodCh(RxSig, M);
	RxDemodBin			= reshape(de2bi(RxDemodSig, 'left-msb')', 1, []);
	RxDemodBip			= 1 - 2*RxDemodBin;
	CorrIQ				= conv(RxDemodBip, fliplr(Head_IQ0));
	[CorrVal, CorrIdx]	= max(CorrIQ);
	Pos					= CorrIdx(1) - length(Head_IQ0) + 1;
	figure
	plot(CorrIQ);title('帧头相关-相位补偿后')

else
	% ------------------------------------ IQ ------------------------------------ %
	HeadData_IQ0	= HeadData_IQ;
	HeadData_IQ1	= HeadData_IQ.*exp(1j*pi/4);
	HeadData_IQ2	= HeadData_IQ.*exp(1j*pi*2/4);
	HeadData_IQ3	= HeadData_IQ.*exp(1j*pi*3/4);
	HeadData_IQ4	= HeadData_IQ.*exp(1j*pi*4/4);
	HeadData_IQ5	= HeadData_IQ.*exp(1j*pi*5/4);
	HeadData_IQ6	= HeadData_IQ.*exp(1j*pi*6/4);
	HeadData_IQ7	= HeadData_IQ.*exp(1j*pi*7/4);

	Head_IQ0	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ0, M), 'left-msb', log2(M))', 1, []);
	Head_IQ1	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ1, M), 'left-msb', log2(M))', 1, []);
	Head_IQ2	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ2, M), 'left-msb', log2(M))', 1, []);
	Head_IQ3	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ3, M), 'left-msb', log2(M))', 1, []);
	Head_IQ4	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ4, M), 'left-msb', log2(M))', 1, []);
	Head_IQ5	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ5, M), 'left-msb', log2(M))', 1, []);
	Head_IQ6	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ6, M), 'left-msb', log2(M))', 1, []);
	Head_IQ7	= 1 - 2*reshape(de2bi(DemodCh(HeadData_IQ7, M), 'left-msb', log2(M))', 1, []);

	Corr_IQ0	= conv(DemodBip, fliplr(Head_IQ0));
	Corr_IQ1	= conv(DemodBip, fliplr(Head_IQ1));
	Corr_IQ2	= conv(DemodBip, fliplr(Head_IQ2));
	Corr_IQ3	= conv(DemodBip, fliplr(Head_IQ3));
	Corr_IQ4	= conv(DemodBip, fliplr(Head_IQ4));
	Corr_IQ5	= conv(DemodBip, fliplr(Head_IQ5));
	Corr_IQ6	= conv(DemodBip, fliplr(Head_IQ6));
	Corr_IQ7	= conv(DemodBip, fliplr(Head_IQ7));

	% ------------------------------------ QI ------------------------------------ %
	HeadData_QI0	= HeadData_QI;
	HeadData_QI1	= HeadData_QI.*exp(1j*pi/4);
	HeadData_QI2	= HeadData_QI.*exp(1j*pi*2/4);
	HeadData_QI3	= HeadData_QI.*exp(1j*pi*3/4);
	HeadData_QI4	= HeadData_QI.*exp(1j*pi*4/4);
	HeadData_QI5	= HeadData_QI.*exp(1j*pi*5/4);
	HeadData_QI6	= HeadData_QI.*exp(1j*pi*6/4);
	HeadData_QI7	= HeadData_QI.*exp(1j*pi*7/4);

	Head_QI0	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI0, M), 'left-msb', log2(M))', 1, []);
	Head_QI1	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI1, M), 'left-msb', log2(M))', 1, []);
	Head_QI2	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI2, M), 'left-msb', log2(M))', 1, []);
	Head_QI3	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI3, M), 'left-msb', log2(M))', 1, []);
	Head_QI4	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI4, M), 'left-msb', log2(M))', 1, []);
	Head_QI5	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI5, M), 'left-msb', log2(M))', 1, []);
	Head_QI6	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI6, M), 'left-msb', log2(M))', 1, []);
	Head_QI7	= 1 - 2*reshape(de2bi(DemodCh(HeadData_QI7, M), 'left-msb', log2(M))', 1, []);

	Corr_QI0	= conv(DemodBip, fliplr(Head_QI0));
	Corr_QI1	= conv(DemodBip, fliplr(Head_QI1));
	Corr_QI2	= conv(DemodBip, fliplr(Head_QI2));
	Corr_QI3	= conv(DemodBip, fliplr(Head_QI3));
	Corr_QI4	= conv(DemodBip, fliplr(Head_QI4));
	Corr_QI5	= conv(DemodBip, fliplr(Head_QI5));
	Corr_QI6	= conv(DemodBip, fliplr(Head_QI6));
	Corr_QI7	= conv(DemodBip, fliplr(Head_QI7));
	figure;
	subplot(8,2,1); plot(Corr_IQ0);title('帧头相关-IQ-0相位')
	subplot(8,2,3); plot(Corr_IQ1);title('帧头相关-IQ-pi/4相位')
	subplot(8,2,5); plot(Corr_IQ2);title('帧头相关-IQ-2pi/4相位')
	subplot(8,2,7); plot(Corr_IQ3);title('帧头相关-IQ-3pi/4相位')
	subplot(8,2,9); plot(Corr_IQ4);title('帧头相关-IQ-4pi/4相位')
	subplot(8,2,11);plot(Corr_IQ5);title('帧头相关-IQ-5pi/4相位')
	subplot(8,2,13);plot(Corr_IQ6);title('帧头相关-IQ-6pi/4相位')
	subplot(8,2,15);plot(Corr_IQ7);title('帧头相关-IQ-7pi/4相位')
	subplot(8,2,2); plot(Corr_QI0);title('帧头相关-QI-0相位')
	subplot(8,2,4); plot(Corr_QI1);title('帧头相关-QI-pi/4相位')
	subplot(8,2,6); plot(Corr_QI2);title('帧头相关-QI-2pi/4相位')
	subplot(8,2,8); plot(Corr_QI3);title('帧头相关-QI-3pi/4相位')
	subplot(8,2,10);plot(Corr_QI4);title('帧头相关-QI-4pi/4相位')
	subplot(8,2,12);plot(Corr_QI5);title('帧头相关-QI-5pi/4相位')
	subplot(8,2,14);plot(Corr_QI6);title('帧头相关-QI-6pi/4相位')
	subplot(8,2,16);plot(Corr_QI7);title('帧头相关-QI-7pi/4相位')

	% ----------------------------------- 纠相位模糊 ---------------------------------- %
	[MaxVal, MaxIdx]	= max([max(Corr_IQ0), max(Corr_IQ1), max(Corr_IQ2), max(Corr_IQ3), max(Corr_IQ4), max(Corr_IQ5), max(Corr_IQ6), max(Corr_IQ7), max(Corr_QI0), max(Corr_QI1), max(Corr_QI2), max(Corr_QI3), max(Corr_QI4), max(Corr_QI5), max(Corr_QI6), max(Corr_QI7)]);
	switch MaxIdx
		case 1;		RxSig	= SyncSig;
		case 2;		RxSig	= SyncSig .* exp(-1j*pi/4*1);
		case 3;		RxSig	= SyncSig .* exp(-1j*pi/4*2);
		case 4;		RxSig	= SyncSig .* exp(-1j*pi/4*3);
		case 5;		RxSig	= SyncSig .* exp(-1j*pi/4*4);
		case 6;		RxSig	= SyncSig .* exp(-1j*pi/4*5);
		case 7;		RxSig	= SyncSig .* exp(-1j*pi/4*6);
		case 8;		RxSig	= SyncSig .* exp(-1j*pi/4*7);
		case 9;		RxSig	= (imag(SyncSig) + 1j*real(SyncSig));
		case 10;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*1);
		case 11;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*2);
		case 12;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*3);
		case 13;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*4);
		case 14;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*5);
		case 15;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*6);
		case 16;	RxSig	= (imag(SyncSig) + 1j*real(SyncSig)) .* exp(1j*pi/4*7);
	end
	RxDemodSig			= DemodCh(RxSig, M);
	RxDemodBin			= reshape(de2bi(RxDemodSig, 'left-msb')', 1, []);
	RxDemodBip			= 1 - 2*RxDemodBin;
	CorrIQ				= conv(RxDemodBip, fliplr(Head_IQ0));
	[CorrVal, CorrIdx]	= max(CorrIQ);
	Pos					= CorrIdx(1) - length(Head_IQ0) + 1;
	figure
	plot(CorrIQ);title('帧头相关-相位补偿后')
end

RxBin		= RxDemodBin(Pos: end);
FrmNumRx	= floor(length(RxBin)/LenFrm);
RxBin		= reshape(RxBin(1:FrmNumRx*LenFrm), LenFrm, [])';
BerNum		= biterr(RxBin, FrmUnip);
Ber			= mean(BerNum)/LenFrm;
disp(['总误bit数：', num2str(sum(BerNum)), newline, '误码率：', num2str(Ber, '%.5f')]);

% ----------------------------- Description ----------------------------- %
% GBK 2312 Encode
% Author:			Robin Hu
% 
% Create Date:		2022/05/06   14:31:30
% File Name:		ModCh.m 
% Project Name: 
% Tool versions:	Matlab
% Description:		调制方式选择
%
% Revision: 1.0
% ----------------------------------------------------------------------- %

function MessMod = ModCh(M, Mess, ConstPlot)

%% ************* Parameter Setting

% M 调制阶数
% span 截断的符号范围
% SymbolNum 符号数
% ShappingCoe 成型滤波器滚降系数
% OverSampleRate 过采样比率(均衡前的效果和过采样有关？)

% M					= 32;	% 星座图各圈点数分布
% ConstPlot			= 1;	% 是否画星座图
% span				= 16;	% 截断的符号范围
% SymbolNum			= 1e4;	% 符号数
% ShappingCoe		= 0.35;	% 成型滤波器滚降系数
% OverSampleRate	= 4;	% sample number of a symbol  过采样比率(均衡前的效果和过采样有关？)



% 调制方式选择
if(M<16)
	MessMod	= pskmod(Mess, M, pi/M);	% modOrder-APSK调制
elseif(M==16)
	radii	= [1 2.7]/2.7;	% 星座图半径
	MessMod	= apskmod(Mess, [4 12], radii);	% modOrder-APSK调制
elseif(M==32)
	radii	= [1 2.64 4.64]/4.64;		% 星座图半径，外中达最大欧氏距离，内中尽量接近外中的距离，使星座图尽量紧凑从而内点分配到的功率能尽量大
	phsoff	= [pi/4 pi/12 0];			% 各圈初始相位
	MessMod	= apskmod(Mess, [4 12 16], radii, phsoff);	% modOrder-APSK调制
end

if(ConstPlot==1)
	scatterplot(MessMod)
	title('调制星座图')
end
end
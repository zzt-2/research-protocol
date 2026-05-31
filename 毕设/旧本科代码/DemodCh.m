% ----------------------------- Description ----------------------------- %
% GBK 2312 Encode
% Author:			Robin Hu
% 
% Create Date:		2022/05/07   09:18:03
% File Name:		DemodCh.m 
% Project Name: 
% Tool versions:	Matlab
% Description:		Ω‚”≥…‰
%
% Revision: 1.0
% ----------------------------------------------------------------------- %

function MessDemod = DemodCh(Mess, M)
	if(M<16)
		MessDemod	= pskdemod(Mess, M, pi/M);
	elseif(M==16)
		radii		= [1 2.7]/2.7;		% ∞Îæ∂
		% radii		= [0.4138 1.1297];	% ∞Îæ∂
		MessDemod	= apskdemod(Mess, [4 12], radii);
	elseif(M==32)
		% radii		= [0.4 0.8 1.216];	% ∞Îæ∂
		radii		= [1 2.64 4.64]./4.64;	% ∞Îæ∂
		phsoff		= [pi/4 pi/12 0];	% œ‡Œª
		MessDemod	= apskdemod(Mess, [4 12 16], radii, phsoff);
	end
end

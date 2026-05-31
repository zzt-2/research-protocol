function x = PSKTimingErrDetector(S_tMinusT, S_tMinusHalfT, S_t, M)
	% 定时误差检测
	y		= [S_tMinusT,S_tMinusHalfT,S_t];
	y_Re	= real(y);
	y_Im	= imag(y);
	
	% if(M<16)	% PSK
	% 	x = y_Re(2)*(y_Re(3)-y_Re(1)) + ...
	% 		y_Im(2)*(y_Im(3)-y_Im(1));
	% else		% APSK
		x = (y_Re(2)-(y_Re(3)+y_Re(1))/2)*(y_Re(3)-y_Re(1)) + ...
			(y_Im(2)-(y_Im(3)+y_Im(1))/2)*(y_Im(3)-y_Im(1));
	% end
function x = InterpCubic(muup,InputVec)
% 立方内插
% muup：小数间隔，取值范围[0,1]，对Ts归一化。
% InputVec：用于内插的前后若干个数据，行向量。其长度为4，依次为：
%			X(mk-1)，X(mk)，X(mk+1)，X(mk+2)。
% InputVec中的第2个为基准点（即“X(mk)”）。
if(muup>1);	muup = 1; end
V_0	= 								InputVec(2);
V_1	= -1/3	*InputVec(1)	-1/2	*InputVec(2)	+		InputVec(3)		-1/6	*InputVec(4);
V_2	= 1/2	*InputVec(1)	-		InputVec(2)		+1/2	*InputVec(3);
V_3	= -1/6	*InputVec(1)	+1/2	*InputVec(2)	-1/2	*InputVec(3)	+1/6	*InputVec(4);

x	= V_3*muup^3 + V_2*muup^2 + V_1*muup + V_0;
% ----------------------------- Description ----------------------------- %
% GB 2312 Encode
% Author:			Robin Hu
% 
% Create Date:		2022/10/14   17:33:38
% File Name:		CRC16_0x1021.m 
% Description:		CRC校验
%
% 生成多项式： g(x) = x^16 + x^12 + x^5 + 1		1_0001_0000_0010_0001	0x1021
% 寄存器结构：
% 			↓-----------------------↓-------------------------------------------↓-------------------------------|
% 			g0						g5											g12								g16
% 			↓						↓											↓								↑(a)
% 			D0-->D1-->D2-->D3-->D4-->XOR-->D5-->D6-->D7-->D8-->D9-->D10-->D11-->XOR-->D12-->D13-->D14-->D15--->XOR<--{Din, 16'd0}
% ShiftReg	1--->2--->3--->4--->5--------->6--->7--->8--->9--->10-->11--->12--------->13--->14--->15--->16
% I 型结构需要数据末尾补 0，且末尾 16 个 0 输入时对应的输出为校验位
% II 型结构不需要补 0 ，数据全输入后移位寄存器的内容即为CRC校验数据	
% ----------------------------------------------------------------------- %
% Len为加上16bit校验后的数据长度
% RegIni为寄存器初值
function [Dout, CRCout] = CRC16_0x1021(Din, Len, RegIni)
	ShiftReg	= RegIni;
	Dout		= zeros(1, Len);
	for i = 1:Len
		if(i <= Len-16)	% Din	if 语句结束后将 ShiftReg 输出为II型结构
			XIn				= Din(i);
			Dout(i)			= XIn;
			a				= xor(ShiftReg(16), XIn);
			ShiftReg(14:16)	= ShiftReg(13:15);
			ShiftReg(13)	= xor(ShiftReg(12), a);
			ShiftReg(7:12)	= ShiftReg(6:11);
			ShiftReg(6)		= xor(ShiftReg(5), a);
			ShiftReg(2:5)	= ShiftReg(1:4);
			ShiftReg(1)		= a;
		else	% 16 个 0	补 0 再输出 ShiftReg 为I型结构
			Dout(i)			= ShiftReg(16);
			a				= 0;
			ShiftReg(14:16)	= ShiftReg(13:15);
			ShiftReg(13)	= xor(ShiftReg(12), a);
			ShiftReg(7:12)	= ShiftReg(6:11);
			ShiftReg(6)		= xor(ShiftReg(5), a);
			ShiftReg(2:5)	= ShiftReg(1:4);
			ShiftReg(1)		= a;
		end
	end
	CRCout	= dec2hex(bi2de(Dout(end-15:end), 'left-msb'), 4);
end
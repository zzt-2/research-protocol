% ----------------------------- Description ----------------------------- %
% GB 2312 Encode
% Author:			Robin Hu
% 
% Create Date:		2023/02/25   20:56:04
% File Name:		Gmatrix.m 
% Description:		通过循环移位子阵第一行得到生成矩阵
% 
% ----------------------------------------------------------------------- %
close all
clear
clc


HexB01_1	= char("55BF56CC55283DFEEFEA8C8CFF04E1EBD9067710988E25048D67525426939E2068D2DC6FCD2F822BEB6BD96C8A76F4932AAE9BC53AD20A2A9C86BB461E43759C");
HexB01_2	= char("6855AE08698A50AA3051768793DC238544AF3FE987391021AAF6383A6503409C3CE971A80B3ECE12363EE809A01D91204F1811123EAB867D3E40E8C652585D28");
HexB02_1	= char("62B21CF0AEE0649FA67B7D0EA6551C1CD194CA77501E0FCF8C85867B9CF679C18BCF7939E10F8550661848A4E0A9E9EDB7DAB9EDABA18C168C8E28AACDDEAB1E");
HexB02_2	= char("64B71F486AD57125660C4512247B229F0017BA649C6C11148FB00B70808286F1A9790748D296A593FA4FD2C6D7AAF7750F0C71B31AEE5B400C7F5D73AAF00710");
HexB03_1	= char("681A8E51420BD8294ECE13E491D618083FFBBA830DB5FAF330209877D801F92B5E07117C57E75F6F0D873B3E520F21EAFD78C1612C6228111A369D5790F5929A");
HexB03_2	= char("04DF1DD77F1C20C1FB570D7DD7A1219EAECEA4B2877282651B0FFE713DF338A63263BC0E324A87E2DC1AD64C9F10AAA585ED6905946EE167A73CF04AD2AF9218");
HexB04_1	= char("35951FEE6F20C902296C9488003345E6C5526C5519230454C556B8A04FC0DC642D682D94B4594B5197037DF15B5817B26F16D0A3302C09383412822F6D2B234E");
HexB04_2	= char("7681CF7F278380E28F1262B22F40BF3405BFB92311A8A34D084C086464777431DBFDDD2E82A2E6742BAD6533B51B2BDEE0377E9F6E63DCA0B0F1DF97E73D5CD8");
HexB05_1	= char("188157AE41830744BAE0ADA6295E08B79A44081E111F69BBE7831D07BEEBF76232E065F752D4F218D39B6C5BF20AE5B8FF172A7F1F680E6BF5AAC3C4343736C2");
HexB05_2	= char("5D80A6007C175B5C0DD88A442440E2C29C6A136BBCE0D95A58A83B48CA0E7474E9476C92E33D164BFF943A61CE1031DFF441B0B175209B498394F4794644392E");
HexB06_1	= char("60CD1F1C282A1612657E8C7C1420332CA245C0756F78744C807966C3E1326438878BD2CCC83388415A612705AB192B3512EEF0D95248F7B73E5B0F412BF76DB4");
HexB06_2	= char("434B697B98C9F3E48502C8DBD891D0A0386996146DEBEF11D4B833033E05EDC28F808F25E8F314135E6675B7608B66F7FF3392308242930025DDC4BB65CD7B6E");
HexB07_1	= char("766855125CFDC804DAF8DBE3660E8686420230ED4E049DF11D82E357C54FE256EA01F5681D95544C7A1E32B7C30A8E6CF5D0869E754FFDE6AEFA6D7BE8F1B148");
HexB07_2	= char("222975D325A487FE560A6D146311578D9C5501D28BC0A1FB48C9BDA173E869133A3AA9506C42AE9F466E85611FC5F8F74E439638D66D2F00C682987A96D8887C");
HexB08_1	= char("14B5F98E8D55FC8E9B4EE453C6963E052147A857AC1E08675D99A308E7269FAC5600D7B155DE8CB1BAC786F45B46B523073692DE745FDF10724DDA38FD093B1C");
HexB08_2	= char("1B71AFFB8117BCF8B5D002A99FEEA49503C0359B056963FE5271140E626F6F8FCE9F29B37047F9CA89EBCE760405C6277F329065DF21AB3B779AB3E8C8955400");
HexB09_1	= char("0008B4E899E5F7E692BDCE69CE3FAD997183CFAEB2785D0C3D9CAE510316D4BD65A2A06CBA7F4E4C4A80839ACA81012343648EEA8DBBA2464A68E115AB3F4034");
HexB09_2	= char("5B7FE6808A10EA42FEF0ED9B41920F82023085C106FBBC1F56B567A14257021BC5FDA60CBA05B08FAD6DC3B0410295884C7CCDE0E56347D649DE6DDCEEB0C95E");
HexB10_1	= char("5E9B2B33EF82D0E64AA2226D6A0ADCD179D5932EE1CF401B336449D0FF775754CA56650716E61A43F963D59865C7F017F53830514306649822CAA72C152F6EB2");
HexB10_2	= char("2CD8140C8A37DE0D0261259F63AA2A420A8F81FECB661DBA5C62DF6C817B4A61D2BC1F068A50DFD0EA8FE1BD387601062E2276A4987A19A70B460C54F215E184");
HexB11_1	= char("06F1FF249192F2EAF063488E267EEE994E7760995C4FA6FFA0E4241825A7F5B65C74FB16AC4C891BC008D33AD4FF97523EE5BD14126916E0502FF2F8E4A07FC2");
HexB11_2	= char("65287840D00243278F41CE1156D1868F24E02F91D3A1886ACE906CE741662B40B4EFDFB90F76C1ADD884D920AFA8B3427EEB84A759FA02E00635743F50B942F0");
HexB12_1	= char("4109DA2A24E41B1F375645229981D4B7E88C36A12DAB64E91C764CC43CCEC188EC8C5855C8FF488BB91003602BEF43DBEC4A621048906A2CDC5DBD4103431DB8");
HexB12_2	= char("2185E3BC7076BA51AAD6B199C8C60BCD70E8245B874927136E6D8DD527DF0693DC10A1C8E51B5BE93FF7538FA138B335738F4315361ABF8C73BF40593AE22BE4");
HexB13_1	= char("228845775A262505B47288E065B23B4A6D78AFBDDB2356B392C692EF56A35AB4AA27767DE72F058C6484457C95A8CCDD0EF225ABA56B7657B7F0E947DC17F972");
HexB13_2	= char("2630C6F79878E50CF5ABD353A6ED80BEACC7169179EA57435E44411BC7D566136DFA983019F3443DE8E4C60940BC4E31DCEAD514D755AF95A622585D69572692");
HexB14_1	= char("7273E8342918E097B1C1F5FEF32A150AEF5E11184782B5BD5A1D8071E94578B0AC722D7BF49E8C78D391294371FFBA7B88FABF8CC03A62B940CE60D669DFB7B6");
HexB14_2	= char("087EA12042793307045B283D7305E93D8F74725034E77D25D3FF043ADC5F8B5B186DB70A968A816835EFB575952EAE7EA4E76DF0D5F097590E1A2A978025573E");

Dec01_1		= hex2dec(reshape(HexB01_1, 4, [])');	Bin01_1	= reshape(de2bi(Dec01_1, 'left-msb', 16)', [], 1)';	Bin01_1	= Bin01_1(2:512);
Dec02_1		= hex2dec(reshape(HexB02_1, 4, [])');	Bin02_1	= reshape(de2bi(Dec02_1, 'left-msb', 16)', [], 1)';	Bin02_1	= Bin02_1(2:512);
Dec03_1		= hex2dec(reshape(HexB03_1, 4, [])');	Bin03_1	= reshape(de2bi(Dec03_1, 'left-msb', 16)', [], 1)';	Bin03_1	= Bin03_1(2:512);
Dec04_1		= hex2dec(reshape(HexB04_1, 4, [])');	Bin04_1	= reshape(de2bi(Dec04_1, 'left-msb', 16)', [], 1)';	Bin04_1	= Bin04_1(2:512);
Dec05_1		= hex2dec(reshape(HexB05_1, 4, [])');	Bin05_1	= reshape(de2bi(Dec05_1, 'left-msb', 16)', [], 1)';	Bin05_1	= Bin05_1(2:512);
Dec06_1		= hex2dec(reshape(HexB06_1, 4, [])');	Bin06_1	= reshape(de2bi(Dec06_1, 'left-msb', 16)', [], 1)';	Bin06_1	= Bin06_1(2:512);
Dec07_1		= hex2dec(reshape(HexB07_1, 4, [])');	Bin07_1	= reshape(de2bi(Dec07_1, 'left-msb', 16)', [], 1)';	Bin07_1	= Bin07_1(2:512);
Dec08_1		= hex2dec(reshape(HexB08_1, 4, [])');	Bin08_1	= reshape(de2bi(Dec08_1, 'left-msb', 16)', [], 1)';	Bin08_1	= Bin08_1(2:512);
Dec09_1		= hex2dec(reshape(HexB09_1, 4, [])');	Bin09_1	= reshape(de2bi(Dec09_1, 'left-msb', 16)', [], 1)';	Bin09_1	= Bin09_1(2:512);
Dec10_1		= hex2dec(reshape(HexB10_1, 4, [])');	Bin10_1	= reshape(de2bi(Dec10_1, 'left-msb', 16)', [], 1)';	Bin10_1	= Bin10_1(2:512);
Dec11_1		= hex2dec(reshape(HexB11_1, 4, [])');	Bin11_1	= reshape(de2bi(Dec11_1, 'left-msb', 16)', [], 1)';	Bin11_1	= Bin11_1(2:512);
Dec12_1		= hex2dec(reshape(HexB12_1, 4, [])');	Bin12_1	= reshape(de2bi(Dec12_1, 'left-msb', 16)', [], 1)';	Bin12_1	= Bin12_1(2:512);
Dec13_1		= hex2dec(reshape(HexB13_1, 4, [])');	Bin13_1	= reshape(de2bi(Dec13_1, 'left-msb', 16)', [], 1)';	Bin13_1	= Bin13_1(2:512);
Dec14_1		= hex2dec(reshape(HexB14_1, 4, [])');	Bin14_1	= reshape(de2bi(Dec14_1, 'left-msb', 16)', [], 1)';	Bin14_1	= Bin14_1(2:512);

Dec01_2		= hex2dec(reshape(HexB01_2, 4, [])');	Bin01_2	= reshape(de2bi(Dec01_2, 'left-msb', 16)', [], 1)';	Bin01_2	= Bin01_2(2:512);
Dec02_2		= hex2dec(reshape(HexB02_2, 4, [])');	Bin02_2	= reshape(de2bi(Dec02_2, 'left-msb', 16)', [], 1)';	Bin02_2	= Bin02_2(2:512);
Dec03_2		= hex2dec(reshape(HexB03_2, 4, [])');	Bin03_2	= reshape(de2bi(Dec03_2, 'left-msb', 16)', [], 1)';	Bin03_2	= Bin03_2(2:512);
Dec04_2		= hex2dec(reshape(HexB04_2, 4, [])');	Bin04_2	= reshape(de2bi(Dec04_2, 'left-msb', 16)', [], 1)';	Bin04_2	= Bin04_2(2:512);
Dec05_2		= hex2dec(reshape(HexB05_2, 4, [])');	Bin05_2	= reshape(de2bi(Dec05_2, 'left-msb', 16)', [], 1)';	Bin05_2	= Bin05_2(2:512);
Dec06_2		= hex2dec(reshape(HexB06_2, 4, [])');	Bin06_2	= reshape(de2bi(Dec06_2, 'left-msb', 16)', [], 1)';	Bin06_2	= Bin06_2(2:512);
Dec07_2		= hex2dec(reshape(HexB07_2, 4, [])');	Bin07_2	= reshape(de2bi(Dec07_2, 'left-msb', 16)', [], 1)';	Bin07_2	= Bin07_2(2:512);
Dec08_2		= hex2dec(reshape(HexB08_2, 4, [])');	Bin08_2	= reshape(de2bi(Dec08_2, 'left-msb', 16)', [], 1)';	Bin08_2	= Bin08_2(2:512);
Dec09_2		= hex2dec(reshape(HexB09_2, 4, [])');	Bin09_2	= reshape(de2bi(Dec09_2, 'left-msb', 16)', [], 1)';	Bin09_2	= Bin09_2(2:512);
Dec10_2		= hex2dec(reshape(HexB10_2, 4, [])');	Bin10_2	= reshape(de2bi(Dec10_2, 'left-msb', 16)', [], 1)';	Bin10_2	= Bin10_2(2:512);
Dec11_2		= hex2dec(reshape(HexB11_2, 4, [])');	Bin11_2	= reshape(de2bi(Dec11_2, 'left-msb', 16)', [], 1)';	Bin11_2	= Bin11_2(2:512);
Dec12_2		= hex2dec(reshape(HexB12_2, 4, [])');	Bin12_2	= reshape(de2bi(Dec12_2, 'left-msb', 16)', [], 1)';	Bin12_2	= Bin12_2(2:512);
Dec13_2		= hex2dec(reshape(HexB13_2, 4, [])');	Bin13_2	= reshape(de2bi(Dec13_2, 'left-msb', 16)', [], 1)';	Bin13_2	= Bin13_2(2:512);
Dec14_2		= hex2dec(reshape(HexB14_2, 4, [])');	Bin14_2	= reshape(de2bi(Dec14_2, 'left-msb', 16)', [], 1)';	Bin14_2	= Bin14_2(2:512);

ShiftBin01_1	= zeros(511,511);
ShiftBin02_1	= zeros(511,511);
ShiftBin03_1	= zeros(511,511);
ShiftBin04_1	= zeros(511,511);
ShiftBin05_1	= zeros(511,511);
ShiftBin06_1	= zeros(511,511);
ShiftBin07_1	= zeros(511,511);
ShiftBin08_1	= zeros(511,511);
ShiftBin09_1	= zeros(511,511);
ShiftBin10_1	= zeros(511,511);
ShiftBin11_1	= zeros(511,511);
ShiftBin12_1	= zeros(511,511);
ShiftBin13_1	= zeros(511,511);
ShiftBin14_1	= zeros(511,511);
ShiftBin01_2	= zeros(511,511);
ShiftBin02_2	= zeros(511,511);
ShiftBin03_2	= zeros(511,511);
ShiftBin04_2	= zeros(511,511);
ShiftBin05_2	= zeros(511,511);
ShiftBin06_2	= zeros(511,511);
ShiftBin07_2	= zeros(511,511);
ShiftBin08_2	= zeros(511,511);
ShiftBin09_2	= zeros(511,511);
ShiftBin10_2	= zeros(511,511);
ShiftBin11_2	= zeros(511,511);
ShiftBin12_2	= zeros(511,511);
ShiftBin13_2	= zeros(511,511);
ShiftBin14_2	= zeros(511,511);
for i = 0:510
	ShiftBin01_1(i+1, :)	= circshift(Bin01_1, i);
	ShiftBin02_1(i+1, :)	= circshift(Bin02_1, i);
	ShiftBin03_1(i+1, :)	= circshift(Bin03_1, i);
	ShiftBin04_1(i+1, :)	= circshift(Bin04_1, i);
	ShiftBin05_1(i+1, :)	= circshift(Bin05_1, i);
	ShiftBin06_1(i+1, :)	= circshift(Bin06_1, i);
	ShiftBin07_1(i+1, :)	= circshift(Bin07_1, i);
	ShiftBin08_1(i+1, :)	= circshift(Bin08_1, i);
	ShiftBin09_1(i+1, :)	= circshift(Bin09_1, i);
	ShiftBin10_1(i+1, :)	= circshift(Bin10_1, i);
	ShiftBin11_1(i+1, :)	= circshift(Bin11_1, i);
	ShiftBin12_1(i+1, :)	= circshift(Bin12_1, i);
	ShiftBin13_1(i+1, :)	= circshift(Bin13_1, i);
	ShiftBin14_1(i+1, :)	= circshift(Bin14_1, i);
	ShiftBin01_2(i+1, :)	= circshift(Bin01_2, i);
	ShiftBin02_2(i+1, :)	= circshift(Bin02_2, i);
	ShiftBin03_2(i+1, :)	= circshift(Bin03_2, i);
	ShiftBin04_2(i+1, :)	= circshift(Bin04_2, i);
	ShiftBin05_2(i+1, :)	= circshift(Bin05_2, i);
	ShiftBin06_2(i+1, :)	= circshift(Bin06_2, i);
	ShiftBin07_2(i+1, :)	= circshift(Bin07_2, i);
	ShiftBin08_2(i+1, :)	= circshift(Bin08_2, i);
	ShiftBin09_2(i+1, :)	= circshift(Bin09_2, i);
	ShiftBin10_2(i+1, :)	= circshift(Bin10_2, i);
	ShiftBin11_2(i+1, :)	= circshift(Bin11_2, i);
	ShiftBin12_2(i+1, :)	= circshift(Bin12_2, i);
	ShiftBin13_2(i+1, :)	= circshift(Bin13_2, i);
	ShiftBin14_2(i+1, :)	= circshift(Bin14_2, i);
end
GBin		= [eye(7154), [
[ShiftBin01_1, ShiftBin01_2];
[ShiftBin02_1, ShiftBin02_2];
[ShiftBin03_1, ShiftBin03_2];
[ShiftBin04_1, ShiftBin04_2];
[ShiftBin05_1, ShiftBin05_2];
[ShiftBin06_1, ShiftBin06_2];
[ShiftBin07_1, ShiftBin07_2];
[ShiftBin08_1, ShiftBin08_2];
[ShiftBin09_1, ShiftBin09_2];
[ShiftBin10_1, ShiftBin10_2];
[ShiftBin11_1, ShiftBin11_2];
[ShiftBin12_1, ShiftBin12_2];
[ShiftBin13_1, ShiftBin13_2];
[ShiftBin14_1, ShiftBin14_2];];];

CheckIni	= mod(sum(GBin(1:210, end-1021:end)), 2);
CheckIni1	= [0, CheckIni(1:511)];
CheckIni2	= [0, CheckIni(512:end)];
DecIni1		= bi2de(reshape(CheckIni1, 16, [])', 'left-msb');
DecIni2		= bi2de(reshape(CheckIni2, 16, [])', 'left-msb');
HexIni1		= reshape(dec2hex(DecIni1)', 1, []);
HexIni2		= reshape(dec2hex(DecIni2)', 1, []);
% ShiftBin01_1	= circshift(Bin01_1, 31+32*0);	ShiftBin01_1	= [0, ShiftBin01_1];
% ShiftDec01_1	= bi2de(reshape(ShiftBin01_1, 16, [])', 'left-msb');
% ShiftHex01_1	= lower(reshape(dec2hex(ShiftDec01_1)', [], 1)');

% Dec01_1_1	= hex2dec(reshape(ShiftHex01_1, 4, [])');
% Bin01_1_1	= reshape(de2bi(Dec01_1_1, 'left-msb', 16)', [], 1)';	Bin01_1_1	= Bin01_1_1(2:512);

% lower(dec2hex(bi2de(fliplr([Bin01_1_1(end-30:end), Bin01_1_1(1)]), 'left-msb')))
% lower(dec2hex(bi2de(fliplr([Bin01_1_1(end-31:end)]), 'left-msb')))

save GBin.mat GBin;
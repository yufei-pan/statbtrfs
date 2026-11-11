#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import errno
import fcntl
import functools
import time
import os
import sys
import fnmatch
import re
import shutil
import subprocess
import tempfile
from collections import namedtuple
from datetime import datetime
try:
	import multiCMD  # type: ignore
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 61):
		raise ImportError('multiCMD too old')
except Exception:
	import sys,types,base64,zlib   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
GhUA(CNJ6"P+T^#60g!*?jSW`;t9:,7d^sp8T_3`QR2*GO5ciUE%#-h!XJeKd])lrY?s)Q!@^%>8(D/a&X_hIl0dffoF1F8Spe4bl>J?Ii`fF<%'.#6\
h(Q7jQihIgL8N:f.('ZBmj!XFecg\<O[5mB'!d(Z8O@o`dSu,QW^9P\gYH9rbYZkQK>+Qf4fRPQ;(J^YYbZG2V0I%$\(*P^'^A-W^u*HXn1O%Cc7V[?"
U*N_WJ!-R0)_go<eq[3mH/cRXH5.lZ,.i.N$VEL"pEGehG_67b%sp'75r5bDA/K&nsn"=Io`#:Z&iI5#:#TSfbr.Mh;g!T2-g'0*9apU4E&mpEjcWlNb
eNb_s-E<X[AbF1tJcD%qU#lfmq2o'Z!caY/Ds5KCRU=APM)bOUqu?2.4S?\5R)p:FqaGOmeKrlIHN!/Q+%E;9:]U\!QaVmodfXB\j&9)7>_`QXtQa2Q#
F4pp5O#EX^ZhnrtHho.._nKP`jgL_^LBp7Y(Z;N8*7jGgknXE>EI2:p3OI2Yq=caFe<G^6dL)'Ck`o(9eHosDMH[Y\gkY:XEo^1m7T-"$)?Tl#OIt@qs
3W&U61jORqr_(I.48s8kB@jlLC_e==Iloeb&1%6(>r?AY*1nPG:X>%c`FUhXd^=sBY:?%>(09C\6g4DdqYKFB/G]+Zl,WO&UATRQ2$*];:B$^[p$b?8-
1=%34[4DomL;#SQM33m3Vmji3o8I\Jhr(:<k>p*!g(sM@L+1I]sHakh]KTtnj7a#o[DL.HU2aN>dX<IGb$a,gXa([=p0sMNqp`1;Jcq2cSGcAad\pZ"r
@Hf56dsaY4@:-COK'U`#Vt5bscUmK1>b&m)9r*/n5)UL%DLc#rDZ/7G//(,OS.M+T9E?mg\Pu<Ar"7B$e^\^@Y`VRKlOs:b";+"<O2*#L?kKio?Y,qE2
@Y48?F$F^)h>K!4LIq.pQFXnqSTl0D]o5/%"NA8s[-DLPI<`$],iLlHL7R6QVCkKHJ$hpLm]HP8('XS&!$E+!rs(:22U,(-`d^<,QuVHSPH0"om>3MPL
DF'S;t/Zt>a17udCJ65XWRAsHj=*8^df4?!%2-k&54U*Yt/m-RT^tXj`eDTV>DnT;]3Qr?A<\t=@3AhM>edB&(:AIV4ED^u<AAJrlaP+=\3>ZEj]_.U\
gMVak1IV4RS^jjbDZ"&OU5A##UXcMh7sH8WXu%Vm<NXtL>ms0n5Y%L]IZnob;#bc::B#V@s26WSiPU3mJCCiArWO7on3s&&!_E%!oh_;aFR*R5@I1/@d
,o,B@/TL@5[B%C6*K7pW*5McU.'Vba=d3W[AmuV6q=kj+IiS0IDf0sfIH+1J12Ro$[A#rU>W:V+Fe&0GN]8TGU$VW$65UOZF!M9&;Y4KOf+Oi&MJkm]/
THYI2O\-):#_lAerXX]EPe<XV^K>M\/(41'YuTl/Ve?6Fa>t>t"Q'cur<q5F%^I_*Wmc_`)iM+f2:/7+bMn2"&/QXN</5L+94`)X/MeeS,N#d/+T!s$`
lQ^K0,$KXaXdO<Ut^rUsZqYC`HM@uT![ggc+upXPYk^G6J=/3tu\;!e@E=S2U=Lb*K8!d(`hPcqqU\jaDN,Q!,Sr;:I>\;HKf[qG5Zk;po7O&&+>p%78
H\iUp@KM[Qe\/m]Gi?8:8_D/IH]\;b8/e55rMu+RPlhNLn7!K./)Y.UX6*eXO<.YEP'Al0a?,.Xnp-CA#J_>N7r,?]K7Rp,d*;8r=[K>h5SccQ;Y_Q8O
5\/*n,k3&&>!ci0?DkadM"#74DmB48WKD$89njMH7TfA)e&J`)H%gr/YKVb(?<0a]IS]8f_/.?t!i,!=,sZmJ^e>J:Ai2rIQ*0]X<!sXZ;RL_o46`'c+
ot'GhL\&c)pt1=-0/rm+>%;#65>>l.710_;@K;3>cec/9K.CW'Bse9/^kj7]hXa=f/6qpb>c(J7@JdiXr1Pt5Z<4dcVPckGIbK'NskCAjh-qUf67LH#R
Ar/hY.;%<^XX'o"[[:UiAUOqfY3P8H#dZpI55bB)o;Qg;3X_Uh`(,Z)L5Qc'otI1N:/^AO@i+3=e,r@*e6[S'ccR?bhaQfQGt(il),M=i_B_nR-8GHpU
V!9`W"ogt#F<J!h>pC_N\>T(gTg9tob4@%V[3h?E*KG+*+Qb6e'9Z5%:FKJJ>8'<gu(p$"2u1=SoN9+2@3;q16T6>Dslnj55(Cq22528`u45'A[QmsA.
XL?3H#:SSt_BR^L[@/Ru=%)Er0P.-3kj5p8Z33+hP"mqV)4j8]Ua`!ZS<J`+LdGJ[$rY036[QQm-(^V`Yr4ith7bBbZ]kHVhn6Jg!a`:Ct)Yj)Z".B\#
],uukBH_8?j1gq+5p-X#)Quj*$X!"I<Nl";k@uhgSQ=?RXi,(FpXhUm@?As;/M5!Z"*!#Rr=d*dg:-_EK%sBVKoA0^g6n3QpC4.\%RL?DEg9rk?LUVa=
iG"%4FULHT8g%l^2]V?[Xf^A1s5FuN&]N20i2a,,L47N?,'E?U>roCW9G3XUV-LdUbQPG`oP?3\G$"L.AY/$GBrA*3$J@Y`S\b2e-LdVrK?<F=:?$M.7
&SW=9,h+Oehti%h-jl#\Y3]9CO3<O_9+s&h$!Fqp^lT+(Mf(22B\dMT6B&r+$9R-d_4@-_]sUhOd.c1Eq,[+#qBKmb1td'P*"eJk+mqI1ZMjP-abt&*K
$'*1t98!GMm&UqB7$eHuaQl8T0E4(JSHEl1SL;jDFtV_h?W^eBn0r<O&U5K6hMj3`U;<_/@"FVj!n@nsI#M]'"]TBn:f=@;e8744&Cj<%s4\#c)c@s\@
X#oBRm73I9u4XVfULL61^R#K3*6Bs4.&-7UF8LkfS_i>g:r^"%>?[r[V@FO!d[YF]S5_)Z40Ld>;1JV1DCHY!j.8<`#S&;u@Jnr;1O>XKqC%*(U-A'j[
:g\=@cL3E7#\aL$eR!XUB*V@=-F,+sA_07=U8!Srl3:??7iG-,&!daP&Fj@c?Y0OaQ=dh8@PMo#7=lP988F;i,>k5>jU'/=U25?L@$Y3ER1Q&dGKBrhp
@`N*^tA$aN26UN1OCA_O7Z+MFEH3Rs4Bh5iMY^l<^QYbM,nBERRnRj>3W/=n?gY29m:??&`G$;LelcC&6m&/*K3#V6F61a+(.];Uqn*_Lo[guOsK`6[U
(WZ'!ts>7IKYFKSba4C%(B%6G#m)Pmec3/@\1jJ5#]-h83[1kY'R_'Hp<8c=*bri`O/p0X_^S2?-GmDuV>2A$"_jc=i`1*DW)UkRlq=TU$@;_MD1LE=0
icAX?67;^54Zm1:I'D!j<gQtFFB<VBQooQt4:M-37UEPrL\Lf$kO#(pet5n<J'VEcJRUYo]tJ_3elHFc`QF+a;:5]%(PT$D#]p)5Hq$f>s[6$-L4aLnK
Ql.m"Uj9i328!:kq/aDt$HFZpsR[J31cD'=2O4qc$U%5Nq+-6\RK?Y,W<Z-^.NiFdXkKZWk\JPLO8hl2m9s*R>C=?ELENCcWX5\P6Z"tXHfeQO<Ma7ZA
7I^kr[*$jhU1409%[E<%m!IZknD>@Ac20!8<3ja67]Hh><Xoco*@@2=/r9,!<m1D!,Zu<b9ZSn<"jirG+C_#G(td/CB!B<g2^AanpkC1@bf"NC`s6.m%
S<3kG:OXFG+I$+(UZ22g."Kb#SE,jCBT'pPKVX_*ZZ]V$7%X'NnjF2`WHbPV$25@d`5NRJi,7Q[rfn2fe1fr[Q[rOQYdhhW_3b9eMQNUV/fcJp4l[XKb
Z;fe,&-e6idn1S6hM>]=?UN3_\#:(1s4,!=mIanj&Qp7:WkbE#?Ja7u24SSU\jGc+^;cW@liqf\21%O=]%6`7g@KifD2pP'j5d5ar$e7_Oml@SNY:4*'
NZCUl738_;@(pNP9F("q!:au1hSpi^r`M2jU!STK5UGW[%:@!*$tVG"1]_F8m.nQ63c%_^u7JL#K:gM&+u,qE%CT36iE8/^^(A*B4%6`U4?KmT:]lWH;
<+W?jcO<&I;FFlU'D8%kid-,\<0W%m!aV8ne*qIL6//n@8H'8M)I^tU&7";$;9Z!O=!l5N0+,L@N2u5$Y+?fL<$Gp8W`=e9+_8f"UrckY8AX02O6IYod
[%Xk6!EMF2+f%ThQ__EUce8ur28P4emli];/MmHYeX[2&mP<3%h;Sp?l6c05bPM2]ciTAA(L$LDY91-N57ra9h_o5EG253@IPeRAc*#:lJ[B4C\pronl
u\G"k7*/O-#gtjYg"d<5$b+1XOC3DW>\tm%q2Bu\u)RdThfQ:S3+XE7Y"rb^@1:'2UUc9>Jm/*eb[!YEG3giI;eF3['Of1GDcA24B:O`e$'iJ>,e5,fd
jjQaNLkoog,k-L$b/:?"qs%*NW">Fi?eL-9HMsH>[mN#i7uU.ZC(O:d39,N4:G!lI36m/)9Pi*i9UUj'n^"3<q?#SV;i/,7W"h(s3h'&co74XSLXFEZ;
/VpJ(slf%cf9n5El*nt@,2M\h7793r_u.;.o`s3C!dOL'FJe..(EUc))Z$A.(*"DrkT`$BhM%=nCCoU,#Q_W7>7'XEb8:PV%BGWODq.MQbCQD76`E4bG
H-e1ePb4"#+;\C`)"IWPk#*6tf+Mj:%[:P@Gc=.EDN`gu:LYDDsiJLG0jN0RSb=^Di'cX%!=nb(+5:tG0!4l!`E_2MjY(Yk+B+pt]HiRrl%NZ4]CDX.,
\Y?'o2J\I(dF9cp#bPQq^#H)Td.Rd60W(,b<-$Zl/29m5/C+oPbhR5G2P?S]k,gA0iOsQi%i'0]A@8YF[u[Jc>r6Y\(S*@E%>.Y;c8KeS3MB"VfsCh@!
VL/*j.(TX-I]l6c]1BfcB/+![/\0ZpA+Id''!?ABW-tj)1:KZL)RmKn/'W9IZ6*<3XPiUU,T\iq%'em9qiZ+(sX=-?u6\UOd*lt;Zb2PG*.e.KNWlRXP
8kuiCFL]`BrhKTZL!AbVXKQ[m6VM1^kad-:a;'8>LPMQEQQ31(Xar?s)o()C]@R4,lThZ3g]pT#pK+%i7Y^JC8),EWfedccuEq89ckK<+Kj:6uTm?l'0
K0)DZ`R";rSRRs_UdRqmDHTN;%3>,a;lPKAQ9TJ"&<o9pBAXq@jO286@`(qT#*6TjVU_jHrr*!G4gQ\@:M`mK^]7*/07aqnd8h;l;c$&d3b)k1L1A;XK
6'u:&4jm#<AIJOn+",!S59El&7Huu/_a+\U5<I5X\08EX=ir2Znh%aD0?IMQl7[#8)`'lf[^Cj3Ro(>2?)<Kh.\-ipMa&Ha)%np)eEXp(n\"$s1_VEkT
l16%0hqfgGI\tmgfe.cYS?c/TQ)p]5bcVfF3-25Sa:Y=3,dKo*\EY8W@pfN_=Gpe1_FJ*2Jk:UIPV%kb#X`4+g$BY#Us@fO>K8a0<QuQa8F3`dZBEohK
;#+*()pK:c&$?<hh%>G]&88&R68a3?D/NiV#1g.[>1tfG&TSk`LXEs3LtI`BU'K&WA=B;heJ0*GMb^m/ZJca)[Ub^^eM!BIa?DKQNEhc;9C"[o)0]1q+
Mkj_f3n_O9a:_I-#-)6ORk2S_5o5H,f(a`[s*_LV9U\gp3ap\q_as2YFsnB/js\L<rZ:a4iaPbYm@'P;XNL7=#n)bV@KVT:B4s4Y;jBDCNJ-C^@a'Tma
&N"oRh]`bI`HV#oY\A4ffMl\nM@nT^KK!&C@&=VQP>C")-\UO.+\&8P*X,;5uS'ukZS<ZdKjeZNu0-WS8KpR=3f!>12DB<[";2Us%-Noj)GGCI%`f]1+
']YSLX:SJpgK$!WXdX#uCR-)&uXeSM\72fr?RkqGfDXH7,Zrl(2Qte-o8DcPO"^%d;)Q%B1)>C.d=uo;*[m=J6n]5!#SMfmpgK`(4p7T^f^K5mCD]!FO
hqUPWjN=-KKSO"-3JZE3Zm-?2Y`:lcPO6O'Q;<aZL(:l59%V#TohgsN[(E9XB=A%H+"P[hnB0QYdNr$\6kaFpJD:[4N6L=GMo[[`(WC>A7m\CZ\oMQsJ
7X"PJD:fe9Sr7d"d7ulWg0\?SY3g/UY7nV"G'YqOnR'@;'TkjiGK+@P=Sl@mEpuUk\.mh#th:=$D+U'69U&q/m?-;@tP^2r)LJBXm5B[Ee=M-.V&PK?]
cdI/%"?;,dW_23UT$kWMfIX"-3]5eEB<K3"t8C9qpg7H$KA)'3T=]Mj\l"J.Gc^/95hc%B#7pLi!!AfBt\^np"UXSq+tZb#JYk(B;PD5UF+`oG>9UaDj
kkVo:_]iKI20Jdt<q\DuNmdl;eBG"ci<p@<ruippZ@[sB6eEMe*GnWrs\CGOLPN9/t85@0;]&APO(Yr\tP;]T%XG.,F9akh(Lj"3TZ"/J<=KT9pJ9$`K
C;[kT(eh,UGY(X^V5k^03h5%g)"lj+_##iIO'+?oYd%K-1JB[4-9YT]l0O7%FV2L`09,0Q\&E4q+J8=jkbPh<#3k,FALW.11Nc3HY+?nf#d00%b1HiTu
?[<39#.IT:RebTWQHsmkFhfe"3tJG/5WJ4.X!bdAFLCZq10=Gboig2BLT+h-dXt'K8:S"GnFE><]?bZ9@/cCA(t2K-SO-?[O#2[Br-(\r5<d0+jZ^l\h
YVs2pk4:Glu,%+gQ0H;S@g]<`b/nSFC9k-=Je[@A_dk@#lN?.pc</XMp4?OAqhdZ6T!UA9cERW=2XM5'[.SY6-R,>-AC540@!aAO#\9P2^WI[O7RIg$/
?O<?4Uu('n47q\P?-_nH%O+>2sLd[&a(;Gmnu8Jdr3'4rnPI<:B($!$%-@WU%5RJtHJ<"$E2S60Yu)1F4tfE:.=ZM)-sO<F%pl3&0=^L$ZSK=:/g5*nL
Q8U>n`E6RN>6CV(f8R9#YRgg2^_J_=L'g(=['`fsq&cj=e!o>%Q\?2$r!\MS\#^<K1Aj/O^JRuD4h1/:XHGPU8>g+^ldILA9]<9`-"++:DWWa/hqRs8R
`&dcLMn3hr47CcKlS4cYTp>*n;]?=N*FX`n**rROc[qV2Ts5J`sW]%,;+9+:#[(2K:]YM6J6PP>PEp/=H+Zc!ch(ZV/)B)nLl3aK.?t?FEn9$DMVUna/
3`g0MW/&l%:&?\"PNe3^4^C+^]PCs-:uffi.H[@MgWK2rJM(R&32b$(2oXsIQ]jTUTD1(Ss8KWsp>N+Efr*-gjVuK)VP!D+nS-Jn-CUEE_A(8CoeT\CQ
[SgLUl<"*lXcT8$P#ML)%/<h&%;#:PGZT";^RV4BZ(#.,<q`lORsGu=-H.cIC_"9^8OL>@O<r&N_%%o,ih$NXT.,=6=[GIku*WGf]^5bDOn7]qdEsmJ4
t$u4eo%_%dW2DV[[;SeZh\(6$L<Wh64&HaXGXTW`-1Dd:or*nT/-c2@rQR?M1pGl,Keq&5[TekZ8!kM`>sXqd/LsY'9(gUMn-2eNn+*f`bQ7fK6Z!"#7
teXk3]$ET!FS)c:SeSe85XB<H:!\(6I=[\j74UUF3Yf@aHg^?'+.h'a;\6b^"Y@H^JEGPMMD!5,0hOhgT7a6l?a#O<uHeIC2inGfo7cFj]g8h$-8=eRG
/0]sAP2!7:%Pui!/k?$7epsK?^l$s,U<musC#NgZ3Y1^"rs!$l7TA)>gqe+kpaHmY-m)>,\R%Q%QLXiEIVm(QKP9lJCk>Hk-.$.Po."M@"J7<U/o=&B/
2:F?C$UCGLF-W`DmQ>gP4oP0KAU\4pbCCnf=oG8W#Wg"Urq$,0J,f;:oAo(Iqj7*-mJaJBAtBEjbL4r?i^NV+pW$($'UR\"TCLa*H:KV.9m&da;,SjcU
Y_j3G!t_2qi*`-)jpSCCaE8H-+AAU110hPHE6YbZmu$@5Ie`8#qMA>QnH/7J'[=c^3R<Nc[@#-mR.e7n*:\gMf$$QkDHQM?<i4<\8(OYWV'\QKLaL:IP
iQ97sVQgnu/8B_eEl$!E6G)o7O*#ktG7W?MOilI3@KfRH9e+I$s)/npHbRC7iep[9JZG#lMZ4C8t/8aq$%#I__J8fdU20!!_h%k.66&>h7aKH<SNGOP3
[`X3f_Hl25?S9a!DQi85;^V^5Q;AErt%48(Qq\ZgSeo2VBNkNZY7:@m`6qJ8:ZFYb_i4UQ6$bd"Rdca86P;&geX+=.iN.Mt+cOXFsAEWbM5-:oSQ>gDJ
N+#KL'Vpe4YJESC%fL/aC1p@JmfFe*h?/0u+0/G3<iBZO-/&TTf/k:"&P`<Og57#;0#8P*OA6Xhf'O^A3f)Y,#Al0O3RpN^/cMpb0PEGT1EjRZmmeN.,
h3KQF;2*d'qPj[k&qtTDZS!QZ'8A[/EDlQY#]>7oHMAh;I):8n8IIaaeUgADSf@fjdT?ncEZg:AfukU[A!qj1Sm,<=\HP.t'!iH<["6DuRg4?,A'TWS_
L+-%LO!MU->9)GQH9JIBd:%:Fqc^pnB*@!'PsNeS[rhr\t-50"=Y_o@89`fgJXN,T*nag0)f$/_eO`mJDu+4UZjKcK?7#]NL&`+mS+GF$Ibu2n>9.r/g
2j#ArXo'2XQWUY>'qVh];KP5BVVpk-j0[4aHW_#9j;M7=WBXQRdqq'*L],!__h0+[`7eFKb(7gSasfgrcGWo&'dg]Ls7EjjgPDe$%AF$o`n[MEl+2E\B
h>M;[TjH/8mY_J#R_2YgO=i+d[O<gY%ckm*`U?Llo%r@Z_>ngYl1WnM$_lG,f<H(];m?V.<+#h[j(Y$0XYTW#A'1>3)Z_Ql'G$XAf:_X[)TDP<AU>7.5
>7?ZB$lobmn*0f7absg7O,ujHn\QL#JSj.b_G,hi$oZbfY#WYqoc&)c><7[6fX]gj]^ZhnqaQ%#Mo9APK?;#>,+o,.(VcIVSn!Y%'M_"BYs&:S*MogRH
/Bdr,cRf!"9]rl5,G_l`HsRj52Xa\bCkg2:6K7O[U(%/C3#=60CGCZlE4k-uk@3d;4&\8l]U504AF?H"#\B';29U\;r\cFUdVbNBmshu=QX/+m/1O[FZ
O@'n"t?$S;hQU;()M5$aia]7-fBnCm';4Xl)1g@dQtFX=dUG%4qR$g5D"6&Fs+>:'NCMI=umqSc9'WkgP/&?=@e[o+4L$6VWY*)SqWM`kQn3(<gaDu6r
rUC'0q\Hg5HI9_BH&;Ja$;:Y1etoL=:=,s/%ksUF`=V@n=&p<`-k)D-Zj]';Imb=l'/ne7=m=<2]c^ahPObj7V_C^nZ3\]:_XdQje(p!jgJTQF9TV7:q
*,:IQ/1OQlG)A94A;7eagW3@rcm\+faIE3mMgApAm"]ZOG#j=aWqc<UON6\\]p+m+T!-6_Q5#,gUF#A?0'm%o8!MiJ,-%F!I3X:PifXG6'Ai#iR&44L^
G5N\TZ#kM!89Xj=f3ucg@"hd&Agr\Mi2Hm2bk%hs*T@Fq21-_fVbHuE"!b)M8XmLtU-)/cngP""]B,&MUa^>iMM]j&(]_K0S57Bs5%iC]+n5X6&SALoi
1tN;<3>R;gq;;7tS=kPZNR^tAo6FO\%3EF@"e]#G.D`R^(9-K<Ho`;md%1CM<LBJ=(i%cP"suI:X(jc4*4FL#dk46.Xr;(T3..^3(G5<pn%;?g3P_WBQ
JG4ZQK0sFSU078Y-un`dAJA\J,A@"Dn45qG.nu\7lNHcH^dl``3.$=fLpfsUR?bO;=Lj*/.Q+0>R4-)PbINZ7DDd+HpP^7%Mk!oPbt'.eGP[=F\cN@JB
^IsW0jP(jkQ>Ea]_FuV6B7"`l?__=Z=&$mpKHs]:Ig(QY*SmVh^IXE7!4]\CeFjG[K<U,-A3<3Q(G=n.5S<<[?I<5eQl.GrJ<@TSr]G9*o9s68S\C\J.
D.#NZF`D(/3u40Wem@Lr=oc41psQ/*g3cs-6k1eLX?[sU6I2CIbZOd0%)DJrYYrc9sJAlFQRGB!O(4'H2?"\/V(4),J_-A7B`A]U6p!X!UB7$N%)+r(D
gI*Sa@%pp=U3&jGpDIr!DaqG8erorim3uOOBMDdUeIa>7dC&bgDnK9R<8kMJF.-CRtfEj.-\<pI'8Ou25f+s8k4[D/q["&#Ga\P/"puL,Wme>P8c^m9]
mQRlgB?5S-pFlIeIkHb>]B+H\GA7%@]>*4G$-hGm3YcN$7XkhM`o<!<-G"A#V,jW;7rjg7,hR3LJ[n.437Km*d9u55;ud0'962SNURjHjbDFnN'S'p?r
Yciu]P#(=bfdhe';mm`:>8nWnYcd^2'CI;rgPJ+1L#U9)usV__dqWqEoOF7U5Ll\q`(!=(RK!.Z#E1>]VE1c2Wsa\rpaSd*j_eFH.5):^&jH7N>?\e[m
0HnfI:EgI1kjRf7PYL\K8k=Q*".uNa/-;(2PBL7]6Q.kNok/Qmcq:,@(nNff'ep(ZPjq.lp0j7o)HC#OHB]&&ZU3+=iQi6onSK)qm94Fa;0qRXof)mC:
+`JJ1N"!/Xb'&)bq9EGe_<SKkJ*Z,kJ&WYUhNVr]5K=u3PWRHpZa7&.;p[AM["X)uK'(.Nq%"-tqe!h2:to>Ym.#jLO(iuoaDc/Q^s**FGSPK+iF_aX,
kY*A\IZW*?6BV#4&B$sCSalpSmCidN3B'4*9?GB6NGg@h_dWUr5pIkVMAj<mal-V3jc&&^k+Go\eZ+Yp)*<PdOFJU6,`s_^.[C!L_4'*k<r;4pobWY:#
N8N2/GF?99^iL.^Q]eJ\^4a(c(k">?Z&&lZ#PBdO]V@<"-DGeNB$HlGgXiPN[$p0f[s>N9c!(^`.7#Pfc;?OtP*-OIprW!>!V>1?rT2cmJ<q,?MZQ$.i
?hs"4&p8F)8NF4D!?QXosXK%jMN`no@QoSo7fWp500,Y4Ck\mE:H3tL'0D%oG<kNFpOp237!O9W"q$Lr*2(\Ck&[^'?qJ'bD+%ciP?BYjm4dWfUuH%gh
Rd`4h)FbR!@UUhdUKh]Z2qg*js(59/,:"rr(Ao&)ajj2D,;9_tCI'c<)JG/7q#e?();JYU2@^/NH\+T]alRaBLplY\H<&&tS'JJ+hT9hDj,Va.IQ'\\h
?GK@Zg;9phobSk>))5$<*#4'@K9+a*.qNXe\D1Y(KsX@C@Kr7eVl;?Y3p52CVC6^Fc'VPbXDi39PR?6-94[WIKM0ND]XP#4Qd-3_T6PFE9q3/C(+FVT<
53=uB6fJ_4(CAGs[qb^9*<W!#n@^J`M,6T7%R9%<"#eDcu9h1i"A_hdu5Re)QJS;*'%Ct*oLq[Nr:=3k_lNEn2dj77bql[NV]`-QAoLE2^X]p'j5$MNA
X./^'N[ORK<Ie5gWoRNXosqIeJ;._/\_eET?iH+^H#&/uIGo4JF:Kb/oD[k905o_H4i[Uh"?!m'SuqSFr,r7k.u)8.9S[!WfZs?,j$A5!FschPoe\5ee
_?FgIt..RoKS`Bc3!p4e%_@O;CiN@\Ct32TaZC!I$E_(g*e:#o([SqgqrL^4q:0dE,@(B+*SM.,LNV'O.OIj''E1U6lE_@__[+')mS]kClT<%d66s&B&
rf?1IsD$'5CG"U*F#M7I5rqB$9Q7h!b44R!M,HObSmV%n.3+GN=NHSJN3lM4@`]_d)"0[NMk6,,MVBDo=8Iq%@\#]rN9J<mC`3dpruW$QsnmE_$1a-*h
GBrPFKG_e'A"6m@;>ZcUJuA=CG2*X,Kiq*6^:c*IH"1]cB\;^Z1?TSUJGHF-ei]iHRTljX?KGZ<Q%=Wa]jAD+`'\R\B>B$6!ueGA0^gFs=SiIjmVS;ZX
$k<YuH"si&l^IM^]G,LaV)M/n.Hh#ltNRi6WG0Rp[r,u7[+pA/VO3;XR:4_P2^,?nnJu\h+BRTQ"o!->(-U^oRZ$QV!qm[ucs"&u8g]g`bgUA<_"fh$T
l^QEc3NL@aB.1G\0N/dBcObjjkWD.G&i0:rK$sN9qtb2IMId.=>p&VIL\H-2SbQahku>Ya#SYnec&JO=!]S?V.*Z6uT(#0Ff&4)l5EaB`CbSJEer4BpE
t*tG\9GhL`:Q-"p\?6_8;O7s%Gr`n0Ij@gF-UlqF'aRnkfe;t+*,>,%NA_E85mU\TN%#,#G\,X0hHL.?&mjOKpc[1EU*&F;LIML7j]LCU*lbd2Kp3V$)
C^Tr!0.S8l%_*'YGmi#aFr=Z\DWlZfYtj_PL_j*onA^d@#ri>P(aNOPB@ugJ`kICfp:?qVf2LNke#IJ!U#fpJtF8^`DDYm'U+6P8Q\:q,J_bVNf-EH`7
Vsk,CDp)UJpGMJ_!I1"a@=Z9FU9fK3cE8K5gfZ81&L>Y0d,GFi'l7UffN9sLNB=7[lt2r=K&3]Xqn/P"u9dHrpr;R\_kiAld^4MAF2hBJ_p[D(g<o4<-
1mI:^.)OV*`pfYYbgJ0b9%aMk;(NM;]SnI\,3Z!".P'?iF.RrG[2@?SrPVSY(bI3EHgM6s`A9qCeCK=]'0F--B:'Z`#(s-6&dMD4Njg\Kb0.2[c\S[b`
2PC[HKS=r"Fn9b\%3!VXMUQ\XTI"QLFGn[-_-a;RoU6.+@$F4G<VntV)Ukch1BPd)ma*=1OtmQL*KpHhQE/+0>l[8SHZaPi%qhfJl&"9S_-QKG7P6$gm
kqoQ0e\.\k]$pTd1?NO!P9C$OhSl&Y2<f1E]G0)#e/Ao_*a^CR^H9jm[uDChOn0dgZ)Sp%=m-"bb@`cJ(Xu`MrPeAOP,X/n_Tsp=mtL%_9a\O-I([^H'
6,.O48CTY&Klp^)/fXbj)_H$M$5q15OagJYH5tK`_@hDbW!&_dKco7cUad2bA1JX#ZnO_<dLr*fJ#0Za2&nHVds$^$rfj@JB/nT77AH;KX2aMmjPT.Q5
Z4_-]!*&4$o6(89I5S5U__6%tXL_]]RYj\oOF40GGG=5UY4[$j`</@Ma>*0fSUE119/+I9(;eWSCSJ'd[nTaaN_`TXU*BJ4"n'r00CekdY'loN2uD7&j
cQ3keu["cEV2']'kp#mrC[Z]*%QRuQ*.'of4:^-Il95WSbo'=EdAU6ODVtmO"h@J0*N,8X*'8qOL38&j8!4CYgT)]n<%Vnd[WjW2J>.PtJb<h0]RV0<<
0JEoOR:U\8m$+$O`m[B]P%lRB+67l]D:[&f.KnB+ZFrt_A*JP1gY$'g>bab`$)@*jWMDbb:m\g,d'OW<j:F%^)[kk4k[]S/&hF*88'jR_<9jk/>[6,:`
10k4?SKkj?\E5Ae*,fpXTKO#9].<AC"-\2p12::8_R.&$Ko1oKh&BS6H:!NES=p=>4Gb%A<HsTGC$M>/^+76?--sE0'%Is:Za&PLP%'^Su%)s/HA]bWG
,#KPh#N/G:0fUTmbYG-7\l5@YLnN2/0W"!qsjlJ8;s?kafM6J4!5Q9S*VPYp'm*(_UD[&5h^qd@b_rDh/\eoJXoJ$G54,!/YUt5]DpV_kFIqr^P`M^qh
N<[:EU4N'MQZNsCY"9DV_`WQMfhM.OE(k-M?jpqA0eUpD67[U#I6C:<Z%raC$/kHSeUDTl*;:Oj44^MXnUa9&ioN4rkGqQ3s5R9rU*%l<)IS,:uWIf@R
2lMW/kY6LDS6A7EeoAoW+"TgT<r&8^>F0WF>=Q>YEaWLdf>BAL/IHTl!ntbJd4FG?[$e>','2+6s^8k[,@<UaYmj@:G%M9F$i]3iu0ed7[nmf'INn1Ud
??5\>p0V&'.?"]m\&*u-=s84<Pq*Et8rr^[F2MFteX@OEeWi`G(!nI$Mla>r$4S;eLb-)r*Vre'[TWP$\>;-Q&=L3tMQ^`,\P][\H_>eH9Y7/?,'-a`)
u^Ns@8*")\9`qQ3MD2AHi+O!1(eA`l>d]i>E+41feJDl>(V9fa"1$D;mhZ<UDkC&7Q$eDgh8u6kr7tD(7J$/+MM)6Vo_SQs'(uYWB&"_'=6(l<jVDDaX
KW&:UpqG_*:,I"W)VKm.+<CJ4a%q7Z!ZW3B&N0;JBtee0Oe5NU[LZ^+pJ"#0IF\g<6BaRXYgAIFUS<lbHRZ^6i>?Y<sT\K(8[Ld!Ap+$AJBuKAZ=;3dj
qN6AZI\WBCh*7<;9TLX_\[;oCWK3_"a`'7?R[RhpfG3_S/%.$^o%+ol;`fDn62,4J$+1J!i/i9"sW3;oE7El?6.6HX4e#,/jl]1&ip_fR!ICZrBPCbXE
NDp?RoZksdDkP&4K>>n;C*^<Km*]=g.P'UVs=sTnjr%(V]+.%Ai/a>j+"2rP5jZ>L.hSQgHs379\4`tlrnN1keXZj&tKb81;;[@8Lb,3\"9Z>])kXJNf
?Fm8@F3g=2odP$ga-Q>,Z6BRl&V+:Ks.V3]9iE]!?e:LeKk=nSCl-D/f3pA!_U+^%rDS`]=6[HRg&MO])d_,7<2:2E?YF;Y:IS=Cj.MQ6I#[rBO0)e`H
rG)aJd2;%rM.3B(kr8/M+9$j,JjPKS4!VO/2[#.22I)""O[n+d49`(ljuGHY`b#^UXF\HajoD.c>[GQ%F(0V%iDmq.9p[NKK%e8@qTmn2j;I2)=G.$XS
.G&hLQ&uMZ"bti`[0O^7/R3Y(d35IakKZVmhZmf5.Y6hO\l8@Nuai].Zp#418rm?P;a`%njt*YV/?g]+_#S@t2GO\ZNqiN?$ZF?5<d<S(l_%gWjQ@W+B
m/K.erdEtJT!89HtTh1iFmZ*8na&RsBCKpl<FI'amJ#\she?rgd]oi8WSU;&"V>N^@UF?-HsUTT?46Aj%,"XJ<in9B4c;bRj9&/YQp`d\=XE]qI-]%5'
rd^:^PE>Msuj!4N]CbklrFiAgl')\T6Xb')b.=N+;/'l$i%0E5uT$o/RV%3iHRZstM)7Tn.!#.'>N[8P?-09Yfk(KT#Jk=PBrO6F9nbpf\n`AN_:>_VT
"PNeI)#W[D1.m&C%9.am82S@L7c^EOlL=H6?B@tEK0>7jpHb87rMdDq[N<8eV*?B4]4i(Q36[u9F1f\sdZNGIh`ejSI@<s;*k65`,]9[aUW&Y,]h<;?V
lou+Y.T*l%/'^CHn[WP0f^YC2<H;hEg0I?IkhR'AFm6'5C>^h2_=?9\X2`Xh:k4S+C:2m9'T+\NX,7RC/cF5BW<kZ$?W..U)dRJ"N1tQ_=p+ES`ZuQ(t
)f/?0C-=>6,(B#b&%ZJfEMaD6Pr8>3Urs6LTU(B;;\.'KTHrjD%+N[5feQDiWRb.:@o7N>u79F&S'*>.5##mZa!;SV=r!_E"$4STpr<f?"?M3YF['dGP
#=1TtG;FisQhP6M7Y?9i7mBgCfm4,'^fgu*[-i9D?B896JRpV8=_>cKC:([S2#H@AR-4d_\NQb5R='LTl[Q0/)jj=K[siTlK)5u6J8<gET$9+)//B^ju
R1MNNei<]5f<r+AWM7Cqk#M#_o:ii;,;cnE9E4p5,E6kD;0H;1BjqpE9biW&4O"UH4d/4iE2-L@7hDs6-63Bb:%h9\bMp>\QS`D];V[Xpa@5/Z9q7ptW
%4kG!7bl8-/4iB-`MAi:P?+HHRE5DIbd!'CE&">h]#\2`'S8oTo4eHN;1WGOjIn:KQiqJ>AQ9G)7_b8HWb^E,#s7)!'H9Fah@611k'An=UHpsuL]&;&1
secqp<@3)IH?7&W@b-8RgPRb/Ga#FJUjd8m"!hlo@;P`$gr=l#t8fl!9)\n`[\.=E'Bb?p0X$^QXg:J>LOFLKgb$D_R4YI@qq1[fL:C1FWPOH5FePRpo
-ug+gaYR1T@?JD:H52)>K+Q[(!ceddNB;Eehd)pBFrT$MJ[J?4'j<:GAqRg48iE6.:.fcD#&5IT>V9OfX7YIRjl=4`9Pq5'l1G?m*-i[/g_cB+;Pi$c_
kJ9QeeT@UELS8h\naqj<K!+!4AIO#^a[N0LBde4Y_W.iT`M=EPpO4HTa&fhY_lblSAd3hK8;YhC3kd">A_9;hi4cD+Gb2knn.DI*:0/A18R%"KJH5:Y@
3C\+mW^([tsd&rKK?k>O)jf^9b0ZjQ(,a916cb!;7:/q[:Z<(E8XDkGG):&e5VFTNI!oq38RKU4rgl?!>35-_P4koe,*<p=?l63B2iV:+Y+q)3>W?g-g
=Tud-&f+[aO+]DGjqL9>HS1C-^>Bg[B,0MZMfD3:)\a;F6>#$h_PoX=OW;k[#qO_/O:t?n"DaYf64NP*=';6G9?VS*EfO=^7@MDnR+]W*31cH.c$Gsh[
.Z@rRV7&[Va]"c20QP3Z\P&d#_1GSVKEs,K$ek!L+#H:Fq<a%G;RJ:eiD)TP1@QL2k!b_g9YR5_@Ah&1j`PHNBt`B6_,j%k>#p4c%])Z_goj!hP&?q,/
s%=%sS@_N9e9C'i9,$%&M/f`gD3O'P!:CaR8ibncd_/A&i?[D1a\Fh]/k(e?\2?[@s:22p6j*fBRX:^sSUCr:1uY_5rU"2#gACE`4prZf``NAlc(s9gU
cOqp\.2lc4if*pk(4n+QC8\.]MMEC%$3Y?uBk]2a+tQX(;e;>4lofIILRYbZ5mK^6c.E`N`a@nu)3`'G#ig;7l7D&/!-crJ+L6o6HJKrEsq==+H8?!qD
,53B5`*\FPWb=_@<=^1qUQ6N#AVA5J\e;qc'=.>Ll;r/aS/Coks)*jIH$E-:'KB8)e3k;n[Io?P@erYM@Hsh']Qq]7pXmre$AaL0*gh0B\c?Q't8PPJh
rY<[dc)"[c%bFgh9t]/>bh8bn9"%'-9Wj?uirid[kqe7[PQaUAdGgo^Ha0ChHr,`I_m[$D%hm2ammSh`GTHb!Z9'n&eI$]OmHo9/UY-KpK4TL6;?;d31
-]up_Isn#`XC"nN$*<Ggo]B=Kf]V3jsA`u-+.S9fbtQp79M2*-1rMkc<\Wrn9UJ*7oOO9GSbdT+R]s#>,#QfJ9j_p[b=l(K!1-km4-d1]3E8.`q_!OTF
OR9K%&?U^L@Y;4ZsCdXgU"+m7O7FQe:[tXS(M*VEXM)g]>B)ZU[B$IKP?UQOtf%n`=Ii/0=q]e!kI1N/);eOUF<hq`:!L&^W5Y<uZCX(4,#/jNuoCs)C
*tlcJI:AVt_Si!t(>l9QQgUBLT!.-8cMDglbV?<(L>q)+BV*h%`RcjUJ]Im`JZ$>Ib/@!A1!c3T:@Vf/%:fTNSe%'lIpp6+k6cNg@>VM\MB^#nAT2YXT
%D&g[r(8#&sNbblW/d,"6IC7EoQDkCq:1%SSkDCDc#Ef(D#R#*K5VronFdM00GlmriS)abD&uR*KJ'Q)D!D-%dP4OsKR%<L+l07I"RHY6/f,'uR00s8G
Y%3+Bbp2CR>"#K)$_&2Xdq(fO,]Uq7C$Pt_`4$5R6Q7jk:6,Aum[So_C:(bAq"3AQ0,UV<bnf9V%*s8rB_[@@PDdlq=>kIASHE=#JCX`Zl68tH`bibtP
rr@QM2kHc-/'aE#V$V0`JTt3>(LoMc3JD!UnGGGTOdPF\2-"!4jC_rZ`-(f-S$f!a&ME>H(,I#^AYOPi_ai\Jg*'UmSk3_PPT-E8@P()O6ZK$V7.t@(U
_ht&YsEp_SDU."Bn"Q\MtX%#YrN\1566c9liQl!QDEQ?6mEKjuCN]R#t2b[lM4>BMlYRQU3m3j@he%RZZhnM;d]c.jD!_gV@SEm$5G^GRd,HCKi+dB^B
1]A'_p3]b(+&+$Ig.B2C+@Ta@=E`?b!f%og"HTuTG-Im#q,Wu_j,)"_Ze$9J8^n[IW2[QtWbg!NFoGGJk+'):Z)mDc[El&^5F&r9HR>4#U/K8`36gZ-,
d^aRN'Bf_3S/u*L);kciie=heI79>HXWaSo"D"f#8TaWUh\op]VE+U=OYEQQiZKH9CQ1"=ZJ+2`Yn"1U`^]0u$jPI?VT"N9KXi$WrFU19Sj\4-\M2a8+
I[q?h,/"cX;SKhbCW.VL.'<>8ae6&YiBus2jKR&,W<iFP5MTUkk/3<`QL:*4hJT?n7m?T<2u6J&4IHeFe%J],SAc8Q*:D!o@$URhb>&2*n_nF;)[Oisf
HC.$6*3&GG$K_RJQF'Y?nuX[ZBCLrk3#g?bnfeg6<W?&d2$;V\'[RT!N4TYS-'Wq/,m&-fr!D\Q2>R46=h-=-?K3(c7L<0!jF[[)?n+FFNbQ@)U61KpW
eTMYSWGdl:ncM$pYBVX*eXF7G@%8:R?Hq_7Z_]g=VZb=\foN.$6g$e":(gdjHK]b=i'\H=+Jkl\hia3*[9s?1sPXXDe/SEM[WRX<uo9SApTHR4D[cQ)!
^"dm(M)'Hak#<:P()<UbS^p/P&I%3B0-6JD0m<WL_RC9-<%qkrp`S1PP?2KMZ8lfFMYW0EBT1hhd(-JJi%:EPKR&p]!@&D2ICm7O?oTnu.-X^Y^umkD$
ieFHE(">.'Sr0/lmBqMf=2!$WlBJin(@P=OgRY<1#^5\q!.`Tg\q,RSjMk(:[6Aa-,84;oXamR*!ON!nr7u.H%EL.(P'OA<R9#e#mA7AAt1do<cF,9p'
Q`Mo3A=jcc.;UEedO&o]L:IEA@(/F6S<T_Ce?8*g;9An.og)*Q.%=5@B*P;Cp-;dpe:mTb=H<n@SFs)oLA_FE6o];44i^UHLhS4j$Ds0Z%jddr]Iegng
Yk8YP>XQDjL\G\rnM?A/'7[_mZ/VcPeCJZVd*:Y9;+!*%\V%<-)u1o2'6%*"IE4?hCu!,PF@Qm@V]$&ZF<Cd,TF=rGI%pW=32SS.7YhaMk8)2<F2J.(l
sG`@K\8lgj$HikD"o+DoSY;X*L!&>p4;L+K3eRpa_BS*f[3OP-uT#6=Yp>W+WV>[D5VlAo1\sXJZ`ZV=RN1[mq=351;,=kHhPc-u_[QJRgQYD$2T`2/k
Bl[Ml[=>!ARm),+@qJnSi0'2!(#3`bYd1^$p[K-[B3B3VeZSrSO.E!@UV"O*]q11ZEeSa!+n:CR2/:jGb[=J=`+DP%NsDpQE*06tD;h'[`9K<[uPZdF#
DQ>`:b,ck.A=Wp3jFWGqg^V'"rq/.mX4k-KFUl/>_,cmS`+OlADCm#1YiIG%S[E'WWl%L#Q@.T5c+ALZ;^mHo^UX8o<RX@j,RJSIcHEq-i#5Ua7Oi3oB
JdWW#19^,uCr%Tli?p.PG:)RH0Zf3kF?Ui-,Xm@lbBHFR!gk3"c1o)4K$+1X)hd)%nU`g1HRDINQOf+J5J-qnLb]rGqrmH?Z'FmW@"VZBcg*sDGdnnq#
Qr+EoG'JY663-C25;/@&'VCN*mFb-#AGdr6gm_(__NVd9O[]3c^*Jq[71t:Z\M8k0jls]7cap[m%tn<"?f.p4$G+MPjOnb2:hMUe+O+C,7T\ina$7u=a
eZm-B$/>VbR:#I;;5Fff-a!`Mp[:9<htP'C&a2)0^3u<nGR?.Z)jI"9,$R`WO]Sd/"Q=(-@=B]&o$eE'!ogn3D0.4?JTl[u8ZJ(bDK`8>:8?h4YR6^)7
+-/aXDDJAt4trK`)-h0\u@s8BVY5<NmUZ,3@D'gQuEKtK_eq%+I^O-2jCGrEM&_kZ!*$A(R9e%3P9L<q$;qE#d(9])QFq0"M&#uae84B*CdI^0\[3jX"
p#^W"Lon3g60p+N=T3@Hl;ps6n*?C4<P;fRF'+qu%#_2sRS-(R\):9&cG(TDo9docf<&Z.+PrMs!(0Mb/%tPu4#ZkB=,5jHU7&\6Ha?>b@QA[&<XjO0c
^:kEiKeiAOD!d*K:?;\58[/7Bd%;KASkO_4dHPJ!Q28ST4@o$b$TZ(Ec"T3Ziek(C[AHhUMstUVG.'AQKg2:@*%03BKdQZ$.%]F@`!a3r^$TSQqIa#f?
0g2;5Xl>0XdJ9b@QRq=UW`7[QVbd;a?08GCPkpORStI94X6.n`O%5M9a76210T).-[;<u6''bT_q[t(_#7qI%,cc#C/U.lR,VX]ah2$Z)TO*s/Z3FY,M
Ob-40ZWUg5-pi5Z_G$$P,*Pb!T[:"9`41E%5V6l3oJP+gWDRjA8!l^F.]c8ZMgpLPd[FLO?W3,mFf>Mi26pAaAQLBQ`tFku1Cln)&Kb@#Yd"1n\c9REh
ttNFf@jC"Wlb:\o]l(H#hi'5l`M=(A^ORC!uJ,SilY,gF9bcfcu@KOVDh+f)Jph2+fgLk.Q-^inPKhQp[RHc!Z\8mUfN*-!XoQ!6*/?+J]5#YG5hp>J;
iGYBR!7K8Uk-cIpJ[LNqW4T^=aFN.ZJh7I^OCu2bO7EsbOYZM5BnX@&o8GU5\U*uDaG]#Im-q&$aT+8$Qa4Z/NpNg/VB+;Ch1$p)?M85!]98nh%oc?,Y
m$i7sM6:R[h034Ls5sk(2@jFMdTgL<Vj!$;b'$lb1b8J]AW([:^sq_&cY$YSCsQkcft7(>F#3-)Z7D7l[1?2&;N]UFM4<LB91WeoAUmB+2Q]e?d\jLE$
jqD-9&KG6N$YGo9H5Y"ag;j$Lsk7\V:n>#niBN:4JS2l)ao[oml&JG@V=Gc<A`*g?AIC]]!Ng)e,K:;Z!N_H]=a^tG5(1SH),SXl%G'8l,gPLl1/"o+,
/ZF2ZH61r=p)p>OG_neiE%TYr`]!\3d)<!ns"7BKh,aH?^u4N_--IN,pJM"Ch==#2c-k./Zp7_#<<DF?.BP+e5pVE6;c>p50fjUWuIsXG^s3m3eR6jMl
iRE4j+r(WG-mq8,mZQ`ht#=1O;imIJ+Tj%MnNRA;G-ioG8%B0Gr_j3@*S,m)S\-?PaoH`=4%+%Yi4a=!&Rh;CN*Nd]MR3qWG!)D5q5W)S(+pZQ.CZ^"F
;10ZI@fQNkhWWT(HOq>LP3JGuCkMajX(A%N[IB@jZP0CPIi&R29OsT:A5fdg@g:%uUX`c@aTCucSFY]HN]6$)*W0&Hubss!hTjTuK+<\Cgj-*Fl[R5rN
1K^`UQ=&aF0U?mpGt(EO8E9kA#]P)(9Xs.%k\-?$R?4U^h@-P\QP4(NL!kKD"eV%F%3rk5k>kR,<SiPA:9\"&H9UAlL@Wa3ek3DF(PEr15iCE,@&YJlE
BqH:P1]JA4Q?XKP?/<P/qO,YbR-G/%Qei]d[<la/"$C[4[;?26;fH>I6l-GArDhI-`8>eIV!ce&d,YnpKgB!S!@N),sX!]),/fUH`*,pa-5TgXuEeJQR
;,!U_r37N2M+ZKC;FWe6ZXRq:Df3SS!2W>OOuEFnk^#oUi_"d;2;8rHXH_fkVtu3__!b\'9F$anSn1BNaa=0m7P1_?O3Fp;&i;AC%.BM1J`A$hP,DT:Y
&!bgFd&Ab3CGr.hhR6RTG?gL(!0Gi(CWhAf"]r_R1oonu[sifHU]56B>iL+`m;4JK;=,9Y!PABQVN1.VY_s!oj$AUmJDWB8,(9YP+/3O^]A=qM"WB0Zq
e1rfsF7]1`Xhbse`BDp:__+k%a/_5K09YEoLBo&T\#0;)EMRCCOKH4%a;Q_oMAu!2a+>eN)+VBnQYn]O!0+\!m0AOj6l#P#l:+uDUj"_-8VhWfZc,&K^
.aQaS,&O`Y$XXIpKqad$*orZRDF%A@:q"F"6]hItf9MuibNp"4B'qjn*$qs?K5j8t:8VkSf^mj;mLtp*BjQVc*S5375^'K^n,2R?E%?6mBog#HF<AY>j
>Xeq<p@SA@TIA*@WRgQp(8M;]#H6Sq^^!$\a'KQ`",5g*5/G#S8$6j)kqj!UQ3Qb!pFY@)I"@b8Y!J0r*[/+$.$eHR#>a6f\f*.9[5<U.msnWf'Y"6!V
G#A"]lKda)R??TnPo::Sb9T9Ge3'3ttPq#I#n@!mCR\-3*N%Ggsg-_FN_mC@!.BP<(,`Yqj58Ya#u&\Q.!`$q1BZgsWGF&d6h'W/H(%PUD.+RDZ\26O!
Ih3L*\/Q*c6[]%FM2!)gOoeJ0D)D6Ff7:#?#\BdS-BRJ-Gu55GH$%d(QLYL8'QZu'hgk5D<-\P:0g8D:&#--%82&c'\.=VT2"Z4H#ESXd:((MQO<mMtV
OkK50:@9:Gl4d8I%</npF+1,Gk46:Wj/8M-r#hM<gE"(Z#^-aAFlEtC%3(k;+j*9R$9]7&G8..g#Rk.X(;lCB1NoSl>3)M;MJPS@*%R!pd7Q;$j-+8*.
NG/mPg@G7Qnl-Y'fu"s@2%(W$`><@TL?s.5^\sLk+Ss12V$E`)5/[G$]NRLW$>E%a4jbSfECsl[q4aA^F5r-4]4X=q?Q>^3US"mbk>&'n,MuMZKt2k:/
O2*Z!.dS1iZX^KO09rI!`hjl!6+=jFJZNb=%Nqk]h"+XEe<!n$=9TmKI_-oeu5AudX0o>J5Nh@1,dJCU+GJj`n]t'.fa#&1+6$/jdi'<nV!$FLFP_2VS
bH\(RPH^P)AH4,!CUUNR?]!Q>C"gL]5C;9TU+-f<W'VZ(L"T5p')Kjo<S*aZB40(qalZ)T^lXD?4!tM0Mc"q;Gp@iQjJoYR1pfJ_%NgN3#o(3UXXgf'[
.0qH\?%n&DcIq<QYOarK=Te)C?@R&o2]Mu)>MVL=$k?j>VG"e3']BQ?_C"9LINHAqZaUPEu#cF[@V5-LC`XD`\,l6aqJb_P%b8r]3:@=p5I=rpr(Q`F.
?F^n/i,u'mo.[!Y<9\M,g'M<gri+:N@/m6^]3/W(e>hWlYNjB_aH'VX>q.DXr+8/GGI*9&cih2a9H`.:mpA8S6:C!(;qZ5T!+T)^,6e&a)TcB,+UK11p
cQQhD2G^?LFJrg1OWcDpjsC-6RZ!C?$:F(U1ZmDs#Ih,cXb^H!4<"a5,S)J^3g<qD`i36_A4M8=VH'^7L0CQ'j7]tK<^j*XB+KK9A.ibFd:mt+qc^`XH
"B^b3#R]`]2)ii#I"[a*Oi\;pE\QIX;TaIGQ-RolUt>[BpYPIo>)<;N:D[4-Z#T!$8oF#GYr0:Q8P<.%*OhAh)#KLT;P,i\%ie?41USk=*W_<^2sQ54I
Ib?.!h1,MhDuNa;K94kObo3R[u(M[ALZS]R'MRkg>HPT=t.oRPh<qc$Tcr1J*f1_r3YY[`G<-EoP^4DW4E7f[WhiI8YnP1*.jp`VFO/)J^Ss<AFCp0FU
EIcYJ:pS&qe0J%\*Ag$%pA0L6k9l"eT,K;.QMpZWp>*XSnpkj8p&i%0ZSUn\%UPg"1E_MaQX42.%d;h)LubYKpIK`:tZ5PN%(Z"l'B/^E[9qclW,QY^4
Tf?oHf=mn;hs0s=iCr.O=TNU'tE<"b:XI<:e2-_)W4^Vt^Rrp[$lXYBEUX%mZ?@Nj[[m?ISJZ:*eaC0ZT@HRsbQCk"O35)"E6t`T[I3OUh*a*<Pq41?6
Q;$_-2n\)rUS>%?pqA'MSg4&;j:Qg$#_cj^Yhj_>VdU+)COTX\VZGF4bM;?D]OuSC)r@L^A)5DLFe4DtAOS]t.rt7?rLZ<es5sp]s5h/qJ,Sm90-B'Ng
P>NQrUBgD9m\j4is+FeD3Ssh-)bP)J"'3gaJFYgWIVn`f+8\P_o?Oq+S7H#?ZmD_5/7Lq/9kaHRgmhI\'An\=Dt/P!'F(7%SY3uKp^gIA'WiuI(<'D.P
_PHcH5/'JOBS1._r-bHNI2teHijNCRYFCN9`dg!kBC\%.<2YY?VMM*VIH#bAj/;Ou+)>NtcZ6X3?N67@'1],oY"\B+$9)m_iSQjIMF)\HnBfLikqpP(T
:5Zis%\jGb3ee'Gf]i*@T5j,1FUF'u90X#b*3HfjW.Z&Gk(5=[9J&60jnlhpg`1Pu^0-\:2(aS9kTWAj;&'mU?[TUc&+_YWg=/p;.2.hJ%8#]_:bWS;2
Z*/^$/C*)6m1;40NXj9PQ,5;8SXVue*0pd7;gb]Lr7RK"/K.+r#8Dq2&_<"ag"'[[Ypo3%Bp(Mtd7Og?s6M*N%6)OtW:BUX6:'>b[[8&sbj^.d^[iPWU
6M&jA\>4:#ar_(oKRquImlqR4*\8,52.1T>Pg`;5ZH.hrFpF8G"mBLETQ/OR,1C;^MB7bk2+SAXJ^=3AFSUsod1dhp+_]p]n#GRi_b5<#]=dY-0,Q3q?
a;P9NISl`Weg]-A8ItNl:0VMgB:_[c)j</0XK4*].epOG0.G(T#.<N)QE4p_aJhm\XnF3faLa%&*rmhe*]!$XOXE(D^`!L\:4qUns(q41GNfAek4/?aU
Su*B!NA4=d\Pf@V-t!Q'd-E^.QU&-MohY=!mh3g)IDj=F3:t_?W!rj(=R977<b,SrYplU0dRT@bupa.kU[ubD\fc\Q.c5KCicJd\3;Md`WP\:$ogMO?/
C<3BJ?l<OK&Noi;b?Df/eLFsW>F&Ll<#O6)[G9u+)PWklnSoouXCYIgn=OD3K\@_C<pAnqP4nR['12r!uZEa^bVDd=kL^On,m@:l+JT,X2D"Fk<$jq[g
)Q'iHXkGufhJ3RCRjsTrqgW]ToaK/YY9>p3m:8!FNfD2s?TmRHdB03iP<fRF9TTbkdXB.SlSOjVSFR.Wu7Bka/9JHG%db6Q0*Yf3Ca2C@)&b1Br4T?58
nH2<^X[L2YjgA-Sg.m(D/An5])BGLCH?jCS4c4('1RS[\_VTM,IflP2X^_'''
	exec(zlib.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.44'
__version__ = version

# -s runs for hours, often into a log: don't let output sit in a buffer.
print = functools.partial(print, flush=True)

EXIT_OK = 0        # healthy
EXIT_PROBLEMS = 1  # device errors, scrub errors, missing devices, or a filesystem forced read-only after an error
EXIT_FAILURE = 2   # could not check: no mounts, unreadable filesystem, a scrub status that could not be read,
                   # a scrub that did not complete, an unreadable /proc/self/mountinfo or a filesystem that could
                   # not be asked whether it was forced read-only, no root
EXIT_INTERRUPTED = 130  # Ctrl-C
EXIT_PIPE_CLOSED = 141  # the reader went away (`statbtrfs | head`): 128 + SIGPIPE, as a shell reports it, and as statblk does

# Colors (set_color(False) blanks them)
_ANSI_COLORS = ("\033[91m", "\033[92m", "\033[93m", "\033[0m")
RED, GREEN, YELLOW, RESET = _ANSI_COLORS

def resolve_color(mode):
    """--color: always / never / auto (a terminal, unless NO_COLOR is set to anything non-empty)."""
    if mode == 'always':
        return True
    if mode == 'never':
        return False
    return sys.stdout.isatty() and not os.environ.get('NO_COLOR')

def set_color(enabled):
    global RED, GREEN, YELLOW, RESET
    RED, GREEN, YELLOW, RESET = _ANSI_COLORS if enabled else ("",) * 4

CLEAR_SCREEN = "\033[H\033[J"
EVENT_LINES = 10

class Screen:
    """Prints status tables. With redraw (-s on a terminal) each table replaces the previous one and
    recent messages stay listed under it; otherwise everything is appended, which suits logs."""

    def __init__(self, redraw):
        self.redraw = redraw
        self.events = []

    def event(self, message):
        if self.redraw:
            self.events = (self.events + [message])[-EVENT_LINES:]
        else:
            print(message)

    def flush(self):
        """Print held messages when no table will follow."""
        if self.redraw and self.events:
            print("\n".join(self.events))
        self.events = []

    def show(self, table, notes=()):
        lines = list(notes)
        if not self.redraw:
            print("\n".join([table] + lines))
            return
        lines += self.events
        print(CLEAR_SCREEN + table + ("\n\n" + "\n".join(lines) if lines else ""))

# Prefix each btrfs command with sudo. Set by acquire_root() for the per-command fallback.
USE_SUDO = os.geteuid() != 0
MAX_PARALLEL_COMMANDS = 32

def _is_root():
    return os.geteuid() == 0

def acquire_root(argv):
    """Make the btrfs commands run as root.

    Non-root: if sudo allows re-running this script, re-exec under sudo once (one prompt, one sudo
    log entry per run instead of one per command). Otherwise, e.g. a sudoers rule that allows only
    btrfs, fall back to running each btrfs command through sudo."""
    global USE_SUDO
    if _is_root():
        USE_SUDO = False
        return
    sudo = shutil.which('sudo')
    if not sudo:
        print(f"{RED}statbtrfs needs root: run it as root or install sudo.{RESET}")
        sys.exit(EXIT_FAILURE)
    command = [sys.executable, os.path.abspath(__file__)] + list(argv)
    # -l: may the user run this exact command? Without a terminal, never wait for a password.
    check = [sudo, '-l', '--'] if sys.stdin.isatty() else [sudo, '-n', '-l', '--']
    if subprocess.call(check + command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        os.execv(sudo, [sudo, '--'] + command)
    USE_SUDO = True

# Each reply is the command's stdout, then its stderr: btrfs reports some failures only there (`scrub
# status` that failed to read the status file part way still exits 0). The parsers skip lines they don't know.
def execute_command(command):
    if USE_SUDO:
        command = ['sudo'] + command
    return multiCMD.run_command(command,quiet=True,with_stdErr=True)

def execute_commands(commands):
    if USE_SUDO:
        commands = [['sudo']+command for command in commands]
    return multiCMD.run_commands(commands,quiet=True,with_stdErr=True,max_threads=MAX_PARALLEL_COMMANDS)

def btrfs_not_found():
    """Whether btrfs is missing from PATH (multiCMD's quiet=True hides its own "Command path not found"
    line). Behind the per-command sudo fallback, sudo's own PATH decides: not checked."""
    return not USE_SUDO and shutil.which('btrfs') is None

PROC_MOUNTS = '/proc/self/mounts'
_MOUNT_ESCAPE_RX = re.compile(r'\\([0-7]{3})')

def read_proc_mounts(path=PROC_MOUNTS):
    try:
        with open(path, encoding='utf-8', errors='surrogateescape') as f:
            return f.read().splitlines()
    except OSError as e:
        print(f"{RED}Could not read {path}: {e}{RESET}")
        return []

def parse_proc_mounts(lines):
    # The kernel octal-escapes space, tab, newline and backslash in mountpoints (e.g. \040).
    mounts = []
    for line in lines:
        fields = line.split()
        if len(fields) >= 3 and fields[2] == 'btrfs':
            mounts.append(_MOUNT_ESCAPE_RX.sub(lambda m: chr(int(m.group(1), 8)), fields[1]))
    return mounts

def find_btrfs_mounts():
    """Sorted btrfs mountpoints."""
    return sorted(set(parse_proc_mounts(read_proc_mounts())))

# mountinfo keeps apart what /proc/self/mounts and statvfs() merge: a mount's own ro/rw (MNT_READONLY), before
# the " - ", and its filesystem's (the superblock's), after the type and source. btrfs sets only the superblock
# read-only when it aborts a transaction after an error ("forced readonly"), so its mounts keep rw. A mount -o ro
# is ro in both. fs/proc_namespace.c show_mountinfo, the same in 3.10 (EL7) and 4.18 (EL8).
PROC_MOUNTINFO = '/proc/self/mountinfo'

def read_mountinfo(path=PROC_MOUNTINFO):
    """The lines of mountinfo, or None if it can't be read."""
    try:
        with open(path, encoding='utf-8', errors='surrogateescape') as f:
            return f.read().splitlines()
    except OSError:
        return None

def parse_forced_read_only(lines):
    """btrfs mountpoints mounted read-write on a filesystem that is read-only."""
    forced = set()
    for line in lines:
        fields = line.split(' ')
        try:
            # Fields 7 on are optional tags (shared:1, master:2, ...) up to "-": then type, source, its options.
            dash = fields.index('-', 6)
            fstype, super_options = fields[dash + 1], fields[dash + 3].split(',')
        except (ValueError, IndexError):
            continue
        if fstype == 'btrfs' and fields[5].split(',')[0] == 'rw' and super_options[0] == 'ro':
            forced.add(_MOUNT_ESCAPE_RX.sub(lambda m: chr(int(m.group(1), 8)), fields[4]))
    return forced

def forced_read_only_mounts():
    """parse_forced_read_only() of this process's mountinfo, or None if it could not be read."""
    lines = read_mountinfo()
    return None if lines is None else parse_forced_read_only(lines)

# A mount that is read-write on a read-only filesystem is forced only if btrfs says so: `mount -o remount,ro` of
# one mount of several leaves the others looking the same in mountinfo. BTRFS_IOC_START_SYNC (_IOR(0x94, 24, __u64))
# starts a commit of the running transaction without waiting for it. A filesystem in btrfs's error state refuses
# every transaction with EROFS (join_transaction, v3.10 and master); a filesystem read-only by a remount has no
# transaction to commit and returns success, so the call changes nothing on a read-only filesystem. Measured on
# EL7 (3.10.0-1160.119.1): forced EROFS; a mount beside a remount, and `-o ro`, success. Decided by the errno only.
BTRFS_IOC_START_SYNC = 0x80089418
UNTOLD = "untold"  # a forced-state value: a candidate that the ioctl could not tell about

def start_sync_errno(mount):
    """0 if BTRFS_IOC_START_SYNC on mount succeeds, else its errno (that of open() if mount can't be opened)."""
    try:
        fd = os.open(mount, os.O_RDONLY | os.O_DIRECTORY)
    except OSError as e:
        return e.errno or errno.EIO
    try:
        fcntl.ioctl(fd, BTRFS_IOC_START_SYNC, bytearray(8))
        return 0
    except OSError as e:
        return e.errno or errno.EIO
    finally:
        os.close(fd)

def forced_state(fs, candidates):
    """Whether filesystem fs is forced read-only: True, False, or UNTOLD. candidates: the mountpoints that read
    read-write on a read-only filesystem. The ioctl answers for the whole filesystem, so the first definite answer
    decides: the candidates are asked first, then its other mounts (one may not open for this user: a mode 700
    root gives EACCES while another mount answers)."""
    asked = [m for m in fs['mounts'] if m in candidates]
    if not asked:
        return False
    for mount in asked + [m for m in fs['mounts'] if m not in candidates]:
        error = start_sync_errno(mount)
        if error == errno.EROFS:
            return True
        if error == 0:
            return False
    return UNTOLD

def discover_filesystems(mounts):
    """Group mountpoints into filesystems by UUID: [{'uuid': str | None, 'mounts': [...]}].

    Subvolume mounts of one filesystem share its UUID, and status and scrub are per filesystem.
    A mount whose UUID can't be read stays on its own (uuid None)."""
    mounts = list(mounts)
    shows = execute_commands([["btrfs", "filesystem", "show", mount] for mount in mounts])
    filesystems = []
    by_uuid = {}
    for mount, show in zip(mounts, shows):
        uuid = parse_show_uuid(show)
        if uuid is not None and uuid in by_uuid:
            by_uuid[uuid]['mounts'].append(mount)
            continue
        fs = {'uuid': uuid, 'mounts': [mount]}
        filesystems.append(fs)
        if uuid is not None:
            by_uuid[uuid] = fs
    for fs in filesystems:
        fs['mounts'].sort()
    # Stable order for the table and the scrub queue.
    filesystems.sort(key=lambda fs: fs['mounts'][0])
    return filesystems

def select_filesystems(filesystems, patterns):
    """Filesystems with any mountpoint matching any pattern (substring glob); all if no patterns."""
    if not patterns:
        return list(filesystems)
    globs = [f'*{pattern}*' for pattern in patterns]
    return [fs for fs in filesystems if any(fnmatch.filter(fs['mounts'], glob) for glob in globs)]

_SHOW_UUID_RX = re.compile(r'\buuid:\s*([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\s*$')
_SHOW_TOTAL_RX = re.compile(r'^\s*Total devices\s+(\d+)\s+FS bytes used\s+(\S+)')
_SHOW_DEVID_RX = re.compile(r'^\s*devid\s+\d+\s+size\s+\S+\s+used\s+\S+\s+path\s+(.+?)\s*$')

def parse_show_uuid(info):
    for line in info:
        if line.startswith("Label:"):
            match = _SHOW_UUID_RX.search(line)
            if match:
                return match.group(1)
    return None

def parse_show_info(info):
    """Returns (uuid, fs_used, device_path, missing_device_count) from `btrfs filesystem show`."""
    fs_used = None
    total_devices = None
    device_paths = []
    marked_missing = 0
    some_missing = False
    uuid = parse_show_uuid(info)
    for line in info:
        total_match = _SHOW_TOTAL_RX.match(line)
        devid_match = _SHOW_DEVID_RX.match(line)
        if total_match:
            total_devices, fs_used = int(total_match.group(1)), total_match.group(2)
        elif devid_match:
            path = devid_match.group(1)
            # A missing device is listed as "path  MISSING" (btrfs-progs 6.x: empty path)
            # or "path <missing disk #N> MISSING".
            if path.split()[-1] == "MISSING" or path.startswith("<missing"):
                marked_missing += 1
            else:
                device_paths.append(path)
        elif "*** Some devices missing" in line:
            some_missing = True
    missing = max(marked_missing, (total_devices or 0) - len(device_paths), int(some_missing))
    device_path = ", ".join(device_paths) if device_paths else None
    return uuid, fs_used, device_path, missing

def format_device_path(device_path, missing):
    if not missing:
        return device_path
    return f"{device_path}, {RED}{missing} missing{RESET}"

def parse_device_stats(stats):
    # Multi-device filesystems print one block per device; sum each counter across devices.
    err_dict = {}
    for line in stats:
        parts = line.split()
        if len(parts) != 2 or not parts[1].isdigit():
            continue
        key, val = parts
        key = key.split(".")[-1]
        err_dict[key] = err_dict.get(key, 0) + int(val)
    return err_dict

def color_error_count(error_count):
    if int(error_count) == 0:
        return f"{GREEN}{error_count}{RESET}"
    elif int(error_count) < 10:
        return f"{YELLOW}{error_count}{RESET}"
    else:
        return f"{RED}{error_count}{RESET}"

_SCRUB_COUNT_RX = re.compile(r'^\s+(\w+):\s+(\d+)\s*$')

def summarize_scrub_errors(summary, following_lines):
    """One line for a table cell: the error types plus the non-zero counts indented below them.

    btrfs prints e.g. "Error summary:    csum=3" then "  Corrected: 0", "  Uncorrectable: 3", ...
    """
    parts = [summary]
    for line in following_lines:
        match = _SCRUB_COUNT_RX.match(line)
        if not match:
            break
        if int(match.group(2)):
            parts.append(f"{match.group(1).lower()}={match.group(2)}")
    return " ".join(parts)

# Older btrfs-progs (EL7's 4.9.1) put the scrub's state in a sentence, and print no rate:
#   scrub started at Sat Nov  7 02:56:56 2026, running for 00:00:05
#   scrub resumed at Sat Nov  7 02:57:08 2026 and finished after 00:00:26
#   scrub started at Sat Nov  7 02:56:56 2026 and was aborted after 00:00:12
#   scrub started at Sat Nov  7 02:58:27 2026, interrupted after 00:00:05, not running
#   total bytes scrubbed: 1.25MiB with 2 errors
#   error details: csum=2
#   corrected errors: 0, uncorrectable errors: 2, unverified errors: 0
_OLD_SCRUB_STATE_RX = re.compile(r'\s*scrub (?:started|resumed) at (.+?)(?:,| and(?: was)?) '
                                 r'(running|finished|aborted|interrupted) (?:for|after) (\d+):(\d\d):(\d\d)')
_OLD_SCRUB_TOTAL_RX = re.compile(r'\s*total bytes scrubbed: (\S+) with (\d+) errors')
_OLD_SCRUB_DETAILS_RX = re.compile(r'\s*error details:(.*)')
_OLD_SCRUB_COUNT_RX = re.compile(r'(\w+) errors: (\d+)')

_SCRUB_REPLY_STARTS = ("scrub status for", "UUID:")
# btrfs-progs 4.9.1 and current print these on stderr when the status file can't be opened (another reader holds
# its lock: rc 1, no reply) or read (at the very end of a `-B` scrub: rc 0, and a reply that says nothing).
_SCRUB_READ_FAILED_RX = re.compile(r'WARNING: failed to (?:open status file|read status)\b')
# What a failed status read shows: nothing in it can be trusted.
SCRUB_UNKNOWN = {"scrub_status": "unknown", "scrub_time": "N/A", "scrub_rate": "N/A", "scrubbed_data": "N/A",
                 "error_summary": "N/A", "has_errors": False, "no_record": True}
# A scrub that stopped before covering the filesystem: cancelled (aborted) or its process killed (interrupted).
SCRUB_INCOMPLETE = ("aborted", "interrupted")

# Sizes as btrfs-progs prints them (pretty_size: two decimals, binary units), e.g. "5.87GiB", "0.00B".
_SIZE_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
_SIZE_RX = re.compile(r'(\d+(?:\.\d+)?)(' + '|'.join(_SIZE_UNITS) + r')')

def parse_size(text):
    """Bytes in a btrfs-progs size, or None if text is not one."""
    match = _SIZE_RX.fullmatch(text.strip())
    if not match:
        return None
    return float(match.group(1)) * 1024 ** _SIZE_UNITS.index(match.group(2))

def format_size(num_bytes):
    """num_bytes as btrfs-progs prints a size."""
    value, unit = float(num_bytes), 0
    while value >= 1024 and unit < len(_SIZE_UNITS) - 1:
        value /= 1024
        unit += 1
    return f"{value:.2f}{_SIZE_UNITS[unit]}"

def summarize_old_scrub_errors(following_lines):
    """The same cell as summarize_scrub_errors, from the lines after an old "total bytes scrubbed" line."""
    parts = []
    for line in following_lines:
        details = _OLD_SCRUB_DETAILS_RX.match(line)
        if details:
            parts += details.group(1).split()
        parts += [f"{kind}={count}" for kind, count in _OLD_SCRUB_COUNT_RX.findall(line) if int(count)]
    return " ".join(parts)

def parse_scrub_status(lines):
    # "no stats available" (never scrubbed) leaves these defaults.
    scrub_data = {
        "scrub_status": "Never",
        "scrub_time": "N/A",
        "scrub_rate": "N/A",
        "scrubbed_data": "N/A",
        "error_summary": "N/A",
        "has_errors": False,
        "no_record": False,  # the reply can't tell a scrub in its first seconds from no scrub at all
    }
    old_seconds = 0  # the old format's duration, for the rate it doesn't print
    for index, line in enumerate(lines):
        old_state = _OLD_SCRUB_STATE_RX.match(line)
        old_total = _OLD_SCRUB_TOTAL_RX.match(line)
        if old_state:
            scrub_data["scrub_time"], scrub_data["scrub_status"], hours, minutes, seconds = old_state.groups()
            old_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        elif old_total:
            # With "no stats available" this line is all zeros and says nothing.
            if scrub_data["scrub_status"] == "Never":
                scrub_data["no_record"] = True
            else:
                scrub_data["scrubbed_data"] = old_total.group(1)
                scrubbed = parse_size(old_total.group(1))
                # Under a second there is no rate to tell; modern btrfs-progs show 0.00B/s there.
                if scrubbed is not None and old_seconds:
                    scrub_data["scrub_rate"] = format_size(scrubbed / old_seconds) + "/s"
                if int(old_total.group(2)):
                    summary = summarize_old_scrub_errors(lines[index + 1:])
                    scrub_data["error_summary"] = f"{RED}{summary}{RESET}"
                    scrub_data["has_errors"] = True
                else:
                    scrub_data["error_summary"] = f"{GREEN}OK{RESET}"
        elif "Status:" in line:
            scrub_data["scrub_status"] = line.split(":", 1)[1].strip()
        elif "Time left:" in line and scrub_data["scrub_status"] == "Never":
            # Until a scrub writes its first progress record, btrfs prints "no stats available" and no
            # Status: line, but "Time left:" only appears while a scrub is running.
            scrub_data["scrub_status"] = "running"
        elif "Scrub started:" in line or "Scrub resumed:" in line:
            scrub_data["scrub_time"] = line.split(":", 1)[1].strip()
        elif "Rate:" in line:
            scrub_data["scrub_rate"] = line.split(":", 1)[1].strip()
        elif "Total to scrub:" in line and scrub_data.get("scrub_status") != "running":
            scrub_data["scrubbed_data"] = line.split(":", 1)[1].strip()
        elif "Bytes scrubbed:" in line and scrub_data.get("scrub_status") == "running":
            scrub_data["scrubbed_data"] = line.split(":", 1)[1].strip()
        elif "Error summary:" in line:
            summary = line.split(":", 1)[1].strip()
            if "no errors found" in summary.lower():
                scrub_data["error_summary"] = f"{GREEN}OK{RESET}"
            else:
                scrub_data["error_summary"] = f"{RED}{summarize_scrub_errors(summary, lines[index + 1:])}{RESET}"
                scrub_data["has_errors"] = True

    # A reader that lost the status file's lock to another reader gets no reply at all, and one whose read failed
    # part way gets a reply that reads like a filesystem never scrubbed: neither tells anything.
    if (any(_SCRUB_READ_FAILED_RX.match(line) for line in lines)
            or scrub_data["scrub_status"] == "Never" and not any(line.startswith(_SCRUB_REPLY_STARTS) for line in lines)):
        scrub_data.update(SCRUB_UNKNOWN)
    scrub_data["incomplete"] = scrub_data["scrub_status"] in SCRUB_INCOMPLETE
    if scrub_data["incomplete"] and not scrub_data["has_errors"]:
        # No errors in what it covered, but it did not cover everything: not OK.
        scrub_data["error_summary"] = f"{YELLOW}incomplete{RESET}"
    return scrub_data

def parse_scrub_time_to_epoch(scrub_time):
    # btrfs commonly prints values like: "Thu May  2 09:56:55 2024"
    time_formats = [
        "%a %b %d %H:%M:%S %Y",
        "%a %b %d %H:%M:%S %Y %Z",
        "%Y-%m-%d %H:%M:%S"
    ]
    for time_format in time_formats:
        try:
            return datetime.strptime(scrub_time, time_format).timestamp()
        except ValueError:
            continue
    return None

def check_skipped(skipped):
    """-d skips the scrub of a recently scrubbed filesystem, never the check: a Status (rows, notes, verdicts) of
    those of skipped with a problem or a failure (device errors, errors the last scrub found, forced read-only,
    an unreadable status), or None. A healthy one stays out of the table, as -d documents."""
    if not skipped:
        return None
    # Each is read again as a one-shot read is (reread_unclear), or a lock collision with another reader would
    # fail a filesystem that is fine.
    statuses = [reread_unclear([polled[0]], build_status([polled])) for polled in poll_filesystems(skipped)]
    unhealthy = [status for status in statuses if status.problems or status.failures]
    if not unhealthy:
        return None
    return Status([row for st in unhealthy for row in st.rows], [], any(st.problems for st in unhealthy),
                  any(st.failures for st in unhealthy), unique([note for st in unhealthy for note in st.notes]),
                  {mount: scrub for st in unhealthy for mount, scrub in st.scrubs.items()})

def recheck_skipped(skipped_filesystems, before):
    """check_skipped() again, at the end of a run that may have lasted hours: (status, changed from before)."""
    now = check_skipped(skipped_filesystems)
    unchanged = (now is None and before is None) or (
        now is not None and before is not None and (now.rows, now.notes) == (before.rows, before.notes))
    return now, not unchanged

def filter_recently_scrubbed(filesystems, exclude_recent_days):
    """Split filesystems into (kept, skipped): skipped finished a scrub within exclude_recent_days."""
    if exclude_recent_days <= 0:
        return filesystems, []

    now = time.time()
    cutoff_seconds = exclude_recent_days * 24 * 3600
    kept = []
    skipped = []

    outputs = execute_commands([["btrfs", "scrub", "status", fs['mounts'][0]] for fs in filesystems])
    for fs, scrub_output in zip(filesystems, outputs):
        scrub_data = parse_scrub_status(scrub_output)
        scrub_status = scrub_data.get("scrub_status", "").strip().lower()
        scrub_time_epoch = parse_scrub_time_to_epoch(scrub_data["scrub_time"])

        if scrub_status != "finished" or scrub_time_epoch is None:
            kept.append(fs)
            continue

        if now - scrub_time_epoch < cutoff_seconds:
            skipped.append(fs)
        else:
            kept.append(fs)

    return kept, skipped

def poll_filesystems(filesystems):
    """[(fs, show, stats, scrub_status, forced)] for every filesystem, from one parallel batch of commands. forced:
    whether btrfs forced it read-only after an error (None: mountinfo could not be read; UNTOLD: it looks so in
    mountinfo and the check could not confirm it)."""
    commands = []
    for fs in filesystems:
        mount = fs['mounts'][0]
        commands += [
            ["btrfs", "filesystem", "show", mount],
            ["btrfs", "device", "stats", mount],
            ["btrfs", "scrub", "status", mount],
        ]
    outputs = execute_commands(commands)
    forced = forced_read_only_mounts()  # after the commands: as new as they are
    return [(fs, *outputs[3 * i:3 * i + 3], None if forced is None else forced_state(fs, forced))
            for i, fs in enumerate(filesystems)]

TABLE_HEADER = ["Mount", "Path", "FS Used", "w_err", "r_err", "f_err", "bit_rot", "gen_err",
                "scrub_status", "scrub_time", "scrub_rate", "scrubbed_data", "error_summary"]

Status = namedtuple('Status', 'rows running problems failures notes scrubs')

def build_status(polled):
    """Status of poll_filesystems() output: table rows, running filesystems, whether problems
    (device errors, scrub errors, missing devices, a filesystem forced read-only) or failures (unreadable
    filesystems, a scrub status that could not be read, a scrub that did not complete, mountinfo unreadable)
    were seen, notes to show with the table, and the parsed scrub status per first mountpoint."""
    rows, running, notes = [], [], []
    scrubs = {}
    problems = failures = False
    unchecked = False  # mountinfo could not be read: no forced read-only state was checked
    untold = []     # filesystems that look forced read-only, which the check could not confirm
    for fs, filesystem_show, device_stats, scrub_output, forced in polled:
        uuid, fs_used, device_path, missing = parse_show_info(filesystem_show)
        mounts = ', '.join(fs['mounts'])
        # Whether it was forced read-only does not depend on `btrfs filesystem show`: apply it to every filesystem.
        if forced is True:
            problems = True
            notes.append(f"{RED}{mounts}: read-only, though mounted read-write, so it takes no writes: btrfs does this "
                         f"after an error (\"forced readonly\" in `dmesg`). Once the cause is fixed, unmount and mount "
                         f"it again, or reboot: btrfs refuses a remount read-write after an error.{RESET}")
        elif forced is None:
            unchecked = True
        elif forced == UNTOLD:
            untold.append(mounts)
        if uuid is None or fs_used is None or device_path is None:
            notes.append(f"{RED}Could not fetch complete info for {mounts}. Skipping...{RESET}")
            failures = True
            continue
        err_dict = parse_device_stats(device_stats)
        scrub_data = parse_scrub_status(scrub_output)
        scrubs[fs['mounts'][0]] = scrub_data
        if scrub_data["scrub_status"] == "running":
            running.append(fs)
        if missing or any(err_dict.values()) or scrub_data["has_errors"]:
            problems = True
        if scrub_data["scrub_status"] == "unknown":
            notes.append(f"{YELLOW}Could not read the scrub status of {mounts}.{RESET}")
            failures = True
        elif scrub_data["incomplete"]:
            notes.append(f"{YELLOW}The last scrub of {mounts} did not complete: continue it with "
                         f"`{' '.join(scrub_command('resume', scrub_mount(fs)))}`.{RESET}")
            failures = True
        rows.append([
            f"{RED}forced read-only{RESET}: {mounts}" if forced is True else mounts,
            format_device_path(device_path, missing),
            fs_used,
            color_error_count(err_dict.get('write_io_errs', 0)),
            color_error_count(err_dict.get('read_io_errs', 0)),
            color_error_count(err_dict.get('flush_io_errs', 0)),
            color_error_count(err_dict.get('corruption_errs', 0)),
            color_error_count(err_dict.get('generation_errs', 0)),
            scrub_data["scrub_status"],
            scrub_data["scrub_time"],
            scrub_data["scrub_rate"],
            scrub_data["scrubbed_data"],
            scrub_data["error_summary"]
        ])
    if unchecked:
        # One text for the run (merge_status drops a repeat): the unreadable file is one fact, not one per filesystem.
        notes.append(f"{YELLOW}Could not read {PROC_MOUNTINFO}: not checked whether a filesystem was forced "
                     f"read-only.{RESET}")
        failures = True
    if untold:
        notes.append(f"{YELLOW}{'; '.join(untold)}: read-only, though mounted read-write, and btrfs could not be "
                     f"asked whether it was forced read-only after an error (check `dmesg`).{RESET}")
        failures = True
    return Status(rows, running, problems, failures, notes, scrubs)

def unique(items):
    """items without repeats, in order."""
    seen = set()
    return [item for item in items if not (item in seen or seen.add(item))]

def merge_status(status, extra):
    """status with the rows, notes and verdicts of extra (a Status or None) added."""
    if extra is None:
        return status
    return Status(status.rows + extra.rows, status.running, status.problems or extra.problems,
                  status.failures or extra.failures, unique(status.notes + extra.notes), status.scrubs)

def exit_code(problems, failures):
    # A health problem matters more than a filesystem we couldn't read.
    if problems:
        return EXIT_PROBLEMS
    return EXIT_FAILURE if failures else EXIT_OK

def run_detached(command):
    """Run command in a session of its own; return (returncode, output) as soon as it exits.

    `btrfs scrub start` forks the scrub into a background process that keeps our stdout open and
    cancels the scrub on SIGINT. So the output goes to a file (reading a pipe to EOF would wait
    for the whole scrub), and the new session keeps the terminal's Ctrl-C and hangup away from it."""
    if USE_SUDO:
        command = ['sudo'] + command
    with tempfile.TemporaryFile() as output:
        try:
            returncode = subprocess.call(command, stdin=subprocess.DEVNULL, stdout=output,
                                         stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as e:
            return 127, str(e)
        output.seek(0)
        return returncode, output.read().decode('utf-8', 'replace').strip()

def is_read_only(mount):
    """Whether mount is mounted read-only. There btrfs aborts a read-write scrub at once, start and resume alike
    (the status file keeps no -r for a resume to reuse): only `-r` scrubs it. A mount that can't be asked is
    left to btrfs, which reports it."""
    try:
        return bool(os.statvfs(mount).f_flag & os.ST_RDONLY)
    except OSError:
        return False

def scrub_mount(fs):
    """The mount of filesystem fs to run scrub start|resume through: the first that is not read-only, as a
    read-only scrub repairs nothing, and the first of all (so `-r`) only when every mount is read-only. The first
    mount stays the filesystem's identity for status, holds and the summary."""
    return next((mount for mount in fs['mounts'] if not is_read_only(mount)), fs['mounts'][0])

def scrub_command(verb, mount):
    """`btrfs scrub start|resume`, read-only (-r) on a read-only mount, where nothing could be repaired anyway."""
    return ['btrfs', 'scrub', verb] + (['-r'] if is_read_only(mount) else []) + [mount]

def start_scrub(mount):
    """Start a background scrub: ('started' | 'running' | 'failed', message).

    'running' means a scrub was already running on the filesystem (started elsewhere)."""
    returncode, output = run_detached(scrub_command('start', mount))
    if returncode == 0:
        return 'started', output
    if 'already running' in output.lower():
        return 'running', output
    return 'failed', output.splitlines()[0] if output else f'exit code {returncode}'

def cancel_scrub(mount):
    execute_command(['btrfs', 'scrub', 'cancel', mount])

def describe_scrub(scrub_data):
    if scrub_data is None:
        return "status unknown"
    if scrub_data["error_summary"] == "N/A":
        return scrub_data["scrub_status"]
    return f"{scrub_data['scrub_status']}, {scrub_data['error_summary']}"

# Some readings don't show that no scrub is running: a reply with no record (old btrfs-progs say "no stats
# available" for about the first 5 s of a scrub; a reader can lose the status file's lock to another), and
# `interrupted`, which btrfs also prints for a moment as a scrub ends. They count only once they have held this long.
SCRUB_HOLD_SECONDS = 10

# A one-shot read can land on a reading that tells nothing: `unknown` (another reader holds btrfs scrub status's
# lock on the status file, flock LOCK_EX|LOCK_NB, so the loser gets no reply) or `interrupted` (printed for about
# a millisecond as a scrub ends). Both measured on EL7 (btrfs-progs 4.9.1): a collision in 3.7-4% of pairs of
# statbtrfs runs started together, a lone `interrupted` once in ~20,000 reads. Both last about 1 ms, so the next read is
# clean; three reads cap the cost of a real failure (an unreadable status, a scrub that stays interrupted) at
# 1.5 s per run.
REREAD_COUNT = 3
REREAD_SECONDS = 0.5

def reread_unclear(filesystems, status, unclear=("unknown", "interrupted")):
    """status, read again while any scrub reading is one of unclear (up to REREAD_COUNT times)."""
    for _ in range(REREAD_COUNT):
        if not any(scrub["scrub_status"] in unclear for scrub in status.scrubs.values()):
            break
        time.sleep(REREAD_SECONDS)
        status = build_status(poll_filesystems(filesystems))
    return status

def held_scrubs(mounts, status, since, seen_running):
    """Those of mounts to treat as running: their reading is one of the above and has not held long enough.

    since is this run's memory of when each reading began. seen_running are the mounts this run knows had a
    scrub, as `interrupted` on any other is left from long ago."""
    now = time.time()
    held = set()
    for mount in mounts:
        scrub_data = status.scrubs.get(mount)
        if (scrub_data is not None and not scrub_data["no_record"]
                and not (scrub_data["scrub_status"] == "interrupted" and mount in seen_running)):
            since.pop(mount, None)
        elif now - since.setdefault(mount, now) < SCRUB_HOLD_SECONDS:
            held.add(mount)
    return held

def scrub_filesystems(filesystems, args, screen, skipped=None, skipped_filesystems=()):
    """-s: start scrubs in mountpoint order, keeping at most -m running, until every filesystem
    has been scrubbed. Prints a per-filesystem summary and returns the exit code."""
    max_running = args.max_scrub_count if args.max_scrub_count >= 1 else os.cpu_count()
    queue = list(filesystems)
    started = []      # mounts this run started
    adopted = []      # mounts that were already running when we tried
    failed = {}       # mount -> why the start failed
    via = {}          # mount -> the mount of that filesystem its scrub was started through, for scrub_interrupted()
    unconfirmed = set()  # started since the last poll, not seen running yet
    running = set()
    since = {}        # for held_scrubs()
    last_start = None
    status = None

    def start_next():
        nonlocal last_start
        while queue:
            fs = queue.pop(0)
            mount = fs['mounts'][0]
            via[mount] = scrub_mount(fs)
            # Forced read-only after an error, it would scrub read-only and could end "finished, OK": the error
            # comes first. Asked at the start, as it can happen while the run waits.
            if forced_state(fs, forced_read_only_mounts() or set()) is True:
                state, message = 'failed', "forced read-only after an error; not started by this run"
            else:
                state, message = start_scrub(via[mount])
            if state == 'failed':
                failed[mount] = message
                screen.event(f"{RED}Could not start scrub on {mount}: {message}{RESET}")
                continue
            if state == 'started':
                started.append(mount)
                unconfirmed.add(mount)
                kind = "read-only scrub (repairs nothing)" if is_read_only(via[mount]) else "scrub"
                through = f" (through {via[mount]})" if via[mount] != mount else ""
                screen.event(f"{YELLOW}Started {kind} on {mount}{through}{RESET}")
            else:
                adopted.append(mount)
                screen.event(f"{YELLOW}Scrub already running on {mount}; counting it as running{RESET}")
            last_start = time.time()
            return

    try:
        for _ in range(min(max_running, len(queue))):
            start_next()
        time.sleep(args.interval)
        while True:
            kept = build_status(poll_filesystems(filesystems))
            status = merge_status(kept, skipped)
            ours = started + adopted
            running = {fs['mounts'][0] for fs in status.running} | held_scrubs(ours, status, since, ours)
            unconfirmed.clear()
            screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
            # A scrub just started may not show as running yet: wait out the lockout before trusting the count.
            locked = last_start is not None and time.time() - last_start <= args.scrub_command_lockout
            if queue and len(running) < max_running and not locked:
                start_next()
            elif not queue and not running and not locked:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return scrub_interrupted(started, adopted, running | unconfirmed, queue, via)

    # The filesystems -d skipped are checked again: the run may have lasted hours.
    skipped, changed = recheck_skipped(skipped_filesystems, skipped)
    if changed:
        status = merge_status(kept, skipped)
        screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
    mounts = [fs['mounts'][0] for fs in filesystems]
    incomplete = [m for m in mounts if m not in failed and status.scrubs.get(m, SCRUB_UNKNOWN)["scrub_status"]
                  in SCRUB_INCOMPLETE + ("unknown",)]
    # Filesystems -d skipped that have a problem (their rows are in skipped): they set the exit code too.
    attention = list(skipped.scrubs) if skipped is not None else []
    code = exit_code(status.problems, status.failures or bool(failed))
    if code or failed or incomplete or attention:  # never a green line over a failing exit code
        counts = [f"{len(failed)} could not be started"] if failed else []
        counts += [f"{len(incomplete)} did not complete or could not be read"] if incomplete else []
        counts += [f"{len(attention)} skipped by -d {'needs' if len(attention) == 1 else 'need'} attention"] if attention else []
        counts = counts or (["problems found: see the table and notes above"] if code == EXIT_PROBLEMS
                            else ["some checks could not be made: see the notes above"])
        print(f"{RED}Scrubs ended; {', '.join(counts)}.{RESET}")
    else:
        print(f"{GREEN}All scrubs finished.{RESET}")
    for fs in filesystems:
        mount = fs['mounts'][0]
        if mount in failed:
            print(f"  {mount}: {RED}failed to start: {failed[mount]}{RESET}")
        else:
            prefix = "was already running; " if mount in adopted else ""
            print(f"  {mount}: {prefix}{describe_scrub(status.scrubs.get(mount))}")
    for mount in attention:
        print(f"  {mount}: {RED}skipped by -d, but it has a problem: see the table above{RESET}")
    return code

def watch_filesystems(filesystems, args, screen, skipped=None, skipped_filesystems=()):
    """-w: refresh the table until no scrub is running; never starts one. Returns the exit code."""
    mounts = [fs['mounts'][0] for fs in filesystems]
    seen_running = set()
    since = {}
    try:
        kept = reread_unclear(filesystems, build_status(poll_filesystems(filesystems)), ("interrupted",))
        status = merge_status(kept, skipped)
        while True:
            seen_running.update(fs['mounts'][0] for fs in status.running)
            held = held_scrubs(mounts, status, since, seen_running)
            screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
            if not status.running and not held:
                # The filesystems -d skipped are checked again: the run may have lasted hours.
                skipped, changed = recheck_skipped(skipped_filesystems, skipped)
                if changed:
                    status = merge_status(kept, skipped)
                    screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
                return exit_code(status.problems, status.failures)
            time.sleep(args.interval)
            kept = build_status(poll_filesystems(filesystems))
            status = merge_status(kept, skipped)
    except KeyboardInterrupt:
        print()
        return EXIT_INTERRUPTED

def scrub_interrupted(started, adopted, running, queue, via):
    """Ctrl-C during -s. Scrubs keep running (they run in their own session) unless the user,
    asked on a terminal, cancels the ones this run started. via maps a mount to the mount of its filesystem
    the scrub was started through (the resume advice names that one)."""
    ours = [mount for mount in started if mount in running]
    elsewhere = [mount for mount in adopted if mount in running]
    print()
    print(f"{YELLOW}Interrupted.{RESET}")
    if ours:
        print(f"Still running (started by this run): {', '.join(ours)}")
    if elsewhere:
        print(f"Still running (started elsewhere): {', '.join(elsewhere)}")
    if queue:
        print(f"Never started: {', '.join(fs['mounts'][0] for fs in queue)}")
    if ours and sys.stdin.isatty() and sys.stdout.isatty():
        noun = "scrub" if len(ours) == 1 else "scrubs"
        try:
            answer = input(f"Cancel {len(ours)} running {noun} started by this run? [y/N] ")
        except (EOFError, KeyboardInterrupt):
            print()
            answer = ""
        if answer.strip().lower() in ("y", "yes"):
            for mount in ours:
                cancel_scrub(mount)
                print(f"Cancelled scrub on {mount}: it keeps its progress, continue it with "
                      f"`{' '.join(scrub_command('resume', via[mount]))}`.")
            return EXIT_INTERRUPTED
    if ours or elsewhere:
        print("Scrubs keep running in the background. Stop one with `btrfs scrub cancel <mount>`; "
              "continue a cancelled one with `btrfs scrub resume <mount>` (`-r` on a read-only mount).")
    return EXIT_INTERRUPTED


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check Btrfs filesystem status.",
        epilog="Exit status: 0 healthy; 1 problems found (device errors, scrub errors, missing devices, or a "
               "filesystem forced read-only after an error); "
               "2 the check failed (no matching mounts, an unreadable filesystem, a scrub status that could not be "
               "read, a scrub that did not complete, an unreadable /proc/self/mountinfo, or a filesystem that could "
               "not be asked whether it was forced read-only, no root); 130 interrupted; "
               "141 the reader of stdout went away (| head).")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-s", "--scrub", help="Issue scrub to all pools", action="store_true")
    mode.add_argument("-w", "--watch", action="store_true",
                      help="Refresh every -i seconds while any scrub is running, then exit (never starts scrubs)")
    parser.add_argument("-i", "--interval", help="Interval for status check in seconds", default=2, type=int)
    parser.add_argument("-m", "--max-scrub-count", dest="max_scrub_count", default=32, type=int,
                        help="Maximum number of scrubs running at the same time (0: one per CPU)")
    parser.add_argument(
        "-d",
        "--exclude-recent-scrubbed-days",
        help="Leave out of the scrub, and of the table when healthy, mounts scrubbed within this many days; "
             "they are still checked, and a problem in one is shown and counts in the exit code",
        default=0,
        type=int
    )
    parser.add_argument("--scrub-command-lockout", dest="scrub_command_lockout", default=10, type=int,
                        help="Seconds to wait after starting a scrub before starting another")
    # Old underscore spellings, still accepted.
    parser.add_argument("--max_scrub_count", dest="max_scrub_count", type=int, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    parser.add_argument("--scrub_command_lockout", dest="scrub_command_lockout", type=int, default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto",
                        help="Colour output: auto (default) on a terminal unless NO_COLOR is set")
    parser.add_argument('pattern',nargs='*',help='Patterns to filter btrfs mounts. Default="*"')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s {version} stat btrfs by pan@zopyr.us")
    return parser

def main():
    try:
        return run()
    except KeyboardInterrupt:  # outside -s / -w, whose own handlers catch first
        return EXIT_INTERRUPTED
    except BrokenPipeError:
        # The reader went away (e.g. `statbtrfs | head`). Point stdout at devnull so the
        # interpreter's exit-time flush doesn't raise a second BrokenPipeError.
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except (OSError, ValueError):
            pass
        return EXIT_PIPE_CLOSED

def run():
    parser = build_parser()
    try:
        import argcomplete
        argcomplete.autocomplete(parser,always_complete_options='long')
    except ImportError:
        pass
    args = parser.parse_args()
    use_color = resolve_color(args.color)
    set_color(use_color)
    # sudo drops NO_COLOR and may give us its own pty: pass the decision on to a re-exec.
    acquire_root([f"--color={'always' if use_color else 'never'}"] + sys.argv[1:])
    screen = Screen(redraw=(args.scrub or args.watch) and sys.stdout.isatty())

    discovered = discover_filesystems(find_btrfs_mounts())
    if discovered and all(fs['uuid'] is None for fs in discovered) and btrfs_not_found():
        print(f"{RED}btrfs not found on PATH: install btrfs-progs, or add its directory to PATH.{RESET}")
        return EXIT_FAILURE
    filesystems = select_filesystems(discovered, args.pattern)
    if not filesystems:
        print(f"{RED}No Btrfs mounts found.{RESET}")
        return EXIT_FAILURE
    filesystems, skipped = filter_recently_scrubbed(filesystems, args.exclude_recent_scrubbed_days)
    if skipped:
        screen.event(
            f"{YELLOW}Skipping mounts scrubbed within the last "
            f"{args.exclude_recent_scrubbed_days}d: {'; '.join(sorted(', '.join(fs['mounts']) for fs in skipped))}{RESET}"
        )
    skipped_status = check_skipped(skipped)
    if not filesystems:
        if skipped_status is not None:
            screen.show(multiCMD.pretty_format_table(skipped_status.rows, header=TABLE_HEADER), skipped_status.notes)
            return exit_code(skipped_status.problems, skipped_status.failures)
        screen.flush()
        print(f"{GREEN}Every matching filesystem was scrubbed within the last "
              f"{args.exclude_recent_scrubbed_days}d; nothing to do.{RESET}")
        return EXIT_OK

    if args.scrub:
        return scrub_filesystems(filesystems, args, screen, skipped_status, skipped)
    if args.watch:
        return watch_filesystems(filesystems, args, screen, skipped_status, skipped)

    status = merge_status(reread_unclear(filesystems, build_status(poll_filesystems(filesystems))), skipped_status)
    screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
    return exit_code(status.problems, status.failures)

if __name__ == "__main__":
    sys.exit(main())

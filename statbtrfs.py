#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 57):
		raise ImportError('multiCMD too old')
except (ImportError, AttributeError, ValueError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE$ig8-O-i5'i9DjZ(gR+RLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)]U<,WTZEDeSe:(YNb%NdN`;%MLm
ps(uYZLt9N^(d>j;?gF2fq.JS8E^d=!D`Sq$Gt&.k_&Jr(6<fc-."_L#%?6QoJ:i3GQHb>?A/=XqGZdH'Nu>j"g6i-cqUX1Al)9;U'hMS[PsbB-tdCiI
VVRN65*?GL<kIO7Z/j:-TJ#--6!gZ@"9F@Y4QIP8RIA*-bdk,+]#OSpqE:>dQXWo%Vq.P6Z$)MWFf[k`LRT2[,*GhHZ+.Lg1@2O[<[B*K-.'N:N8H<<,
&E1(pirr)5m!#H$,j*ACTEldRI5YNJ%bV?H%V$;hdcSHb_`4D:n9m6o6@reHo[D[;$.gm!9.Uh1`p@H#R:?pqY4dp,biP?jQA8q`8J7=e]+2fTO:g:r5
JD/Ok+BP:ZNg8Ufpp3_R\<^ssZ3(N!N1mi^M3B+b</b`/fF4E#P't""3\3U3n+KsNdn[1$*@<O#[P9\R2mZ*;$KpQ;XhrMlS-FUZb`eQ,TOC-C/_K(@j
PS&3r><Ohgcbp[!B!$O+V0s6Q*L=G+)9sZT4"^I33/EHdeWoqeM1AFkeq;a9;_(1$pohE.-O0H8Z%ig;DbR7sJfs!6,df=,m"Yh6+Jl[7)fnV89KQCa>
3[_N#]9:M5PP]W7s"2cp4i!CBq:"AATg$E%1S_/rL2m-6XXi*5k$<V/Yl0R,8?)[&/2ejCJu^?Ke67`g1/<jVKg#j$PTRGgQRs98%nJ+NOUbn%8]ad--
ma!bMPQn5/M?bHbm%ifkhBrKVu?^K?$#B(Q*SoIg<Q'Ep-(4HWNA:g+_Ep)/;T4KS)ir9$hSAWc><up/R]#U*>W^IO-LN`^hTa7P9RK)SF*GFNOdX]8N
/3(.`NaL!NX"O=j=KrM=&*GG^]>H)OgF5+nd:$R=u[RHTCZr80Wos5]#U>WKDXm)SB:h)@`^G9KKs1kZ,umF0>FH75KKO:o8.!F[3Y\P@CTTm/L6/[s'
u"E#+Fki,nQBnoR:<*R3S\M.hRaNu<1Qn9Q"GR?$DaM2)YP5_$gXTNCLb9h;V]Q)uj*&7Cg0@nC5;HH#Q?Z>^&$OrnWq^I)5!>1tE.Te&0:\Iej]Dh5X
7N_Rl@-.K(fruakhuWDsa8IdP'_@YbhX]9qQ0Y#rQ#HINO"TAdjSMr,/o\KsR%%?K]U#BoRMp8#;m:cpKE&%(Y'eI<iK]u@Nek4@:J`[]UquS2q*eEd(
*aF,^,3R-82%b?3OS?55]1l@Ul6GSgVDT/$BYW0)[l7+<G3aNDJ/890F*3N5X?K6;A7KGmqEDA]q`W0`SQ13&Rh`Ifd-7W.PXjR7.kh3h):5B37kA%Q]
8Q!SUPlN7G_pQU`F5F.8K5I[L"YMfjrFiC?"ca.@s7*(oXDMlnY#iDggDune[gu3-)ceAVTpPE8=IMK]72IZAu?-.p8n5j!17AK&a0[R_:(:Hcm7PG3n
1;H4jTGSG/g6]jcta<;LqQ_b=Rk.kc;.o7,IEn<1LF]lRMHJOjG8/,LA*r'1&+?:RR-06Su9Z1`CRIK?9q)%u.q]'L,^_g(LQ,#@<C`AY1XJ0"jb(=aX
aR7M1BTS.EpY(#;@rD?DqA7[[C+\l1bIGp-h!KpG^ZVl0U:M*IiX\'(jHd<9YPr:B6D/#sDI:-^k%f=*cj^;bTEV55l98-^51[nLaN%1'=0U8J<55Z+Q
rJ=/keu5:`$C<ZaUq'U2oSa+18d<m!DR%Qn!rQ[cH)#"gXj^qmUb6Z`ntY[k[H,*j\LYSas*C)4XkIA+,r"QRbUQ:+m+_9!cU(/]Ohu0U/:nIFDrs/$:
>#",l6Wk@kSUH]\p"EbU%8u%E)O"dArh,n43^%78FAo',d00'%:@FW%,o+PQ<oXM6L_7!o@m*ag$GuK^O'fq6aaA/>Z1n^a9)/60;s@Ns3HV07YtsnUX
\XXC7XVHW_3X+70L<'8]=2<aTa/!HDqqKFk(dVj?(6\FrlNe<=0,R"s/$C`%I28?q]N?"m`#RRr'f9RkD2u%:nm88\hL%9J3D_-M;t1km!4V)m7J&f-^
17lY1n6mOCl!7n.&I4N%h'8XV1HVY"WAJU@pT<>n9%j36bVYU->KNreqbgilGDiV>.lK,b3I\]ir%IRl0CFlO![-1RTDI"kgE1g!9Q0o_T1J8pI##II4
43VrP&m[u]LZn4`Hm&/^a32Lhucc7c4&o:qKKPC"73.[uh5O4$-,c66.-J2CLi``S7Q=.uiS%dXnqupaC!g-IJ*HIQZ1H_su-f_+uUYH3(k0="X4>U9D
^([WH%oRg9I1!pra3Za-!(TeWB4A"\Q^3bj4&9p+*4aM"Kb!<NeI"40.4.N^S%TR,(u:Z-d?=in*TR$+eD.tp!d"j5R3VVGFqI8o7EW75ai20WdW'>FT
;\1mVWYJ2%U_!/IKg85Y[K/3gY`&Sei4=_K>c9HBjQ^)l)'Lqfp22Q7984hrh(t)WC:$a'T=)Yp`3ehdS_N4B%IbK+#eW1ousKsUfE<@>YpJGME"95kF
0qjcTb\fJAVT]#?'hW1hS@<A$pb?k0t<n70P;_RlI#lNY!?qa*hqK)nel\$_n%fdfpg6SU1;'G=4ntjuk[Kk_%skR=sUCrldB*R_V.M?@RC9jS!fN*Po
@$6n=u7EJ5q@_R4'2M&gK<.7<:1;,(:V&'&T_[_!f!dTTZ@,FRnN@FkVW:D*ZE-IF]LeH['8kj6Og";E=VQrf7c^W;>?mceI;ejPN!0h-/l$u6\P3Zga
Q^Q$W6n):&tL[M&Sr\)YL>k`8hlk@]Kepb[P8BE`s.,oXnc!UWs[c>dMV?qYjA:MV*41?'+jU=PFR&EHb(KP<j)*osOG#T\6:"F_H@psl_jUF:qH194%
8NFGG>VQChPO/*cA$?0"J8CV[ZAO:jU8;7g_,TI97uF5#<Dq1EkO*tQ^<$02@ICVOn@`XGI^2T,?D-,T-ACteP6OigQr,PS6;="m?$pm.0D2n#o[U<Rj
rg1reUut_nLBU:$qM<noHUZ^(`LMb&&&@G8MU?ZKB@b5J./__(@8)3aFerC8N_3^[db.r)'jWV'Q`^"+`\8J]rU+?Qb*>HCBXId[!]Rl7][)XZ2jsL()
*>CY[bjMjLHmJB9@FnND#k90kRU?pm*?-:KQg@"NGtGf68CTKS=)&kpd(Hm^Jo`k'5>u]R=Y=Y,/C*>lqK&r:Rr9Ic2\tYqg]8NQQ"70U@:+=#8B[CLr
(8Qg?h^RZrHrd@C]f:-'XAbRkuA:NLhORhZ2MYNe40.+D=QKt3CHR'&O#n)k&m21jU_dKD6iptKBJE4FAGfEb)?[=&)L&-h"^%e/WFbm75"_kap<UH2F
$=)<+hL%>L;fWdcTflL*Z_EU1PqXURi"D]SG!C.#jl)Fk-bN4GuoXa+;oR]\Z.bct.f;W$Y[Uq2`lsh#8e]#TNK[Y<4Z#XFR$Ro;uC_J[5:@J7:G*,Qp
c<V.[hK*4oIGBcb7R@u<To6K-['/Yh5oC;6=PmI.&r1(*&"$%@BA_O"fPLdUe'2K;)%,tRB8Ir2dB1-VOJi?4BY^bjZM,nLW!?^I^^aadDRI!7l<fU<j
+1_l;qEtCrCC_3VOtXB6G[/DYUBIZq!e8bNY?#@G*H`L$F>$H!a]Co=DT3/!q)SK@C#'*!,G6^dnuNP7<#fL(9M/>8,64q2ZtqtW5H*AhRl=Ur$^9t7T
*+8?Lsu;^\KOk=o[@acks)dKf,r%hm<AC;c;34ki@Md+^M28BD)j[@.$Ag;CH!305Yr^8i0IFm)\aRF-GSq-P4ch&F2_4X),=n)s\2+)KO/4p1?SaW2I
%TO$<Puo^8VXBOY!8m5r#/46h?%V9dX[1,,8eDurUo"O$k8%TXYP(sEYkC@LiHG94\,%JW:f,)Be[aBbYCBQ_b&s0!K,X-UbgDl&`s;0H+iGbmO7pSP4
+B[7A6X_:[N"%c$:Bk1i0pgK<$&0$i4B2odQUuI$)+96Wo(;'sEMA=QJ8q-bScAm@W]K^]nDtp.1&D3.4Y1Eia/+^!F>?qRnICiNk7l.<1W03Hah\C/#
l9O8/FlIcpRrgqD`fp2P+PV!@LpOi7L1(QI%h2&=D',]OE?'?QRj&G"fZhKn-,I2A_a(ds@PfHU"XMuN+cb;eIq_M3ZW[l*6$Z6pQJa@`!&]9E!e@PTb
pR[:=ab$,EpUcPaYV22Pk`B!Q_AOJJmoa??laIe#UsbUBK`@(Z20Ra52qABD_OVCc^h91)iZe2+J!e4S_"gXr!-=hW7WM^'JiB4W0KQlHhVur5WFd'5p
PS4Q=<_o@tqme_X:-.:cN@SU2m`:kTM/YjX/&f+Ef]!-C#KF3^sulYG,b=n7VHGcdQc6+D9V`\#LDcje24KoZn?;LBG/<jr<1'bTpfkV0>[dOd?/;[^S
:YX1?:d=iNK549n,9nu=KI.?P51-D%.,45jjgY0_NP!)\`6Z5(U%?o&i%qM#<+<m/:3Ue1@G5A0K+""#(H*?G1"B*EX\^Q7K_NM>#G@3^@l,*RfIKqhF
K&-r[4#%L<HqdIA"mjgRB]Etl=Wo<X"iAts):QF!kqSX/dj_/"C7^5fol\K_h2W@#4A9R7h#mVTup'+=gEl2F_<&BY^<6a"?e$n\.pSJ9$NdpB[p!PQo
X?!Y7K)2kcP<D,k[RR;Yn\q=&-n`hZV$Q`2#*Q94Mg;)=!i,ut@8#AtNgEHKe,CQ#Nrip-!8TZO-<sd"iTjqV"G7K<>ZN=u;5mc/TTl/#Sj95LHsB$WF
=R!h!<,0SIc3/.i]#LV=e`^iOA[IF]sh7)LGXm[Ir]Y*34Uof\k$O)d)t%;H%^Da(DP%>W-)=1!l0jA8!NliA_S]LW3[!&">;/;R7R+O^\F/X?Q0?@d%
trUO<Xq4eKB;a(1#.0qV7^Hb)t53C4mAa$"IYuD&mFBAm=Z7T/&;p:.HF/H0<((YAE<QjAG.7D'lC\NI5bRBO#)6OGMICY6@99J+*uA]@q(m%""3)8$2
t/:g5!a#]s*2hdC_ecWF&Y`mnE1K\*=o*FfnaEd"2MAepg9&BOp5JlAgfQAt!j$cmQoLY&Dc+IZ=7N7EkKL9-kB)<3(kbg%E9Ed1,kWdh]/pOWk[&83:
b;3o1i:YqN</iBKU,V(>U&Dke#&l&kDN2SO5<(MH3fqI3EDHO(G@Fib!'*N:8VR3&I2L.=n@)Q=cQ*q%Jk1.01[MS7U!Ga[)Xkc"oE0OlOmG`htDT"PY
_BChXVhNsu$1RTTj-2**Rm/e`@KD%Go0bhW0uUpf%.IQ+-7k;!IfEMW[gLN^N,h;D?-&^N&+e"em;*a*a1B)nEJ&3J;X\>Pm)hpn8"FN`PDa?[<Met>g
M,Jk=K(>.C:9$I<c=rl:"K9%^G<:cp&\7cMu((OY5=h3&EXe3m,MB0V/`#Nr"HZJE[&)ldFuN)UqSo['=T70>EYKr`=o$L?o^RmKZpQ#gf(I1Ck\aT)s
olp3?i,r&F1,eX?)?-S%0or:$A'!Tb9;0-)i+7MrANK`j2M__UXA6BX]ppQRmtK_1*M:$70c0`;o@^8+:mX0D3jJ_26-4M%>'pm9([L27;mui>kE;m#>
mql4`#Wl:h<?/n^H,#[<Ymft%E@eI)T&.pt=R_o/M_jqlar'qLaF9-,ooC@2bkk?:nNn=$+m:F&88rGpJC>+dX$d=&nXf3]=WN5n#dRlH9jBFWRkQ@)X
N*4q,NHDK1<c0V06emd95_J)kEL!VFB]k96R@eYhEju:07/kX>k?e+QT]8Wh&b$10p%kR8c0o0anS\Mmnr:Gj^l%l8ue-&kjK*,+]f+H;gN5eF+A%!?O
rCo)X#YM/AWan!YKB5!NI>!YG15.mr!/4Sb/SBYqo>`Ek"3YE\>>b1iirP"pX:_2LW=C@cm*/><:LcoqLC$b.K%(oHpWV9(!h6A7#HGWYh%^=YDIgi,m
b*hT/GR>98u)/Ek[$pamr"5NpCb5eE64j@JD18/\<7mLUEa*ji@G#aB$gRB=Ddj?\>C3nG#Yd>a1p>gHdF2]%PG%RGO1,K7s$\!WFAgR`J("Z%h%N*`Q
UNk7NHJJj>lu_>nC)hmg]qXckYTF#:d#Be[]GS)a[RPcm7_=dM(+/<sYI:X8qk1-.q,b\u>aMBI`V\1<[AGa`(U3kXT)Y[)N.[$I_[A<_P-`9aaT$Lf,
mp0quDXB][rM]<.h-CuuaI&>K"CC&-4m1lWM+4*91H")Ds6AiI&WNrg5_@:mLI$@Y?\Z@'?S>X'>W1oS[l\nW'$rH1"6Q8u]:g_W:HNP&?DX@c[t/^>A
Tq)E9V_*)HEP"V5g'-.-*Y];Nl]^hW*Y1Ze&[4!tgHo>=OlPKh2^Qiap99=J[>aXJrf=kPkInEIb1TU)$5*@M3Rj[]':Pc>[J@`a)BGj5PBmtK"._=Ea
XpsPBVb,<Zb'bF/2SL3_r0jU>R?C_&T4%):q+p0]qVjgT(r?;kYXWSAdfRV1"tT)-/qK%[SuV8@+'Y1q,JJj\p&dD357LS^'Mh.*guHQZ59?IM^Y?MFX
bE4a2***HW72g`,m&q0,/S!mR[\4CYb++9gGo[1!'SbD9'eO$9+R:DGcXl/)iAL9Bg82#!YXb)I5&L$;1rds4_M7>j[#6p3NLl2[J]r>2U_oiTQN#T9M
HVkC-0*W?Q\.G\\m+!W.k$o#U"n4lODUXbIoSu%JdKRXTq:Y"0'"8cQTsqVRn4'oT?4L,2@T>+?Agg*J2ID!2-$#"-D>KIp$3/V<jE#X.lPBch^#S;3*
KOJBR+i9:f1*+Q"jrjCF*JZf-Sf$Kg,7m?0<<W#L-U+g9sh]qt,Y8i8@!ZAt!rA*1.>L/>;cmF#P8oE6!.gH1SO;13YP)Tb0DcaE$eQRu)cKe>Ve%>eW
U9($W5W72BHr+QVb$&_n(4*7t>_E"EiRR"nKeKol;6tHRiml-q)R%e\u@C6$+P`Qi%Mg1sp"oFRXKQ@1KU/(.M*_i&7?'#g<9*mhn#[>X,U7"HAm2eFM
ccN&5l\]*[g%MO3JK&$%6ML%CqlbBlhUtlGT6].gGZ57-6mkI<5X7$`5W5(Xr)+ps[(n*gh8i@3+@*d,.Up=55o,7udd$+!cp*Z8Uk%<(GejXf!fC<]q
ccX7l_og:DZn5NcrfJ03f"mu:>n9%q1mrk]bYZg,LI2;(8/bkb#cI!dd5HlHH&oAXK^NqF$_d%E340mK1S!(P5<"?#Z"9fH"1?9F%1[cB]s+)H2IMX!&
NB&G"qR!%r^+I4P([&M<<-n6NTrj[s8iGm3$fG.4'0:iGU,*0k;FXLUfS=nVWs1#.+S:=MHS.,<&N=7oaA7\<-<m'TYp+5*J_?,kX[<Oc)3Uo1H\iZ84
0H>7NSD>4Z$'0*-rD/5a?i4!jajUrk^:G>;WmVc2Gpc1qO$7<4YKkFJn2Q+/j3PutlK^uS9"AA]s,2\i]?K[Ts7^t[-f*0V$$K!2Z$Tcj>:O)b=YPYMo
lc*LrRk9Rk>S''[ME:q3Qddj+RhBJc7C8a<eo5glGnqnI!7F/WZ-=PqS6=uadd=K"*MXVcH=%7Q#pT4K&CG;6C7CbJ?i)iR49?*r+J4"[T?U@V?9(LXn
GTdlejCHIrQAk@3i_3')XXlGkH&Wc$=s%ie#fA969^N=[n6M(b]rA_k\B29XW<Hr4:X)Y3Yin1C#i!=/YPCpM#jOaB,6R2#fI`%IF:lrb`:$orNPT9X=
3<;CgJu?)"#0Dr)bGOY89.J'(t[og:K'k-c21SXii[(IUOAl+VGlUjI'<9b$!Bk6/V'gt].0gb.;s-]Tfa$T54-Z)=5R5'522aA>O':QcH.PiY"&OW`k
(tn;Z8uK!BHI^op<J'),mu=W,;lq2`XM3kZ)OB;]'sV%#Eql0Uh>'.TJ";l_*4M[1ZNt7-l3>@BCjda0X4k,J@Su7KfJSY2O7K)Jb%5S6a:u:(eXg^)9
He6E>EF'M6`=-#NlO%K\W*1=]IG"#i+0N8!T3P7HA#X/i1_)*-NP6+!:,8RL-$"IereO_M2_QeZhH1A0qhHa?b+=IhjU,$.JcM+.*Z7EYHgcouh07oBW
%&VH4X$b>`[oAZ`p<42Oo(43r;A@tj:DW^NTLNW9\Oh:N.X+I[tCja-?Fu]Y:`B0E>;2-+qd5tkELS+JeR;R\*eh4]RnZ[o=F'[`tSL(6!+3V?#p7jt2
8jJ7@ajYZ!7"T=u<Pa@3O9E[>HduQR8`E[$q3+@KPIlnco<k,pW"-CPA27kC]SR/V?oX,TQLs*qC<E>9M2eBs+^WKhC/Kg4ZK92U#g'[c\8ArPV50B<B
jFSc:3s6ZDR]18Hf]IYk@f"*8-#Sb[2r1e.32pVFND.YN0.D!Q5lUkA!hdl*G.]KGQ"$fforNHO'P:\m)W!0n4F7@JoX.d2#nfJAm,IXjHJ\(Q%keGj]
hQ*,,S+u;+b0T;3YI9B<AN/\tKRjM3NuJW)c&"_Nh\eIZo'2n8!2Zb4@HEb,tq/A+>sgf^mr$A4_aWZq,cBcI`0tQYArR4,7\ma6=1piGgLl18t^MA+9
'GhS]C\FP[9U;"c_=n?,TF5o]f<!<F%8Ys0bkpnqG/>O^k:h_=l,U9eNgnJYZ#%K$2>W+jXeJYB%8VOQQ'!_OZQKWB4SRAI,>l)c6KoaKY,Rdk8RH@/"
h-?J_+2e"dG7')hH+m$;d?:L=@Y!NaFKNCIoTY:rkJP@"7Qq'?h??3qmW1C-=E4-cq"B$[L4g^eN=@btE<pB=@B-m/b>B1#0-TB=]Q7!>NSG5pFe.oQG
l8dm([%kZU?+R;tFV8Tu:?Ms_ZV8AqHArnVotmI<LkE.O_JQ0AQ)q]ps%gXup%WqFI8UcbJF$fVFMZn"lp[#lMcTki-UM)K)kfZgFg)u,,.41V<k"036
X3K"16&!-*81:\&&@.c&t"M.f6&;N"T=:NG$>l\MKla]]:YA??+_*r(5%i,?\$`-L4`EnYS8("%S4Li8lro+Ipt850\VESpu_4J/X#PRKmH8@S[)em&u
peYP/Yb08^C8VJP&*oE;^&7$XBqGX(R]Uf:,4bZ34:L<idG8#L$-(=Hl*p]?Y5\HU+RL2uB75"kc*5#DHQ4\#RpHZH1PKDJ[M_eg+XKW-!RsH@]c&::I
?m1%VBM[4a;g?4,;!;Y3es["Oq2mlb5C`a4E?ACJDWSecSD)H3L2$!+Z/*XB)4`D@"Bpb0)dd9sj4P'RJ770A;RV44LG&Q_3a[.2Ejb.T!3PIG6K1T[F
W#41PHZ#cK-:)pHi#/'//?_AHodBWM1<\2+1V\.;[_;4Lhm9TN?GjGCm(IsBP/X$)?,.biKfcAVE\t(W[0Vbo(e\t7WQ4^lhp'CmHQFLJ!7'be%cDRfs
r=+s&%Fc7G2HhZ<Imi\H"*AA[,/no`?tg^OTIY4q^%a.5'E:uR&hV#^da@^8Ee(=-];VT1Ceq`(GlE-V$T%uL,FJ?QMGZM(P(n;XKg3M]9jI;O_kGVWn
_HDlKIja$C1fS!$VY+a+:%,$\oBf+rUH<!2qKp?geW=(O(%A@Sm.`g67CP1ci.BY&Ao?>(ngpb#UG<Sp]'iU`goJ$`cIct:&f!SF!!s!0:q)?>?C@RpB
D#'64hK7(lJh$JjYERjBsYdAFp=&cVh)tgkC_Sr\lsLrMS__N1'?^bT!_"bcf-lQ@+!1/dIccgF+HrE@W\pRUM7li2/l)(Q/)rf<EI(rUjjO[4Cam?kh
a-R7_`t%6_anG#i!7ZlQ'Uo6;W,C1XB>GPgC;kJ=f]+R-ur9i.9^&>M:U0^`9-GAa$E#K'.*h&L='l^]t48_kkG@pupQ;-sB21A#BLR0mGtm1pLVhQ&D
W#2+:BCi/UkX8JaK%*HQo"#RnHb:>*?`&!AgVT&Eq0c'i&%4TWLX;_OWP*W>4l&f&T570mumI=R!n$hkhQ6RDR&4fi(4cEj<'`aEjbBIRFY;]N9&p^'"
/]'6Zg$ZC#M\?WglCAC(c+>)^?O@SXRTAtE!!@#*k$=ulmrD6G:GX<*#<H/"TDXYAI!7m_?S[*B[oNsKegJ&^:/+H_a9$$dA\V;*WQsDJmT5m:,g`9rZ
N)W)RQASES4hhS9b1AqF!7l9Bh68;2,)fb<KmN.#Se:pK=^+@]BnRW<-P>)d$@+1ikN\Z;Cg#YFuMiLZ'MQ*>MoW\PDJ45C/qbkErP,]9c+=C$[p66kB
cYE?:]mif9&jtjT-^.[WZ4KC]?SD1[[4#.D&bu6ol`9K!<>ojX-#?,Y*62hmj!TcfX@kc7%SNJ^1KC]PK^Mb>BFe%)k*kkS'W.J-N?<3-_(W%&qE>:(#
2G<8@6\cY8+.:&GaP7W(GEGiVih28MYh2iToA!d:)2%9'j/:jo?H4rn+G-08nLP;q=D?(\jCq3J^k1/f>nj\?mGR4^DDTAS&;N2ID@pF$!"Tm3FMI83V
!D=!CZA@!tf#_%fa?2+:#Iu#9bej%1q<0sMZrZW#jD&7%u^S.bIPf6MP*I/Ta:TKA$>r]35>SLt.hS8Mbp<M7G@KAYG!h>n%Y:kk=Ma5lA"c.NE&VSuJ
]&raa[-_+pdRO8@IN^MqQqo^q!$S3&c9m(CpqoNoi\0>VoH"536KVN"]MgnuXs<(%al523nGH1::)''OLL0JpDde4qIb7c/>cI-HCb4<YU9Id0FZ&e9h
Iu-p?Qt,gDeT4lS^7gLTTiOuNaUQd[ErW2V<kMV7[:ah:e$9k`(hg+o2P"ePpn%2VoX3n;*6u1=5]ZHbg`4ior6\L+Cr[^.'bf:7I&qg_m\q;RsTtk?6
*G.kqm9FM0qY_iO3N_WQcq&dhaA+'b\6j0S")q+,o=5D3Sb4?HLea?.fDtb.M;KW3hG7\qgQO;&p3k@90(u%36QS\)k0WdW,;^X]7?CFZ0\lP5'(%5i,
\MP\e[g?Z%0*,*P_bCpTWB#Ka.JBFpP<&gJVfWR*r<!mE^be\@r?:\fftk:DYhPk0(M9:p$1f)2)L;,%E+b,bK3UG&30SW-?:k3[?X8YWI05BdBq:=!A
MH7UrkXa\XHqj0`tIMDP48Nq#`0C<p.-5+s%<4;d+cClh0EVdiq?ZJM\N/sM=Bbs4prJN&L1J7;eqV&A-"[:"YCp^FP4l7u[mE-.P>X=;d'4PlD2#%/#
)V9OB`$b*uS/6]8b)D1aHq**BPWskgSsPC-X[:Zs<k\RcO#F3siAeOee4.2'oZJ4R/Th:;5hN-_Ou?8,kg2L#jZg-n&OsV/DVJ(:s+Q6\gKuV5DKeHLK
W7,6r@AinLX'*?*Q-^I/Af'5Ys*W-S#=3Tr+fjj.['Qr[aNFc;I+[<SEAEW781D-CMS.]KE3qUP_V?Ip_J->P4Wk[G6o$\R@]9X)FFt&qCK&SQfjU0D0
Dp!-gn7W%V'9U<aqOW!CHkSnFVN7<L#fFO1u0[4hFLt^c-(_j6_%h,<Y[e,Z]J6Dk=,(XjH!a!IjhZ(nJ/1I-4f`_`<LgrPIZ&gRB'85ToYjoF.YLrU4
o90n2V#fq-'u>7S9s=r_gmTMR@6P<k$?Y,N_UOolrrYB=OhD/kn!P_d9T<Em;EZNtq9,p,>SJ:Jcr'kW01)EDOF5CZk;3GFqX<2RND8\Z17[R,l46qSo
WI#g?$dpFmDeiNMJ:0,Tf<!-3XXh%6FnUHq<<"E%SIfRm#CmL$f_?+,W*KTpt;jqO!N=CuKYQo"-%*Tq@D-25^KMu;[=]7E?g];NrB(0s@>>-Q6Pe_2l
mgn3.N3P=4a8l/"UfGHi*ohI@)"mL-i%o]!qrTNW+-,?7K\?ISH$Rf])GmCSgO_>L=$Y/ZJp,i.o83qAPM<4NY>7:O>j;iE]&dGX_f<ii6/1#K<M'G7F
sRl?`A_NN^O<hMfF:uIQdF9R/"u11`'APH.Br>No2h>q;7W%A&;1cCNt+.W0k.u(dg30.6#jg20i:>N;P(8_a.J[V[$hP-X4kP?(V#TQ%<<cl8Ckj3Jd
$DHEO<QOnI.Pk3!f+l=@q[9O\ncIk+/&DR#'S14CuVn%(L-u?VCARV?/]0gMsn/KPd@#p*r1b](_cS%no8J-9)<k%;3IpN2=hURTD"qEtO+QoVl\>\Wa
g&A-IsFN%HVRZI(9bh<Em%M%Gs&ghL%):?&-6X>q?6BRs$;p5HR1CZeI"?oVS,M+:PQ!OT33;iicd/i]4=FlEI!*YEAX#=<g]Q>1WmR=&=j;pF`c*]Z_
>/2*0I?%!=&@=46&$D;E%%`Ic2q,YHd7^S_>JYP?:[m')7U:s%9eioG4Y(XQ/`_bSN:sbEC?.jG/[RG\miRkgHo@^,#m0_kOS0<=mq+=[o/e+biETD*L
K#J]%XG=]<3,`/ELs81,?Es)H8$c`\BLKbbEQ1D6Z2Y'DeXq7PXVF_2^W<4qqn0K0]l8iO&I/o=mOk9:Zser3*W*Yo4Ld8,!gAsh5E64@ao*I?CI)eIc
jtnNPEW"QdKi-m'eM2LkV1l44:UmA,#3VJQj$hHZ$mT]8uR:,m,CV4Ya[)`U8eu\0p+'K4TAjAs&89[DY;Sc(:Fl/Ks,lI'j\a[#[dVNL9Bg;F`E^KG.
K9G8l..l&%(_Uh?]%UJqV]7SZ=YX#q+Z%r\*1D34I:Am@6YEOk^Ip/pXNa.n$(lkmi.0@>DPk89(M$b9H>([B)IoUK"g%5/VI@!OR/rG<LGeLF\B'?NQ
%,c]A!m&[Ou@/3&71-Vo,(+U3/lY\&nc9j@OW`"jO$+,N.cltdL=E9c5%?K:o$[="I\l88WQN,U25BMe/f$-nOOmiE_4fFo>i_)4p-=M1<hC+.[,%;5a
gG_J)"rf^csFkDCki#1h$RSdub*d[;hdg(X-Ydj@o$Nu92Q+hBu%Q!+.+'a&YF(F[!Y1l1DG"Y]#YGffkD$O>=dk0q\1Kr*Pmujb%ms"[l^t=,/aohFh
K-npQF_4Y2W'[^(%#$^KkXS<O56AG<Hf;:sS\?&[.MMTXh"M85;50A-dY:-'qJQEp?9AV(XYV&G#Kbb$6m^:aW(m^nJS[E)&=*JHj)CChReTnZ\[>7Qe
7cMeCWP*Xg@6U&[)`a.QC:CPPUp@-[AWHR!k:Ot.)i_nL%%R7V:2ZcC+[;r%:q"r5Z8p4)0gN4>>tUFr^F]TN&?kWLUurro:<D^W4Fc;K>TB:'GTsJ]I
Qg1#\M[b;O1=NS\&$0cf/\,1M"4SW!Q*F-YuR5#;*l+->;f8maBM6)^uu9\\kT(Va'Gf]b=e:Rd(:81M`GpGH]<P286iG^poD;=&!L*m*!?]Pc%JMRR2
uj<C-fgokjVPo&`P4e1[RmKcmV+6:H!C!JSTa0&L\-_k4&-qVn,9()pOKE1!7pYYr?"2n)T:Mn*`a`\VC\h#?"r@<_5fT5)MZ+aYEI]1Z-s/d;U9ZrOE
u&_ql%hS3\.b*'&10D<_W2.qp4A@1#fHA)jJEibS76;gMo$>DbO9V\&,i(^^9$SC@I)o.9dSk,E2T3mT+r:2#AmTW04`(SRb:umQH-7oi0SIc2O\W4F_
WHnU0:=F&8k75T8\<.P65*1fY!]?&c:m6:_<GVu)''`^pnP^biTb1=Y!Di"B^(@kT]1LM@&aZB'1E^>sKEX<_:gD^^do8O&_T:_n_;fol7sFPb2Qo.G@
9^CSB4!7*Bdq;].7F!rnu#0`WA.;C?2e%^IF"-FI!'C[V8K$&P3T[f9&ahqea*fUMLP.lF_.QtWJ#@s)(rLj_/SR?1FmO^#q<691Df[V,j6-9j[ZsUq$
G2E+C61tKde1tmk%02+WEQuDZa%CD2q=gdK;24!kq/qp`)F.+;1(3-MpaA?^0VbjesiYI_/Wp'!'t513f5IJ)IlN\%U(GS^X.Nh8bMHe9rO`">`@2bpL
01<1o^knPNMMC"!To,s],Ie+rFFQdBl`ERM;Hn0Jf_SSufs]8iUu8O#=Q2Kjn#h1BX5%*388jB@VJiK"npP^\_E3lX-cSi2P9EFn^4S\r<%H:bMVfeJ6
BYU=F9Hg.ir+9-q#6-TA_6NCt'XO8/U<)'ng>3C1heu8bu"@qEKN'J;_`d\4&ctFeih4H!I_)f)Z&J.ig?"X\/Z&4hC>En]u7QR`n>'Y>TIpDl<2+Q&j
&^t@@Eca7"%arK[gHKkMlk+hqcL'M5(,KKf@@[.Ar[_5r5#0]Gg<m>hf7"+Y1jN;km'Cu#R?4loVb)*R,hOgi<%[&.446e;!5H`qF)i>-6XGjr0X=ZXK
S@<ICO7R$GdCVqF.^8nTB&fGe1HnR?t6pKE!IMWdRSh"WF,pP&&J:^5^%J[YGb`dBE&elf7Ka3KL0Nu3Pbp>*.f0``*rR$KTn.F5%@_aA!!'?Pbb@<@e
V_R[7josbKQq6hb24*n=!+CW9EA'>N!k88m-q!p+aSfs._8;nV"`r#7nB^n??pY@TC)Gaf/]b,),>8l?l\DQQ@#U`h,QS3Eefs%d;3Vm>_-A7Ykbr@X0
9`Wsf62A*d9,Z!9#QdF6^Ch'S]rDS@Q&fW;ucX/8^G1r4?*^qe3b5/G(VJH@PhPkRaNIS)c^Q_;$NoCXZQDs9p8EpQBZZ5^;L4Du&ZFj_J7s#G<<r=[\
BR/?Ci5Y'Z7,5Rp&/FfUNM,%W5B1>?.=H>"'cQl(Cgpa-Ee*Fhdk,UEK"'YIP@lM)G:1D7]'f(NADoEEU$YqQF"ubl%-Vj=#m,#="rKBY`<PAL1.8OM5
HPYQSO\&jsr#PYYA]EoRpMS'7@pi@>*et'ub?%6jkqr2LrL<I>X@3HQ8Pb'Y'V%T^XU7!s<.9#IO.+KU6@TnL)`8T+1@X$=c`e%H],,MQT@Vk[.:mFqO
Q)5^YBlY)d>NAD>]II"]O)SQiC@`2q0^4@<]^l0^>?$9Nu(>q^],=":9RpOL68(;["XJD.dlBLs*hB%qt#W'YHR1FU80a1@/44i-Y:@g3/9h9Di)R.R6
rD681*h_m*u^B]3mo)epVGIJRtYQI"/Hf`c$24^7A).jVW_V)'mN[BOj/tL/1d$VIm%'&7^f<L8NQL?Osd5"?;%P]V@b=YFMaM#7I?6_SVbrQ$pc@#qi
%UK$UK^._j^GPD`p@+i6R[.)ArqZ/)\aE^1g#puT%ElrHDLes#.D%r!d%qM-IHE*=K@8e8)V\E-qCJi0OKNUR>a6sX_!4mZ1aZiOOMSJL]ms6&t!_^37
[44(Gg./=;m(hDt'hUi<sJU+dT+1_-5Lt,e=Dp>U4?8f-\mB^V_H'S)^o+=.UjR0T9Y7VA)3LVGDC=qJM\0P!kR>DnJmbdhd$,"XQV:F$HV49+,b8Qo9
P_#X_7jt@e[N\XXZ*UOUb=Qdo?IP]?cFqL?Z.i+(^dAJXcEpZ>&j*UbhfJu=l@@Tt4Z08K@e-o[690_;?uQZ:#/nK+T1VDRXWk4P`t!_Om60rq,"44-j
\Vq_p%&c%IqS.Y246<@*g;;85@GM8>Z_]-fGb+CqM6fgcN2EalCKJJ3OF^,AP.Q/iN\+V_2$s5eS`KsEAmp8@`W`<prlr<8%Hh"@(P*>Z*+ULcs0gkJ\
>hmQ>CZPfP"LuGEMLkAJt:L,p9,%P"C(pMa_k$kXp^.JmgF^#AY,V)>a>6(g@WjhS6bA+]OipGoAJ^?jX]<Q#H*:'ar0DXmr'kqBTS1/iS(E+NN3q*?>
fKMo%6mfhK-^okmPsq5\c@W;Kk9'^O]ig=e8t:s9J$#a!XhIk:Xn_"L9m2/11B02)^"_E!jhNu_`d7:r?n:#3MtHRE<[^cT<(:NJEE/91Hh:YU(#)EnJ
<b)f^u1SjGALA\2t7;WX'cm#.,L@sfhip,&[SojPYgFbG;o>KJF"\3'j3-">Vm"G-rjmXW(>qhmj,+`i9/^L->#-L9Y*,\D/05s^E"IoLapp@&e=S1fB
'&"&i5K#qiit2P>K^3s.ekda!kT>3G>?'QT/Du@RkF0E,8*aqti4V;NbCRLl]/42iP=e1^N6HE@ga;RdM?gUr/pbV'.4?/SPa'UAmgk(0@XL,1@8ecS@
lN@.Vkg*URU=(M_\_]_$smD&J;VV#<EeZFdO%6`?37&YO`qU.AbA'b"2AuZPJtLP++BfH*`YC^IpRUl/<h\L#u$G1?I=In:SQd7P9?&%=%1>aGU$+5HN
+E+qqXheGIG$lYFm4GMC5YqAD4\.Z[D,ceI;&Ib(oS[N;r)lK)12A57R+0M7[_`"Ib\:U'Cf616T8WlJ^$q$37^9S*,R9iA$Ctcr/.Q'/K+?n7.n9R%B
\*B>VjQ$d/IdP)1V5#ucOIMmG+snNmCOHdZW]o[olQ,,Tn(^:t\$m2&WRElJUVDo.kbE*Z@1P7"=&Q[;a?6DqK[f=HFN$SoNH,sm?7Bb!#\;IY.++DVW
7rR5?mV.XR*fnBeB5j``#8Rq#DnJ;H7[35PpX$_cW.u-L!#BX5u'(AAA5]W-o1o6C9o0XJS93TfA:3aui1TG,e@ZC#:P2`TPU_.eFB7OEsVXk>X\%@)b
^!ZDDCA00`#&R2Xg*(i=?6`hY%At;3Fp@_i$=^9>8Fj?Pm%cH@+a[?_SJ@E6Vs-i:s%pK<3++!d#/(8ch)'8ZNN`Z+6fk#6(W7!QA1\Qoq"m!d@2_n64
9?aPXU<[uc+ba"'c'[Ae<MN`X:fF!Zknc%15LW5,_h\:OUmD`\+PSP+o3_J$1KjCm#L=qNu&T/(]LsDZT(J7af<iA?O;KX&D5=0d#&k7+=jfbdm]5U\B
EF[rISA1]-hEUb9!mC%1(A"QcB@TH-(;fn=@"TiPn)B]QF(+.)YNo7`GGqr+P,`:k;1K*o6PZ+5[I#R/a['0[Q2/9JFp=mpd0XKsGHCb?<>U-1qEq'E<
4/TgE"3!A%r5KL,,tEqG6,Ynd6f@`\P32hNh=)sYb++,?&qOqFHUj9T',e=sWWag%0V);'Du3DtIJ-WE=(Q["=;EAeg!1Qi=HX]3B/o`^hAGqi\+aMbF
QWkY3)=Duo]_VMp5?RFDtEE<i!;99(l5r+SR<[/1G_GfY?WsjdK$?8AiHY(Hd3kqM][A@a/^Jj5P8-.7NnPOEr9mi)Mk!j7X9AptH[fN2$_0l:R;M=%R
2'X4<PE&B@Tn_NH\B!E]i-!I\Xt"O40=Cfh/HrcA6g.R@8uq7=&_I5a5jPWsoKFr<+Qmb;L?`OT"'D8^NjmMqG"_8U$Jn\)6;m#dQJLWN_e.I\,9QKp4
/"h<CC+!\J(PI1RIEj5_FJ"A\]Ud?1u@KQkMbl5G&VVg#hYNrgWWNfKY:fp`#jh)D"TFg`ZV^0j@dI9g+OKXq,[g@3IR&W%NBO5*kZ<mluXGqU+//6:X
*gV`k+Xg$#LhlMhXfmm=0:^lAYYrZ1u6HU;0guH.O)!r$5-$-/[[b,/@`ll[SbDbKf,JVNN!_(?5l/>9*]*laZ=iaAcj%q?cB<C(G&;8i%7p_:mACPk(
L0k&m5^2PcFDTV3TUGPD4+$VKr5K@hg@i#K\iLADK<8k$0m\P@0!"5;@5(I:uI+:/.*C_3G<^=Sr;($QTdNbt0K:*-gO]0ZI#$0&$*:4WupiO9'(*TB@
%I`0lA&:"gI(rg=[>u^GZXCf=J:l?@U*Ef"-9_LnLeDY@WYLJX;Fg]j1B*-ZC]r2V@6%BEg`7tn/c#^/\UX[&L3!JhGJ'F@jfc/Zc_$5uu==5^g.\N^'
c6aJqWJC\"+WtV\0>^>Lb6Z/Jrl2gZ'm$aIPFO?!RK!i5Dc>[kUd2p8CIuh#4%WdPI)hndcX0KEHo9D,3W2!NPeOogm>eA/;uqiD/!UD![gBJ;%Y?#f(
N8,hf&WGlZtJ=j?4_Tj:n!2i*3\Yr4&Uq1M5jF1oDC+$2m8"uL;cT1Ag8JLUQNQsoeZ>2pu:%2JiTjX+J>-Jn9<73"NaYGbQ@,ST0JfG+Q\),KWho@OK
s5kq6R=-&+ZUGYLX-*lT#X2AkVWFC?!$)nTr.ur6A#5<or:o6DDJ+\`YSmDX;,L!9RG)a`2$i*r%,k:mX42P4f1$-</<QVlt;d%!L^NFPbmp(R\+3%4Z
fM2_:g@i4>;5-Ih&+7:W>@<L$-rj\J(2k(uZ!2-FFV[RZ1#d\28MR%sS>'4QX2f_n-I]b(udnNG(\biHeZW\n9@K&#SOWB9;D[,s@t\05H69_-qP2P4q
rmg_!W,M5hYPuogEW!Iq&4e?=7j5FFD(:0nJi'f%ODOLp-4FNri.uI2JN8_&n]sQn+gkE"[J\jsW[DaH9S=T<7BC-<oG(ou.D0$IN+?O;qW2srEPOE`D
7)m@%G3TH_Ps"Lnd'0m=BheO>d'XG:4u[&,s44=-504b]<t1Y\BKHpXT!p*q4u;Ds`GJnnAL`dW*itIM@D:H2'"c3phs[M_GfW?7FYTrYnTA"@+5eh<X
/..-mr6CIUFO'6anE?]rsX7"$4Rf$W+/B<0_SNAOC24BqeI<"i^t#kef0s'SK&"+kc[bmac0[\YTVu8@<CFTlWPK-n7TsjR94UupYX5eEE1%CJGm)qT5
ed([+AP2>'_so3F5UqSH8Z9a%+gu@S0Ft"^HWp(_+.q8M&Y2V*WZ$4pDo\&M,:u,`iqK&Q!;A2o:\s3nQLA[Lk?6ZVT,FVDIa`V."8_cPCTIO_2g3d2q
"E[O:DXAkN.3[A$He"PmS.A#=8-P^)_2`onio:e!'2]kDZ#;!43qcM<G'9?o)9`BA"8c$D@_X"S$6)fu!HqA"\#[p^0M&GVoTqc0Mo+SNj`M?=Ts7A,A
RCJ/lr3].]MURVbu9.1We8]c&J,E<\W'10<OX5+9$3,@[uH(6E"?V%sDNP10gH97eQgKh!=%9bgMT%%3gG1>]^.97m+9@YL4^W%2q$u87t@Y\,e5'Z0l
*8AXs$WG4i_R*EGN/p2nhL>EpHeq5[T_45seP[D\,WQ[3-T)0r-fL[M)dcOO3gMDiVfZ[eS**b`"I<dIM\%E/cVVo`L+foT.NcEmi0-F7c?aVk&qla(m
Rn\j#_I;\5S7!1NA"O]Z3%R/)CmZ"18_pcd>`C%QsduLcGI)mZ\2S]%[<D!Z&:s-Yaq5l0A\*IT`aM5M+:@N,97_Zh',aU%'j$$b:fK+9A[1bCG_d!8c
oV^*jo-)m?!70g^1TNeLl3Y^hG^?^Em)(%Lb50>#LU0c%.+-2LsgAF]TrIE!Tc$n>&1J'J19M7hrAdZh6@3+/"J5RNhg%?L.h5#R'aSj4aSE9<()Z@8A
eHShZ".,1rGFW)d6Go22Ak<&Wu)'q:iAR3-ac2\jnt(>C5(A?1P8'#:7g_KeY"34[5h6,#knOr79FM#r$iierNpi5,N9=e4'rXguLb]XtDK!7QuPYC$`
'p5:sV`S&I`5lHAjkp'_a\/_[iHD?j*5,8[KB1nkfYdUG?jirL&]+%5_[dPKW\hL%cV3);V2-Zh!cNHXYc&(M$jiX:Jeq%`]hePd_HUq(oqqi1Z`SpL]
\9^4C7ZXLgU]H,O1,`_elO0liI'UTpXo@Ie<`97'1/iW<?6K4#.:;"=h=/T%eN?X(7pX4G>7NtCAe=UHX4>s4X+*6F.+;E3TItS8O&0kEB;/946mA'US
Tcb`!E:T*3N#uW(&#4=io3X82kNI0#Wj5KM3l;=l.a^KRP,B%;ns.l1B9?l'bs/>oC0:T0%=Q^P#7h+[Cp9a*2jJ3'ak#+8<c40^:=p+DrelZK0@h&on
BT3caX.mHnYS4JXZKs6_,K;PU.]O3AsrLU7NBVh:i[3%b_&E!L]nogporM74Ws2qi`1(TuIF-UfR%,q8kn`_.E(M^7?VRVAS2F+j=ZXglJ_jM\ji/4k#
PH[^TL`>cUKd`:KS^M7lrk;fg],SsV%E0HD:G9tlPco2i>'QQY!QHq__HoC**HbjMb(@_J/1`.K/>1OKp-qcWTE)OuL!*c("sF<K"aq.k>n,3,q;5*rH
=YZ0eS'Jg_lmGWrMek>*A37=LN)>XG5='"@/<3[)9l3=3&A0Ct)'&eb\-#a_^.iu9;<;n@uG4ed\;t]'%B1P&a3Q[H"^KR*TK4i#$KF.C>QA9R]LkOhq
4`2C"`66`Vs*4ZIQi>(!N.($`ZQ^!U4X'Tt#n(^*bJJC5KGj38X:bjcO>V_.laQR8m91r#@mc!ZZ,O[RTPI3?71;TJXXnL8<G[QWD,gY?b5QDB>Zuo*g
KTBBe`=UNfrS"$kd<o$9gi.-0&nhD1@8QjjiFtbJ4E8(HVgbf#!.*%nQsr&Xd->@G0>PpA\=EpV$ckclK)7iKmmcj$#'cVYf4VW(;&17+Y/l&Q=NL-0F
jpS<39J*K!n*Z;Uab/X\_SGs1;9/CcZC]^>UIfoshUQX+AN\as7f\943D]>`FDdX`K-Jd0F7(Ht2DjU3GN>$?!/tc42]D\gj7l<;g=X[%&?\ID6]/AZ_
7XdqEB>]6c"GXV9]MRH\p,jBeb_Ikc866VS/j%C,a#9\!\;od5McS>@0p,m>>P2RTm+eOH7BjUj>M[T\rUr"c5^ptPTOrI^inDOZ5^?A)SMM6c<do;CS
8#`QZ#V'u1dipY!A:8Z62T5V9,5``Z>cbs_'!-2$W(SCUjB.9^E?jmTo28fI%O=0SZO\17/<O&4%;OfG-cJe1abjHfdP`9"Jhp%;<AntW;j.Q&>X65m_
f*Mp)*FX)6ago\?(P<lh*pg-'Kb"Wc)JMPDW/g4!Ff7,!P[e>bBN2gMXrAP[Xgp5!Go>4A&-t3oWmAWpF-i7JGi-UT813=)kQ6pE6t]sl=#nNW%tb@/8
WJ)?&u#74Vbab%Y\VI>@`4`UF<^)jh>hV;Tppm6O"VC6RON1r&_B&5."l70FZ]*3?FFLdku9,[(8jk!fDk_#=b_9tCG'ssc%7I'n0>31a?qP3CE;D%*^
W:-cb.I;=qhlkb<8R7)W_,hXf!'CckKW@K)abt,e`<ZF*Q4)`Tmj[<&%GSW]!IT"cOQ@Z(9%\O4-fhc)A*4S3K4?A]ioVbKX%BnJ`Wt4qN#+'&3RQOBH
L(0>5]R/'5[AI'LIN$XC_lTp/24DRL0^gS[BVH"en),:l;$C;WK4F?P!S[IoJ!qi*ftb,(<D28C8Lb+F^uNEFNXA8M?>p#bfKK&TGQi/;Rhh3Ng5Ba@N
'erkE+FoD(2pBn'cM_+HG)]ta0g\L@&VVl%Z:E'`J[iN2:5)Vgt,cd[SEEDDi^mM2j,bbhG(?5I?m]`MHhOB7A9s9]6q#JfbKVS-tN"d`A`MMcI7PDrR
!!0HY!NjiR]:N`,Z,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.39'
__version__ = version

# -s runs for hours, often into a log: don't let output sit in a buffer.
print = functools.partial(print, flush=True)

EXIT_OK = 0        # healthy
EXIT_PROBLEMS = 1  # device errors, scrub errors or missing devices found
EXIT_FAILURE = 2   # could not check: no mounts, unreadable filesystem, no root
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

def execute_command(command):
    if USE_SUDO:
        command = ['sudo'] + command
    return multiCMD.run_command(command,quiet=True)

def execute_commands(commands):
    if USE_SUDO:
        commands = [['sudo']+command for command in commands]
    return multiCMD.run_commands(commands,quiet=True,max_threads=MAX_PARALLEL_COMMANDS)

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

def parse_scrub_status(lines):
    # "no stats available" (never scrubbed) leaves these defaults.
    scrub_data = {
        "scrub_status": "Never",
        "scrub_time": "N/A",
        "scrub_rate": "N/A",
        "scrubbed_data": "N/A",
        "error_summary": "N/A",
        "has_errors": False,
    }
    for index, line in enumerate(lines):
        if "Status:" in line:
            scrub_data["scrub_status"] = line.split(":", 1)[1].strip()
        elif "Time left:" in line and scrub_data["scrub_status"] == "Never":
            # Until a scrub writes its first progress record, btrfs prints "no stats available" and no
            # Status: line, but "Time left:" only appears while a scrub is running.
            scrub_data["scrub_status"] = "running"
        elif "Scrub started:" in line:
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
    """[(fs, show, stats, scrub_status)] for every filesystem, from one parallel batch of commands."""
    commands = []
    for fs in filesystems:
        mount = fs['mounts'][0]
        commands += [
            ["btrfs", "filesystem", "show", mount],
            ["btrfs", "device", "stats", mount],
            ["btrfs", "scrub", "status", mount],
        ]
    outputs = execute_commands(commands)
    return [(fs, *outputs[3 * i:3 * i + 3]) for i, fs in enumerate(filesystems)]

TABLE_HEADER = ["Mount", "Path", "FS Used", "w_err", "r_err", "f_err", "bit_rot", "gen_err",
                "scrub_status", "scrub_time", "scrub_rate", "scrubbed_data", "error_summary"]

Status = namedtuple('Status', 'rows running problems failures notes scrubs')

def build_status(polled):
    """Status of poll_filesystems() output: table rows, running filesystems, whether problems
    (device errors, scrub errors, missing devices) or failures (unreadable filesystems) were seen,
    notes to show with the table, and the parsed scrub status per first mountpoint."""
    rows, running, notes = [], [], []
    scrubs = {}
    problems = failures = False
    for fs, filesystem_show, device_stats, scrub_output in polled:
        uuid, fs_used, device_path, missing = parse_show_info(filesystem_show)
        if uuid is None or fs_used is None or device_path is None:
            notes.append(f"{RED}Could not fetch complete info for {', '.join(fs['mounts'])}. Skipping...{RESET}")
            failures = True
            continue
        err_dict = parse_device_stats(device_stats)
        scrub_data = parse_scrub_status(scrub_output)
        scrubs[fs['mounts'][0]] = scrub_data
        if scrub_data["scrub_status"] == "running":
            running.append(fs)
        if missing or any(err_dict.values()) or scrub_data["has_errors"]:
            problems = True
        rows.append([
            ", ".join(fs['mounts']),
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
    return Status(rows, running, problems, failures, notes, scrubs)

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

def start_scrub(mount):
    """Start a background scrub: ('started' | 'running' | 'failed', message).

    'running' means a scrub was already running on the filesystem (started elsewhere)."""
    returncode, output = run_detached(['btrfs', 'scrub', 'start', mount])
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

def scrub_filesystems(filesystems, args, screen):
    """-s: start scrubs in mountpoint order, keeping at most -m running, until every filesystem
    has been scrubbed. Prints a per-filesystem summary and returns the exit code."""
    max_running = args.max_scrub_count if args.max_scrub_count >= 1 else os.cpu_count()
    queue = list(filesystems)
    started = []      # mounts this run started
    adopted = []      # mounts that were already running when we tried
    failed = {}       # mount -> why the start failed
    unconfirmed = set()  # started since the last poll, not seen running yet
    running = set()
    last_start = None
    status = None

    def start_next():
        nonlocal last_start
        while queue:
            mount = queue.pop(0)['mounts'][0]
            state, message = start_scrub(mount)
            if state == 'failed':
                failed[mount] = message
                screen.event(f"{RED}Could not start scrub on {mount}: {message}{RESET}")
                continue
            if state == 'started':
                started.append(mount)
                unconfirmed.add(mount)
                screen.event(f"{YELLOW}Started scrub on {mount}{RESET}")
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
            status = build_status(poll_filesystems(filesystems))
            running = {fs['mounts'][0] for fs in status.running}
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
        return scrub_interrupted(started, adopted, running | unconfirmed, queue)

    if failed:
        print(f"{RED}Scrubs finished; {len(failed)} could not be started.{RESET}")
    else:
        print(f"{GREEN}All scrubs finished.{RESET}")
    for fs in filesystems:
        mount = fs['mounts'][0]
        if mount in failed:
            print(f"  {mount}: {RED}failed to start: {failed[mount]}{RESET}")
        else:
            prefix = "was already running; " if mount in adopted else ""
            print(f"  {mount}: {prefix}{describe_scrub(status.scrubs.get(mount))}")
    return exit_code(status.problems, status.failures or bool(failed))

def watch_filesystems(filesystems, args, screen):
    """-w: refresh the table until no scrub is running; never starts one. Returns the exit code."""
    try:
        while True:
            status = build_status(poll_filesystems(filesystems))
            screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
            if not status.running:
                return exit_code(status.problems, status.failures)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print()
        return EXIT_INTERRUPTED

def scrub_interrupted(started, adopted, running, queue):
    """Ctrl-C during -s. Scrubs keep running (they run in their own session) unless the user,
    asked on a terminal, cancels the ones this run started."""
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
                print(f"Cancelled scrub on {mount}")
            print("A cancelled scrub keeps its progress: continue it with `btrfs scrub resume <mount>`.")
            return EXIT_INTERRUPTED
    if ours or elsewhere:
        print("Scrubs keep running in the background. Stop one with `btrfs scrub cancel <mount>`; "
              "continue a cancelled one with `btrfs scrub resume <mount>`.")
    return EXIT_INTERRUPTED


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check Btrfs filesystem status.",
        epilog="Exit status: 0 healthy; 1 problems found (device errors, scrub errors or missing devices); "
               "2 the check failed (no matching mounts, an unreadable filesystem, no root); 130 interrupted; "
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
        help="Exclude mounts scrubbed within this many days",
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
    if not filesystems:
        screen.flush()
        print(f"{GREEN}Every matching filesystem was scrubbed within the last "
              f"{args.exclude_recent_scrubbed_days}d; nothing to do.{RESET}")
        return EXIT_OK

    if args.scrub:
        return scrub_filesystems(filesystems, args, screen)
    if args.watch:
        return watch_filesystems(filesystems, args, screen)

    status = build_status(poll_filesystems(filesystems))
    screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
    return exit_code(status.problems, status.failures)

if __name__ == "__main__":
    sys.exit(main())

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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 54):
		raise ImportError('multiCMD too old')
except (ImportError, AttributeError, ValueError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE'EA+5s6&_Ti3^3S2I-:pLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)]U<,WTZEDeSe:(YNb%HJ57qq1/\
*gL=8;jBHJ\fYg4:j%to1R4$=%aO[S5W>p`gA_=$'[uT/?.1N_&PE1HaE>4:M&BCBVcr3$)%gS.F#Y0U;'G@Yf#\iaYMX8n@Cj7`rmp%aCrJu%B[E*^L
S#9/4@nY7\_*&('7?"ObNK^I$nStm_t)5D!<$XBk]A8FSldVFqkipZ;EWnA;)9(JK#j9Pg8;XEEFcR&MXS$i8K]2@Z)d(Fc2uC*D(R5&XBjOabb#nGQM
s'jk<mB2kgSK<iH7Up,F9L!`X'-4q[s(,,!OKs+R;A4P#:D(9F&6"H-::L31I>l>F7FcpCR'TuK\)3iV_%ms=;+MJU^li"a#5qt/XYPkN5YYCn?/L"Y9
`YKd2^$XX`_0C@\.Y8GnU'3R!cE6c><Gj@T/l.dA@#Y@'89c>!>R>8f@b[+0An>r^6A/gX)W)CDc1L_86SU+RdgW->rUPk!WadE/L9>fri=%uV;mun'5
2_H#a9V4FZFU@>WEd%CE3T`13F,*D5jnV7@&%/X_r0mN$m(uMs3]J)]nP>G)=>E$<Ka)@W:H=qDF!e(2DrId6E+Z"C:Y+AtXI::L\,=9=c.FfG`o.dSo
%uH7$0.2oW90b^E7BeXP1$YdbC<7@KF!8Hc.fK488]7m6(LL7^F94hZMZCP#G-g$#t$[![OrtHQ.dNq2M"K`io4/Aaq:)NY%oXKqdal!if3T"J\jYUMa
LjW./0YE:)=T0`+ld;^/R@33e)T89fst(Z>>?q\sFNgYoIo'<_JQBY'\f>H/hcSh+VW"%i$#@LOBfpHSrTj,-6r$,u]&;aj^I,O#&Fr=lD>U%4ZA3-7?
qi(sCNJI;W70*G&[-fJ9+\1WLo/`7\E(]EH.DE,H6&c&Tr=.K$ssRlF@&DY@bmMPH0Y\$SeWq'fLJGZ'PU2eN-Cr\e-k7O!^?2<R_a8MG,LUBC%a2C,q
SAMc+^H?IF$4Sa9OX)PksrN1<9etSPYK$Th^bjGkW8712[%<ZYdkA$<J;>\N>_k[_Yp6\(PVQP`uX(m+Qa5')Bs"9*sVJUue<mZRI4gd@bSTc.*l_DB:
]h'7/kZ",I.#!O.G)U3M5tT8.`JJD";p:m$m%nY8Iu$MC$2!"*5s!;nLQfud%'YF6[\%AYF<WT5BTWhm=(+nL!;kS<56m%$-bf]iiT:%>pacJ=:42g^I
R+Y?iX4m8HhP"G_nY\R!!DRtrG_6TnSfK5oDGg`ZTcb$b%ENX*M&/WqEj[%>M)d;2@YIgMt?*i-Mm0O:Sn_4&B!*f;qPpgi8XGMl1/_'N4:Xt=aVTUNG
`XH^:h&2_+Jn[T$(QZ@rEcHd^Y1^4]"P@mI,e?W\Lc1f\2P?r8F+VVKP$b-c\gj-P.;DV:K\VXJ.THKuQV#A/,P5:_2uYQr(g!?>BcXk=3_V)KEm)WFZ
6]UA<LG68SQB"@T&F8Ju&GE8C\P8GfqgJK&s=c?N=Jo!d/EGRWuPqt+D1K)qNo96LCM'Hpjj2q-O@p*23uq3Yb[X8bg%b:%5'%3)%l=a-bnWI3`1HLd^
X44'I,mF6(A]'0%1Z)gSI_[G31^mBAJep8*SGBp5@L-?A=K>T+:rAjmV<L;IH7B2Gj@"M-P-012P3@)(,cYp7Sd[c:>U<E8FT@NILI:=]1%L8X;6(^TX
[;7o$RigVuVS_RuedEj>b-nAJ)PNLgi/SJd]"p9:&jj@r6I/6Ym\3DPWgarahNTc&=8F`aY7+t$M#L^0TRq>h]-D_SWGTHf>T@V)j@@VLUZQeI1urGt(
6Srf[E@/sX8Q,L^S_kbFm;c']h-,gXt(I)(Y'?=:37U^n]Zo%ggJt9%t\;t=C&jX-c@bf@!fUXYqJL2:<ODD;,u6l'0*]THKO%I#FjPk^Eq<e;5.B![t
EPS/frTV`*sO"Q9Toi!C=lo=J%!*b'D6'cP)NHZ95o'3G``H9,pK22:16I6FFe>Kr!AbD00R)ID1;-*8d@e-Z$sQRn"U2fcM($\H/MG!;2<A;-*_^ap!
V2AHQVu,`Qp%/K.(t+>mkgEfl>O2T#/lYDeXpi`!+k(*(!a/`M6l$Za&*8!VWS3Yod4'<G7-?&6E@ZGK;oWDJ$3Cq5>i`k6T#F,1]<^n/418o(<1"76;
eSY`kiRVEN_=WAE.eB@;*L.I)H.t6=7UgI!";T+cDPJ2:LVpAmW$)>`\,4/1'"m:"NL*jD8S0hPPVMAp7$m*7(8oAab=4LNkXZ%k%+r3\;[3NYB*Hh+'
ZS1EDot3U`.]4S.;4h#:f2R0-PlOet!e[Lj^gmi"k\!^[:;QPkX/`9(#/\nZhWf,B;Pl"eI)Y5j+1u1haGpaE2]@S0$Z??!2&;C^.u,'N6at@K5Dk)ab
R[K2qM8Y,r5PnRhN/bH!1AC'*lBmo,D>2+pnl(5Z,$TUo%?05,;Np:AXsSb?3tgd6F1Jc/a"GKN;^lp?b?qG+<'<TE/8))BSMD$*^Y(D-_7?$6m0R$aF
&oP4_Vb=#p#Y:;C"#$[$9iD:5Z)DF^mBDG$drZnXgKd'.1eUeW-j-F*J@<UC;&G$o;(kN\?t@n!F+DC!tc^cmoYn`aI>RM+*%![dX-oCraelJ:#u>KI`
R1*K&j#a30,J\g$i/+"mlg>i\Et!Lo-jp^-sFb<?k3g';e-<Q'X<b\J>3aU+Yo'[gs`WiPh#S0L9Wa3BOQl:'6Q(q6^EA4=ru:!*u1O+`:%,rZn-eT@)
>(=LMO[rll<X[mt#l?h<9k/'9`-o<RI1ZsAa`&+)H/s_00b??4kWYG8Q`_'1Z"TnTmBU[gYQg5G<P@T^1)OP<d4/fa8$"bFt\!u5?UHUD%T*MRe7f\;]
n"qjD#b/a(mXn!Af5A?e[2<R>i\j4qr%34mNT`87!eMsJ!kP_A0,/W^V#e@9q.[kO7=OlDEsut+#*PZeT;)Z?>C@("'e'GpN49hF`>k?JR(]cVhjDDs/
GF12JGj4h.*_)ni=>cre2:J=_QeN*iRHt>&2!p!\oQPsf?M`Tj!!cg)fb;&BW[mKVp4"OIT)*fQp_[L`a%qH.n,tK'Tqujp4hTS`]Q*GK#VnlWBBoK.b
pFeJn\["::I_K?&;:ORA$#Sj#:Cc2Dc;dIu[I^mQt.?F)NSLL#N_IV0d?S#F*L#jWE?a21/f7d25hsKWV%!WpTfT9kn:QU0-^[1Pnl8*%8nu[N'0C[hj
j2<WE!k[2ac*4V2#/3CWPqB7TTj/R9E&*nTiaMnL]NN):0Ep2hU3Vl5O-;*/M21"SB92=gJQEEY@6+L[,.'csN+nrjhC08[ItlWB5GkQ'(WXal4P6V<U
C;Akf&<Z[%5=pRn0ai-DcOtfkK1+R&j-qrRkn75KPL0D0l+VsYr`/&f!M[JOHY]/t$%,&:\ofnq&LilJ3_<!E+On50^\u!1=baF%01^Q)6,MG*GjKYV1
/G22K$s:^s#c/$]"LQVl+CiQ>CAZU#'[1]n$.H#sB4\VdFE'iJ01X?ghjOU8gRt65?_9BkbAfU(r@qZpna3Mo$$qBU<noX.'s-*b<=Y`4D]r*?JnV'^\
*c$aq2-dB*$@P^@haCA]+44$N6fs/FJgFcr_8J?7!+2C)r-S"r)X_t5c)sB^gosL$Fr_hdgTOK48NJ,4^>;Xc/3i\qdAuC5!#Rp[o7eVG%@Y9ZT*Jdm*
7Gfo,+93XV#EmTj.F/,Hu@['80_'C*kJ:!;6b)ntAM8[o<HYC`frVE1k3G,W+jSU6A,sYsF.:R6PH:C;$7PSdlK%Io4CinX&2qkZ"[HKRnNa81_FF6>$
B^N*RF5:-@7Q2*Zr@>B2:+M:[GXe)(O(]Nn(+."f-`Fd^%:$5UqK5;75Vm^&KuRH-dnU9^r&`82`%HfH*HETY%b,H6NGR4/#)<^219m6H/9j^fpp.QK#
U/@lk>i/M$D`fmDg)<dn1bS!TS=\`cD6^iG=Ud>+/[7aYS`K2U&;.GMN"7+?GmEeWbM/g8I)1ZZ,bG4;4r8Y((;gK(#^fm@VUb5;P]bYO_VG=/[b40@=
Siqf\B+>@XZLOh)kpj"RRR1`#%,]9Z>:^R':[mI`H]j]#2^u%Z4O3\!qs5'`H%:1#(mt)b/@.EPj$er<GgbLnQ:7pBN"D@J0Zb9+o_Li94-b?-U:hl)Z
DW%*<;)mlj--r>KU?Rf'>nro98``\QFV9Oar6OrL%X%F@I/"cXj's./a%&Jl*"=Ig<7TEAs+u3g-A>HTQ((b-nD6D9R--TlXqFt8$\#ERFTRA<ZAG$rN
6)]rSc>eG]XtheijutKop0Ap,@;8RKB$gZ!u:(pTi&1,F+"pU9Z-U.P/d,`Pr,A8UAj@-tV;'fIR?p0Bk\VFL0bNc[7,,c#ktE!^;`]HlIg(in59L-G8
0YT!Oef;?NY4^L-G&9*SVO(CFRGC-f.:@Dco1$U9i9?_$n!$RLme+:Yi%@*^]l<_%7&?+ODLe`1`5WR0*fKh4eb?OG9!^$YrIVi)ZXmGQ`)34^`'UpOD
%VXWV#]A1CjJ;Olg?QgY+ML=DBRU!;G;]6U=PP9HRgiud[%_"3NbCI?SP;+PFObE&K@>GHH`Vk`GVR-5;\,X8+''7Ih]@>2Z.i$]kjg:+T/oDoRV:!F8
[N8c$Of/,r*"kMF<6o=7b(B=]2meGVM4sh;<ZG"-.=$nn3,j6\b\aRCG;#>cUj6=9'a];N-?6=Rn_UWZ\;dQ%KHmb^g4rBB$Y_`o6`.'%BrtG?=RJ)OX
CV2Qb6"]GH<s>@aHWkjWSY_t6F'HCg2%nlQ9]!'g)^BFn@$6'R2,7:*p7aRLnn7A8EK:oF\8*J/XoEP2j%d+S'\4YdGhDYs#U9Y`T;!Wh]cWX[k0;O;m
<tEGf_2<:,$0kH?U8H#5sO@lk%IcnYN!08lpr`G_8"4[\<+[cUBAa_<lT8(b0>Z\D.KWgg"'$]uVL>R_RKd\WWn?E6+-p^I'[cF6%?Am2Ldt_8M6$2m1
<=8r&$L<DSVRBKhuJZcnM3fmH-Ud;M-1HB1#Og"gP\nt2FDTLej+AF%IK8p0fO.<C,?AS.8g8Ig]eJS78HM@anCMiN#3Z?;0gf&2an:Q_Sj)Rs75+FK[
kY)'\^cpi.B9(BQ+kS`Yl3*L2[3G(Mf41]L-%ceZ9OF(n;"R]r-bQ#[A6<iX\=o((YX\$Cj5_D9U,)PfA(.DdI"Ud:/4ijPs2csf(8@(a-,n+"/Oa)!2
`kO4SIt3/GU]1^0a@]q6/*:;V%%hn*\j@kh)\7R3rs,YW(X1>"e<)M7\P"@3UEDpRF@[IDJ,QH8q]#::?l"WDn=WZ!JYi8<rP_cH=bVqHV,)NlJNmG9]
!?=4ZIL//-hL[?"*RF.Y:6_f";hdg_hU^1nrBi>%#TNj+@)@a\X6']=.hY?gk6EEP\onA(et'E04cL$("JJj(\7nDKq2sTW?(HtY7%0@k>M"38XY/jBE
+KnTg(!VkY'TJ:3=C]ZI^Gm+=qg!"2\8t?UrHUr\=G"BX-AV2,`Sg!3#FP;<]OL=e71a%\#LDIglGL8k"YURpBg+3FjY570uYs4;)qjK`BiaAu`.Z9%q
/kY3f"GeQ5>,ZfhQ^<.7lFI'8('-@kLdQ(E\f6!D&FNG?7'\`/Ggqb<8KNB*YB-jO2:+>Z,ZlQf<]O9if9/\2c(-E:HiBUHK_V\WenLuBS5@qcP%\(.i
GS!X+MWAj(-o6YP$Y_GIgS&Qp&)b_Z]Q?cg!rk)indZbgTQc\TdFU\W9GA:(WYA_>s+KeBrEa@h/9)so]:iSXH7LTirQ\t$lO^/n=9dQ#5,O7B0aIrH8
PR5S8TFPn;J`NI`WB.6M6iS[adcM=R%uRm(HC*7;1)n/NWR4'f!RYDM5to;p0SDKG45d5r8hPh4$!+W[0/E[,q,U=?9?<tBYXJdY0lWl1AIkFD,2V%MH
fE8<"'^!b[M1,GKJF]Z`Mp_-oQ3,SOtlob"k\sH_05i2)',Lhq4'Ri;N\ek/.ZpJ%CG6.c'KC_Gu\J[5mJK[S.;2+K`qAjf#fX$bp4H$VR0a)\5D91?m
K0]-:m[BA.Mria&@WGH(e.)WAGJ$7+Ed@!QoX>HAQ`I,J6*i9t>6Qi8#I[oDsD11\<W>'YrZJ%Jm:moQZJM8=lPtmfNBHq("/ugT\b14fl029dWD)0*"
]n?BC`"N,-KQ;m#\,qJgNVBqt%\N_\5P&`,AOVrumG#esrN/JA,ZH@t;R)`Ga2*=+no'ojdlZ(bCB)9CP*bX^SCIMKe3mo[U(L5b:mGbg#6Ck\QI)S?+
fg'7[VhnX]W-1<?Xl%IU\Tnq/WmdoSf5ocfDDin=rr<_g^5POI'EOdZWBq/$HKm*4VkrTE0Q#'TU>KsTbGj1(\ig0"$[,kb;ke2P&0;V!!oXjXD(uPG$
53kB:9:&;grj#&4($o91HXCs1&Pf^4S-^N!2B*II5lY5ql#n?/dFq^gU$;8P4s!*KR,fhHg_Oj3Y:,m!-XRF/>()cPl/W`Vq&k\I,;!nm21K3N;&C!a#
of,)FeAm_dfeB3XIoV"ECqKB8jc.1)uph`6eT*)l7qGl(1O?dpEFf)pSkl/7k=DPR8W+*Aa`t3Qpq-:3V^0\WV,kB;2h?"X*Q!L]#W!sJOI*9HoUjTb.
87P!)`6917s99c:@77^OWVJE'-ALW2r]rAY]f5U8$mYFIp."K%u!!RU@#7E0"'7NbEURr4t&u<f:oH:`U[Z[hF:u,7Suoh^H?/iH_g/1:5UL,35eS_PL
kB+W@JG<L/j;8B.&-X*]Eb4h1d[e5$jV.SQe*i?Rd0j#*WU84]Bo(F&qMj^.PAB5"-%`CHL7WuFW^b4WC'V+fI)OJWIrZYYoF+EGhPB`h8IM]EPn-[g]
p3^1;Z*2gVMgUoHbIQ/@[%Ihh)Wi^uU-YOWG=t"";BSs9Jd<:oN\l@*,6?r>Q2R:TQbTI%LI7h1;4XqipD/f'4'ar.(<!9tJ%pc4G?KprCNH:X'Ks&PX
]WlA(Q`\N[L?J>[e5dX$hLCB]<WS/Z!AD?325jspm+k<:=c%brA.IMQ'"u)p=MLV)#(L?sc>^?dF5\tqm3F8u>)qm@fi^VD.W$dqC<1G_&spE(Ypp$62
BV$YnoVrX/m,M5jmE&).X#g)RcNoJWkOGbEXN5m4eINF8=>RC"88Z]GLP)Tl]iuQgH_$#^IA8pV'H8iJrSVtP'O)24W^^",Mq':9$AL2d[[VPZu9(l7A
o$TllE?IX)>Hhp^.SO<uJ00-ET8rT5?TC\+uVB/5^C0<L-4N)8kcC&q]7'?nV&Zc!eT9jPJp$+SJ'J\g\QWSr"E_,GU4Hm?PO2;,SAbMcbg`$V5[W=KR
#oA"h&:=d*!cT-'s(,o5EIe.lK07-VT`lG8PTRSLmKfd@;"9hA/giY[/9O;)]Wm+7rBrJWWaggufC>iItS/[J'MCZEp@^BsC/&0niO@SYJI*^Iq?SR>d
`!FCO[df<2GS+;e"3KS'kT:SEkB\s6e;abj!gSO:Hm+fB`-"mMC,n95q,T1pG;D:?aAr6s+q"H%0*P1T'bb++r:Q*Pp?Yf4"nL@(,UkD[m]h)!3BF=_3
Gp@YeU80?F_T#B`!R)0N0d_c7+UT;:qN?8sNVu%R-`%JeQ86DGJ"hu30rg?Xr.S\hnUSs'2,bAN?^:t4dV';DFs*S-3Q*(320c+,U1)2p&t5=6@>u&lq
tV!J<s.Z7"!>>q:i1'VFBiL.4K5m*FVA.q0If,E^.tLg+ujV\,HkmD"N8ei!n?!T"B]]FFhj6H,<U2k2"!G(FN+2he&W.01lC,XOTd"UEQ)t4NBO"D&P
E$[]qdiBmdiag9LQC'-3ID`Z9saqNLpieJ>1e_hHi6VKlZ"n<,O6C*b>f]qa1T>'OkBQBoe+'!>r"3Xq-4iS-Y(4n?=;pJD[qRTBeF!#<nY42ra<(GB7
A:;h5C:H?>cuES/</Wsfib(\8)g*?ZPh7PESdcNRpK/m.N@F[l7+Fiqd-mnm9lnFsSMn>`(/U?60+^>CrBkX%sL.gL8@eT3akC$t<^r3F2;no$0Wc*>G
+bkoOO5B..9>dZhZRqQjl9^lVLi4nl1U?\=XYuAl7)Z-JeR?7n%(d0nsdbC:be8]MMZRO:D2+Ps6R!F%N]Esam5"efB$B,4pbAg+_6:[Vp[dV2c=Rede
V/)G"r5K(00(uha![b;lP1f&;&:M*._`3=YT<3K%an:e'[)8HTrCH!FPLV]c3h']Nm!MPQ'\!B0X`n!#O:Y4u_LXTMnJaKFhY/Q#5@Tp05ZgLX7/_N2(
iGc35*?_";Di[O!Kdl"i'L!,%r4\ViD\L#cV5d!TZe,a`?-H%i1ni=FYspP>l=Ir7"cJS[32TG#$V;[d0](\#_^<g4K'qphF#iT#7'hIfWPT35!2,)\j
I(6TYXa"&rJ:Y7qujk$j*bq[Q@VY)1=J^M#u6P![>F"G,6>o"gp'^.-9;2:m#0*%s&.>.A`/sj&Jm.gGPiN&L?H*Qbu$u1A_l<k"*p_AVJ[!(q*TM#T[
C1#;Qo!STgZe#cW<e!?Q__[(h!>p,O1/;$uBns#gaQZB,>[a-8Z]hmG`IGdLeda$a>G2(b=m!`Pd0M/$0G_PuYt(N:V(kqMFI.Hh3cLY!`E)jO1d_IB0
UeA"#jJPD3u/nLMb?;@/?*kYO1-pt0'!1,,T(a_J7<kZkr)\IL,nK9#82TO/$f-r0;0HDBXOk@;gT^e(Ykdu<=;>K!_Jnt\;1"p!(^tdaOoA80gN>qMZ
Tj[D'[t%AdFP]"'l8]0P)Kk"X;gM7N)O(gZ@I>:'I!ou+Aa[+?7dg&lZ'5N0p*u$&8:dYdTqnQN;Xg*qm\Z=+kW7P(<(/S%S'B!VO20Bh]'n)qpd+9p(
UI3QpV:p((WWpZ.BAa*eb/D%g)uRqMkGP+Nj-)^35p%ABu95Yo$C;Rf-nQuiRl89j3EhXU9i(]XhWqR@J?;\b$N_s>7nG_&9(X_&X<nf[0=\2Bg-O()^
q?t?^BFfAlK'A$/1%I?Nhh-"\d<-QJ/dr#if+belhu+RKM5b^m&(tJ37$[:aX_IRt`l'`]MI-0hl-6jtP.RgfdnXq$<!I>*FrrX<uNL#E1(#1>[7Xh`=
ndMF>_e%A-bir"9S&JLqX$'u:OQB),Mql)CftN6$]aKP9d]_'J=T3<[#"+)CdoR%m<=8)grIYc.@]]kf!K!1.S/q#h&X(2.1"ld'(_Wq.V0^MR#fN.KF
p^ahf^a6pCCGBbP<'+ZrYa$<1Q(r_A.8+mCAjZJ%TVdbN,``@S/RdLL4k2<QXm*LAf;AJo314sCF1cV%NMe/nt>h>hB;=r(7F,5Q3b.n08@O-TRFtQM6
@T3iHT_P1nr'>ksA[^i5?l<`5_g<4gK'CBToH\8N`a]\S(#2)ciN.bcWh[FJdbN5@X]OTA;O_t.[_F&e",IMZ]-K;&U/9Onm1q<HHWQ#QR`]s-<aG/&:
c9Hl9;[L*O(2P/rnLtbrEMbuI^BZH+Ql5,llmIkO@(0$e>*g?#6T<?c1JlhH;rJF7PGmp<MJbX1jB"_XBp@WW/e=m\S&Z7<Aj(^Dk#(Vk8^p6l;GS_gg
sa:H6jY#=U!4b4GNl\=5'C&8(U+e%[Kj`"IHg;etLEM%P;".@bE+nWd:P`eBhQ-b0CET"-*Foe5o($mhn\;CJt98n>rte^40GCecKlI3r9m=[$F%3Ghe
)RkgseDgUA#"8-/_C(0cnE^0Mojjde[j7?)dTS#)N@l#;M_/^t_2R%<kj>u-:iQe3;lXtZ`)C]!1E;Xr.uG8'n[%1L+"r&;uc;LUr7^nnmn2Opt3W%MJ
ACC*>.//"sZ^'@PdnJ"'#2!7@??M$h#.=n.?6qp>=ZPLpd&ZP62a:YM>jrJt`$blT$k!b09*talW?Oqc`W#(SbJN;JoMGk%$1]3#%748!U@,a0'WrNV]
-rgQ/9K,#u6OR'sF+7K]ej9c]oO4B&OE"ne+W'EZgF^Fe97'PK8Y)%gNKft_p+9NLal;8NbKK(+->N%kpG1K66a?[CKM>^rmIPoGHX`./rHbaVHn`>JL
KD6TI#[d6XUf.JZFc<Tp8/kW^!cKuP$=2^$f=`F[GR4kBi.$"7MW"Se!&CYNQ>J>EBaSR7Ymf"+^GQ._sSqiGG2`dTHJJ]GEDuS225RaQpo<=&8:#bR3
OlEKSe?j%EcsXA_B`Xlka?.Q?7CqRimEWM3`QF*SK^L?abKk@:pZMM^W4e]Kr2B0;OImroS>\'D7,SC\nab`0+2D7mn%K#r[RWJqdod*n!;9%%JFY_o4
Z<Xai.P53eVc^b*%A$LNkdlJ$@9Vr'(iF3hHP[Kl'hq;Klse4CjM"YDJ\eZMBFXi%!C+or`JcrjMQ8`?/[:-hVsTqN+:=E%j'WY)>S#s/56oeq,*Z*Tg
p$6]?`7(HUJjtd#'^UOB#hINQ!SHfY$Y6aI+^acu5O7e2GR,D\CQ_#N'EH61klGhgZ:jd21kkY.ME^IaqV.m,VSVNI^(WnPh(\aJKed';!/,0Y`HNX'_
H4Pf_s,HtMZX5.,hO.mqE/`muT2;HWM7bWYho;$[ek"f$8/F1T4UOT:;%'l>OXe;_bt&U.]FeH92(#8F1DM8WMToAbJ->nrKZE(CeWDadgeS4\IOH%ri
Qm1'DhMkF,Y]N6oP@i&T(l[3rC"ipaC(VKlSUaX7bQ9D+IM;b@gCR2\1a^MLlW[D''mU>s$=sDQH?O+>FJhpIXha2P^Wk;$1YBs34S^Js2.r$RjWiSch
,'K1(#cnN&[K%[Ng6a:aBDtVb(b)4?FiU`0VOpV2\YE()s)EU_Z"j>PG<2]!d-'6V*-A_W7Mb'%0@;mBs5jE5QI!q*^l>7!bDI+H]Z2H&"/&R"N".C\]
`Ng)S#sJc4HjCDA]F;mkN2iY-N2QG8mpZ"2W#Vn]7R1.%)$RLTC@>co9pLD$]QDfu2=P77iK8R%#CYgWI3B)Gu+AXL=9h<cjE4Qs=%l`Z#Fbo]$U@IFE
NJWH/DH.En@)\^96Z0Z-U]=5gb(K,k9/4BK"gufKnN-`U6m%0Uj$G4itO:?@6GY1(AG[?0Y^Lm%pRu't!]'@LiOU^/W0m?@BqI+L0(`=C4@bMqtLPq#D
Z\e;BoL@4:F:o!@ds8Kms,Hd2Fo!*:XOsrhA@!<sd7sHh"d",XDg/S?Xfsog8PrUs\/3^7A"Q(^aJHb*hS0Dr%K=6`nrrGF4]l`+9&HqU8&*80,l'BO0
p\,MppC'aS1@EgnqM+Q!%FmN[5*]LNbO;lgYXnABbUOZ;C5^B-p>HZ6EkP!>j7&9>?&Ridna_?TQtjMM)fQaXU]ePY;Q=r/^cOd9mPW[$0(0o]?+WmKS
s^5b:i^npN^!Y=CRH*m0=k-)Ag8URX`kcDQbZi\>2Z)6Q;LJc;h<#H^*8bkuk/&_G(d/r#65+N-i%`":P1V9cD!8_qi8l^3M(VZ[9*RoK&=1WRe26*\a
9Y/jlT8["PKp6al/oJ'A`]:YSgq0\'4(bD77In1Y#-%`h_:JNZ<:=cS_Imk?V?087de-_.*cDk[%1g=)1F?p@aCg>nQ/RT6o'C9j;"WS-mj[$\'u<'H%
1gJ%E6dJ;t\q)=8ho&?YQc$:&)grJ0/Gu*$Us!lQikR7+ih`U>B!l7TpGU887:M5/GUn*$]m%P#)8Ou_K[5GD*Hb3jXTb,c1QF!=SLf;Y5^"8"O;a"+;
N#BP!&c_\N]VoJ,+>4+b/0&6S&lQ0+dPln:1_kRfPA'1:c^)s(L#O#%7dEDsKfG$3BV78u7KsiUrR@Z`"'(a1p'(9Q,mOTIl<+r*lho,4J_"Idc(^mM6
JKqP&NL_C>R,gm*=B1uQbm38LXLNE<@3Q"J]9TT8ZaE&llsThXPX?ZDXk\7+*?,6MA/6'2eXlKean"7GiM2<+0;[7Q6`(Y;:Z3,d6?>1n)kk`0W'W?<*
o_S6"Ug#_sJKt1!?:M!G3YL]2<1LAX5m:TTZjgojr4%(Y?,o]@BD=(Z$6#/IJL%!rL"A)]K1;aEbFtAV.3qe*kt,pO"8s_Yjq8`[FgBg]$BlfD,l:LO7
YQ]hu[$?>5NGoEr1_IT55<iWi+Y0q`5MEn!b>*BsB_32o\O02((GL<]lIE4M1%F_7G;lR5;r*o/bhSNb'[/r2qrH5\kt_@).tg)a]V&eC\sF,bUq\8q%
DI(+HX_Hrr>8I\p?Hs`::D#k3k3TWr$\M[5#NL?Lod"j[V_1(^>q?$^u0/tt]'?)J-Zl`2NqEnc96!JnX;Rb1e*t6i5.?U9OE3*Im?<%cXK4+IqbI;+(
'jWfb_dFp-A1OHMMHlK-C<ZTpURO_(q],9o.u+_Q)D+1eb5KVD:pQ4,F)Y!gM0q]nr<jpIln-//+#7*X)q%T$j:#9bW2b072.2B%TU"NNWg)\aOiV<3-
5g):4UtjBMrhZDhs$_7$cO2=lj+I$Q2cQqnJ,p'rGjG131gbB#YV,\\JfW)l"C$1A6HBu:Ak-<c?D2u(ITWUqVOT3)<[kZ"?MA>4UI2$8Zfi9km5TYgM
&D4fC%!jSo7ONBb9a`gg/(OpW/4K*Te>MAjHBA2E(/"8]iEd\%Jhie<dK!Y<-SVVr'3qNltGM]PO55oqP"tHPNGBT=XqkIDLY!fFotYCW9*dOocklGG+
2&(,$JmSI;q%%Qnbse75NJXg)lSOTNI=14$c1i5#=R20"OWF*"mZ)*MBe?u"gm+0SE*IAH.fg;2/_@trUn>OGfW_N!RopM\"!aV-,cOef6]R+Zk&0o]T
,_7d^j;RI,F'm#1ibEshu<@AM`$@^$um,nGWIn[U.gI<eUqhpRS"[HY<C#acPgT4L6mCKG1oTF<,=LmH_&fu)b?":[Q=e^L@h<d.ei>-YEI'srg0uKhS
jMJMRn8AUSs!-%27,7W<B$pHViuF`)bE3<PYn<.n(es;#4(39OYk)/reD3tFCe+TV^+?VVcMjrK^g@d;D+L=O$[gbhLU+E.>%$0fpJ9l*(]h?0M.jXIQ
GP*;N9e%O2FHXL^-+%\_"B%bI0`0I!cKF2-K0jDn]&<:+KtB6Z@DqY/RJ4lGbQ!#)BNVV+FiS1mcS89]e]AiI9Z4K@%Ro,E6AR<E>u&HlIY*I-$Tq5l'
Lb:X]'A([dFG2oJ..XL7e%8UMp69*<1/CgMEAZ"eM9LW*2!HkL-H^1c=?r!,$^(WoF%QdAm;Zoo66K2j*2rWBSH`C&b(J#aYAJ1<6Zcj)pe(@QkVN4OC
@?W_,^9lPlVaEXl^b3K_BD\n"gdFfj*h!.M5u93a]DVbHT2Q^\qI`5FRY"SIVD7CcjVP!MC&f<g%>auZoR(f0a55M5ijJX8ng3oJs^V_%7eKiAp76kT2
8.siq%]2@fEF4j[sA+i&L.](C`OZna'ln1j-I$E^`Ef?_OM)0ljKlHfFfJZOs2XGY[\MPR<oMiU>WrCtuelQYu9).SSikU.]%(HD#_iX\4`0i*U_On>4
?9Uj$D.ph(-8DQCApYd(l&<+j>u_mf9.pA)h")XL%`"FO5!n[QVo@3Cag36RiSJ6IY4:M>U/AUO&p5t5J!-DAh'S4<&RK*S!tp5#*eqB<ha=gC(79fDS
_UUdlZ*;jM=3c&_#Ck02ujc1[35!9c.*Is+,I'*kW[bD7Jt(i1u3SX1oNR;/&9CDPk)%G,gB&q-5deBnn?uT"b6%5P1UYY[Cr`Cp_osW)R^'5g>"L3KL
Ylk%YC=dZ:_mV+H!S$%F&%-hh9dXbU'LH?XpS(NG(g/dNYn&<:&3AhC.,(n5Q.SL=0cia4\s>DeIY0;aq2Kg/k%6Ui-&!aSG'j'>h&?hND%@oa4n])86
tB!n;nZCPhhJ$k7,d(sZWW=!uqM4^24,1[ck_&?f7X"/c(5<G23>BZ_A>8L?M-lp]3mPlCs5q73%\ihPRq;VA[pP_H_O!gN^qhVEf.^bW%k7CKV#_a_>
^6-Z]?20Q41%fGWW_GuS3J,UYK25:en28`X$&.3D1>0D.[[0!`k(dKl;V8edUE'!5j73.;14#iZI@K:eHE;p/:NMD2F-aaaF3,,mtbI7)PW=;(tT3BO8
9jO^"U8S[lB]M0Fe*cp9p:+#V'T^mMaSYp5<Q:a=_$7ZeRj%n'AD9)&hJsL3.sl)e*Y@57]n:5hr7ZU-jO[CeUAD.VLd=nRL(\;j`BNZXQk!I1P6,,t'
Qt=P9e4iP,<uq`YMPE$qd=kD=KL='3,oJjH@Tn&E(ff,RQ1ZNW1-G=opV7SUZn)ZJ$hemQ8N]rkD:ZnZU`qC8>aA(VCgdVPJ-PAJhE,Wk>Q7(Z@Gq6>a
WJNq%$;LYa7LZpRXYWGQ:SbGmpUG%,0[0gVYV?aXJGIAZmBLU`iEsk[,qeTb`\[_j,l(%cH74I0"V!A2\D@;%(hc+,6g2G-qkc/P;<g)Ibal15d)6ePJ
m-Wd:@r.&Y<Z@67O;^h;[nR.s4f*:VYG9tB6KF)V)T^nBJn0JQYo<#2Qshbn;I7hQu?[q(q0?H.md-Y3Jkb\>i@=9(9(Id#ng(V@tr:"2V&4=,`5pIcO
5H:D,]_AePATuZ#EqAUupq=@m)P(SZj^*^dZ\cls=3p'#G@qO?Bh(#(7O31Apb;87&!lF"t62C<^^(blCIfF,>Ua.Dl4-Fl3S6Uo8UWrs&Am5JZ(tE\`
r(`W'63M`9&J4"-Bs%4%Z\JCf<\WtQBFZ!We(f84K&u`$O-C,6q-3YKZ'6dU[2(&OeG06FB!5=??,lB`>JpM<+o&RCp&_+),3oOZLiT(@bK]/3pODUe.
`[M!<Np'dY=`D.mMX?&6gWZGZ!&S-_+TcR>Q-ZX"P2/rKhm[:L+'jAluK^EbDngnEW2_$8c@r9k'cIL%e+483TXm4<]i+E/102e8lRV7oPiM0H'.`Sf!
&[E%1CGHI72c@d*NcJAE$4EgfQRKZP(eRs7`Y;(jPb0.@3hT-3sA&AW6h!KOb,Nd!2Y@ku8A+G3sL/C,%7hI-YmoACH)Gm@agLCj[padjZ5X[Fk/S*<"
X9!r;'o6SmRh^Po+8WKN<OkkQn'=C'rmU/49T>4TEj.4HAJi[q$hdB=Va1q0H\BN$+6+4eC78(WiU<:;>ceBOC0Jr#Y$]pqPK=/6NI+6K%<U'[+nUb8"
%jWb/#&JMTZ=IXEo3iq>Td8W^=Z7"oFWa)B*2Sm'48/5QtMh*7c+F>o0`rtef`&Q'-\ca%M?n(!pP7mEG?koSfj!H%.K1#_10\9HQfT31^iu4/)l<DcL
1MFI$J[Au`HDu_[#15`Dfh<4a\h1keGT\K;DO4][..]tqYo:`L(;]\QP%&ZD;4.QQJlf6QSGNAm38k./C8i&UBf`mL,YDs#^"LYrhUB_dDo4dAHBoF?Q
9iR3BJD1/B/I`gQ]"GeBgsu8^_#HAe9]Z`6[JnL6'V/tbH<K#!BP&F;b"=5hX,<mn(Y`>$,TKrqZd_j9(!;.f57Zp8o%pm%Js$t]lq!]$f^o@X'YqV>@
;LkNST`nO\sg$5lYd`Xk1l(^4rJYE.3U5;e/=eEf-APD[q5%C\)mZSbT2`c*_Of1sfYYohGe(7F0YZrgn5[VaW<h;4X[WqYL((J#m\!D&S<UB&TfZM"(
gd7[mk\/Eh)l.0;7nP2]U5**3S^nGbW.`YWeM+T4jr&`UOJ_pW!``B2q;30$D_!F%9<JeX/XEXkK3c%W+!"VRSY4.aH=2%9PDaD$2["jl(eFr4+aZtC%
O]LhbK)@pJ!Cd\@KkRU<6BR,I+X(_:s6M5RieHSu4A*F-bSttC_a=_B.%9#JlSihjtE_nRSm)k(Kk[8/cU[F$[YE9Z1QSi!>FN6neC\LWL\:WcuqPMR-
gqH+K4g/BXJR('aH'Lu$ZYaO_-1GKbj1d(mX%O=Moneo5Hq%fBV;q#;#S-sld7om>DEeR[C&7)d$*-L0,Rg.i1Mm9*`X[j0@O2eNW\RAqPQBs>5A/7)o
HDsrfQa!a:?@R;.P!]2,]>(PKLG0UH%Zj\V>uj(i]A`nKJ[pU(gbDor+SD[>ca3a.WatkheNpKW6`e7nZQ#M;*T,9V((5DU?cZZ1JIo`SuQTVM_i\-E.
?LKIVn_M$G_n4J)7mD>%6e0$(_cDq4Y23f)?K4SG&?.FaQm&-k#"c**U8"=V,Z;BB:t**p(=E62PGn3To!B>.IB-T>7k`13I>.YX6K9n+9/$a?U)??WK
%&(\A,#Hq4JrJ;.2Hn#"Xu@&[T(Ng*umO`-dh(\(C0dF#fSG@iJK0jLhZs0kut\&50YqC"WcOe'/V`uhB)>Oj1&+1$%>bU;8pYi3o0!5VJ?6/5s1B8Dp
F]84<Y\%^<3HdZ==VkK"?EpOWI&PLQ0QYRH^?T47jH9%,:8Z-h%h%Cg'X094q;0!,$AaHk^c@\'RbY:_57R7p*D=&>:'7XUpo<>VD4c\A?F1lgUnf8@C
6#MAiPJ.c4p5l`XkQ!KqESq]CoE.I/3Wc\?SEb+J3@_=s"'E#SAVLXR;o,2a+lpg-2Q,jUBpF.Ya6aZ4On@8p9(SYt/*^)5MQje:`9ZIW[1e!(mgi#mC
R0ll=/-"61`@TO#lgfjEs6Y.0XWd4,Rg1dKs"$1.tN,emV';`#sL'CK7d9?(h\Geq%>+Z]Dqp3`9UO'`;@Y_!!1M[^Zbe"FZdWIZ,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.35'
__version__ = version

# -s runs for hours, often into a log: don't let output sit in a buffer.
print = functools.partial(print, flush=True)

EXIT_OK = 0        # healthy
EXIT_PROBLEMS = 1  # device errors, scrub errors or missing devices found
EXIT_FAILURE = 2   # could not check: no mounts, unreadable filesystem, no root
EXIT_INTERRUPTED = 130  # Ctrl-C during -s

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

CLEAR_SCREEN = "\033[H\033[2J"
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

def execute_command(command,wait=True):
    if USE_SUDO:
        command = ['sudo'] + command
    return multiCMD.run_command(command,quiet=True,wait_for_return=wait)

def execute_commands(commands,wait=True):
    if USE_SUDO:
        commands = [['sudo']+command for command in commands]
    return multiCMD.run_commands(commands,quiet=True,wait_for_return=wait,max_threads=MAX_PARALLEL_COMMANDS)

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

def find_btrfs_mounts(filters):
    """Sorted btrfs mountpoints, optionally only those matching any pattern (substring glob)."""
    mount_list = parse_proc_mounts(read_proc_mounts())
    btrfs_mounts = set()
    if filters:
        for pattern in filters:
            btrfs_mounts.update(fnmatch.filter(mount_list, f'*{pattern}*'))
    else:
        btrfs_mounts.update(mount_list)
    return sorted(btrfs_mounts)

def discover_filesystems(mounts):
    """Group mountpoints into filesystems by UUID: [{'uuid': str | None, 'mounts': [...]}].

    Subvolume mounts of one filesystem share its UUID, and status and scrub are per filesystem.
    A mount whose UUID can't be read stays on its own (uuid None)."""
    mounts = list(mounts)
    if not mounts:
        return []
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
    for line in info or []:
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
    if fs_used is None or device_path is None or uuid is None:
        print(f"{RED}Could not parse btrfs show info.{RESET}")
        print(f"Output from btrfs filesystem show was:\n{info}")
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

    outputs = execute_commands([["btrfs", "scrub", "status", fs['mounts'][0]] for fs in filesystems]) if filesystems else []
    for fs, scrub_output in zip(filesystems, outputs):
        scrub_data = parse_scrub_status(scrub_output or [])
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
    outputs = [output or [] for output in execute_commands(commands)] if commands else []
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
               "2 the check failed (no matching mounts, an unreadable filesystem, no root); 130 interrupted.")
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

    filesystems = select_filesystems(discover_filesystems(find_btrfs_mounts(None)), args.pattern)
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

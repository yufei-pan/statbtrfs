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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 53):
		raise ImportError('multiCMD too old')
except (ImportError, AttributeError, ValueError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE('"=7F>)aNi3]:91L0tmLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)]U<,WTZEDeSe:(YNb%HJ57qq1/\
*gL=8;jBHJ\fYg4:j%to1R4$=%aO[S5W>p`gA_=$'[uT/?.1N_&PE1HaE>4:M&BCBVcr3$)%gS.F#Y0U;'G@Yf#\iaYMX8n@Cj7`rmp%aCrJu%B[E*^L
S!Q)sV)EkU$%'R5+]C&D34]WSp(1GMpjr?eFZUFBtO:7S"_FBE_:Fp]P1cirl3Lp[BOnN[d(sd=iG5[;N@uk#/s16<X$)QPsBk09+5VCTZNTN,I8&Gf'
NK3p;9`7T[<s8!9b^%su\coVp#R!?RH,5WRp01=#ll$L0DR6]U/mk/1.3m;'j9RpR[)9rbCfeui0V4/M:1r0W4P(-HKO0UX(.Z?u/NYGp0@'?cbtT)Z<
V8;dnK`UI+!>^SO;K.nL4k9:p;Y/$V<5nf:EgiMGZaInf3fS@Sj[Od>=<[FKoFSZ\*1GQa%D7eV3(g/Pf'T>ni]=4RZ/Mrr]T`WMT)fo01F5aV<dMl/\
SJ%m3H`,;:iiID26pDo-CmGX`9G&.:bFs08m^WUSP#d@nG?E$/q9:>'.5XRoOoH"+N-"ohrG@j#?:7lInp]r4D_e50-=nO1Y^eD`cl#Bq!<<sYo8`rpW
>oq?;0+T%);t`S#Nf99S,'iM?Knk]$%J-Bc]O$&AlMcA&bueFj\sl"b(<Q8AAW6DT6!6:U>3C/lI<%'X=f[Hkj*Gh$IV?+\HL>VKq\05s#N4XnSc>;=,
ZU@\Z-j>@0U>m0/,g#]nu=H`_pN=g+a?b.SCQX9!%ne!GmGtpeoLljHmrfloCAR^2`5$F23_T4:OVD=L!A/+i#RoW[WPk^T^^nFEn=91t[YA>";S($DA
Mg@:k:m+9M5Dr"e]qli:sNPghu35>tagG7Oo'oY%CNC3K@eD*t\1TjPV*h3t%Yo4JsO@C4<%CmZ@bdD4mJ<<[>O93f(n&N)^DmUOa?FR<LP[82&0WgoU
l'A1e./r]/+I`46K*+.UsZ"7ns+D>d*364G2\>0EgkSiKd']GJM0\XMsIio\kqEP`2@1,VAhTUDQZiD@EQq:o_h@_o"+S#oqn3+'-j_&VD.CRg3+Vu\h
_tL].TF#pj@q]kPUS0ar%5rf+[:ITAB:nTBE)?\4c_"tWIeC)SatWs,9`D1=25@iG3PX]EMP*>0PYJ%8>aZ:,dPH*?!d3EEID%pTC04o7EO,L_AV:hgj
NN>X=OV"V%%:\dj`Uc=D]_L)4teBDcrNTp^ZO#T'p9gG\frRmD.`KI_:b:\=^Di3Qon)@/;Y(3<NhBdmqC]J6S$&uqK3\pqgPh3!95dQYL[0H/b/%B(O
)t69WF<j:bVnu4tQ!sHCR.GVReYu"L;62[r.b7-)Hoo%Js*>riCS&kH7WX`1r<<qkGcA*UGg@E;76!'U-m\]92,]nkrZP#ip,VWLn7g&jFFSM18gt&3$
^?FFS[jM>QapShr&HjOJY&URce4$Eof(pPZl03RGK<]@uPC9/Yd`i:f?@*s$*o1]BCg!I7J:gn$=o-aQB$R2EOZ]&[;f$k]PY*ZhRO2<B-:E!aP@8rH#
a]8;`u`b5,#NCPmY[sa).HaYuA+.5BAY58+!Q&V&Y&mnM1muP\2*=/c)3GrpC+V[[4&Xkl^%Bo:jl1+PNA&$jE%*D9a7jd90>2H,'FM:>67-VJ_Y3hnZ
S@pURM#k;eIJS3)lsTWsR/gd'=FbBdJV:OEPAlHVS<'/+^h\nNoh'LhgV?)eo4&[UYB,3D:Aqn;iY\ls1Tq:@>&1*kpLTN*4@qdABcn];\mm=nMTNiI@
N-]a]F$hS-ff7!f.eiONGTTb2BqM5@o8O/BYeSh-q^jY)hjJ[-'t)'[u.;SV8iK@#JaF\!I4d5AHFta#)0Nk)TH9^rZ9Q0JP7B.)LR(,/R1B6dR7+m(g
RkQW:*X3")<0[$UXnbca_hV#K%W%;&GprQ)mU`kT67)H#K+^1HaG8dM/YnLUSDH:b936V*BLd;HtKjk7dQNNubgIa/qf`.XZSd\^XB_!DYlgjLt5e%mt
rl.2u7C.QPg_D^hLqjI`\T[NXEf2jrQfZP"GIWoUk7l/-1&N_[n%]*P[,R:mmtLD>QG<WZ2/$?oH7fe%9b^EQiG5S.0aKIXf*?%Q<,(@M6%co$bW<mq5
lrW'j:rRt14Yl?ckmfR7?Ou[D.6;$SqrT!QA(F9UNqVQT7dEAW&gYDSCq&TdfpHi#qk,fZ?c_'Qs:qY`8-qIY0p[A,X&?D8u;8osNWD1J9Tf^d;Hon2t
p@!b6M!2\3WMnVtgcS"`15!)=NO9FW%#X6j!7iKm4nJj9Bat&Ac(Zd+;kE@_?/i!Jat:63<3;\m-NI&tV3\[,+f&5j8kpj6Tp/%+mZCf8`)s*S#jGf,b
ocopEL.!&^sH*ZaZj'I0(<fa@MjagN&s5Y`+EKaO]'p*p'8_r-(7n7:IML8MV*E8@1Yg_6C.%`*F@KVW%0Xg-9kjJ/F_*F7[0.\c.B6@i_M_ab5+\nW]
P;<qTO"IIqD6P*Y^NG40==c7Wl-KUG9%O\n@hUQ78Y5hb&#Ul&8i/N#>Cde8bPY=Vs8K![$MN%Ho33L&P=df([<OnlJ.Oa`em(>V87%k!=!`r-gr<%5-
bCMe]c)OWt#[<Zd(+7d='iZ8%u7Xl)XtRa0C4C%:T$iml1m5S'"c#SIH][bQlB,pU4OAmtRXkE!-'X%d*_5Zp1JpoZV1/:HVN5-HG)HE:hmp(R><*2\C
WS<*rrIU]jt[Aa6K=?MTNknAbA4\Q<qj^<<65S$I=j<D40>E3m26:ogHk;0c`+1W=c;2FI)Lc2k[(f(pWe^OD7duKL!9o(S$TViS,OEZXeL3Wti5EEk-
+l8U\HZ>.9YjZ-maD=do/fMI\]Tk,#b7C043n4.>@Ee`A2W?E=:=?$sH-UF_-,8/@<Q`1:'^)GThG-hF]m15`dB?>bYFXg^^Kt@s6DH;gLsON--Vm(22
MZ-%ZPtp/T_tKF]JC=?".EqJ5M*8;/_giWd6Oso-1XjQH9u0g!WI`Bi$c,JPX1"?HNQ?Ri<YY&i/-UL2>cl;CpJ/""knT@$Gi(G=u^1&PUl`2mka@KU8
_^!s)F*:)O/c=ZoLasQ^(Lbn[\-p6+.h"=&:(EaOT5n?CP;1"`E;.m.[(@Opk+:jRSRq#N>#@8415nbPcprXSQDbO!c.#C$O,''i?T<eoY8rfO1037%n
+Km97:>RJRlt)1L`:+"UMLK_Q`lgr:Quo?2rOj4[7mj+fQ8o?YUmT_T]k&5WZA3:%&oN9aF%9&klIHs&7f&e]<cee"\(-E=_;NkTUG!;cS1-9@&PHtX.
QI6IHCH4n:l<T/cC8M6ZkA2M&\)rBctn$@1?m%h<.$X\[']lJ+-2CG0Oa^4\NRNQ;[prTA%@g6SZ@leq3/nce@)^TeZ)J,F#&#S1Kk'Kusc@Qgq:>Qma
K_BeG!+WrhWsE/R!FslE<nhm7J/fLKgsYu7l>R$HdI*nU;`@#Nb^IcVg[j#mgrAp0I?jl:<*`t4m`n,-ND>ZL,ZCJpgbhPo+0VaXr"'uLfXWE4jg+WK!
h&R/3jdX'/CN*=-g'<1:piMWbn\\lF]V[]+7q;je0Jl!^uebW>Sd.1o.`rM%G9HqddcNbUCHcKXKlleR-j2ljJpk)US?M+4&/a:dkZsf<.\ge1h"!qJ*
9@+*O]U=NmIW../,+/0s]CD.Z96V$Is1Qqk5B[=DhLJ"n$a/rl!&I%29\oAKTN.`+PioEMNM3cEL5`FJFhNN;j&/`*BYR^NT`\N,?^QY@g0*gn0@[E5^
D4"oLh*k8'H'(U4D-7k"NcItMZ'\<92JG>/83FfM(L/XI0(PpF(`(i+"A3/r,K.\8f[au3g$LbZMCjHQ/9s(?RgG_Coi^!T6VmBoqfeCko$O`(II6_h'
m"-5V/`eN:if_?ft_),5*Dgf`s*[+LcN^jS><'ZL2`n:.t:lP.m)<Qk0JoKDh)&9L7(W+AQdhJ>qJ[&l?*P'/tM=_rF$YHJeD+`3CZ8_$TfN'Z+=2I?M
')li)6/40&Y&'+J?tO@IB+_>pHmI,k>.O822E^Vm_0ocj,X0:T&1Y8YOhu]>+tF^=#m0o`60o/gC&lO8c#)icg%>UP_a9\/4fqV^A:np-a:P'*5FIN`B
1;??Q3PK])b9P\j@SrJdP*eT@YGr(6+j12-DD6h-T/5F9QW7J_[d$lh@Q:h<da5-02r$N5"`us2f-fQ_)Kr__`]=D)X_n2%&^4Tdo9e5,frob`I>6=+@
E>](l?M)&JLk7O3dV/QD9EG=V("MPk8o`ON&="2_llt[2ZE?lNut>n=+HGM//Tp%45R@&J@D`!$(nEK\R3G&*Dm@#^T]LRbM01DX4`$$&Lum&R2u(`'m
[&r6%$,ii@DueN?1gd&00^Ea0HoH>bEh6ZkZuN7L;)\pb#0#j5&kh+i"<ChAgA=kp\jRR'`6bUdB=-g>UV9H49"Ks>q>5)Z&-:Bi0LNsXlZE]l>Mf]j'
i`5bl?o=0fq1!-\NeJ%XLmo*ASQ#@kis"$K5D&04ejn$j?82K_;S7<TY2QW"DI;ONc@AP=qKh9nnRFe1ch!4k$"PZdbcl(f%lY-i!&2<"9RJ_nrJfsk0
[e8)2mEp7V77,.d:)t;)CDAL(@\ePH**X?[68"o(0i=B)l`nUnT$/g6hm)o]W1"aTX'&'d+]uE^<Ch>"X$qk:9k"(Q3^i0*HX)f-:,::j1LPdsg6$-3b
i`UmgI<5L2$jVjhO`e:])3!RG7[QfZE"T#W#,C1OFpoGG85GmMk2i(qt%_k\NBYE,%gSFM8j!BM%_0FJs&sp6'=db!)t"BT&>CbTC0rEQbcIEaF)nm6.
9ltN4jm,#I$T=@$k86HB+KM1i;7PM55"r7;G:/6!M.`kI@jB"pjF.:(4\%o(A&EZ^RSQF'*;c'Ja]9j`bmt$WMdjL;QX4KCWZfW3Lm;/f[TuG\`HV>2\
/d=]6Oeb.(04^o9L]<>j?XWA]pu+Z8NjJAM-7b5k+\V'.QZQqNQJ4,mNaDrsRGHIGfn$3kF,Sb=QQ$q0M0X=]TF\i4X_DUfeP$/-%*3]+AXSg/39gc'm
!&V9\d5UA%nki:^5_VNjCm]3e+_CNgQ,RLYPNOYol^Pg'-#K\fXnD`4.H\`!`G]G,,6KA'g]kR25r-t$f8E7oXBW4N`;j2\Kfs6970j8Cr]H[BOCcP4J
ETWV:i`>$OW7a;\f.qV'adXlLg1;"cdhjbN@o\\E8X%:HrB&^-c;m$?'WfJ3-pF5].'W^Li/]9r-&=!t2Za3(qLO+DDs*WMjFbXa+$R4p'/Ut!ZrrVc6
tUZ,0P32>@"0\C(jbF\GR!(>,7I1HYPeU;3FKlKg'4#@Y!n='d]QXdRfW\.rF?D%NF^?f2_XUa]K"uXk$#3,SUYTM_L$-;EBNgm4iR""\euV+Z=)tXDP
c3XOu&Cs1kU0nZ9F(4*U<QTAVDh3@gSLpSB'Upo4Fmq@$M[RjdQ9UFkj(Ri+G+ZRX(]GR"Fa@l1^S;N9F_SX;+4k2A-2aKW\fGBjG>98O57a/)=uTFn/
4##@K"EpCbMFE!O__b:ntP66aAd^Q.ojN!4(KL(OJf$$/aoS"eK4U26uV2N(nha9C&Sg7EUrc/PJ"(HPq=em*$<Dk18[C3Ljje2TaN9V!"MWd<K5RI%Q
jU)<aGObBrM[1LtNI7;XC*K4WFZTf'pfs7Q;>l8"A"X/t(a?TE6&8&Q1I%7Z:?KIh&ak:8<bAXV#.4,Rhofa_?VYiUe<]\a*n1T[340;IlpVoZULS8:H
A)p+E'i9HT#t6*j.pFX%5]Q3qDu^@&K0-lHdDQ<tS\nj=.OXd*,pi^8ri1j>ShF+t!sI,bo$<E\TJ:3!UBVg1hY^JIV^O9tcSg4WTPsp!B+BRg"!Ke&S
/;4rI=1p!hs(bs=9q872\:X`99rG0P&!,Z_R)Dt,Af)aRoE1r=EcUG<sWc.?mVW4)Vp#[<g?H[USKEr19.b]D$Elbb0j_]C?'g-DY-oBd`C%[X;^u1l)
.Ime;Wcg(r2I=gtrA(,ac9ZLVQ@Da+L1eEC":Y.I4IkJPlU'%:08_q6prL0sU^7,8;?]nOP(t"cb23[dUGKAh:@I*JW/F541H]O&qMkK,6'T`j%<+TCX
E>o;+b*dLZcQ+)MVue#;C$.<cna(d/;ON)]'is5l8/lrBR2>XPC1j3O._1a\B%.f9]IQ''\^E]sBr#pDiJJ#!M'Sn@!K>\g0*!@-f%eDoKYGQM,k'Kh'
q',f%&4H;G#nlV'>j_P^g.044;=oC)ipi#9FOCXB=WT3hDhufWLR.Q1n^h[BKO:jd;Z(=BoL%uS<)i/U%Lm]'D:K)2'2'2!rl0tg`6hV:[/pV!1R@^)$
KALm5I"73Go4`RDE)=8]7s;YCb"T0fjX_!8!gQ]%C#<>>YFB':m\(+G(cS>2P3g:oZi9r7qe1:\HGTaI[oQ36X4HAVZ_WpK,gm2j!9a64kjlta]FMfbi
JmFeW^8H9H&4s'>IVh#@'Pf7B8G6!MBF4km!rmE1g7A/n5'NlLf^XCM*CI5E1M5/&7jh/3=lNDb>ZN\\E/>/?217h5ANQ#&MA_4(!J!"db;BH%Zh(a/B
Ms#H_c^MV#g']p2530W(=W%3)B<Fm0th,%`YajqWq'k)n_F*K$Ga0K'('sMGjZ]'iJ>)1%]3_Q_a+F9XK^:_qJ:4M2b`J':bsk>cA2e'e7;B/)+D[MB0
XkO&=XCn24Zu-+GJP(8:XlZh*u>OaUFO-sg/INdt,C[T3Fg748+/P+-5t8W9%@P9+HZk29&e_ES/X5V.n\P.0l`R6/IEYg*trIV[i7l5u$n&9R:RqPTJ
`UBDJ_nsC9RiiZaO?u_A3bF_W<&X0Z\le.bQ[^RE"=joC2\iW'sE'(<_?\`#HAfUL\Ce>`?(eg$IbN^b*9(i!%.>u#KX*ks+g33J3j4*^rlnQ5"#/9BP
pP]D_@=G769-dm&!,5dB+BieubR$f.Hl;aY:^O&C3otGpGon[.0qOA>GdFtI4b9/G<@X.-<SmE0-HCkdF<Y\_[(e,iapLVcTr<6LE\F:!E]<7$9IX`XX
Z2AR"T'?h7(dVtVIB0(-$540p#d+KgS$/V*l;<$n3#kaU(+:$Qt>T%;$`D]k2W*D;6POH5I&3IW2+P[e@5`QQ>.m[#3/O"^H9T@E1Fq5g7LJCi-4SB6g
NP'6L9B3W-["2?K!i"F"gGC$aR5SJEj:+NFr!aEkp>E.[ctufFF$L58%D]/SKu&O1UXIT/,t+67N%GbF52DfA@qdON+:9I344:YbNe&\bN+%],uf[Y(o
_eH!ii4foH0Vm@:XH"(Rmd[8^n\A<%YmeTMC]U&>H6#RtnjSBV25_s9<bJkn738hl%S8Bs"D#Uk\Fi@X]NKR^+@imACIqogd"cC!No7e]-8'sZs3Q&#&
)>>+gOKP!ii[\0j^>upU%(/f/]`04n_C(8.9[M!)6]kXRMYm;N6d!Af*,kDg4F8B9'+^MP>:Ze2k6h(8ab1gqd?^P^8<&A[9&tG[DH8__j0$XJ56smVO
\g=Kra7K@D\4B*"++K>eR5PX[GPT;GR'MU^q1+Q<?*"8&c2\C5CcVZs&fYS7[l,t+HtX4TK4JuU,R's:c4bSZ6N,-l2(V.'V?RC_VMd!p:aWE.,sGQeL
j"#gc$PDfpPW]!"l(n<<C=W?+gVl\/t<GR*'WFb0):p_Pm$T[8!T>0dI'G)g6,SLQbdQJP).mgj@C0t!;9*&Q9Ti>]^mjm,eY?udp8RYYPl:CpC9N)3=
;/bSG%.F*+.1:5aAKa#Ab9\[njRrjjHk%[Rh-OSud/r8!C/X5$8u;YHJ.ionB>791\pqlh"W>165..&Dg<4A"#=7n=WgtfFb=97Cms0BJ0*ng`p^G(GX
B466H9SZ17i=q-fXB70s"<KRP7MPG&505&lOXHG+_(WY-<\'Sq'U<MB)))X[!0kpcY+XZIojE=3MB+HdAgiYLluQH./igOoHH4Hb(a"p)NXIu&b_>b>M
n('b6T&74ZE11PSc0I+U[*D:>JlYkd]YI9>Pj9BU7!7:4]mi_@8/*aZF5Y#MuO_SVWVM+c3,05QS^!]H&2T6dI9nirqT4Ju*Y3`f<oTi&=8&_"HQ^>eC
4.qf7NK7Xbqp-P,<%8h+#0H@X@MI;BH@+rZeb^6%!_K"/VatF24:k9l4P'YZYAa1o._ai7];*bl\GFUF1U1V:;)>(2IVUEu,Rco2:*#=2rJg97`o"^mE
."na#!^NUUIc=qMI7So5DV?6%^gO;R(Jq2q)0;,,I`Z^f-]oIf5@lYrTdP\'UdNhO3UTJK%eI!Ou*fR+:7.r&9!>u8\Xaa.m:^?N'.+r4N\!A>dDS%Fd
`*naQID"#RsS]o;h.d4^a@:IUl7"/LL)V9phae:&32C^=\$8L>gAjqo>XbP(NY6E'q?IR1aJ$Z:Q8EYo)%-?$?q-7":B(2Z"!AYVdF(JT^Ee*gn+K7&E
jt4.:sR21;![$&]j,nJi_kGX.YPBA7UBn-FnkW#l--5,B$66m!lbYj]2S%,bNG;2jrW1TRIo#i,XHK;Ytj0j7Z'J8L+L.^8PO5NX7FQ%(B$O^.tl4o:"
3"YCqAimCe-Al9"OO9F=maMsbA]-"0/$Q\Slaj3]EG[$`$2P(i88=ja9b+Ej)$&n7J*j1d6IJ20[#[U,gC!j*hkp7<]T.9Z5fN0f'YQc6S<F8(QAf%kB
rk;V[;p<Y8lO4N=(3]stT^([n1LnCH'[!)J"tnS]Xr>sX.;%j7O9F9Q?--thJ=6")8^[`n0j":"l5"M0XrNoF=W.,#i#d9kDYQHC`5"FC+Sf0)GE)^i1
"8iXdZ).9O\3'%qY/]-2W]FTH?)8^]m!orJ:qF%0ccBjp`,msI-PqRE,f>FP<.'MS<W8'#.[9@]bsgM:NXg6,etA/(f=)%)nsPGVN`*H`UU7HMA3_`fM
m^_XjY9HOk,8?o\h*@4-aN]0hP(Vii_9Z5n7_[R:';OcJt_Ak)<fI+(95LOHkOC@0meIeCZ(XHmCD?P(FeUj$o?l.(DV!Z"TlNkQhcd(4OMb_=\9/[uC
4*@4(kG6tC9,l]n$"Q#)=\:-Y:-Ke-()[\PF"=c@X"i7l%i"75]a37n\g3-c3*&'VOLYk\qp5KSrI4L%gf36[[-kbP8:j_r:i6)8QeVVdNYpplkT+g)I
kDO6ahe\cBrHWip0FqdrB'`<n?kgrS-FMaBlDJ>29SPDj^[+5Oga74?aYt-Q4ec+jDr@h=aiVgL6P&dM=WmQC+WE&,8J=,F.Ko_X*(Z_lB2*k,bk30N>
c_ksOAM4aVCFVZ`Xtq%A0Z>4tA;H_9pDqhETo+EpmR7a!PhJlt_m5f<n]YPH!N+r+;b'fk@.s9YjVABgYsmPn-Y[BILe3J/-d_A:4X">O25"H0##n7F4
Sc@c"jf#67q3Q6=Q9F$d#b^o98It]\a@&T(P4!)eWVdc3\ap3"&?T,78`1-+ODDI'L2Y6_*?4/a3+.J6S"5t5Sc@E>)kQ)\9"jXegDESEEk.&5W2^c;Y
le\Cb?sl0%4I%1`RmGXYl7IR](S9HZhj(0Skk!)n7b@OU^)TWR/2aA[-e$[@dY,-\GU/l?bd>T:+3/DcMYa'!PE%7K>?Cb2c;c>!5nagRhKU_(Khj\_b
`%!XSJJ\"\;OZh78U-Gj_GEDLD3=*$gFenqXqNobpBdB(BLBe02T$phaEY4:iGE1?]\!g.rUVUGD,8>7ld[7bW--(qIkjL]Y/pUErr?FTdgmDQa^PeCE
_=*bdmOCH'%dt?iAj.r@`)[%F.ZYKGOZe>D6qV*>IeR1CP9'"j@?9JI:ejtTQ0km:NZ3JjN9s,`lodf,,PP8F@ilI`03tRM%Ym<M#;SmW8pWK.`?AAni
FS4cp4)+mN@9uT'<sge;!ga:QP,H$;RFkDREt7cW3g<[\VY\EM^(t7SKqprp]1JtU6=$#bV!Vo^LBf+.)$&N!i;bI\^3D=1?j@FT8?)FS?<bh)d"Nto@
l(h+,]5s"*lSIpJTl/F5iNL/%h#P#7\qJ&VWZEdA6A_Eq[8r\p9i#NE#8b,/k=,bhc$9\XJ0n#45[oHjCQ'3?Z<.-ER.1g&/#@mI)DF-!cep4;Q*#$S5
A[6,X48e!G/><iFl;TK]Hua.gTuuBF.*9baDtRX5thm8RR^2_@UI<]c#-Ukfa0;5Ok+=#kY:XEmP;XU6oR9;a=6Wg`5sNpq#0>!7:>6/AF5B*ONpSFo-
J%;[^r8[goTL62.sQQ2o,eRrbcm:G!N;j$dO]n^B7na6Hj$BCka@m0s(ZO_isG3qX)$KhO<EELmdJNLb)qX?pu.WB"?;ipT[ko8jK:jcu,.2nBst93#R
.mk*"#dRk+3Lsl.0HIII![Rg8p0T@?CG,bUrOr38#b7HpsUlJgc9$i'b9hMJb2Kik\k7@5Bh]^<"hnIEj+*4uJ-7MlN;D=e1CmM?1aiTbY\t:?(?KB:j
epf6"D[hl-Lt0H)l<<Zs%frJ:s6oN)`?ET+\1gSkAEG;reIua]W@uoQJulj0AF6)./u;H+R[$07Ekm==(oJ<+3;oq&pK>oB/o$-DO.!SIf>W>g03n7sP
Z)hU5W;]\ng>D"<>gu*`)g4U,a4^?WPCPLNpVQ.P/$1_Z\K[jWhL9TfE0P3'*_Ifrk7q:N[JK3YqRQpKUspY<";C",&N2Tg?oS:gbs\HBFQd<'/]S=Gf
r\$"PMFi[,nOnjdFl5(2D:-!<ojHf2McTCNqb-2J$@.25j3,YlB2VFWfi$dW3)rM(.TGUb6.9EA!Ke@5R"od6RM6gb-SQ4p2;Jf%;T'bh:d6K%">[X^Q
cD$hd4'U8:;-;kF^X"ikRB;KI"TT\5!BFO-qUR+`3TS,$<l9m]mpX)YKin:aqO#?Jd:A23C*M.*E+2C6b:E<7<4*OPL5<*(EK4ARM)4J19$5Lm16g@Oc
'kFfKT]!V'.bm:`hpHs10IrG0*HpF,$\(3.9AWD?!23o&D2VTMf;dZGnMhs7[eBt?/&g4-QkiB')TT14-qo!?^pJK+Hdq6rVGH-L^14INM4B9o]!n$Lu
9\(+[/?XA9C8Na,%OX;+rnLLVqe?P\3ubGLa6:`0d5'+DJh3H,C#?0\JZur__#r!@$0a=^:3YX+)94.%3#7_32@_HObWHp-'ke^ubYuS2o5>^WaQtk@>
`YON1+:s75/TF+!Xo)"(\PUVkOFK^`^r7PZl&rYUDM80HXR/"@bQ1e_R]:/Q*4akD1RZ+i`NOgEdHfs)"IJ1&6EM]_@:Ljeq02Qj<ASo7_57tj[-eB<[
7(ZP\'(.H<8HEPh(DVeg'm>![)e&$C@?e^HFYWp&.J0<;^(lcpd^=Q1YVF0tS5=o>+"4oOcf'+`^:8c/Rs])cH=t2q3R,/V^oS.JP2V&UN!P5<j6j_;H
Y&98>VD,&ZUOiu"urLKE5HG??PA[:i%"'.4>sNcb-+\('aOfX3Lq.,os8qTd\%4hh)oeJ)WMq%IN54:'mDs4?qgh5b!;7pA^eBOeo,-s.*CD33,1cdUo
+]Mj2ufGgrt'>t6>a$C$Oc>J=8(35qK,$7?/"Fk].P)6!b@Jh6P9i3W.o>'3`:,6YL5h#>.-4K<KSliaSdKo/B\@F>amtjpKLZ`@?qop7-N$k=Ib24G\
&%4*D$W+s9IhI4>+*i9CNjbTp5%2Tmnl3@MG8DBHE5OXnB%$Zk]cr'(q;/CdeQ6-(aB1;b10-4gg$)8:gqA%QUUl=sKc(*@h1Y8;01:Qp?oE,KV3u7?e
HZ$nY:9Qnc7tUY92rT$o4ik/f,gNY9kYb\Z9OMd1^:XEk;5$5Z^1UA1Vue'nn=At61>XEcpKi!7&*]W5hX4(-E5Qd3<WA[)!p-Ol[]KZp$q)42gF<@"A
Onero2^-7kdgCN:-VS3'$He-`^91KMJu0?>+Rd%n@Xm'NP)piA=p"#CsOh5rDuWcT?YYI=8&Xm?;nlht%o8)tbB>F2_Q>#Sln-=XnlkX@"eVM2b^1VWh
-KkE=I\7&M-e$R%9KmF`*!X/8<ZYJ'tVqZOY/..E/f\c68]D_mYWHU8fZ'FkUDgt&55iJh_c_!\e0+?=P8TZGZl37K7M^oLkhdUQW7ec\Mtk7$))o]_]
..R4O1Du`)Z8N6EfB8,NHWFdr9jU&<Wp&=HI??lIl?384eC*,5m[g>$nIKooCp[D7W>a?r$?._bI2QIKl+kko@%'d48>qIRiXfB`nPelUi)1[oVCCm*[
^##O4Kh%*/N(83sW`/o%(dsf20HUIA_NYbb?,NlRUjiLF.BWUR!MODSH.=:n^&LdPooZJ<:<QKu)*5Kue4*-j4p/fgA6ChM](o-33]kn6hq(d&9Q4LYP
jlhXr]n,PBd8unC<QYa=Y\r!]6$*X..02N`)o#ir4(Di9s+p?Hsc9^L&M#ohT1f]T1kTF2!A/*RoeR09KfsGs1%Gf'B\ORj-btJKhTWo:juMLc-+I)#q
tnd,luE!SVKkebf!ObjdjSk?-]felP*a\J^D#J&Lpnl%-@=iec2Bt-3rEaC`:fe\a,\E;kcLL.s<jUL"9cn#J>[*>$ip!&U2VUb.lTj3!WolBTAI3;-i
qE,1i:R(PRniL2[7m!F2sC`?2;Z:O=]AS>u:jB;FqeR@#WOKNS$PQE.m!@<SI#T3(aAP1@FZa*&q2NW9kI\m)q6O7[3?pR\)+=H^l8[8u\u7-SDMn?;f
Np4guPT=%Lt7+6u^I185<Z%]c6Kdr2j,,$a5G\]uu],(r;?iWsOaoi25*r^'!%/(QPFAIA$Eb]&n[opsf_H#r=j%eJ^HVVG>k_aq=iChF4BSjd01&:<B
*aFDkS&I.^nT_^7&(G*](1Zceh708?=h/]MV@lel6=%L>kK1b%/1,]_l"boo6:6>!ZUFp;:G,68S7&`sN;Qn85%U%&OTiYOC^ne:VILE?G=Ab-]uo9LF
b;+Z;)M<_\?+mWXr;g6eRT(27PQ+2D]`&]5Y^8Xp8=A)eM_(/%A)j?5F]c\>\Z>4R!;Ft.r8N6mIAsYF$]kpn$oPA0'bKV7)oJC0h59;TsDm4oB=3GQe
R*>Ynr*ceuE,gIFu?hL0'>W$*VYf`=^Pl.!E$$qC<,Fi5]Ne0kMFJ0.43P+)c0)61A.`Q%o'5cM!;'K*p[;ZA2*@plFumQmY8*;eAq`CDu%;SkYmWCQC
sq[rbTPnC"&tHGh)neR*a_1u.:!V?"nN8T/98o%'kN1LXQt`U:of<9S7=BA0sSk\/^S/@qTV%@Z3u*SHf$]f:E9r.U.QK3XS(Z[X/cq#!!i!!09X[,l-
7VJ<RqnTC#B$E9!*p#^G?=2<]Ii<L7;5g(O#^*>QqKu:"U@'![,`lMd;SF1][!#KWZ/#F)sLVd,0fF_.J5oPO*_noJqFsZ&hj+jdAYU?DLDTF)h@7uS1
JJtW>q3U2r@Vt%0FT(RP3gr-#f[[+0%'&8-aS,g(VLoGe_6nBfUTdig#'LL'9#hT(6L:d5'lG:K,fl'Up:0ODlsP1^9DoZ]\9`PmndshoQ+)G46H!b:Z
D,'J'$#iB43r7TpTI.^*=j![=BMB-Iqht]*8d*Rg\rnTb('.5gT(-U9'SoMFPp7'=@t$g]aR=t&sqGVnS/4),A-?g58%fB^>M>uN*7rmJn8b6qfTm+Ll
/BB!o_1T:Rg%:G,b1GD/&f+1)32fS1$lC+5V\[)@DGF+KGg+m!/FG1jud[9R7uJaWr[lZQS\5o-EA*:<BZ"/6XDbQ&]9gF;L)1=+a*IAX2a-\P=5`L7)
MU&W0;E@0X&M18TLFrEMi-!b!i79[*U__$.IsD[-@fBe`l=+Ll$\,Y][O?m]hHX#@aK#G[tYn7n$>V'l9>FlqkPhWSf5m:!%&qA#D";bbOT*a<Zpj/Vi
b@;l*L?7s(B1+2B",Vb'@98f"\[KS[dm*;/F$]MknLiN%t14e[Q3E`XG4/]<s"E-UuXI-D+ZO=rbQGApaoWsAF2AP57;AHSb[Vfr\Q6\DYbA81@#.fKl
^%%V5jE^?H(B!5f#$nG8?A=8.2DpJUK(g0O5"Z:nW>Ogn5'u@gO29@C,brXj&>+!>ros%H"R[j(;3h.u57FWIDGKEk(O#Pk,g&9IIaIF]15hi@8[)eO$
GY2uiXmQm)oc@!-pm,f)2l"pNEfhhQo<09"[,D?FoYk(pL<(l5QN/1*?:_q=kR5ua&!lfHCCE$.uhH+*S_p1M2I@=ZM"'(C)hhI@=aAZERYI(-T:(C-$
H2"RA1E7f:`g.i<gZ5"65^T<hAQYh/(\$$^%d@P5%m#0Gg&,po)%Tj'9S(GVj<NLDC&%%.N!0%4iT9oV^,1(7"2TTK'Jan>AJN!*3<];)NS%g13fs`"\
CV+ZZe'S:Qtp*_!(K:ER8cpn"1gp1D5/e+@CrHWZ]EZ>QSX#b-pl<uP(PBj%-hS@SthZpOeD[_s\mf?UrW5:mrnNL;cq/?fZENGc[O!W"A3-;W//=r:u
V/V^+N%\"=p1-#J@hq3u":/I^0H8/k?/5_dtHWlF$atiligcH=Eb>G/N.5("fS5F/`8DHdPd[Bcg<\IoQ+X`gRYi(e(_ei%'s6Zu0kJb'P=-DE/Sp\+"
@cqr8r'Tg^d'EiTF6Nt5d%;=uX?!-_a]Q;3+!tNlW!/POXaUlE/k21C!Y3i=XrV-g=AIH*GFgH2/?;h'L2b8^)Y\OM^kc):8Bo0TmLL,9,ZVj^EZ1R85
,nu/W]qcJ3_cd?o9mf*96k9aJ5pN"$5Va2,tLU#3bc@[UA1h)m-0\ioQb@"@AP'\I[H12RAE!,3!3p[TT/XQ1qaHbHtIU7oe3B^3GOJm8.<n.k&*oC%?
"7jRKmtlB&M"'3A:+[L,Z6ph(Q\3jg4'(8Z[]tdsm2+mG;VrXF5M>$5GtQhTp-Vd;fBO7h(A4n<XL4L25=l`#rI/+Pl>Sd*BjYQSHK9\rZt^EXg@2WlQ
P(ZK(mE_A9:#M4[>q,]c$2a.L2jMZQ7aj_Fee,^FoB;oM>X*-ioPPec6]"GrN!K6&J0PQaKL=7]#,iHZ\Mo;(I__e^lOkbe-`Wj"dT.ISC7]6tJt@P,S
7Qp7]<Fel3#G:8QJ75%pU^a'$U'RL3g;bmSJM:""1j,K3m;O7,on4hOk0]Mp#)UYT-6[E4Gf$r,s,?(N41pF`r,e,4T):9Ph6RS!99P;=8/r)OPHT%BK
L[Wk*2YHhHX-l'(1M^>:Ml&tns3u&$n572[G3l4JTp"5]&`uNui8(r`j3O7M5(dbnZ_HYDkC9L>li6;&H\<3pO'l9X#Ki;%'H!eXUdDsep9bR=oBd0Id
chXKfW<?gAl@)JLdo6Q"W@k\9]SeSaW:28CUrC2$F`HO`%,MI#h6$c>;CNfY3t(m3Esk9ZYqA,Q6CO*#.@'GKVmP<C]$%qd55J/rdCL2bhJ%+;WRW(kJ
Iojcs$LF^4g`W?+`UsQV'202D2,2E_A6tfb53S%ph7F>3'iTQ8I\VcaH\]i:,R(OPB=QQ"XSL:b"+S?1\3R.A$i^lP=N#f@]H\Bsh2"3UVs=oB4j?)e0
%:8])@SD('b'`Ys`X0YOQ5D:_!ffDbtCd+dP4a:Gb(PlEsnB^msI;./@&ai&i=f.=N"H)ooZ0K1K"XDP\OilBSm`Gnq+WMg-k>([:QIaE-ecK2!rTT,d
'=5]'reS`W5?M7RA<7#(0f^UTFdsTO(:J)sq':q%J4'6.Q419o#;pVG#9@r)L>89bII!@<Y0d3iEhEePW7u.1sE#YaUmu%QkhR:5G_C0<a`rX&:dE"4E
kH/$.QjI)7*NDiJDl8834M';MqKe9=Jrdb0)'Zu=`/lN]9gWJoN!Cbf0XdK:QX9Xc?H^`kp^Z;`%3A@@%!f4(=1iXQA(:US.ATiQHA1pLY6'(&h,36u6
Qd0V`h-],$Kn3g&p^GmHeq$pmS>1bH.8#i>Sq5[Tb#kud'MXpeYsUTfMn333\e1&?3E=c$A_X!GS?Y]D#j.;faM3J7)Ma3.6NVVAWN/4&*VFQ[b.j_O`
5j,?3AXO:Q0q[;RC?GnZ>CBca0')R6&=OG^QXXi=GM:7)H-S(;rej8(XKq:gU\\1goTP.VME#nhPB.[7?/]p/0R\,a_>".aR-';1$ph"/-0N\X+dqnV-
p`2@09H3';i+$!.PjmrFOM"*sZM+gEhn+=FVqQ^'O_(*ZM2b%``W@f5bYP%IlVBt42`n.7m18NjSA%pI6KP$t+B_,1Le3LI-M^<0*G(HF#1RlYVr"W^b
];b:[dM8R^]L4m%^O?C4KGeU;fIuWd?rZk9*-ooRo'%^E>3.+N3Y05_$V[%JQSocm`.$;_CEp)Tr*Ls9P*g=i)7FHfqB/Vfr`t)<:(5U"MOukR1NW**:
Bi6[miAo[KQq$2[a9<0/j]iK0fQ#$1R'<Lgm/Z=C?R/uN:oR@fH"e7B#t6R?^87"4)u/aU^k$MAAiOo<N+NY2`d7!CkN6SM@Kk*WMI&;tN,_%!g8[=Tp
G$Zd5a(io)0lFG-f=*e`d4qc?'$MRgG^>L.lkl4\ll45g<NgD^*e\:H=C5XEU&7QkPtS_71g1Ubs.-K!!1DXV<J$]bF0m7Z,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.34'
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

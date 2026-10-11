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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 51):
		raise ImportError('multiCMD too old')
except (ImportError, AttributeError, ValueError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE$ig8-O-i5'i+r01HsH^aLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)d^;Cl"iF+?;5$GY\@0&f>,"jBk/
YiH%6+MO0G/&_cVMbEIV%te4SsUIN@I9"V,DPig_^G):A?gs:G4WIo4U9V(ca0E&!d7=Dp]k!,Ha*Kah\qE4^ZV8^P$l@o]F\b'NLI.UoSLB2-BsAPK<
TC+)/F=9lUh$$,-L0U,\B$Beq)E4d*p3?al3[\ThsBL1lSo.bKBCPcZ<_?NmrNo)ZLj0,OEjn[/cE:Vptg0[Cq7Wfn#8`N8iGq@':[%E_d<[n<Da,s![
V)Tt+8:H>-U",1)'J#^*$DjC3hYHqso>I7'F)4%WckpDf5TQ[U>Pk,]P^C%M?]kDI/O16EW_.512+,N&D1#T:M<Me?X8f!KNEY"U?8EDPpeDJ;-.&W;?
-326YM;Q9M/&S.GMTP2c@aHA+L.,7!!]lK=G"2A9$Mn#i)90BAG\g`*=3<p@:IY(m8,"V^d3PJT@K]W@?A\!W6kH"hmEp.8DK*R_ohW,n+I7QR*Sfb+L
S5(D&1#C.%&r%+^HcL(J5*YnF0MA+4SHl8QPl4V@UCUFk<QC'@&7UcN*cu]g&F@0od<6jU``WZ,a:MLcSb8BA(%3QN`>>H+DC$,5K+8TK7<BO`@;aZ*[
?6L7CjnGCER'7]CXE_\_"<1M:InKkKGE>AlM%"EQ5P_'Y,t[&FsU<a/WOBAb4mdU+&c"$n^gPqMbZN?PoQE'gc^fHX_(R#,:;:[WKZ%<P53`fY>X>%24
u4,L;!3R>]4+n:7,9,VpcVc8_qP0=RNh2o\J+1jDoXmGcRr2YE4QRW;i7m8kmseZsr-"N>-E^_rhp(WM)\dh[M+`mX;]sW!dtj6bQ"$]rTjs71\k6@ik
V'EX!9N?-j"Fa'NG#r8T-L9QP3mSDPMkp2BpSM4>U/:.(mHbA+H)IeP9a4lAQmNT,S>j+(U`+.%p]g[_gP<ol;a?brX'Uhf9"@l_OA@(>>DF$Qp)q5<J
L4L%tG>WsXg0hYG8ODMFCBedZHSjg'7/('>=6^F2t[dT*0@XGshE*Qb">Zn@MEqNEA,W)Jhq.=:\DFJ$5X.P(2c0oWAM)sCQX4a+ppLYRu*C$a?-`)"t
heej,p1^sE4khB@M%@6Ao`I\PF5E6X@Km;Q>J4%gQXdf8rVp>X@e]/E&?u,o@mq!8N=S*?/9=H2GO+)g5%?*oAkVp_ba3V$Wiqn2ck^*?Y`*W:,%tRoj
2T"P*^jp:Z2%S2ocM95+GuT9D^C5?)k<)m?cFn4Xha^NL;Ym(2^uH%2R8e?,@_K%X6QSO.Kg@N[3B8(Xe_?SDDk><B5..I2r.b$"K!Ei'[A20o"QDaOW
4W4fGRBSGM>M^CddKF#LT_$eYk?70p+rq)ems(WKCVmWG>VPoai[<?h@T#feB`?+WkMqh,E-oQ`Ir>fol>(qYcpedQ1[Ul:=%Yj`kpmB!]$^fZZ@J']<
;4&ujr7fOlB@R@P>pf8]k7I-,i8gml7j.sEb4T=F3H/s9E47sPPU\o/JT\huWtebQVX9HYmD-eA)-IX>?OY)TpW2JL+S]`qtMP%MNM#fAG8*SmZd`:*e
),dK9+bNAL.IEWbsbk&Qd*6)`['\Bgk5XMQje1oqh*2D\@!CXk8[!"/:<^F$.?"m<QVPQs+s)Zc$n6+;Zr3UBma$.`0@*^8/')/tS*[Z$tqC*pH0$;8S
^gi9el!6%oqNHejC;*U)7))l1cOXd38%'Tp+WN=WI9QV'1@S;d'Y`(]S"iQ\.H4OVgFrjo_l0L=8"oA0-5'@$#Tjk2j@?IG/?GQB]rtATb#F'^>S+,eU
>EG^$+?01'Ntu#D`fM_,6=KQ&j9d>GI:j]U':WMe$<t%9H6LoqMJ^c@pb/(`DomO5Q#f8o@Z+/G2i)HnC[b2ElL)(=Yk/m__&QOhK_iE*%<b[XfaqBI!
o9&^DQ.nhOgI9`Y6V`D$Q<AjOEg=>M=TP44pk8R%\&J)Pc&23"I=.(k8g9931T.4DUP4h\2pOCG#WZV4)FNq5KZ\n+[eB;r?mU`\c;6(l!IQFeCJmc__
@Qr(';0WIY:j;u#<UUh&':1Y%PI'K)TD-2$3`0o?G7!deqi>OO-?X`,g?4DUY,o5;@;a&*\)p,Nk4OYHLR?m)`e/nPqS`Nbu;Tpd^Y"jErD10E5V:H*n
en;qR3^UkjT&)HY7H@[oe0@)=dg./)Q4>=g9c(,OjS>>ImG&Db%3:11Noe3[g%8p4(j)1Fnh',L*UZMaV'%Ea)Pd'*Bl/#KTMb)2p%gI@cFpR5MEslcf
\!#^uO3@eXeI/]0!+8;mY[c/4`]@8&7sH5fZ-,H@!78MQ7sa`l#m+&bHrj=.5^0Sc_hnQ.X6<S)]sl"W(Ji/a0ro#DBMdSaE9Uis#b.i]ITCL5#`oR7)
sU>*Ft]Q*QW/8%?mHW?OrYce_pSi#'*bDO<j=rH>dCMf[RPUgOZU(`DDu^+5,gh0qQp^uYKI0p9c;`Onho*d\CpR2dn3S"4]7KPREE5a<J&o(E"lUh&a
Jq%chOD1I_6"j>QNkWQYfPc:mVl-Kj/]^;-^O$kp`?1$g.MNRO!O>]Y-V4EYn>!/Ij4%i43\[Nd/NK65B\]Q+p?/%_u($_mdP5\I#Il35S5Z.*i="60i
Kg]Z1mc5)6AD3EDR->j8)N[qe4=eM?9C]%4W\0p3E95it<&#`)sk#HoZEHJIh!LecRIf9McY+^)m5#fI:0GqifK=PX3TjX9!#Z\-3>b[LP!+?)gJ>D2?
fN`u@pW2T5T*7]#7+B:*nk7DL/E6&XO_Nq;P>#&Hd6hcB"UZ9PN)t=sX%ZB$YI,@WO?o\B<?TR6;TL>R$g+@cPGjQmr199QeK4Kg]fS\YN!]-Si(BJk\
GanO#;c73L.XZA`_G4jNIo@<D4NVl<7O@&]EB?t<l)QjJ+L&!:VJ*-+Fe!].,$u7WkD4s4qOK;_BnumShGbhd!lFSj1CYc;M<iZVe,o^q@B`77p]aA*6
_M'5+tK,!]?!/s=inj$qj!Fpftfq!Nq?QZ\7sMrj67Wfr=Q?1pFP[r<Q%+u1-3bs!W*/$jp)Ep#3.Q=q+gQCmh9S?7(hp4JbbmH[brq4&^RpU^mT]gi<
'3bkdnnUNhZ<L\jo>p9H@F$=K!j1-2OK?;cKeL)sZc9d,a9%IBI1)EVkQsqos4"X>bh0KZS>=@G@pCa;*u6,p"maoU41F`;j?a(o\GQC`H/pfQ/2g0a7
SWU-ogXZLb+e$D7ToI8R^D7B9hT;:6Z[I_.CYlgXl#&@@t9Vr't)(7s13-'6ieK8CJDJ;LuWe`0cs,kp(n"&"pf=R0'q?pm&lbiRfu:$q=if#/YR0`?H
]F7!;R@n>QAmFCopc3/6ES6CR(PYfM"I4VdVP@I.P7m"@_-O?qkCXM^p(dm#7h&H1J<f8l7a0fabMSfWd_T[uBYB0St_#!)KY;N<N,Kd03a?87=.guQG
1TM6!9HN;u]0>F:]\%oH2082]@!k$ERMbu!Z&9bPF!H]Q8T(0G,sfi,.ORL66:"N-'CWYV$7+o=A+/'M1I-'XE9g0P\poHKSc.-0F0""Mphb7a0j9O>T
G=_,67d-Q"cGed2cnq%/uS7,iT2C^DJWCL&<9D&D.63ph.LMh/MKo)<1J_;T,/$sYGIFu7RrnIA&f5%*iR[iRops8>+IdJ&Wk);J"S2;fd`+_DJDWUg(
p3X,JdXLLF\SX(o$2\SS+nbh+P;W6-b-5N8O(11Jsg\b?Y3.OoBXdjZIZ$;b%84/'5jE#9nijE(`Q=0L9L`ViS7QT#3JjBTH%!/")19,pd%^kstW'dJI
$l^ILddi_JA"cCbRnr=nQ1[?q(KN7@-&ONu5VH'5Rp*Ql_(5</\Z*O_!H>`-4Q3b%)haV=:b.e]#cL?pT$#:Enf&ZoMrrSYYf^bu7uY:819Mt`gGWBB?
@&ZQK"dq(R_Ug1d!+YQkI>^0!\Og[gBM&\j`Qti/,_f"f+(V)i]B/<?W-]>9#'ff8@bB-,A;L)L>&9Tq;DEfXD_^_7I"aTNrQ<O3d5gr=?>dShPTt9TP
#gg#RD-GI\@Q#c-ELRE//Qo$'+^,c(2XG6]NNq2jCJoq2CLG3IJu!TiVQRBLpuKS.&V>6*AVm1:+=j5C]*5[b)Wm:*<6$WLjj^U&p8&@TQetCXW$+2_A
"SQrR8P=L+_/f'WZQICBNkQk9uM^Z\jZe/Rf.b$l"c"I>Wk\=X-PIt&Kc\2prh-Ce<bgk4us-Lc^&t#'U7bP%BETUNSPoH^1bhBEi3?)?%YL7PXDD'P>
):@]ZqUcO!DNn*9&qNq!s>KcJlGppY.hUc87IM]cmJ!#2*6;9FJod*r1EnO<`l0:;L;7:)4XqHgf3q7mKuG_H..Ch_U(kV]<;<C5kg3JN2h*aN+qtfde
/`KSiTliQAMaK(AfLkA-n&I,T11VIWHe?r;'19LK7SrcKil-j>Z?pH&_H)Xo_C*SIXFS,`>'`8=W)d"Z_"b@VHTRu#]*W4aZJ;Q/R]2N9Ma#$8ttU;,^
@XNk460U_;E"3htH"26=SRFph9WCq?;jEm=^l?Fbi:=^.O@G)^W&*ME:jkQIJ*JnDE)9.;BVHX$:]Q]K3oMNTTYH!tf,i!"K+!<</H!p-G'5saD6M&b8
1]^dhXZ>>mrf$G]E)D$]8LeUt02l83![>2Y+O7\68C`>5_Rc&3#-kA$n:R='],b>\@8:ns&+3X?Zr#Y1=5U`,c5I%5,)QLV4Wp:G5;jnimndrI<tIpJ6
$?biZk^Z:g>0+HK%#58D,?gQ88#uRY-iVs%]-m(6lgd0oFP[T-e:)#$-rRUIODoA!";!76[7M6jL(K*rA63^HXikX@Tj"?^4JU^%D'b>FV.u5.pEb`Z=
L)'(JXo>HE:M`2-qX9FA\44Kp"tD)(4"q8T>s37t7rITW_Y*-D<^<1g&qVUg%GBNs0gJaK4.^B0#04Cll'2C=Nl?H3ch!KBq3-'Dg'qL#]j(j_%6%c*\
g>Gfl!0=\MY=1\Z8NcJP>eYpEaA<gLcU(RL9$TKU)Z2?\B\L.jKNB3V0L,]2s8H/jce_@aBfc!@HVJtj-n#Pp2kl;oZrYG-b)Djn/H0?:UH<nM>U42-Y
qM3H(BPUsE<7/Nq`:JOG5o3j&I0o\+J)#ugSX))AU$q)THd<7L23&u2IH1TJ=QQ*4?B'8iO5otnQ`@0]?1Kf>`Z0jgR@Sm?ZMZ(+T2l:K$Fpbt_O^YSo
^/G7BL#o4CC-I=bB&$FR<)Vc;b?qr^B[=,F2.HX%U5uWmR6S(pF7dN9]IZ7;R/7`J\M*G_l68BoL_N[I\-7]6dN0P_;H@,T'2hu''-<bAm_EO;5?`\ti
OXLS>]P;b["Ul2QgR(n_bXoGh?#;=0aCYO+7Mki-E7a'Uh@"5q[-TP=D#%C3d%)hAs0#;ZY-K*3Cdf':4o"R>J7ilWAgq4E\tasQ--8D"']pa_j,)PkM
bsm^=CfQ71AutU;t=GbV+)dl40bjFQWCB.*8G_,,@c0%KolE%NjI[o6=XEJI8ZE,7su!_o<.D2KP20*bJM03UHLGM]jk#j&I,Do[_)0i/Sk+?dTG6NCf
^(R$Ci_8i[6\aPCf64<TGpi>a7Ib!6oeoFq6h>$aE[gQ24is"<M0ShoMUM)GVS#$\$15U4i0PRsD6dO0sU0.q)$bI1u,o6l&kPfW?"p>_SARL`\PR?1R
5o@Pl"!NtJenU+98.k/r5U1UZ7M,/T3GSG90Nq.+AZtd>oDmre2bS&hnW''H9=OLGSb(DN+$_agg+BPAU+Z$P@Y#0u`b!`BqjK(c-M3'8B]mU*GZ^EY2
,bV727dI"NRl[93o'S*8K@R>-,J.mL8K>t0:Fk5NBr"7)QVGM:p_L(N+TtR/^uHfqqZ'F+*u%Q1*8GT4oZ)SY79/=LSO]F1>f)t<Eu7g$`"(&1k5RZ?`
d,bF_s`rs`l<=NS.$Y!D@keL*pAHGM9Fsr48..sfP+2>;'1%:;77EEB+Rr'/]0SN_\4NZjP"l]a#>t"=Fq.?7BGEM.Uf*ZXA9<k)rlUg(6@'DdkDF3F1
+)qm(DCUmN1l25O[S]%:12CY3ER"afKn"(OGP[?lNiNVuH/O^`E9O0`N(t(mEK;giRBoa87G:/0L"P?MZoel.bRg*JfYY%)61]'^Xtc$k,X\L.#-=;_3
OMHk:(I1_&;K"bU_UYj.r:aV]=r(,"`V@/&%B]8^a6AN5kei_"p5T6kYURGOZ]s,j_J87k$HXY2\qhiK#F>WA-kp&tLioJM&;]KCLF48B)EI'+lpqd>/
nF_lifh'39C7qV=`g!k?i+/B.+g+@@%c%rfrAP;oGAnPl(`_*qaF9!fg<itd`&Xt;Q(S#:m>1W!OE>*OfN^fZ<KG"`c)u+LC/Gq^\K/@]^W\SRa4Y$Am
hMeg"0t=JoqpXRl`E`K[-kh@nOQEp_#pbbIYS#F\&GZ^ejs))]CAjm#5tOF,X5R5SIbL_A0gn,((P?D5@?npXKK[d2q;t1\EGD*g+\7B%Kdm9,<;`d',
><$A3T@Q&U0^@&8(:X?U-#h%DCd4>a0Z[8`CBqk=9L>B_W+AkmfCM^RS?.A0UQ/;lTa]N>j;^n6N:Z\OO<"kHI8aeV\Y"HGZ;XE5Du`58VR"u!Q];XI`
"%2,:u%l`eVtimgc`j+A:D*YRl1JTt+I;EF[b"0_oH+rQ,gaI!WHg5J8?(_WkT7,V+I).+JP:>6u?_UDXrt-Ro`NO&X<,Q.bqd*tJ%kqIf?trIe.!^Y'
Bms+miQk<;!&"[mZj_V"c\->3QYd`N6^C0`FS5.8IZ;CbqVS*K8`_ioo!1CLRKdG2b"3*g!ML.H/;mpXO%S@IF^KE=J"L\DgVO)fdHk,cmSWL!1LnXuo
KaF.9D;Q%^XMP1:PGSOd-;g0]foW%+3/ttgCQ7c0&jDSs_6mt-9i1%&WpRr2K5q6%A$L]d.7Xr&.HDH,]rDMEVs0q9h$0NW.`JtJ8^k1<<Q]dd``d_F-
gP'Gf]t>8TWaX:RP?Xt1YTAfneY<D*5K8\<E*J>u5J^]fI/'cagZ)_Z&U^n(/pHePI*6DhOqMC!/D,lXR0ViO#k]2s,/9/?"9qe6fTQcJ_qLb5L`_e"f
J*%>/D)d*8*qaEEfcI//s\P"(OlN$a=;ntrQIS2KM$s.a=Dqfo;Fm;qpWGYVcKQlqVSlZ)8..<kcWQSb5bi^#Y4drENObuIf*+d2?1h.K%^10cukEoSV
F,Y@hFbHH$%O$JDU.;B&U)AIJ>NX8J7cl'qJ3\D`^*[Um5=(G^0Z>DkGlGo_Nn!&!;7'/H2r0Y)n)nJnMtHf0!P=hf@TE&m(Ip\>^sR;l#K5M^)iZAZ4
*k?AK[G#h'@L,?.hekCiJ#BO-[lZogLl`T$S^Dg$_-9XVM!pbPMANER2`9H$F-C_ZWi;)i"rIY\\7p@;GLF,Hg*Z]A=I]eF7_q=jV<G=Grl4)fo3=<uY
4/#g=<ObXqc?D=>-,,9f/UkV6/h81L]:+8SFBsr\9U"#EM:oG]MUcm5kH[8IiS[i.#A[`?aA:0:>;#<pDK5)l^fWjY<$To:XMFt#Sei=Y?Kc"YdA[)56
gT=%0o(3^JrY0c1bQRqMY;Z)go$c^&VW6c\CNg#&XPrh(nB4u+ltW<J%X']qV]Fc`aU1tEc(V#-\V(CqS1b2GR<D=iZSO$d/'gJJ5kh?<4$.$`IbPe:R
5==iH?U&__&Utl6cE9F5frdBXI#NHUW(JlH\Y$[\HaBe@t).qlC61b9c=8-T;H0&-.`==Jt,Dq_1FK^[j,Jdho@e;KuPm8oG%)X@)&\A.gX6l%:^4,kO
'#^"_CkcLUm6M&t2^`>\b6B*;gMY]<W<0Cq7111'+41eknqg,,F;B=)]8!@AaH_<r?4T>D;EbYm&FWQSC^q$iWNsBZG@a4hf1;8F_P3:)+&F&B^.EL;f
(AdhP2#WF)l`<#bE0\#&IJCU$1K_'K^^4L8Js!3nX?2#@F-eqL.XfJItb64ia\J-$"C;c%)71P0fJ4psK$Yiq]F3.:N;W<6@c/bZ?(-I?Q>]l,T[gRfh
.A0kNfUa.eGEULKtA[_gU#VT.l=]kgfo(uUkHW2^E=jkRS\LkO.+E`E3p&JaZ4e^7Q]c;bj\TiI0H\sETXLMu!_WF(>baf(ZHZ+?T%UL54W'h<[BpUD9
9jIOLDC$]\k+(9r?cCS#lLXJ`?Mb*Dk3M\d%5-c[1e81Cl*[O&?p@?H6]1a^,,N"%J>DRQSd$Uj=mdq_Z$rd>hAnG2O9!6-A7f+M[j"s#&=#!CFbYtrM
'mo-fGT7JTg>^8#(%>pM6^#DHnP]!YbT89j/m=!Z*Z_S]bZGelFlS*&O;RJ'E:.X3=4:E\@o5Kb@fCYN]h=b!t1Nk3rTV)QCpk/*]+.M(KAQM_*6.l\!
`ja9_eH()4*&(0G0oJ]*\1H/t*nLflr_Bqj#PLODig\;1^%i1BWMa<U_gQAr+hOP7kcC/MKg3NG]L974)8t,f<b)J"KV\i,c2[\C6BO'VL2@FI(+@]5'
S@/Mnef:&L'p9;3O\F0,u=(@(>apt#?($GBL!Ya:M%[$i*`NG#'!\),TR+Bh4YTl%h!#iMbIPho%7`Xn/jB@E&n?TYaS)K/G;VqrL^pekNYA'Ll4ZD3R
`ktS[c%r8d.8LGiFGX<i\JZf)7?<S7?@rZ]_%EVeC8nQFF`;E%[eu,<kT9SIV<'!]dFPVL$_EWD-mEA/m.soZ.g+);q%jDSu(QbElb&3K^^chec1$ieA
Htk:%*$g=ji0G$.dnNRE#UH:<DZu9f'a27Rmto0QF!b(WrRO=(q,,N5C=hZ@bgJF&>a5R@ldX/I<Pq155]n<FKQ=&&4@nZ*hqUCFJ`DT=RT.t`LdrO8X
sl'PrQb)rQW,QAmC[DmhX._[cOr1E0<VMP1KLip8Y.qWYMfY7-Sqm"o(>iTp#:lPT"Zc1Ud6S9Y/X.`bBTRZ/d4sNI*Wi@O4=U[W+$KE72+S_o@eY"P\
@^.Q2gDB<;!P`&U-_o?>lAQ)L.$D/o.`r3THQP2RqTPLe65RPtsF]c"[FtoZM%S"tC[)7tq8-T<l/9KH(g1%gM<\*cB*BgXL`?+/s]]#264p5^rQ:s)U
"qbj;Mie!Rq;`87n!Q-D0i?4h=q6[=_YlbC`NO]\luLcY%3:gV(2k45fipEmpsT0)R77.cfeXNp<,.TfG-3Q+a%6mXViRT7>ikIL-`fJ#*qb&u?_CAi$
YHIEt9+A$7XXi=`TDL><snVAZ-KZ->p#/";eho+]3.PE%[JRQLcaQ2)B1L?(fn1@_l8/h`#X/>kZaB(?+igB9!$g#U%q9)\jK0d%!\DPII1E+YB%fZ*l
_'&W*QPn=VO8T.q`Wd`C/1OStg5GPj5%\'hR5nmcnF##s#ZdZ5\!lnhnmLWPOYg/.XJ@G>--rf7BF)<tAAN9aiFcf^0/63F_6Pt;/i\4=A3kNg57HVuS
Bk?Ia#@D8h35UhPh20m7(MP*I@JEIp^9h!.t1]T_>K,&;>*sZ00DI;`;FHVIZMCG.f<Tu>f,C3E2M2(20'qMW>m[`/kX7<-\gtFs";4*E"7!u!HnI-I\
:CrXnN2=$WC7hT2VjPN>-/ncqs(e1C=OBQfuIiRIq]Od[O3nWm4X0`5UfH^2Mqe)%2DhPmmU+m@UW+I\"g?kuEGGG0?(R[c9?,o1=MKmu:'b';u%dnld
hC&:PC:E%[FANK#cH#@/_I>:!&/)=\B\c="2%19!$[Zl]el65mfBHS+OJM(bb*[5$&m0lZ\p2AiZ-`3@2IfRBSt^pl,N8\=/q[nfdI@HP).o0T2USWJo
#-H=)K\O@*IBaYQY*5)<QXXiqV0<g`TS`9^5\A`eL3h(@';$d4&U,IgcO]eX`!!/HMqptiKQG749Z,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.32'
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
            # Newer btrfs-progs list a missing device as "<missing disk #N> MISSING".
            if path.startswith("<missing") or path.endswith(" MISSING"):
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

def parse_scrub_status(output):
    scrub_data = {}
    lines = output
    # if "no stats available" in output:
    #     scrub_data = {
    #         "scrub_status": "Never",
    #         "scrub_time": "N/A",
    #         "scrub_rate": "N/A",
    #         "scrubbed_data": "N/A",
    #         "error_summary": "N/A"
    #     }
    # else:
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


def main():
    parser = argparse.ArgumentParser(description="Check Btrfs filesystem status.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-s", "--scrub", help="Issue scrub to all pools", action="store_true")
    mode.add_argument("-w", "--watch", action="store_true",
                      help="Refresh every -i seconds while any scrub is running, then exit (never starts scrubs)")
    parser.add_argument("-i", "--interval", help="Interval for status check in seconds", default=2, type=int)
    parser.add_argument("-m", "--max_scrub_count", help="Maximum number of scrubs to issue at the same time", default=32, type=int)
    parser.add_argument(
        "-d",
        "--exclude-recent-scrubbed-days",
        help="Exclude mounts scrubbed within this many days",
        default=0,
        type=int
    )
    parser.add_argument("--scrub_command_lockout", help="Lockout for scrub command. Used to block two commands sent quickly.", default=10, type=int)
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto",
                        help="Colour output: auto (default) on a terminal unless NO_COLOR is set")
    parser.add_argument('pattern',nargs='*',help='Patterns to filter btrfs mounts. Default="*"')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s {version} stat btrfs by pan@zopyr.us")
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

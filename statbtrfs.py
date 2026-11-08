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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 58):
		raise ImportError('multiCMD too old')
except Exception:
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE$ig8-O-i5'i9DjZ(gR+RLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)]U<,WTZEDeSe:(YNb%NdN`;%MLm
ps(uYZLt9N^(d>j;?gF2fq.JS8E^d=!D`Sq$Gt&.k_&Jr(6<fc-."_L#%?6QoJ:i3GQHb>?A/=XqGZdH'Nu>j"g6i-cqUX1Al)9;U'hMS[PsbB-tdCiI
VVRN65*?GL<kIO7Z7/-AG(/KNr5CflUSB48`AZQ<O!o56.5)A@KI42W!FK_W9I:Z*Pcu"q#26B[j5r\YtMNh3f/mh[:>.a?bbDGIl?<"5%j?DIG5d/Ts
'(PMF=5S;i-6>tYJB5\%lM:6R^S$?hO50i#I^("oAY)i;aaQ7OYBV/cti8u"ChJ,38fE9?;!dUO&>(t9<Ak)MrFI>U7WU'7u<"0V*sN=aLl+*[XMP=5`
JC1<`.kA`+.R+@c88R'7#?+L\n3"39^b6hl5C1UNZ0Fd`^MNIq?0k8c#hQ/Hsl1^D"LbQs[P+4WE`o0Pc2Rm2\bi3?-,]s37h(ct]?*[4J)5+H+nn;7L
;YJru3S\[3Df]`dbC`NqS9rOQ/t6m5UKh6LE>n5'KkMotdIMC">4ml;BXhH>bce81>'GX:Xtbt#&B)SPT>Yue:a3Ag('$-_0=`r<DT;!F-JosiL\Q`So
*5hR-aXjSc!_Tk7PH$&e^P)"XBkERKjZI/O*NLbXR-_occ*pIXXrGd\d]#rbLu,R=fk?J_Ch)@)[-i,^1Q&R>nQ"!DQ\pS!<Z<d-q\F5O@iJ>S#qH"4B
DKLn9=l!Y(3)U^NH<1[AU.*-)Zu&87MG)\L=f+:^>c*Nbpb'Igd/<\Pufi5hV<0.VcYYis&5IEKYrlZptI"q'TFj=ZN,H"U1gLeOLLlJT2m/_l7mR"/,
3QmpoKLmkjYpSB!T_Omafd/\BOP!IaiYcOF_?&uo$4K-*sK]gi,GEW%cCVVq0#'ZqX_Mp@;:#/rfToMn4&D&Fc37W1SqV%`[Ol,[GcN=E^5HL/=RR,Dd
OMpHL_PJ]hImU*366mj>b>67"Y!L9)/r)uppSu4]k6R[Q`lUm)A(u>%eZ/M9d]W)P%QZmF/=2-&>9q7i(7S2br_h'a<%G<,QRYFoY*YY%4J+h\gm6!TC
N6KFKCqOP+/^r/$`AR?kgf*cenOHl^M9WK3V?bQ-=A)DP]Y$3%#'"/Bk#A'(?0o8;"M)<+*U^i`NEir5/7#^7m96@sLcmciZ<09cObb5+eJZt0(.4k6;
R]hEOWFde>^63]cs!@XK_8kX!^*>"Ac][m4q-.ZNM.`J(1tZDQ@MNu&.P!*p]%]4<X:4=&JC1A./-_/g`VrQb6m!jamsdfd?ukZK'G(g1T:.t=<I5D#<
dLO9Qc)=/jj5?W=0V6j%BV<.a<ipihYknjF'%uc"J@TX/D:OXU`4M*-AVX#N'$&H/?DBs77mf\(]/hWJdLP.LbHnV^]T:?Keh5,7]'jF,_nkMN--<e5%
"M:=.U8CVChL&cKaXT0p5#Y-Fd7m7Y6V&k-keK0__mN%N8k,k\oi[joGg8K#ZER@,Eqqb-BqCU!<'(A3Q'Qt09;RN((!AFli&+k)=P]<:d_)o_<SYLc-
.isdir\n0O3@#SsL'^@uilMEUkYqJS*5/XIK+AtH$e=%i48Bg[;@MM^O[,1\Zb5bN9T\fh?-d'9oXoNGrn'fCu"Y]iK$rnM=lJnNB5F%$(r#4tdBnfI3
ch$gD'7C!,+M]=!r-:^^U0+ThZ)tVUNnZ<I!kVeGi4&ogk-c4[9+.<C#ORbak^O:XK^R!g8$OsX*+1DimS"mo/\AQ0run]Tg-DVdOh=B:.-m9<=&hBX.
PZ\0?l:j?S*eri;:L\lVK$RMmYbrW;qTl_aGlZ.CcdH0mYA1>X-&=O1#',pis].a'4.PM*\-P<8.1eeo!H/`Nu]OEgA(?L%&m69=_Tp>6[!E/htsrR/L
QdMgsb+V=YC+i)PhVco92nVh('@-!YY,AHc6os@G(L3Of>.c)OBGU;X#&7>l,*pc&m*=WkAj*NsuVSb2OrJ2a!Q)<^Uo+kG<LgAes*G!Ym]VfDG2b(th
hd4IlQ&NjX;,(*ik<#u>gWNj2uGrV<0f\)J;:!J5l"N1j<Vlf*5,qW-r%it>[>D%icns47AFHK,biT(poe!Ef/8n!1i7ZlPnU[W#ts'<r_H`ng"jVk$Q
@Q^=\\pP>CZ]KY%^B`lFge['7[2,(&g?P9V6Imh.&;uZ`?#CgYFrOcDcb!1o5=R`'?&n;elQL("A+X$@j_+$DfE=-q[T(S,G*hMhK0/Q1G*hDW)A-4J>
.$0<brl\gD6(<paV4N-L2PDOW?R1!R?6mST_Yb_ZjI#2!Yn@9+BF;J]nFRWWe>+8\>*ssg_[6<,9s86g;5S1lhsRq+'WM%oGkc<U'=%^0P1Vdj->j@-b
fd$U,CpUIg&Vg_##Tjn>.4sKC)<YZdscb8D^R8RN<.<5_f7&!QVkg93<YC.i$h+hNX;9p.j-'s>>f-t\ZuK[PeVQmbdB*pce8S=4%NKq4h.fgU)%E(3-
nhH8`<R1b9>s0nlRI8B@qKnrg!,/CR_pCB4PX1SkPXEfJ^8&omkA1H)=@64XLt2C0r]f<Sao5ZWF^lL^nU8A3245P\I6m\k"0`hrjNJo5V2sC%j=c8-L
ftTe?RUYUHt4NGo:.c$'2aP@i%W'bl[PYLJ3=oJh:s=i,q.Xu0nt@2#cp-[m_qN6QHeA;-FF>TJNe?mBpX:)aF-V)tRY)oG0`IH'.q$^d\FQ_D(l),>2
BA%l=<Hb^3*:d,Lr(Js`V[N8_Eo(42,rXF>a4X+j)8>eS_&J!oUb<#r-7_Y2Yo75Ah;I6(H:sHjS'<];Yb=1>[0%1@<id_-4<G1cuDsmMoeYZV$kBMJ'
G:rD9D_!:jqY9TYa;@*E(B(laX%)iDa-S<dF:dqJdi]+81_G(a^j4`'9@Pk6?X#Oc/kFqJ$m#Ji0_-&W-oe<t=Lgr[gg;qpf,/6-Vq/YOVb[TK"EBbis
#.jX0!%U3[!P:"+0)MHTWsH#6BOVOl;>n1rMcF<W[Y0]#E_J/Zo.b#S%K8E:\iE7?L*[9VInqK-ZdmiehRD8`&H[:d=EocJM>CcrsZ?8k0%Z@!.$/<PT
qrgM_i-HF7+0-L,/8YL\][#Q<%CDCp[F*+QV!>9n,jSk;c<6R&Nkr7>e7]fJ!c<@G.6')o?4U0RQhfcTIj*Z,["r\(Q3cA`U+_gutpO98MC]ag&a_e8K
T9]$jtFQ7Ed3l@3`r_WPkF\jj<hMB\hGBgC:^T/9IWZVc8%XG@J*D"ah<V)f8O00[FRO%&ut"NO/72M:HUR;kJV!t!JlTJD>(@="@i?_)"XAtD;X;KRT
>7sBa(+:mR4nPfF]S44=.Qq'e*bP@ng3(%ZaYQdMk-C?SK+ZmP"h(4c!D0eM7#ZIaf28"OKl'i@1]ik)[H25l+-E!Z&UO(_I5=/QTCUKhR#3H#Nm9$r_
+rk>U.QF02Sq.B6.^<N84'B7#m#p`HEh-oq6&pcUUg&:%'54^WBG)g4R5F"qN%HRd[LFm):u\eT'IEI?p?.Bh'&A2c`DU/%MkfGaEi]0,E.Y2Or3(YEg
Vh\EYbKMk8cqIs7=ZJ7_(@d>^(n"]Z<KKCG^Ep*c5:&YPJ#S*o-cZACgL+\^Qg..apRV7BjF$QP\#(8f$<(iK9YmY8n=,"rFkBY=06;Dfl9+LF%En's#
N,CF)A[$mM:`F)pAq2qrq7Tr!.#k)d1gsBm\P:)Wi!Te=R<mW1']2hIIYi2-Zh9!d[CL_mr'fSPa$5^0EMCjbQ-gr^FH2^Y96B4"/]VB.Y[K2I9l&B3U
0jTnSfZFUW`O3p(_'pms,;Pr'(_d=U<d6ZB9cRKd&qF#^X<;]GdCZU"_=6rDHK6c9I*B`5@@k1#%:5N4m@K=]8,N%5Mq`Erb`Js[dA,r0dhjt*:=-mB?
3d!f`+4g>n;VRO]ZK8<9U:;:$Kj5Bs'7%l<Gg=_bJYY%s`ri;G>Wh/^hLBn@]AB-uV;ML;2o,ain&ENdRFq)[M5&u22bc&Y===L2cH0"0L\CXsd;Ga3A
r(-@Bm>&RF*L"nRB)"/L2NO>Y=7u55?^3[qceCn[!3]Do63`s3g5r4@C#sAo?9fN&Cubbts3qP5?5W#\I.3>X^MO-Ve1_h41%E=[G[$T)piq\;^!PVI+
pOj0F#PonUSWJ9Ep/:I5nM^E4!=SrpA3[uKKt&W'fD=nDCpEaFdbgqpg,Z!.%<6r8f:3H[Z3[7j'<,2^u%=h4V#'d8(V+DFB2KOJo-RiK[>"rhQgrS/Z
m,(*KWV*WHYo4NWbr:^f.o-:e8\V8LT<eB@f9#T\I('"]GPVeRAE\`aTeD?p0I\mptdQ"L(!?PAcNaT!47Qpk1nEFp#i.lFQ]/oW8ZtE^`N3g=E]C4O/
ob^l\`Z9@3&mD/^j@I*NjejFWFlQ,C8g-F$T:Mu)H@o*n[cB7c3cDl]::K,D9[kntIX(]\.W%!;@.8W=WV)!t#T-;D,Urhb,EUZ861\M;_mf6`TO3un$
W.je,/)M:VAUrFO0.^[C-U49`Riu[rtbNTpum^?>k,a",m8QUt;(A+ShgojT+XZ%k]BSn6ETjg!<Y/-ZucW.bq3^jIB#BG3-+<Gn`-7"RP#=esu&D!Y-
<tbeZ1O.;X0gMs''U:u:8tT-a.=/5KoF%ZQd$#C8[e4saQ$R)r\&j5!bRCA39.LcZRj(E;duP\Q:RIFg#b<du"_;9ZI=gs6FIE])jj9qq"idOKTgg`V9
7^EO8T@U8eM(&Z4VDkr@/eNb"K>Khrhj.5>Q3+?%E9P'UZ#F*efiUD3i_B58;+f>Y4#,5M]6\uRH2H:'2U(d1J>CfDeP&1/<g:]0UUSM)eW4f/&LAM1i
#+?#d*dK!t:hg2pd/FbL7YWG9$@gf-[a\:oZbL>G3/4.R.tcf0:or3EQmP;?iFoT;rTH?*7J>DKA"4D5\L/TopKkHQ&6#j)+R(-Z)2J98?g1$A?!d4*4
/jmbu!'R4t/P,JkjE#U;iQjE+i*h4fsFT$p2`[1J28::5RGWCsOiiXiMLbt:%f65t$^r&^"qbB)W$dMl66Da!nS3'm^E!nfN-f9Kj"BKl9CW#p5](^uH
Qkj8c[Z'u.I++f<SXjZoi#;8LS)g,KLi8'R*Fua<i^0'OmF+NJ-hig'pG'R?'IllJS_s8S+]&(ink.4cb`^dH.N9KuV=4A&fRJ5?hl?2NIbbj(mkRpDY
W>MN8jGrk]Hbg*s0e)a3'ZBNMqZ_:]]s;F'_>;bA+(MNfQ!(6^\%k!+o7iG4pMJ`bP6BKfJmU!Q%T`#Gb,LnQD`N;^M;KRU@-&PB-9<'Ei8hs(kH*uH%
bN.Rl\`W6*F],*).h_gE"NYglk;3X'q+#+F`r(q=\7=+aM8km@f83"a$*bQ<sM@Z,-uV?H9BWE=J%sUGn;c)Rs]>LL$u/_\UpktpD$OUl6;VIYFTU?+1
c!b5MC#qnZRMM@#c][GrVk:]OJQtGR:lC&mEBX+rqesegZA`aP(-+F0l<ff1,)+,+_O!cS3t<T?hj#Fr+dOQ,J+tqhKD\601Ece.rE@-h%unVDY+k[N=
W,2<r(^?CY>87A[nK"NVW3E8;'4RtE2js5qKe9tE@doJ!C1d1hY!]=Kc/#u!LR\S8Z#G'A:OGN@2QgfB.0].n#cnu3Lqa'D;e`$rst#Ene.CXMsM)]JR
d,MUFGg.tg@rQrmc6mBp0@+Ea/e:H7()4[F=<Q8/8bPjK&Lrd&aI:2X3d=C#o=uOU@mH-Tu&0_%i8(;U'FDk4.r.-%kU?."d#Pu]M<=K/>>BlG[-:Dp,
-%n?-O$)^gIes2k^@e@jd4S#8ZLZB:EV9q]<Wr28j7.LdF$M9nYAI[#^)_/3qss5tc=&RF.iC+Z>+94L'CN>l_PbF]WlQ-18&OeU6$+r.D[/-dddJ)e8
EK"L5$pcP'Hrf\6GPECZtcC!ZQ?=<`k9I"h0.d@-._8H+r@#-A)7(JXGHI$e3S%VZO+j:F@gE,1:g@u`2`J&b3Cu(^XE2'*b9,0OFaDa4Q%X72HuP*D)
[3(JT-J;X"uWYU:b:A"%F1cXcTQd`,"Ar-2DRHn`?YPc4G22n*NRVKl'8-3gRQcn_g#uWmu-&&S/L_dG`BY!pi`E?7@57?K8q8-D@1Irkk]#QTOIbmV=
`R=r]EAY:E-MV0GiU3cXfQX<pn*/]X@XC#RA<V;(KYBVXdpGj*\;J1Yc@+^:H.%>.6sDEPd"F+hghqcEFpfX]#GFUh=%*idp'<#W8J.eM7+\O]&cU'a7
1aR^M*CIXAd=t?E+#`_=V"YOmJNkjU!S(9nDdXd6Y-0NE8l>/Yo\EuJq&&N`"Xfm0HafQHer#b(^U8#bkf;%s"c7"Jh1fpB].hju%m)pQs+."YYMu6OA
C;Tb,O8[%RO?]ITN%5Ec>I<)k?C;5';hRS1p4i1C@;A7uDrp5Mi%<RO/F&Mo$VgZR/9Kf?5oRR&\T0hDCM:]XRt!K-`uO_^S,QZ4ZZ5umA'k5j@GD,&(
]]BN:2::o"&r9q[>)MXH_-i(jDGD(LU%!k)3(aXIY?c]il;/TUj#s)g\/[0aX=(_gI>gKOm'&@CUV8^Dem@C58$W!mD2POFeOO[WdFohlR>e2^C'',[G
NC&iT2mlqn_GNOWB^"g3M0kW<GA;Y$'"[.5'6F@D([EJ"4K*@(_%pa(nfl1^*Vc\g:`C&:gkoTg6K).>46AjmLDkJ/k;E6W\f@l,gK=La&I`OUr23gMa
e,m"D;:ah'0jD,$m)r,rdn0^a/P8r.bHh929l`j>iT>G:J.$r13K@JBi9Dg#&JQ`<92it-Ql0M<-"W9jjepRI@pUPKpN'M]IDh7,Q.`Qi,<i@\6"&#d]
"Y-ZjrH4*g-c8[Mf;f#uUa(_JTWCs1B'U%5jbd20LGV<_Q[NFn%g7i=-4mB$Ip6<+?j$JXDrN-b!i0F=_%@r-+1SeKb,c*+`%BeY)m`QGC$B-q75gdg<
G8E?uXS=+W,:Oj$$46co$WW5m7MeKMVmRn<8';81eOJ:/QAD'92j;M#*U'G;mN>kTQK/!:!]CiA9^Nj4^ujr>W6,o$cl-p:JYRB$qT>DN6U"$DB[cl6*
)^&;rj<n7[\f"+2p>^Ag-+B+c(8O5i1p]e"2CsX\(`;0&4trt8[7?m9I.&/\R*gj*j])oK8@0U8JFXmP%$WHfI/CN8-#&)/[>NdLN41M-U?&P$PD^Zj'
(,?\>e#>k.+;G.##kF4a"4],#o%S2%7=[4.o^Mf>X_iX'%"6bbmH*JDI[ZpU9soFeF5Co1,(::d*u"3:9%fC<lm9@;smk^H)eIk#9W!a]g]Sf:@7"\(]
K<4g])pe3&B)@Dm@?>o)flK&!4('TJZA^"$4,69a_f)m1a5<MJh?_M1mW1L3d"nU)T/T/_V\C$j4kh9sSpJ)('ldi"@pjM(/V998!2i2P4*,.h)cTT[<
>$R`#5CtE=HE)ZI.@]2C6,-[FD)+`KoF?F^<V#kBhNeH'Us(l:8m3W>>gdBMqdnH\,]TrP_Hdq[g6-t<4%\>Nd@eDgSR8K.M6-@EF'<b?<dcHTE<mD#q
qGaJc1'1"O@%k;fi$LUA^"C1aDgR$Qg@AZob>tYF_stYM:o\<aBMPBG3&TXQO;"80>qTrcJVCu'CAR&43X*,W#P>enXZIm9=B=k:5l/jO*O:ZWQo(64[
G%-=/1:@M9^XteRlcuZe<\)F/OOG.?BnT*)HV6b[&@8%BTnjlcT2/@i]X$]EiY2$0e)cqMLf[b25o\>,;"jQ&*B\-"H+M\/a/c.joIj^T,ULHaT*ug*&
t3]^iBS*AYpI2CA0$`GI[qPG@+d-^8B]@]8J<QQb<@P.r)c74>cTA*)t[o+52qhcf\Y%QJ"%U:d(F5o)WO4mXqP*pc;0\hotpo^jL%erV=M'Ufnth3q>
@2?Hr[_NZ1J(YGK9D8.pBppF_$MPSkq#BK[;fpOW2Y`HoD.!;I^k(0?qt5qs7U(!MOuUR+_<ocho>=XonY:Q^`+oAeDGToH?(X"k1a$g%[XT0O[(c!>5
U%5TZ(,H.Kq]dLVWN$o$FdQ6H%7G@[b&&8*YNt4PVeoGCYJgkdQ;kk?#<3GLk<Zg]XlHF.Q/gj)Mc]d6ENUOu85oE4H=TQP3459%InAQN">])R.fK1[p
)eJ3/=rtaiA#OEM=f0del\jT4E@.glC^;8_;XfI$AC/TB.M`r)+4C#CBD?sTeZYn)Yp]*>08]a$V@c\60I8qoR-KnES,i?n$">?\';2@<.ES!j8):3i(
Z,;(pU`0`3Q3LWlSR)V28,%?[!_;p%<U.a1$_a>"uj43[0,!rMA%.+R"?0M</17?+/'<d7K[%4;/)GLZBC9bRdlr-@U)If/?UFcklK:1fZaBFB]27M)!
eu&Rr7?'/W*ftp,[Wma'Ig:S`4+L[DHVW'serhmedBf$I;,D"@)3-n3e#NRN;nn:=634#([me:204W9Pd\5%T^*dk,E(tX<Rp^8fo;+F4.1\pdMl8mZf
"u;]m#]EL->5?2@SrX]L2gfgu`c?plXA_:Rp:mA33r-S^&nR:3?f^R3KrK*!u#LWqqg'Cu$,UJWrc=ZS2>Dr)9k),3$eM25iF*U.=#6d"'Dm5os99##'
7hCS#V5UUB',G?amWC>>9<M)kG9B%tM8*A(a%;&1+*1=[#IbubA:0GcHLQ#+uB`knSHA/WJ#NY+-<%7`un7LN8rW([EcH1pSb0geg-fmsNP-JbV3De3R
RIjDXB@9@U\R*AXf#;ga,O+&OmUOtr4S)'83T[s9B0$mT/NIGmgb=2Bp&lO,d*2YaFUmGFea(;5L&Qe$JrMDTosfaD!GNN,T.J6o,/,uE"1-hT@u#Yce
eZQ/06h"km,h5DmV\D#*lpf\>UM1e>[B=7k!Dl4q!>%9:kQ>=7]p_pflrF78^,T'+F8*[C7-sdOV,-hpc8,m=jIWkLtIiG$TeB?aaC5V.d>cEh"+%G8f
H`-XF!nfc10A"#B+Y/jWPsl@6R58>dr>@_nLJ[@+e&:daS[;;-V:?2=^!'YC:KpkW;lUF&5.l^UT0hV$[6AHhOdI`anm\aQ9n2(D.n"+7'\-Ne3)?U.j
0\/bRQ:>)mA4.pK]0ZXV,R&TR[l!X&2Ia?ghO%>YmG5j:W0B=<`,jFXb&,-D\'_7<1A^X`GQ1.G6uo'EBnf&V/2&kX:tYNdeLjN62I!IIgC27@ZH-pc,
C6AL?7/DM0Gc<&c\`%KN7l%VO\1pBiF\?HRN8/\471l=lu0Z)(k#mofP:=THAK%&0pGfJKK4Khpi#Cq\WED-0tF5YDCX1`rXb>C;r(=\\io@[V;9JWgV
lOZ*d6?/*jj3"Bb*MT<bT#D>:&'@k8/Ai*#5\+*AiJjK,ljb&sGfs0_dqb8V,mam?+G&Nh/\<p5?#4KIM2)et@U26_@Mt]3#S'"9Jt^#L_#/)S)EmbMJ
)R@L.See[0P+a>^(YTHrl.g/.`4BC=/l<Fo8Qcpe`kqdb0su/Qa,YTVkR0FE?>kXdr#.O/`A'c6cs)bla-;`grY^r<h>Us(:2PTOf<L^/a9[0rCuc1,,
(t=%eh;,BKL&H>o9?hfs1Pji23KcH!CtlQe]u&&-r1_.RKaNWoe<<Ba#3Ia3BmVPjn955.Jj3'(]5GNWR_'r#]<m,Y'onH8]&[7Q(r$aH(H\$4Ve4d0b
]gU%=e:,<%oC'd-)p\pn>q8,U"hb$];T/p:g<)0;rKMk.b#."\XY*[TUL@([b3d47Y=_D;RpdS?/IHVm%-/c70s`WtMd(6Q&>+c)7mC(sA"^RL]<%rfV
9c&2D0@>5a\)PjH$kIpliAK`K5Sk8p]l2tpOH&jGs#_h7tBnVk62qRInC*;6#)^eae/Q%,<*S+FIh=5-.ICQNcK->(Y_cXYakuP,XA1R6>`YA3KT.(%&
L*N80)fbH_.oj@pjFVIC5+6CWNEiVN.^NCaM&!M.S9$n87ubjL4eif>J7337k5QMt4HRt;g3LO98Md/BqAogM$!$d%6F1KlKOai$n+)o=AbL^VYd?7+W
MWY=-I^'cerW$<"^COeUErO-*9pVCGY(lUrR&#F=](nH<#`M%nbnioe6q>D\-UZ,L)C[K:1=C6;*GFThA^f`8lZXj:HEV7_DqFtdVsPQc,4Y.f5]1h?U
AIHVoUK9-B3gEV/%&:@/W6rIes%X,<eG&B0p@[LaM3a@g$q0HcTne?hO>(aVhnZiE4\be@-Q+$Zg"Zi%':!"A=Q.ZbP58-\DnWmT[@X1Vtd[&P4TAlic
g@VtU(4igMKr5^9pF7KUiM'm^k-)`KU7Z&7<!ZdW-KpJol=^_T[`.C]Lh<]Q3%$eOW^CQu'A1YUQ$L>TLcS<jf4d$#,9otH-DWeS?VXQh<O7N<U^,\Bi
mU1p/Xm:K,A4l\RA%fIF2YF7_d]ZIi&XBR,:`%4Wr(YpMe9=nFSi\3kP+XXfZfk9+Rl42cX2*DSVI*/g1l2[Lu<_s^7+c])/92UdB=T6ioTndX]*JgsT
'Oi?5L$>r6&2le32Vp85"%#H=1oU^JDXKgr[.FNl\O[Sj30B'lBGBA$$"p-(n!8Dn#Da3r>l_'e*_'oNa,3=@."HVQ3m]R`::CZAKcj9B`R,+QL`WCq`
FP8ZUYf"X9.8Jh>'ENB$gD2"OoSN(28'uE<LJuc9s8k)01#1kIU'%f#T`Jlkh4%'G<F`2`J$;:og<a<`7/N$&79uA.gf+"i"M"_dYir"'\gfb1%MSKg9
/]GF^r_u&0,X.4C>`([u=qaKPI>a]Tt%pg&be)CfuHZi:g1_._bBm-\%jE:<e87mjSYr):P:1.0jW0WI[``8at3/$*L>2b_!lG]4A:'1DX>"Mb6(nb(4
I?O;]hhXJR+p_c>+)$(D/0Lh*Ke/HK%0Fe02V]H0!V&:QYH#Behn&kY;kKHMa@'Tc7/&d#ZWM2BYr4S?bb4G9'G*V134Hu1UT4Q,aqU26Xb$/N9IQar5
6Xa,_:HR[<frGuTIcq&/!Tn(M6i$JdAQoSJ8,HVN/@aaY6r-+mA:#5of/gkR0om*SlNM7cF!aq\)Rgu^@9)JbiXI#adA?gofE>\d=db0E((u@SW_,k"@
+0`cg14eV![4$TGs#qXDHE"_4kjM)JHh]*^1!=:]5:*88LKiWl*sp]8"!K!U@iT)]AHchBZQ2r]5qt%9MJSU&_s,(sSLS6E7j8cY-L?<P8M*!2cbk/W(
?a_ND!3A$Kt&fTa5U[9)?/<t^A4;3`jT>,KWOGY?JrcMHJP7l]c&;OUJsm^@s-!?kEOli0M-QWT6jgsUg3n9f]KO(V3M3M'+8!]?A=s^=oV=BmEVVq<"
+bT-%>l!F5>G'fn<6V\f;<KQ[RVk/X&=9)3ZDm28I0A'STdpFk5"=<>$C-:m?Jo(2KDHBfe;MV(PaO:"-Oi+,[K/Lus\0;$n0$LkAWBa*c//FlITn('/
"XOU_B_*S.ql8c$]8*1%DXKf'OG#<UqjL=sKtU[9^D!8\;?"HL^66Eap!j8Kf\m0rH3":bh/rH<T("ZI,=?(h,e$E>o&Be08>0,kVg9Ua<W0EW'%b.in
/#ku(;AnQ%sLb%5TrL&C8IZLOmNhdG!!$'%-pcV!RAGA3F]?FTh2C$)[)8=AJ["-XT.JG3IE7+FPV5RJUC/&J9iEWshaOKeU/@;eTYZ!7Vc2+bWK[hXg
G9'ZuL?3R)+(RfC(6Y6CBR'@YC'k-'>q.sF2`M5)o,=ikU.T8LZD^[g'@tU7Qd_:eVhK2Eq&80.d&r]M0-e[1j-MATH+pM@GggK;lc-)j2e3MLQ6E8:L
ZgJoJXo;_a]lbH7U]:SH2OLj/i1=;/3:oo_gpUuqT,>KT8SDpPalEa3G*hA>XS3YBrNG&9:r;Z'"YocCi032JI3Q/HPsrIJ9g9`_!DJ8Qg$^%6dDVJ4B
GYTb$6@Y'0oGF3Y=(@icGEBi*_M22HYuNPN`"flgWh^UbYQF:jV2bq$Fi5=kkhH<;@NU4/+pfSo\&%&"OoIjIJHOKHRVjaHn53$p3INYQLlF<e\E4Dgd
2?@m6NLosm2_"5/[s5"VX)$$>-oUcr-\+``$'g]F<c+Lrb\4-(Z79ZA4+68/fF%][:`DVET.EMKqLc)).?K8FXV,Dpi[99q=N>:"f2UWYI:p%CiC94%6
(A;/+Eb5d?Y&#!G;;0",5Ih)DfSfoQYo_C5M2DH6&D9#rAS=nEKM3c)e%Pg&Yc8:7PRYNh548k_q96W[So?d"&XiEUK2G*1,V$l<W`_X\VniIC$FR.>%
kW&pQX"C+r_8tHj>s3>4ID;u2>us8&%e$ek3eEP,Fr5ffNqo3_n-`A@G"r`kYq1c/LBZKaMIQ$%'O`)=;d%km92pEg>"IWDM.`7Lg2CZTEK\PF&XD/dR
,7*`"5VL+)B^lprr">UiD'O'"Xk6dN*RW`&dds!2NeFh6:mDQi27*B*1h=f[=(\N*mVK;K#s?<:8OuWs6f+OLjg`f?d'C@h0V*0#+TWK;S@5XdVhg%OJ
6*%%/EtrRH9:b`bBl?Kh0/Lbe17/0(G5&)C%?4Vf$Qe+6!HMEO<IF#!)a]jGRTMOPC.q+FO&g7[=OH#fqcT[NnpIXSi/!9?&,KQEDZOi/9-*a*:cOW1N
Fm["X]k:)3s65D#3q(N`DTeV_(.8Ko1RIRKI"lX?EIeZYVjV.$ds-mI5,p0UZ7C-c:e5"e^W:!F:hl%BDHI6j=nm0F4?l)!m4^VdnVp0lt3F=P5hM*[0
P967<.P+NphQQt)r'T+>!j*Ai5'/FB(V[MX8M(8?c6.)CIki&GM#LsijQYl4>p+MnVPf>YNPBN,pJ*W=.\\i=)HM_`nk&lbfg=o[NFD,re;coH$Mu\n?
MHdh?3;BnT=Xd3Db/!#<N#b^m67s&%1$(IXS#fW;s&Qd5^"Y@tC&HL.WW5N[(s.E_#d\gSa*.n\W+Qoa+sE2Y?Yj%nL@KF:\5F*c-XC6#j:Ii"P^+ChV
Kr/i!V-29S+/K=RgE;"*&8r:/ZW<FI2<Tjq<gQc1*`9AH)R]$JC$Rdir;ZV[WMrgBS@^1]KdD6,[PQVT&MtOF6J:keAM"+MppWj&Wmc9J"<.>jMPK5Yb
Juk/,-`s4hS6Y#tEj?%6P"s$d2`qj;.K:o"hOY..&+$0,5oMoUU@/5QAQ!"N&u@E>+V!1AaZW+XVj"*Y"MnfSW%!CC8@Ul\1VT_:C1D[LXi(?WL2EIXQ
aU1]rU7@1ZCdfT`.q.`oWNEmRMe`VPN4JaOSUn+)]raSO^T?!DuubWS,fKHh1M)ug3aWZ>\_LO(M)g)Aq$l6F_2$S&%c10<,\'K;]%kD*1sT/*WrB/At
WA)3F6)SAH\;aq10W-#mc>[-A*>?ARP\V$L%J6NCs0Cf'of$>fj&_`E34+B7351Y?g>m\L1Hu7scHOUmIk0nIA(db0j'u1*&=;Hc]BfPOkY(f-d$)&Zq
SL7E5+\1V*pi[_br\guCD#t'm'8GpT!2S"dmU,U%$"37ghd"GifJ'VW,2Vc%ni6]73.;L*O[E634`6LjO>&$3GrQ>1"#NRS8^QaT*e6-ODK;3bX]J\C`
8PPAOJ,'pe]GB%&dc;nR_Y*lA7[X[0Fh8-$,m$(Hr4b@Ib3W%Y""T^8DRMB+WtQ@#/CpAj[qV55JLbES*3Bi__<,2;:1+!Qoc`iF7dAr]&2<g7[Uso&d
\u;mgD4YRt.qcT^Sc48tmJF@XBE26CB?I,^WO[i4FU*NOl)>7^$V%$Eg\GCCF8_!;;US%#%#:e].,d#I9?lq1DEI!<5Z8K<1k(Z.*!G?T?boq`FBT/79
6^A)6dN!4Upf0Pd94!aPuanb0N^ojMstSM[`MBQCh)`JTR!+-Bt"KrA,iNs/lh.t*@e!$KB(1s0r-a<7fpqj>bVj30HjQZU,MVEY!H,b1OZm4cge2cc9
O^dRKi#s\!&IlZ+(m/_(;,,@!Y^Rt[/_Ck;n/]S*sT\dO59"0G8E5VWb>B9t'b2t9%eDIQ?52Qi`D,H$cGJuNK%c`a5hEHS'0LDg3J@:9]l@n]NJd3^p
?A1asN<BO4alTki%P9aH8Yn?)`:YoFVY>"Sq`Gf!i=bp2NE/1R7]]!TQn]$V2bt[JFn3'a_\lEpHq./Ja@"^L,HTD^0(l7F.2,ca$0h+pT;8Ka^OI(A\
h%8!KghZVp;<eU'je@40bn;BJREJW)*sYZSs/#A7UII,`\jdh>l"7.[NnT#-.1pg[Yq$G<tL#\WMf@[%K_hM^]k<7696!e/k2ITkU^9;)gi`jiWSYHNm
E8,%gKRJdOJGLm5sd',*S$^19,_iA<TJ<T_[Pt.5Ms]"9=si3**ZnI=&;/]9XTFAOgL`#[=V+B(tLt7*F/DZf<e7,A:)MqCOsTE.T3=BHNfA(\hVs(9$
,aO4LI>IU400ZA-:JrXQ;Ee112[ghT>qTFMV6oWgAr.i0;r3EUlI3Cu4i]nY_V?f/pa"p4/DQ#*^Y,.knf15Go(jub?"KrX0^%s*qcOT?Bg0(^3@k4)Y
K?:"Vr%FBM*GYTOlC)t9X&TE:*iHS=@s5,>A/Th8pM:lfrd8bar<6$gt2!or6ArZi_d`*NhF5EO,Klt[9.bJKQP3mP>1U`ou$q,J@Xd9^8#F\rZGVhuF
4*pb,]+#]^qR]mUI9Rc.i5JN[eLI`8mW>mL2C7hik1`/B/KNtNRr4dTX.uq-5+3Q1bo?Y'iFB5,h.oKs?@s--:H79:NqOmMJEk:VGNr#:-u,K+/W0]'0
Y=aiT$X0ih9si0Jp?,LrJfj9$+/#bnc/e-PnYX;g8b_K+Vk?2P_6bi&YMA>X?_T;r?g+)\WQ$7qS(63Ht;sViSg!7RY:/o"ia)4a[6+uU3.bBeE8*BC\
M5k18K:l76@'H1i7q&gu,!:7E\5e:&n<2j>E$p(-Qm\@(PK]1Pc_!8;5<p>7UT?e+alcmV$$UW>:gBUl*6',dN/uNTmm5.i\L=&rU%-=4`nDF3!.^2*g
?X:Tq<?ce_LGqfM<J(Gmk80bf36T_XO!SZ4KB/7l']Gc&_4[su6qYTte''"d.Q=_Ps!>Pg6?muUsW>A6I0]$PN?]rfXgMX%erSC-SPk[e9:Mo0Au)LM-
b:8t@C"O]kR%C%H7DcCX?!@3/o$)*I-cD+9`7_!p`j9LnaG%_9(cZ<)LLs18E+,lct!)a&k-1TGC<lVguA9>.Dp83\H"%LrpHY`G!Xo@_n&i)m$j<.\s
4E4ho**eMdn:<B<UhgHZ*N/\bE,YS;r2@32Y6H^Po<YXHV3sJLr6'0ZQFo`NTc80(^E0X"E;!Xr_g+joLVWs-RtIdY#7rm?m.4GIW57)nnA`_!4O5@DH
T.-Hkm4DJVqGn>"l@]65HIhA<8k,DqK'$;,V==g`B]YG/>KE01MhE%GTHecVhDZY^e'&O?[(eU`8A69s,sSq!?fncQcOLj9*p:f]"'mU*EYra3J,FX_D
`jBg3(Uo:fr)RJ8O"["^>X4:)OR%TQ`^S4,`0.I%h'M2M=mMEYOl,mA\1DRR,Y*&IHobB4h+9.CNeehnA.,ja*t$Dd]I%N.aR;j6esQT*;B(Hg+OC2?*
J]i^QoPS,(Ne-L>3Z7]M4R`V.glOG)3qiOV6mi\07q2k;%B40ra4ICd?.YW2od9@:AT$$>ap.r,DH'"#o+mO5-bIAXH,SD3dGrCt@V048;$r\q&OqLbh
9p<iLJf)*V6Dmn/'[Fbe%8jg7oQm*13N^AhZA4Y<$a-rgolN:XA#r(#cS")JK"t@;.6gl.c:Lu%$,)R\cHHhSl-RG#rZfKIF%#4He#;3OiC+P?rn'R=_
ISojf*hl1gTct1)@[2drni2jsD9#Fm%COKt1\Gsa>_)Yb.Q.d=Of9dZfYK7L*[A(?]`#[SYMp`RnT?PL`aQ/[0G+0lbR>8oe%-uX.>>m+!GLl-WsgWg`
Ht#05>+aY9Bt?^0)m.Rl8OVt.0cCdW@%p8OR2f#.oVB?,TM27N@!nn?%j*N7L',VnttGK@HT`q.4i4teqp]mN3f:.rOAt@^Es-EZ9p^2;G3fK%pf@<`q
:A3P*NlDi=b'0X?WRH$U?jX!%/7s)190UIc;ZM)=`eCSjp/gOE[1L%:LF5nd"Z-0)eeEr,L>B-C=r_bt-A`2)l?0N%V26EWbpl^@EWp@BNZ1&=#aeF.M
oRg&!UBYP-,mC(^qPl%4'R<%d%7m"NM\5)W-sbl@;$*<Z%h&WAI82<KRsd^LeN-=(%"8[LTQ:WJih]Dh_6e<5[m,W%36:)M"dd6WZ[]/FrZ$7C2;B5!(
"&_je$$GQ\f5D0DA.-PsRdtV8T;F9b[\DpCs2N3cX.HqVDmg^gZ)-6D'Wp*YW0^K]`eH3i9fiBI`Yc:0Gl0Te\[/buLLDEW;X!ou!.R`i=kEUs<HDVar
i,B%s+rhbTjO'AsQcQckR5&)h]qEe.dr"T>1^2K._g8d:\q.WR!PqSC>FkR.<^TicIS<ME\D@oV3*M@)N,>:,UtQ1c'p-!8VfTRRD#a(Mq+bIsA_(LfK
KlWFEX2:^%@1IkfL2<D[k&;h]/%4,aWQjEm6f^M3>aGmTdU<UY@ao5V;*7I_<F0!RhO-SWaRZa)jX\`*!W[l!mW2Grah<C=(tBLR"3*uj,Y^B0s$-d5+
LaJj\/lkUIuVb]Gqb.$0)5NEQ0iP!ePa<3qdUPX!_IS!pO/b`7oQ%1NbcFes/qD"]dk^_Q&mu&POJPU7lc@k::=-B<$qt0:`JSTfMt"L`1&($G78Zbs%
8m5(N&H+/HDjq3T'KkE^$&/*Y6(e3YQ&<S'2-\!W7CHDY<#5`/u1Bi.Pjf:Jd8AhWO_>@t*s]Fo5s2n&,<1H(sgW7I'd$p79`89h&lCRf!F'ZJ(=DCGa
%g=,tTR<-,f)\!JH;B+G*L61D&4u$U^^p?eV[8F'<\W?X3#%e3r]6b.r5(XD"g*CiHLdQm>;pHeGiLU2Y_#qWiIQ\g69,Z\1P1&eA,^5#r/eU>+cS]+o
5oVso9q0AUW-OJ]]s$Gfl=Y#iI&`rXC(`>)a8,4mYX2<L9]+=R/_B7kmNos<j.[0Ijl!/ir'G_G4j:FL4^QG"2]t9.TMRY@,][UEH/!_%Y-!pZD\d6k_
"Gos)PCbR#+jT&areYKR]4g8E:PeMrYZ$A#^Hg^l34c>P"V9E/Os':J-0kK,SplB*nZW,Ie,uXd#O(topi+WW`Vua8uom0>B5I;SBIDMdBi:NN(bi#r(
DK%lH,[3BhPN/f7jLK&duH(\jc;I_aG$o8I;t;63%qF'<Ctudl&65U')1+Kr;%820@R$`ZI-^Gdo9!8\W>1.'oi"/T\f0=.*XE`&[clL]Xh$!UQESnY%
9;embaf.Ygt,V10imDjT5bTRtMU`bg,S1'G.7k/2J2YJnuU(s.bJ%=6_>=D/2Gki>ODDd!Vp[X1@i?/oSIYKi>ZI2N,t$7&deD0kD"AhLN#:,BtD*bn@
^AO.QAVk]k3O7Pna:re1PMb9Bg/I=&:)`fH=dC*;7'+G&_kZ-q%B8U,/S:ZXi_&!F8$Bi1Q5:*0idkZ*77mQT>nK5b*gB7L^Xm-c$fteLE#/GusFN%S?
2]a&P;=I+0!4HKld@;lb`+TkH([Md?<YiIQ-k\9>O,\sMSNWc#=Zq(R1f``1VsTQtXGO_p)h(*8o"1u@:Vc7RkQcI^VV>gEj^A7,#S>.FXJJkAAi<Pmc
KD3PLE`qG!LdSQf[T]nKSm?^VQhp`NLbm8D[+*JW?>p9,Ir-S+k6hr&geV,Fn0b`)]Hkk$qkV>@UjMU]#t1\#$s+n8%+^gQ<K[u@Ue9IS`YCci5X2^(C
>i\bU]#HJIdBtec0Xr])!V$8\f>u8HWe0h+DWiaA@rt0hA_?1h2pJ,[j&O02:[EP[Ycg$fk&-au^h`*2R%b6'!rO-Zi@I@<K<sBL'\dnj?sf9)]`^a$"
LZ'4s:=.;LZBTYWhI^3AjIN[9R/kW00)@L?drGSc>c:;!V-A(c%KB*?<+2P(DFCO*s,Dd?f`aXZ1IpF3jcP8bM6-Z!^H,hrG"#R7LMGRR=W7lZNN1*Yj
XZTK)=Doe*2T5ar+KNqE&Z>9fS+X"?s1^lg!6JY0>Ok;qrILq)\>LSdE8+k??lFkclm.55@KX;mQfFn%]&Cu`do9h(]UW)+C/q"_Gotp2iHbb#1_e4c8
i^@+)Xj0--25A'5YNpr/e4=m2X!g!XK;mU'SLe-g&s^+?iV?#fWO#_7-*4[Dg6EifD?_jQO?OO0C.hdf>c?q_19B1dWZe8h-"8Q,i?N"J^'+]^MuOhKG
-e2WTHl\@84ce4g\oCo-+qDa#ID@f!Jn,aSQ.A(L;c\iqJSWl(LJFlW3@P-fq:cl)77_\-8#lpB;0YCor[i6?J41^^gK1/eVt:p2'dg`8C:*pJGIt,cM
^QCUCkchO(f@(N3J:>H!=.TH`f/f?qALP5j7t!"R&5u,<9f6)WqsEI"IK:#2jK:MA#!h@R@_20=(&La(cV*bWK#\-(YB]$'4udOH_G]TOkC%M#jB_G>p
k/rA?39IUL'8HiR538R@cK[iMWV/Xl!:rI9`DaZn@+nOW4FU>"%.CL8UY.1\nXK97*hZ2>J09+kb/`8Aq[CdpN#;N8DbBM)WjI)Oea&<`5q8umn+#pIK
sj)tB,Q_b]D+;No8Yn:8g:hqIYqk=el/`#[c3h"mU76Dd==`En*Sk5njJ\YDP5_.lZiY^S*bei2m]r0J_mJQm&[G?+O5i.!Q103;<P``9`7X>i<\u=4V
rq,ITnQ%f!i_BUp246]SHbMCS"MN!cQ^D,SA$W@9/0XN-(M/L_oq]B;F[F))Y_t>pgF^*3#j%\6cA"kE09#iThXrGbg%"oXpNO%2A`/nb<lC-J?E,(BN
I'lkNX?]!Xk'1):TF7N"8bn0DukjT&SZY:>h05sY[?)4ZGt.W_+*Zpo45Xf%K,M@/@Vg9f%W:8%=O]onGP]k"qb2I<;NB]Alee5s&>ipn[h#Z5d+>]k3
\I`RZUXq94fRk$qr@5+sEFc>'&@)1@L2H)BjlBJ-QGoFn\M&^G]Ou.?M'T"O@&/*<eT7?fSeEXT&'^=7odG1fqc]!!bDT:Iso$@D(<F7Ppd9<auJKZOO
IFlEk1RKX3Xu^1qafh2PbQhJMnT?Mhsn/rmVV]_cX,Rl;q[+mK^5r:7BaHJ>f_+,$4E61L=PT^YBo2/_:$h&\#HQ]_U=0m)\XM&kuI1G],5Mf"V.9Ph+
jC#k30Osn!X!15&ZX(Ye`3Q9&foG7bOKhp=:(^=*f]@`[!=p^pp:*Dt;H5.3%>cnVeK4`j#K(1[N&V%=_epf_.'tV&F-]LQto./m>[_u6DlZM=28G:Gs
C[GoZGj8,G`=Z1o@]fK;N+QreLC`f9b>[;^]Y4&=1k;ZAT"X=DG'h;K["(*O8b`,I:pGahSrM,jP1<8n*^$d.r63sT5BN@YTcX_Zn8;X/o"@.02Vd?DY
UcC-[EL#"Jah/4<i+Fo&!O%kLY!<-asGH=Bt&QTF":3D)YnhfJKqd2=0LY3NE@3a<#=foqbu$#cKg)<@/9%#i_U9R@o##XXLc%6n<GB7_95mT%a#uuCH
^J*?/e"([%hh\/:^n%JDk[eUJU.9!BYd!@T+jL:k*ds4h_Vb8B[N]AG,-sX['YQ/u65O7D"K+!S8?0!Y_CN4?c,eTQVGe+d8iX5e"RX)r[Q%^=\pgDWH
BU*@Q5T*<%-\GY!&Sp)YZgJf]+G#T.^:p\WE0Naikh%g3E^*7IZg8m=D$(u3trm3cm;G5unDVUcMe<>OSl&GFJb3NJ2qbknNkkT&Ro"KXepA!dA?K,k>
(;6*fBb*VEHjhcPCP,XXLDhf%54RK,<^Bq:l,Y^udIl]cIMCZ>FJEb=;JXuel#F]?B%k*#(D()7Y+TL_ekY1]!ZL2oZ!g=;UH9d@l9W2IQ7_U/10o/H$
:ARBi/nK_;WjnlggV&!WIA;Pc&S%7rq%WDaoqS<5P8gi;-aK<Z$]Ws8P3Ii<:0jn9AifbNm&&$;kXLW546-L;5#$m[:1&_MQ3*g!+Yu;X#61GX6I$ip(
kf82bTSO,ga35-U[+7N)f3!sn\&hu\hY,I%$q:#SM=<OWf;/kg'`!k9G97?N"qi?pfD%e7,>AL/%809PU%(9^hSA)7P;F)hHWS+i6DRCBe#"1(d36J2'
p#'_n+(X)`r!7P.'IJ>b@Mj`.E6N`,h>e=:2fR@(J0sO66.bY5PBij09n"XnM-JhlLJpp(2;4mmW)e8Pl^4nEn_qZ=P\GCn9p*o1g.U-0d2e0\6?u[FY
*B!<#$YPRBG,2)*D5%3J?U+[t1C-%_5#^#XM\nJJt`',aUqRn`_-=r(hu.Df_hS,dq*rYkL@Ztj=:YI*\;*j?F;;g4]/)-5Dk;39Sj`a-F)Aq2Q5>>)5
_ppO%p:1I$65t6H3*f$=P!HqtD;fZChaO;UWB/"6YqEs[PGJOmm``M9;N>P>FPJ-"AO2@/k%kU!bc<P+;87(2#rKEkRVnYH>+9])!c*3hjW'WYaQ!7Gb
\*,G-&338.:!sbS0Mrpf"nS)%c[Jd`q#e[N$_p\Z`h18?,TJ)sDfIE'-;Z;LI:^QT!t-Wu>=<OMmUnhQ)OXa;;;f8p^J2R_iS<R3W0+sON_B0=2mj<4?
4HK#SlCH7C_3.'=PFq'rP'Gt]FRn_Z)U^)(AT'#SEbNi<`ju@H#mJ>N[J,YCRX6!b#RX9lX304CB^/[_fM2X[-uQ?/iIZYbnl7Nfunb%3qVUhU*M_#9_
d[:*X.QH-n#Ab4ihl?Y>pI:$_N_nl8$;Ii7.*35Aa'!T/raIC[80g)&I.^GSqUumYX.-D]@BLFk'I\lkC9KCV0uek9:`9gV1tgLG)jSo12-1Wgqg_/^M
%.P`^UPrr%_i'8Y]B#P_9?.dg.EHXbQ8)s22(oK;kh,;IDg"GQ/&nTb240Ob'1.es:<-/VON/DT.u'3>@7R8Caso]kd4LR_k'AEM8:d5t@Pnr]rAl2eU
A29k[Y%X%b*8G23-6fn]%PJfV*gXR/$P5".&Jh]pshciOl.[VR0@t$"u18gT$IPp=U'\&/LA;hKZhLGk^c&LE?fcE(5*+r'_)TfarNr=q;);jTCR3.Nm
!!0HY!NjiR]:N`,Z,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.43'
__version__ = version

# -s runs for hours, often into a log: don't let output sit in a buffer.
print = functools.partial(print, flush=True)

EXIT_OK = 0        # healthy
EXIT_PROBLEMS = 1  # device errors, scrub errors, missing devices, or a filesystem forced read-only found
EXIT_FAILURE = 2   # could not check: no mounts, unreadable filesystem, a scrub status that could not be read,
                   # a scrub that did not complete, no root
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
    filesystems, a scrub status that could not be read, a scrub that did not complete, mountinfo unreadable) were seen, notes to show with the table, and
    the parsed scrub status per first mountpoint."""
    rows, running, notes = [], [], []
    scrubs = {}
    problems = failures = False
    unchecked = False  # mountinfo could not be read: no forced read-only state was checked
    untold = []     # filesystems that look forced read-only, which the check could not confirm
    for fs, filesystem_show, device_stats, scrub_output, forced in polled:
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
        mounts = ', '.join(fs['mounts'])
        if forced is True:
            problems = True
            notes.append(f"{RED}{mounts}: read-only, though mounted read-write, so it takes no writes: btrfs does this "
                         f"after an error (\"forced readonly\" in `dmesg`). Once the cause is fixed, unmount and mount "
                         f"it again, or reboot: btrfs refuses a remount read-write after an error.{RESET}")
        elif forced is None:
            unchecked = True
        elif forced == UNTOLD:
            untold.append(mounts)
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

def scrub_filesystems(filesystems, args, screen, skipped=None):
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
                state, message = 'failed', "forced read-only after an error, not scrubbed"
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
            status = merge_status(build_status(poll_filesystems(filesystems)), skipped)
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

    mounts = [fs['mounts'][0] for fs in filesystems]
    incomplete = [m for m in mounts if m not in failed and status.scrubs.get(m, SCRUB_UNKNOWN)["scrub_status"]
                  in SCRUB_INCOMPLETE + ("unknown",)]
    # Filesystems -d skipped that have a problem (their rows are in skipped): they set the exit code too.
    attention = list(skipped.scrubs) if skipped is not None else []
    code = exit_code(status.problems, status.failures or bool(failed))
    if code or failed or incomplete or attention:  # never a green line over a failing exit code
        counts = [f"{len(failed)} could not be started"] if failed else []
        counts += [f"{len(incomplete)} did not complete or could not be read"] if incomplete else []
        counts += [f"{len(attention)} skipped by -d need attention"] if attention else []
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

def watch_filesystems(filesystems, args, screen, skipped=None):
    """-w: refresh the table until no scrub is running; never starts one. Returns the exit code."""
    mounts = [fs['mounts'][0] for fs in filesystems]
    seen_running = set()
    since = {}
    try:
        status = merge_status(
            reread_unclear(filesystems, build_status(poll_filesystems(filesystems)), ("interrupted",)), skipped)
        while True:
            seen_running.update(fs['mounts'][0] for fs in status.running)
            held = held_scrubs(mounts, status, since, seen_running)
            screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
            if not status.running and not held:
                return exit_code(status.problems, status.failures)
            time.sleep(args.interval)
            status = merge_status(build_status(poll_filesystems(filesystems)), skipped)
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
               "read, a scrub that did not complete, no root); 130 interrupted; "
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
        return scrub_filesystems(filesystems, args, screen, skipped_status)
    if args.watch:
        return watch_filesystems(filesystems, args, screen, skipped_status)

    status = merge_status(reread_unclear(filesystems, build_status(poll_filesystems(filesystems))), skipped_status)
    screen.show(multiCMD.pretty_format_table(status.rows, header=TABLE_HEADER), status.notes)
    return exit_code(status.problems, status.failures)

if __name__ == "__main__":
    sys.exit(main())

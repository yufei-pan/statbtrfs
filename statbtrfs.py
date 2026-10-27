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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 56):
		raise ImportError('multiCMD too old')
except (ImportError, AttributeError, ValueError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE('"=7F>)aNi9BGja'AZWLdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh)]U<,WTZEDeSe:(YNb%NdN`;%MLm
ps(uYZLt9N^(d>j;?gF2fq.JS8E^d=!D`Sq$Gt&.k_&Jr(6<fc-."_L#%?6QoJ:i3GQHb>?A/=XqGZdH'Nu>j"g6i-cqUX1Al)9;U'hMS[PsbB-tdCiI
VVRN65*?GL<kIO7Z(I@QtT7--6!gZ@"9F@Y4QIP8RIA*-bdk,+]#R$+La,Jh\<l'=[)FCUf"DiJ;Y_2E08,M;Tj[Ld)?GSu+lFqq<Nb>r(RsY@X(sYW_
C-GV:'QhS:IZ?:cZTrM*G,>%^OcKH&@qHVtHo$?LMYe1;P8aj6@5@[sK+i]>CL)suM"O3$.*^0\UhT\4]JKN:T^X6gL9>u?1fbM(qVR)BKB8MD@+[Wc#
iikSh2A,;C?r(#<LLFi@$Nb[-9gKXJ:8LY2t.:KZ[G/H6D]JtL"hr\1)Ms5fr[-VUBo2EOI[5D75Q,6,24^DrD#CJ999!XRA71&G@ecV(_Md?TRIct41
Brfq:?W@mZe>[oNO)#aE1(bMm26C'n?+lPa)W/%X%9NkeU2`e#rt:a&!j1")ZAf;57PgLn6YcNM+Iu=h.^WrMg:&SK9G+N^Q*V]C>M10#(@oL!e@^M+P
+Qkqd?"])EPDoOI$g?->]Bmpa*kNLD$'[,Cq3`An#*BDFek5i9@IA7MP-$Y1Tc0Q:QUl^K)m[LV3D)3/V`bLK8I=T5gQ4&eAV];@<]\oZ(M.aB?lM)0=
orR+;PlfWE6aqN;DYF?'O<=XaR(cPU8EtG0'HpYeV-C6#k'9J.HHmpDdpXLi,dZ'se/@#2qZ83T+D`_Y?UtS,9!HK\t,&bs$U7iF[!Y7]BPJ#fX#@X4n
8^e)Hch@YjfiEmL+%P>TtdaA@ts_nX?S\DtJ2"GeD81olk.XpdeSqNu5c]3TK!?(5LXs)QCI7p-.?)_h=e,UYOD45MJC-p'Ap,?,1-RAKTMW_Kp6Ua6`
<pZb1J"e?O[/1MN<a&s4//sfhA7C^6$R75)TJ^E5VE6hWCZEk_.FmHYZ$PGNQ\_?qf+dN?.E_[C4:cYd.8%d7CRae:TR0S0&lnt*5Z"C&$>DGo_(3Qn\
LcotQN[e='$bWF#S^+=n\$7BYQg4$"9]2QLd(+G9<l2`m,46pB`s4s\cKqi1:>CgZ2!@:t<op`"g,,9(D)mKCLednp>Crp)''%*QJlb^@dpf%n"dUlo@
Sc\&BjV-MYh[H4Hc-9o6uU_h@.4?QK.5-(*j`?TLab$&ggn_15G;`iptpMn\:h1U,2\caF21VPcK?:],?ceU5oOQ@]%/,k<AJuT6/X8rgX8\V[0[u&94
WjX44eJZ?Y(MN86e[8QY4/eAbTmZEe_GG$F:/)^%>?uqhoAR.WC??GU5UKG\h-[gQjmR"@RG+D@CUSkd7i,FWD"L0"/QNcU+3Hd2A0JU?7cGD--r_10H
NmR!A2]R;Zh-haNGX?g'4o-uk?MEK8M'ZWTiE_H]@!bE()ZmFe<!NMO_BCn0cdSkE>BCN]ffSX272NSe_.nf:%%#+8:5h<@4`h8:KnVCE@IWp\3`^u7[
mCZ2!fAfdMp7.LrfCBF5IiaNP-b<iRf6/`%!UW@fqEls\*'Z@?9Da68;qm96./l,6*[]eJU+)TV:o'S#TeN7G:6H?@&-'EhU6?[2RmHS3,jm01#hB1d:
-?V)?U?Irm@auZKqD^RQYQqJ$S;RAg.A`.T_EYYqR!aA],QTd%X@F+#+7c:Y;IL9)KS3NiLg-nZ0%n@nYe.uo]03df-ppC_W[Hk\[K8R@BZc2j+DhW'_
c)^KI=)Ke@;@-Q)6uEVcl.oEq3h$[UL!\(]@SOar'^S[m)N!L[T[>I:$aLcJn`Vu-%44GkWD"7$@UO&fu*l:32^c6@"3VaR'ZUTS1Ko.T8^Z.IMrf=:X
%TD(:Lp3r\IFD`]X@"YWgJsh2Y;$_m"!=I_QeX=;$P-J)Ben4<;:FqZCFFM](W>4aJkPJi"Bc/1teM?gE1=K@<)%mW!_YeV-Eug83m<U<<t88^#^u*_h
4i'SAAlHKL,+(![3nRAEn7(9A\kMq=<K[-^_qc`9+&2o9h:=>7^$-;M'25Z/I;l:(BlZEJO.\#pQ&.L0@Wm(Hk7%."3=pZlrm0E[<gjo6l%GM@_)3f7E
RPic8K_O"E=&10*3(PmO'rBNDJ*spag5nCM[s)I=87m!icZNSS-O_KMMPW]><Aj.;pgsOC)qM2Pqa<7r5RU+ZLC.>HV+DF?I9ER%:2cWt").K>P!Y@V5
k`DQTTS087ZU>26Qk@'5L&FoO1]pB6a9k$2KB_TM`A<=KWc,@$YKh"NB[J$='6oY$aRD#//ICL_)E301OMatc/oiDJlN#7c$ap[!m[pLinmtTV-)>7=F
^Af`?#)R8J/hi)ZX/YkG__NXmMGBHZa5FrLgJ&K`\pCNM3JSjP#"4LhGE#.TC(Ako]1C10dpf5^+@)/3LNlL$_8)m@Sg=O3anSV&-<2W)`PW=!4/9\%N
/2q"\Ggge;oo.UH<cp5JFjtI?-HV[,WnNKlQ_(\K4bsK+;K@P)I4&Xqr5;k.AM>5T>9OD8.g)3pZBl:b4H_s7p=.d7B$pPS;j6&)ts7&e$%hc1"U([oY
BZ@qV'`:]DV\q*kJ1[NK-M"<="@1_(_,Ym4_3AKY`0R8:UdXPKEu9f;*s$;6f5NU#HCK$<mgSgl3_\#tl`6=<NW'n<+Md&/gTS_CiT-Cf:6)j="%?\Vf
T"6qq_[_JR-4d5PqCo;ATaGaOVpO;#Y8dN`_'m&L06aO&1!,]PHds3!9[\MFngeXO3FqeiYT`joCeJXJFYa?b'.\"E9rbSO?Lh'6soWF'UVZQ!;D@>S$
5&6(d!m="\S);n50`dtW<oH_,5AS`T9-_8hWCT:hN9:krZWTR:Qb2,G^tV/6XZKcPZCk1acB"0<\BLlNpFZ##`oWqBP*;[(p9L/]BAeY#?-Z^`TqO/f7
U3WVk3q+MA:kT._aS*/#2-/O'l`:SbT=lV@Fe:Vpg,:0ehSQ30DJ#--``]U0uVPmc:YsU3T,onX=Fj7bP1cpf4]KIL$jpf@DInAniK38rtn&\OC$>?:]
e:c:^gT?6Xb#FBDRBNZj?8=H11\L\S!gt%V\[]`dMZj^CpD1.Oe$=V6'G9eC->BfGfm6YW#48b^._aD$:=U@^B&?N<dg8g:gV*DoJ,VjQS+kQ_,.gE_m
fT^@S@$fbL>r;HJkpdUui+qV3pr#U^qX\15Xl?SI7<[f(u$]7A<uX+H6BFH)s.i'"mN#geU(9)(R=;D$odosIO"KBM]&[.")@?h!^2^OJ!"V)_aLaFW%
'?uY.,5uo)6;iVLGY8]^_5"i0.-hu:[.dt6qO>q9.l(#&ALR9kCA+UR"0/1=!=,?1dhohjne.?#Z?n%#Ncdrh)JUU0'Y$M0&P@<2C$GnY"30Z@CZajDm
LTd!uk*_2T3l6dPK*D',%cGR_1PbnBkBLQNI=:J:V1YQI@l43SC.6QRCal8tHA/N6Sm-k0Vhli8;l_"coD5)4Ym($5Lnj]?;`'.ZI';`DgOeL>So/%Z?
i$TP&:.IDUW@p&l2?OC$<Od_JEQ_]iL+FB)re,K##QbDF_kLF3pFuD!h'-@@Kg$OVa&,L.Cc;q#r>,FcmkM!1ZN)V[4M',/0fhD\RkcV)c%YnmG[RuHK
tP<3I[WUf]hQn+nHh'r#jl9d0:RfgJ4&i)en.u>e,$N]r*mU9u9n#^ND/j,KkOs(pZ+e^o=.2=Vr`nr\h>dfL8ks;@Hf@V#`\4r=52'6]\4N:c`DB$I!
kgqXA//7`dJEmcc^9[;t:dc5:LGIMV+fc4o#<'(2m*<PJk!]%6NChP^$d'%;*<(AVo!kWACdM+JasDcedEhpm=iGZFA.]>foKOIF_`<UYnlSCZ"Sh7?m
9X$TtMQrbs28IO74+Sc9o#o46ThMeHubQ51>5dOpERB=,a5eI->f2NG5&4r9YajEK#%YQ0g6:aCrCD&P[-l7+]POH3tr4rrJ30lMk*adC3hCJre_$!r0
P'_jC75A'fZ]p]VM0%-3V/K;&ME9tBA^)`m<6:-._GM4'ZD;E`?$\pnmof+.5N@5_*`n>_^2f]r:%VGtmr3eSac>n^r53iX-5$H4fqD>+l`CUO'r1YIO
8V9Y,>^j=U+b*E\VFR_)A"=18O0n`g6ca@*V4]HJ0O]t?=oS<o5)e>!IF:CT9mPKMi[8q":m8K81a$\l?^cOjmGI>m7l!l4mV=3Vfb`sBY,CeXH<1sK?
10`fV[XYa.LWVl3O$:"Oh)=>&nO%R2AWV0$l4"W<YR7Kk_6;1qiq.5[^%T=C(5K[BZqoY[1m<YF%etUo>Z!ZBk:u]>p_9<5AVsY\g[TUPORJ=NKo8\o!
t#^j:>,2tP!V;D`n;0;&<(\r@`r!Be*[U&KH!TfR89SbYEr0*@]92GI7mD;MU'X;LT-ZLXM[cIF+5Xf$4n9@`>2pJk54Nk3#Lj8qVL;G^D?]H.)TiFOc
YY#?n,N.t>GCU!4Mi^;Guc$IGCk[t02<A+2H5A<9HW@9?oFqTsW#J,bV*gGIc>WO$2WdQ3H_5q]#UG634]$G3Oh[A!@kB#p.qF0-eROe*T]'QIG.<o_t
S[VtY7c5OC^mg$]&+P4BK-"b,$4W=jrB".K,YJbCIj#<e%%t;PQ8phj2Rb$A>0DsEJf$M-;';ADZ$&YU%l#[U&Dj;FF)m[4VF7JRCNNcRA0r@ca:$DW8
RQ5e,"W`kCQXGOI3f:?&[iVR8(d0o5:6SV`'/8-?p+^qI2a-L!CHF(h?BMIQf`QW$EhduX@U.a4?'"RUEBkdMT>#5;WK*t*_$=fp&Sl88N'SDe4=ICgD
U#=nk!'2T2o?$!2"[H8'u&rl%=+Z\e4o!)tfLK+/'hbF'>L^&0lQ%!@!Y][TJh$Z*Zm11#Rb-VDR\3"j]V`;MnJ$Mh#+'>]*CAN/Lip>0s'])9n?[XbP
rZZ>\IOHks@m<n@rPHi-pjPCud;d>d!555Z"4P\Urd90$J36eH52_3uegB'2LkDHsecR[@jEZfKQ3Rfi&q1Ytf->\MfmF-MF)i=B)fqs[-oBHCNdidEm
B_UWP7"VCX8W>F1^S%TB6"gHd'(3/quM#P:'AH3(Yk.?fKCX<P1Q)!"F)(1EtIO,=g?^[d@aD0QOD*4&Hn!D35h[d/#In=dg2\%"sJ+HW-T90M7+8M2s
!*k\'dM'7E3seEG0YB8W-)Tr4ki;'+\0%,]&l88..`m!O#;qq&je`FIWh/%f:M\Yd66ibM,I$*cZp,YkG6un8.f+O;>b3:nrppmaEgWc1ENRi4>Y\O>N
$bT\N$$)[rL+"1J:Cg4^/bD8&\=J'9<,1U@!PKkU;i:1*Tf#+A\\sl8AjW,6qXNW]%<]db7s=R'%6ZR3>E4h*sj<NQ,`_>'XgODGlU0tqS\[%DI_9$V%
&SB0iLM6NoPdfk'35fR=FD!XaJUqD;PacYjUi'-%Oo1L$!lTlMmce!+G.Z[`e,)md=HuScEZ@XbV4uqp.i&n">C\KS]+PX?Q]qQOGS0<-7__\]3Z?D'5
m('Wg%=oaC'78#ot-`.<KAD/_;<les1C$2@qc7M]ba\GXR/;GtH4"-c216s"$%<18sM#4=QdN!"/RCPZ`eL)ai9o`AunrU0eb-(.%c_(l5\'PoITk"fQ
lr"ck0&9fb437Ke?L#/3f6GP\1\@HID,ZkI:@;f7_Qk)8)1Hb"8##2##7kOK3L]9AVlGVE5k1_=;=nGX-#aa362C1!Nmb.FTJ7<6B/Q-]2OUQQs">LZ-
(bU>X\)D-[$`_1SU%Q/iAjbL:4T@^5C@X\Dnl6Z/n@/4+dorYX!jLBQO7"O3M.$\MMH0&#Zq/(X2SUV-s.dbWB8ku$-gBV1P0_sSV@:ZXJ*^1or'.Xb>
uE\j!RlO;&k6os/M>cFlHH0+bO%\qO:\;8$H!op#NbB2hI2M%]c2XWnuTH\,`Z7]rLjcp`/p.XWA\]@33HI4Ma<(tc3u+r(q90N(eOb9--Jt,+s7NU#H
Hm1Q_SRSV`Ij>K\>*=Jr\G#YB#crOk`$6SKu.pQb(?EZb^(?Pt*mnlDX:WCKhDE5W5s"b(L"\LIrM!s!sShKBLr&,f#5m?%7e41@0Gf,@&,>h>4aT_8A
h%f&X9H@]DYfEKF$)(jBdqq3IF&pN`d=q^Kbjgr5.*`>YCC*=jJ6!Me"K^kEsXJ'GdL#Gb8`jWa:]O'Wle"\taM%-0Tgj+ArO-9.3t;*ZbgWUP81'7-d
\G`0FuAgdR[F6)&fe/[,u5AN2;5]Ra^-pts4<3f%Bs%b;RfE/tkX95bAaX)qHao2fQA#ZgDFjojlF*<Y"bDHR)r2ADlU\D/S:mnPR#@$-1i^S;Wld0>q
2(r_mlTq8T[%F[Li+PNUQRQp%ELO3K=(p[F;q41K+GooUTM$in^\c-iJ\h-Ef0+gQrZ!^nFr\bA)tP4GkLthhbO;IiTHY4fGcO"I1>7d@aK<Q:g03RLk
Q5Wh;<-MFZQJITPn`^/\pgUl>FWJDStn2e[GT/^217-3'o]1eM&G-;8kK[J1i(O)9a__sEFB(jFSqY#U42aM@;lp).T-4IKUlAtfG"tkr/;YB^Md'a\b
1^0gM2E2'p"@`4mjsqW83M=&tqi#hnN65FYh_;`ZJ;k4G]rt2$C!RZf?="V`G\9o\g`">panR>$u]bJ@iWNmmWbPL0Bt$Z?))i)44<!"hR(Sr(?V\i^S
TKn3;*Di)nfU6Z0q<CD*."=HIW\3XS:?UP1d@-a/W1Bde;9k,Le?><;b'?Qf$eiW]-I-2$P5dl]lko-N/'!OqiYI)'PL*qg_fG)-T.+@OgNV*3J02tfS
Y!qqUG`?aWdH@!51lWkNtH#5QFI0TK?OR@0<T*p4c5CF"rZQ(NcO:A!'C.9u=ffmjK7QGH&T\B:Y<L_KFdkJHeF99,=qB=DZk!52X6SVQW;(H$P<nqeP
?amr?&2TA)m^XS=fo'3S0=O7,"*uT8FIsQq*rp_+MTBmb4)/hR@U:Ya;pY&s7DIB(Xk1EtDJe-g[ol3mW-U^u7k!6]CF<n&d@&ZO^sP@g^7@Rk>i6/I`
EE7!%Jm5=fRDL&IZ70C?oGp;-#GY],/i4h,[EV&`ZC+VR%OsIZ<rD#8p&,?ZiDc)3.ME<d"eJkJ2SgRF\NV%?H(iQO'-#,5\@[os(-,/h6(mL.:>CXcs
3W>XcFkCD+G#t]Bra#&.9`XeVD>Z0)<!45VLMR-S%?fINP+%e^Sfbe1_mU/FEOdA85%Ja03jPi]EJZ(.NOf:/`KoA\hgtAXA#5+G%%bk:ni0J'cH"JFS
*lEF;8>djh\[D3G``]/+=oU9Gsmf&R`na6e%>Q/oZ_c`kP\1G*/&E.@b]P.CL;3H:/2>[bj_K/)ZWN]^.=*e27)b.`D(-$E!kImtX>+5AgnIjpcBQ:+b
q2QY!D!i,RQAUq[S$7UrRn'C/o5HRAU%m,P\l'Jq:K`,leUd=:WgH9pMg,p1!KA]MC%r*\:g+I`hodB$4f7a`J":omCi4'T=><"pr%2gujne=<(L2S<<
6K(OKm)('o9`])]Ama"=b;5:FRY7-Kco65[*km<j=0)a3:d:"^f1)#k-8qAn"@9PpJa$e$G(1E+cF.]spS^Y>.LRTYYo//i\NYqQ_qu[I[k$S%,:D@<8
?Y_1mgTDj)aAM9p<S)R=+_=Ti=p=[VE5.4ODIH!8A?UD%&qF'X5*qLpY%X3eifDr]Yq41='M!N3t\f"&D$V`d/2F_AWA<q_3")plIP-^H)[W/1JbCB*S
1[ihdL&)J/Q?_=X\QjLPTD<eJ%!\S\DT28hKrT.+:teOkA6h>$>EA6I9G=fG0C2\!(/:/p4@^.?$5g1p-XRF<F5[6+/dYFC-D\Heif(s!H@f]1[Oj"K9
5VXdfQsoS$Fd>1L++.Z-p'>-^jsDg$+U!)*ReA8)nGL'qQnH&5"3ZA8WYct'FF?V0'FZM8]eg[p@:oPsKsDn[@O0aRjNmeT,e]7uE=LZGu3^UC5F"%fc
@iSN(l<4iTe%Wpl?G*#g+bq_AGiV@>ST)PF!o,uN$HAK"ij6_IE]3E';#&6b*5qD=O(7hhsiVIaqF'(5b^Au^?@B++5)O^:QZ:+U.YZSId\(SLK@Bs"`
BL$i#*&N07N)fn)=,+MfXO,YJ?]AjAb]4G1&uVBf*cs6@,ouJj:pgmD^Qa25AFEeu2ICP2TT1F=3i"I[ISN>#i.O$2PX,##jue"ET/W/j),:ms*"r=TN
p30F?,'>/!?U^]-O`\8P?6EKlDjj!J>S&aJI0lM.HHC+DM`99P(Fl(5BRF91_5T$3ph@c]ou"]o\l'3TM6jVdPb=jf&<%6?emt5%Qodl"e-[g4W?Q#p=
JZ3c"ab5]u'/uPZMH!BB^_r3U79^<1;]m;`<)]e0It-WKam`eZo3n+?o;*geFpkiQ6[]P.)@f\$85tiQ;l0Uc84!N+,fT.#?OjTMnXUM;]h@,C6k%SO[
'-=t]oVRGm\RDMi-S,m`cXTQ]:`e]`*"J`aeD!Fg<)S)h@s/C4c;PQho?6A9orQk+m8lQ.F&5DF>\R==,BM\L/0't90,9\M_@H53]pf/3>)3Wf3K@[#)
s5K6q;`NDo.!1GUX%sB=Qr<Q>U(mn!2gWQYXUT&[B;sc(Le`\,@R*a65fl(3&7CIi8<.N.&+sBURL2Q[sPbUCi/XiWToMI'K3i7?5arJj.jB54aZ@QeU
8gK>6`':!H2^M8Po_?gONQhMoMc:T*\4VUF1TNLR@lR(\KBJq%>!Wb4#L4u2*e@+fl<)F?;:#5)+\tbVO7WK83\A#/CZQH"5U(!@=29>M93cpVoC],.X
HJ;VC)1HjYl>6@k:ln>f#5DhX_?`*cRPuGQXaI.,Z%$qQ,>5m*)\?25k=LrgUcX_^V_0pJ_)D%)dV'`qS`.>X^i<Bj&gto(N$?5jPGSA>i.^GIeP.LJ8
P!o&XmnY,sq;F"2a>)<lU9`'p;N(dK:QpE57C-*)/Pl0lg'fCKQ.j54/Kp-dqfk$'9@$rXU"t(,XdqAJOiPVe*KhA5im%7&Z9'mc*S$K(C<5l,$cV2^G
S[.MpHs>'&i;)t^W1]"V._h5LCN=o[Xpn:LmU)_nNFo0D7C>M!N<o9_.%pHm`O7t]lIL/:cWo&O_XrnJ>VG5](d=If$S2q-)M#J6il5e)+_L\,mf!42I
BmG1953;on\*FEDlWkcgT8jfBYi!drQ=eujFBSj:I2F5^Fr?l)<.`p9..A[pBLkhNfES(278b7luAM*>s?i'1NgGF)jh'?=,SBer5R8du^fARV"gu&AJ
Og>)9Hp5L(QT;Y1fNpAG8?g=0%\+rj0KeY?05!&-F`RkOj*=nj0M%n,moQc?5Mk-`d+29%>119&XhUCg,9.oHhc:a[;T,DHM@OHI0ZU9A\T[I4r%_li5
LIOHQ2i%JqG\r@RbnEAZqcooVP]k:p?6tq?/"ZT(d+Nhs16>FgrDsW^D>f!$]u0D'4LAsL(k'QabOOEUB.4M>5r>7GhNtmiA*=ZEk]>d`*3>sC]kId>#
]kX<ko_X"Q85t-SR*"X?0]>%)SRU-\;40Y>I'6BG"b_fMEl-iW<D>*Gdb`GkjRn?=qd\0IQ-c&Z@V6q:ihcO=+G_@1a!-aJ$QRZs=u;9Ri)URNKbVRA+
:#()Be0QCo:7/^R@%!,$G##.(*MB]MJZdK-UuR,$Q+IRfc?57k^==1,0b2Md[F75(l"4mYNlJDW.F9/)8W[ZiJ"9r3e&`[I%tUsa$'O7GJ)9OPQ#WfOs
3)oY(Fl)[Qjh^LGB[TJa&QIQ,+/Nut5FtkN2KR_7e*0,?ZJ\:n23T3Ro,)u5*p3`Dfe'LGTglm[mR?hYkJX7NC"5^6WlU^q,);eWCfORB?%SVhin>AL%
3,Ci0Gjh:Wg!`&#Oh;=t=DI"FE'o6%jj(Hsjupb3#B;;/7TrOV):!_Sc/"tqKYtV8mor<]jciCLr]oUV-.ern`C^A:"hBQ0Z$61/%8DKXfpB%(b`?$`<
Si0Jr1;=*qPKp2#*TX."Cn@k'lsRu:4"4FbLP0&.o7Sf/t!('aeD"nW$6YfXRI@r`FAW\_K%t:=m&r/gGI#Hn!m?*>Jn",2l"\K.$_u^%cU=qS?c*2k"
HVEV7k^KiM<4%;Xuf'GZ\6_KiJj<[YM_+_)/I)aKm?3_"Cq]$9;%A2K&iJ%4`d$25Ng:?E:pk(Uoa]A%>JaD`mds,JuYI2_&:oYHtg>KH.ep<j7#VC7'
t:`bB+q</1]ej*_<q!42P]Z)Go&5f4*j(?=Or0nVs?95tBu^S4f?#^U&K2;pl:*I;oZ;F-r1GD=B]Z(T=Ik)Pm`hMg%-])g4]V'\@h9T&!t`?l3</*H:
'9*<^3AHHcklp&CP\])_^0]+/mA@r38p*Q;#UuR=/379#L?jDiQ\EQmtTjM=7km@Y@4?Z<MVlcCrP]_Kh2aYep<5m2%50Ns]b;9?4pHm9N4+-noo8hVh
)!qLS)_HbHrIutdO]ZQ,5c_7IE=F15\gOqZ*L;ZG-$HkKjj?Ue2tgUrpOkY16>Y3;Y^7M$"J.-s=CWPTdK5=kqY?6Ik;(cYh<::&"aGb+:.m_+M$6(Lk
Q!A?i;0nC<4"W`^^>A;"5um?/'p60Dr]TW#QP:/n_1sS0rlu90Daiq/K"O15FKh.cjtO$6<AV<6\nT**!DEL-tjALgd!WRS/[S0fk<<Nr-uG;'-V+9-Q
A]=5R"`C2VH1)TTtt!7&0CB%Wr-Kq&W/.Ju*>qG4#p%XRr5RHn5iP?A.=6"$ZR6Y#0V\Bg-eY5ii"@bX&ka[:\`/-uaR^ZGJ/s6\e6f>H`0bn/?,l8>Z
jMMh<E!?r?8f1il2L0qiF9akuqXM!aZ_V;e;2q^!OIWtGURr)*js&K*+TKs&?)S_6KjkMV9LN/=A@EOk>>Y_6]J^mjH+KIgED(O.\BZqe@W_T9^M,M*Y
8mbsQ06#3(G<r6co`D3XN27S<JQRWo,DESl:LI_"S0lnU,2mk0n=-!"LU'CJZ$FZ'IX"04%kD3]?@ZNa;PqmL5<=Sj6M#:B6%E=Wt";4p"P3)$fPL%0Q
i#n@%os<!a4]Z+WU78:6"_l^TRclLK\oqt>.8udM*N\:uI[OPr[YYiH&0\d%TdP?AKD`;>Xg$Fkg^RrFao>\^.T#90#;dC4R:2RDki>bs"T=7I$W'>S7
S-P38Y?Fqgi$P1j=_a#XS(*RnkIT3k2=V18:2s!A*r6Uk1WAA*KgV_@A(Q,\e!9fDSnNfd.jHT9:F_5>,OF65(N"Mq=)!!4o3$+rec`HB/Hi3e0df7:V
+$)/,NtYEgI9?^8;G'MPN&iJ#^qeF/Af%icmqn)M3_T'KRV8$[oN#QeHAuZq@&V(N"q/&hhK-)<cuIdQBW2XGGi:GoKBUpcUc#CGEB:r[sg<L[,BVp/O
'.F^D_Af$"\08`i=<[?7Le6U#^*ar-^fA\i:EDu.!t@DT9M[u;agFUG*<Asb;HhS`r+//aP&==7lE+rEm4ka3op/qrO1[)C'<<e5=!8tk^u<03ZfIq1/
GR%N[YX8npFpe@SCmR7D^!MZ36bX0I6[d^f-HtMLkJ`7M-MK6k>]>S#uYspH`[Er.q[ZB-@mIW3J(#U5_&bMC@H!GI*?&(r1Ei:o:p'GXHKl3,uqR7PR
0'nOmJZ4Kr=`BU/&'@OHSiXM-;%0^)c"d?;Wh5IgLBic6O&SBtjK#fk+>cl63J@oP)s=[<=K9N3ph<q31N2>a^>h$p4n)JtK"AT]Y57*"YO%q:6=7k5g
>eD]IW<&qRDk#QQ51A(]&KMN4#:`cVLUNA@%^runFMG+YPZ*T(J4U9N+#VqKNQ-:MpU$.Qql1G?`9cJ%@E$@^WIhQ[V3RW+Ku^_Qn-rL,VA=NX1g\FNW
7,0c-M/kKpPI'`/^&))'S)YI75FVWX[A14.PkjgP"+,C0)=sHRk?]BE<?^`XSWKMJC0]QPPs[]cPRef&jNTK5O?e.u<`^a>NS,<SZEu(l,R)AID&Dh`T
Z?o'8lCHkV*_Y\,fMF"''Y6#DIhkjWf-3iV(uoupUZPR3c>[O;6#SNm7kiZOlV8&s4"cWg]*74?n]ZpGM@,i##Pdo<RaFaaP&WBCnJG)=oQc<)p+O^Op
>T!">O"T-XY3Qm/="td^=jl/r0na8gWJ&;:%bl17=0g.IYm6ktTHH#p0B#o,CC%E.i4//C#b)7G9\PuWY6H<%VTqhR)hWY$_9\Aq4JdB$?iE2PBBSR'%
e:$N-V`#f_WlcN]75>uqDtn]oKnfbW*I6]O<sYj5]2MM'5J*ZlRK./Sj-]uC!H-ZbUiGm">=M,>oeT;g`-?k0:nJlj)ud1=\bg>=5c7LEG"tcoekWbI:
dVVM[#jYM8_B5^Gq_`2%Zls#Qc3-Ul-1IZnBg]JUsjUpr<#]7nZA`?!]'?EiDJE`r9QW\L^:U^eu4T/[#\Eb34.-_2\G;S1!Bu4R#EoAEuad9Lt%0s>H
Jmj2f5otY$LT;e"j*bKt5+[2Y]Cl"Y$)"[LQ&19'XN>#R`1pU+H8AcLAV>A$d[pSJ#Ij9$jElW>SpTh?9".0?uAl7fs]<K-XY8PSu)84o"LO>T5)=#R,
ofddN]qo>s-M*ia%[NtYJW`3N?q\NYS89*7&.A@E=In.#BqCeaV$=2_Whe-+B*ncLds`ltF]an,rH1i"FY76VILEPL)Kq+t`%=QNLA]CQl,?)_!7Fi!_
C?SGi@ndnr20E@cGd<M*K2Ndn'@WRC#a6scq+:QSKK$JA[ES/ju(*EAb@6PN2\_2os,:hQlrp1W'j?h]p33gcuJee4#KO.86-?C!ol25:no(%CgY=SD1
IZMted+ZkBNKZQK86Zb:@BDG$;A*0!C?4Z1U1#Ijq9KW5=Vp5/$f6bpWP/3;`hP@GCt()p7Q]@eomd&S9hr#4GgJ+_>*a@+SMr1V,BgASQ[<H<s$KPfm
O0mOihO0e3T2Kr)I[0j.<m7[.[;**WiY9sffR+Q[D)Zl2`U7$jND^SK"="CJ4fPCg[B)s3HP>BT36%B9'gEha$!,BRNGQ0eCH`>IKmEU<hF;iOBgk#<%
Z'7I3)m<U!dqD8++.^BS5g)&`]87WdJ.VLGioV<EfcB2,g(ThYHFQ4(MT1T7$N+J>tloO**Sn.lR2nLHJXIUl5uc1`RK$MRamp%<fbNnI+O<dE,d+:f"
Qil1JB5(_:a*>%"[Os0?DXgTLfjd3T/![kc@MT:1X\;qc>t?uUems&Q$;nE6^CUX30;6sNkGFEUnC1?`;GqZBbhmLAg"<*aVZq#72gjMcd/,?:2kNnd6
?51<NH)VY%0aV()L/QQULh3]Pm30<mQ6&@]&V'p<%+-E^JC>>XQYNj3r*ELojg8Xs0^]C1Ud$q;B_Rh.q4=1S[>HH3,r[1^ZF?7]!Bg\aDCor,besg&=
>k[+17IU3+SS+Rk1J)#Eq!*_@_U@5/Z!cd2K57B#ai+?SK[LL63cB;]2lAHYbH>?#k`K[Nd][V2'sDoN#i_Og#;H<^`R8`Nqh8OBA>Wu2?e]3Jg<Nego
cO5(B&8St.?"RK8m2"1s/q?;1]WnC&[]19oJsVND7u:Srm`q6Pe=u_e79E:0g/gk@t%al@obEHq#hY;cq%$;f>%t)!^a`!2M/iTVi*:$c$q:/7@c!OKT
VDuDZmFI7&U'NeA9o/a;<P;PnK16jc2OuKQqL)d/ZR1;Ie<dLb'O5:.RWs#9[WBBP`X)>]!fVq*>.XO\Oh,@lff4,9dAAh#$J]M6#`I0l>+nmr`Vm'XT
E!c>p3)n#u&_b+M;QQ*_u-\doAaGfF2irK>W&RE?,m'1\X6OSaNG+Vm;7$=9uU6$1l^Ia4\<k"gn4NJNUGb0M_<#Z,lrGsoT&c3"q<`sp,eR&JOEM^aU
hC(;!(oeklWZe!HWd0kot+2bYUWFU[Qhu)UM8h062+JJs,-\E`6AtSQs="]JZF:1Zo$!/hD[)2b?p4R?D*I=:][g9!kHH"nD]^gc[dP;LnO'r3c9J^o6
h),<D^TC^#^II]56Ai?qCoDCT$:2K%#THE)IS)a_cC+?C81^=;U9Ze"G^0nIc"t80kk_c&89Jj>#2f?_@,Y&U;!^elc#9<lmO*`b`ab"*>..%5r1mW\-
O/XFP)",9O9UY(^d+1L@UklT3nXt'O?<=dRZ/?1dQF>bPbIbuW_\B8(D1--Rs$=?46UgUVTu0'CP`6&'Rc(lcS;1IW<dUqPXL+cnd[*97oK^BH_1USdD
5&i2-epHG^#TG,I:lq<f+SuelOOW>6!:?3BKnBY+g;^&*^!K)3V2/;\fpEc(`9RjZeT%O"I<Xo9f9/0aK?Zq".BTYStUIc'JX6MAPZ2>bGn$cWZW62A(
Kg<m];r3XH#RR-ludjA2&`LP!UYFCS9KJPm<rnc4jN<n=IMds7`e1(gT23\,[Vp53&P&=$A`S16<q!On88s6F00StV,i4YNsd6am?;)Ceu9"Ijjqk2l?
i^M<3M$V7S)b6hST(h1Th.$%O+dAMbI3tPD#Zl0s&?6aO);#*nI:"V#Oi/aQPn7gO*5q_INh+rPA+f@JM,SC%:SJnW$'>lBtM/%UFO$DEWG?Hi\UQXKX
WV\L1k-7/'*.XF+DLqSWdhYt.AO<:9*1[Uo\lQhUc?706-Aoa.1d7"[>\Yf>%$X;q*oLl<=D)q:"#/!%3IKKJ41$bUa5tQfA)gh1&=<7NEP^csY43C?l
:/jX6Hq-oqZZG9]3*.j4q]Q80S^_bLs*S3D<V[o:9K*t#2$b*bTrma`7^Z)me.@l4@7L+K+2#9lbfRMrILP>r1&70@:o:(2&9W\McS^KIa#J*9F9bo8r
N1O@Xh[rF<YYt&Y01>,F,8*dd.$\+'6eu9b-c/h8(O>C8+M^^%;X%W^Xi(bUB!=MHpiMVfr_&\WoE#B[kHiV]!5[%Y`$;;85NMrJ/*r2Ua<mh@hJQH4N
M"DRU2u1FAKn?);,+;OMjcRJ`FLDMLRn?K50Q-7h\^![Y$3C(b<N>$1d%%Pc9P>f2ur2B@8MZo]WL?1.kNlg5L?m$FYI3a,$hXJq.3%E.#L'V$&/eBE]
8$k9%[9uh6QV[DES'O5-[:u&nXqOh\U[9nBJ-L3O#&\pk6A<e(MLZpNP\3?bXi\@!Y9Hlm1#Kto.<UABL1&'ei%<)*Y'-)K!g2>V-g)uYU/BT8?J86FK
gkCd1p@CKdb]\#s-M2Q>W[=_']J<T()3oRB%n+8RC#JFm)4b\_M^dA[J,(pZ9tOp-IDW00eP#_YUrL"3,$W/ls26ZIq'NXW&,BLtG;cG:3%>HSX?dme$
+"`M4:M9gN6]M#A34mVKH=i3+re`"Fk'[1a4t(lJ#%,!UfCLtr-jo3nGZY)a3d:m$$<ihmD1D2kJ:Tbffn2on:%]f-0=h[$')B1*Tm*H`&qDnb#>2Z&\
t\?e`Ec.\#S7KXTO#&m&&eO$ZmOe4qNa2Sd9LY3n3.iB;VX/ZB-3c=I\2i)t*RhL3Nl6T[PKEk"2MOZR*MrC'-'^ra-VF(0,F.@s6`I>H`_CdEK5acb>
n[R2.dm4#0iJ=cLH+dfhjb.TPCOE"jid'8&+Rs03%s_KGo\a#;g[`Qa>ZHY/U<-+fN3dMJO.[OckZ/l1\6r@ArFT;:2j7?;;tojO#K2sg&(H0j_]I<6b
>HJPT--6$'6,odZDACa998=XBK3l5qhQnl-acDZ=b2lr-MhgH,MfG9:F$q`%U:-.un*F6o,W5c![gXRCme54r(r%Oj.+2f6?`!*M%&Rc+&8agTVo)dAt
5'HH\UBFi%i<TlB/YL`01B!"04t:jY.MR4fR,OL#.L\&U4B934k;T*K=C743O4h39HlHqF`?7T<&]JY[Vu8n-qEpu:X1+>/+b$^=!qd;\'BdlW7cD1O6
CVhWR;87ZO`Um$$thPZ>ZchY6h,2rh1_?^<YAo5!pYi"m2Dlm&Eig9ed0u)_FZe2C>R[HV!DZL6foMsnBo,51SCt+d"hDT&/u(I"^"Aa!IeF:a6)J]%K
r*pW=<Pu.u:[-q_jmA#@#TB-\]M3_FUI6=FKFA3m(@b&^,_+c9-i!QN;g8;U;Dt/2=!QZ+si8+GIaj/5d)PJ#<HZ/K%i;q/?@M[>"G;oE.(F@!uSnbLF
D4bl<[:f6`=n#2Br\Kq"BE@6>aQlGJpkU']n8!DDQ&dme92,6JYG'W!O7#!K^]7]am'HEVnNc\?Eo2(LQ,%^1[=ZKKs+BR:>!=Ytc;f/eoZ9Yuc>G^V"
(eVK(=ZBKhr]ZleopS>4;\:BEm'#t#Z]YOr`9,i.Tj)_4@/[&NQUk7h0!=^1h=ILq6,3$e&P1ScP`W6a"h[+C9AoRQ*A+@:[3*c.%g9,U)0l^:VG:h?a
dV+$eepD:)W%<BR>[guLTY`W\Zn_Q5^)2,g"VjCSGE]%9A$sBG*^6RoJPf:po+jej<7=U<<*fVGPPrgfs%m-u9=c90YV'3FrWNWXFDDcsA=P+)C5R9XV
PA5"gIcp7"j"i"K9bfHJ^=rIE&iNM]1MU/[jj=ZX6.S8PIYrJ)FWN[88-I6B+AWlrV$o.4O^3lXjQ<>`+-ngqQ)`:78a6[rL0FWT9_KPK]m6/?8X<kog
"N8qIAlj(`Z:(^PKT]g+R(>eTE]9Juc<TI#0LQMs)<O:O?rK0h;je<cn]:,(7EeE!ruSS)@hjWi2^I4d">N7Bi:q^rk'lD:MIB.&fTuCW&Y4KZ+XrL/m
Q&@1T#!7h:f@QH;#V[B<7$b^!dZ*n"9$VYGhj5bq#'lNl'S9.f&Z_k&IJJ($.r:k:Q3Rg$n7HEkj+`L6*VVQSG+"aaA@SakWqTIiQ1R=u%:!8'_7qpC,
U^@?gi-N>_NDb>^FL!edpG0e?0Bd1:38@)[TiK4%tk+NZ:HLTn=R(%P2@\ZqWK`Bsq0`WN[kdIb&rqaZoO:L[PP<:N.QYn;j%dG$r3uZs+"CF^iL9-MY
a=?XM'tV[7/'+r@FMR$G.Tfr6Z#r@c3MZ[fFCW#V5OC*f2jFm;^""&GCT8A%l8J`.B]u2)FKLf@V?fN_I5KdfCs(F<KPC`iE6%gDa^2A2q^Q=!%3;aD!
C^De24q%"q-5JN(:*N/31gp&GFp%NEH"2!C.\>>M>/:%P1c\j12p=r6W>]$W,oK^XtUoJ^&V'X"9AlgO(!.LhV.JDil;n$f6eKp[2:+mg#V9,eTrU,fV
Vi(NKPD%m=Q-^U;V$RS&p>i>;`/@#Z)UQaK[jg#-6iZ6q`i<!],<#ql3.4MGO(Yrft5:E1lDiBH^T\\k:>:*(R[p#!>UA&ljMX=&6\BXkFT^di5,ec]a
PK'@^=4&hSY&SkU!]Ue5\M,5E@rD(q"iEf6Qd_0Aa6QHb-M#`%3O%8sRmK8Ckl66N["m530l3ka181(.e^IgO#.&h@/A.nXMj\^7Rc*L(S;`%1o.BBpH
5nW94q=1]Nlbj'M^CBp4W5L&"*`<''**T)L5Si?-n?cO82!l16'<'6,.$S?serQDYc9:+*WaJ&E4%M5,E7s-tSN2[ufcth3e#T1?N9Hrr(Ljt@O0nku2
p9>Qfrm@Htm.W=_5Z7q.AG*mTZR0S<7L<i^RC'4T1SB+0Y!iSF>16W^:<36s+)rOMn!hbEK^n4D=`4f(^sbJ`@RD5;.+#CD88Jb)Z++lZjB5Z#/&;9r^
H2,hV[l9@d$.j<-.3P`\H2l2hY@AAUXse:D@N')V##9[-a.c!oouW&C_40YM_;16>=>uk$/,,#@1D*l99eLgfW+$Q3Zp\3+48jf'4i[pCFu(2V82Nd7:
YKagFPd<743>a-4#hr\]0-Q%eVJ_4jB#!W=2F?W36g)eN[RO/^q:On!FlNEmtWs!m@2u9uM3%5R9$,pTajhQ^ZbZj`'c@BM$=#4m77E)Jk]pdZ/c;+!S
JMRn8@$>0%=@J#<D7KNKgiWK4>3VVk?2el'"D1ME!kd?.4PS^;?dAhph>ge(l_P@9aP%J.Cl!u79d4ZZ@>761c@\Vf>L;Eg_)^4SC$6_WZZO28&TG%Ll
dBCO%]WnJU!+e5H#7"rlu;'854<@8][OG7n`6%O<<^#a3Vl#(DA11qL+QX!5/1kO6:,8P^O`*]`8#s95Ee%$tM!Pn$Ibd9S/YZ9H5gS(KLUoV'2=qpX<
bB92YEE`A<77mt?!D6B1I&II;deea3q:]V0FARG`e'.V`XE@`AqH+0B,@*WA=/lel8=SbK!1YO@V^WC(P9+%i'A_b(:1]p]\80X:\WuBghhF7.cPY>+n
4]o2X\!'n_E7MOR]SmnqnsOpp\cm,VbW#hCF/I.4V8'c?\9B)ckgqG7$%_[VYW!0=;EV,DSGj(VsGpQZP$'")[F86Q*r6o0<C6=4dcF4Za*kQ$hdlKXq
6olXt%P#r&i5tTURmhND.eWi)^-,YJ(!YC_Jm*e&R!WT\geW1"CT"H3i[A%dt&&0Eg)n/'4Ge+'#3&4aFA@2B$p/^gGH"`r^M/Xra9*3GUoP1HB#Y1L/
"')TIMhccU>QUbrC93M5c]gtRVD^lL3Tm4huKOWfH%Nd_pp;mTp#?I4K94F@;t5k.9;d#Qp5>pCd%,(=8&:S"uA;sh6=3]CQAqMo,SMnFn/lc[_u>c7l
U+m+]q&-#q.p&*Z9kAOY9'=?dEi5b_GBgiI"e7"jK/R.3K2SERZI-Dt,FXZ,+?&ak!cna0-8i,r>.p5927.kii$-9^;B1D\%^-`U#Y&1XLa*r1"qEM6'
*&c)BAJ=43mVAH?3aT`?3okoNP/RdlTM%q<O,M6j=':"hkPjL!6?rX3W)&+DA8h#=6ui`19m+McU)BW>E:TC"19XIJnoFK9]rj9L]=L7,"YuL.T*%$p+
@3%G.`GloE.^u9?8j$ceXhIK-%2#-^MOBTZSZd9.*9mLm0g_EmbBCbChGd%,PkE_O)K2>:=oX>[7nG3o/I@5;H-b"r`'PUk[FabM3I9Af#E0"V^NTdop
Mhkg3P/tjjjS[4IRG`j*JRja"_99c]8TPZ>k=Z`(E;nU+FMrB-Jpp:WDj$^#+nD"i`=[m*>,SDI1H!:4!CF<?<[Ah!?GrI]h7IZhrE*ieR$H]\0h`K"c
?=Z:,P/h'da6T#LlFT0L[;QYbXt9@CF7"t+38j<$EUJQ))[j!8M3Sio[bc+Np\r#tn`-oJVm+6'.1T!qAknel=ADo!hPnFO9,k0G+TXTCB>PA&X(f5oZ
!"%VC(UdXg7BPZa'r2a]j4Y%cV<T#N=/C]f[8!P)2;6F9+?h<ATogNmLR/PnZ;e'qL@OB`NM=bT#Y@p`%+mH`O2>BAGP7uXnQSd-c)kI?F?l,j5oYM#!
,dIFZf`bu!<t<+FZaAH_TtIam[7Lm$,^;r\>g:26G2@hIM^ZjA)b28F7GkI>n-b/dAisU4U0"q/XqKp?^,FU.ZNTMKnM-T&E4j"Egu1.?P>JH\,N*ZTA
b\?_C_:dF&RBfT4JZ![EHi9E>t)-9W]>Oq4%TrNc*R_5U^pW/$CQCQ=,sK3NWGt;k.>+RRAe,KYBG6>EN&<0n]/iur"@Z@H\)al*#e])[pXlWW`!?0aT
"oq/&5%%$#),fnPt6c$fgR)/r*FjDU&h(?#fO]05<:B-WI6rEo^OekRBPA#5eddD]m@$DKUQ'>DV-A>FuX[]1.i29dgGHM\j&&aE4[+]"4.sflC0XR:*
(HiF_FB9*o(0bA.S#'t<-/_A7^(hrq:9F7_dqkhE[`E%6ot(F:QH,"Wps.V6K4K&+S%^i$FC;EM*75d[3bI?b[e*6(qcOO5\I1ep)2nQd<TnFKdt&n^#
C0(gAT\6tD7E]PZ\a3C`DDf.l&\4<4'7J^(6_c&bOh@+-lRL3]cFJ=so#k^[6^@6FF],C4!^C99$k2Lit`#gK3Xf[d.^ToO=Z,cXLUcIFc,cG7gPL%ni
UeaW&:fh$^c>PhW)[Oln"WEj]8i+=FAPSPpg#b>J.hruNRu^KPI=BD=jZ!5If2[=p4X"=B^i?k-g<O01,^h#U%oMk&D,DdX&/EeCNM#5R;])#6O&I/ni
W/bX(Z/<@r16h$T[%N'%_A]d6IVO[B]^&#U4XCFM"3D&%&C*a?+0>+Og982h@u@8SZkATbuRB`9CJ)i`2$'QXo>*_6!s![NT%9b#']9+gpS[8qaJ9OCt
i8qJ80D7i3HQ>"mssaF.7-'HSC0!A5a"kY^,TlNb@>*'$[8oV_iGT]b!h'%,_se:qcDBRM"$0Has]T7m$f15IhXS"jjW[kar0^=K7&DRjue/Uh>dUMok
l*Y(h,.SfEk(AAW.-i#LksiV-Yq*eeIcq:`lb/C<kb#=83XKnUp9i8s?=c#3r]eV((mYhO2))?"J7,h\p/K_lqV9RY8l"80UDE*Hn[F[Rt&(OD1s_gL"
KO;`&Rj8BR[_TP_$GcTN+ggSn]hnb`i2e6tNpl_\:J:l4'Gs*LH3b`8k19BAOa+&BlL_/poO%H_Cbm,]*qKUD';LsB)b7i@LDaqlXH-MMAJ'gViAQ7R"
;:r=.-[*gJ1)&:oYn9dl':ja"UQ;:T6]hV8p7UJQNaV*6GKC=j.l,V6G2@HTEf5]a:UYt3b9AT4eWF;6rN'nQ$pDmjl%4SY#Jcl?QfF^qE`=`8MZ:OCL
-@kT5/W&@MQE/]_u#i,JY2O9c]7-\*"$GHi'pr#*/^HE1.RQq*'67oPU%u1fW.f77iCmJ,r^+1mj\"/6#m8SUKuq\"9/_5^DOgtW^1,!kl+[o3aK*lg,
;/)1:BR#5+d?he^9q'"ko/gM]iUamj7eAoc[k.8;'HKrqpFb+QlJ9f/8\VV"AnmRdcSO$pVI@/ZX>2C90ZjX=cDVRTU$<IhGYq:KP<!'V#N*nqU5Y5s<
CLljLKdn/G[02Y;;Zfb)uFOuhq=\qc$sEDpFlB-pB>e!O$27\5n9&2K)J(]Q2$L'Xa9E%ul"VMoUO?M8UcUtV*ZciI41J!C/5=+\@i&MipidHI&R`WN4
6,EDg)R;^Qe&2cNV!!2,2!U8&8s)4"iZ,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.37'
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

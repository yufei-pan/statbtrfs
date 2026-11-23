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
	if tuple(int(x) for x in multiCMD.version.split('.')) < (1, 70):
		raise ImportError('multiCMD too old')
except Exception:
	import sys,types,base64,zlib   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
GhUEUl[%=,Z5EGmI"h.sUU=_8&4)bLkI*[oZTYa/7N's$/:62$#,+Ra6;.tr"DM"3UO5'LaiSg[ofI)4?JrIaeruW8oaLmMH"N6+\VNMG0@eV'e^`4#<
PSFtiMKjC4NeNOZc*/fH+gp?(6;Ypjg&!j]l\\-b/VnD]K0D[=(N/,f@e2l*DMFe4I`GD@Stk*h=9/Db#YQ3&`rN>3a8_E@U;Njj7Pi?PgLt=ap^'rji
'@Z#_+f!HleRKq-jaslS3chYO]YX<,U!IX(%6WAQ3!&&VGWVf(ikmX]OOSFuGr)Dp;>%V70\rRC+Cr05&62)JjiC<[@a2q#0X44hm8ZP)uPt4LLb$^O1
>!2LYSsm:"uroFAV#o_Y238!nS0=Y-4/5sUj&ffBB^I?lPWnfjRg%sI]Ffj?ZUB)=O-8$C@-:]Hsaq"3)I$1smk)UB5+ic4H9qWI(3YZQ2$:W)tT-qW?
D^DHR9U@6r$IJ2.Kg[ra_P#^)('UR!jSd#,XkqEtR]@56VW#``^+*'PnnJW<mpG-.cG,P.]^+S122D-A&T$FZ"N(GIde"c)U8o>tqmK(=Z4IUs!_TN^a
bA7@"*9\<YgK+1=e`"WVVlpW'VpCB1*5AMj'7B]PZW$WHMuf0,GL)?!f2(<'R.0loY:fCf7GsN%B`Xj`SK+Mo-2E!P0=+]*FHX@%4urI<;O$"VpbGJTI
p&$37i6q%T>J&ra3P5k:=:6@*5?i+6feuu<?M'eq!&CS+.g2<r:K*_(N5A+]mNRH:s3W(RNDImn6*&pL]gq<;FPl_jXF0;neN:>+Ri0eIX$;5qTt;mkt
g3/r5B3,e&CQ4T6V75EkG_^!`a=S`q%dDTAVh9=)t6_\klW-r;.;hl%7XX!`:Pqo4`_bIC^7ompN/D3*fc75gdDmGVF^[B*i3@JdX3*4sU.SMdl(E`V_
%$=W-iB^=6.Yk!b[A(S(.L8^@59?hH^9"-<l6(4\oYhM.XK2T/*M]W1\Qc/6m_e$VePnjL=GbAm@7/dbSNh2C<+5=O-!6E"=UN/*H`Vi))-X(%2g2o`c
7kd/4rE(AK[C\g2"In6I4A0#X0JW&Wj@PL!G&AmU/s7:Wf/XLOoe<us(J4Cl40?5eSN>Lb\^c:eD_N;?jI@OikFmr=QICNGqX6:)Sq'MlW:g1j>/([^-
H/5M9n@QKNgs"A1Zl)653'CZlAY-\ZR/rYk-9kk.ShBre-fG%UOKnZig72b2mpe'#eFp`%9+UnQj.(PA-6IhB"K7/I"J_6RW=RA]WTm_gKt(;tlcj2'$
0;2I_FOAq08jQ<qd.\M\d/6\#s@06cU,G;8\P.%)pR?jKc1=!fmi3167;<D@)<I%m`9Wr^UsutHQPSM72Qd#)EsEiafqD?&ReV,Q[A+"[Tit>1>:Coes
*DPLUA_ig6V5R!hBZ0\PV`'=;3m#1Vc5N"$6q.#e1Igj;]"B<_gZXbR[(7%6sR:n4o1H#Hdl/TAO;'Zou5@VpLiGH'PRaXZc;DDKjfhkOsS8jqd[\?c3
M9XEk]4ILiZr.b<JnS&LVS$u\q6k:9Y4MUf*WHT<]O\"G*Yif-SaMc\"-i?WNI`]:h$n$U;jK1HIO.cZ19_GP'J'J$63G5rqA/G*I2-9)sTp\7%s#?dC
IJ4qm)Xb:-;8$WY*`Bs<+@qBqR07YAcP:XeL)VfpPSg/Tao^1BtVnacg4ah=5g_eW4p?g8.aF6:$GDkf_XY9f)XlMG_9$#s8/O@5cV,Fp_m1CqY'FRR6
*8[mg3'Y:X\@el4]/-nDH2\s[;;`me)d$sT0Sh-*d*$4gllVk6H$/meXdFo(r5u4,3DbM*(939s%rg*tYVPA,1^u_$RXo^,Gr]2)_\h:Bns7AcJ.d,[j
-66tEZtp=YurHlOa`"8e?@X<-[W+/JCOI@[8'S&ZSK@mW@"GArAoXuQI)"a%!'pDT)UC3g6JPYosOBd[,n1+JtZL8_M"j7icIe*+M.fNUl<oY<2ZV<K"
<o]BrlpQ,ZkN9lTCY44VU,5^_^h`OcABT$@IJ/q.:9/1ZMS$nV\Y[a%S8$KV<u!=eLL9\F=<QD\!-s:r@W)6?(i_F;qWhTt[K+o[sScbG_o*$3W3bNat
udN\Jn*+G1V-&Q!*GYUS4U)cT+)p!=%@?_jTFR>u8j\CiIn6`,o"&2AXtT)Gdl91*Rr!Y]>U>EN^(Ge*qG(?@ub\Fnb\n;%Frl3.>[FIR=DHHbkD@2gn
cX&Gumk3+TB#Nh/(`,,L7Y]8C"@5q]Q;lk]M&>7fGr0#:qEZNM:38e'5N4["G6Kf,[]5&W;%HdI1/!Jq.:EV.#fbeu%e-g.D[G6)Ibe'QH[pcoSF5[/&
a7p75A<R\CH[tc9ZTZVRXsQsPdOk=,*I0U.?T5qb98+JpIRBZQ"69WBbn3jTOg9[C5P,7H`gGITr7LVqpo^%iiH_te0aR7P$^;SIpE8g;eA=97GQ1$m0
.9I"[)O>SrWok+Fgem*f8ZP&As_Q>7Bt!gNU$7+5H/*7j(1(t`tt<*UT&GZef<Da<9j_#c*K,qnDV0KZkU$rOTZU'Q"jq&n[ZQ\Y/]q:6uSg308dkuc2
7!7G<G]e#)!JW.*YP-"]Ee](XDkf`3qX`q6!8Ri-;lfA:mONN8j1gJ67G&;GT=/&FP7FOthd=JU_k17p$r<g;Vt%JlEtL)nd0QCRHn2d0a#E#_XZ!Q7.
p;+6NahW6>N<ls:IC8W#r#$,X.3JdPoC3mWW&khZl=K.+9(\pY1oV%'n/J2uie,PA<?D*nmk<qJB93Pr0"<$*&IA;!Cg/bi/T#W&p;PIF?F]EQF9k\\a
d&Z%0Kaqs;22TLXtb+0us*AIX]]V/kH8EDGp;^s7#THt28^4V.t+(M:4lVS<-B-FD<oBR6_l*Be)<6TIie],$P`"bgAW/8B6S+r`eF`!Fcf#01lJ"l0e
K0^W3'KW-qn.38XL^?d.4V="U'GV9X&NhM:@r0f`LT#hZ?^acA#6_8f2BBC4GttXFTTh`<,(Z?O`)3n],N=h`0L`lVK^oD.&Usj2HB"9r^(Db9GaoT'P
u?KCeY/$hb[@g3K+IkIE'V</ZO1,T)X(9oPcK[9!K6#p_J(O;pu)uthOO)YYU>UaC1FBbfJA3or.#M2$IWE0A9=0.^qJ#a)P@]k-0XSe(#bZ@_?5d@IC
O"-B]_$qVF("&m#n;@;D$GW0[dkBk#%iY1-M@oORH4;o5(kdNGRQWj,ZKE2q()cGBB</eOutTTB^5(;kq(?)"[;+adNaQJL5r0=q<kbS/:KH9bTbQg$;
.WMK9S_Z$5smaM^Ta[!t$<;!_(X7H2@+<kb[E5aqRL[]jU$#.!T4((igo[UGABlHG.*Ccke#Xp+^"DnjE,dBhk_hP>-`RQ>9ki[r*nMqWDq/KGF_4>oJ
\WpC?6nl/61[2hSM0:NKB[?t-b>\'&m$DRF+Jf(hY)T%;AaeOkG3,gT+gBqDOD`/!i,]=Cpa`rBE+[T1MB,S&ce!CEA$)-P2o=S>Ra4EBU`&S*R>NEV#
2I2<G`b4neQ6=4!MDH#MUuST=4L_YZf%J`^6\;YH^)F1&(T^D@kZG%,KE>p,P<85"7JikuS^iDMQsosc6M]p$1Ro]"(=?B\4JKrl`pem;EUSG"_(Oi2p
+!0B;<gKMnDO]u?[^:Y*hU_Zr'@H=/nN9/<?h#(fW'UE!p%6A9enq4l:R=s`C$V>2W'`8el(;!N$Z;5(1g!u-@(I'dRB;$LsZEA(F,]oF:Shr+=Zj]JM
NFG9J84d)/CJ!_*I?+>akaA!o]ha*DJ6B]C@O%QW)e#@ns(XesQ?DYpZ>B"_"U77Q%]L8mhl2,[Yl12oMtm_TmUuYoX,1&XX3M@SboobZR=eUuqQSA%2
\!PR$b&N5I,r$k`FS7P[Br/70hUN_o88U?4D*LusOJZ<UtIr*r.d"7md;)/^W@X/@<c%FYs\Pb_EUh/n`7jZBAY";02._jVi6@^ut>L'a>P)cQ,r!;B8
jI[ab]'5VNe\.,(anEj`cD"s2i-UNLM1rmM9lQE!SnX0rV/h47][a`Hq>N$ebb*pt>ZW!,D@PNF;<>qRSX=VET(9aYGfI)Zs*4:.-VFLk:VG-48i2i;P
-Uqt2FIL\jciTd&YWN(/)J?aR,bVS-F?5/9[^"+9IJbpfX1-dJH"LT>9",^SCo(':',%]4"L<DY>X?X&$5Xk''7@8=hIhbuq3$"uoW2.Gpt5I<"qWM]B
jODO7N3@1Ot>/*B*:dm5Ma5P=+>JkK"`.4"9Dr!.7gM=Z;jnV$ZP=t#rM8PdJ(\+6o:Y`0!g4QnJGq:"JJ$Odeh\T.5:MoCpTGAh0%T)9&CUPI=Cr<rO
;6'F0-5`[VYG?+2<&?pu[PXotm>j^A[ip21FR\d;gX@$O$9]06PL?$8.84gfKu&3[tgOk1,_)Fg2@VlBDJeELrM4)!2$]7!='e_MQDiPY<7b?T5LtU`q
;LjV8e*4U8+C1qY;t)Q7@i)g9ZO*BRt98d9!oI=To^)6)?rUS8R)7?[9@hX5Pl!B"jf\FNK/A?d[g3N7=#$;F4g6qOD=&b+UFUBkX2bNm..n7+B0XG^)
RiWHW#g=W3>1m(A=gXW$@07lePjq?'`FcF!<=g,na8"NB+ZHlN3EADg-'_?oP>U+[8&uefna?;qJXQ'u#3O,9bSs?B"5f77;fWj[o);#Uf(0JOC<IKM:
eS&noF"AX4OC(aneBhRUjU$P"QP164oN+el#[-e$E\PN.8*!sm)uZ$aJ3E[W!6AWV-*hrLKE)ZOG5U8g.(?#*-0?Ok<+P/ifS7'(d>qZ[='Pd8LAe*J^
J\Qnqen=KEjjke!!"XTQ"9=n,8F')DF$=ATl33)2n,JIO:8b:WnmjNTN8WERgYnfCm-a09Z_LKB/jDonYW*4d^ltHkC[<#eS'H_FC6IP1aa>X%QJVRX#
[N8-;6G[Z;PQb6g!Y:9YJ>&YpXna'R(36(K9pbJIg4_VJg8XLNFm/)aiVHVC;>]VK5:@ik@.#IN.]9PUk@F3.f\TR^7$>UiN%A`OqWSe(hU$K/j_eNoU
[!961e6B3u-S#b>be$"c*t&ukD@f'&ZtCr]-Gld?Ft'h_M$"npgBBJIaqnt&ZrG-$!l1o(1Fj[+R*$R/QOe,Xm]0;:V%V,^P^>!'qg-U5RNWkF*UF3+)
"(5iCQBmRk8,J203EEB+DJ>o?5U9;cWHW*5;-(1WVn)J.6R30B%k5H5Trglbkf5^=Z9-,a2C9?Ne5dVsr1(gbUG/s3*S>D%!Jt^\l4D+7e3\Qa]f&Zl7
I3>:sB".4;-<4J8X6[Qqp1]NYMJX-iaYd.e'T7+Ji8+22BA=T]g-:uGP!L+h+C<JiGZRN4,@Mn(%Qe)-0>f@iFm"I:@6T0<9UdJ&LhL0H5,Fl,N@IFe)
FO2hr)f@p3)t###E=?M%hkmcgpu+0kR_t\L["r/4PieU],,&6bFN8b<P%!QT(WbOUM;[17/"gT&_CR">(Q1B79H-bU#pmjCqOkkG=jIOU"!_Y6hnqW!B
qt3O3c&AnHgnh^Eh4R2\ouoO[U*ZKUIJ-8:L33M34j&jW@fn%`fVjTN%gS[+?bPB)sQ/m4M@>;D(>-P2+hYZdNh'l)`rC?+3m!c:<\P>`9B'%Vkgh8>_
6UG"W<5S]\j%Tp?:e'gem7L@K&9NLYie/U83'7Z<RHf%6o3`Q4@T5X*O-*e)!m;$*D<ZU?grTa/o/r=hkK0JumAC`PgF`Vetf:@1]CqIma:Uh?0E5,C8
@#+@e/q)P`KB;-_)%21ur^t%ge&^ikj\tm``@u'!QjRje_S&6ck:95Li;-t>QWP3%80*Drd+3*o"3aVDj@UHp(A^]9OS'R8s!,LOj";Y5Xo+1C1d,2nY
$jUNYdM_!i5XmeR=?)og.8H'Udl&^BfY:a5S!I/W=&q_qG(2abi\VMWG:]U?nbRd9C$/>hfEEGAF=P_p&,!4Ng.Y`j>]$>q$6s?HVG=>^n+KLBI:pXo.
Vn)MM^_jX;Bf+?O_Kh-*+lAGhmo98=[cf#Zs$Pe$J[McA.Pe.Ze!!qCCY%lA5:h1fE)n5enWI<=!M`DD:]8iNDeF]^Lcf?\mu,T3u:7W)'[n8/T8r"p9
/=QZd1t/-$^n7USso#Lpj6H,"qYA<R_L2a/!k@dc$^V^*0d]%?Y<A5*<<hK8X?2WQ;sQrTpFYa2LW2HhT6o0HpK0)i5!O,[3'^c=aBC`76m<`]bN)k4:
jS)-IgrkF"KR/C$5ReQD.WQa$4+Lg.;eSpLUqYc7Ac:7RS@Z.1*=j&C?!LB9E%[/")^;V>`WN/83fBCiF[dkEfGQ;]34)cC%5d_=;d!rd5p&]Me*,TmL
gRNsbi3RO0me9`tU!/G)SJr$Wpg+^(lkR&;*&s_#$a@k'Q-*I-V>%Q,Z/=W^XG*8"uV(cj>QSB<.4FnNs@^Fj!,,$TeNO;.F@ZMb#iVa]iJ$SoJ,#!:=
?<V9m(/l=,\U%4XI1aJaf$.o7$`@$AT<57RRss!X*RTj@1#F@,VXCgN4O%24;2]$XjOTT0>\pZ=<`0$<Zh<D]CCf^sr@@.L=r-cKJ3&J8k0pTf3m6f-l
]pp[4I2"aI.2O;fP:akgQTl5SZR?5c+kjl8lN0rc=[mi`n6aI:DPW3KjO6*KU@?)Z,luUNH*dIqfHgE#>+IM@Lpd@4\ngE"dsIH!'d"#rI>_\NLR5qrJ
#1MKI9&.2K._nfbDn416ak*fdH9>"RAFVpp:'uD7/Oadg@/<du`'PD_GO,`%id9VK>e0_s6/rX%Ef=@1TZ[/I;>f62#</MEZQTO90n8=TJG.9JSbHB^`
DE),m]6h=tOO60[O+g9%QdFb4=DM<Z2Vj%b(<h;!$<ed?.m:K7V)\!Z;/E7@r=:7(b^D#Aq+X9PM+SiR3S!+iacZO*jAr%"lOPk:Ek?bAalj5u0B-5s$
2bAfW*%LFAipL2g-,WVM89lJ)Qo9'Rmo3%+)LbZ:s<*r-e%K64(5>km2`<$,p@E3hM[fm^?LWOS0()a_Gp$rBohsk^J`>i[pL"6V\fe3J$eMbk#dSos<
K<`_d.LVINAbV#T^Oo]C\3<B#35A]:ZbZm3WFbcDJ2=c2c3ATVa!AUHnMFZ9cNQ6?7ehe:+KG=Vg"oFEpMM,>mIYS*iQeP>`()B2m\>H2S&`2(`k!NO\
>a5?ktC?[HrOh$A0+XVUW?&Y$:iWY<C?OCT$N#q9io&)J!#0?$hcEDjU9dq+T1bAM+67BLh5"r#:6>UTQ*)$?B!8Y+YTf+Onh-ob*T!rBXYs+^%),UQ7
Pu?)m=Y]Dth+c\;pDmBlrAkGF`E?@0Th4ZYCLI3RDJmk&lnDOu`!8Rj!sM#D21B_PD3i@l9bu1PI'/@o-fG:GW2(2M]8*fOKrm/u=l,n<1%Ke4[<nL=]
VOll9qSPLQoib,!&nSX4/Y!7YSM06BKhR*sA*[AVRpb,TXZ:S<_MeYtC?6cqX3:JU'"Lf@"`76\i3'F`_K2eUbuB0BT:+<U=M^#Y"FpB/E%2LUSF!Y!K
8UJQTZL6B.('!X9oPUl0'RJ;rCefdW*>_k1j'L.6TTadQJr[QWED7bV#i=kohHOT-k=2f8;+cBs8'1fnZrhP)`>3UsC-Z@Hu*kuuLP4ZB+GQeU<ZghVB
5KZ0[e6k//5Mi\]\H;*<n>M#a"^R<W`u%W'`@E.00h"Np^1<&m.$IGVZ^u<Rn_(4R9H&jWD::7l5Zj6Q8'E!J'0Fnpo;bclOX[!OXAT:_7*&u%Q3H?P4
ut$(@9fd2X&H&Yd#G#fXTrMeRZ?LTY>VTr?*@[TYsS&h!=GXuHEBn]7-3*@RQJ(4/D_a:[cA^/++3bCQ]JkdO)UYjm:o.Q<Gg*C@rp_02Z0S1e;F(I?*
nN'=#ZUL=bE7lMl<`sPFS^m&P\^J.C@WoYA=C/:E:nV`0qa4L=o0J[U7N8-:(T,Eea:`]X8;u:pV^@;1`tqJ`_s'':(W/O(GQM>eiM`<.Yra65_3MH!@
+(:^UF(''\]d2=8==FX]u%<_Y]]%CT6\G"sffE\`sG\C(q-X`%#3<ZN;[O6S=.2!oCU<hM_bK27q__G+]=e`$+0r5`7sZ7FAI1!4KU@Z7(/#FIN%QlJ#
0Q-UuVN7+=t5[oQ1Ib[<X9CK.^p/l`N%?GhaF([4UgoHA[Z[1ri^>Uk?>'cPa'iTW8HEM[H7MR",E(,`DTh?B#g3E//<f!DLW\uo\!o>!W.Ml!nR]CN1
O4[:Pe6m)&ReRm9!8;#YAHCZ@A%*W3#KussmlM(NA62$UHTKXcdjg33P]\.i<u8(@Z0[7TE7;-nIX\PV7A>H$lB/+$8ierqkmNt-3ES`5d@"%3UB@`<q
,`Z*\d/95chjdArI]:fbAY,O5GtE.s,6h3GQJ^`M.uq1PQ"Xu5PXfm_7>d)%AfUuBq/R=WWPQhTp6ke`TMbpo!/t>SSYnY$m-O(*?GuQoUeaH:Y]u13>
p/L`(bVm*X;gMZJ)4(dCK1HnZV;`:%lU[OL.O=#+Y=3"1XTroL.,((o`2[C4\:EmePCPfDkuSimC2dFF+Tj>G?[Ac$n\<9PtrRP@._(060=TReokYmI`
Ypcrl(M\U$FMUGMRj(=lZ](WkB)7f\.t"KBb4<M=`4)V#5DKVD4q,'5dXX?qOP:-#MS!'DhFK_V3B*@PEIcf`:#Gj["FB*3G2DUGh6Zmld%0%%&W+J3?
Q1.<)Vn=4@dW?9C*QY4ceg^hdh\lU=4PbVG=T:(88`mMMh6]Th*TG_n_LCXb^l8HolS`W2'Y*Yb6$JbW4T\f'ZrGYSI>4/#V_;q)%#3D`I\l'C>=;lr_
O="%=hWu`ki*Hp:bOM%i2u:H^K]G6$%@_='UMog?A,C%,ene@a/V=4(=<ec$"0\8#J-<;1d2!O`([Ht^0+1mbWLD%EffbUFVip#Dgea+D.f+;C:n`Lk&
VhJ^^6[GM5XElr'YW<sPm'U0@.C@aUo/)Hk%K!QjqI4>;*;Y<Enpor+SG?G$GR%Lj9Vc9:U"Y#Re?m&o32sO98"T6BXNsR(61(?cOnU`dtn+#E]Lj;"R
)m=P"Ter=1+%-U$!*N;^YJpBU^QoQ.HqU%V7aLO(hK8QGM7!PpJ&^5VE,:Se=W*,+:Mi#u_9IAEg],mkqBVL]*?^+1(B+9/[3^NXoL1N=ZBW:s8hL=t$
j&Os;U_WhPPc[&2jYEXR1NAi3?F\(R9`g]#4nZunHPnD2J&JcTLZ2nA[GNm^?YD5(.GO4`CYN9h*Ko]N0V&8f/`bBg_l"jAY#8)Qm]HEm3il$m#J$rIc
q4BZMcQgrmuZ0UZ;(W*1H+7@(1C">`f*k6#eiY2d"0WC2qJ7^'AW8-dDRAe5.Q9olHM4)>ZoN%85[$1KmU.'_."<70eZrnKEfH%cbQ;kgl`F`Ze67j^3
;+6,T^+`Stb#b8d<WAq$`<&i(WR7]P=%QHG"[hRWL8S&cESn5V/J]/l=FA1jk2P5I\tV'?h?WZ3MH$6BgT/B:!D%E99)l,I'c/Z%2p219:q/.'84nG,0
eRCO^R7fU5R5h\bKBse:pb!i5bqR`40hDn-f9gBbjYGVrr2dFnt\Ok;9MYYb=)k/Y$ef-@m!1?X$%NNb,,eAFS:;n@'L(EgrduF'>kn<lcg'.AH'B=L]
3*9,Jpl=*K_BYVJ'EY-?igd:?t(Pe/F75,5_PaVc*je"j8GP*RkZl<\_`49/<=NG2rs_aN4l9_foDnf)>pdlY]S/']S*$k]'Pt,;[JW[5S0/*SdYl0X2
H2IGQ9K0J\h2o[&pXr7F@4o><f*HM?DfUjW$Xb#a*Qo8<b\])RKX]=0BH&3"L"!b7!Y.XVDsK.g6KI"m78`E^>\;Nk_]or2Au"njW*5tF`3bR^_Z/tJI
A0LA[;!J'FVL86<pP@Z<so&rA=R5"6JOQfAta!,Vb=$.nD&)6<U[r&%j@8cSYqS:[Z+1a^TQXp_goV=fiO4ZU7=t[h<ntK5j!rlEj-=5mO<E;D:h5p0)
NR"qa*&`R_>pI@mr9RP#8q00tL"Kld`^b?<%fOG!8;7i[`pXoCnE0rS9`3!*A0"NI,a"/AAC#reKP%="P-(=nl?Mg:qe3rO7O(JqC!@i=)CagtPl.4ih
p.O'B6!8HI6L#&-02)7gXZX5Chjt+AQ)pi-+&j)<L[u<XZt]&Kl/.-HHe!f4,d.&@?C6#_KfRpeu#HC%c>!JHLb"1i3bQ%4gR(&3S-nkjT`B.fW?p9[T
[ZQmVQ3qN7qQR<Obj\V01@)p07I_/&NG!mbajua^Hm].AW.YGd-mU+s)P'XQAa[)CP4O/pEF0F4OrAg"g-ID=".g/*=^bS<B>3?54tup-ZTYqkNl3m`'
)3k5B.;o77G&(!fH!(O-YrYO)t\RK:Oke+IQ?^MR'HhQE[VX/a,3P7=!jXK%iH"/n;];k4qC)Op+;*cCW>;,cGUGD"PZh;_@IoZA&ro1N1W%shDhU!>,
h)7o(YVRA(DVt#eV>hEH:1',9=JVK^j8B'YDQNkWBdo5EFa?dqqkMq5gnAM\VOUYemkWBckIFM20qXfL"k^!@"SZ_N4lrIpACQeEWFSCQ_mnZFpCb%LV
n"\*$+81iF1?TBnI6A:Nn8WJA1m3lJSSHkCq!-$U^3K;3f3e3#huE!-YJ39bJ#O1-=FR^QIgdEI1H66,XDS8%kOAN)mH%Zm?<_`B^,k*,H1?QcZ+>*h#
i34YbIt>DN[e?)`kac+9e`o0Z@r)>R-_*7pn7a_*)<`VH(G+6Z2@i;nLqsCO=lF,Ki:;\B1\@.=]AZg=d@D!+19!&<CPXI/42@VI_cc:'\W(?GK!d/S.
%Q-T?l]Do0=*3(i*R=W39@JGu5:E2bUk'9SY&-[QmPY#a..V8+(<jZg<4eGmoU,apd!3Y[p1>O(>rG<`<XWVTji:m&6rk:rhIl0k_q=WQMnC4sH0e"P[
f#%&OoRW9O#%]e?FT%chP]LGUgq8?&s"%1$%h%GUSQNpp*&V>+-LC9Xk"/0n_XP?*DQNs4`]rufb#UM^U>10%K&ZY[`DKIkH3C11e6KgAVUjCEUECL,K
/CE4_iQl'&O25neW756f6lV0Si[p5-?BhDP,0WqqW14_&s,C-&mPdbZn.pJ\H0(a;QotAcmcX:5"&d-"r:Id'EpbfPY5#Q)+U(ab"!B^1t3TR(W87X8G
W5C1K160?qRAhTAr"W229RO`G]nJ'8PaRVKS[l9-V-cQ9qL1>N>GL%dJK"XQ2RGQ2FMmc#e.7geq_fjGJRRJE%*M4d,7M28fM9$:FsPW5]!h4=kaZme;
l[^Im3.3&XJsb;otsS)aU/PupuWk0n(YQ@4+;m$C`@@K5aMP^'*.":C3V6G.'IGql(\IHFmV9+a(])JfKcFZ<ennH:h+\;+iDu'P7JT4&B)`>SQn)-@<
W\`ndKerWl&">57b3ICj3)pM3-_gZI(GMDE:'S3P4EE8<-Uq'ec>f2isC;T(0eQF?a,WlkTh*/\\$X6?O:Il0,80GIqWF/eq5Wg't-Y@Kk^UL\;k(bOu
+Gg6,Vk2)pT)T-!=A:X0)p`N&S25r:OEgpL4Eo1iKH55rEie/k3N)RUW&A\nM.^642(Ru-gPZkKl-Eh2`Qei5(O.o`QBg=Af_BInJt6&rPNZ^SajAIgY
(9f90ri2,j#dg@LWS#/iigQQ3a;T9c]SfHH4nhqeS4).>[5A]n#Mg>it&p,d2I=T`5D<mT)*=#dhQQ?o1YBcU_2Rj_O#,?3&rW%:eo:_'o/8`?n?j5"6
hFQaqkEBmo$QX73Lb/ZT&BNcV]+#c;lrf[4bk\[&\_1Mu`k[5-c"%jB3aIsP1a4=]H0_U\g9(GQ)tN0#J+WX!5H6id0G8:/VF5-b;"]"h5!+&dlM-DP<
IbFSq;u]p7]YOK6mmSca9hGPmJMQT(a"\@"CO/A-L5rb[\Mkq-\"7)Fn-?"^UqGMgA[0&O&)%8V,e_@FOZ[J#JDh.G]QU%+\/QA8(ho`aSUFTM3_sR]S
'eloWq<]CW/W/V38L=H_-9i^>iAW8["8=F_W8+:S`N@8m\b\Mq8gpeb']Kn/1q.5;r!-aT6V>^&qTQVYP#@\%?JMf8#V.f`%iE8hS)@YQXtf]O,T:8g0
Y7Z!?%AfU&;<^QTtb>i1f/iB;o8<C`RMPt+eM/g0a)D5r%*ENhX%!PU&2k^b+48)<8SV,H?XZi4\5TMqG!5/Vm!S(=\>:kp'Xj5gpJUt.hehAt#?9Ll8
lf)+g&D]+eNPSuS]=:7ufgYR#b;oS%/cQgLB8Mrk[*ei1%^C$t(EZ?P^2glG`;S8/8(Q>LL`p:3.\p!n*Y8"C_]EsQ&5"kgmg..NGjT;`e`FJVnj7UBL
r-]>]mmkg"O'L5nMb']QDm.+pY3H*0P3Z)sbp(ZHhW:V>HY44t;?5qj3?0r>:'!?.rC.hoj0?Fd!m&-9#hM"NW)b$kI6*Zge([%QnGR=riC&ZL,ogjtV
&;id]E/@>@m=`!2i:t,.l_oOn;k]tlP,ABap[65#p"PaBt3WpKTYi_bJBj@Zb]qBn"AY2<JUiF\n#=dSSfcW[2lkue52/N>,R%6=Je?iJd((`J=:^B>.
4<'5'Ch6Nd.=X$J#(,f-:X$lF2dt"$n+Z2F4@o$?K@q_`T71DM[(?RfF1%E(KI!*j"CE3]_hB3R;5n)hM?Xa?7nHK7\rJoN7(S2g.LAZdpmB=N/EIrRg
Gpj]Qk'jE]t5Z?RW#0i"8AdmUnm^JA`Gh@8!*g$2Tq8KDl4.E.Ir$neMaj;MT`KrN(H;X8#"*V`rkF\l?e1'U[@B=hQtB=a:+g%MT4g:`DR:7Ho<mp:7
&Mt(OEJP!=`N'@bqe;A0B%68(h0YNa#WRgt!3JghmEI0YK#uu:1j<E<MU$4.p(>!tp_%n/[\4e(d^L7nAiLCbWecs8PGHn#^h5+uT=D:a3APf_K;Ag]A
p5F6Id<@^iVE(WV2R@FmQ'54^>f2j6<a1W[VQi>ijfoad1hJpDjBA3h(#/q\af;u2cIOT:k)2)X;Gh>PFh5mNqI*Vbi/:cNd:WoMA_L3i,l`)_g`de-!
<R+Sc-9S.8tFZWVfC1Fqs9^\%aPpFC\/o$Z4&1CV[5O+Y%=:K57m)l&qt[)1jE)c;sMb*gWa!X)A8iSY%`5-mfmQ[q1e:2b+3_(AcR?;_5-ZhGM6'`%A
sdZ+GTW,89fnQbVhD(.n6W,+I_-:$B[0mO(rZh\(>f@4e$>E=cV&ma8hVL2B&piCqtYSDMn]#Z*2D$CVp.k]Ar/*Z$BlL_6P2M=\/K@514I3^GaXCJ`A
Blabpr4"M&GP>S+i`P$0pKZrUt*>*]&,FlBNl*[kk9M&+Vd='2@5qEfs;()Y%c1,_=?%r8)r*8qf&qP^f=Kq`=;<gBE_?7N!9j[<LQH/1%/o5b]d=Y+B
aO(^O;cR_RCBB)lpjsSm(,c]L-nC=d`kuo%4bOqk]$WV*QJp+\lf>?njDRRcclW4?iM?.SrE?H1Of2$lUI$=>hn_0%Q3-q&tn"JD*h$kn9.]Qn:%g&GI
5.CUF@6gel5N68[eZTlDQ(t2STZ5`chFnb+"s(`MgDH?R(?ZsJU1LbJiM4IK3`Dq,iiiK$q8?=2ib[*6=KSPm>Gj@t.%.:PNpD/e=Z!I4PCUl/&OHeP/
U"8[if!5YP2?XEJ`%cE+;rec3JOeED3i<Yf!_([TOV%6XOYL957)[lp:I$hP^usVbq1b!'=h+RRsB#8o!`o(E<(^XV&5V?p2'nKJYu5"=efbMo.)?<!A
$Kf9'N+D;",7]"mNU<U%28t5.e^5*j;paWB5E<=_o1n5-2G!D9MA6U'2WCS$3(%%9fRBTImHdHo2O(no!RI?fGZSRI^jZBbS+9a!%_3$lTW:[$*@iRJI
EnkE91BOsafWr]tJcGPYZ#`%;QJ"5=V_[+-%Mb[<KjEq4nMrs*O+g8_L??d%Q3RTDmZn?je_a];F<Y0ac"rki0V64F^<8]n9d+1YtTghSgd)JgdO(3uk
71"m'M>Yd0T(=qHr=*iM@>%'K%?2J?P3A<[aZDi,9Ua^#R"9!2\WbHI759V*V9)i,/qIN""X(>"G%eEP]5Mb$Vqs(l(HA+["n]o)YAm"^SIUL[R8d!t[
I?Pjt75jUH%=<b:+6<&WiEU++@*MfecW81'Mp:EbM--D*gK&Ze>7<9P,/R*^&j8/G.R2^Gf,0"XgH(AU<pP(NMdBk`/QL_/98f6U43fE/PsrTTgPO9ae
8JX2SW@u&A"24dB98SF['@3@fn0/pgDEA&gKJ9`<HY\-Oru8bqCKG4&ZXCgCZtX#?cXG?E11:1>T=-`@plun@?P4Q<)C`)7K-M/p+n;a<h21\kEr\R8a
SO&hi[qRYCX-/`b4Vfgj98&^GTh'@3,(PJ^L$$MoiAN!d"E:a0cCAqH?V'lDIBaejACk[DdP^CXXm$VKOe\BY+D*aB__Qg;@*$`D*2rc+E7;55D3kbKl
H8A2XCXFXLEO\QF7:?8e?#hB>=tZ.Wl`5[D-uY$!ftY#`,2]`O?ac]NCDgFV\Jh.,$&Qr0i>pQu8h97W,U:,2e='rt/>$#CEd(&)"VTkhP'$J+&4lL*Q
WYlBGpBTu4dm.p$S(H6TCJNM@2lM18?@"uEH`4E2YIsktt]dIT9R,_FKXuUg7mO(*>J*is`lmGrX9i8V2OT*)JOY8>4q3na8aPkl>CR?K[GEOHmHR&Eb
DV3Um=/IQBgWkVS[>4`J.T(BY;@dZV/FuYc];\q*Cud[1h(uN_-g<W*1MC`J/4T%aYo9,Nf6nS+)=hQb.(kQ3.[K3Td?u]?@`LmACXEM+3D&6U#._E96
sMbLj%V:T.\_Nna\5BOWX.F*;S;$X]X;VNoMhRids3udB4$<l4)0,ePQQB/!P[u.'@"a2X"o?nR*]qC??&7om#>nJa`iI,A71m8,Y*TGA?eMk%W(@J.3
`>@.pnNSBV(ph`@cL<9f%L5J;t>RT@,8\Y>%r$-r%V+%Jb@320s5n'"rWngpDZO75J_T=&hHO3rTmBhLZ?VO4#3',)OFeQ"#Pd#pSC6%bnP&gL9KX>N3
dgcFVf9'+Ad7<ONbLYIN/]"RM;JeHeH]94=kTe-OGsHo1ThXt&o*A?+[QBik;^h<ho+rQN:)>4KC1I46*n',308B[2XW[j/7h;e/>G$"^EC.Ku\6)6]n
u8=[0lJD&RsWR\^:9/e;FhO7ZF!gbpRfm8f+.jp)gP7"rAH2)2u><B9*a=t%qMV!b:GAWm$-hT8MkPhTtXPA2Kf7YUC+.hSPLZO6F+BS)K>'DjNcs7-4
7L$p;>->[s`M]C*BN3r@I:Vr3m!+)JIQ-K.QRp=m^mq)j9Joq63C9GV`]!hi['"j[]kmK1puTW`_e5qD^RX;CH'h)#6b@sdXoUqP$;f`G#=c4QF/rQ6W
XjFKQM7iVmJTt5cYkt^4j@q&+ETCUcAacSr%[U2XkH?/P]t_8s/dC)@>pP[Aa]BD!X65h\t(FXs%e(A!B.lCCasU#,u0#4%.\R^?onrh4-)e;43U4;Pr
#4fXDpjUE)bS)ae$7;<cRMU"aCD3;cB3q%n?6cC/C*Z$-`KK&PbQ&fJ0A%]Q+WAPTCcc_H3dHbX8N*c.-*3"f/G4?^'5sd.*]*a/_#DTfsp.otB/Uks0
8/85H^o9"C@Sp<P_]qlLk.l%\:(K'hfM^bSVBIAZIQLrH9\YkIIVC1\bG!BXrAW5<?pG/N,Iq9Qia*0Q'e6K1%:6]IR4>CfiV[9@7^2JDglZop*QrokT
8mh#S)_W\X$)+coY\c_k]>Wt`LMb6(7,]1)P1gnYSH@/_O&WVKR`(KfS:_bSTe%e+Ide5j,kLrlZ^B<5%FM^6o>N\hGNJMS9ag8GhAl0=UlNdp.-\`CE
p%mU-CA4QMBs%`R1l8#Wgp1u`)d/+gSCpWZij$j>)8@T6^^gA^g>NL`iVIk#;g\[Ibjjpn4&'cHbH0ti<2kn5d3*=CRJA'P2/Eks[ML47Xpg[3aM'G/A
LjWu]E%6rRh:lZfRm=uc0["@\e^"*0_/rnWF^_Q(o>4&HtYVnR4\<2l=^TAjn6Hmq4_=GQp*A:+p2b<d-5VbR=Tq*^:%:cIoE_-Xal,?)0P-g2m,qn;O
)tN68c+EkK[(ZAgpml#8]h>2SkIO:7ObL@OCR$GA3GHi(RjiQs[JICal4gj&K:HN!+7^qBb/?Smb;9Rh!60]N@lH0"#m=rW)D^c*J+2@Q@l&8=TKibOm
RYZTYV<^7j8!]tS\Xfl$OR:5,!0hn.$Oj;iWbEM_AYEoL!]>$OE12^:Vu&go#</OK-6$&NAWS+U#.]kTlF+J$!qJ6(OE/Qe)@A$E(+SPOnF(DKfs#oR>
=H>F]hO(9@u,o!h)W7S3$Sm%:p=Y#n"Z))KRe$.CB9+.l@=lNW/b;-%)arOXhHdHLg$7h^>\[SU@;:>CQ@U4K,QVMU1M!c<3mk$]K$[<-AQGljTkAY5k
=:+UcW`p.sQuiHXI`hd%m7le6F/Y!%C.DqgCjEeD#!_k/3Bd/>[4t.9@=u@BTW@SaO-hTrp7=af3_)XMEf;0KBp!AQS.J^`YB*FZo]>R7ZmMNaA=87TB
4)H$%=P#lS%(E,Ucj.%/p\CFhQl1#`!$">>>:L6OpA'%eK0>pfW8a;2T.'X"4%SIR&e@:#BkRH1SIr#;%"8`Zs6TkCH[^]"]Mp6(ENaP?__.'<k<Xd>+
/9_aUNqe&m220m^B-3btVj4M=ZHq<Z(Q"((K/>Ga*.>2*qaD=;scBdlatXo%h$(fL:Q-c>d(SmPqcjpXC2U$c,4lA8X9qF#E0&cWM^nT6+uKCKGWe]1g
03-jp;u;:T_r$,t+A*/U(`#)X^U\q36<p855Sq/$4.s3FhJD-b=*/$'5!XjO3k**c^opBZ4b$^%&&#eNEg%<B\m,.cQ``rFjOb""7aBmH&rN>4_O&cUn
P,W?q?+?])4p5kYQ&VY2c[*D9mdO-)OQ2)uqPH'ShF-lL2!BL-P3"R=HCmAQk*3_C)bO@E&Juf@1Psr:;YT^5<hcf%p(?7[%%5h34>4P!a(aKP8]UWN!
j5i_7b&$#[Ct:j$_ih#DVH'l^WNVAB;9`j,`+[E0^PrTgSD:nn]0h_:AN)je[^*6HAe`+ioe:0S#YW?ANTYZ92YkZSA^WI^Hs2?gX[ZD]j49Z(4L4=4R
XG<p,ZPXcaf;1\/1*;9[RYUEobqh]-JIjMmHuFY4h1+!DI?+BVN4`n$Y-=0B3+-I`[BNb,9PD]PrnKnHHE+0m-``__o*8S,h/QlfDSBVabe-lR`nS(n\
'-d9T9L.\Bp5[Wa*a'6(do+!nl.P>;nhAPplkCBSPQm@S]9dC6M9tm4@#o0?L_EX?+]*DH4?q(9_e%T2<BScuf^<c1/`B^Hft^nlUh3j^sX_iY#n"%7W
[]J6n40HMLhifgQu1g1c:;NW`%##/'"oXN,Bt;00)Z>/7XDUi@-QS>aRB7;T$$;DS0e=R)cG];)</;9rqh-r-l=0ZlCUQTLZ%P]Gi^V#bTk=.>e/b=p<
rPM*003R<i@DLITQEY#'"].\-A`<M#"WM?^ZcW(<E[B^F!k!Z/[(>%s-O7U/Y4$u)rgCV4UZF=S9?u_[<$_q]Xp\*E7qW$Omf83;+oC2J>VMn:eT%ESt
+8#DWD%$G'P=_'7dDQnFl#^>/n%\p3r`>U3pVGQ)$!DXq[:$237)"43Mt>5s`?2a:&psS0DqZRFBN7u?]C8[i@X8j0'l_I;[7i8:6fi8`CTlX]A'kB2\
g])H,u-Hom6@>:fZ):6Gs\"fc8,HV)eXYtat_jBI/<BhCPJhg7A!ssJsSI#JbSUd-^RaB8Cm[k])]eKHSfrn%O,ludD\5fe`?]rQ,o>s8MmsP,D_;t<U
#4O\loA%OU&ZM!lZ`L^LO?FXgKN41sIIdq`MbkD"DgmduYG_B"J<9S"fsK7`R,sfCZSnp:#3L<kuChEuFV"$0)Gh55P1&,g^YLMja0A]Rs,GQ$KfIj!;
ho$05uREuE5'(k*pBh-!'b38i-kYZfrb9-S.P3=+"Vn7B-.aQMNJF"PP(BJ4AlLR,Te=SJRMf<ue,:tW:3`g/h^XQTXS5J2m8e]AOtf*"k!`58ij+uGX
.CCaFP*->+C?GiAs_d\8.To2X2gMH\9iHXSc,K7Hn,kRjRSGr''nZ*IU[P#Ws2p6h=AW_=;l70Mbetqhm8RCFCYedl$A^$&*P@rJr:GQoi:*[NmkGFb*
C[9Y+=j7.T/S9!E.ATaNG^Z!N^)CK&@MR3Yh1+HcnRbF2'JQRN%*u\<6,@H[95d+)J!N+K)bOH5R+`6HWNGg;iS/Qp?9LB!I[IioqVC+gPN8Tjn3sGIc
_.gmX<OU"NAi25*W*jpr)V$Yq$><j4WTTW_F5FSd`=\<=!l>)qKC?lS"%XqDCkBp:J>X".^_J..=%1`&1G3=:Dm7s-mTl<7`mPu_^/rBZB!^BKl6Vn9<
5qIhJ$^)d57ntITr^fl</lh_hb<o<f'(P<d3WOB*6>ql<6UH&f*Fe?'`NM&Oop*0[g@8)Em79-.gKSn!6`SjI!5M5=+JR$j6*GDL]H1PU%XY(+5])5/`
1Cs*)2kF9#*TN"NeMQ`g7K1']MU&Zc%<Q'I7kFS_cKFMe>E9T/1QJ5%Iu_2s9?:s=Z-kB3#+6m)4F4OI/o]9h&UJCTFbHSE&`pI9P<Muqp'<U4F#0;Sj
3^!'%F\8GRS3SkUshHKK.Q/'2G/d5B/RHhff^^kcadbS1lNh!7dcSF,R=PHeUH,:Rt@?k,9ee0.5V8<Kb(q?OXHR<*Aq:pq2C<;4#g^0_Y710<"1+p8.
SgfXF</add]NJub7!-?Q\SQ,[\jJafV>'NFdi#JkfBI7BMK9k5o0^]J]Jc]$(i5sEM8bFF>`u3)V]%V`2hb_XBb-BXa,9DHY!OIj$Euifd.a'PW^D?<V
a/5tQ[t*C'L[AdilG@R!a1r8;fa_HorMgi'NhAA3@)Mp!GnuE+hLb^`_n6E1?LRH$Li+`W1^*CQLIlh&F6]T?H(oFNN=fU>Ep%HC?,'c*p-GSFUYUsB&
!ZkAP]-d_B4Z=WC#+!`cd2+C+_"3.$K)2`3[Le2Q\7CNOg]6X@/0eC`=,><GZ`T8\KbTdUr_6Q;u=<1Q1NEOpZ!5--ECSDHM#+#$>&Oe03Q8LAr[)&:,
!#dQrEu`mgf^[!C,sgY_fB%ElNm=@B[XG*CS4NIKWJ:UR9?bbXV1VSiC3-(cTN%&tm!2jn5o#Cr2](/nAZHE1b3U%)g#r;rEZ8ug=RIt\oIFS<9?lW,I
qi'R?HBXqBDDq_QFXA>ALJK#>%f:XG]VUL)JJq#*<*0"_P[P^*D)Vp"CL/RGQ@,3$F:9cUF9!;?>X5u5*NN?5W:%;MYNQ/ZV<cI<s\i>(cNQd:>WY+"N
5*[W6S?@%LCeI$R>3,ma'#fR;Q\q.sHB97cK?-="b>iP2)fm#BN^s>_He(sf^q(RV",W/H#_GH1W-k,/XG.OF4gJj*c8-t-`WE?j_!kuX5K];f]Jr]%$
E&]R6uu6m6))!jApj:,2"G-7?[f2aU;]#WJ\KQ1FUKMb<QdR6ANbd5+Ak^ZKX^n64sTFO1")u7mmf&JQT@X9lokI_+NCYu"@+0CjngU9.ZtPp)c)R9!V
9cT(A_7.l7?q?ma*mW)G_2]jgnQ*A<`qk+iNrViD_:=hdK1/&X*#W!4%@CXUVJ5@D,sr83&\XG5UY$M'-@f0?/6(R_3Pb4b3f]X4GN;;2]E[`Xo]s,l^
!*H:+qnn9SCB&f8PbUc\'Dk76!H&qnh=L'=E;8ruC624T)G'6<3$RnF:c6"d:WY7;sG<rd"Nn.<t6n9"0(FOqY7Ri41LhECphV=&>nV&bilE@YA2MS4p
qC7)`n2]uqZ<Y>*>%Lm=)arNWJ:t)/*h:4Jj5\=b3M\"_DJR;ZJkhKaHn!N+6a]@JbGeKk(*"KS,e6s/_o*\@4=g'W4c;KIRa;[P(':JrH5GocR[2o4j
W5!Gf6W;@4V_8RE5<OAama(sQ19(DS"MA4sU_V%nH@'a19:+)jFrU)1eU@bE#dQ/im0s;*_g%1Ss!kW352aD2m:_q#UaQs\TRMC_@OmP9ju3nihE&UA&
a@r7R0ZcCf--lah:fY+Ru\BSGqVHSr#O;f&A[T=M!9=_>4_+e*>=g%n4B;(#$B!L1^,b@J5Ye:E=uZ^2J5JVf=OGDarEr'O=rQY%>l!IZPuqRFHo5`Qi
`hj@?OR#&'UhS!thJ5QZ+;U:d88K>[XE`;Dr`^DEGEDTrDYX.:tR"oP=sN(Q:L>cBHL8%UEfCW!;:VpdJTMV'ZAD>WLgNh@/97\I@l3\]_/OXBQgZ(u\
LhF#:,=hi5:LMp)NpAMN8:D3I914dtL5QqkgqA6K`j8._9WSg:):f3j1@C*;_[4(K1rbB/!q/^"P<N/e5Hj-9cX`jLa5H8mZJ_UqaP<O&n`(A^+c_pR0
E+;qmP6O4>9,rH/cUkT!h@k'0tJXU^F'<b2tBC,PkGm+.4]E:Na!=/lDSKJHbD!uFe.s2o!hMn>eHN3!\4?J#f'#_`O:Z!5M,"DV>k[4<i/?`.29aPhi
8T<*5rF"Ak?qdNS4fd;Xl.p#(AM`G[`ukI]Z`poXC?+d6U3D]:9qCfA__RMF$-"qDQYZId<3o#2$2'DpR+g7Fj7^qof3lt7C9o^(PZVd8$kLML90jUr`
`$KAjRl."W/+Z-%g;=uS6%_Y?"^A+]N_;?Y3`>G=\<i=S<sA6q/oH(2#P;$Y$5<X(Vn^1-[SCBZZ4')[<uJUPuE,@kn%VD+2+UJ@pgi8mgkLXai'0_gi
sKPYl"2l+*ng<8R3Fg&B(X_^2%aLV3$uXH.1BMILi(]AL56_W:dQr[8Qd9SJe_f:gYsrmg.95j]rN_8eN(*\Z36q#*oTQR3'h4])D.>D/-[c-daiE[I7
:UR4KY@EN?6];5B4d0^[=HeeSm4fapDZfcW.TT;jRR487m'(XB$E65dF9XnZW&l/ns&ga3<P=YX5WO-Hb4Klg'+8&bnPcqFC9cgVrdW[ZhO'b^SPJ/+M
#pAC>[rXBpe[[],+V%XVa6DLf&0LR%c!,YG/)I"AX'U>qF-Z*%[1L)(Ri9Ze'=H6]4s$Q#Q[uf4\Aq^h.33ii2Zr[u0e_"h">g]Z4]RfJM7<apVF4Eg+
>E302O.@p!Tb@OrZMZCZXnAVp&aNp*,l/Q).UnNs54#Lj-1q#;qAB$%)Eo+ZKnGf)jb#I><,p00[V>l7rL5#Hj7+5RG630(=BH@GB=/l5<o6kI4"`o;Z
0QDsB%(_oB_6ZEiTStD=3%M]_0W6OrG=V8^H8)Em`25^Ndu\t2Ghpj?$C=,GhjSoo:X;mJE<72JJi!(18O]rUs7tZCh(<-T-`!1bRd<SQ&&1:()]]8.d
`<fhaBEW#p`l5%n<C,@QhC*RI_[[*O"5'\od/OEJpsN8>-8HA#HuqpLb;N-Tot<LJ$s8O)nR3&3SlmlLI_)S4uN$OT*/si2$_2"P,uKChSGsFb*`[oPQ
RH^?GOe=3,lJdZd*p*riZ:O:mn7n4_c1TsH1f^k.E_XOn#p9j*=H@9)8"Cra-,LT@b)8&@1+R#fO"M!dka."6WDdAW,><W&)A$m`nq_^qZ%2!C-cO2YP
>Z!#C6htU&I?DO=Dj@"Yq@#OJ]N[_i9=aADC[jX2Y-&$7s?L%EFZE2-9FEm_s)bMo0.Vk&H0%\E'UE0(DVi[K`((&S>*Q<o#\-M%o8p;8,M)l!8>Wh`[
^]3A![UI%!2B2^QLE<WAR!4dQcNm.E#FMF\%HQ@:!`gK>KLT#r;+:-joet-.4sKZLr7Cu:5>Im-`;^qZmJlj]V,+4t?DTZHX4)'VNu&"HXSRuSl1[@`T
_/'*q3I4kfJ-8$54P`s?'(U25L27a;@T[Lf\]4LOZ0BUC.?Ds)lS`j^O+<LUkubLI0n.&jnGWu>F`L&bMkQBRueH^SoahdZ0;FaP>SXR7VJEu@5_[5>\
scL98)sO0Y20qf6dl)NYR;r#>G6L)obl/-l`$OZYP'/&YZ\bdY1@@T7\Wj&IcOmV'qhT>RNb_F\1X+I65'OQ9,K?M^2<8?l_!*<1U;_W8n(ViukUe&mZ
PQ/PX:9i0Ati9;fZgbg;BD_hJVk$s1DJ,8!2P<KWrRPW2'+>EEo*02_7N^p,r"?0U4"35i#-h/\XO6Zao_V%R'bFCq31IFsUSiPjplk8<(YP9PYLU<I%
[7Lla-i?IcDe'jBVZd[C^Yh/\oZp41D&)lulFT1;+2'n!P,o1^be$BS3/XZPe?2p)8o<C&-OXO_l"$p-6(S@BO5C4bK;&k_3QD)28\KYNtL).!G9;U)=
3YF+-6MqHsf95TfR6Z[Iht-RE9'j&aWaLOb>jG;#]pqQ>Vbu,!"F7AuZUs:_LN/YoUrlN[ir&BMgFX8/Zi,D;0S%VB?HTGa[s)S@7VLLW:FJA<jELG&F
4K#b"@fPr5_QYqG]R,@_=BhR(<QbnA7#oPlRaY['rupoEg9-_fhT:*j"OMF-%*L`H"&"b$E6Q`o-^Ek+]LIZ/+:T83PeanlQYG%JP8OXM68ECH3\tY8R
*j6ZUJ5sgMh^&9r%Wchi\-)N8hE*LUi^smq)(J8?3Tp/dQ,P@aKKK'j^2.@r"e5e$eq"+*8/Sid"]=EH*TI)OtJBdDZj*EdEi59.!Tue/fO0i9[1WCBh
,p2)e+l'@pc<'0:bt!dS3KTe:Gr_[LY:8:N`_(,fXCE6$TrNa:j*>R),oB')/%1U;a7:*J.,f-6b>mRsc$+p@'q5/K5"1Eb8jYpc`W6O$j8bS=/9Y-d7
Jj$iiPJgt?2C!J-3dF0j<bCF`?8pp)?cQ?C+X8HnOFtcCsq:',&r.,?LcEuIC:VA,1Bh>C)Crm4pe;3a/fIX=@1Y?R?^/+KRXUgu:E8;8OfIKB<'S0Qd
+Y?Z?'fGYSLU5O6G_agiS1J`ZYnG?56sp;9*de&h)!qRQp#@H'7#_'N7j5DKB#OkV._[4WLebdL;fNX<:>CCU/oGL\Ob@;rF[*eV_l]$FceF8QXUNYXe
GrCudqM"80iQP$FDUXS]<N72<L7q,j#pKd>pi<sFf]3=h2l9m-Xi_/,,$=2"9M=!OuNN:iF&Ni+i]F8k2XXkl.GkMG<QN6,OI(j!A<0F.^8t2#>bRN=b
;FIE^%)^T/i8^C8r[%3390Ek]2[XYeCLc=D\h`01En(=:uFZ7`<G"![E*uMK&oU;pehe2f,E2j-8uS-jU_@_OT/V82-9H!et_uO-i"*>bpZr=iR`e\7&
MQ&ZnfM%Ua$q]=tF@Foq?>hg<0BNo@(*e\-TAL4;W29oJR\3@e5:?^9;KUC0<oQOQ/U*JSa,AB@,#4T-Yoe?o9EH7QD^=csNS,/I!t8apTPh>\63_Jd?
MgZ8"6]^aad:X_#5!(OF^_h\2?$N7deROVoieJ36qZ[=L(XgZ^t=Y5B0.S)9IN;7-D:s'0.A70jbIBIB19n[mb2Q'rp#pjcjTY,3nMjmoseP"b\K+^cg
j*(LN."7"q'<$>EQQ^_r=kP)rVc'_A.\Q1QF`SN]&,!HTf[j/Si24rVU>*],%`^ji8aW2iC=_^O[a!,6Y(iND8?r.;'gp><Y5YkGaQ6sKc+J-o8)DgaG
/Z"38HZfKAg!bAM/[/VdH/Xq0m]VGWTf?u,KfiE4J,nPA97I..gibS]$"!i%Cf>-ZjLOgo3ARm^MWA/((gZKeb;9ko-78d_UJ5VcW0tI6n7rOjWr1Na<
r(P)9bIqrQ9o",lue0cHt^&q!UsRY@(CR7c^hH[8-cXqPai3Z]WHPa>n"1@=rH"k'SQLR@c=WVLU;OH:*s$R>Zh'6:`@o-@@,D>-QuBU3cquRk3-4o5Z
Wi8*W'I8IeH-qUWoLaa,$#eAq"3UZ5uOr:0"$a^:iG(UFAGO782Pp%Vn\\Iif(6um/\G$]&5*6&5YVF)V/QFbZeBEZE0(8;/<fM]o6/tglU"-UL1)klO
I%i@c,WAod5lolFk2I$Me=-04=ZTr7e!d]+>;jZ9=52O@(n19W>5AJ"1c]2AFHhlsFO1sl+fsLC5X#p*N([?p!Uom3Me15fao]d!f3;B4S`Kr_D6h*^n
ToHi7+2C/<h:"=IG;"uKrH+4ts7lKkq2`;j?iTouJ,[LGs3!Y+ra5]qp](+4J,aHeq"t*O\'h0%c]4#>1Ce0oEr8+*_[`jYXR_M2NB9^Ys7>.Dl=_<0c
V'-k@loI!=/?;":Gm83V7(2of]@>q=K8leEi;GclS9JR(nB@aK7[0dl4V_pqP$IdEqU)3?SDmm?;C*54?'$.16Mtj@R&AOc(nfdQc=TC-h5H(;9UW[L0
?$b!)V>PlV;U!&cIKSG>jj`Lj-1?'j]Qp6434W:rh@^MTSWD'iV/kLc/s;+$:[pc6P=Ys!ZhtcWlQQn4@!)R!q*[Gi(n!_eSuLWWc?ZX;!pV'/:`:[O>
p/Y+&fc.t)F4o].Td<57$W0mMWGitj'W[(;1O+Jh").YO6\#@Z8nhD$ujs!qJ<OoMP%Ld=^"!jMmU_K`3iP/#LWB1d#(Gb<r[4WJ^YL<b@/20kZhU:Ka
kCeQOe?lN%;-%$J5-piM0.CjY'mDh(Fi=!'a\_Yjb/4j<IUE:F47KR#D\k.LDP7ZO[O?t"U-*G+#_C=-AU5@Ga5uiG-gX`H).6Oe_p4!`8ePPKB0/k[,
EW0YjEW/kjGYr5A!DdC_=)gF8>>$5L<s^-[c$uI?Y_EtBn7)ZikIiRT.TK$fK-tfbi*@'Jf_A;VcW50s%5=c*"eM5^$^S$@0Wm)bPt:\9GDmpr2r9(o`
A@RSD>ig8HH,,+d;al3/(AU2/PtlU(o-8pX=Vi,1%!0ZYaTdmb#/Vn7&\dl'o0._if](@KUA(e425oPOeGFSRR)UiV=C$7kEDo-rKc"Y,]rYf4.4cnVk
K#eo]*&t_tDmS%;<LFj'UsO6;^ib=JLX0-49k.Q3?p7N)ZIQ(G<&E"<A3%p3saGDgHE45J-UMqGko2p%AhI+4>"qJ@ZDKiU,gb*lqR)V=*b;a"Z$E6d;
_>b4m9&fjNmd&HKGe<Za*&VP-#q!&?/'56FI4hWLI`/uS&:g3+u`WTORS8://^7]D$NShtD#bg`nUGGI4T`36Ejl!#pr&91;Ii%9=#cW#YFnEEeE4hKa
d_:8X?'Rs1u;bG.+?@=)"hQS\IkD)fbgkMCkPY!2p!u%KMg^9]\(rC?0HFVio/g5?'_='Ka2MC7pJMW#d1\/ML9%>>-oAdQYgP8J."3i#dTE.)1ZK#?$
@RG'q;cTur<Y&3ZE>moU>4UlBD)]t^\p:c%eB`mPi)K?;\0$L':-P1h>'qN5`FnjqYfuK-pY1,();UJ%WO/cmC&=m5Wc3;7Fp&-iM&lefK5F^3SrMos%
Br7M*d5/eYD948J!0H=@Lhi%(6"-2.r-ZPe!@gO3HW23;L4IMBNtQeK.,amLSM:Z/Z&(t5c*4E.W9:r8aX]$Y,GCg(8Im\;k<:ChQ\9_OQtn4*nr0epD
69gI^=.)Ig-mN8ukdB]3;ug''bC_;!DgrkQo)6meUt%aXA?,S%-82;[boJ,Yr>fUP/Ao5BRDnlY\crajo1gZ%N=Gb]re&86K&tb^uff*-bbtn(4<s6!R
MhRC8^M?"hr6-9#m4!CLoXh;$M?bXZ)hejjdKS*`3<PF65J5=KZ+@$K"NhX9&KK``5(.Nj'e?-O$XQI?0q]*tcd9V9EiV&EHtn35mn0Wt+81rBjjbYj.
phn%amU^+39aQHnS+5)[P?\"lt7SK;f-*7WGca!9l%Q&G3mIq+)i&%m3>8P)"ea@aCQEJAo2*?^%?K-/>Ah$2$(\#M(^/hO<oi=b_l6dug:37YQ<KEg>
<:PL'bc(HWo1aNS,GJlkrcI+C5Q!E-*IA?F)\:h5T!+L6hl_HTq8:t=LO]-kBUBm$^(%gtSp^i.0`@YZmF5XM=lemj5!FTr95],AmR@,%5OM&@V&pdIr
ja+8MYsk(IhDKL5Q29tT-&Otq1&"rY9X)$O2&5*B#=li$R'nk3D(NtgfD.U!B5hGdC%D(l4)C6Dp34j]3t\"TXusa.c(5:cMa]479%F.QjXEG(a)f<\_
d6-0<mRUK+,:?,?DEXE?s.gn@Ocd(J'%D:"J["";51iQeU@aCjkA7?Ih:.7\8N+Id-fmJ*/%*i<qiA/q,3&PQTKMh:Cet[*=ca]6K1r9Fgdjq`V'dkHo
\VJ,^,H>`*e2j.aJVKRpDs6Xen:C_+TjY_I0-'l9p[iBGf(^Ma\ppZLL&Cl;O`WP#>[*7e_3ij;jZS*m>GR-][dbY.P@"hO2nMUfh-MB&@Mak$YaA*ac
MR$VKG>Aou$33O9aC#?:W([*kSDE/CX1g,:j47e)ZL><nIEBT(.-TtZq+G<sk/njY-4Fq/n@d%R289tAaf.<[5_i!<3rL\*p3f*a$nFJ(%It4.E@fJ%X
Hl;gbiTI8o5D5Z4A,e4Oo1eTO3VRHO*Y;b,P#0]1$`&tE].&i0#sSq\f3m!L'S>Nm"MVl7L'hg,;[qaKm>YDrE&"r[1HqNqc]:oA@2"AQBm+WdqodgWh
K!8>YM<.Gl+aB]g5`V2VPBifYVHa,f%+Uq&+h-`SKf.?VJ24gBhH2a;a8hS>1gYeq#:Gdp6uc'''
	exec(zlib.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.46'
__version__ = version

# -s runs for hours, often into a log: don't let output sit in a buffer.
print = functools.partial(print, flush=True)

EXIT_OK = 0        # healthy
EXIT_PROBLEMS = 1  # device errors, scrub errors, missing devices, or a filesystem forced read-only after an error
EXIT_FAILURE = 2   # could not check: no mounts, unreadable filesystem, a scrub status or device stats that could not
                   # be read, a scrub that did not complete, an unreadable /proc/self/mountinfo or a filesystem that could
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

    Non-root: if sudo allows re-running this script, re-exec under sudo once (one prompt, two where sudo
    remembers nothing, timestamp_timeout=0: the check below asks, and so does the re-exec; one sudo log
    entry per run instead of one per command). Otherwise, e.g. a sudoers rule that allows only
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
    # -l: may the user run this exact command? sudo asks on the terminal, not on stdin. It may ask where stdin is the
    # terminal (a background job then stops at the prompt until `fg`, as in 0.45) or statbtrfs is in the terminal's
    # foreground (`statbtrfs </dev/null`, a pipe, nohup in the foreground); elsewhere (cron, ssh without -t,
    # `statbtrfs </dev/null &` in an interactive shell) never wait for a password.
    check = [sudo, '-l', '--'] if _stdin_is_terminal() or _in_foreground() else [sudo, '-n', '-l', '--']
    if subprocess.call(check + command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        os.execv(sudo, [sudo, '--'] + command)
    USE_SUDO = True

def _stdin_is_terminal():
    """Whether stdin is a terminal. It is not when fd 0 is closed (`statbtrfs 0<&-`: sys.stdin is None)."""
    return sys.stdin is not None and sys.stdin.isatty()

def _in_foreground():
    """Whether statbtrfs is in the foreground process group of its controlling terminal: sudo can ask there, and
    in a background job of an interactive shell (`statbtrfs </dev/null &`) it would stop at its prompt."""
    try:
        fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
    except OSError:
        return False
    try:
        return os.tcgetpgrp(fd) == os.getpgrp()
    except OSError:
        return False
    finally:
        os.close(fd)

def _has_terminal():
    """Whether statbtrfs has a controlling terminal (/dev/tty opens). That is not whether stdin is one:
    `statbtrfs </dev/null` in a terminal has one, and sudo can reach it."""
    try:
        os.close(os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY))
    except OSError:
        return False
    return True

def _as_root(command, own_session=False):
    """command as statbtrfs runs it: behind the per-command fallback, through sudo, with `-n` where it could stop at
    sudo's password prompt: a command multiCMD starts in a process group of its own while statbtrfs has a terminal.
    There sudo 1.8.23 to 1.9.16 stopped and statbtrfs waited until a Ctrl-C, showing a password typed meanwhile; with
    -n it fails at once ("sudo: a password is required"), and the rest run on the password that acquire_root's `sudo -l`
    asked for, where it could ask (stdin the terminal, or statbtrfs in the terminal's foreground); a run it could not
    ask in has none, and fails there at once.
    Elsewhere (no terminal, or own_session: a scrub start's session has none) plain sudo can't stop at a terminal
    prompt: it asks an askpass helper if one is set (and waits for it), else it fails by itself; and `-n` would only
    refuse, before it tries, a sudo that authenticates without a question (a PAM ssh agent or Kerberos) or asks the
    helper. Plain sudo has a cost with no terminal: PAM counts each refusal as a failed login (docs/limitations.md)."""
    if not USE_SUDO:
        return command
    return ['sudo'] + (['-n'] if not own_session and _has_terminal() else []) + command

# Each reply is the command's stdout, then its stderr: btrfs reports some failures only there (`scrub
# status` that failed to read the status file part way still exits 0). The parsers skip lines they don't know.
def execute_command(command):
    return multiCMD.run_command(_as_root(command),quiet=True,with_stdErr=True)

def execute_commands(commands):
    return multiCMD.run_commands([_as_root(command) for command in commands],quiet=True,with_stdErr=True,
                                 max_threads=MAX_PARALLEL_COMMANDS)

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
    an unreadable status or device stats), or None. A healthy one stays out of the table, as -d documents."""
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
    filesystems, a scrub status or device stats that could not be read, a scrub that did not complete, mountinfo
    unreadable)
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
        if not err_dict:
            # btrfs prints a counter per device, so a reply with none (sudo refused this command, or btrfs failed)
            # says nothing about errors: not "0 errors".
            notes.append(f"{YELLOW}Could not read the device stats of {mounts}.{RESET}")
            failures = True
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
            *[color_error_count(err_dict.get(key, 0)) if err_dict else "N/A" for key in
              ('write_io_errs', 'read_io_errs', 'flush_io_errs', 'corruption_errs', 'generation_errs')],
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
    command = _as_root(command, own_session=True)
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

def _run_scrub_cancel(mount):
    """(exit code, reply lines) of `btrfs scrub cancel`: the exit code is what execute_command() does not return."""
    task = multiCMD.run_command(_as_root(['btrfs', 'scrub', 'cancel', mount]),quiet=True,return_object=True)
    return task.returncode, task.stdout + task.stderr

def cancel_scrub(mount):
    """None once btrfs cancelled the scrub, else the last line of its reply (btrfs's or sudo's words, or multiCMD's
    error when either could not be run), or its exit code."""
    returncode, reply = _run_scrub_cancel(mount)
    if returncode == 0:
        return None
    said = [line.strip() for line in reply if line.strip()]
    return said[-1] if said else f'exit code {returncode}'

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
    if ours and _stdin_is_terminal() and sys.stdout.isatty():
        noun = "scrub" if len(ours) == 1 else "scrubs"
        try:
            answer = input(f"Cancel {len(ours)} running {noun} started by this run? [y/N] ")
        except (EOFError, KeyboardInterrupt):
            print()
            answer = ""
        if answer.strip().lower() in ("y", "yes"):
            for mount in ours:
                failed = cancel_scrub(mount)
                if failed:
                    print(f"{RED}Could not cancel the scrub on {mount}: {failed.rstrip('.')}.{RESET} "
                          f"See where it stands with `btrfs scrub status {mount}`.")
                else:
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
               "2 the check failed (no matching mounts, an unreadable filesystem, a scrub status or device stats that "
               "could not be read, a scrub that did not complete, an unreadable /proc/self/mountinfo, or a filesystem that could "
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

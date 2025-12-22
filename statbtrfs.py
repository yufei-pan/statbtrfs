#!/usr/bin/env python3
import argparse
import time
import os
import sys
import fnmatch
try:
	import multiCMD  # type: ignore
	assert float(multiCMD.version) >= 1.42
except (ImportError, AssertionError):
	import sys,types,base64,lzma   # noqa: E401
	multiCMD = types.ModuleType("multiCMD")
	sys.modules["multiCMD"] = multiCMD
	_SRC_B85=r'''
rAT%)=o\O*k16n/!WXAE)uos=&C4J&i'O+R$XE`ELdFUh,;[5]%l=/aQgL]knEMJj2Td\)1[`bH(.0)JfPPs3eIh*#BVY2@n9=XkOcI@DKhS;S&As]ZP
9!<g%=C-.%/0Ih=#O/1YsCX1=T[AZ%Ln2XNTcW'0qer&.B;*#ARBc\-147SBU'CMdPY2@.iA,rhT6fbA1A5mK8)nUX%5ViLm\+h]N.Y8':Wi2TuHDUjm
gM*:^FDY(CBm.A+qC2`>1]:cu9K$D]b2kWFgR^g'\i[gIC^HTuYaPXgHFSl9XXX#NRC9jbAE=,?4]cN(PrihO$tYZ5@E3%)(:D7Kje-MgI>dc#sSt@[T
Ttq8j:Q5]/9!M4T1N^.m)GOZU'&klU64#Ct]R2c'j%]bNY'nc[-Km$mOCK0X2WNDiHO,ij&mFn[24S&YQ]"6J@HVr&2"JG^mD;3E,d6A/SYlVM^BOc6D
-fMC/K#(?WER:77uQ)c1lH1,)!J'u+*ie4Dp3<!>;6JsY1$!)E`oe@oH>0hs0#Y6;NEUXCq2qgb]@*VI'W#/M!$@Z2h=Y<&o:1ML!meO7BF"+BTT*rQ#
aISaeS_ig`G0;KfPb1>\?2#bI_AgO\=&M;pk-(2XfD"2bX:2E/7.j-fKqM"9>lI.Tb_fLgF-O9(i$Q!CT40ZQ2@S"Af=,2!k"[rAmm'iR70"QBmNdGd!
FqR^H`cTtM*BC7Ze/9<RL@3,)8Y#M!\3`8L5sdTZV8R_1!ig6E%@(O9TP"&hW<eA09A:$"dm8ME2/o#AV@JeVZ^q7C87sISO2VoW>Gb'<)VG'O6Gknm@
/+Jcq@")A)N%7*Am,n-1+j)fq63^g>:(,WAr1:1)3rRlS=?jTm+Q/It`&(Boe,Dh\QbJ]kr#8:rQNFKUg3S'mRD&%06c"CD\eBBF@*ob&4inbj;:;-!A
ObH_7"\?%5sAa#:?ra*AQ>b&r("]!a0RN3AU\,Sclo*GGdK!D52c^Eko\MHgL)E8_>X#,1N3STW@O&p)<)3A@:8d"@6@[+Kii<`-)FTj5=f)7g@`Xqe+
3W6PYh?G[NR7>Emu0hHq8pk/+Bk)RZX;RX&rNMWD<^^\;Y%>`@R#9H4e,%#2J3(kt21!Y;K0eqZ*^d8gD>Bgdm^_$2ikFsEWr9H\j)Ib_op9\W9T(R>\
Q*7s8L@jPoF_pLM1(QfN'0Ja@)HBim2"=mH,X/upcHr[AL_NmB"RdY\\V,!Nlr;Y<mkk%gH"V8]P<.<NGfo@.8W]+ui9Lc-/n3e%Y3iW5J2Hg@Dqbs0(
=[f>3hO;SDHZg6FftC6Jf.YPmkQi3N@Vbt(_H<K*ta4s2j?h'-,P*7WFY*gUun$[jXi(kN72+WD3=Wtc[(8ShQ<Js-ft]^Cu_89kY`\WiKgrfXm>,g"]
pm,@Lr?o#2FrmM1\t''uDt>>*0t2Cp';b?VQ\#UtU,.q[R(@GD`VQR.!Do:jj0f(gN\iP?EFVE8H7I/WT!G8,hE>A4:['*`8A!.^We[Vp)Q/U#gFj&!m
u5Y_"CVd5(VV"S&*P)[8qrAl9=NK-QJi-b,ImMopqgV"/=djP+7/eO'A[5h%bhEAn*u-Im:Imiq@c6$+.r_F`+7\ZL3(SJ2b.jNHSDn&C-`qUuGFBMm-
L&RO0j#6S^JOO/X#)m4D\c`'X2FBVriq3?=E:A$76/glK/#i-I34(D->+*[K**^n5i7>bV3"iFJE+fU/QjP!^5-1@=KB]!$4;2>'^Aohn8XO*M2ZkGSB
X-?+R"f1u?H].$c,(]<e-MN`D:%^%]8?Kp7pZ.4NU\LR.7W+;`)"*)7Ki-9BAg!jT`3hZ+=IDCn;n!JLY1Tqb[BqkhFAod$Kr0:/F=*M+[&IOo-ksdZn
MOBgrARuQE^?`fQumE&B_Dn75)>KABeF&GK>jsNdV,;TPol.&b6qc4HlE&=4Q9oF'U"^@9<aa@AWcpJ'nX-j7YLQC6b@!^cUF[jAOnj^ksj7HRi!pFid
a$+//GNjIh(u$+gXZMMo.W.4C2Dplsl3<_3c<8\R$.K)7lF`9G1r$O`b.RciN^r!<M=m$dU(3AkWtuJ5_+:iW*euY2_;I?3uZ[Th?Zm1\"1JhW<APDHe
1Dd6;P]<VF2_PsQ[5a6i9TWF#q.&"k?3[B*A-+j"OJMRf;*h"n!!lO(uuqUZ0Ur2p>Kg#OT)G:]gB=cEAGkpn4MNR!-6"LG\_MF!k@=#IPD/ZDgM7=^;
7B\Q>'rMC=9-5o7"jFni>qO[csf^6ndRdBtoK9hShnTAU#"l"QScZGYcf6g<S"je./IQ60ITR3VXln,Z[@8J\DW%sWiDU7tsGCaduhcJmBc8VBm&M3Fk
5PLKYd<$ma!F73D2/k/T15W-c\]b\0Uda/#CLt'AH`rUJDHg35!0f-9R=g*[,AAa1O79:6fnB1'fP5F]%QHA5_lgdHLTVQ<.FQ"H@bqD2T^s)HoY=bZL
SQK1H0*+\`L%JZ=fR%kY,,1KHcH@b=k&_5N)D<85uK"5fY:U9a@K,*/XQi`rrIM8LOISo;ickU'(?h_IT;4lf'SL58i[Psnl0iGheGV7o/5uSD8EQgHb
b5IA1"K!"jlrHW!,\(:gcGWUQ_s.(WUQ2`h>:<>qu<WJ!gU>:UQm.G9E&(iY383Ojg-NWpM@e0Xog&k_/ok`Cj'%)<?ig'K<D%-R?qZ\=0<fC6[l)Fq[
aH$Z#2>0=O1i_+gWmfhMui2[D\rZG>uP/_TX@I=W5DZ2mKjfe7Th[d;W9:n5Xf*eeH3fHg$CeLFl)UDGU/9ip@d\HYAK=]7JfhZH@6.7k.+=^8.=NFW+
$VWB_[@47iH74]P4LZehRaHLN>ZgA#1#Sap6'QX]W+cpb9W\0]_:h*DnbqFrWGW:E%)tCA5#0,_'=f7hZ]btG?=raDC>Q6];cP?bsW9hS;m^ZltHCS';
A8$CoShZIKZe1c%`GnsM"-9i$ER4-99)C$U5+R^g,;R8M'+pEc(4V.MO[OHK_oIQSK=`Zt5!q\KQ8TYAj/_+VI<\@AE69dfpAL4]l6.Z77#o*:d)3!mk
11.%iVlTbYG9Q:hjoBJB%kSX"t#Phd9R@cYA?Ec5]u_mqr)!'"isjWO--MVQjoB,@MqO,U]f<lCsi\-e'IpD,>Br(=?E:33R.5>``JHnTZt-.$b-&jC0
)F,5a,ka_J2uZF[kF8b==4;m5Ap.R8ARVSM6VdTs,%[ggUONH?j;j*8U+D/JMW'G0:3TVDH'!["nMqBCdCJ;jE+&.%nY^5AX6[2>aq*@k!hT<tZWE(_o
[@HjJZ$"7[*]2sMbe!le7GoFbRBE(;5tCaDfrUtmua9*jE=AVO>9l8H<9`qi8!:L>I)3.]-k)/BN=oVN!r$-"bDW^Fh.ns`DfMp!<5`O_3Yfu;+dH<<%
pH?'k_g.0jbOh89I?"mpqT8Y?$A-I(lH3<X2WD"L!fBB6A?"da'@4&q5\$&mWppSiE0tkfYRoHG5ojKR,H?H5=j2]:h+],C"7Q*k`rD!_R%,U(K69hjc
:-!r^,uH9/?:;j9c;A1?H3#cn)gmnFeGS/R#r3th'nX(YX9j=*mW2<UID.XqH/T/r$O#3Z,1o"#;0I4[jXb?YmMRF_JY^$-5T^ci+BJM.*/JXTTa[Ee2
Z)[n&0SkulUa4Wju*LKR/kS9/7rGRP'G!ALQF$dQcPdTQHNMh3TboQ$\<Xu8?Qkrk^l/O(6_kn<i5gI=-c5K_j]-3ajs8`R\otSFu..5\W-sOJ^/+dD)
h7DZ-BaHFMPV9mbqnDCnX53\(qG1]Uq].gT\".-g+_Qs$V2aB&#,T=q2pV9*3=8K=)2jE?`Dp(-Z.j^(`J"Bh;N**)Hase]:RB$r"::a-!:S`^N*C%SD
Z;+A:Y!qdRkXXW384C4l6?mt;eEe^9<FF_Ie-Ot]NZN3^t>]i)r0&3?j&S-/e^NXPt%l^t.Tottg\:[MSkaX)T7haP,pl:C=]m%bA1"Y'/,Q<3Her<3u
jl^e>YMC!VsQB1.<buV3%qoRU%LL>+Rk@ATo[\f<OO=$+MmKD"_ha:2thsDXcr>cR_oZ2JYrlEKgNf*\&eg5_gE7)IBH+=D2LRX/';q8P9(=C#8]JPi-
NP%b\rN'=cQODrBoYF/hA)bcH&Zjsl#WCZf6[9.VHlpPP?fg`)jkHqZiH/oZl<R&D,31H8ZH!M9/Cg$sbYZ1k,LUTH8\WR2UJP">ZmD"K38k``ji`'#"
E-Rn_>%Fr8&nm`"Hmcr%]CBBiIQ"!@8qi5^UkoR+&<S`k9CUBORnC(H""'A>9gTS24N/*4_0C1TV&7]&UrO`1CXYU/NG<://?SM=mQJ#T-/<':0tjtCh
rD39&K&6'&k0Edt\If<6m7[e>ea:BVq+Y;T6]0YbOc+hqAmAkPOCNG,*;aJ,MI48+#sQ+#3^+aT`(;KBZ+94uZg#<KjCH^;3*<+?e&nT#/RpI4UZq,=k
*qAV?u"XCFS-Bh-`c5#ajkLJZL@kPW44I%#tc#j\t"^XpPi0PSX1XgA<Y4<\UmQ2FCl075Si:&h+u3LVq'md,hm\#f8;aBA:cTA&9V5IX-/H<f/b,iS<
.:-*&e)"IGRg1Zh1/P#CcS%eIc2t[?(/R;\0V/N"jaq%go,rn;]EhjWY5)1V],KYJKO_+WBEnALDqF7!+-.9cPa+\YQ`6I6:ca]NB_^7ep$P^&=ZbkaK
hb:?1.h4g;a56S#rfMXWZ-@ERhU5Sjhgb<7/bD%cKHZ=KQQoCJ\E%Caa>_r9g0f7(7E?9O?18-9"H)X.]Ce92^0Q9Gc:(!Vf=dR(V0J@_Fj)>a3Q,h'r
;/UcNp^<Eak][t(4qo<h,WVjEc+a&)d^e#-$KX':u*_M_jFc_l+P\,>snZf35<^ra,HpccqB55%pM@g3%WJ.9mj+($l_("Xo(hg.DMcD#Z1RVRCiY"d1
75aB:YM;.t:-EcD#l26k\P\RsQuc^/]3/e#"MCr<@r907^iW4mQD;66dJ19o"WD`S'`^82QB[KG,f!0T3j75Y;;3^ea[l]CIO-^@o^QmGdJDD#mFqU\5
7Cht9DHCX('uI84rKR-B/=q5XjOZ@L;=QK6`6n::hsA"uEQm[EFg.XcRrY+M.Kl]*m]`-n-@R)EMjfYK5ECT4e>mCsno5,iKS!d7G^EJ4GBL(?!^..$)
<S?F_*PTHop<V!:i8&r&5UVrq$a<G$R+&4k2]p>6nqX0jm?NrDF>BZV=T0!FmlD%2BQu_K]TW%gH:h%4YZqcb0:cracEi"),9tIA+Pnt'hZ-@o1SruG]
.ouX0[adm("!`ZJOu'p'21ik8S'9e=CDUoVr^6g8H!KNc<+VSrfK>MTlht^`VD!HW"Ri8\9CX9WTp`*_Sa^;F_DU>Y+B<glO#boY"CJJ"aB/r3d0ua<j
O3rV[IiLlOU=[k6`ep7,+:=Y3J;rJ+9PVm#%)1+)0Go!JQL34j(KW,%saG^EEnJ>QE\ha,s8MUa/5Pi_Zp!XbuJ5hX`'S_SAnSJR8q@.F-BCN@_fKE,j
@2+5IhSh%W)]1];3:*6ue7sBQG5q6?qRoZZ2)<Ncg0E+2i&mKt[]6RS'pD7l%-LMf>abN&&sF]9C+7a\s5lo[DWsa?mkP*`Ocjs-b>FVE!LsC]+h02G;
dk,"7LF=_$qHP"TN1X^XE6P+nRb`2Q6g'ri=$+,.ug`W"ZA%nSPcPS%Ro0DbPW8,=u2QnHMB\Z5GTnr"R>MU@s5=gbV.;&dHlHI2U-LBRiZ(Ch4V\,nV
5$T5+U.=eV7)[iThAM0-n/P)sHqm.b%^[)Q=PX)_@6oYd\O6W*Mi"o^EhPSt*PV4At5GYdRU4X=3'G=OALad&<GH[8"8n%O<;Vq-0q"[%?e`GUflU<.i
F->VUn!cfff)qHlRM8H^(<[_)00DL_2)gn?s(G:',/_6H@XCW0l<qlQm&)oU\eR=.++<@/gJqJD(7FfsQ0HV?([;Po*dJ^iO$DBD;u9_IGS$hiUus]US
Xne2DG@Jc@2mP%UXB`OU"NVclqIMhg3UZI-q#oi99MDL"%=Jn=6D9ki1`/!Y>)*m4AOEC<-SBqM,#@/@T_a]ka7k>k2f8#)<[4lOgU8dXe4YF8,PeDHd
^2\5eAg(%qQ!.a0VbDG[_[q5<F_t62qCcUX=s8lU']bVO8$d#GWBdGMbp85B'L3On,8(l^g?V^378\3eC_tnFJ48-48_lJ$qs:\n^RW#s,\+F+MM"75,
p%VT!S)IO@N8>uoWtL(p5e7EEP2=Y'1%2Fg3(97n]O.'9fY3.]Btl`Q)2P?jqBcC;+=n465;J0C>G]5d5*`@ojUTuMa:^+;(^';f<I-=&);7YK"]Qh>u
ndqtEf3I.pagjfq=n@Yp#([4CM&SCmiSe!1W@;0mXr9onp"PN<[j,)G^7l85)A]*X[NC^qdGJ2IiGF53W?K,5R]Glmfl\',D&WBNC$%[!9Y)VkSKq>bO
D`7*@)>d<jd[9Uh,Z&p,#3=)7LPBe*(4p;FWnd/>c%FPBp=c>\meH/e:EVr;,=>@('<lt1;#<f%r*7TedR\?q/JdTM"a0'u^^F[QajNRfG,/.e189<4=
D^9<0f!,bhnI.G->c</jK-k\3Ltd/?]Ff0?LZ1]3U3]jLRL$5??G)`3[GeQ"RZ6XI$/(p_R0\t&64[d6,dM(*_7Q9.HpjqbmZ/dgo(HKJGhBTle.N)IN
hiaTEDa$8gLoa#bPE9qQ,Xt!.H8^O5CB70_Xs`Z:trDs"D9F>8&bXpBcoNqX9H2C&QU5V$84p32?fkcC1`nbYKHYe`m'*^q\c\l1YcGq*C-Ujfrrti:#
^RQqiW,-8%O4cpjqJ`fA>C0,'V6JC9U`#a;Z#]re"'7pfs!,-%AM[X(LDlq(n_J%pA;Rqd-rl^`jh#5H3?n+lL-:g.@D$%[!Ag:V1c@"-]oLNQTIgm/i
^^e!5,_Ib=LR@_Q=Lm:O'3'D>DmifOXJ'q\+OSD.H[#kMVjO:bC!JboUoq98A3hp,e&]CZ*qg9DUD,1VY#Kj#DQ3G/nQ--N=Xe:RNmA?=4`!$\;gXhg6
;!$:3@iRH''Jf'Vqb?^e94&(qbb)BTp65k5r6Sm3Gl>E1R.g!r4OaqHH([c.Qm5:+>7RoHXFnp%C23[8=Ja18f(ZH7\re<bW-h_Me9%A!N[9.diR$iZI
Nl_ljI?rO]gtK2E';6*(Ojtih67kA937_<UA9l-^R_D7]&VircFdU>Q\F?g-kia\(LS>uK+STaZO^MlBjJ9uFkr86[F@k!^CIKP[#0Z3.=`9DAO'AK70
d\o=S<"qi&MSB\aIoJ)[VI+gX>j<_E&IGf>M"*rR"7'=&q+)]&B//Ad++fSb)R.<TqA@'#3=EQ93g@!HuObmke**M94E=@b&VN5eZltEeZSC<1lV_aYI
%BqT?l[h!]$I0QSfk+fqQ,&b:<_3I_Q4alF@oN5;d2AFojJQ;<X%iiC%bnqEP8<ae[U^#M=&"P&4@fS%As<&C+tj%S[]<b2"6=A1id!."VF1)-K2HNpa
)!!/uMU4iUJ8mOKNZ,C;P!WW3#!!HG.'''
	exec(lzma.decompress(base64.a85decode(_SRC_B85)).decode("utf-8"), multiCMD.__dict__)

version='0.26'
__version__ = version

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

USE_SUDO = True
if os.geteuid() == 0:
    USE_SUDO = False

if USE_SUDO:
    #check if sudo is available
    if multiCMD.run_command(['which','sudo'],quiet=True,return_code_only=True):
        print(f"{RED}sudo is required to run this script.{RESET}")
        sys.exit(1)

def execute_command(command,wait=True):
    if USE_SUDO:
        command = ['sudo'] + command
    return multiCMD.run_command(command,quiet=True,wait_for_return=wait)

def execute_commands(commands,wait=True):
    if USE_SUDO:
        commands = [['sudo']+command for command in commands]
    return multiCMD.run_commands(commands,quiet=True,wait_for_return=wait,max_threads=0)

def find_btrfs_mounts(filters):
    mounts = execute_command(["mount", "-t", "btrfs"])
    #mounts = multiCMD.run_command(["mount", "-t", "btrfs"],quiet=True)
    btrfs_mounts = set()
    if mounts:
        if filters:
            filters = [f'*{filter}*' for filter in filters]
            mount_list = [line.split()[2] for line in mounts]
            for filter in filters:
                btrfs_mounts.update(fnmatch.filter(mount_list,filter))
        else:
            btrfs_mounts.update([line.split()[2] for line in mounts])
    return btrfs_mounts

def parse_show_info(info):
    fs_used = None
    device_path = None
    uuid = None
    for line in info:
        if "uuid:" in line:
            uuid = line.split("uuid:")[1].split()[0].strip()
        if "Total devices" in line:
            fs_used = line.split("FS bytes used")[1].strip()
        if "path" in line:
            device_path = line.split("path")[1].strip()
    if fs_used is None or device_path is None or uuid is None:
        print(f"{RED}Could not parse btrfs show info.{RESET}")
        print(f"Output from btrfs filesystem show was:\n{info}")
    return uuid, fs_used, device_path

def parse_device_stats(stats):
    err_dict = {}
    for line in stats:
        key, val = line.split()
        err_dict[key.split(".")[-1]] = val
    return err_dict

def color_error_count(error_count):
    if int(error_count) == 0:
        return f"{GREEN}{error_count}{RESET}"
    elif int(error_count) < 10:
        return f"{YELLOW}{error_count}{RESET}"
    else:
        return f"{RED}{error_count}{RESET}"

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
        "error_summary": "N/A"
    }
    for line in lines:
        if "Status:" in line:
            scrub_data["scrub_status"] = line.split(":")[1].strip()
        elif "Scrub started:" in line:
            scrub_data["scrub_time"] = line.split(":")[1].strip()
        elif "Rate:" in line:
            scrub_data["scrub_rate"] = line.split(":")[1].strip()
        elif "Total to scrub:" in line and scrub_data.get("scrub_status") != "running":
            scrub_data["scrubbed_data"] = line.split(":")[1].strip()
        elif "Bytes scrubbed:" in line and scrub_data.get("scrub_status") == "running":
            scrub_data["scrubbed_data"] = line.split(":")[1].strip()
        elif "Error summary:" in line:
            err_idx = lines.index(line)
            error_text = "\n".join(lines[err_idx:])
            if "no errors found" in error_text.lower():
                scrub_data["error_summary"] = f"{GREEN}OK{RESET}"  # Green-colored OK
            else:
                scrub_data["error_summary"] = F"{RED}{error_text}{RESET}"

    return scrub_data

def issue_scrub_command(mounts):
    # print(f"{YELLOW}Issuing scrub on {mount}{RESET}")
    # execute_command(['bash','-c',f"btrfs scrub start {mount}"],wait=False)
    # limit the number of mounts to scrub to max_scrub_count
    scrubed_mounts = []
    for mount in mounts:
        print(f"{YELLOW}Issuing scrub on {mount}{RESET}")
        execute_command(['btrfs','scrub','start',mount],wait=False)
        #multiCMD.run_command(['btrfs','scrub','start',mount],quiet=True)
        scrubed_mounts.append(mount)
        yield scrubed_mounts
    return scrubed_mounts


def main():
    parser = argparse.ArgumentParser(description="Check Btrfs filesystem status.")
    parser.add_argument("-s", "--scrub", help="Issue scrub to all pools", action="store_true")
    parser.add_argument("-i", "--interval", help="Interval for status check in seconds", default=2, type=int)
    parser.add_argument("-m", "--max_scrub_count", help="Maximum number of scrubs to issue at the same time", default=32, type=int)
    parser.add_argument("--scrub_command_lockout", help="Lockout for scrub command. Used to block two commands sent quickly.", default=10, type=int)
    parser.add_argument('pattern',nargs='*',help='Patterns to filter btrfs moutns. Default="*"')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s {version} stat btrfs by pan@zopyr.us")
    args = parser.parse_args()

    btrfs_mounts = set(find_btrfs_mounts(args.pattern))

    # If the scrub flag is enabled, issue the scrub command to all mounts
    if args.scrub:
        if args.max_scrub_count < 1:
            scrub_count = os.cpu_count()
        else:
            scrub_count = args.max_scrub_count
        if scrub_count > len(btrfs_mounts):
            scrub_count = len(btrfs_mounts)
        scrubber = issue_scrub_command(btrfs_mounts)
        for _ in range(scrub_count):
            scrubed_mounts = next(scrubber)
        print(f'Issued scrub to {GREEN}{scrubed_mounts}{RESET} mounts')
        scrub_start_time = time.time()
        #print(f'{GREEN}Scrub all issued!{RESET}')
        time.sleep(args.interval)

    
    while True:
        header = ["Mount", "Path", "FS Used", "w_err", "r_err", "bit_rot", "gen_err",
                            "scrub_status", "scrub_time", "scrub_rate", "scrubbed_data", "error_summary"]
        table = []
        running_scrubs = []
        if not btrfs_mounts:
            print(f"{RED}No Btrfs mounts found.{RESET}")
            return
        for mount in btrfs_mounts:
            mount_dir_name = mount.split("/")[-1]
            if not mount_dir_name:
                mount_dir_name = "/"
            # filesystem_show = execute_command(["btrfs", "filesystem", "show", mount])
            # device_stats = execute_command(["btrfs", "device", "stats", mount])
            # scrub_output = execute_command(["btrfs", "scrub", "status", device_path])
            filesystem_show, device_stats, scrub_output = execute_commands([
                ["btrfs", "filesystem", "show", mount],
                ["btrfs", "device", "stats", mount],
                ["btrfs", "scrub", "status", mount]
            ])
            #filesystem_show = multiCMD.run_command(["btrfs", "filesystem", "show", mount],quiet=True)
            uuid, fs_used, device_path = parse_show_info(filesystem_show)
            if uuid is None or fs_used is None or device_path is None:
                print(f"{RED}Could not fetch complete info for {mount}. Skipping...{RESET}")
                continue
            #device_stats = multiCMD.run_command(["btrfs", "device", "stats", mount],quiet=True)
            err_dict = parse_device_stats(device_stats)
            #scrub_output = multiCMD.run_command(["btrfs", "scrub", "status", device_path],quiet=True)
            scrub_data = parse_scrub_status(scrub_output)
            if scrub_data["scrub_status"] == "running":
                running_scrubs.append(mount)
            table.append([
                mount_dir_name,
                device_path,
                fs_used,
                color_error_count(err_dict['write_io_errs']),
                color_error_count(err_dict['read_io_errs']),
                color_error_count(err_dict['corruption_errs']),
                color_error_count(err_dict['generation_errs']),
                scrub_data["scrub_status"],
                scrub_data["scrub_time"],
                scrub_data["scrub_rate"],
                scrub_data["scrubbed_data"],
                scrub_data["error_summary"]
            ])

        print(multiCMD.pretty_format_table(table,header = header))


        if not args.scrub:
            break
        # issue scrub command to next mount if there are less than max_scrub_count scrubs running
        if len(running_scrubs) < scrub_count and time.time() - scrub_start_time > args.scrub_command_lockout and len(scrubed_mounts) < len(btrfs_mounts):
            scrubed_mounts = next(scrubber)
            # print(f'Issued scrub to {GREEN}{scrubed_mounts}{RESET} mounts')
            print(f"{GREEN}Scrubed issued to {scrubed_mounts}.{RESET}")
            scrub_start_time = time.time()

        if len(running_scrubs) == 0 and time.time() - scrub_start_time > args.scrub_command_lockout:
            print(f"{GREEN}All Scrubs finished.{RESET}")
            break

        time.sleep(args.interval)

if __name__ == "__main__":
    main()

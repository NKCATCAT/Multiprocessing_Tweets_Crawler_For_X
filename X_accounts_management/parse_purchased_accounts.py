#%%
import pandas as pd
text = """CFields98292----Ebw0Wuosgv----anthonyedjdz@hotmail.com----Ebw0Wuosgv----fcfe24d9ff64c7a8ef113bad267689fb68c3929c----henduohao.com/2fa/HJYGHROLT5MOZBHK
MollyPatte69152----sJgocvf6ag----daniel4ltubarnes@hotmail.com----sJgocvf6ag----2425d2157ae30aa6dc445a99c5211e3af9699756----henduohao.com/2fa/Z6KQNUKRZA5XCV3M
GretchenSt84168----a5HCtp3ivV----thhayese1@hotmail.com----a5HCtp3ivV----85fc7693f3d21d90bc770aca3ba2014df7dae104----henduohao.com/2fa/NMBZAZRXFTYXDYIV
adalynn_ja20180----Z143en7aLA----ezraburnsfzp@hotmail.com----Z143en7aLA----a7207401133415924e498392d91d4c93d1facb0d----henduohao.com/2fa/736QTFMJNK3VCBYC
RichmondAr82708----c4b4aoRK4S----mateohuntcs25@hotmail.com----c4b4aoRK4S----93aa59ddf00c488eb740c11dfc65b327b66536e8----henduohao.com/2fa/67KXKHKUQG5DB5ZI
MylesCobb17787----oVs8aaPb8p----charlesvgken@hotmail.com----oVs8aaPb8p----4a821f1b6e5a3f0d090aa2f60db8d4f7e66ed201----henduohao.com/2fa/WJMCEFE77MVTEHLT
BentonFabi3943----whFKnfv7oDR----johnburke0ifm@hotmail.com----whFKnfv7oDR----c741b643d129eb203dce00cb3e98b76f396267e3----henduohao.com/2fa/NI4IPQ2WFYO6WCJN
DavisMarle35278----OCeLg0jC4D----ales9ynnelson@hotmail.com----OCeLg0jC4D----96df50e92c0d3806acb656063b6b1bf113bf3cbf----henduohao.com/2fa/JCTV7VAEUKGLGNT6
HurleyKael42511----D7o6el4k----ezradyportega@hotmail.com----D7o6el4k----93d347f1239633a201265c32410dd42698c7fb5c----henduohao.com/2fa/NJQO23BBHZIMP4YD
AlexanderR3177----sJ9Jdl0lFt----leoarioburke@hotmail.com----sJ9Jdl0lFt----4fa9b7bb5ce9b249da0780044fd4e78bb66815da----henduohao.com/2fa/WJ7TNBPFAFD6RHQY
EFrench73592----F3u6hd131s----josephmt51cruz@hotmail.com----F3u6hd131s----4c969088f3e3b2870ab7c2d5fcab4d580d430a16----henduohao.com/2fa/P4TF3UDSDJV5QHHW
AlecSulliv58916----dpqwJ5763----loganr9dunn@hotmail.com----dpqwJ5763----cb2505e20d98738e5537b4ac34ec0c56debdddd7----henduohao.com/2fa/HRHGNVW5JTXWSKCW
holloway_o89245----wbFA47me----aidenzgeopa@hotmail.com----wbFA47me----d66bfefcc7c93cba64de4612d778fbae3b21626a----henduohao.com/2fa/KORPQ62TUXL5ZTG6
RoselynBow57442----j4kzc1CTW4----elijahkingeo@hotmail.com----j4kzc1CTW4----16e2ff6f35a9cff4c1e2377bc784a7cd6869a741----henduohao.com/2fa/DZSMK6UOFNKYILTE
kiera10934----aOK8bn35----aidenking0393@hotmail.com----aOK8bn35----c797de8ae69d2172638b48b743870b1bb1486bf5----henduohao.com/2fa/VPCVZNWGBZRX7B2Y
brennen34687----Ia78q38g----oliverherxhm1@hotmail.com----Ia78q38g----cc8c133ce11e58ef98dad48181636b068e35c93f----henduohao.com/2fa/GAIZVEKPQYFPNMMR
kamryn_wol42056----S1OKtici----jack6yor@hotmail.com----S1OKtici----6f71a64b15c24496409f974baf75ad0883945e90----henduohao.com/2fa/UTYBCMUF3NBZQMPH
clayton_mi9737----rofMvoei8----danielm89grant@hotmail.com----rofMvoei8----0594a89919ec4e32517e9ed76d2e342820315768----henduohao.com/2fa/NPFNIVAT6DP4WZCD
RishiLuna173796----Et6Kt9H9----g80jharris@hotmail.com----Et6Kt9H9----33f6496a1ef1e707bb80dab995311c9d16a42033----henduohao.com/2fa/BDZJCESJS27AB33T
NobleLaure4024----Xy2NsrPv----jackperez5n5a@hotmail.com----Xy2NsrPv----fe923948167d35319194ae12c109cc796dd2fe32----henduohao.com/2fa/S2KN5ZYVQNNWHW6O
banks_mace32961----q818m325A----jamesdavisrj2o@hotmail.com----q818m325A----35beed145195dc900de56fe15c8a75a2fccf65f1----henduohao.com/2fa/YVCPMFCSRWTNLURW
BrentCerva10792----jBZa9y3r2----johnt6x1hansen@hotmail.com----jBZa9y3r2----ca68c2c5791217d836806f84d8e777cf3ba48ac5----henduohao.com/2fa/3VB6OV2G3C2JBXIC
MeganWood224248----idZ6rTa41R----josephroblgt@hotmail.com----idZ6rTa41R----00a473dc0439b29c060b1140ab040fe9f2381453----henduohao.com/2fa/ODR34DBUSNYR3TU6
JairoDa5009607----cb2d0sbV----benjamin2djvma@hotmail.com----cb2d0sbV----645412d205c405bc9c9d1c280beeddc9b6084a38----henduohao.com/2fa/B6UNFX2CSDU27LFM
edwards_hu86197----LvfeGFj7----liaml8jj@hotmail.com----LvfeGFj7----dc2f40c2dba7b3dac81d6fc03313aea56a693df2----henduohao.com/2fa/DLZEAXCS5H7MU3WM
LondonSant70237----lY0mbti3----leobutler2vv@hotmail.com----lY0mbti3----2cd69bc8898a30cf9036e00cf9c08699436803dd----henduohao.com/2fa/OOYMQ3Z3KRCA5IGF
HaasMarque68933----S3Sq7QjlhH----wyattkpazste@hotmail.com----S3Sq7QjlhH----6aa203d6090675cddcd47f9daac65dd590c9d98c----henduohao.com/2fa/Y4FU2Q2E3JIRLX2R
DylanCross23246----LMAaJ3G9----michael7pmo@hotmail.com----LMAaJ3G9----ec9bdf4a98169cdd3669ef723ff84170a6070b1d----henduohao.com/2fa/SBC5MVKQVH62RJXR
KarinaCool99925----dksFc9C9g6----ezracarter5i8x@hotmail.com----dksFc9C9g6----0e9286c63efa3dbc959b97c29d657ab5441d6e95----henduohao.com/2fa/6CGSM4FNDRHV5XS5
DavonGonza50294----V74y80Xm9r----jacobgeorgeucuc@hotmail.com----V74y80Xm9r----46ec5da1fdfa6abb59db4b95c857776fa2e7b1c0----henduohao.com/2fa/3Q6P4BIO2NRDCPNK
VFoley48541----HAinra6Bzi----michaeloyfr@hotmail.com----HAinra6Bzi----1baa4f2f696bee473ddde6c12e6f86d01a88f802----henduohao.com/2fa/YWULPVM5SQFT5GSH
JayceCleme47739----U9kQLvsR----davidootzs@hotmail.com----U9kQLvsR----8901cf6b1dc3e9f94731b817c81dab7ec9a8bb16----henduohao.com/2fa/472R25F2CIMQAY2Y
AlvaradoLe2743----DGj1esz4UI----tguzmanoi@hotmail.com----DGj1esz4UI----a95f160d4e06f6c4ce5a7afa335b4a7310fe2ba5----henduohao.com/2fa/T5ST6NC3NR7QEEYU
nelson_les10357----wnvxRIcqg9----jacbarnes2gim@hotmail.com----wnvxRIcqg9----8a4ccd77319de37ae9085389f70834f457e8f91b----henduohao.com/2fa/3TYW5JSKEUESSPMU
KaileeSala95409----st2P5De5----eliasgutf669@hotmail.com----st2P5De5----3f4e80d1010178e9f24bdec9397b6eed0c39fc51----henduohao.com/2fa/64UGXJVIAZLAKLJY
YeseniaLi161741----iW5q3ngUk----antrileyad6a@hotmail.com----iW5q3ngUk----454d3c11c15319a9aea33f77aa2e3cd363509d49----henduohao.com/2fa/36PNIA4KWOVP2765
PrestonSha57430----rr2Ga3rs----wyattvgkweaver@hotmail.com----rr2Ga3rs----b95cc4a9a1489dffc19b80206672013106d72eb7----henduohao.com/2fa/TZT5ZTGJSWJEXA3E
CarlsonMel29408----TROyY1ikq----wiltorres3n3j@hotmail.com----TROyY1ikq----fc0303bc47cb994357f65897c36cc283eff4a13f----henduohao.com/2fa/WYFLNK3EZKKMFNHV
DelaneyFox30934----GW0cmquu----lukeptblgreen@hotmail.com----GW0cmquu----c1d666cc5b392eacb34e74eaafbdc393be512a39----henduohao.com/2fa/VCU5LDHNRCMGDJJG
HahnMaddis90115----iHKkZfaO4----isaacpeters9gw@hotmail.com----iHKkZfaO4----601a549f3cd60788690fdee1d8084f5da33809db----henduohao.com/2fa/ED5XBBJO2XPM6UZW
desirae3251----vMp9gA9t6----davids8acr@hotmail.com----vMp9gA9t6----7e781795640af8b8ad833425e97ab98b192536d4----henduohao.com/2fa/MARHVN6QWDOSR4NM
MasonJasmi89632----fuz8ghaB12----aqbellis@hotmail.com----fuz8ghaB12----e45c2a916c044ae738c2764574abfd3beb64ded5----henduohao.com/2fa/DQJQ72R6AKIFA4S7
AlexiaStep49514----V0a13J93----josephbdzpena@hotmail.com----V0a13J93----8019b3edfb66db71786ea2cb035ca6f46837745b----henduohao.com/2fa/X2MLP2EVNV7JA3UV
AbigailPet16326----HUmEvwxn0L----antchentx@hotmail.com----HUmEvwxn0L----511a3fff075817acccaea48fbb3d73f8c99d9735----henduohao.com/2fa/CAM4VHA4O5TFYTYC
SLester22438----gd9pZEoAh----chakimdm6l@hotmail.com----gd9pZEoAh----666ef07434b79dae19a24af0357b3dc9cf1a7476----henduohao.com/2fa/FQXFEECXA33WNRVL
JerryRi50614764----rku0b3wSh----asherp9onunez@hotmail.com----rku0b3wSh----18f1e87a6b968954e27890292b6c9f8e0ac31a3d----henduohao.com/2fa/F6TGW3KYT6KMUIOS
RowanR66801----XmqSfed56----sebastianjohwo5@hotmail.com----XmqSfed56----173a5dce1dd3f22606b4b6fbcb314f35c09a32cb----henduohao.com/2fa/35VTWTOO4CDXHDGB
RobinsonGr1384----mMw2zo8J----aidenper468@hotmail.com----mMw2zo8J----3f9560ffebaa522beb0dac2d514b79ff32191833----henduohao.com/2fa/O7UJQPLWZ7BNLWYQ
LanceMcint73400----C0E9rgq6A----williamkys0@hotmail.com----C0E9rgq6A----1997e324d6b89776d54d0aba4bc75b1364d62c01----henduohao.com/2fa/DA4PVCNXU7MJKGSL
SpencerHen1032----WoDpfU7fUb----leowhitee7@hotmail.com----WoDpfU7fUb----e412ea2ffe5560473991e2a5c60d48f121350708----henduohao.com/2fa/OBJX2CXIS2XKN7OJ
JoshClark818065----UpYYQwg0----brice5l5@hotmail.com----UpYYQwg0----75ee2f9f6f2944cb528557abaeb01544edcf2204----henduohao.com/2fa/6ZHZSELETTVHUNNS
HumphreyCo56255----rpFB3Jawk----jacobf2hsrose@hotmail.com----rpFB3Jawk----fc8658c7b654ac1a140593b14828906c04db7661----henduohao.com/2fa/YOVMFOW7PEVMNJNF
day_reid51685----upoptkRe5----daniel1qstaylor@hotmail.com----upoptkRe5----eb7d267a6a68a3387d422263fc702970d689a6fc----henduohao.com/2fa/SYHBI4LK3IMYB2HC
montoya_am69333----Su4h0SXr----jburke76t@hotmail.com----Su4h0SXr----a4e176db61ac9f879db2c4977f25f73e2a76e334----henduohao.com/2fa/4ZSYZX7FEMVJY5VT
WardSolomo84190----DtvZ1Olf----julianhicksye77@hotmail.com----DtvZ1Olf----e708a56a672a6277675b1c40569c0e32b0fff3dd----henduohao.com/2fa/GO2SMQCJUGTUAOTA
AlyssaCont79817----Eh4lvRFU----davidkmchavez@hotmail.com----Eh4lvRFU----7dc95de5fe4a014337ce0d7adf0f14be82e76e61----henduohao.com/2fa/AR7ZKE2NWL7EASI7
NataleeLyn12798----ir8Shnv9py----hudsonldmills@hotmail.com----ir8Shnv9py----0b0c207bf55e9881c435985ee3efdcf233ab5d75----henduohao.com/2fa/W4HBPJGTHF43DMKM
RomanJonah40609----ZIZp0R859----mih7rogarcia@hotmail.com----ZIZp0R859----b62f44d56cdd732fe8e6993a4cf1122a57ce2bb2----henduohao.com/2fa/OWDI6WQU3L7DOYG7
AlysonBald9026----nTx91T0hls----levit1bell@hotmail.com----nTx91T0hls----15ff8b45eee603f5f628ba4b8f5f4bbcc89adac1----henduohao.com/2fa/LKPENPUWJF7FV6VF
GentryGabr33180----slj3J1jh1o----lucanp1hortega@hotmail.com----slj3J1jh1o----8c7f607fbd3600b6c370d59b592fb6246e4d1740----henduohao.com/2fa/HZ4UNRTQKMPRIJBQ
JerimiahSa85542----cdC3iVw8----litorreskk@hotmail.com----cdC3iVw8----59c078a159afab42db6df57042602102433663d8----henduohao.com/2fa/IS3ZTY5U22RDPND7
kason25845----kim8Po3X3----logandijcde@hotmail.com----kim8Po3X3----af23b660eebf7fcea7f119f2d010d0532777d2ae----henduohao.com/2fa/UI5CHTPESXD5JMWW
FlynnJosue63998----uDWxc41cc----henry89syholmes@hotmail.com----uDWxc41cc----c21bf64465b30523b81b8e54129b85023bf390b6----henduohao.com/2fa/2U4ZADA6J3MVXQOC
MaloneEmil99671----funggZ2Xw----dylanjd4rus@hotmail.com----funggZ2Xw----a10b9c4d023712850efec169c0559a8bac3aa583----henduohao.com/2fa/OYRTI3DAWUDHTMWZ
KayleeGlas28018----kR7i74xy6j----jamesw99ged@hotmail.com----kR7i74xy6j----f1e54d55ee9f90d78a0fe36bfd0ed8609a653e6f----henduohao.com/2fa/YCZB3UPRO6IMLUL7
love_brend99068----o60n1Gum----davidg730w@hotmail.com----o60n1Gum----3465e10e0fa2b0a660f1044c291456655a3ec4aa----henduohao.com/2fa/PV5SYPWROX3CE24P
MessiahGut46104----szG6lUuz----isaacsplpw@hotmail.com----szG6lUuz----76eb92f9864388f952638de74e80b60ab50428f2----henduohao.com/2fa/7QUPEMOGNCBPYV2M
bria_green63260----Zaq638p22----wl83rclark@hotmail.com----Zaq638p22----a2826cd5f64addfe6dcc1219d1a9fb42d7c0a296----henduohao.com/2fa/N63EOKCHAF7FFFRM
TownsendOs6300----qmO8dbewfh----josiahcox7hq@hotmail.com----qmO8dbewfh----c47ffe3bd14ef4b47dd91b29683b73926c47386a----henduohao.com/2fa/EY3WSUME6QJ5MOYG
FranklinIm7735----q61V6t90----noahr1unx@hotmail.com----q61V6t90----45f92a9db8a6a806019f513264bd83ddedae44b9----henduohao.com/2fa/6WOMP2ANF3KLBHRD
hopkins_ka70133----vIP1vde3t----aidenhhcarter@hotmail.com----vIP1vde3t----553e87540a924205093878c90f05b3b9fd551b51----henduohao.com/2fa/EUV5L7TRSENR3JJF
WrightEmmy21559----r42yxmeT6v----noahfjnss@hotmail.com----r42yxmeT6v----2a55a2a7413dcfaefbf46b8be94a997f245f1307----henduohao.com/2fa/5WE2GL6QXJGWYEC5
Alexandria62860----dldR01hs----ethantho1z2t@hotmail.com----dldR01hs----0d31bface19a288a004573eed79a906d06423dd3----henduohao.com/2fa/KTILCGVXCGDMY6ZP
IsaiDickso6024----rd110hYnb----henry93aromero@hotmail.com----rd110hYnb----7be54a3deb8730a5b2e02d96c376484a27b42909----henduohao.com/2fa/ZL6XJ7P5X5R3WVBL
TrevinMend54497----Imruu7az----danielmaw8@hotmail.com----Imruu7az----673d94cac5d987a71ad70cdde50c79b38f2cd4b5----henduohao.com/2fa/NB4H6Q5LC6DYAXSF
HoffmanDra11841----YJ9i2g80----ethanwoodzoqk@hotmail.com----YJ9i2g80----644a37fd74327ed8bab939db004f9dbd6973bbee----henduohao.com/2fa/G6LDUGDCBM3JD32S
DakotaMcca51864----nsQj4jeuwoK----benjaminga0coj@hotmail.com----nsQj4jeuwoK----59e7eaaf65520713f9544cdafcd6347ce85fc7e4----henduohao.com/2fa/HEGJOCYMLN2NUVS2
YorkAva85513----FwHK3XO5----sdiaz7f@hotmail.com----FwHK3XO5----a9b682897979c8fd809bf6682a9585066e6bb829----henduohao.com/2fa/Z25SKFOR4AXVU7YI
DonaldEwin75623----Nro3we4eaA----henrytucker7j6@hotmail.com----Nro3we4eaA----c252337d6b4f3c94d4ae99859943e4b80fee6735----henduohao.com/2fa/D5ZTMRFSCUIMKYSZ
LandinRamo27039----lI9abrwve0----samuelgtbben@hotmail.com----lI9abrwve0----ab99ff39d7dbe04e9b23e4c4bacbf745c1ae5f50----henduohao.com/2fa/ZDY3HTFAX3K4NUPO
WillisCorn74276----mk6azowP----hudson78jhof@hotmail.com----mk6azowP----f815dcb4c2d90bbec71c14d1dcecdaeef3abdbc1----henduohao.com/2fa/YUJ4OUYHI6FWJZBL
TristanAce12783----q5dxcoFZD2----thmng7gordon@hotmail.com----q5dxcoFZD2----59c36d8fadaab9e318a069fddc9d896cfb22374b----henduohao.com/2fa/UN6WZMDOAVLIG5LZ
AdenWiley2713----g1KnAb3eFb----aberryu3ax@hotmail.com----g1KnAb3eFb----eb24ced744ec6589d3a3c6113039be3ff6849936----henduohao.com/2fa/X7B5L7XEGLFOCFO4
HeathV41312----Y606w4201----lukechendp@hotmail.com----Y606w4201----3140cd8b5e3490037a97404e6e3bcd6207653e91----henduohao.com/2fa/4VIDO3NLNJKPPYHG
KarlyJohns31649----ty9us96Ee----olivergu4kc@hotmail.com----ty9us96Ee----929bc7112068de1a718492249cb795c849cbecce----henduohao.com/2fa/OLTUZDPGP7DQHAZS
KnoxRogeli89237----s00sX4c81j----gmorganfgr@hotmail.com----s00sX4c81j----c5552fe4e3134b9eda2bc13e914556ed47dec52f----henduohao.com/2fa/2IWJABFWV7DBX3KP
benjamin_m8658----Y2a533kt----lukemurphyq6d@hotmail.com----Y2a533kt----7744ef113809d6e01253c55f3a3414714a65e258----henduohao.com/2fa/BSNNL3YFXAO46RVL
AdrianaTho58043----LK8z0am7----alexanderedw45ln@hotmail.com----LK8z0am7----f5e201015199f47935577308daaaf0605121f3c1----henduohao.com/2fa/VLAWHQJT5JN3SKB3
MadisonMcm7306----b8j1czFt----mavericksazo6j@hotmail.com----b8j1czFt----0b8b2d37e3a95951d58fee725f73fe9072cabe1c----henduohao.com/2fa/OVEMCKCJF7344FHS
andrade_mc47754----wWytft6nl----gabriellawgs5@hotmail.com----wWytft6nl----8b16e5a5fef19e1af3a3738531e8c4869f65ea0b----henduohao.com/2fa/A46IAOWGMMOADSWT
ShermanShi7759----qnFmsK3v----samuelxopayne@hotmail.com----qnFmsK3v----871880e59c37e7eef2775de017f06224135705be----henduohao.com/2fa/GPEFO55R4AAURXY5
quinn33719----eH40imxR----michaelfs9@hotmail.com----eH40imxR----cdc440b7b04942265ae7772595010efd3585fa5c----henduohao.com/2fa/DMZEJOF2NP72MQTE
WareDavion55956----BJ93aci6dk----aidensotowul@hotmail.com----BJ93aci6dk----4133593923fbc1806d80a186fdcc4e6cb3bf55b1----henduohao.com/2fa/ARCWFYZCVIKRZX4Z
PranavVarg47565----od5u3oWIey----liamlpf7p@hotmail.com----od5u3oWIey----28667634426f2e2e2bb6d53e7b01ea381843336e----henduohao.com/2fa/3D6DXIRGIT2HEW7M
frye_luke70930----Gvfhe4a78----matthewisal@hotmail.com----Gvfhe4a78----e7c7c0d82c364631c67c98e4546eaa7b5a85876d----henduohao.com/2fa/F6PHB7SEV5CBEEYH
FrostRicar34399----d840QnpW1----josephfsacarter@hotmail.com----d840QnpW1----151158c93432d0db8e71343342efa53f4004bcde----henduohao.com/2fa/ISMTBT433VR4IRI2
HornJessic59384----fvxW4v5b----benharris8au@hotmail.com----fvxW4v5b----ef19c1b1b0c741c4b87ca3dd6346b6fd3322304c----henduohao.com/2fa/U2G5QPMBKWYEASRW
RodgersSul50031----iCzB6B1w0----samuelg53vburke@hotmail.com----iCzB6B1w0----17026f39a6a0e2392e946afc85a275dc1b567052----henduohao.com/2fa/7GGCUTYTLBLBWYGZ
AMathis44769----anu8D1fN----noahgrayy1xs@hotmail.com----anu8D1fN----b9482081c58bede99cde6ffa9abe3f9cbfb44052----henduohao.com/2fa/CCPCOJYK5Y22B6NE
rush_aaliy8818----lr2kbW1Q1m----wixjcooper@hotmail.com----lr2kbW1Q1m----846b1d8a7c639de0277b519de1c4d3e6babe66a1----henduohao.com/2fa/R55UDABKJIS4JXJN"""
lines = text.strip().split('\n')
data = []
for line in lines:
    parts = line.split('----')
    if len(parts) == 6:
        data.append(parts)
df = pd.DataFrame(data, columns=["username", "password", "email_","email_password", "AuthToken", "two_fa_link"])
df.drop(columns = ['AuthToken'], inplace= True)
df[['availability', 'is_rate_limited_now']] = 1, 0
df
# %%
sql_cmd = '''ALTER TABLE twitter_account_database ADD two_fa_link VARCHAR(255);'''
sql_connector = "mysql+mysqlconnector://tangshuo:tangshuo@121.36.100.76:13310/ai_summer"
from sqlalchemy import create_engine
engine = create_engine(sql_connector)
with engine.connect() as conn:
    conn.execute(sql_cmd)
# %%
df.to_sql(name="twitter_account_database", con=engine, index=False, if_exists='append')
# %%
import pandas as pd 
from sqlalchemy import create_engine
sql_cmd = """SELECT * FROM twitter_account_database WHERE two_fa_link IS NOT NULL"""
sql_connector = "mysql+mysqlconnector://tangshuo:tangshuo@121.36.100.76:13310/ai_summer"
from sqlalchemy import create_engine
engine = create_engine(sql_connector)
data = pd.read_sql(sql_cmd, engine)
engine.dispose()
data
# %%

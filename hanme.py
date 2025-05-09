import pygame
import random
import sys
import time

# --- 기본 설정 ---
pygame.init()
pygame.font.init()
pygame.key.start_text_input() # 명시적으로 텍스트 입력 처리 시작

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("타자 연습 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 폰트 설정
# 시스템에 설치된 한글 폰트 이름을 확인하고 사용하세요.
# 예: 'malgungothic', 'nanumgothic', 'applegothic' 등
korean_font_name = 'nanumgothic' # <--- 사용 환경에 맞게 수정하세요!
try:
    word_font = pygame.font.SysFont(korean_font_name, 35)
    score_font = pygame.font.SysFont(korean_font_name, 30)
    input_font = pygame.font.SysFont(korean_font_name, 40)
    game_over_font = pygame.font.SysFont(korean_font_name, 60)
    print(f"폰트 '{korean_font_name}' 로딩 성공.")
except pygame.error:
    print(f"경고: '{korean_font_name}' 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다. 한글이 깨질 수 있습니다.")
    word_font = pygame.font.SysFont(None, 35) # 대체 기본 폰트
    score_font = pygame.font.SysFont(None, 30) # 대체 기본 폰트
    input_font = pygame.font.SysFont(None, 40) # 대체 기본 폰트
    game_over_font = pygame.font.SysFont(None, 60) # 대체 기본 폰트

# --- 게임 요소 ---
# 단어 목록 (원하는 단어로 변경하거나 파일에서 불러올 수 있습니다)
# word_list = ["python", "pygame", "game", "coding", "programming", "keyboard", "practice", "typing", "speed", "accuracy"]
# 한글 단어 목록 예시 (UTF-8 인코딩 확인)
# 이전에 생성한 hanme_formatted.txt 내용을 여기에 붙여넣거나, 파일에서 읽어오도록 수정할 수 있습니다.
word_list = ["파이썬", "게임", "코딩", "연습", "키보드", "프로그래밍", "정확도", "속도", "단어", "문장", "개발", "재미", "도전", "이승담", "최강민", "이해원", "최규빈", "이지은", "이예진", "학교", "부산", "대전", "재미없다", "오락", "깃발", "오리", "고양이", "가나다라", "가냘프다", "가노라", "가누다", "가늘다", "가다듬다", "가닥", "가두다", "가득하다", "가뜬하다", "가라사대", "가라앉다", "가락", "가락지", "가랑눈", "가랑비", "가랑잎", "가래", "가련하다", "가로", "가로막다", "가로채다", "가루", "가르다", "가르치다", "가리다", "가마", "가만히", "가물", "가슴", "가시", "가시다", "가시덤불", "가엾은", "가위", "가을걷이", "가을보리", "가자가자", "가장", "가장자리", "가죽", "가지", "가지다", "가지치다", "가파르다", "가풀막", "간", "갈기다", "갈다", "갈대", "갈라지다", "갈림길", "갈매기", "갈무리", "갈묻이", "갈수록", "갈증", "갈퀴", "갈팡질팡", "갉아먹다", "감감하다", "감돌다", "감싸다", "감자", "감쪽같다", "감추다", "감투", "갑갑하다", "갑자기", "갑절", "값어치", "값지다", "갓", "갓나다", "갓난애", "강", "강가", "강강술래", "강아지", "갖다놓다", "갖추갖추", "같다", "같은또래", "갚다", "개", "개구리", "개구쟁이", "개나리", "개다", "개머리", "개울", "개키다", "개펄", "갯마을", "갯벌", "갸륵하다", "갸름하다", "거기", "거꾸로", "거누다", "거느리다", "거늑하다", "거닐다", "거두다", "거듭", "거룩하다", "거룻배", "거르다", "거름더미", "거리", "거리끼다", "거머리", "거멓다", "거문고", "거미", "거북하다", "거세다", "거스르다", "거울", "거위", "거의", "거저", "거적", "거죽", "거짓말", "거치다", "거칠다", "거침없다", "거푸집", "걱정", "건너다", "건널목", "건더기", "건드리다", "건듯", "건몸달다", "건방지다", "건사하다", "건성", "건지다", "걷다", "걷어차다", "걷잡다", "걸다", "걸레", "걸리다", "걸맞다", "걸음마", "걸치다", "걸터앉다", "검다", "검둥이", "검불", "겉대중", "겉돌다", "겉장", "겉치레", "게우다", "게으르다", "겨냥", "겨누다", "겨드랑이", "겨루다", "겨우내", "겨우살이", "겨울", "겪다", "견디다", "겯다", "겸사겸사", "겹겹이", "겹치다", "곁길", "곁방살이", "계면쩍다", "계집", "고갯짓", "고구마", "고깃배", "고니", "고달프다", "고대로", "고대하다", "고동", "고되다", "고드름", "고랑", "고래", "고루고루", "고르다", "고리", "고무래", "고무줄", "고삐", "고사리", "고소하다", "고양이", "고요하다", "고을", "고이", "고인돌", "고작", "고장", "고치다", "고프다", "곤하다", "곧다", "골고루", "골치", "골탕먹다", "곪다", "곰", "곰방대", "곰보", "곰팡이", "곱다", "곱사등이", "곱셈", "공기놀이", "과일나무", "관괌", "광주리", "괜히", "괴다", "괴로움", "구겨지다", "구기다", "구두쇠", "구르다", "구름", "구멍", "구부리다", "구석구석", "구석지다", "구수하다", "구슬", "구슬프다", "구실", "구유", "군것질", "군데군데", "굳", "굳다", "굳세다", "굳이", "굴비", "굵다", "굶다", "굼벵이", "굽다", "굽이굽이", "궁금하다", "궂다", "귀", "귀고리", "귀뚜라미", "귀띔", "귀머거리", "귀밑머리", "귀양살다", "귀엣말", "귀엽다", "귀찮다", "귤", "귤나무", "그까짓", "그나마", "그냥", "그네", "그늘", "그다지", "그대로", "그득하다", "그래서", "그러나", "그러니까", "그러면", "그럭저럭", "그루", "그르다", "그릇", "그리다", "그리움", "그림자", "그림판", "그립다", "그만두다", "그만하다", "그물", "그믐날", "그사이", "그윽하다", "그을다", "그저", "그지없다", "그치다", "글", "글귀", "글쇠", "글썽하다", "글씨", "글피", "긁다", "금잔디", "기나길다", "기다", "기다리다", "기대다", "기둥", "기러기", "기르다", "기름지다", "기반", "기슭", "기아", "기와", "기울다", "기자", "기장", "기침", "긷다", "길", "길다", "길들다", "길이", "길잡이", "길쭉하다", "김장", "김치", "김칫국", "깁다", "깃들이다", "깊다", "깊이", "까다", "까다롭다", "까닥이다", "까닭", "까딱없다", "까라지다", "까마귀", "까맣다", "까매지다", "까물까물", "까부르다", "까불다", "까치", "까치눈", "깍두기", "깍듯하다", "깔깔", "깔때기", "깔보다", "깜깜한", "깜박", "깜찍하다", "깡충깡충", "깡통", "깨", "깨끗하다", "깨끼적삼", "깨다", "깨닫다", "깨달음", "깨뜨리다", "깨물다", "깨우치다", "꺼리다", "꺼림하다", "꺾다", "껄껄껍데기", "껍질", "껴들다", "껴안다", "꼬다", "꼬리", "꼬이다", "꼬투리", "꼭지", "꽁꽁", "꽁무니", "꽁지", "꽃", "꽃구름", "꽃밭", "꽃샘", "꽝", "꽹과리", "꾀꼬리", "꾀다", "꾐", "꾸러미", "꾸준하다", "꾸지람", "꿀벌", "꿈결", "꿩", "끊다", "끌어안다", "끔", "끔찍한", "끝끝내", "끼우다", "끼치다", "나그네", "나날이", "나날이", "나누다", "나다니다", "나뒹굴다", "나드리", "나들이", "나라", "나라글자", "나란하다", "나무라다", "나뭇잎", "나부끼다", "나비", "나비리본", "나쁘다", "나아가다", "나오다", "나이", "나이테", "나중", "나타나다", "나풀나풀", "나홀로", "나흗날", "낙낙하다", "낚", "낚다", "낚시질", "낟가리", "낟알", "날개", "날개옷", "날다", "날뛰다", "날래다", "날림", "날씨", "날짐승", "날품", "낡은", "남다", "남달리", "납작하다", "낫다", "낭", "낭떠러지", "낮잠", "낮추다", "낮춤말", "낯설다", "낱낱이", "낱말", "낱자", "낳다", "내기", "내다보다", "내닫다", "내두르다", "내려가다", "내리다", "내리닫다", "내리치다", "내밀다", "내뿜다", "내젓다", "내쫓다", "내키다", "냄새", "냇가", "냉잇국", "냉큼", "너구리", "너그럽다", "너르다", "너머", "너울너울", "너울너울", "너털웃음", "넋두리", "넌지시", "널뛰기", "널찍하다", "넘어가다", "넘치다", "넝마주이", "네거리", "네모", "녀석", "노고지리", "노다지", "노랑", "노랑", "노래", "노랫가락", "노략질", "노려보다", "노루", "노름", "노릇", "노리다", "노새", "노여움", "노을", "녹두", "녹말", "녹지다", "놀다", "놀리다", "놀이", "놀이터", "높다랗다", "높이", "놓다", "뇌까리다", "누구", "누나", "누룩", "누르다", "누리", "누비다", "누에섶", "누이", "눈", "눈가림", "눈곱", "눈길", "눈맵시", "눈물", "눈물짓다", "눈보라", "눈부시다", "눈사람", "눈송이", "눈치", "눕다", "뉘엿뉘엿", "뉘우치다", "느끼다", "느리다", "느릿느릿", "느티나무", "늑대", "늘리다", "늙다", "능금", "늦추다", "늪", "다가서다", "다다르다", "다달이", "다람쥐", "다림질", "다물다", "다부지다", "다스리다", "다시", "다음", "다지다", "다짐", "다치다", "다투다", "닥나무", "닦다", "단골", "단단하다", "단짝", "단추", "닫다", "달가닥", "달걀", "달구지", "달다", "달라다", "달라진", "달리다", "달맞이", "달아나다", "달콤하다", "달팽이", "달포", "닭", "닮은꼴", "담그다", "담빡", "닷새", "당기다", "당차다", "닿소리", "대견하다", "대꾸", "대나무", "대낮", "대님", "대다", "대들다", "대뜸", "대롱", "대목", "대바구니", "대부분의", "대중말", "대패", "더구나", "더덕더덕", "더듬더듬", "더럭", "더럽다", "더미", "더부살이", "더불어", "더없이", "더욱이", "던져두다", "덜되다", "덜컥", "덜컹덜컹", "덤비다", "덧셈", "덧신", "덩굴", "덩달아", "덮개", "덮치다", "도가니", "도깨비", "도끼", "도둑", "도라지", "도랑", "도련님", "도리깨", "도마뱀", "도막말", "도미", "도시락", "도움", "도토리", "도톰하다", "도포", "독수리", "독특하다", "돋구다", "돋보기", "돋아나다", "돌다", "돌다리", "돌리다", "돌림", "돌맞이", "돌보다", "돌부처", "돌이키다", "돕다", "돗자리", "동그라미", "동나다", "동냥아치", "동무", "동산", "동아줄", "동치미", "돛단배", "돼지", "되뇌다", "되도록", "되묻다", "되살다", "되새기다", "되새김", "된소리", "됨됨이", "두고두고", "두꺼비", "두껍다", "두다", "두더지", "두둑", "두둥실", "두들기다", "두레박", "두려움", "두루", "두루마기", "두루미", "두리둥실", "두메", "두엄", "두텁다", "둘러보다", "둘레", "둥글다", "둥실", "둥우리", "뒤", "뒤뚱뒤뚱", "뒤뜰", "뒤범벅", "뒤섞이다", "뒤엎다", "뒤적뒤적", "뒤통수", "뒷골목", "뒷바라지", "뒷받침", "뒷짐", "뒹굴다", "드디어", "드러눕다", "드리다", "드리우다", "드리우다", "드물다", "드세다", "듣기놀이", "듣다", "들것", "들끓다", "들다", "들뜨다", "들르다", "들볶다", "들이받다", "들쥐", "들추다", "들키다", "들판", "듬뿍하다", "등쌀", "등지다", "디디다", "디딜방아", "따갑다", "따귀", "따뜻하다", "따로", "따르다", "따분하다", "따스하다", "따위", "따지다", "딱따구리", "딱딱하다", "딸리다", "땅거미", "땅덩이", "땅바닥", "땅콩", "때", "때때로", "때문", "떠나다", "떠다니다", "떠들다", "떠받치다", "떠벌리다", "떠보다", "떡", "떡갈나무", "떡보", "떡잎", "떨기", "떨치다", "떳떳하다", "떼다", "뗏목", "또래", "또렷하다", "똑똑하다", "뚜렷하다", "뚫다", "뛰놀다", "뛰어나다", "뛰어난", "뜨끈뜨끈", "뜨다", "뜨뜻하다", "뜬구름", "뜬눈", "뜯기다", "뜯다", "뜯어먹다", "뜻글자", "뜻밖에", "띄엄띄엄", "띠다", "랑", "마감", "마구", "마구간", "마나님", "마나님", "마냥", "마당쇠", "마디", "마디다", "마땅하다", "마룻바닥", "마르다", "마름질", "마무리", "마을", "마을일", "마음", "마음껏", "마음놓다", "마음대로", "마음씨", "마주", "마중", "마지막", "마찬가지", "마치", "마치다", "마침", "막내", "막다", "막대기", "막바지", "막히다", "만남", "만들다", "만들다", "만만하다", "만만함", "만지다", "많다", "맏아들", "말", "말고삐", "말괄량이", "말굽", "말놀이", "말다", "말다툼", "말똥구리", "말리다", "말머리", "말미암다", "말버릇", "말벗", "말본", "말솜씨", "말썽", "말썽꾸러기", "말쑥하다", "말익히기", "말주변", "말판", "말하다", "맑다", "맛들다", "맛보다", "망나니", "망설이다", "망아지", "망치", "망치다", "맞다", "맞들다", "맞먹다", "맞붙다", "맞장구", "맞추다", "맞춰서", "맡기다", "맡다", "매기다", "매다", "매달다", "매듭", "매만지다", "매부리코", "매섭다", "매스껍다", "매우", "매운바람", "매이다", "매정하다", "매질", "매한가지", "맨드라미", "맨머리", "맨주먹", "맴돌다", "맵다", "맵시", "맷돌", "맹꽁이", "맺히다", "머금다", "머나먼", "머루", "머리", "머리맡", "머무르다", "머슴", "먹구름", "먹다", "먼발치", "먼지", "멀다", "멀미", "멀미", "멀쩡하다", "멈추다", "멋대로", "멋쟁이", "멍청이", "멍하다", "메기", "메다", "메뚜기", "메마르다", "메스껍다", "메아리", "메우다", "메주", "멧돼지", "며느리", "며칠", "멱감다", "멱살", "멸구", "모금", "모기", "모내기", "모닥불", "모래", "모래찜", "모롱이", "모르다", "모름지기", "모서리", "모시다", "모으다", "모임", "모조리", "모진바람", "모질다", "모쪼록", "모처럼", "모퉁이", "목덜미", "목도리", "목마르다", "목소리", "몰골", "몰다", "몰래", "몰려가다", "몰리다", "몸", "몸뚱이", "몸살", "몸서리", "몸소", "못난이", "못내", "못자리", "몽글몽글", "몽둥이", "몽땅", "무겁다", "무게", "무너지다", "무더기", "무더위", "무던하다", "무덤", "무디다", "무럭무럭", "무르녹다", "무르다", "무릇", "무리", "무서움", "무엇", "무지개", "무찌르다", "무척", "묶다", "문지르다", "묻다", "물", "물감", "물결", "물고기", "물길", "물동이", "물들이다", "물러가다", "물레", "물레방아", "물리치다", "물밀듯이", "물방아", "물벼락", "물오르다", "물음", "물장난", "묽다", "뭉개다", "뭉게뭉게", "미꾸라지", "미끈하다", "미끼", "미나리", "미나리", "미닫이", "미덥다", "미루다", "미리", "미리", "미어지다", "미역", "미움", "미치다", "민들레", "민며느리", "민물", "믿다", "밀기울", "밀다", "밀리다", "밋밋하다", "밑거름", "밑둥치", "밑천", "바가지", "바가지", "바구니", "바글바글", "바꾸다", "바느질", "바닥", "바둑", "바둑이", "바라다", "바라다", "바라보다", "바라지", "바람", "바람개비", "바람잡이", "바랍니다", "바래다", "바로잡다", "바르다", "바르르", "바쁘다", "바삐", "바싹", "바야흐로", "바작바작", "바지", "바지랑대", "바치다", "바탕", "바탕글", "바특하다", "박꽃", "박달나무", "박쥐", "박히다", "밖", "반갑다", "반기", "반드시", "반반하다", "반장", "반지", "반짝이다", "받들다", "받아들이다", "받치다", "받침", "받히다", "발", "발가숭이", "발개지다", "발끈", "발돋움", "발딱", "발름발름", "발목", "발바리", "발벗다", "발뺌", "발소리", "발자국", "발칵", "발칵", "밝다", "밤새", "밤톨", "밧줄", "방그레", "방물장수", "방아쇠", "방울", "방정맞다", "밭고르기", "밭둑", "밭일", "배겨나다", "배기다", "배뱅이굿", "배우다", "배웅", "배짱", "배춧국", "뱃노래", "버드나무", "버럭", "버릇", "버리다", "버선", "버티다", "벅차다", "번개", "번데기", "번득이다", "벋다", "벌거숭이", "벌다", "벌레", "벌벌", "벌어지다", "벌판", "범", "벗나가다", "벙글벙글", "벚꽃", "베개", "베다", "벼락", "벼락쪽", "벼랑길", "벼슬", "벽", "변변히", "볏가리", "보금자리", "보람", "보랏빛", "보랏빛", "보름달", "보릿고개", "보배", "보살피다", "보아주다", "보자기", "보조개", "보태다", "본체만체", "볼기", "볼모", "봉오리", "부글부글", "부끄럽다", "부닥치다", "부대끼다", "부드럽다", "부듯하다", "부딪치다", "부러지다", "부려먹다", "부르다", "부리", "부서지다", "부스러기", "부스럼", "부치다", "부피", "북돋우다", "북새통", "불길", "불끈", "불리다", "불붙다", "불어넣다", "붉히다", "붐비다", "붓다", "붙이다", "비구름", "비기다", "비늘", "비둘기", "비듬", "비뚜로", "비로소", "비롯하다", "비비여", "비빔", "비슷비슷", "비우다", "비치다", "비키다", "비틀다", "빈말", "빌다", "빗금", "빗맞다", "빙긋하다", "빚다", "빠르다", "빡빡", "빤빤하다", "빨다", "빨래", "빨리", "빵", "빻다", "빼내다", "빼앗다", "빼쭉하다", "빽빽", "뺑뺑", "뻐근하다", "뻐기다", "뻔하다", "뼈아프다", "뽀글뽀글", "뽀얗다", "뽐내다", "뽕", "뽕나무", "뾰족하다", "뿌리", "뿌리치다", "뿔뿔이", "삐다", "삐죽이", "삐죽하다", "사나이", "사납다", "사냥", "사다리", "사르다", "사슴", "사용하다", "사이좋다", "삭이다", "삯바느질", "산들바람", "산뜻하다", "산", "말", "살갗", "살결", "살그머니", "살랑살랑", "살림", "살살", "살얼음", "살짝", "살찌다", "살펴보다", "삶다", "삼가다", "삼다", "삼키다", "삽살개", "삿갓", "삿대", "상냥하다", "상투", "새겨듣다", "새김질", "새끼치다", "새나라", "새바람", "새색시", "새우다", "새침데기", "새카맣다", "새해", "샘터", "샛별", "생각", "생소한", "생쥐", "서두르다", "서럽다", "서리다", "서리맞다", "서슴다", "서울", "서투르다", "선선하다", "선하다", "설날", "설레다", "설레설레", "설빔", "설설기다", "섬기다", "성가시다", "성나다", "세간", "세다", "세로", "세우다", "셈틀", "소경", "소금", "소나기", "소나무", "소르르", "소름", "소리", "소리치다", "소매치기", "소쿠리", "속다", "속삭이다", "손가락", "손꼽다", "손놓다", "손버릇", "손아래", "솔바람", "솔숲", "솔질", "솜씨", "솜털", "솟다", "송사리", "송아지", "송이송이", "쇠고기", "쇠사슬", "수고", "수다", "수레", "수선떨다", "수세미", "수수", "수수께끼", "수수하다", "수술", "수월찮다", "수저", "수줍다", "수풀", "숙덕이다", "술", "술래잡기", "숨결", "숨기다", "숨바꼭질", "숯", "숱하다", "숲쉬다", "쉽사리", "스님", "스르르", "스스로", "스승", "스치다", "슬그머니", "슬금슬금", "슬기", "슬며시", "슬픔", "시골뜨기", "시궁창", "시끄럽다", "시냇가", "시늉", "시다", "시달리다", "시들다", "시름", "시리다", "시새우다", "시시하다", "시집가다", "식다", "신나다", "신다", "신세", "싣다", "실", "실리다", "실마리", "실없다", "실핏줄", "싫다", "싫증", "심부름", "싯누렇다", "싱겁다", "싱글벙글", "싱글싱글", "싱긋", "싱숭생숭", "싶어하다", "싸다", "싸리", "싸안다", "싹싹하다", "쌀가게", "쌀쌀하다", "쌍", "쌓다", "쌔근쌔근", "써레", "썩둑썩둑", "썰매타기", "쏘다니다", "쏠리다", "쑥", "쑥스럽다", "쓰다듬다", "쓰레받기", "쓰리다", "쓱싹하다", "쓸개", "쓸쓸하다", "씨름", "씩씩하다", "씻다", "씽긋", "아가씨", "아궁이", "아기", "아기자기", "아까", "아깝다", "아끼다", "아낙네", "아내", "아늑하다", "아니", "아니꼽다", "아드님", "아들", "아래뜸", "아랫사람", "아롱", "아롱", "아뢰다", "아름", "아름답다", "아리다", "아리따운", "아리랑", "아무쪼록", "아버님", "아쉽다", "아슬아슬", "아우", "아우성", "아울러", "아이", "아이가", "아이고", "아저씨", "아주머니", "아지랑이", "아직까지", "아찔하다", "아침", "아큰", "아프다", "악물다", "악쓰다", "안간힘", "안기다", "안마", "안마당", "안채", "안타깝다", "안팎", "앉은뱅이", "알뜰하다", "알리다", "알맞다", "알아채다", "알차다", "앓다", "암컷수컷", "앙", "앙갚음", "앙상하다", "앙큼하다", "앙탈", "앞뜰", "앞잡이", "앞지르다", "앞치마", "애달다", "애매하다", "애쓰다", "애틋하다", "야물다", "약", "얄밉다", "얇다", "얌전하다", "얕잡다", "어기다", "어깨", "어깨동무", "어느덧", "어둑어둑", "어둡다", "어렵다", "어른", "어름", "어리광", "어리다", "어리석다", "어린이", "어린이", "어림셈", "어림없다", "어머나", "어버이", "어색하다", "어설프다", "어여쁘다", "어우르다", "어울리다", "어이구", "어제", "어지럽다", "어쩌다가", "어처구니", "억누르다", "억지", "억지로", "언덕빼기", "언제든지", "언짢다", "언청이", "얹히다", "얻어맞다", "얼굴", "얼레", "얼룩소", "얼른", "얼마나", "얼마나", "얼빠지다", "얼음", "얽매이다", "얽히다", "엄두", "엄마", "엄살", "엄지가락", "업신여김", "없다", "엇갈리다", "엉겁결", "엉금엉금", "엉뚱하다", "엉망", "엉망", "엉성하다", "엉터리", "엊그제", "엎드리다", "에누리", "에워가다", "여기저기", "여느", "여닫다", "여러가지", "여러분", "여름내", "여리다", "여무지다", "여물", "여물다", "여미다", "여우", "여운다", "여울", "여위다", "여쭈다", "여태껏", "역성", "엮다", "연방", "연장", "열다", "열없다", "열흘", "엷다", "염소", "엿보다", "영문", "예쁘다", "옛날", "오가다", "오누이", "오늘따라", "오들오들", "오뚝", "오락가락", "오랑캐", "오래오래", "오로지", "오르막", "오리다", "오막살이", "오목하다", "오므리다", "오붓하다", "오순도순", "오슬오슬", "오죽", "오줌싸개", "오지그릇", "오히려", "옥수수", "온갖", "온통", "올가미", "올동말동", "올망졸망", "올빼미", "올챙이", "옮기다", "옳은일", "옴츠리다", "옷깃", "옷차림", "옹긋쫑긋", "옹기옹기", "옹기종기", "옹달샘", "옹이", "와글와글", "와들와들", "왈칵", "외롭다", "요즈음", "우거지다", "우기다", "우두머리", "우두커니", "우렁차다", "우리말", "우짖다", "울긋불긋", "울리다", "울먹이다", "울부짖다", "울타리", "움직이다", "움츠리다", "움켜잡다", "움트다", "웃기다", "웃음거리", "웅그리다", "웅덩이", "웅크리다", "원숭이", "웬만큼", "윗사람", "유난히", "으뜸꼴", "으레", "으르다", "으슥하다", "으쓱", "읊다", "응달", "이것저것", "이글이글", "이기다", "이끌다", "이끼", "이나마", "이나마", "이날", "이날", "이다음", "이따위", "이랑", "이럭저럭", "이렇듯", "이룩하다", "이맛살", "이바지", "이불", "이슥하다", "이슬", "이아이", "이야기", "이어지다", "이영차", "이웃", "이윽고", "이튿날", "익다", "익살", "익숙하다", "인간", "일깨우다", "일러두기", "일부러", "일어서다", "일으키다", "일자리", "일찍이", "일컫다", "읽다", "읽다", "잃다", "임금", "임자", "입", "입맛쓰다", "잇닿다", "잇따르다", "잊다", "자갈", "자개", "자국", "자그마치", "자기", "자나깨나", "자라다", "자락", "자루", "자르다", "자리", "자리잡다", "자장가", "자주", "자취", "자치기", "자판", "작다", "작은말", "잔", "잔", "잔등이", "잔디", "잔뜩", "잔소리", "잔잔하다", "잔털", "잘라먹다", "잘래잘래", "잘리다", "잘못", "잠결", "잠그다", "잠깐", "잠꾸러기", "잠들다", "잠자다", "잠자리", "잡치다", "잣나무", "장가", "장구벌레", "장기", "장난감", "장님", "장사치", "장아찌", "장자", "잦다", "재갈", "재미", "재빠르다", "재우치다", "재채기", "잿더미", "잿물", "잿빛", "쟁그랑", "저같이", "저것", "저고리", "저기", "저나마", "저녁노을", "저녁때", "저녁밥", "저다지", "저러하다", "저런", "저렇다", "저리", "저리다", "저마다", "저만큼", "저물다", "저승", "저울", "저울질", "저울추", "저절로", "저지르다", "저희", "적다", "적이", "적히다", "전나무", "절간", "절구", "절구통", "절다", "절로", "절벅절벅", "절이다", "젊다", "젊은이", "점잔", "점잖다", "접다", "접히다", "젓다", "정어리", "젖니", "젖다", "젖소", "젖히다", "제기차기", "제대로", "제멋대로", "제발", "제법", "제비", "제비꽃", "제일", "제자리", "제재하다", "제쳐놓다", "제치다", "조개무지", "조것만큼", "조그맣다", "조금", "조르다", "조리", "조리다", "조마조마", "조바심", "조아리다", "조약돌", "조지다", "조카", "족", "족제비", "족족", "졸다", "졸라대다", "졸라매다", "졸리다", "졸음", "졸이다", "졸졸", "좀더", "좀먹다", "좀처럼", "좁다", "좁다랗다", "좁히다", "종", "종긋하다", "종다리", "종달새", "종아리", "종이", "종이쪽", "종이피리", "종종걸음", "좇다", "좋다", "좔좔", "좽이", "죄다", "죄악", "주고받다", "주낙", "주다", "주둥아리", "주렁주렁", "주룩", "주르르", "주름", "주름살", "주리다", "주머니", "주먹", "주먹구구", "주무르다", "주무시다", "주변", "주사위", "주춤", "죽", "죽음", "죽이다", "준말", "줄", "줄거리", "줄기", "줄기차다", "줄다리기", "줄달음질", "줄어지다", "줄이다", "줄자", "줄줄", "줍다", "쥐구멍", "쥐다", "쥐며느리", "쥐어뜯다", "쥐어박다", "즈음", "즐겁다", "즐기다", "지게", "지게꾼", "지그시", "지글지글", "지껄이다", "지나가다", "지나다", "지나치다", "지내다", "지느러미", "지니다", "지다", "지레", "지루하다", "지르다", "지름", "지름글쇠", "지름길", "지반", "지붕", "지새우다", "지어내다", "지우개", "지우다", "지저귀다", "지절대다", "지진", "지치다", "지켜보다", "지키다", "지팡이", "지푸라기", "지피다", "진달래", "진자", "진작", "진저리", "진창", "진흙", "진흙집", "질겁하다", "질그릇", "질기다", "질리다", "질질", "질척하다", "짊어지다", "짐꾼", "짐수레", "짐승", "짐작", "집게", "집다", "집안", "집오리", "짓궂다", "짓누르다", "짓다", "짓밟다", "짓밟히다", "짖다", "짙다", "짚다", "짜개다", "짜다", "짜릿짜릿", "짜임새", "짜증", "짝", "짝눈", "짝맞다", "짝맞추다", "짝짜꿍", "짠물", "짠지", "짤랑짤랑", "짤막하다", "짧다", "짭짤하다", "째다", "째리다", "째지다", "짹짹", "쨍쨍", "쩌렁쩌렁", "쩔쩔매다", "쩡쩡", "쪼개다", "쪼그리다", "쪼다", "쪼들리다", "쪼아먹다", "쪽마루", "쪽박", "쪽배", "쪽빛", "쫄딱", "쫑긋", "쫓다", "쬐다", "쭈그리다", "쭈글쭈글", "쭈뼛하다", "쭉정이", "찌개", "찌그리다", "찌꺼기", "찌다", "찌르레기", "찌푸리다", "찍다", "찐빵", "찡그리다", "찡긋", "찡하다", "찢다", "찧다", "차갑다", "차곡차곡", "차라리", "차림", "차분하다", "차츰차츰", "착하다", "찬장", "찰흙", "참고하다", "참나무", "참다", "참되다", "참뜻", "참말", "참새", "창살", "찾다", "채우다", "책", "척척", "천천히", "철나다", "철모르다", "철새", "철없다", "첫마디", "첫솜씨", "첫인상", "첫째", "청개구리", "체처놓다", "쳐다보다", "초겨울", "초라하다", "초롱초롱", "촉촉하다", "촌사람", "촘촘하다", "총", "총총하다", "추가된", "추녀", "추다", "추위", "축이다", "축축하다", "춤추다", "춥", "춥다", "취나물", "치근대다", "치다", "치닫다", "치르다", "치마", "치맛자락", "치밀다", "치받다", "치솟다", "치우다", "치우치다", "치이다", "치키다", "칙칙폭폭", "친구", "칡", "침", "칭얼칭얼", "칭칭", "카네이션", "카드", "칸막이", "칼국수", "칼날", "캄캄하다", "캐다", "캥거루", "커녕", "커다랗다", "컴컴하다", "컴퓨터", "케케묵다", "켕기다", "켜다", "켤레", "켬", "코", "코끼리", "코뚜레", "코멘소리", "코스모스", "코앞", "콧물", "콩쥐", "쾅쾅", "크다", "크레용", "큰기침", "큰소리", "큰아버지", "큰일", "큰집", "큼직하다", "키다리", "키우다", "킬킬", "타고나다", "타다", "타래", "타오르다", "타이르다", "탐탁하다", "태우다", "택", "터뜨리다", "터벅터벅", "터지다", "턱없다", "털다", "털썩", "텁석부리", "텃밭", "텃새", "테두리", "토끼", "토라지다", "톱니바퀴", "톱밥", "톱질", "통", "통나무", "통틀어", "툭툭", "툭하면", "퉁기다", "퉤퉤", "튀다", "트다", "트집", "틀", "틀리다", "틀모리", "틀어막다", "틀어박다", "틈바구니", "틈틈이", "틔우다", "파고들다", "파내다", "파다", "파드득", "파랗다", "파르스름", "파릇파릇", "파묻다", "팔", "팔다", "팔리다", "팔베개", "팔짱", "팔팔", "팥", "패다", "패랭이", "팽개치다", "팽이치기", "팽팽하다", "퍼내다", "퍼뜨리다", "퍼붓다", "퍼지다", "펄럭이다", "펄쩍", "펴다", "편", "펼치다", "포기", "폭주다", "표", "푸근하다", "푸드득", "푸르다", "푹신하다", "풀", "풀그림", "풀다", "풀리다", "풀무", "풀밭", "풀숲", "품다", "품삯", "풍뎅이", "퓨", "피나무", "피눈물", "피리", "피어나다", "피우다", "핀잔", "핏대", "핏덩어리", "핏줄기", "핑계", "핑핑", "하기야", "하나", "하나지", "하느님", "하늘나라", "하늘하늘", "하루갈이", "하루바삐", "하루속히", "하룻밤", "하마", "하마터면", "하물며", "하얗다", "하여금", "하염없다", "하였다", "하자스라", "하지만", "하찮다", "하품", "학", "한가운데", "한가위", "한가을", "한가하다", "한걱정", "한겨울", "한결", "한국인", "한글날", "한길", "한꺼번에", "한낱", "한눈팔다", "한더위", "한들한들", "한때", "한마리", "한몫", "한바퀴", "한술", "한숨", "한옆", "한올한올", "한잠", "한차례", "한참", "한철", "한해살이", "할머니", "할미꽃", "할아버지", "할퀴다", "핥다", "핥아먹다", "함", "함박꽃", "함박눈", "함부로", "함빡", "함석", "함지", "함지박", "해내다", "해님", "해돋이", "해먹다", "해바라기해어지다", "해오라기", "해죽", "햅쌀", "햇볕", "햇살", "행주", "향상시키다", "허깨비", "허덕이다", "허둥지둥", "허드레", "허름하다", "허리허물", "허물다", "허방다리", "허술하다", "허울", "허전하다", "허투루", "허파꽈리", "허허벌판", "헐다", "헐떡이다", "헐렁", "헐렁하다", "헐레벌떡", "헐벗다", "헛소리", "헤아리다", "헤어나다", "헤어지다", "헤치다", "헤프다", "헹가래", "헹구다", "호랑이", "호리호리", "호미", "호통", "혼잣말", "홀랑", "홀몸", "홀소리", "홀씨", "홑이불", "환하다", "환호", "활짝", "황", "황소", "횃불", "후두두", "후려내다", "후루룩", "후룩후룩", "후비다", "훌륭하다", "훑다", "훔쳐먹다", "훔치다", "훤하다", "훨씬", "휘감기다", "휘날리다", "휘덮다", "휘두르다", "휘말다", "휘어지다", "휘파람", "휩싸다", "흉내내다", "흉보다", "흐느끼다", "흐려지다", "흐르다", "흐리다", "흐림", "흐릿하다", "흐뭇하다", "흔하다", "흘겨보다", "흘기다", "흘깃흘깃", "흘리다", "흙", "흙투성이", "흠씬", "흩날리다", "흩어지다", "흰", "흰자", "히죽", "힘", "힘겹다", "힘껏", "힘들다", "힘살", "힘세다", "힘입다", "힘주다", "힘차게"]

# 떨어지는 단어 관리 리스트
falling_words = [] # [{'text': '단어', 'rect': pygame.Rect, 'speed': 2, 'surface': Surface}, ...]

# 사용자 입력
current_input = ""

# 게임 상태 변수
score = 0
lives = 5
base_word_speed = 1.5 # 초기 단어 속도
word_spawn_delay = 1.5 # 초기 단어 생성 간격 (초)
last_spawn_time = time.time()
level_up_time = time.time()
game_over = False

clock = pygame.time.Clock()
FPS = 60

# --- 게임 함수 ---

def spawn_word():
    """새로운 단어를 화면 상단 무작위 위치에 생성합니다."""
    global last_spawn_time, base_word_speed, word_spawn_delay
    if not word_list: # 단어 목록이 비어있으면 생성하지 않음
        return
    word_text = random.choice(word_list)
    try:
        word_surface = word_font.render(word_text, True, WHITE)
    except pygame.error as e:
        print(f"Error rendering word '{word_text}': {e}")
        # 렌더링 오류 시 해당 단어 제외하고 다시 시도하거나 기본값 사용
        if word_text in word_list: # 제거 전에 존재하는지 확인
            word_list.remove(word_text) # 문제가 되는 단어 제거 (임시 방편)
        return
    word_rect = word_surface.get_rect()
    word_rect.x = random.randint(50, SCREEN_WIDTH - word_rect.width - 50)
    word_rect.y = -word_rect.height # 화면 바로 위에서 시작
    speed_multiplier = 1 + (score / 100) # 점수에 따라 속도 약간 증가
    word_speed = base_word_speed * speed_multiplier * random.uniform(0.8, 1.2) # 약간의 속도 변화 추가
    falling_words.append({'text': word_text, 'rect': word_rect, 'speed': word_speed, 'surface': word_surface})
    last_spawn_time = time.time()

def draw_elements():
    """화면에 게임 요소들을 그립니다."""
    screen.fill(BLACK)

    # 떨어지는 단어 그리기
    for word_info in falling_words:
        # 입력 중인 단어와 일치하는 부분 강조
        if current_input and word_info['text'].startswith(current_input):
             # 입력된 부분은 다른 색으로 표시
            try:
                typed_part = word_font.render(current_input, True, BLUE)
                remaining_part = word_font.render(word_info['text'][len(current_input):], True, WHITE)
                screen.blit(typed_part, word_info['rect'].topleft)
                screen.blit(remaining_part, (word_info['rect'].x + typed_part.get_width(), word_info['rect'].y))
            except pygame.error as e:
                 print(f"Error rendering partial word '{word_info['text']}': {e}")
                 # 오류 발생 시 기본 텍스트 표시
                 screen.blit(word_info['surface'], word_info['rect'].topleft)
        else:
            screen.blit(word_info['surface'], word_info['rect'].topleft)


    # 점수 및 목숨 표시
    score_label = score_font.render(f"점수: {score}", True, WHITE)
    lives_label = score_font.render(f"목숨: {'❤' * lives}", True, RED)
    screen.blit(score_label, (10, 10))
    screen.blit(lives_label, (SCREEN_WIDTH - lives_label.get_width() - 10, 10))

    # 사용자 입력 표시
    try:
        input_surface = input_font.render(current_input, True, WHITE)
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        # 입력창 배경 (선택적)
        pygame.draw.rect(screen, GRAY, (input_rect.x - 10, input_rect.y - 5, input_rect.width + 20, input_rect.height + 10), border_radius=5)
        screen.blit(input_surface, input_rect)
    except pygame.error as e:
        print(f"Error rendering input '{current_input}': {e}")
        # 입력 렌더링 오류 시 빈 사각형 표시 등 대체 처리 가능


    # 게임 오버 메시지
    if game_over:
        game_over_label = game_over_font.render("게임 오버!", True, RED)
        restart_label = score_font.render("다시 시작하려면 R 키를 누르세요", True, WHITE)
        screen.blit(game_over_label, game_over_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
        screen.blit(restart_label, restart_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

    pygame.display.flip()

def reset_game():
    """게임을 초기 상태로 리셋합니다."""
    global score, lives, falling_words, current_input, game_over, last_spawn_time, level_up_time, base_word_speed, word_spawn_delay
    score = 0
    lives = 5
    falling_words = []
    current_input = ""
    game_over = False
    base_word_speed = 1.5
    word_spawn_delay = 1.5
    last_spawn_time = time.time()
    level_up_time = time.time()
    spawn_word() # 게임 시작 시 첫 단어 생성


# --- 메인 게임 루프 ---
running = True
spawn_word() # 첫 단어 생성

while running:
    dt = clock.tick(FPS) / 1000.0 # Delta time (초 단위)

    # --- 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: # 엔터나 스페이스로 단어 완성 시도
                    word_matched = False
                    # 입력된 단어와 일치하는 떨어지는 단어 찾기
                    # 여러 단어가 매칭될 경우 가장 아래에 있는 단어를 우선 처리
                    matching_words = [w for w in falling_words if w['text'] == current_input]
                    if matching_words:
                        # 가장 아래에 있는 단어 찾기 (y 좌표가 가장 큰 것)
                        target_word_info = max(matching_words, key=lambda w: w['rect'].bottom)
                        score += len(target_word_info['text']) # 단어 길이만큼 점수 증가
                        falling_words.remove(target_word_info)
                        word_matched = True

                    current_input = "" # 입력 초기화

                # KEYDOWN 이벤트에서 문자 입력 처리는 제거 (TEXTINPUT 사용)
                # elif event.unicode.isalnum() or event.unicode in "가-힣":
                #     current_input += event.unicode

        elif event.type == pygame.TEXTINPUT and not game_over: # Handle text input including IME
            current_input += event.text

    if not game_over:
        # --- 게임 로직 업데이트 ---
        current_time = time.time()

        # 단어 생성 (시간 간격 기반)
        if current_time - last_spawn_time > word_spawn_delay:
            spawn_word()

        # 난이도 조절 (예: 15초마다 속도 및 생성 간격 조절)
        if current_time - level_up_time > 15:
            base_word_speed += 0.15 # 기본 속도 증가
            word_spawn_delay = max(0.3, word_spawn_delay * 0.95) # 생성 간격 감소 (최소 0.3초)
            level_up_time = current_time
            print(f"Level Up! Speed: {base_word_speed:.2f}, Delay: {word_spawn_delay:.2f}")


        # 단어 이동 및 충돌 처리
        words_to_remove = []
        # 시간 기반 이동으로 변경 (dt 사용)
        for word_info in falling_words:
            # word_info['rect'].y += word_info['speed'] * (dt * FPS) # 이전 방식 (프레임 의존적)
            word_info['rect'].y += word_info['speed'] * 60 * dt # 시간 기반 이동 (속도를 초당 픽셀로 가정)

            # 바닥 충돌 확인
            if word_info['rect'].bottom > SCREEN_HEIGHT:
                words_to_remove.append(word_info)
                lives -= 1
                if lives <= 0:
                    game_over = True
                    break # 게임 오버 시 루프 중단

        # 충돌한 단어 제거
        for word in words_to_remove:
             # 리스트에 해당 단어가 아직 있는지 확인 후 제거 (중복 제거 방지)
             if word in falling_words:
                falling_words.remove(word)

        # 입력과 일치하는 단어 자동 제거 (타이핑 중 완성) - 선택적 기능
        # 이 기능을 활성화하면 엔터/스페이스 없이도 단어가 완성되면 바로 사라짐
        # for word_info in list(falling_words): # list()로 복사본 순회 (제거 중 에러 방지)
        #     if word_info['text'] == current_input:
        #         score += len(word_info['text'])
        #         falling_words.remove(word_info)
        #         current_input = "" # 입력 초기화
        #         break # 한 번에 하나의 단어만 처리


    # --- 화면 그리기 ---
    draw_elements()

pygame.key.stop_text_input() # 게임 종료 시 텍스트 입력 처리 중지
pygame.quit()
sys.exit()

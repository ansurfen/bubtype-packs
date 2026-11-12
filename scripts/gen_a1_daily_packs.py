# -*- coding: utf-8 -*-
"""Generate curated A1 daily packs (words + short sentences) with Chinese glosses."""
from __future__ import annotations

import json
from pathlib import Path

# Packs repo root (this file lives in scripts/).
ROOT = Path(__file__).resolve().parents[1]


def item(text: str, hint: str, kind: str, spell: str | None = None) -> dict:
    out = {"text": text, "hint": hint, "kind": kind}
    if spell:
        out["spell"] = spell
    return out


def write_pack(
    pack_id: str,
    title: str,
    lang: str,
    gloss_lang: str,
    description: str,
    items: list[dict],
    source: str = "curated-a1",
) -> None:
    payload = {
        "manifest": {
            "id": pack_id,
            "title": title,
            "version": "1.0.0",
            "lang": lang,
            "glossLang": gloss_lang,
            "source": source,
            "lemmaCount": len(items),
            "description": description,
        },
        "items": items,
    }
    path = ROOT / f"{pack_id}-v1.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.name} ({len(items)} items)")


# --- Korean: Revised Romanization ---
KO_WORDS = [
    ("안녕하세요", "你好", "annyeonghaseyo"),
    ("감사합니다", "谢谢", "gamsahamnida"),
    ("미안합니다", "对不起", "mianhamnida"),
    ("괜찮아요", "没关系", "gwaenchanayo"),
    ("네", "是", "ne"),
    ("아니요", "不", "aniyo"),
    ("주세요", "请给我", "juseyo"),
    ("얼마예요", "多少钱？", "eolmayeyo"),
    ("어디예요", "在哪里？", "eodiyeyo"),
    ("화장실", "厕所", "hwajangsil"),
    ("물", "水", "mul"),
    ("커피", "咖啡", "keopi"),
    ("밥", "米饭；饭", "bap"),
    ("친구", "朋友", "chingu"),
    ("가족", "家人", "gajok"),
    ("학교", "学校", "hakgyo"),
    ("회사", "公司", "hoesa"),
    ("집", "家", "jip"),
    ("오늘", "今天", "oneul"),
    ("내일", "明天", "naeil"),
    ("어제", "昨天", "eoje"),
    ("아침", "早上", "achim"),
    ("저녁", "晚上；晚饭", "jeonyeok"),
    ("시간", "时间", "sigan"),
    ("사람", "人", "saram"),
    ("이름", "名字", "ireum"),
    ("한국", "韩国", "hanguk"),
    ("중국", "中国", "jungguk"),
    ("영어", "英语", "yeongeo"),
    ("한국어", "韩语", "hangugeo"),
    ("좋아하다", "喜欢", "joahada"),
    ("먹다", "吃", "meokda"),
    ("마시다", "喝", "masida"),
    ("가다", "去", "gada"),
    ("오다", "来", "oda"),
    ("보다", "看", "boda"),
    ("듣다", "听", "deutda"),
    ("말하다", "说", "malhada"),
    ("공부하다", "学习", "gongbuhada"),
    ("일하다", "工作", "ilhada"),
]

KO_SENTS = [
    ("오늘 날씨가 좋아요", "今天天气很好", "oneul nalssiga joayo"),
    ("커피 한 잔 주세요", "请给我一杯咖啡", "keopi han jan juseyo"),
    ("역이 어디에 있어요", "车站在哪里？", "yeogi eodie isseoyo"),
    ("창문을 열어 주세요", "请打开窗户", "changmuneul yeoreo juseyo"),
    ("내일 일해요", "明天要上班", "naeil ilhaeyo"),
    ("이 책이 재미있어요", "这本书很有意思", "i chaegi jaemiisseoyo"),
    ("한국어 할 수 있어요", "你会说韩语吗？", "hangugeo hal su isseoyo"),
    ("잘 모르겠어요", "我不太明白", "jal moreugesseoyo"),
    ("다시 말해 주세요", "请再说一遍", "dasi malhae juseyo"),
    ("지금 몇 시예요", "现在几点了？", "jigeum myeot siyeyo"),
    ("음악 듣는 걸 좋아해요", "我喜欢听音乐", "eumak deunneun geol joahaeyo"),
    ("주말에 공원에 가요", "周末去公园", "jumare gongwone gayo"),
    ("밥 먹었어요", "吃饭了吗？／吃饭了", "bap meogeosseoyo"),
    ("너무 비싸요", "太贵了", "neomu bissayo"),
    ("한번 입어봐도 돼요", "我可以试试吗？", "hanbeon ibeobwado dwaeyo"),
    ("만나서 반가워요", "见到你很高兴", "mannaseo bangawoyo"),
    ("도와주세요", "请帮帮我", "dowajuseyo"),
    ("저는 학생이에요", "我是学生", "jeoneun haksaengieyo"),
    ("이름이 뭐예요", "你叫什么名字？", "ireumi mwoyeyo"),
    ("천천히 말해 주세요", "请说慢一点", "cheoncheonhi malhae juseyo"),
    ("여기 메뉴 있어요", "这里有菜单吗？", "yeogi menyu isseoyo"),
    ("계산해 주세요", "请结账", "gyesanhae juseyo"),
    ("지하철을 타세요", "请坐地铁", "jihacheoreul taseyo"),
    ("내일 봐요", "明天见", "naeil bwayo"),
]

# --- Spanish (spell = accent-stripped for spell mode) ---
ES_WORDS = [
    ("hola", "你好", "hola"),
    ("gracias", "谢谢", "gracias"),
    ("de nada", "不客气", "de nada"),
    ("perdón", "对不起", "perdon"),
    ("por favor", "请", "por favor"),
    ("sí", "是", "si"),
    ("no", "不", "no"),
    ("adiós", "再见", "adios"),
    ("buenos días", "早上好", "buenos dias"),
    ("buenas noches", "晚安", "buenas noches"),
    ("agua", "水", "agua"),
    ("café", "咖啡", "cafe"),
    ("comida", "食物", "comida"),
    ("amigo", "朋友", "amigo"),
    ("familia", "家人", "familia"),
    ("escuela", "学校", "escuela"),
    ("trabajo", "工作", "trabajo"),
    ("casa", "家", "casa"),
    ("hoy", "今天", "hoy"),
    ("mañana", "明天；早上", "manana"),
    ("ayer", "昨天", "ayer"),
    ("tiempo", "时间；天气", "tiempo"),
    ("persona", "人", "persona"),
    ("nombre", "名字", "nombre"),
    ("España", "西班牙", "Espana"),
    ("China", "中国", "China"),
    ("inglés", "英语", "ingles"),
    ("español", "西班牙语", "espanol"),
    ("gustar", "喜欢", "gustar"),
    ("comer", "吃", "comer"),
    ("beber", "喝", "beber"),
    ("ir", "去", "ir"),
    ("venir", "来", "venir"),
    ("ver", "看", "ver"),
    ("oír", "听", "oir"),
    ("hablar", "说", "hablar"),
    ("estudiar", "学习", "estudiar"),
    ("trabajar", "工作", "trabajar"),
    ("baño", "厕所；浴室", "bano"),
    ("cuánto", "多少", "cuanto"),
]

ES_SENTS = [
    ("Hoy hace buen tiempo", "今天天气很好", "Hoy hace buen tiempo"),
    ("Quiero un café, por favor", "我想要一杯咖啡", "Quiero un cafe, por favor"),
    ("¿Dónde está la estación?", "车站在哪里？", "Donde esta la estacion?"),
    ("Abre la ventana, por favor", "请打开窗户", "Abre la ventana, por favor"),
    ("Mañana voy al trabajo", "明天去上班", "Manana voy al trabajo"),
    ("Este libro es interesante", "这本书很有意思", "Este libro es interesante"),
    ("¿Hablas español?", "你会说西班牙语吗？", "Hablas espanol?"),
    ("No entiendo bien", "我不太明白", "No entiendo bien"),
    ("Repite, por favor", "请再说一遍", "Repite, por favor"),
    ("¿Qué hora es?", "现在几点了？", "Que hora es?"),
    ("Me gusta la música", "我喜欢音乐", "Me gusta la musica"),
    ("Vamos al parque el fin de semana", "周末去公园吧", "Vamos al parque el fin de semana"),
    ("¿Ya comiste?", "吃饭了吗？", "Ya comiste?"),
    ("Es demasiado caro", "太贵了", "Es demasiado caro"),
    ("¿Puedo probarlo?", "我可以试试吗？", "Puedo probarlo?"),
    ("Mucho gusto", "见到你很高兴", "Mucho gusto"),
    ("Ayúdame, por favor", "请帮帮我", "Ayudame, por favor"),
    ("Soy estudiante", "我是学生", "Soy estudiante"),
    ("¿Cómo te llamas?", "你叫什么名字？", "Como te llamas?"),
    ("Habla más despacio, por favor", "请说慢一点", "Habla mas despacio, por favor"),
    ("¿Tienen menú?", "有菜单吗？", "Tienen menu?"),
    ("La cuenta, por favor", "请结账", "La cuenta, por favor"),
    ("Toma el metro", "请坐地铁", "Toma el metro"),
    ("Hasta mañana", "明天见", "Hasta manana"),
]

# --- French daily sentences (core words already in fr-core-a1-zh) ---
FR_WORDS = [
    ("bonjour", "你好", "bonjour"),
    ("merci", "谢谢", "merci"),
    ("de rien", "不客气", "de rien"),
    ("pardon", "对不起", "pardon"),
    ("s'il vous plaît", "请", "s'il vous plait"),
    ("oui", "是", "oui"),
    ("non", "不", "non"),
    ("au revoir", "再见", "au revoir"),
    ("bonsoir", "晚上好", "bonsoir"),
    ("bonne nuit", "晚安", "bonne nuit"),
    ("eau", "水", "eau"),
    ("café", "咖啡", "cafe"),
    ("pain", "面包", "pain"),
    ("ami", "朋友", "ami"),
    ("famille", "家人", "famille"),
    ("école", "学校", "ecole"),
    ("travail", "工作", "travail"),
    ("maison", "家", "maison"),
    ("aujourd'hui", "今天", "aujourd'hui"),
    ("demain", "明天", "demain"),
    ("hier", "昨天", "hier"),
    ("temps", "时间；天气", "temps"),
    ("personne", "人", "personne"),
    ("nom", "名字", "nom"),
    ("France", "法国", "France"),
    ("Chine", "中国", "Chine"),
    ("anglais", "英语", "anglais"),
    ("français", "法语", "francais"),
    ("aimer", "喜欢", "aimer"),
    ("manger", "吃", "manger"),
    ("boire", "喝", "boire"),
    ("aller", "去", "aller"),
    ("venir", "来", "venir"),
    ("voir", "看", "voir"),
    ("écouter", "听", "ecouter"),
    ("parler", "说", "parler"),
    ("étudier", "学习", "etudier"),
    ("travailler", "工作", "travailler"),
    ("toilettes", "厕所", "toilettes"),
    ("combien", "多少", "combien"),
]

FR_SENTS = [
    ("Il fait beau aujourd'hui", "今天天气很好", "Il fait beau aujourd'hui"),
    ("Je voudrais un café, s'il vous plaît", "我想要一杯咖啡", "Je voudrais un cafe, s'il vous plait"),
    ("Où est la gare ?", "车站在哪里？", "Ou est la gare ?"),
    ("Ouvrez la fenêtre, s'il vous plaît", "请打开窗户", "Ouvrez la fenetre, s'il vous plait"),
    ("Demain je vais au travail", "明天去上班", "Demain je vais au travail"),
    ("Ce livre est intéressant", "这本书很有意思", "Ce livre est interessant"),
    ("Parlez-vous français ?", "你会说法语吗？", "Parlez-vous francais ?"),
    ("Je ne comprends pas bien", "我不太明白", "Je ne comprends pas bien"),
    ("Répétez, s'il vous plaît", "请再说一遍", "Repetez, s'il vous plait"),
    ("Quelle heure est-il ?", "现在几点了？", "Quelle heure est-il ?"),
    ("J'aime la musique", "我喜欢音乐", "J'aime la musique"),
    ("Allons au parc ce week-end", "周末去公园吧", "Allons au parc ce week-end"),
    ("Tu as mangé ?", "吃饭了吗？", "Tu as mange ?"),
    ("C'est trop cher", "太贵了", "C'est trop cher"),
    ("Je peux essayer ?", "我可以试试吗？", "Je peux essayer ?"),
    ("Enchanté", "见到你很高兴", "Enchante"),
    ("Aidez-moi, s'il vous plaît", "请帮帮我", "Aidez-moi, s'il vous plait"),
    ("Je suis étudiant", "我是学生", "Je suis etudiant"),
    ("Comment vous appelez-vous ?", "您叫什么名字？", "Comment vous appelez-vous ?"),
    ("Parlez plus lentement, s'il vous plaît", "请说慢一点", "Parlez plus lentement, s'il vous plait"),
    ("Avez-vous un menu ?", "有菜单吗？", "Avez-vous un menu ?"),
    ("L'addition, s'il vous plaît", "请结账", "L'addition, s'il vous plait"),
    ("Prenez le métro", "请坐地铁", "Prenez le metro"),
    ("À demain", "明天见", "A demain"),
]

# --- Expand Chinese (gloss EN for learners of Chinese) ---
ZH_WORDS = [
    ("你好", "Hello", "nǐ hǎo"),
    ("谢谢", "Thank you", "xiè xie"),
    ("不客气", "You're welcome", "bú kè qi"),
    ("对不起", "Sorry", "duì bu qǐ"),
    ("没关系", "It's okay", "méi guān xi"),
    ("再见", "Goodbye", "zài jiàn"),
    ("早上好", "Good morning", "zǎo shang hǎo"),
    ("晚安", "Good night", "wǎn ān"),
    ("请", "Please", "qǐng"),
    ("是", "Yes", "shì"),
    ("不", "No", "bù"),
    ("水", "Water", "shuǐ"),
    ("咖啡", "Coffee", "kā fēi"),
    ("吃饭", "Eat a meal", "chī fàn"),
    ("朋友", "Friend", "péng you"),
    ("家人", "Family", "jiā rén"),
    ("学校", "School", "xué xiào"),
    ("公司", "Company", "gōng sī"),
    ("家", "Home", "jiā"),
    ("今天", "Today", "jīn tiān"),
    ("明天", "Tomorrow", "míng tiān"),
    ("昨天", "Yesterday", "zuó tiān"),
    ("时间", "Time", "shí jiān"),
    ("人", "Person", "rén"),
    ("名字", "Name", "míng zi"),
    ("中国", "China", "zhōng guó"),
    ("英语", "English", "yīng yǔ"),
    ("中文", "Chinese", "zhōng wén"),
    ("喜欢", "Like", "xǐ huan"),
    ("吃", "Eat", "chī"),
    ("喝", "Drink", "hē"),
    ("去", "Go", "qù"),
    ("来", "Come", "lái"),
    ("看", "Look / watch", "kàn"),
    ("听", "Listen", "tīng"),
    ("说", "Speak", "shuō"),
    ("学习", "Study", "xué xí"),
    ("工作", "Work", "gōng zuò"),
    ("厕所", "Restroom", "cè suǒ"),
    ("多少钱", "How much?", "duō shao qián"),
]

ZH_SENTS = [
    ("今天天气很好", "The weather is nice today", "jīn tiān tiān qì hěn hǎo"),
    ("我想喝咖啡", "I want coffee", "wǒ xiǎng hē kā fēi"),
    ("请问车站在哪里", "Where is the station?", "qǐng wèn chē zhàn zài nǎ lǐ"),
    ("请打开窗户", "Please open the window", "qǐng dǎ kāi chuāng hu"),
    ("我明天上班", "I go to work tomorrow", "wǒ míng tiān shàng bān"),
    ("这本书很有意思", "This book is interesting", "zhè běn shū hěn yǒu yì si"),
    ("你会说中文吗", "Do you speak Chinese?", "nǐ huì shuō zhōng wén ma"),
    ("我不太明白", "I don't quite understand", "wǒ bú tài míng bai"),
    ("请再说一遍", "Please say it again", "qǐng zài shuō yí biàn"),
    ("现在几点了", "What time is it now?", "xiàn zài jǐ diǎn le"),
    ("我喜欢听音乐", "I like listening to music", "wǒ xǐ huan tīng yīn yuè"),
    ("周末去公园吧", "Let's go to the park this weekend", "zhōu mò qù gōng yuán ba"),
    ("吃饭了吗", "Have you eaten?", "chī fàn le ma"),
    ("太贵了", "Too expensive", "tài guì le"),
    ("我可以试试吗", "May I try it?", "wǒ kě yǐ shì shi ma"),
    ("很高兴认识你", "Nice to meet you", "hěn gāo xìng rèn shi nǐ"),
    ("请帮帮我", "Please help me", "qǐng bāng bang wǒ"),
    ("我是学生", "I am a student", "wǒ shì xué sheng"),
    ("你叫什么名字", "What is your name?", "nǐ jiào shén me míng zi"),
    ("请说慢一点", "Please speak more slowly", "qǐng shuō màn yì diǎn"),
    ("有菜单吗", "Do you have a menu?", "yǒu cài dān ma"),
    ("买单", "Check, please", "mǎi dān"),
    ("请坐地铁", "Please take the subway", "qǐng zuò dì tiě"),
    ("明天见", "See you tomorrow", "míng tiān jiàn"),
]

# --- Japanese expand ---
JA_WORDS = [
    ("こんにちは", "你好", "konnichiwa"),
    ("ありがとう", "谢谢", "arigatou"),
    ("すみません", "对不起；劳驾", "sumimasen"),
    ("おはようございます", "早上好", "ohayou gozaimasu"),
    ("おやすみなさい", "晚安", "oyasuminasai"),
    ("さようなら", "再见", "sayounara"),
    ("はい", "是", "hai"),
    ("いいえ", "不", "iie"),
    ("ください", "请给我", "kudasai"),
    ("いくら", "多少钱", "ikura"),
    ("どこ", "哪里", "doko"),
    ("トイレ", "厕所", "toire"),
    ("水", "水", "mizu"),
    ("コーヒー", "咖啡", "koohii"),
    ("ご飯", "米饭；饭", "gohan"),
    ("友達", "朋友", "tomodachi"),
    ("家族", "家人", "kazoku"),
    ("学校", "学校", "gakkou"),
    ("会社", "公司", "kaisha"),
    ("家", "家", "uchi"),
    ("今日", "今天", "kyou"),
    ("明日", "明天", "ashita"),
    ("昨日", "昨天", "kinou"),
    ("時間", "时间", "jikan"),
    ("人", "人", "hito"),
    ("名前", "名字", "namae"),
    ("日本", "日本", "nihon"),
    ("中国", "中国", "chuugoku"),
    ("英語", "英语", "eigo"),
    ("日本語", "日语", "nihongo"),
    ("好き", "喜欢", "suki"),
    ("食べる", "吃", "taberu"),
    ("飲む", "喝", "nomu"),
    ("行く", "去", "iku"),
    ("来る", "来", "kuru"),
    ("見る", "看", "miru"),
    ("聞く", "听", "kiku"),
    ("話す", "说", "hanasu"),
    ("勉強する", "学习", "benkyou suru"),
    ("働く", "工作", "hataraku"),
]

JA_SENTS = [
    ("今日はいい天気です", "今天天气很好", "kyou wa ii tenki desu"),
    ("コーヒーをください", "请给我咖啡", "koohii o kudasai"),
    ("駅はどこですか", "车站在哪里？", "eki wa doko desu ka"),
    ("窓を開けてください", "请打开窗户", "mado o akete kudasai"),
    ("明日は仕事です", "明天要上班", "ashita wa shigoto desu"),
    ("この本は面白いです", "这本书很有意思", "kono hon wa omoshiroi desu"),
    ("日本語が話せますか", "你会说日语吗？", "nihongo ga hanasemasu ka"),
    ("よくわかりません", "我不太明白", "yoku wakarimasen"),
    ("もう一度お願いします", "请再说一遍", "mou ichido onegaishimasu"),
    ("今何時ですか", "现在几点了？", "ima nanji desu ka"),
    ("音楽が好きです", "我喜欢音乐", "ongaku ga suki desu"),
    ("週末に公園へ行きましょう", "周末去公园吧", "shuumatsu ni kouen e ikimashou"),
    ("ご飯を食べましたか", "吃饭了吗？", "gohan o tabemashita ka"),
    ("高すぎます", "太贵了", "takasugimasu"),
    ("試着してもいいですか", "我可以试试吗？", "shichaku shite mo ii desu ka"),
    ("はじめまして", "初次见面", "hajimemashite"),
    ("手伝ってください", "请帮帮我", "tetsudatte kudasai"),
    ("学生です", "我是学生", "gakusei desu"),
    ("お名前は何ですか", "你叫什么名字？", "onamae wa nan desu ka"),
    ("ゆっくり話してください", "请说慢一点", "yukkuri hanashite kudasai"),
    ("メニューはありますか", "有菜单吗？", "menyuu wa arimasu ka"),
    ("お会計お願いします", "请结账", "okaikei onegaishimasu"),
    ("地下鉄に乗ってください", "请坐地铁", "chikatetsu ni notte kudasai"),
    ("また明日", "明天见", "mata ashita"),
]


def pack_items(words, sents):
    items = [item(t, h, "phrase", s) for t, h, s in words]
    items += [item(t, h, "sentence", s) for t, h, s in sents]
    return items


def main() -> None:
    packs = [
        (
            "ko-daily-a1-zh",
            "韩语日常 A1",
            "ko",
            "zh",
            "韩语入门词句 · 中文释义（罗马音拼写）",
            pack_items(KO_WORDS, KO_SENTS),
        ),
        (
            "es-daily-a1-zh",
            "西语日常 A1",
            "es",
            "zh",
            "西班牙语入门词句 · 中文释义",
            pack_items(ES_WORDS, ES_SENTS),
        ),
        (
            "fr-daily-a1-zh",
            "法语日常 A1",
            "fr",
            "zh",
            "法语入门词句 · 中文释义（配合核心词表）",
            pack_items(FR_WORDS, FR_SENTS),
        ),
        (
            "zh-daily-a1",
            "中文日常 A1",
            "zh",
            "en",
            "常用中文词句 · 英文释义（拼音输入）",
            pack_items(ZH_WORDS, ZH_SENTS),
            "1.1.0",
        ),
        (
            "ja-daily-a1",
            "日语日常 A1",
            "ja",
            "zh",
            "常用日语词句 · 中文释义（罗马字拼写）",
            pack_items(JA_WORDS, JA_SENTS),
            "1.1.0",
        ),
    ]

    catalog_path = ROOT / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    by_id = {b["id"]: b for b in catalog["books"]}

    for pack in packs:
        if len(pack) == 6:
            pack_id, title, lang, gloss, desc, items = pack
            version = "1.0.0"
        else:
            pack_id, title, lang, gloss, desc, items, version = pack
        # rewrite with version
        payload = {
            "manifest": {
                "id": pack_id,
                "title": title,
                "version": version,
                "lang": lang,
                "glossLang": gloss,
                "source": "curated-a1",
                "lemmaCount": len(items),
                "description": desc,
            },
            "items": items,
        }
        path = ROOT / f"{pack_id}-v1.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.name} ({len(items)} items, v{version})")
        by_id[pack_id] = {
            "id": pack_id,
            "title": title,
            "version": version,
            "lang": lang,
            "glossLang": gloss,
            "lemmaCount": len(items),
            "description": desc,
            "asset": f"{pack_id}-v1.json",
        }

    # Keep stable-ish order: existing non-overwritten first, then ensure new langs present
    preferred = [
        "morning",
        "cafe",
        "commute",
        "meeting",
        "daily-a1",
        "daily-a2",
        "oxford-3000-zh",
        "oxford-3000-en",
        "oxford-3000-ja",
        "oxford-5000-zh",
        "oxford-5000-en",
        "oxford-5000-ja",
        "fr-core-a1-zh",
        "fr-daily-a1-zh",
        "zh-daily-a1",
        "ja-daily-a1",
        "ko-daily-a1-zh",
        "es-daily-a1-zh",
    ]
    books = []
    seen = set()
    for pid in preferred:
        if pid in by_id:
            books.append(by_id[pid])
            seen.add(pid)
    for pid, book in by_id.items():
        if pid not in seen:
            books.append(book)

    catalog["books"] = books
    catalog["updatedAt"] = "2026-11-11"
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated catalog ({len(books)} books)")


if __name__ == "__main__":
    main()

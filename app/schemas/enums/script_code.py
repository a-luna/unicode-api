from __future__ import annotations

from enum import IntEnum, auto

from app.schemas.util import normalize_string_lm3


class ScriptCode(IntEnum):
    NONE = 0
    ADLAM = auto()
    AHOM = auto()
    ANATOLIAN_HIEROGLYPHS = auto()
    ARABIC = auto()
    ARMENIAN = auto()
    AVESTAN = auto()
    BALINESE = auto()
    BAMUM = auto()
    BASSA_VAH = auto()
    BATAK = auto()
    BENGALI = auto()
    BHAIKSUKI = auto()
    BOPOMOFO = auto()
    BRAHMI = auto()
    BRAILLE = auto()
    BUGINESE = auto()
    BUHID = auto()
    CANADIAN_ABORIGINAL = auto()
    CARIAN = auto()
    CAUCASIAN_ALBANIAN = auto()
    CHAKMA = auto()
    CHAM = auto()
    CHEROKEE = auto()
    CHORASMIAN = auto()
    COMMON = auto()
    COPTIC = auto()
    CUNEIFORM = auto()
    CYPRIOT = auto()
    CYPRO_MINOAN = auto()
    CYRILLIC = auto()
    DESERET = auto()
    DEVANAGARI = auto()
    DIVES_AKURU = auto()
    DOGRA = auto()
    DUPLOYAN = auto()
    EGYPTIAN_HIEROGLYPHS = auto()
    ELBASAN = auto()
    ELYMAIC = auto()
    ETHIOPIC = auto()
    KHUTSURI = auto()
    GEORGIAN = auto()
    GLAGOLITIC = auto()
    GOTHIC = auto()
    GRANTHA = auto()
    GREEK = auto()
    GUJARATI = auto()
    GUNJALA_GONDI = auto()
    GURMUKHI = auto()
    HAN = auto()
    HANGUL = auto()
    HANIFI_ROHINGYA = auto()
    HANUNOO = auto()
    HATRAN = auto()
    HEBREW = auto()
    HIRAGANA = auto()
    IMPERIAL_ARAMAIC = auto()
    INHERITED = auto()
    INSCRIPTIONAL_PAHLAVI = auto()
    INSCRIPTIONAL_PARTHIAN = auto()
    JAVANESE = auto()
    KAITHI = auto()
    KANNADA = auto()
    KATAKANA = auto()
    KATAKANA_OR_HIRAGANA = auto()
    KAWI = auto()
    KAYAH_LI = auto()
    KHAROSHTHI = auto()
    KHITAN_SMALL_SCRIPT = auto()
    KHMER = auto()
    KHOJKI = auto()
    KHUDAWADI = auto()
    LAO = auto()
    LATIN = auto()
    LEPCHA = auto()
    LIMBU = auto()
    LINEAR_A = auto()
    LINEAR_B = auto()
    LISU = auto()
    LYCIAN = auto()
    LYDIAN = auto()
    MAHAJANI = auto()
    MAKASAR = auto()
    MALAYALAM = auto()
    MANDAIC = auto()
    MANICHAEAN = auto()
    MARCHEN = auto()
    MASARAM_GONDI = auto()
    MEDEFAIDRIN = auto()
    MEETEI_MAYEK = auto()
    MENDE_KIKAKUI = auto()
    MEROITIC_CURSIVE = auto()
    MEROITIC_HIEROGLYPHS = auto()
    MIAO = auto()
    MODI = auto()
    MONGOLIAN = auto()
    MRO = auto()
    MULTANI = auto()
    MYANMAR = auto()
    NABATAEAN = auto()
    NAG_MUNDARI = auto()
    NANDINAGARI = auto()
    NEW_TAI_LUE = auto()
    NEWA = auto()
    N_KO = auto()
    NUSHU = auto()
    NYIAKENG_PUACHUE_HMONG = auto()
    OGHAM = auto()
    OL_CHIKI = auto()
    OLD_HUNGARIAN = auto()
    OLD_ITALIC = auto()
    OLD_NORTH_ARABIAN = auto()
    OLD_PERMIC = auto()
    OLD_PERSIAN = auto()
    OLD_SOGDIAN = auto()
    OLD_SOUTH_ARABIAN = auto()
    OLD_TURKIC = auto()
    OLD_UYGHUR = auto()
    ORIYA = auto()
    OSAGE = auto()
    OSMANYA = auto()
    PAHAWH_HMONG = auto()
    PALMYRENE = auto()
    PAU_CIN_HAU = auto()
    PHAGS_PA = auto()
    PHOENICIAN = auto()
    PSALTER_PAHLAVI = auto()
    REJANG = auto()
    RUNIC = auto()
    SAMARITAN = auto()
    SAURASHTRA = auto()
    SHARADA = auto()
    SHAVIAN = auto()
    SIDDHAM = auto()
    SIGN_WRITING = auto()
    SINHALA = auto()
    SOGDIAN = auto()
    SORA_SOMPENG = auto()
    SOYOMBO = auto()
    SUNDANESE = auto()
    SYLOTI_NAGRI = auto()
    SYRIAC = auto()
    TAGALOG = auto()
    TAGBANWA = auto()
    TAI_LE = auto()
    TAI_THAM = auto()
    TAI_VIET = auto()
    TAKRI = auto()
    TAMIL = auto()
    TANGSA = auto()
    TANGUT = auto()
    TELUGU = auto()
    THAANA = auto()
    THAI = auto()
    TIBETAN = auto()
    TIFINAGH = auto()
    TIRHUTA = auto()
    TOTO = auto()
    UGARITIC = auto()
    UNKNOWN = auto()
    VAI = auto()
    VITHKUQI = auto()
    WANCHO = auto()
    WARANG_CITI = auto()
    YEZIDI = auto()
    YI = auto()
    ZANABAZAR_SQUARE = auto()

    def __str__(self):
        return (
            self.name.replace("_", " ")
            .title()
            .replace("N Ko", "NKo")
            .replace("Phags Pa", "Phags-pa")
            .replace("Sign Writing", "SignWriting")
        )

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.code)

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "ADLAM": "Adlm",
            "AHOM": "Ahom",
            "ANATOLIAN_HIEROGLYPHS": "Hluw",
            "ARABIC": "Arab",
            "ARMENIAN": "Armn",
            "AVESTAN": "Avst",
            "BALINESE": "Bali",
            "BAMUM": "Bamu",
            "BASSA_VAH": "Bass",
            "BATAK": "Batk",
            "BENGALI": "Beng",
            "BHAIKSUKI": "Bhks",
            "BOPOMOFO": "Bopo",
            "BRAHMI": "Brah",
            "BRAILLE": "Brai",
            "BUGINESE": "Bugi",
            "BUHID": "Buhd",
            "CANADIAN_ABORIGINAL": "Cans",
            "CARIAN": "Cari",
            "CAUCASIAN_ALBANIAN": "Aghb",
            "CHAKMA": "Cakm",
            "CHAM": "Cham",
            "CHEROKEE": "Cher",
            "CHORASMIAN": "Chrs",
            "COMMON": "Zyyy",
            "COPTIC": "Copt",
            "CUNEIFORM": "Xsux",
            "CYPRIOT": "Cprt",
            "CYPRO_MINOAN": "Cpmn",
            "CYRILLIC": "Cyrl",
            "DESERET": "Dsrt",
            "DEVANAGARI": "Deva",
            "DIVES_AKURU": "Diak",
            "DOGRA": "Dogr",
            "DUPLOYAN": "Dupl",
            "EGYPTIAN_HIEROGLYPHS": "Egyp",
            "ELBASAN": "Elba",
            "ELYMAIC": "Elym",
            "ETHIOPIC": "Ethi",
            "KHUTSURI": "Geok",
            "GEORGIAN": "Geor",
            "GLAGOLITIC": "Glag",
            "GOTHIC": "Goth",
            "GRANTHA": "Gran",
            "GREEK": "Grek",
            "GUJARATI": "Gujr",
            "GUNJALA_GONDI": "Gong",
            "GURMUKHI": "Guru",
            "HAN": "Hani",
            "HANGUL": "Hang",
            "HANIFI_ROHINGYA": "Rohg",
            "HANUNOO": "Hano",
            "HATRAN": "Hatr",
            "HEBREW": "Hebr",
            "HIRAGANA": "Hira",
            "IMPERIAL_ARAMAIC": "Armi",
            "INHERITED": "Zinh",
            "INSCRIPTIONAL_PAHLAVI": "Phli",
            "INSCRIPTIONAL_PARTHIAN": "Prti",
            "JAVANESE": "Java",
            "KAITHI": "Kthi",
            "KANNADA": "Knda",
            "KATAKANA": "Kana",
            "KATAKANA_OR_HIRAGANA": "Hrkt",
            "KAWI": "Kawi",
            "KAYAH_LI": "Kali",
            "KHAROSHTHI": "Khar",
            "KHITAN_SMALL_SCRIPT": "Kits",
            "KHMER": "Khmr",
            "KHOJKI": "Khoj",
            "KHUDAWADI": "Sind",
            "LAO": "Laoo",
            "LATIN": "Latn",
            "LEPCHA": "Lepc",
            "LIMBU": "Limb",
            "LINEAR_A": "Lina",
            "LINEAR_B": "Linb",
            "LISU": "Lisu",
            "LYCIAN": "Lyci",
            "LYDIAN": "Lydi",
            "MAHAJANI": "Mahj",
            "MAKASAR": "Maka",
            "MALAYALAM": "Mlym",
            "MANDAIC": "Mand",
            "MANICHAEAN": "Mani",
            "MARCHEN": "Marc",
            "MASARAM_GONDI": "Gonm",
            "MEDEFAIDRIN": "Medf",
            "MEETEI_MAYEK": "Mtei",
            "MENDE_KIKAKUI": "Mend",
            "MEROITIC_CURSIVE": "Merc",
            "MEROITIC_HIEROGLYPHS": "Mero",
            "MIAO": "Plrd",
            "MODI": "Modi",
            "MONGOLIAN": "Mong",
            "MRO": "Mroo",
            "MULTANI": "Mult",
            "MYANMAR": "Mymr",
            "NABATAEAN": "Nbat",
            "NAG_MUNDARI": "Nagm",
            "NANDINAGARI": "Nand",
            "NEW_TAI_LUE": "Talu",
            "NEWA": "Newa",
            "N_KO": "Nkoo",
            "NUSHU": "Nshu",
            "NYIAKENG_PUACHUE_HMONG": "Hmnp",
            "OGHAM": "Ogam",
            "OL_CHIKI": "Olck",
            "OLD_HUNGARIAN": "Hung",
            "OLD_ITALIC": "Ital",
            "OLD_NORTH_ARABIAN": "Narb",
            "OLD_PERMIC": "Perm",
            "OLD_PERSIAN": "Xpeo",
            "OLD_SOGDIAN": "Sogo",
            "OLD_SOUTH_ARABIAN": "Sarb",
            "OLD_TURKIC": "Orkh",
            "OLD_UYGHUR": "Ougr",
            "ORIYA": "Orya",
            "OSAGE": "Osge",
            "OSMANYA": "Osma",
            "PAHAWH_HMONG": "Hmng",
            "PALMYRENE": "Palm",
            "PAU_CIN_HAU": "Pauc",
            "PHAGS_PA": "Phag",
            "PHOENICIAN": "Phnx",
            "PSALTER_PAHLAVI": "Phlp",
            "REJANG": "Rjng",
            "RUNIC": "Runr",
            "SAMARITAN": "Samr",
            "SAURASHTRA": "Saur",
            "SHARADA": "Shrd",
            "SHAVIAN": "Shaw",
            "SIDDHAM": "Sidd",
            "SIGN_WRITING": "Sgnw",
            "SINHALA": "Sinh",
            "SOGDIAN": "Sogd",
            "SORA_SOMPENG": "Sora",
            "SOYOMBO": "Soyo",
            "SUNDANESE": "Sund",
            "SYLOTI_NAGRI": "Sylo",
            "SYRIAC": "Syrc",
            "TAGALOG": "Tglg",
            "TAGBANWA": "Tagb",
            "TAI_LE": "Tale",
            "TAI_THAM": "Lana",
            "TAI_VIET": "Tavt",
            "TAKRI": "Takr",
            "TAMIL": "Taml",
            "TANGSA": "Tnsa",
            "TANGUT": "Tang",
            "TELUGU": "Telu",
            "THAANA": "Thaa",
            "THAI": "Thai",
            "TIBETAN": "Tibt",
            "TIFINAGH": "Tfng",
            "TIRHUTA": "Tirh",
            "TOTO": "Toto",
            "UGARITIC": "Ugar",
            "UNKNOWN": "Zzzz",
            "VAI": "Vaii",
            "VITHKUQI": "Vith",
            "WANCHO": "Wcho",
            "WARANG_CITI": "Wara",
            "YEZIDI": "Yezi",
            "YI": "Yiii",
            "ZANABAZAR_SQUARE": "Zanb",
        }
        return code_map.get(self.name, "Zzzz")

    @classmethod
    def from_code(cls, code):
        code_map = {
            "Adlm": cls.ADLAM,
            "Ahom": cls.AHOM,
            "Hluw": cls.ANATOLIAN_HIEROGLYPHS,
            "Arab": cls.ARABIC,
            "Armn": cls.ARMENIAN,
            "Avst": cls.AVESTAN,
            "Bali": cls.BALINESE,
            "Bamu": cls.BAMUM,
            "Bass": cls.BASSA_VAH,
            "Batk": cls.BATAK,
            "Beng": cls.BENGALI,
            "Bhks": cls.BHAIKSUKI,
            "Bopo": cls.BOPOMOFO,
            "Brah": cls.BRAHMI,
            "Brai": cls.BRAILLE,
            "Bugi": cls.BUGINESE,
            "Buhd": cls.BUHID,
            "Cans": cls.CANADIAN_ABORIGINAL,
            "Cari": cls.CARIAN,
            "Aghb": cls.CAUCASIAN_ALBANIAN,
            "Cakm": cls.CHAKMA,
            "Cham": cls.CHAM,
            "Cher": cls.CHEROKEE,
            "Chrs": cls.CHORASMIAN,
            "Zyyy": cls.COMMON,
            "Copt": cls.COPTIC,
            "Xsux": cls.CUNEIFORM,
            "Cprt": cls.CYPRIOT,
            "Cpmn": cls.CYPRO_MINOAN,
            "Cyrl": cls.CYRILLIC,
            "Dsrt": cls.DESERET,
            "Deva": cls.DEVANAGARI,
            "Diak": cls.DIVES_AKURU,
            "Dogr": cls.DOGRA,
            "Dupl": cls.DUPLOYAN,
            "Egyp": cls.EGYPTIAN_HIEROGLYPHS,
            "Elba": cls.ELBASAN,
            "Elym": cls.ELYMAIC,
            "Ethi": cls.ETHIOPIC,
            "Geok": cls.KHUTSURI,
            "Geor": cls.GEORGIAN,
            "Glag": cls.GLAGOLITIC,
            "Goth": cls.GOTHIC,
            "Gran": cls.GRANTHA,
            "Grek": cls.GREEK,
            "Gujr": cls.GUJARATI,
            "Gong": cls.GUNJALA_GONDI,
            "Guru": cls.GURMUKHI,
            "Hani": cls.HAN,
            "Hang": cls.HANGUL,
            "Rohg": cls.HANIFI_ROHINGYA,
            "Hano": cls.HANUNOO,
            "Hatr": cls.HATRAN,
            "Hebr": cls.HEBREW,
            "Hira": cls.HIRAGANA,
            "Armi": cls.IMPERIAL_ARAMAIC,
            "Zinh": cls.INHERITED,
            "Phli": cls.INSCRIPTIONAL_PAHLAVI,
            "Prti": cls.INSCRIPTIONAL_PARTHIAN,
            "Java": cls.JAVANESE,
            "Kthi": cls.KAITHI,
            "Knda": cls.KANNADA,
            "Kana": cls.KATAKANA,
            "Hrkt": cls.KATAKANA_OR_HIRAGANA,
            "Kawi": cls.KAWI,
            "Kali": cls.KAYAH_LI,
            "Khar": cls.KHAROSHTHI,
            "Kits": cls.KHITAN_SMALL_SCRIPT,
            "Khmr": cls.KHMER,
            "Khoj": cls.KHOJKI,
            "Sind": cls.KHUDAWADI,
            "Laoo": cls.LAO,
            "Latn": cls.LATIN,
            "Lepc": cls.LEPCHA,
            "Limb": cls.LIMBU,
            "Lina": cls.LINEAR_A,
            "Linb": cls.LINEAR_B,
            "Lisu": cls.LISU,
            "Lyci": cls.LYCIAN,
            "Lydi": cls.LYDIAN,
            "Mahj": cls.MAHAJANI,
            "Maka": cls.MAKASAR,
            "Mlym": cls.MALAYALAM,
            "Mand": cls.MANDAIC,
            "Mani": cls.MANICHAEAN,
            "Marc": cls.MARCHEN,
            "Gonm": cls.MASARAM_GONDI,
            "Medf": cls.MEDEFAIDRIN,
            "Mtei": cls.MEETEI_MAYEK,
            "Mend": cls.MENDE_KIKAKUI,
            "Merc": cls.MEROITIC_CURSIVE,
            "Mero": cls.MEROITIC_HIEROGLYPHS,
            "Plrd": cls.MIAO,
            "Modi": cls.MODI,
            "Mong": cls.MONGOLIAN,
            "Mroo": cls.MRO,
            "Mult": cls.MULTANI,
            "Mymr": cls.MYANMAR,
            "Nbat": cls.NABATAEAN,
            "Nagm": cls.NAG_MUNDARI,
            "Nand": cls.NANDINAGARI,
            "Talu": cls.NEW_TAI_LUE,
            "Newa": cls.NEWA,
            "Nkoo": cls.N_KO,
            "Nshu": cls.NUSHU,
            "Hmnp": cls.NYIAKENG_PUACHUE_HMONG,
            "Ogam": cls.OGHAM,
            "Olck": cls.OL_CHIKI,
            "Hung": cls.OLD_HUNGARIAN,
            "Ital": cls.OLD_ITALIC,
            "Narb": cls.OLD_NORTH_ARABIAN,
            "Perm": cls.OLD_PERMIC,
            "Xpeo": cls.OLD_PERSIAN,
            "Sogo": cls.OLD_SOGDIAN,
            "Sarb": cls.OLD_SOUTH_ARABIAN,
            "Orkh": cls.OLD_TURKIC,
            "Ougr": cls.OLD_UYGHUR,
            "Orya": cls.ORIYA,
            "Osge": cls.OSAGE,
            "Osma": cls.OSMANYA,
            "Hmng": cls.PAHAWH_HMONG,
            "Palm": cls.PALMYRENE,
            "Pauc": cls.PAU_CIN_HAU,
            "Phag": cls.PHAGS_PA,
            "Phnx": cls.PHOENICIAN,
            "Phlp": cls.PSALTER_PAHLAVI,
            "Rjng": cls.REJANG,
            "Runr": cls.RUNIC,
            "Samr": cls.SAMARITAN,
            "Saur": cls.SAURASHTRA,
            "Shrd": cls.SHARADA,
            "Shaw": cls.SHAVIAN,
            "Sidd": cls.SIDDHAM,
            "Sgnw": cls.SIGN_WRITING,
            "Sinh": cls.SINHALA,
            "Sogd": cls.SOGDIAN,
            "Sora": cls.SORA_SOMPENG,
            "Soyo": cls.SOYOMBO,
            "Sund": cls.SUNDANESE,
            "Sylo": cls.SYLOTI_NAGRI,
            "Syrc": cls.SYRIAC,
            "Tglg": cls.TAGALOG,
            "Tagb": cls.TAGBANWA,
            "Tale": cls.TAI_LE,
            "Lana": cls.TAI_THAM,
            "Tavt": cls.TAI_VIET,
            "Takr": cls.TAKRI,
            "Taml": cls.TAMIL,
            "Tnsa": cls.TANGSA,
            "Tang": cls.TANGUT,
            "Telu": cls.TELUGU,
            "Thaa": cls.THAANA,
            "Thai": cls.THAI,
            "Tibt": cls.TIBETAN,
            "Tfng": cls.TIFINAGH,
            "Tirh": cls.TIRHUTA,
            "Toto": cls.TOTO,
            "Ugar": cls.UGARITIC,
            "Zzzz": cls.UNKNOWN,
            "Vaii": cls.VAI,
            "Vith": cls.VITHKUQI,
            "Wcho": cls.WANCHO,
            "Wara": cls.WARANG_CITI,
            "Yezi": cls.YEZIDI,
            "Yiii": cls.YI,
            "Zanb": cls.ZANABAZAR_SQUARE,
        }
        return code_map.get(code, cls.UNKNOWN)

    @classmethod
    def match_loosely(cls, name: str) -> ScriptCode:
        script_code_map = {e.normalized: e for e in cls}
        return script_code_map.get(normalize_string_lm3(name), cls.NONE)

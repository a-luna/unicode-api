from collections import namedtuple

MAX_CODEPOINT = 1114111

CJK_UNIFIED_BLOCK_IDS = [119, 121, 316, 317, 318, 319, 320, 322, 323]
CJK_COMPATIBILITY_BLOCK_IDS = [154, 321]
TANGUT_BLOCK_IDS = [266, 269]
SURROGATE_BLOCK_IDS = [150, 151, 152]
PRIVATE_USE_BLOCK_IDS = [153, 326, 327]

ALL_CJK_IDEOGRAPH_BLOCK_IDS = CJK_UNIFIED_BLOCK_IDS + CJK_COMPATIBILITY_BLOCK_IDS
GENERIC_NAME_BLOCK_IDS = ALL_CJK_IDEOGRAPH_BLOCK_IDS + TANGUT_BLOCK_IDS + SURROGATE_BLOCK_IDS + PRIVATE_USE_BLOCK_IDS

CharacterFlag = namedtuple("CharacterFlag", ["name", "alias", "db_column"])

CHAR_FLAG_MAP: dict[int, CharacterFlag] = {
    2**0: CharacterFlag("MIRRORED", "mirrored", "bidirectional_is_mirrored"),
    2**1: CharacterFlag("BIDIRECTIONAL_CONTROL", "bidi_ctrl", "bidirectional_control"),
    2**2: CharacterFlag("JOINING_CONTROL", "join_ctrl", "joining_control"),
    2**3: CharacterFlag("UPPERCASE", "upper", "uppercase"),
    2**4: CharacterFlag("LOWERCASE", "lower", "lowercase"),
    2**5: CharacterFlag("DASH", "dash", "dash"),
    2**6: CharacterFlag("HYPHEN", "hyphen", "hyphen"),
    2**7: CharacterFlag("QUOTATION_MARK", "quote", "quotation_mark"),
    2**8: CharacterFlag("TERMINAL_PUNCTUATION", "term_p", "terminal_punctuation"),
    2**9: CharacterFlag("SENTENCE_TERMINAL", "s_term", "sentence_terminal"),
    2**10: CharacterFlag("DIACRITIC", "diacritic", "diacritic"),
    2**11: CharacterFlag("EXTENDER", "extender", "extender"),
    2**12: CharacterFlag("SOFT_DOTTED", "s_dot", "soft_dotted"),
    2**13: CharacterFlag("ALPHABETIC", "alpha", "alphabetic"),
    2**14: CharacterFlag("MATHEMATICAL", "math", "math"),
    2**15: CharacterFlag("HEX_DIGIT", "hex", "hex_digit"),
    2**16: CharacterFlag("ASCII_HEX_DIGIT", "ascii_hex", "ascii_hex_digit"),
    2**17: CharacterFlag("DEFAULT_IGNORABLE_CODE_POINT", "def_ignore", "default_ignorable_code_point"),
    2**18: CharacterFlag("LOGICAL_ORDER_EXCEPTION", "logical_ord_ex", "logical_order_exception"),
    2**19: CharacterFlag("PREPENDED_CONCATENATION_MARK", "pre_concat", "prepended_concatenation_mark"),
    2**20: CharacterFlag("WHITE_SPACE", "white_space", "white_space"),
    2**21: CharacterFlag("REGIONAL_INDICATOR", "reg_ind", "regional_indicator"),
    2**22: CharacterFlag("EMOJI", "emoji", "emoji"),
    2**23: CharacterFlag("EMOJI_PRESENTATION", "emoji_p", "emoji_presentation"),
    2**24: CharacterFlag("EMOJI_MODIFIER", "emoji_m", "emoji_modifier"),
    2**25: CharacterFlag("EMOJI_MODIFIER_BASE", "emoji_m_base", "emoji_modifier_base"),
    2**26: CharacterFlag("EMOJI_COMPONENT", "emoji_c", "emoji_component"),
    2**27: CharacterFlag("EXTENDED_PICTOGRAPHIC", "ext_pict", "extended_pictographic"),
    2**28: CharacterFlag("IDEOGRAPHIC", "ideo", "ideographic"),
    2**29: CharacterFlag("UNIFIED_IDEOGRAPH", "uideo", "unified_ideograph"),
    2**30: CharacterFlag("RADICAL", "radical", "radical"),
}

NULL_BLOCK = {
    "id": 0,
    "name": "None",
    "plane_number": -1,
    "start": "",
    "start_dec": 0,
    "finish": "",
    "finish_dec": 0,
    "total_allocated": 0,
    "total_defined": 0,
}

NULL_PLANE = {
    "number": -1,
    "name": "None",
    "abbreviation": "None",
    "start": "",
    "start_dec": 0,
    "finish": "",
    "finish_dec": 0,
    "start_block_id": 0,
    "finish_block_id": 0,
    "total_allocated": 0,
    "total_defined": 0,
}

NON_CHARACTER_CODEPOINTS = [
    64976,
    64977,
    64978,
    64979,
    64980,
    64981,
    64982,
    64983,
    64984,
    64985,
    64986,
    64987,
    64988,
    64989,
    64990,
    64991,
    64992,
    64993,
    64994,
    64995,
    64996,
    64997,
    64998,
    64999,
    65000,
    65001,
    65002,
    65003,
    65004,
    65005,
    65006,
    65007,
    65534,
    65535,
    131070,
    131071,
    196606,
    196607,
    262142,
    262143,
    327678,
    327679,
    393214,
    393215,
    458750,
    458751,
    524286,
    524287,
    589822,
    589823,
    655358,
    655359,
    720894,
    720895,
    786430,
    786431,
    851966,
    851967,
    917502,
    917503,
    983038,
    983039,
    1048574,
    1048575,
    1114110,
    1114111,
]

C0_CONTROL_CHARACTERS = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
]

C1_CONTROL_CHARACTERS = [
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    148,
    149,
    150,
    151,
    152,
    153,
    154,
    155,
    156,
    157,
    158,
    159,
]

ALL_CONTROL_CHARACTERS = C0_CONTROL_CHARACTERS + C1_CONTROL_CHARACTERS

DEFAULT_BC_R_CODEPOINTS = [
    1424,
    1480,
    1481,
    1482,
    1483,
    1484,
    1485,
    1486,
    1487,
    1515,
    1516,
    1517,
    1518,
    1525,
    1526,
    1527,
    1528,
    1529,
    1530,
    1531,
    1532,
    1533,
    1534,
    1535,
    2043,
    2044,
    2094,
    2095,
    2111,
    2140,
    2141,
    2143,
    64311,
    64317,
    64319,
    64322,
    64325,
    67590,
    67591,
    67593,
    67638,
    67641,
    67642,
    67643,
    67645,
    67646,
    67670,
    67743,
    67744,
    67745,
    67746,
    67747,
    67748,
    67749,
    67750,
    67760,
    67761,
    67762,
    67763,
    67764,
    67765,
    67766,
    67767,
    67768,
    67769,
    67770,
    67771,
    67772,
    67773,
    67774,
    67775,
    67776,
    67777,
    67778,
    67779,
    67780,
    67781,
    67782,
    67783,
    67784,
    67785,
    67786,
    67787,
    67788,
    67789,
    67790,
    67791,
    67792,
    67793,
    67794,
    67795,
    67796,
    67797,
    67798,
    67799,
    67800,
    67801,
    67802,
    67803,
    67804,
    67805,
    67806,
    67807,
    67827,
    67830,
    67831,
    67832,
    67833,
    67834,
    67868,
    67869,
    67870,
    67898,
    67899,
    67900,
    67901,
    67902,
    67904,
    67905,
    67906,
    67907,
    67908,
    67909,
    67910,
    67911,
    67912,
    67913,
    67914,
    67915,
    67916,
    67917,
    67918,
    67919,
    67920,
    67921,
    67922,
    67923,
    67924,
    67925,
    67926,
    67927,
    67928,
    67929,
    67930,
    67931,
    67932,
    67933,
    67934,
    67935,
    67936,
    67937,
    67938,
    67939,
    67940,
    67941,
    67942,
    67943,
    67944,
    67945,
    67946,
    67947,
    67948,
    67949,
    67950,
    67951,
    67952,
    67953,
    67954,
    67955,
    67956,
    67957,
    67958,
    67959,
    67960,
    67961,
    67962,
    67963,
    67964,
    67965,
    67966,
    67967,
    68024,
    68025,
    68026,
    68027,
    68048,
    68049,
    68100,
    68103,
    68104,
    68105,
    68106,
    68107,
    68116,
    68120,
    68150,
    68151,
    68155,
    68156,
    68157,
    68158,
    68169,
    68170,
    68171,
    68172,
    68173,
    68174,
    68175,
    68185,
    68186,
    68187,
    68188,
    68189,
    68190,
    68191,
    68256,
    68257,
    68258,
    68259,
    68260,
    68261,
    68262,
    68263,
    68264,
    68265,
    68266,
    68267,
    68268,
    68269,
    68270,
    68271,
    68272,
    68273,
    68274,
    68275,
    68276,
    68277,
    68278,
    68279,
    68280,
    68281,
    68282,
    68283,
    68284,
    68285,
    68286,
    68287,
    68327,
    68328,
    68329,
    68330,
    68343,
    68344,
    68345,
    68346,
    68347,
    68348,
    68349,
    68350,
    68351,
    68406,
    68407,
    68408,
    68438,
    68439,
    68467,
    68468,
    68469,
    68470,
    68471,
    68498,
    68499,
    68500,
    68501,
    68502,
    68503,
    68504,
    68509,
    68510,
    68511,
    68512,
    68513,
    68514,
    68515,
    68516,
    68517,
    68518,
    68519,
    68520,
    68528,
    68529,
    68530,
    68531,
    68532,
    68533,
    68534,
    68535,
    68536,
    68537,
    68538,
    68539,
    68540,
    68541,
    68542,
    68543,
    68544,
    68545,
    68546,
    68547,
    68548,
    68549,
    68550,
    68551,
    68552,
    68553,
    68554,
    68555,
    68556,
    68557,
    68558,
    68559,
    68560,
    68561,
    68562,
    68563,
    68564,
    68565,
    68566,
    68567,
    68568,
    68569,
    68570,
    68571,
    68572,
    68573,
    68574,
    68575,
    68576,
    68577,
    68578,
    68579,
    68580,
    68581,
    68582,
    68583,
    68584,
    68585,
    68586,
    68587,
    68588,
    68589,
    68590,
    68591,
    68592,
    68593,
    68594,
    68595,
    68596,
    68597,
    68598,
    68599,
    68600,
    68601,
    68602,
    68603,
    68604,
    68605,
    68606,
    68607,
    68681,
    68682,
    68683,
    68684,
    68685,
    68686,
    68687,
    68688,
    68689,
    68690,
    68691,
    68692,
    68693,
    68694,
    68695,
    68696,
    68697,
    68698,
    68699,
    68700,
    68701,
    68702,
    68703,
    68704,
    68705,
    68706,
    68707,
    68708,
    68709,
    68710,
    68711,
    68712,
    68713,
    68714,
    68715,
    68716,
    68717,
    68718,
    68719,
    68720,
    68721,
    68722,
    68723,
    68724,
    68725,
    68726,
    68727,
    68728,
    68729,
    68730,
    68731,
    68732,
    68733,
    68734,
    68735,
    68787,
    68788,
    68789,
    68790,
    68791,
    68792,
    68793,
    68794,
    68795,
    68796,
    68797,
    68798,
    68799,
    68851,
    68852,
    68853,
    68854,
    68855,
    68856,
    68857,
    68928,
    68929,
    68930,
    68931,
    68932,
    68933,
    68934,
    68935,
    68936,
    68937,
    68938,
    68939,
    68940,
    68941,
    68942,
    68943,
    68944,
    68945,
    68946,
    68947,
    68948,
    68949,
    68950,
    68951,
    68952,
    68953,
    68954,
    68955,
    68956,
    68957,
    68958,
    68959,
    68960,
    68961,
    68962,
    68963,
    68964,
    68965,
    68966,
    68967,
    68968,
    68969,
    68970,
    68971,
    68972,
    68973,
    68974,
    68975,
    68976,
    68977,
    68978,
    68979,
    68980,
    68981,
    68982,
    68983,
    68984,
    68985,
    68986,
    68987,
    68988,
    68989,
    68990,
    68991,
    68992,
    68993,
    68994,
    68995,
    68996,
    68997,
    68998,
    68999,
    69000,
    69001,
    69002,
    69003,
    69004,
    69005,
    69006,
    69007,
    69008,
    69009,
    69010,
    69011,
    69012,
    69013,
    69014,
    69015,
    69016,
    69017,
    69018,
    69019,
    69020,
    69021,
    69022,
    69023,
    69024,
    69025,
    69026,
    69027,
    69028,
    69029,
    69030,
    69031,
    69032,
    69033,
    69034,
    69035,
    69036,
    69037,
    69038,
    69039,
    69040,
    69041,
    69042,
    69043,
    69044,
    69045,
    69046,
    69047,
    69048,
    69049,
    69050,
    69051,
    69052,
    69053,
    69054,
    69055,
    69056,
    69057,
    69058,
    69059,
    69060,
    69061,
    69062,
    69063,
    69064,
    69065,
    69066,
    69067,
    69068,
    69069,
    69070,
    69071,
    69072,
    69073,
    69074,
    69075,
    69076,
    69077,
    69078,
    69079,
    69080,
    69081,
    69082,
    69083,
    69084,
    69085,
    69086,
    69087,
    69088,
    69089,
    69090,
    69091,
    69092,
    69093,
    69094,
    69095,
    69096,
    69097,
    69098,
    69099,
    69100,
    69101,
    69102,
    69103,
    69104,
    69105,
    69106,
    69107,
    69108,
    69109,
    69110,
    69111,
    69112,
    69113,
    69114,
    69115,
    69116,
    69117,
    69118,
    69119,
    69120,
    69121,
    69122,
    69123,
    69124,
    69125,
    69126,
    69127,
    69128,
    69129,
    69130,
    69131,
    69132,
    69133,
    69134,
    69135,
    69136,
    69137,
    69138,
    69139,
    69140,
    69141,
    69142,
    69143,
    69144,
    69145,
    69146,
    69147,
    69148,
    69149,
    69150,
    69151,
    69152,
    69153,
    69154,
    69155,
    69156,
    69157,
    69158,
    69159,
    69160,
    69161,
    69162,
    69163,
    69164,
    69165,
    69166,
    69167,
    69168,
    69169,
    69170,
    69171,
    69172,
    69173,
    69174,
    69175,
    69176,
    69177,
    69178,
    69179,
    69180,
    69181,
    69182,
    69183,
    69184,
    69185,
    69186,
    69187,
    69188,
    69189,
    69190,
    69191,
    69192,
    69193,
    69194,
    69195,
    69196,
    69197,
    69198,
    69199,
    69200,
    69201,
    69202,
    69203,
    69204,
    69205,
    69206,
    69207,
    69208,
    69209,
    69210,
    69211,
    69212,
    69213,
    69214,
    69215,
    69247,
    69290,
    69294,
    69295,
    69298,
    69299,
    69300,
    69301,
    69302,
    69303,
    69304,
    69305,
    69306,
    69307,
    69308,
    69309,
    69310,
    69311,
    69416,
    69417,
    69418,
    69419,
    69420,
    69421,
    69422,
    69423,
    69514,
    69515,
    69516,
    69517,
    69518,
    69519,
    69520,
    69521,
    69522,
    69523,
    69524,
    69525,
    69526,
    69527,
    69528,
    69529,
    69530,
    69531,
    69532,
    69533,
    69534,
    69535,
    69536,
    69537,
    69538,
    69539,
    69540,
    69541,
    69542,
    69543,
    69544,
    69545,
    69546,
    69547,
    69548,
    69549,
    69550,
    69551,
    69580,
    69581,
    69582,
    69583,
    69584,
    69585,
    69586,
    69587,
    69588,
    69589,
    69590,
    69591,
    69592,
    69593,
    69594,
    69595,
    69596,
    69597,
    69598,
    69599,
    69623,
    69624,
    69625,
    69626,
    69627,
    69628,
    69629,
    69630,
    69631,
    125125,
    125126,
    125143,
    125144,
    125145,
    125146,
    125147,
    125148,
    125149,
    125150,
    125151,
    125152,
    125153,
    125154,
    125155,
    125156,
    125157,
    125158,
    125159,
    125160,
    125161,
    125162,
    125163,
    125164,
    125165,
    125166,
    125167,
    125168,
    125169,
    125170,
    125171,
    125172,
    125173,
    125174,
    125175,
    125176,
    125177,
    125178,
    125179,
    125180,
    125181,
    125182,
    125183,
    125260,
    125261,
    125262,
    125263,
    125274,
    125275,
    125276,
    125277,
    125280,
    125281,
    125282,
    125283,
    125284,
    125285,
    125286,
    125287,
    125288,
    125289,
    125290,
    125291,
    125292,
    125293,
    125294,
    125295,
    125296,
    125297,
    125298,
    125299,
    125300,
    125301,
    125302,
    125303,
    125304,
    125305,
    125306,
    125307,
    125308,
    125309,
    125310,
    125311,
    125312,
    125313,
    125314,
    125315,
    125316,
    125317,
    125318,
    125319,
    125320,
    125321,
    125322,
    125323,
    125324,
    125325,
    125326,
    125327,
    125328,
    125329,
    125330,
    125331,
    125332,
    125333,
    125334,
    125335,
    125336,
    125337,
    125338,
    125339,
    125340,
    125341,
    125342,
    125343,
    125344,
    125345,
    125346,
    125347,
    125348,
    125349,
    125350,
    125351,
    125352,
    125353,
    125354,
    125355,
    125356,
    125357,
    125358,
    125359,
    125360,
    125361,
    125362,
    125363,
    125364,
    125365,
    125366,
    125367,
    125368,
    125369,
    125370,
    125371,
    125372,
    125373,
    125374,
    125375,
    125376,
    125377,
    125378,
    125379,
    125380,
    125381,
    125382,
    125383,
    125384,
    125385,
    125386,
    125387,
    125388,
    125389,
    125390,
    125391,
    125392,
    125393,
    125394,
    125395,
    125396,
    125397,
    125398,
    125399,
    125400,
    125401,
    125402,
    125403,
    125404,
    125405,
    125406,
    125407,
    125408,
    125409,
    125410,
    125411,
    125412,
    125413,
    125414,
    125415,
    125416,
    125417,
    125418,
    125419,
    125420,
    125421,
    125422,
    125423,
    125424,
    125425,
    125426,
    125427,
    125428,
    125429,
    125430,
    125431,
    125432,
    125433,
    125434,
    125435,
    125436,
    125437,
    125438,
    125439,
    125440,
    125441,
    125442,
    125443,
    125444,
    125445,
    125446,
    125447,
    125448,
    125449,
    125450,
    125451,
    125452,
    125453,
    125454,
    125455,
    125456,
    125457,
    125458,
    125459,
    125460,
    125461,
    125462,
    125463,
    125464,
    125465,
    125466,
    125467,
    125468,
    125469,
    125470,
    125471,
    125472,
    125473,
    125474,
    125475,
    125476,
    125477,
    125478,
    125479,
    125480,
    125481,
    125482,
    125483,
    125484,
    125485,
    125486,
    125487,
    125488,
    125489,
    125490,
    125491,
    125492,
    125493,
    125494,
    125495,
    125496,
    125497,
    125498,
    125499,
    125500,
    125501,
    125502,
    125503,
    125504,
    125505,
    125506,
    125507,
    125508,
    125509,
    125510,
    125511,
    125512,
    125513,
    125514,
    125515,
    125516,
    125517,
    125518,
    125519,
    125520,
    125521,
    125522,
    125523,
    125524,
    125525,
    125526,
    125527,
    125528,
    125529,
    125530,
    125531,
    125532,
    125533,
    125534,
    125535,
    125536,
    125537,
    125538,
    125539,
    125540,
    125541,
    125542,
    125543,
    125544,
    125545,
    125546,
    125547,
    125548,
    125549,
    125550,
    125551,
    125552,
    125553,
    125554,
    125555,
    125556,
    125557,
    125558,
    125559,
    125560,
    125561,
    125562,
    125563,
    125564,
    125565,
    125566,
    125567,
    125568,
    125569,
    125570,
    125571,
    125572,
    125573,
    125574,
    125575,
    125576,
    125577,
    125578,
    125579,
    125580,
    125581,
    125582,
    125583,
    125584,
    125585,
    125586,
    125587,
    125588,
    125589,
    125590,
    125591,
    125592,
    125593,
    125594,
    125595,
    125596,
    125597,
    125598,
    125599,
    125600,
    125601,
    125602,
    125603,
    125604,
    125605,
    125606,
    125607,
    125608,
    125609,
    125610,
    125611,
    125612,
    125613,
    125614,
    125615,
    125616,
    125617,
    125618,
    125619,
    125620,
    125621,
    125622,
    125623,
    125624,
    125625,
    125626,
    125627,
    125628,
    125629,
    125630,
    125631,
    125632,
    125633,
    125634,
    125635,
    125636,
    125637,
    125638,
    125639,
    125640,
    125641,
    125642,
    125643,
    125644,
    125645,
    125646,
    125647,
    125648,
    125649,
    125650,
    125651,
    125652,
    125653,
    125654,
    125655,
    125656,
    125657,
    125658,
    125659,
    125660,
    125661,
    125662,
    125663,
    125664,
    125665,
    125666,
    125667,
    125668,
    125669,
    125670,
    125671,
    125672,
    125673,
    125674,
    125675,
    125676,
    125677,
    125678,
    125679,
    125680,
    125681,
    125682,
    125683,
    125684,
    125685,
    125686,
    125687,
    125688,
    125689,
    125690,
    125691,
    125692,
    125693,
    125694,
    125695,
    125696,
    125697,
    125698,
    125699,
    125700,
    125701,
    125702,
    125703,
    125704,
    125705,
    125706,
    125707,
    125708,
    125709,
    125710,
    125711,
    125712,
    125713,
    125714,
    125715,
    125716,
    125717,
    125718,
    125719,
    125720,
    125721,
    125722,
    125723,
    125724,
    125725,
    125726,
    125727,
    125728,
    125729,
    125730,
    125731,
    125732,
    125733,
    125734,
    125735,
    125736,
    125737,
    125738,
    125739,
    125740,
    125741,
    125742,
    125743,
    125744,
    125745,
    125746,
    125747,
    125748,
    125749,
    125750,
    125751,
    125752,
    125753,
    125754,
    125755,
    125756,
    125757,
    125758,
    125759,
    125760,
    125761,
    125762,
    125763,
    125764,
    125765,
    125766,
    125767,
    125768,
    125769,
    125770,
    125771,
    125772,
    125773,
    125774,
    125775,
    125776,
    125777,
    125778,
    125779,
    125780,
    125781,
    125782,
    125783,
    125784,
    125785,
    125786,
    125787,
    125788,
    125789,
    125790,
    125791,
    125792,
    125793,
    125794,
    125795,
    125796,
    125797,
    125798,
    125799,
    125800,
    125801,
    125802,
    125803,
    125804,
    125805,
    125806,
    125807,
    125808,
    125809,
    125810,
    125811,
    125812,
    125813,
    125814,
    125815,
    125816,
    125817,
    125818,
    125819,
    125820,
    125821,
    125822,
    125823,
    125824,
    125825,
    125826,
    125827,
    125828,
    125829,
    125830,
    125831,
    125832,
    125833,
    125834,
    125835,
    125836,
    125837,
    125838,
    125839,
    125840,
    125841,
    125842,
    125843,
    125844,
    125845,
    125846,
    125847,
    125848,
    125849,
    125850,
    125851,
    125852,
    125853,
    125854,
    125855,
    125856,
    125857,
    125858,
    125859,
    125860,
    125861,
    125862,
    125863,
    125864,
    125865,
    125866,
    125867,
    125868,
    125869,
    125870,
    125871,
    125872,
    125873,
    125874,
    125875,
    125876,
    125877,
    125878,
    125879,
    125880,
    125881,
    125882,
    125883,
    125884,
    125885,
    125886,
    125887,
    125888,
    125889,
    125890,
    125891,
    125892,
    125893,
    125894,
    125895,
    125896,
    125897,
    125898,
    125899,
    125900,
    125901,
    125902,
    125903,
    125904,
    125905,
    125906,
    125907,
    125908,
    125909,
    125910,
    125911,
    125912,
    125913,
    125914,
    125915,
    125916,
    125917,
    125918,
    125919,
    125920,
    125921,
    125922,
    125923,
    125924,
    125925,
    125926,
    125927,
    125928,
    125929,
    125930,
    125931,
    125932,
    125933,
    125934,
    125935,
    125936,
    125937,
    125938,
    125939,
    125940,
    125941,
    125942,
    125943,
    125944,
    125945,
    125946,
    125947,
    125948,
    125949,
    125950,
    125951,
    125952,
    125953,
    125954,
    125955,
    125956,
    125957,
    125958,
    125959,
    125960,
    125961,
    125962,
    125963,
    125964,
    125965,
    125966,
    125967,
    125968,
    125969,
    125970,
    125971,
    125972,
    125973,
    125974,
    125975,
    125976,
    125977,
    125978,
    125979,
    125980,
    125981,
    125982,
    125983,
    125984,
    125985,
    125986,
    125987,
    125988,
    125989,
    125990,
    125991,
    125992,
    125993,
    125994,
    125995,
    125996,
    125997,
    125998,
    125999,
    126000,
    126001,
    126002,
    126003,
    126004,
    126005,
    126006,
    126007,
    126008,
    126009,
    126010,
    126011,
    126012,
    126013,
    126014,
    126015,
    126016,
    126017,
    126018,
    126019,
    126020,
    126021,
    126022,
    126023,
    126024,
    126025,
    126026,
    126027,
    126028,
    126029,
    126030,
    126031,
    126032,
    126033,
    126034,
    126035,
    126036,
    126037,
    126038,
    126039,
    126040,
    126041,
    126042,
    126043,
    126044,
    126045,
    126046,
    126047,
    126048,
    126049,
    126050,
    126051,
    126052,
    126053,
    126054,
    126055,
    126056,
    126057,
    126058,
    126059,
    126060,
    126061,
    126062,
    126063,
    126144,
    126145,
    126146,
    126147,
    126148,
    126149,
    126150,
    126151,
    126152,
    126153,
    126154,
    126155,
    126156,
    126157,
    126158,
    126159,
    126160,
    126161,
    126162,
    126163,
    126164,
    126165,
    126166,
    126167,
    126168,
    126169,
    126170,
    126171,
    126172,
    126173,
    126174,
    126175,
    126176,
    126177,
    126178,
    126179,
    126180,
    126181,
    126182,
    126183,
    126184,
    126185,
    126186,
    126187,
    126188,
    126189,
    126190,
    126191,
    126192,
    126193,
    126194,
    126195,
    126196,
    126197,
    126198,
    126199,
    126200,
    126201,
    126202,
    126203,
    126204,
    126205,
    126206,
    126207,
    126288,
    126289,
    126290,
    126291,
    126292,
    126293,
    126294,
    126295,
    126296,
    126297,
    126298,
    126299,
    126300,
    126301,
    126302,
    126303,
    126304,
    126305,
    126306,
    126307,
    126308,
    126309,
    126310,
    126311,
    126312,
    126313,
    126314,
    126315,
    126316,
    126317,
    126318,
    126319,
    126320,
    126321,
    126322,
    126323,
    126324,
    126325,
    126326,
    126327,
    126328,
    126329,
    126330,
    126331,
    126332,
    126333,
    126334,
    126335,
    126336,
    126337,
    126338,
    126339,
    126340,
    126341,
    126342,
    126343,
    126344,
    126345,
    126346,
    126347,
    126348,
    126349,
    126350,
    126351,
    126352,
    126353,
    126354,
    126355,
    126356,
    126357,
    126358,
    126359,
    126360,
    126361,
    126362,
    126363,
    126364,
    126365,
    126366,
    126367,
    126368,
    126369,
    126370,
    126371,
    126372,
    126373,
    126374,
    126375,
    126376,
    126377,
    126378,
    126379,
    126380,
    126381,
    126382,
    126383,
    126384,
    126385,
    126386,
    126387,
    126388,
    126389,
    126390,
    126391,
    126392,
    126393,
    126394,
    126395,
    126396,
    126397,
    126398,
    126399,
    126400,
    126401,
    126402,
    126403,
    126404,
    126405,
    126406,
    126407,
    126408,
    126409,
    126410,
    126411,
    126412,
    126413,
    126414,
    126415,
    126416,
    126417,
    126418,
    126419,
    126420,
    126421,
    126422,
    126423,
    126424,
    126425,
    126426,
    126427,
    126428,
    126429,
    126430,
    126431,
    126432,
    126433,
    126434,
    126435,
    126436,
    126437,
    126438,
    126439,
    126440,
    126441,
    126442,
    126443,
    126444,
    126445,
    126446,
    126447,
    126448,
    126449,
    126450,
    126451,
    126452,
    126453,
    126454,
    126455,
    126456,
    126457,
    126458,
    126459,
    126460,
    126461,
    126462,
    126463,
    126720,
    126721,
    126722,
    126723,
    126724,
    126725,
    126726,
    126727,
    126728,
    126729,
    126730,
    126731,
    126732,
    126733,
    126734,
    126735,
    126736,
    126737,
    126738,
    126739,
    126740,
    126741,
    126742,
    126743,
    126744,
    126745,
    126746,
    126747,
    126748,
    126749,
    126750,
    126751,
    126752,
    126753,
    126754,
    126755,
    126756,
    126757,
    126758,
    126759,
    126760,
    126761,
    126762,
    126763,
    126764,
    126765,
    126766,
    126767,
    126768,
    126769,
    126770,
    126771,
    126772,
    126773,
    126774,
    126775,
    126776,
    126777,
    126778,
    126779,
    126780,
    126781,
    126782,
    126783,
    126784,
    126785,
    126786,
    126787,
    126788,
    126789,
    126790,
    126791,
    126792,
    126793,
    126794,
    126795,
    126796,
    126797,
    126798,
    126799,
    126800,
    126801,
    126802,
    126803,
    126804,
    126805,
    126806,
    126807,
    126808,
    126809,
    126810,
    126811,
    126812,
    126813,
    126814,
    126815,
    126816,
    126817,
    126818,
    126819,
    126820,
    126821,
    126822,
    126823,
    126824,
    126825,
    126826,
    126827,
    126828,
    126829,
    126830,
    126831,
    126832,
    126833,
    126834,
    126835,
    126836,
    126837,
    126838,
    126839,
    126840,
    126841,
    126842,
    126843,
    126844,
    126845,
    126846,
    126847,
    126848,
    126849,
    126850,
    126851,
    126852,
    126853,
    126854,
    126855,
    126856,
    126857,
    126858,
    126859,
    126860,
    126861,
    126862,
    126863,
    126864,
    126865,
    126866,
    126867,
    126868,
    126869,
    126870,
    126871,
    126872,
    126873,
    126874,
    126875,
    126876,
    126877,
    126878,
    126879,
    126880,
    126881,
    126882,
    126883,
    126884,
    126885,
    126886,
    126887,
    126888,
    126889,
    126890,
    126891,
    126892,
    126893,
    126894,
    126895,
    126896,
    126897,
    126898,
    126899,
    126900,
    126901,
    126902,
    126903,
    126904,
    126905,
    126906,
    126907,
    126908,
    126909,
    126910,
    126911,
    126912,
    126913,
    126914,
    126915,
    126916,
    126917,
    126918,
    126919,
    126920,
    126921,
    126922,
    126923,
    126924,
    126925,
    126926,
    126927,
    126928,
    126929,
    126930,
    126931,
    126932,
    126933,
    126934,
    126935,
    126936,
    126937,
    126938,
    126939,
    126940,
    126941,
    126942,
    126943,
    126944,
    126945,
    126946,
    126947,
    126948,
    126949,
    126950,
    126951,
    126952,
    126953,
    126954,
    126955,
    126956,
    126957,
    126958,
    126959,
    126960,
    126961,
    126962,
    126963,
    126964,
    126965,
    126966,
    126967,
    126968,
    126969,
    126970,
    126971,
    126972,
    126973,
    126974,
    126975,
]

DEFAULT_BC_AL_CODEPOINTS = [
    1806,
    1867,
    1868,
    1970,
    1971,
    1972,
    1973,
    1974,
    1975,
    1976,
    1977,
    1978,
    1979,
    1980,
    1981,
    1982,
    1983,
    2155,
    2156,
    2157,
    2158,
    2159,
    2191,
    2194,
    2195,
    2196,
    2197,
    2198,
    2199,
    64451,
    64452,
    64453,
    64454,
    64455,
    64456,
    64457,
    64458,
    64459,
    64460,
    64461,
    64462,
    64463,
    64464,
    64465,
    64466,
    64912,
    64913,
    64968,
    64969,
    64970,
    64971,
    64972,
    64973,
    64974,
    65141,
    65277,
    65278,
    68904,
    68905,
    68906,
    68907,
    68908,
    68909,
    68910,
    68911,
    68922,
    68923,
    68924,
    68925,
    68926,
    68927,
    69312,
    69313,
    69314,
    69315,
    69316,
    69317,
    69318,
    69319,
    69320,
    69321,
    69322,
    69323,
    69324,
    69325,
    69326,
    69327,
    69328,
    69329,
    69330,
    69331,
    69332,
    69333,
    69334,
    69335,
    69336,
    69337,
    69338,
    69339,
    69340,
    69341,
    69342,
    69343,
    69344,
    69345,
    69346,
    69347,
    69348,
    69349,
    69350,
    69351,
    69352,
    69353,
    69354,
    69355,
    69356,
    69357,
    69358,
    69359,
    69360,
    69361,
    69362,
    69363,
    69364,
    69365,
    69366,
    69367,
    69368,
    69369,
    69370,
    69371,
    69372,
    69466,
    69467,
    69468,
    69469,
    69470,
    69471,
    69472,
    69473,
    69474,
    69475,
    69476,
    69477,
    69478,
    69479,
    69480,
    69481,
    69482,
    69483,
    69484,
    69485,
    69486,
    69487,
    126064,
    126133,
    126134,
    126135,
    126136,
    126137,
    126138,
    126139,
    126140,
    126141,
    126142,
    126143,
    126208,
    126270,
    126271,
    126272,
    126273,
    126274,
    126275,
    126276,
    126277,
    126278,
    126279,
    126280,
    126281,
    126282,
    126283,
    126284,
    126285,
    126286,
    126287,
    126468,
    126496,
    126499,
    126501,
    126502,
    126504,
    126515,
    126520,
    126522,
    126524,
    126525,
    126526,
    126527,
    126528,
    126529,
    126531,
    126532,
    126533,
    126534,
    126536,
    126538,
    126540,
    126544,
    126547,
    126549,
    126550,
    126552,
    126554,
    126556,
    126558,
    126560,
    126563,
    126565,
    126566,
    126571,
    126579,
    126584,
    126589,
    126591,
    126602,
    126620,
    126621,
    126622,
    126623,
    126624,
    126628,
    126634,
    126652,
    126653,
    126654,
    126655,
    126656,
    126657,
    126658,
    126659,
    126660,
    126661,
    126662,
    126663,
    126664,
    126665,
    126666,
    126667,
    126668,
    126669,
    126670,
    126671,
    126672,
    126673,
    126674,
    126675,
    126676,
    126677,
    126678,
    126679,
    126680,
    126681,
    126682,
    126683,
    126684,
    126685,
    126686,
    126687,
    126688,
    126689,
    126690,
    126691,
    126692,
    126693,
    126694,
    126695,
    126696,
    126697,
    126698,
    126699,
    126700,
    126701,
    126702,
    126703,
    126706,
    126707,
    126708,
    126709,
    126710,
    126711,
    126712,
    126713,
    126714,
    126715,
    126716,
    126717,
    126718,
    126719,
]

DEFAULT_BC_ET_CODEPOINTS = [
    8385,
    8386,
    8387,
    8388,
    8389,
    8390,
    8391,
    8392,
    8393,
    8394,
    8395,
    8396,
    8397,
    8398,
    8399,
]

DEFAULT_VO_U_BLOCK_IDS = [
    51,
    78,
    82,
    96,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    137,
    147,
    148,
    149,
    153,
    154,
    158,
    161,
    164,
    229,
    238,
    239,
    255,
    256,
    257,
    265,
    266,
    267,
    268,
    269,
    270,
    272,
    273,
    274,
    277,
    278,
    279,
    282,
    283,
    284,
    286,
    300,
    301,
    302,
    303,
    304,
    308,
    309,
    312,
    313,
    314,
]

DEFAULT_VO_U_PLANE_NUMBERS = [2, 3, 15, 16]

import app.db.models as db

CharDetailsDict = dict[str, bool | int | str]
BlockOrPlaneDetailsDict = dict[str, int | str]
ParsedUnicodeData = BlockOrPlaneDetailsDict | CharDetailsDict
AllParsedUnicodeData = tuple[list[BlockOrPlaneDetailsDict], list[BlockOrPlaneDetailsDict], list[CharDetailsDict]]
UnicodeModel = db.UnicodePlane | db.UnicodeBlock | db.UnicodeCharacter | db.UnicodeCharacterUnihan

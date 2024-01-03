import app.db.models as db

CharDetailsDict = dict[str, bool | int | str]
BlockOrPlaneDetailsDict = dict[str, int | str]
AllParsedUnicodeData = tuple[list[BlockOrPlaneDetailsDict], list[BlockOrPlaneDetailsDict], list[CharDetailsDict]]
UnicodeModel = (
    type[db.UnicodePlane] | type[db.UnicodeBlock] | type[db.UnicodeCharacter] | type[db.UnicodeCharacterUnihan]
)

import app.db.models as db
from app.core.result import Result
from app.data.util import finish_task, start_task, update_progress
from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    DecompositionType,
    EastAsianWidthType,
    GeneralCategory,
    HangulSyllableType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
    TriadicLogic,
    VerticalOrientationType,
)

ONE_PERCENT = 0.01


def save_parsed_data_to_csv(config, all_planes, all_blocks, all_chars):
    all_named_chars = [update_char_dict_enum_values(char) for char in all_chars if not char["_unihan"]]
    all_unihan_chars = [update_char_dict_enum_values(char) for char in all_chars if char["_unihan"]]

    csv_file_map = {
        db.UnicodePlane: (all_planes, config.PLANES_CSV),
        db.UnicodeBlock: (all_blocks, config.BLOCKS_CSV),
        db.UnicodeCharacter: (all_named_chars, config.NAMED_CHARS_CSV),
        db.UnicodeCharacterUnihan: (all_unihan_chars, config.UNIHAN_CHARS_CSV),
    }
    for table, (parsed_data, csv_file) in csv_file_map.items():
        spinner = start_task(f"Saving parsed {table.__tablename__} data to CSV...")
        total_rows = len(parsed_data)
        column_names = get_column_names(table, parsed_data[0])
        append_to_csv(csv_file, text=",".join(column_names))
        chunk_size, chunk_count, row_count, last_reported = 10000, 0, 0, 0
        while True:
            start = chunk_size * chunk_count
            stop = min(start + chunk_size, total_rows)
            chunk = parsed_data[start:stop]
            append_to_csv(csv_file, text=get_csv_rows_for_chunk(chunk, table, column_names))
            row_count += len(chunk)
            chunk_count += 1
            last_reported = report_progress(spinner, table, row_count, total_rows, last_reported)
            if row_count == total_rows:
                break
        finish_task(spinner, True, f"Successfully parsed {table.__tablename__} data to CSV!")
    return Result.Ok()


def update_char_dict_enum_values(char_dict):
    char_dict["general_category"] = GeneralCategory.from_code(char_dict["general_category"]).value
    char_dict["bidirectional_class"] = BidirectionalClass.from_code(char_dict["bidirectional_class"]).value
    char_dict["paired_bracket_type"] = BidirectionalBracketType.from_code(char_dict["paired_bracket_type"]).value
    char_dict["decomposition_type"] = DecompositionType.from_code(char_dict["decomposition_type"]).value
    char_dict["NFC_QC"] = TriadicLogic.from_code(char_dict["NFC_QC"]).value
    char_dict["NFD_QC"] = TriadicLogic.from_code(char_dict["NFD_QC"]).value
    char_dict["NFKC_QC"] = TriadicLogic.from_code(char_dict["NFKC_QC"]).value
    char_dict["NFKD_QC"] = TriadicLogic.from_code(char_dict["NFKD_QC"]).value
    char_dict["numeric_type"] = NumericType.from_code(char_dict["numeric_type"]).value
    char_dict["joining_type"] = JoiningType.from_code(char_dict["joining_type"]).value
    char_dict["line_break"] = LineBreakType.from_code(char_dict["line_break"]).value
    char_dict["east_asian_width"] = EastAsianWidthType.from_code(char_dict["east_asian_width"]).value
    char_dict["script"] = ScriptCode.from_code(char_dict["script"]).value
    char_dict["hangul_syllable_type"] = HangulSyllableType.from_code(char_dict["hangul_syllable_type"]).value
    char_dict["vertical_orientation"] = VerticalOrientationType.from_code(char_dict["vertical_orientation"]).value
    return char_dict


def get_column_names(db_model, parsed):
    return [name for name in db_model.__fields__.keys() if name in parsed]


def get_csv_rows_for_chunk(chunk, db_model, column_names):
    return "\n".join(get_csv_row_for_parsed_data(parsed, column_names) for parsed in chunk)


def get_csv_row_for_parsed_data(db_obj, column_names):
    return ",".join(sanitize_value_for_csv(db_obj.get(name, "")) for name in column_names)


def sanitize_value_for_csv(val):
    if isinstance(val, str):
        val = val.replace(",", ";").replace("Nan", "")
    return (
        "0"
        if (isinstance(val, bool) and not val)
        else "0"
        if (isinstance(val, int) and not val)
        else "0.0"
        if (isinstance(val, float) and not val)
        else "1"
        if (isinstance(val, bool) and val)
        else ""
        if not val
        else str(val)
    )


def append_to_csv(csv_file, text):
    with csv_file.open("a") as csv:
        csv.write(f"{text}\n")


def report_progress(spinner, table, count, total, last_reported):
    percent_complete = count / float(total)
    if percent_complete - last_reported > ONE_PERCENT:
        update_progress(spinner, f"Saving parsed {table.__tablename__} data to CSV...", count, total)
        last_reported = percent_complete
    return last_reported

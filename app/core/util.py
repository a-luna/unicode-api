from collections import OrderedDict, defaultdict


def get_code_point_string(codepoint: int) -> str:
    return f"U+{codepoint:04X}" 


def group_and_sort_list(unsorted, group_attr, sort_attr, sort_groups_desc=False, sort_all_desc=False):
    list_sorted = sorted(unsorted, key=lambda x: getattr(x, sort_attr), reverse=sort_all_desc)
    list_grouped = defaultdict(list)
    for item in list_sorted:
        list_grouped[getattr(item, group_attr)].append(item)
    grouped_sorted = OrderedDict()
    for group in sorted(list_grouped.keys(), reverse=sort_groups_desc):
        grouped_sorted[group] = list_grouped[group]
    return grouped_sorted

import copy


def merge_dicts(d1, d2):
    """

    :param d1: Dict 1.
    :type d1: dict
    :param d2: Dict 2.
    :returns: A new dict that is d1 and d2 deep merged.
    :rtype: dict

    """
    merged = copy.deepcopy(d1)
    deep_update(merged, d2, True, [])
    return merged


def deep_update(
    original,
    new_dict,
    new_keys_allowed=False,
    whitelist=None,
    override_all_if_type_changes=None,
):
    """Updates original dict with values from new_dict recursively.
    If new key is introduced in new_dict, then if new_keys_allowed is not
    True, an error will be thrown. Further, for sub-dicts, if the key is
    in the whitelist, then new subkeys can be introduced.

    :param original: Dictionary with default values.
    :type original: dict
    :param new_dict(dict: dict): Dictionary with values to be updated
    :param new_keys_allowed: Whether new keys are allowed. (Default value = False)
    :type new_keys_allowed: bool
    :param whitelist: List of keys that correspond to dict
    values where new subkeys can be introduced. This is only at the top
    level. (Default value = None)
    :type whitelist: Optional[List[str]]
    :param override_all_if_type_changes: List of top level
    keys with value=dict, for which we always simply override the
    entire value (dict), iff the "type" key in that value dict changes. (Default value = None)
    :type override_all_if_type_changes: Optional[List[str]]
    :param new_dict:

    """
    whitelist = whitelist or []
    override_all_if_type_changes = override_all_if_type_changes or []

    for k, value in new_dict.items():
        if k not in original and not new_keys_allowed:
            raise Exception("Unknown config parameter `{}` ".format(k))

        # Both orginal value and new one are dicts.
        if isinstance(original.get(k), dict) and isinstance(value, dict):
            # Check old type vs old one. If different, override entire value.
            if (
                k in override_all_if_type_changes
                and "type" in value
                and "type" in original[k]
                and value["type"] != original[k]["type"]
            ):
                original[k] = value
            # Whitelisted key -> ok to add new subkeys.
            elif k in whitelist:
                deep_update(original[k], value, True)
            # Non-whitelisted key.
            else:
                deep_update(original[k], value, new_keys_allowed)
        # Original value not a dict OR new value not a dict:
        # Override entire value.
        else:
            original[k] = value
    return original


def get_search_space(description):
    if description["type"] == "choice":
        return description["value"]
    elif description["type"] == "range":
        start, end, step = description["value"]
        return range(start, end, step)
    else:
        raise NotImplementedError("Type must be choice or range")


def get_config(headers, para_list, config):
    config = copy.deepcopy(config)
    for i in range(len(para_list)):
        header = headers[i]
        para = para_list[i]
        tmp_dict = config
        for k in header.split(".")[:-1]:
            if k in tmp_dict:
                tmp_dict = tmp_dict[k]
            else:
                tmp_dict[k] = {}
                tmp_dict = tmp_dict[k]
        tmp_dict[header.split(".")[-1]] = para
    return config

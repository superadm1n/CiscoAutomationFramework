from ipaddress import ip_address


def abbreviate_interface(interface_string, max_chars=2):
    """
    Takes an Interface name ex. GigabitEthernet1/0/4 and abbreviates it ex Gi1/0/4

    :param interface_string: Interface String ex. GigabitEthernet1/0/4
    :type interface_string: str
    :param
    :return: Abbreviated interface string
    :rtype: str
    """
    return interface_string[:max_chars] + ''.join([char for char in interface_string if not char.isalpha()])


def is_ipv4(addr):
    '''
    Checks if the IP address provided is an IPv4 Address.

    :param addr: IP address to check
    :type addr: str
    :return: True/False
    :rtype: bool
    '''
    try:
        _ = ip_address(addr)
        return True
    except:
        return False


def column_print(data, spaces_between_columns=2, separator_char=None):
    """
    Print in nice even columns where each column is only the width it needs to be, not the width of the
    widest column in the list. This will give output in a table format similar to much Windows/Linux
    CLI output.
    Based off of code from https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python

    :param data: List of List/Tuples of equal length, the first list being the header, all the rest being the data.
    :type data: list[Union[list, tuple]]
    :param spaces_between_columns: Number of spaces to be between each column (default 2)
    :type spaces_between_columns: int
    :param separator_char: Character to place in a row between the header and data, default to nothing
    :type separator_char: str
    :return: Nothing. This function executes the print
    """
    # Get the max width of each column
    column_widths = []
    for index, _ in enumerate(data[0]):
        column_widths.append(max(len(str(row[index])) for row in data) + spaces_between_columns)

    # reconstruct list if a separator character is specified to be placed between the header and data
    if separator_char and type(separator_char) is str and len(separator_char) == 1:
        separator_line = [[separator_char * (x - spaces_between_columns) for x in column_widths]]
        first_line = data[:1]
        rest = data[1:]
        data = first_line + separator_line + rest


    # construct a string where each column is its own max width and print the line out when completed.
    for row in data:
        print_string = ''
        for index, word in enumerate(row):
            print_string += str(word).ljust(column_widths[index])
        print(print_string)

def chunker(list, size):
    """
    Splits 1 large list into a list sub lists, where the sub lists can be any specific size
    """
    # looping till length l
    end_list = []
    for i in range(0, len(list), size):
        end_list.append(list[i:i + size])
    return end_list

def matches_search_terms(key, search_terms, case_sensitive, full_match):
    """Checks if the key matches any search term based on given options."""
    if not case_sensitive:
        key = key.lower()
        search_terms_lower = [term.lower() for term in search_terms]
    else:
        search_terms_lower = search_terms

    for term in search_terms_lower:

        if full_match:
            if key == term:  # Exact match
                return True
        else:
            if term in key:  # Partial match
                return True
    return False


def convert_config_tree_to_list(tree, indent=0, indent_step=0):
    """
    Converts a tree representation of the configuration into a list that can be pasted
    into a device

    :param tree: Tree representation of a configuration file
    :type tree: dict
    :param indent: number of spaces to indent root with
    :type indent: int
    :param indent_step: number of indent spaces to increment when going from a root to a branch (default 0, no indent)

    :return: List representation of config tree
    :rtype: list
    """
    data = []
    for key, subtree in tree.items():
        data.append(f'{" " * (indent * indent_step)}{key}')
        if isinstance(subtree, dict) and subtree:
            data.extend(convert_config_tree_to_list(subtree, indent + 1, indent_step))
    return data


def search_and_modify_config_tree(tree, search_terms, case_sensitive=True, full_match=False, min_search_depth=0,
                                  max_search_depth=0, prepend_text='', append_text='',
                                  replace_tuple=('', ''), _depth=0):
    """
    Searches the config tree for a set of search terms, and if specified will run each line that matches
    a search term through a modification algorithm to prepend, append, and find/replace specified text on that line.

    Modification will ONLY occur to lines that CONTAIN a match! if you search for "description example" it will
    also return in the tree the interface name ex. interface GigabitEthernet1/0/1, however that line will NOT
    be eligible for the string modification because it does not contain "description example".

    Additionally using that same interface example, the interface will likely have other config besides the
    description, but if you search for the description, all other commands in that layer of the tree will
    not be returned, just the path up to the root which in this case is the interface name.

    You may also specify if you want your search to be case sensitive, and you may also specify if you want
    a full or partial match. For example if I do a full match for "description" but the line of configuration
    is "description example" it will NOT match. Also if I do a partial match (by setting full match to false) for
    "descrip", and the line is "description example" it WILL match.

    :param search_terms: List of search terms to search for.
    :type search_terms: list
    :param case_sensitive: Whether the search is case-sensitive.
    :type case_sensitive: bool
    :default case_sensitive: True
    :param full_match: If True, matches the whole word exactly; else, allows partial matches.
    :type full_match: bool
    :default full_match: False
    :param prepend_text: Text to prepend to matches.
    :type prepend_text: str
    :default prepend_text: ""
    :param append_text: Text to append to matches.
    :type append_text: str
    :default append_text: ""
    :param replace_tuple: A tuple (old_text, new_text) for replacing matches.
    :type replace_tuple: tuple or None
    :default replace_tuple: None
    :param tree: The configuration tree to search. Do not specify this, its only used for recursion
    :type tree: dict or None
    :default tree: None

    :return: A dictionary containing matched and modified results.
    :rtype: dict
    """

    if not any([isinstance(search_terms, x) for x in (list, tuple)]):
        search_terms = [search_terms]
        # raise TypeError('search_terms MUST be a list or tuple')

    data = {}
    for key, sub_tree in tree.items():
        if matches_search_terms(key, search_terms, case_sensitive, full_match):
            # only capture results that are between the min/max search depth variables, 0 max is infinite
            if _depth >= min_search_depth and (max_search_depth == 0 or _depth < max_search_depth):
                data[f'{prepend_text}{key.replace(*replace_tuple)}{append_text}'] = sub_tree
        elif isinstance(sub_tree, dict) and sub_tree:
            path = search_and_modify_config_tree(sub_tree, search_terms, case_sensitive, full_match, min_search_depth,
                                                 max_search_depth, prepend_text, append_text, replace_tuple, _depth+1)
            if path:
                data[key] = path
    return data


def search_config_tree(tree, search_terms, case_sensitive=True, full_match=False, min_search_depth=0, max_search_depth=0, _depth=0):
     """

     Searches the config tree for a set of search terms and returns the path to root for that match and any sub
     branchs under the match. Note: if a match is found, and there are other branches in that same level that dont
     match, it will not return any of the other branches. For example if you search for an IP address and it is found
     in an interface, it wont also return the description if configured.

     You may also specify if you want your search to be case sensitive, and you may also specify if you want
     a full or partial match. For example if I do a full match for "description" but the line of configuration
     is "description example" it will NOT match. Also if I do a partial match (by setting full match to false) for
     "descrip", and the line is "description example" it WILL match.

     You can also specify the minimum depth to search the tree, for example using the config below searching for
     "router bgp" will not yield any results, searching "vrf MYVRF" will yield results, but searching "vrf MYVRF"
     with a nest_level of 1 will NOT because it is nested once, and you specified to not return any matches at or
     below index 1:
     router bgp 65000
      ipv4 vrf MYVRF
       network 10.0.0.0

     You can also


     :param tree: The configuration tree to search.
     :type tree: dict or None
     :param search_terms: List of search terms to search for.
     :type search_terms: list
     :param min_search_depth: Minimum depth at which to return search results if matches are found (0 returns anything, 1 excludes root, 2 excludes root and 1st nest level)
     :type min_search_depth: int
     :param max_search_depth: Maximum depth at which to return search results if matches are found (0 infinite [default], only includes root, 2 excludes root and 1st nest level).
     :type max_search_depth: int
     :default max_search_depth: 0
     :param case_sensitive: Whether the search is case-sensitive.
     :type case_sensitive: bool
     :default case_sensitive: True
     :param full_match: If True, matches the whole word exactly; else, allows partial matches.
     :type full_match: bool

     :return: A dictionary containing matched and modified results.
     :rtype: dict
     """
     if not any([isinstance(search_terms, x) for x in (list, tuple)]):
         search_terms = [search_terms]
         # raise TypeError('search_terms MUST be a list or tuple')

     data = {}
     for key, sub_tree in tree.items():
         if matches_search_terms(key, search_terms, case_sensitive, full_match):
             # only capture results that are between the min/max search depth variables, 0 max is infinite
             if _depth >= min_search_depth and (max_search_depth == 0 or _depth < max_search_depth):
                data[key] = sub_tree
         elif isinstance(sub_tree, dict) and sub_tree:
             path = search_config_tree(sub_tree, search_terms, case_sensitive, full_match, min_search_depth, max_search_depth, _depth+1)
             if path:
                 data[key] = path
     return data


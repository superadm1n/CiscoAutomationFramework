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
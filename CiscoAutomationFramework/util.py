
def column_print(data, spaces_between_columns=2, separator_char=None):
    """
    Print in nice even columns where each column is only the width it needs to be, not the width of the
    widest column in the list.
    Based off of code from https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python
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
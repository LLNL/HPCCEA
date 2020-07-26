"""A slurm-style hostlist processor."""

import re

# ========== HELPER METHODS ========== #


def append_hostname(machine_name, num_list):
    """
    Helper method to append the hostname to node numbers.

    :param machine_name: The name of the cluster.
    :param num_list: The list of nodes to be appended to the cluster name.
    :return: A hostlist string with the hostname and node numbers.
    """

    hostlist = []
    for elem in num_list:
        hostlist.append(machine_name + str(elem))

    return '%s' % ','.join(map(str, hostlist))


def sort_nodes(nodelist):
    """
    sort_nodes is a helper method that sorts the nodes in ascending order.

    :param nodelist: The hostlist string.
    :return: The hostlist string in ascending order.
    """

    list_of_nodes = nodelist
    result_hostlist = []

    if type(list_of_nodes) == str:
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')

    count = 0
    num_list = []
    for node in nodelist:
        iter_node = nodelist[count]
        nodelist_match = r"([a-z]+)(\d+)(.*)"
        machine_name = re.search(nodelist_match, iter_node)
        num_list.append(int(machine_name.group(2)))
        count = count + 1
    num_list.sort()

    # append hostname to the node numbers
    hostlist_no_suffix = []
    for elem in num_list:
        hostlist_no_suffix.append(machine_name.group(1) + str(elem))

    # append suffix to hostlist if there is one
    final_hostlist = []
    for elem in hostlist_no_suffix:
        final_hostlist.append(elem + machine_name.group(3))

    result_hostlist.append('%s' % ','.join(map(str, final_hostlist)))

    return '%s' % ','.join(map(str, final_hostlist))


# ========== END OF HELPER METHODS =========== #


def expand(nodelist):
    """
    expand takes in a compressed hostlist string and returns all hosts listed.

    :param: nodelist: The hostlist string.
    :return: The expanded hostlist string.
    """
    node_list = nodelist.split(", ")
    # print node_list

    result_hostlist = []
    for node in node_list:
        nodelist_match = r"(\w+-?)\[((,?[0-9]+-?,?-?){0,})\](.*)?"
        if re.search(nodelist_match, node):
            match = re.search(nodelist_match, node)

            # holds the ranges of nodes as a string
            # now we can manipulate the string and cast it to a list of numbers
            oldstr = str(match.group(2))
            left_br = oldstr.replace("[", "")
            right_br = left_br.replace("]", "")
            num_list = right_br.split(',')

            # if the node numbers contain leading zeros, store them to be
            # prepended in the final list
            final_list = []
            lead_zeros = 0
            lead_zeros_str = ''
            for elem in num_list:
                # if it is a range of numbers, break it by the hyphen and
                # create a list
                #
                # will then be merged with final list
                if '-' in elem:
                    tmp_list = elem.replace("-", ",").split(",")

                    for digit in tmp_list[0]:
                        if digit == '0':
                            lead_zeros = lead_zeros + 1
                            lead_zeros_str = lead_zeros_str + '0'

                    rng_list = range(int(tmp_list[0]), int(tmp_list[1]) + 1)
                    final_list.extend(rng_list)
                else:
                    final_list.append(int(elem))

            # put final list in ascending order and append cluster name to
            # each node number
            final_list.sort()

            # prepend leading zeros to numbers required
            hostlist_tmp = []
            for elem in final_list:
                if ((lead_zeros > 0) and (len(str(elem)) <= len(lead_zeros_str))):
                    hostlist_tmp.append(str(elem).zfill(lead_zeros + 1))
                else:
                    hostlist_tmp.append(str(elem))

            # append hostname to the node numbers
            hostlist_no_suffix = []
            for elem in hostlist_tmp:
                hostlist_no_suffix.append(match.group(1) + elem)

            # append suffix to hostlist if there is one
            final_hostlist = []
            for elem in hostlist_no_suffix:
                final_hostlist.append(elem + match.group(4))

            result_hostlist.append('%s' % ','.join(map(str, final_hostlist)))

    return ','.join(result_hostlist)


def compress_range(nodelist):
    """
    compress_range will return a compressed hostlist string given a
    list of hostnames.

    :param: nodelist: The expanded hostlist string.
    :return: The compressed hostlist string.
    """

    list_of_nodes = nodelist

    if type(list_of_nodes) == str:
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        list_of_nodes = right_br.split(',')

    # get machine name and numbers for nodes
    # append the numbers of the nodes to num_list for compression
    count = 0
    num_list = []

    # check to see if there are prepending zeros in first node
    lead_zeros = 0
    lead_zeros_str = ''
    for digit in list_of_nodes[0]:
        if digit == '0':
                lead_zeros = lead_zeros + 1
                lead_zeros_str = lead_zeros_str + '0'

    # check if node is in the following format: node1-2,node3-4
    if "-" in list_of_nodes[0]:
        for node in list_of_nodes:
            iter_node = list_of_nodes[count]
            nodelist_match = r"(\w+-?)(\d+)(.*)"
            machine_name = re.search(nodelist_match, iter_node)
            num_list.append(int(machine_name.group(2)))
            count = count + 1
    else:
        for node in list_of_nodes:
            iter_node = list_of_nodes[count]
            nodelist_match = r"([a-zA-Z]+)(\d+)(.*)"
            machine_name = re.search(nodelist_match, iter_node)
            num_list.append(int(machine_name.group(2)))
            count = count + 1

    # build the ranges
    final_list = []
    num_list.sort()
    low = num_list[0]
    last = low
    i = 1
    for i in range(1, len(num_list)):
        high = num_list[i]
        if (high == last + 1):
            last = high
            continue
        if (last > low):
            final_list.append(lead_zeros_str + str(low) + "-" + str(last))
        else:
            final_list.append(lead_zeros_str + str(low))
        low = high
        last = low
    if (len(num_list) > 0):
        if (last > low):
            final_list.append(lead_zeros_str + str(low) + "-" + str(last))
        else:
            final_list.append(low)

    result_str = machine_name.group(1) + '[%s]' % ','.join(map(str, final_list))

    return result_str + machine_name.group(3)


def compress(nodelist):
    """
    compress will return a hostlist string given a list of hostnames.

    :param: nodelist: The hostlist string.
    :return: The hostlist string.
    """

    if type(nodelist) == str:
        left_br = nodelist.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')

    return '[%s]' % ','.join(map(str, nodelist))


def diff(*arg):
    """
    diff will subtract elements in all subsequent lists from list 1 and return
    the remainder.

    :param: nodelist1: The hostlist string to be subtracted from.
    :param: following nodelists: The other hostlist strings.
    :return: The remainding list from subtracting the two original lists.
    """

    conv_lists = []
    for nodelist in arg:
        if type(nodelist) == list:
            conv_lists.append(nodelist)
        # if there is a range of nodes in the input
        elif "[" in nodelist:
            list_of_nodes = expand(nodelist)
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)
        else:
            list_of_nodes = nodelist
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)

    diff_list = conv_lists[0]

    for i in range(1, len(conv_lists)):
        diff_list = set(diff_list).difference(set(conv_lists[i]))

    return compress_range(sort_nodes(list(diff_list)))


def intersect(*arg):
    """
    Given references to n lists, intersect return a list of intersecting nodes.

    :param: nodelist: Any number of nodelists to be intersected.
    :return: The resulting intersected list.
    """

    # will hold a list of the lists passed in
    conv_lists = []
    for nodelist in arg:
        if type(nodelist) == list:
            conv_lists.append(nodelist)
        # if there is a range of nodes in the input
        elif "[" in nodelist:
            list_of_nodes = expand(nodelist)
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)
        else:
            list_of_nodes = nodelist
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)

    first_list = conv_lists[0]

    # use Boolean logic to find intersecting nodes between passed in lists
    for i in range(1, len(conv_lists)):
        first_list = list(set(first_list) & set(conv_lists[i]))

    return compress_range(sort_nodes(list(first_list)))


def union_nodes(*arg):
    """
    union_nodes returns the union between n lists of nodes.

    :param: nodelist: Any number of nodelists to be combined.
    :return: The resulting unioned list.
    """

    # will hold a list of the lists passed in
    conv_lists = []
    for nodelist in arg:
        if type(nodelist) == list:
            conv_lists.append(nodelist)
        # if there is a range of nodes in the input
        elif "[" in nodelist:
            list_of_nodes = expand(nodelist)
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)
        else:
            list_of_nodes = nodelist
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)

    first_list = conv_lists[0]

    for i in range(1, len(conv_lists)):
        first_list = first_list + conv_lists[i]

    union_list = list(set(first_list))

    return compress_range(sort_nodes(union_list))


def nth(nodelist, n):
    """
    nth returns the nth node from a list of nodes.

    :param: nodelist: The hostlist string.
    :param: n: The index desired.
    :return: The host at the specified index.
    """

    if "[" in nodelist:
        nodelist_match = r"([a-z]+[A-Z0-9]?)-?\[((,?[0-9]+,?-?[0-9]+-?){0,})\](.*)?"
        if re.search(nodelist_match, nodelist):
            match = re.search(nodelist_match, nodelist)

            # holds the ranges of nodes as a string
            # now we can manipulate the string and cast it to a list of numbers
            oldstr = str(match.group(2))
            left_br = oldstr.replace("[", "")
            right_br = left_br.replace("]", "")
            num_list = right_br.split(',')

            final_list = []
            for elem in num_list:
                # if it is a range of numbers, break it by the hyphen and
                # create a list
                #
                # will then be merged with final list
                if '-' in elem:
                    tmp_list = elem.replace("-", ",").split(",")
                    rng_list = range(int(tmp_list[0]), int(tmp_list[1]) + 1)
                    final_list.extend(rng_list)
                else:
                    final_list.append(int(elem))

            # put final list in ascending order and append cluster name to each
            # node number
            final_list.sort()
            hostlist = append_hostname(match.group(1), final_list)

            # put sorted hostlist into a list, use comma as delimiter so it can
            # be accessed by an index
            hostlist_indexed = hostlist.split(",")

            if (int(n) not in range(1, len(hostlist_indexed) + 1)):

                return "node does not exist"
            else:

                return hostlist_indexed[int(n) - 1]
    elif type(nodelist) == str:
        hostlist_indexed = nodelist.split(",")
        if (int(n) not in range(1, len(hostlist_indexed) + 1)):

            return "node does not exist"
        else:

            return hostlist_indexed[int(n) - 1]
    else:
        if (int(n) not in range(1, len(nodelist) + 1)):

            return "node does not exist"
        else:

            return nodelist[int(n) - 1]


def find(nodelist, node):
    """
    find outputs the position of the node in the nodelist passed in.

    :param: nodelist: The hostlist string.
    :param: node: The host to be searched inside of the hostlist string.
    :return: The position of the host within the hostlist string.
    """

    # if input is a list, just search for it using index
    if type(nodelist) == list:
        if node in nodelist:

            return "At position " + str(nodelist.index(node) + 1)
        else:

            return "node does not exist"
    # if there is a range of nodes in the input
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if node in nodelist:

            return "At position " + str(nodelist.index(node) + 1)
        else:

            return "node does not exist"
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if node in nodelist:

            return "At position " + str(nodelist.index(node) + 1)
        else:

            return "node does not exist"


def count(nodelist):
    """
    count returns the number of hosts.

    :param: nodelist: The hostlist string.
    :return: The number of nodes in the hostlist string.
    """

    if type(nodelist) == list:

        return len(nodelist)
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')

        return len(nodelist)
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')

        return len(nodelist)


def remove_node(nodelist, node):
    """
    removes a node from a passed in hostlist.

    :param: nodelist: The hostlist string.
    :param: node: The node to be removed.
    :return: The resulting hostlist upon deletion.
    """
    if type(nodelist) == list:
        if node in nodelist:
            nodelist = list(filter(lambda a: a != node, nodelist))
            return ",".join(nodelist)
        else:
            return "node does not exist"
    # if there is a range of nodes in the input
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if node in nodelist:
            nodelist = list(filter(lambda a: a != node, nodelist))
            return ",".join(nodelist)
        else:
            return "node does not exist"
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if node in nodelist:
            nodelist = list(filter(lambda a: a != node, nodelist))
            return ",".join(nodelist)
        else:
            return "node does not exist"


def delimiter(nodelist, d):
    """
    delimiter sets the output delimiter (default = ",")

    :param: nodelist: The hostlist string.
    :param: d: The delimiter.
    :return: The resulting hostlist string with custom delimiter.
    """
    if type(nodelist) == list:
        return d.join(nodelist)
    # if there is a range of nodes in the input
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        return d.join(nodelist)
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        return d.join(nodelist)


def size_hostlist(nodelist, N):
    """
    size will output at most N hosts (-N for last N hosts)

    :param: nodelist: The hostlist string.
    :param: N: the number of hosts to print.
    :return: The resulting hostlist string with custom size.
    """
    if type(nodelist) == list:
        if N > 0:
            return compress_range(nodelist[:N])
        else:
            return compress_range(nodelist[N:])
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if N > 0:
            return compress_range(nodelist[:N])
        else:
            return compress_range(nodelist[N:])
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        if N > 0:
            return compress_range(nodelist[:N])
        else:
            return compress_range(nodelist[N:])


def xor(*arg):
    """
    xor returns the symmetric difference between n lists of nodes.

    :param: nodelist: Any number of nodelists to be xor.
    :return: The resulting xor list.
    """

    # will hold a list of the lists passed in
    conv_lists = []

    for nodelist in arg:
        # check to see if the list passed in is a string; if it is, convert
        # to list
        if type(nodelist) == list:
            conv_lists.append(nodelist)
        elif "[" in nodelist:
            list_of_nodes = expand(nodelist)
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)
        else:
            list_of_nodes = nodelist
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            conv_lists.append(nodelist)

    first_list = set(conv_lists[0])

    for i in range(1, len(conv_lists)):
        first_list = first_list.symmetric_difference(conv_lists[i])

    xor_list = list(set(first_list))

    return compress_range(sort_nodes(xor_list))


def exclude(*arg):
    """
    excludes all HOSTLIST args from first HOSTLIST

    :param: nodelist: The hostlist string.
    :param: node: The node to be excluded.
    :return: The resulting hostlist string without the nodes specified.
    """
    nodelist = arg[0]
    len_nodes = arg[1:]

    for node in len_nodes:
        if type(nodelist) == list:
            if node in nodelist:
                nodelist = list(filter(lambda a: a != node, nodelist))
                final_hostlist = ",".join(nodelist)
            else:
                return "node does not exist"
        # if there is a range of nodes in the input
        elif "[" in nodelist:
            list_of_nodes = expand(nodelist)
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            if node in nodelist:
                nodelist = list(filter(lambda a: a != node, nodelist))
                final_hostlist = ",".join(nodelist)
            else:
                return "node does not exist"
        else:
            list_of_nodes = nodelist
            left_br = list_of_nodes.replace("[", "")
            right_br = left_br.replace("]", "")
            nodelist = right_br.split(',')
            if node in nodelist:
                nodelist = list(filter(lambda a: a != node, nodelist))
                final_hostlist = ",".join(nodelist)
            else:
                return "node does not exist"

    if not final_hostlist:
        return "hostlist empty"
    elif ',' not in final_hostlist:
        return final_hostlist
    else:
        return compress_range(final_hostlist)


def quiet(nodelist=[]):
    """
    quiet will return quiet output (or exit non-zero if there is an
    empty hostlist)

    :param: nodelist: The hostlist string.
    """
    final_hostlist = nodelist

    if not final_hostlist:
        return "hostlist empty"

    if type(nodelist) == list:
            final_hostlist = ",".join(nodelist)
    # if there is a range of nodes in the input
    elif "[" in nodelist:
        list_of_nodes = expand(nodelist)
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        final_hostlist = ",".join(nodelist)
    else:
        list_of_nodes = nodelist
        left_br = list_of_nodes.replace("[", "")
        right_br = left_br.replace("]", "")
        nodelist = right_br.split(',')
        final_hostlist = ",".join(nodelist)


def filter_python(nodelist):
    """
    TODO: filter maps Python code over all hosts in result HOSTLIST

    :param: nodelist: The hostlist string.
    """
    return "This feature is not yet supported. You can file an issue on " \
        "GitHub: https://github.com/llnl/py-hostlist"

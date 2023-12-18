 Y = np.zeros_like(M, dtype=str)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            Y[i, j] = str(M[i, j])
    nodes = []
    for node in path[1:-1]:
        # print(node)
        delta = [node[-1][0] - node[-2][0], node[-1][1] - node[-2][1]]
        if delta == [0, 1]:
            sign = ">"
        elif delta == [0, -1]:
            sign = "<"
        elif delta == [-1, 0]:
            sign = "^"
        elif delta == [1, 0]:
            sign = "v"
        else:
            raise ValueError
        for i, j in node:
            # Y[i, j] = "#"
            if (i, j) != (0, 0):
                nodes.append((i, j))
        Y[node[-1][0], node[-1][1]] = sign

    for i in range(1, 4):
        node = path[1]
        delta = [node[i][0] - node[i - 1][0], node[i][1] - node[i - 1][1]]
        if delta == [0, 1]:
            sign = ">"
        elif delta == [0, -1]:
            sign = "<"
        elif delta == [-1, 0]:
            sign = "^"
        elif delta == [1, 0]:
            sign = "v"
        else:
            raise ValueError

        Y[node[i][0], node[i][1]] = sign

    # for i in range(M.shape[0]):
    #     for j in range(M.shape[1]):
    #         print(Y[i, j], end="")
    #     print()
    nodes_set = np.argwhere((Y == ">") | (Y == "<") | (Y == "^") | (Y == "v"))
    vals = []
    for node in nodes_set:
        vals.append(M[node[0], node[1]])
    return sum(vals)
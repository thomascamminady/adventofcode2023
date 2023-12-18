 start_node = (0, 0)
    G.add_edge(start_node, (start_node, (0, 1)), weight=0)
    G.add_edge(start_node, (start_node, (1, 0)), weight=0)

    G.add_edge(
        (start_node, (0, 1)),
        (start_node, (0, 1), (0, 2)),
        weight=0 * M[0, 1] + M[0, 2],
    )
    G.add_edge(
        (start_node, (0, 1)),
        (start_node, (0, 1), (1, 1)),
        weight=0 * M[0, 1] + M[1, 1],
    )

    G.add_edge(
        (start_node, (1, 0)),
        (start_node, (1, 0), (2, 0)),
        weight=0 * M[1, 0] + M[2, 0],
    )
    G.add_edge(
        (start_node, (1, 0)),
        (start_node, (1, 0), (1, 1)),
        weight=0 * M[1, 0] + M[1, 1],
    )

    # now th ending ones
    n, m = M.shape[0] - 1, M.shape[1] - 1
    G.add_edge(
        (n, m),
        ((n, m - 1), (n, m)),
        weight=0,
    )
    G.add_edge(
        (n, m),
        ((n - 1, m), (n, m)),
        weight=0,
    )

    G.add_edge(
        ((n, m - 1), (n, m)),
        ((n, m - 2), (n, m - 1), (n, m)),
        weight=M[n, m - 2] + M[n, m - 1],
    )
    G.add_edge(
        ((n, m - 1), (n, m)),
        ((n - 1, m - 1), (n, m - 1), (n, m)),
        weight=M[n - 1, m - 1] + M[n, m - 1],
    )

    G.add_edge(
        ((n - 1, m), (n, m)),
        ((n - 2, m), (n - 1, m), (n, m)),
        weight=M[n - 2, m] + 0 * M[n - 1, m],
    )
    G.add_edge(
        ((n - 1, m), (n, m)),
        ((n - 1, m - 1), (n - 1, m), (n, m)),
        weight=M[n - 1, m - 1] + 0 * M[n - 1, m],
    )

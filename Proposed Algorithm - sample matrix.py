import math

"""
Proposed matrix
"""
matrix = [
    [0, 10, 30, 31, 20, 28, 44, 43, 10, 21],
    [10, 0, 22, 18, 40, 26, 37, 39, 19, 39],
    [30, 22, 0, 18, 26, 23, 50, 18, 41, 41],
    [31, 18, 18, 0, 15, 22, 42, 20, 12, 30],
    [20, 40, 26, 15, 0, 12, 10, 15, 47, 34],
    [28, 26, 23, 22, 12, 0, 16, 33, 28, 18],
    [44, 37, 50, 42, 10, 16, 0, 31, 37, 48],
    [43, 39, 18, 20, 15, 33, 31, 0, 34, 45],
    [10, 19, 41, 12, 47, 28, 37, 34, 0, 28],
    [21, 39, 41, 30, 34, 18, 48, 45, 28, 0]
]

"""
Set cities label by matrix dimension
if 0 = A, 1 = B, 2 = C, ...
"""
cities = [chr(c+65) for c in range(0, len(matrix))]

highlighted = []


def dimen(m):
    """
    Fungsi untuk mengetahui dimensi matrix

    Parameters:
        m - Array matrix awal

    Return:
        Array two dimensional, e.g. [10, 10] untuk matrix 10x10
    """

    return [len(m), len(m[0])]


def average(m):
    """
    Fungsi untuk mencari rata-rata matrix

    Parameters:
        m - Array matrix awal

    Return:
        Integer round down average
    """
    el = []
    for x in m:
        for y in x:
            if y > 0 and y not in el:
                el.append(y)

    avg = sum(el) / len(el)
    return math.floor(avg)  # round down


def highlight(m):
    """
    Fungsi untuk mencari highlighted cost

    Parameters:
        m - Array matrix awal

    Return:
        Array highlighted cost
    """
    sel = []
    avg = average(m)

    for i, x in enumerate(m):
        selected = []
        for y in x:
            if y >= avg:
                selected.append(y)

        sel.append([i, selected])

    return sel


def sort_method_1(h):
    """
    * Fungsi sort di bawah ini berdasarkan jumlah node terbesar (descending) dan sum total cost terkecil (ascending)
    * Fungsi sort ini tidak memperhatikan urutan start point, yang mana memiliki total cost terkecil, itu yang menjadi start

    Parameters:
        h - Array highlighted cost yang ingin diurutkan

    Return:
        Array yang diurutkan
    """

    sorted_list = sorted(h, key=lambda x: (len(x[1]), -sum(x[1])), reverse=True)
    sorted_list[1:] = sorted(sorted_list[1:], key=lambda x: (len(x[1]), -sum(x[1])), reverse=True)
    return sorted_list


def sort_method_2(h):
    """
    * Fungsi sort ini mengurutkan berdasarkan urutan alfabet route, mempertahankan posisi start point
    * Start point adalah route jumlah route terbanyak yang berada di posisi alfabet terawal

    Parameters:
        h - Array highlighted cost yang ingin diurutkan

    Return:
        Array yang diurutkan
    """

    sorted_list = []
    route_flat = [[x[0], len(x[1])] for x in h]

    while len(route_flat) > 0:
        max_len = max(route_flat, key=lambda x: x[1])
        for j in range(0, len(route_flat)):
            if route_flat[j][1] == max_len[1]:
                index = route_flat[j][0]
                sorted_list.append(h[index])
                del route_flat[j]
                break

    # urut route ke-2 dst berdasarkan jumlah node terbesar dan total cost terkecil
    sorted_list[1:] = sorted(sorted_list[1:], key=lambda x: (len(x[1]), -sum(x[1])), reverse=True)
    return sorted_list


def calculate_cost(m, result):
    """
    Fungsi untuk menghitung total cost pada route (result)

    Parameters:
        m - Array matrix awal
        result - Array route yang telah diproses

    Return:
        Integer total costs
    """

    costs = []
    for i in range(0, len(result)):
        if i < len(result)-1:
            x, y = result[i], result[i+1]
            costs.append(m[x][y])

    return sum(costs)


def get_city_route(r):
    """
    Fungsi untuk mencetak label route (A, B, C, ...), bukan berdasarkan index (0, 1, 2, ...)

    Parameters:
        r - Array yang dihasilkan oleh proses TSA solving

    Return:
        Array berisi urutan label berdasarkan hasil route TSA
    """

    result = []
    for x in r:
        result.append(cities[x])

    return result


def solve(m):
    """
    Fungsi utama untuk solve TSA

    Parameters:
        m - Array matrix awal

    Return:
        None
    """

    h = highlight(m)
    avg = average(m)
    sorted_highlights = sort_method_1(h)    # atau bisa menggunakan => sort_method_2(h)

    def tsa(m):
        """
        Sub-function untuk TSA, routine sesuai algoritma pada presentasi
        """

        routes = []
        route_list = [e[0] for e in sorted_highlights]  # deep copy

        while True:
            if len(route_list) == 0:
                break

            # jika route masih kosong
            if len(routes) == 0:
                routes.append(route_list[0])
                del route_list[0]
                continue

            start = routes[-1]

            route_check = [e for e in route_list]  # deep copy

            while True:
                target = route_check[0]

                x, y = start, target

                # Jika target adalah highlighted cost?
                cost = m[x][y]
                if cost >= avg:
                    del route_check[0]
                    continue

                routes.append(target)
                route_list.remove(target)
                break

        return routes

    result = tsa(m)
    result.append(result[0])

    cost = calculate_cost(m, result)
    print('n =', dimen(m)[0], '| µ =', avg, '| Σ cost:', cost)

    city_route = get_city_route(result)
    print(city_route)
    print()


"""
Main routine untuk calculate matrix:
- 4x4, 5x5, 6x6, 7x7, 8x8, 9x9, 10x10
"""
for i in range(4, 10+1):
    test_matrix = []
    for j in range(0, i):
        test_matrix.append(matrix[j][:i])
    solve(test_matrix)
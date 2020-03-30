from algorithm import GraphPath
import numpy as np


def main():
    size = np.int32(input())
    gr = GraphPath()
    gr.input_graph(size)
    print(gr.graph)
    result = np.array(gr._get_path(gr.graph, [0, ], 6))
    print(result)
    power, graph = gr.find_max_power(1, 10)
    print("power : ", power)
    print("graph : ", graph)
    check_point_one = gr.check_point_one(power, graph)
    print("check point 1 : ", check_point_one)
    selection = gr.find_section(graph, set())
    print("Selection : ", selection)
    check_point_two = gr.check_point_two(selection, power)
    print("check point 2 : ", check_point_two)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()
'''
0 6 1 0 0 0
6 0 2 0 3 0 
1 2 0 3 0 0 
0 0 3 0 1 2
0 3 0 1 0 5
0 0 0 2 5 0
'''

'''
10
0 4 9 2 0 0 6 0 0 0
4 0 0 0 0 0 2 5 0 0 
9 0 0 7 0 2 1 0 0 0
2 0 7 0 5 9 0 0 0 0
0 0 0 5 0 0 0 0 8 0
0 0 2 9 0 0 6 0 7 4
6 2 1 0 0 6 0 4 0 2
0 5 0 0 0 0 4 0 0 3
0 0 0 0 8 7 0 0 0 6
0 0 0 0 0 4 2 3 6 0
'''
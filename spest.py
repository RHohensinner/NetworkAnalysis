import networkx as nx
import matplotlib.pylab as pylab
import sys, random, math


def main(nw_name):
    G = nx.read_gml(nw_name)
    a, b, c = get_landmarks(G)

    error_list_a = calc_distances(a, G)
    error_list_b = calc_distances(b, G)
    error_list_c = calc_distances(c, G)

    a_mean, a_variance, a_std_dev = calc_and_plot_error(error_list_a)
    b_mean, b_variance, b_std_dev = calc_and_plot_error(error_list_b)
    c_mean, c_variance, c_std_dev = calc_and_plot_error(error_list_c)

    figa = pylab.figure(1)
    pylab.hist(error_list_a, bins=max(error_list_a), align='right')
    pylab.xlabel("$\epsilon$")
    pylab.ylabel("$p(\epsilon)$")
    pylab.title("Distribution of errors: $\overline{\epsilon}=%f, \sigma=%f$"%(a_mean, a_std_dev))
    figa.show()

    figb = pylab.figure(2)
    pylab.hist(error_list_b, bins=max(error_list_b), align='right')
    pylab.xlabel("$\epsilon$")
    pylab.ylabel("$p(\epsilon)$")
    pylab.title("Distribution of errors: $\overline{\epsilon}=%f, \sigma=%f$"%(b_mean, b_std_dev))
    figb.show()

    figc = pylab.figure(3)
    pylab.hist(error_list_c, bins=max(error_list_c), align='right')
    pylab.xlabel("$\epsilon$")
    pylab.ylabel("$p(\epsilon)$")
    pylab.title("Distribution of errors: $\overline{\epsilon}=%f, \sigma=%f$"%(c_mean, c_std_dev))
    figc.show()

    figa.savefig('a.png')
    figb.savefig('b.png')
    figc.savefig('c.png')


def calc_and_plot_error(err_list):
    sum_err = 0
    for error in err_list:
        sum_err += error

    mean = (float(sum_err) / float(len(err_list)))
    variance = 0.0
    for error in err_list:
        variance += pow(2, (float(error) - mean))
    variance = (variance / len(err_list))
    std_dev = math.sqrt(float(variance))

    print(mean, variance, std_dev)
    return mean, variance, std_dev
	

def get_landmarks(G):

    n = float(nx.number_of_nodes(G))
    ndegrees = nx.degree(G)
    degrees = []
    nodes_list = []
    deg_dict = {}
    for node in ndegrees:
        degrees.append(node[1])
        nodes_list.append(node)
        deg_dict[node[0]] = node[1]
    mdegree = max(degrees)
    avg_degree = (sum(degrees) / n)

    a = []
    b = []
    c = []

    # (a): 10 random landmarks
    while len(a) < 10:
        rand_index = random.randrange(len(ndegrees))
        if nodes_list[rand_index] not in a:
            a.append(nodes_list[rand_index])

    # (b): 10 random "high degree" landmarks
    while len(b) < 10:
        rand_index = random.randrange(len(ndegrees))
        if nodes_list[rand_index][1] > avg_degree:
            if nodes_list[rand_index] not in b:
                b.append(nodes_list[rand_index])

    # (c): 10 random "low degree" landmarks
    while len(c) < 10:
        rand_index = random.randrange(len(ndegrees))
        if nodes_list[rand_index][1] < avg_degree:
            if nodes_list[rand_index] not in c:
                c.append(nodes_list[rand_index])

    return a, b, c


def calc_distances(lm_set, G):
    n = float(nx.number_of_nodes(G))
    sp = nx.shortest_path_length(G)
    distances = []
    temp_list = []
    name_list = []
    for i in lm_set:
        name_list.append(i[0])

    global_dist_dir = {}
    for node in sp:
        if node[0] in name_list:
            for target in node:
                temp_list.append(target)
            distances.append(temp_list)
            temp_list = []
        temp_dir = {}
        for target in node[1]:
            temp_dir[target] = node[1][target]
        global_dist_dir[node[0]] = temp_dir


    set_s_u_t_list = []
    s_u_t_dir = {}

    ndegrees = nx.degree(G)
    all_names = []
    for node in ndegrees:
        all_names.append(node[0])

    for item in range(len(lm_set)):
        for name in all_names:
            s = name
            temp_dir = {}
            for target in distances[item][1]:
                t = target
                dist = distances[item][1][s] + distances[item][1][t]
                temp_dir[t] = dist
            s_u_t_dir[name] = temp_dir
        set_s_u_t_list.append(s_u_t_dir)
        s_u_t_dir = {}


    min_dist_dir = {}
    for start in all_names:
        t_dir = {}
        for end in all_names:
            temp_dist_list = []
            for set in set_s_u_t_list:
                t_d = set[start][end]
                temp_dist_list.append(t_d)
            t_dir[end] = min(temp_dist_list)
            temp_dist_list = []
        min_dist_dir[start] = t_dir


    distance_error_list = []
    for start in all_names:
        for end in all_names:
            dist_one = global_dist_dir[start][end]
            dist_two = min_dist_dir[start][end]
            err = abs(dist_one - dist_two)
            distance_error_list.append(err)

    return distance_error_list


if __name__ == "__main__":
    nw_name = sys.argv[1]
    main(nw_name)

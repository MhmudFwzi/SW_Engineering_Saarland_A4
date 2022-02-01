from operator import indexOf, sub


with open('samples.csv', "r") as f:
    lines = f.readlines()

feature_names = lines[0].split(",")[1:-1]

ids = []
feature_selections = []
performances = []

for l in lines[1:]:
    l_list = l.split(",")
    ids.append(l_list[0])
    feature_selections.append(l_list[1:-1])
    performances.append(int(l_list[-1][:-1]))
    
def compute_split_error(feature_name, sub_selections, sub_performances):
    feature_index = feature_names.index(feature_name)
    left_indices = [] #f=1
    right_indices = [] #f=0
    for i,fs in enumerate(sub_selections):
        if fs[feature_index] == '1':
            left_indices.append(i)
        else:
            right_indices.append(i)
    left_performances = [sub_performances[i] for i in left_indices]
    try:
        l_avg = sum(left_performances)/len(left_performances)
    except:
        l_avg = 0
    l_err = 0
    for p in left_performances:
        l_err = l_err + (p - l_avg)**2
    right_performances = [sub_performances[i] for i in right_indices]
    try:
        r_avg = sum(right_performances)/len(right_performances)
    except:
        r_avg = 0
    r_err = 0
    for p in right_performances:
        r_err = r_err + (p - r_avg)**2
    return(round(l_err+r_err,2))

def get_best_splitting_feature(s_selections, s_performances):
    best_split_error = float('inf')
    best_feature = ""
    for fn in feature_names:
        err = compute_split_error(fn, s_selections, s_performances)
        if err < best_split_error:
            best_split_error = err
            best_feature = fn
    return best_feature

def split_by_feature(feature, s_points, s_perf):
    feature_index = feature_names.index(feature)
    left = {"selections": [], "performances": []}
    right = {"selections": [], "performances": []}
    for i,p in enumerate(s_points):
        if p[feature_index] == '1':
            left["selections"].append(p)
            left["performances"].append(s_perf[i])
        else:
            right["selections"].append(p)
            right["performances"].append(s_perf[i])
    return left, right

def build_tree(subselections, subperformances, current_err, name, indent):
    print(indent + "datapoints: " + str(len(subselections)))
    print(indent + "error_of_split: " + str(current_err))
    if len(subselections) < 2:
        return
    mean = sum(subperformances)/len(subperformances)
    print(indent + "mean: " + str(round(mean,2)))
    print(indent + "name: " + name)
    next_feature = get_best_splitting_feature(subselections, subperformances)
    split_err = compute_split_error(next_feature, subselections, subperformances)
    if split_err >= current_err:
        return
    else:
        print(indent + "split_by_feature: " + next_feature)
        l,r = split_by_feature(next_feature, subselections, subperformances)
        print(indent + "successor_left:")
        build_tree(l['selections'], l['performances'], split_err, name + 'L', indent+" ")
        print(indent + "successor_right:")
        build_tree(r['selections'], r['performances'], split_err, name + 'R', indent+" ")

initial_err = compute_split_error('Algorithm', feature_selections,performances) #feature that doesn't split, Compression also works
build_tree(feature_selections, performances, initial_err, 'X', "")
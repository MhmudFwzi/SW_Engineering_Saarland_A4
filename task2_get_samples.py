import random
random.seed(1) #for replication

with open("per_measures.csv") as f:
    lines = f.readlines()

distance_sets = [[], [], [], [], [], [], []]

for l in lines[1:]:
    id = l.split(",")[0]
    feature_selections = l.split(",")[1:-1]
    for i,f in enumerate(feature_selections):
        feature_selections[i] = int(f)
    distance = sum(feature_selections) - 3
    distance_sets[distance].append(id)

samples = []

for i,d in enumerate(distance_sets):
    if len(d) < 5:
        samples.append(d)
    else:
        sample_ids = []
        while len(sample_ids) != 4:
            selection = random.randint(0, len(d) - 1)
            if selection not in sample_ids:
                sample_ids.append(selection)
        sample = []
        for id in sample_ids:
            sample.append(d[id])
        samples.append(sample)

with open("per_measures.csv") as f:
    lines = f.readlines()

f = open("samples.csv", "a")
f.write(lines[0])

for l in lines:
    for s in samples:
        if l.split(",")[0] in s:
            f.write(l)

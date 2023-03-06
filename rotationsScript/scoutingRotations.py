import csv

# Constants

number_of_matches = 70
matches_per_rotation = 10


# Reading scouts from scouts.txt

scouts = []

with open("scouts.txt", "r") as f:
    for line in f:
        scouts.append(line.rstrip())

number_of_scouts = len(scouts)

# header for output.csv file
header = ["Quals Match", "red1", "red2", "red3", "blue1", "blue2", "blue3"]

# array where index represents match number and value is list of scouts
rotations = []

scout_sets = []
for i in range(len(scouts) // 6 ):
    scouting_set = []
    for j in range(6):
        scouting_set.append(scouts[i*6+j])
    scout_sets.append(scouting_set)

print(scout_sets)

# write logic to generate rototions here
for i in range(number_of_matches):
    row = [i+1]
    row.extend(scout_sets[(i//matches_per_rotation)%(len(scout_sets))])
    rotations.append(row)
        

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rotations)
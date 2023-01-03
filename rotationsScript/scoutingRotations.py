import csv

#Constants

number_of_matches = 60
matches_per_rotation = 5


#Reading scouts from scouts.txt

scouts = []

with open("scouts.txt", "r") as f:
    for line in f:
        scouts.append(line.rstrip())

number_of_scouts = len(scouts)

#header for output.csv file
header = ["red1", "red2", "red3", "blue1", "blue2", "blue3"]

#array where index represents match number and value is list of scouts
rotations = []

#write logic to generate rototions here






with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rotations)
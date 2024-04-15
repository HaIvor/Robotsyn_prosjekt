split_lines = [
    [
        (-2000, 778, 1999, 779, 779.0, 1.5707964),
        (-2000, 725, 1999, 726, 726.0, 1.5707964),
        (-2000, 679, 1999, 680, 680.0, 1.5707964),
        (-2000, 624, 1999, 625, 625.0, 1.5707964),
        (-2000, 576, 1999, 577, 577.0, 1.5707964)
    ],
    [
        (-2000, 332, 1999, 333, 333.0, 1.5707964),
        (-2004, 236, 1994, 305, 271.0, 1.5882496),
        (-2000, 227, 1999, 228, 228.0, 1.5707964),
        (-2000, 179, 1999, 180, 180.0, 1.5707964),
        (-2000, 124, 1999, 125, 125.0, 1.5707964)
    ]
]

value_to_add = 1
for sublist in split_lines:
    for index, tup in enumerate(sublist):
        sublist[index] = tup + (value_to_add,)
        value_to_add += 1
        if value_to_add > 5:
            value_to_add = 1

print(split_lines)

test_tuple = [[(1, 2, 3, 4)], [(5, 6, 7, 8)]]
print(test_tuple[1][0][3])
distance_info = (distance, note_pos)

    if no_intersection_found:
        #code for notes in between lines
        for line in split_lines:
            smallest_distance = 1000000
            for x1,y1,x2,y2,rho,theta,note_pos in line:
                distance = abs(y1-y_c)
                if distance < smallest_distance:
                    smallest_distance = distance
                    smallest_info = (smallest_distance, note_pos)
        print("smallest_info:",smallest_info)
        if smallest_info[1] == 5 and line[]:
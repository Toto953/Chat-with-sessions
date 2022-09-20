sessions = [[["id", "password"], ["user_name", "s_client"], ["user_name2", "s_client2"]], [["id1", "password1"], ["user_name1", "s_client1"], ["user_name2", "s_client2"]]]

counter = 0
for i in sessions:
    for j in i[1:]:
        if j == ["user_name1", "s_client1"]:
            # print(i[1:])
            print(j)
            sessions[counter].remove(j)
    counter += 1

# print(sessions)
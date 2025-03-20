def output_txt(profile_num,time, depth, pressure):
    with open(f"profile{profile_num}.txt", "a") as file:
        file.write(f"{time}, {depth}, {pressure}\n")

#brainstorm more util functions?
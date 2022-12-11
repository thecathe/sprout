
# array of elves 
elf_log = []

file = open("input", "r")

working_elf = []
working_calories = 0
greatest_elf = 0
for line in file.readlines():
    if line == "\n": # log working elf
        elf_log.append({"total":working_calories,"items":working_elf})
        if working_calories > greatest_elf:
            greatest_elf = working_calories
        working_calories = 0
        working_elf = []
        print(elf_log[len(elf_log)-2])
    else: # collect in working elf
        working_elf.append(line[:-2])
        working_calories += int(line)
    
file.close()

print(greatest_elf)

def greatest(num: int):
    total_log = []
    for elf in elf_log:
        total_log.append(elf["total"])
    total_log.sort(reverse=True)
    
    top_log = [total_log[i] for i in range(num)]
    print(top_log)

    # add up
    total = 0
    for top in top_log:
        total += top
    return total

print(greatest(3))


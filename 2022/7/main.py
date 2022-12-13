# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# Build tree
class File:
    def __init__(self, name, size):
        self.Name = name
        self.FileSize = size

class Directory:
    def __init__(self, name):
        self.Name = name
        self.SubDirs = []
        self.Files = []
        self.Size = None
    def getSize(self):
        if self.Size is not None:
            return self.Size

        self.Size = 0
        for dir in self.SubDirs:
            self.Size += dir.getSize()
        for file in self.Files:
            self.Size += file.FileSize
        return self.Size

root = Directory("/")
all_directories = [root]
current_dir = root
call_stack = []

def stringFromStack(stack, current_dir):
    names = [x.Name for x in stack]
    names.append(current_dir.Name)
    return "".join(names)

def printTree(tree, depth = 0):
    tabs = "".join(["    " for i in range(0, depth)])
    print(tabs + f"- {tree.Name} (dir)")
    for dir in tree.SubDirs:
        printTree(dir, depth + 1)
    tabs += "    "
    for file in tree.Files:
        print(tabs + f"- {file.Name} (file, size={file.FileSize})")

listed_directories = set()
processing_new_ls = False
for line in input_lines[1:]:
    if line.startswith("$"):
        # Command
        parts = line.split()
        if (parts[1] == "cd"):
            if parts[2] == "..":
                current_dir = call_stack.pop()
            else:
                call_stack.append(current_dir)
                current_dir = next(dir for dir in current_dir.SubDirs if dir.Name == parts[2])
        elif (parts[1] == "ls"):
            pwd = stringFromStack(call_stack, current_dir)
            processing_new_ls = pwd not in listed_directories
            listed_directories.add(pwd)
    else:
        if not processing_new_ls:
            continue
        if line.startswith("dir"):
            # ls listing of a dir
            parts = line.split()
            new_dir = Directory(parts[1])
            current_dir.SubDirs.append(new_dir)
            all_directories.append(new_dir)
        else:
            # ls listing of a file
            parts = line.split()
            current_dir.Files.append(File(parts[1], int(parts[0])))
printTree(root)

# Part 1
dir_sizes = [directory.getSize() for directory in all_directories]
total_size = 0
for size in dir_sizes:
    if size <= 100000:
        total_size += size
print(f"Total size of all dirs under 100000: {total_size}")

# Part 2
total_capacity = 70000000
total_used = dir_sizes[0] # the root one
total_unused = total_capacity - total_used
target_space = 30000000
min_delete = target_space - total_unused
dir_sizes.sort()
smallest_dir_to_delete = next(x for x in dir_sizes if x >= min_delete)
print(f"The smallest dir we can delete has size: {smallest_dir_to_delete}")
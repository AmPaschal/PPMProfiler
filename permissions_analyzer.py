import subprocess
from profile_enum import ProfileKey
import time

timestamp = int(time.time())
output_filename = "permissions_analyzer_" + str(timestamp) + ".txt"

def execute_shell_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip()

def run_shell_command(command):

    output = execute_shell_command(command)

    permissions = []

    for line in output.split('\n'):

        # Sample output: [PERMISSION] org.apache.commons.TestClass 3 FS READ src/main/java/com/ampaschal/google/testdir/testfile.txt
        if line.startswith("[PERMISSION]"):
            entries = line.split()
            if len(entries) >= 3:
                permission = {}
                permission["type"] = entries[3]
                permission["op"] = entries[4]
                permission["stack_size"] = entries[2]
                permission["target"] = entries[5]
                permissions.append(permission)

    return permissions


def process_permissions(objects):
    count_dict = {
        "stack_size_avg": 0,
        "stack_size_min": float('inf'),
        "stack_size_max": 0,
        "unique_targets_fs": 0,
        "unique_targets_net": 0,
        "unique_targets_runtime": 0
    }

    stack_size_sum = 0
    unique_targets_fs_set = set()
    unique_targets_net_set = set()
    unique_targets_runtime_set = set()

    for obj in objects:
        obj_type = obj["type"]
        obj_op = obj["op"]
        obj_stack_size = obj["stack_size"]
        obj_target = obj["target"]

        count_dict[obj_type] = count_dict.get(obj_type, 0) + 1
        count_dict[obj_op] = count_dict.get(obj_op, 0) + 1

        # Update stack size information
        obj_stack_size_int = int(obj_stack_size)
        stack_size_sum += obj_stack_size_int
        count_dict["stack_size_min"] = min(count_dict["stack_size_min"], obj_stack_size_int)
        count_dict["stack_size_max"] = max(count_dict["stack_size_max"], obj_stack_size_int)

        # Update target information
        if obj_type == "FS":
            unique_targets_fs_set.add(obj_target)
        elif obj_type == "NET":
            unique_targets_net_set.add(obj_target)
        elif obj_type == "RUNTIME":
            unique_targets_runtime_set.add(obj_target)

    # Calculate average stack size and update count_dict
    num_objects = len(objects)
    if num_objects > 0:
        count_dict["stack_size_avg"] = round(stack_size_sum / num_objects, 2)

    # Update unique target count
    count_dict["unique_targets_fs"] = len(unique_targets_fs_set)
    count_dict["unique_targets_net"] = len(unique_targets_net_set)
    count_dict["unique_targets_runtime"] = len(unique_targets_runtime_set)

    return count_dict



# def process_permissions(objects):
#     count_dict = {}

#     for obj in objects:
#         obj_type = obj["type"]
#         obj_op = obj["op"]
#         obj_stack_size = obj["stack_size"]
#         obj_target = obj["target"]

#         count_dict[obj_type] = count_dict.get(obj_type, 0) + 1
#         count_dict[obj_op] = count_dict.get(obj_op, 0) + 1

#     return count_dict


def write_to_file(string):

    with open(output_filename, 'a') as file:
        file.write(string)

def print_permissions(program_name, perm_count:dict):

    fs = perm_count.get("FS", 0)
    net = perm_count.get("NET", 0)
    runtime = perm_count.get("RUNTIME", 0)
    read = perm_count.get("READ", 0)
    write = perm_count.get("WRITE", 0)
    connect = perm_count.get("CONNECT", 0)
    accept = perm_count.get("ACCEPT", 0)
    execute = perm_count.get("EXECUTE", 0)
    stack_size_avg = perm_count.get("stack_size_avg", 0)
    stack_size_min = perm_count.get("stack_size_min", 0)
    stack_size_max = perm_count.get("stack_size_max", 0)
    unique_targets_fs = perm_count.get("unique_targets_fs", 0)
    unique_targets_net = perm_count.get("unique_targets_net", 0)
    unique_targets_runtime = perm_count.get("unique_targets_runtime", 0)

    write_to_file(f"{str(program_name).ljust(12)}\t\t\t{str(stack_size_avg).ljust(5)}\t\t{str(stack_size_min).ljust(5)}\t\t{str(stack_size_max).ljust(5)}\t\t{str(unique_targets_fs).ljust(5)}\t\t{str(unique_targets_net).ljust(5)}\t\t{str(unique_targets_runtime).ljust(5)}\t\t{str(fs).ljust(5)}\t\t{str(read).ljust(5)}\t\t{str(write).ljust(5)}\t\t{str(net).ljust(5) }\t\t{str(connect).ljust(5) }\t\t{str(accept).ljust(5) }\t\t{str(runtime).ljust(5) }\t\t{str(execute).ljust(5) }\n")



java = "/usr/local/buildtools/java/jdk/bin/java"
file_encoding = "-Dfile.encoding=UTF-8"
permAgentPath = "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-perm-agent.jar"
agent_classpath = "-classpath /usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/classes:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm/9.4/asm-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-util/9.4/asm-util-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-tree/9.4/asm-tree-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-analysis/9.4/asm-analysis-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-commons/9.4/asm-commons-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.15.1/jackson-databind-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-annotations/2.15.1/jackson-annotations-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-core/2.15.1/jackson-core-2.15.1.jar"
app_classpath = f"{agent_classpath}:/usr/local/google/home/pamusuo/Research/dacapobench/benchmarks/dacapo-evaluation-git-334f6fcd.jar"
# app_name = "com.ampaschal.google.apps.AllPermissionsApp"
app_name = "Harness"
app_args_list = ["avrora", "batik", "biojava", "cassandra", "eclipse", "fop", "graphchi", "h2", "jme", "jython", "kafka", "luindex", "lusearch", "pmd", "spring", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan", "zxing"]
app_args_list = ["tradesoap"]
# app_args_list = [""]

write_to_file("Program     \t\t\tSSAv \t\tSSMn \t\tSSMx \t\tUTF  \t\tUTN  \t\tUTR  \t\tFS   \t\tREAD \t\tWRITE\t\tNET  \t\tCONNECT\t\tACCEPT\t\tRUNTIME\t\tEXECUTE\n\n")

num_args = len(app_args_list)
count = 0

for app_args in app_args_list:

    count += 1

    print(f"Running {app_args} ({count}/{num_args})")

    try:

        command = f"{java} {permAgentPath} {file_encoding} {app_classpath} {app_name} {app_args}"

        permissions = run_shell_command(command)
        permissions_count = process_permissions(permissions)
        print_permissions(app_args, permissions_count)

    except Exception as e:
        print("An error occurred", str(e))
        write_to_file(f"An error occurred. {str(e)}")


import subprocess
from profile_enum import ProfileKey
import time

timestamp = int(time.time())
output_filename = "profile_" + str(timestamp) + ".txt"

def execute_shell_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip()

def run_shell_command(command):
    profile_dict = {}

    start_time = int(execute_shell_command("date '+%s%3N'"))
    profile_dict[ProfileKey.PROGRAM_START.name] = start_time

    output = execute_shell_command(command)

    stop_time = int(execute_shell_command("date '+%s%3N'"))
    profile_dict[ProfileKey.PROGRAM_END.name] = stop_time

    for line in output.split('\n'):
        if line.startswith("[PROFILING]"):
            entries = line.split()
            if len(entries) >= 3:
                profile_dict[entries[1]] = int(entries[2])

    return profile_dict

# Create a function to calculate the average profile from a list of profiles
def calculate_average_profile(profiles):
    average_profile = {}
    num_profiles = len(profiles)

    if num_profiles == 0:
        return average_profile

    # Sum the values of each profile key
    for key in profiles[0]:
        sum_value = sum(profile[key] for profile in profiles)
        average_value = sum_value / num_profiles
        average_profile[key] = average_value

    return average_profile

def process_profile(profile):
    # print(f"Using {agent}")

    start_main = profile[ProfileKey.MAIN_CALLED.name] - profile[ProfileKey.PROGRAM_START.name]
    # print("Start time to Main: " + str(start_main))

    if (ProfileKey.AGENT_CALLED.name in profile):

        start_agent = profile[ProfileKey.AGENT_CALLED.name] - profile[ProfileKey.PROGRAM_START.name]
        # print("Start time to Agent called: " + str(start_agent))

        agent_setup = profile[ProfileKey.AGENT_EXITING.name] - profile[ProfileKey.AGENT_CALLED.name]
        # print("Agent setup time: " + str(agent_setup))

    else:
        start_agent = 0
        agent_setup = 0

    if (ProfileKey.FILE_TRANSFORMER_EXITING.name in profile):
        file_trans = profile[ProfileKey.FILE_TRANSFORMER_EXITING.name] - profile[ProfileKey.FILE_TRANSFORMER_CALLED.name]
        # print("File transformation time: " + str(file_trans))
    else:
        file_trans = 0
    
    main_exec = profile[ProfileKey.MAIN_EXITING.name] - profile[ProfileKey.MAIN_CALLED.name]
    # print("Main execution time: " + str(main_exec))
    
    total_exec = profile[ProfileKey.PROGRAM_END.name] - profile[ProfileKey.PROGRAM_START.name]
    # print("Total execution time: " + str(total_exec))

    profile_dict = {}
    profile_dict["start_main"] = start_main
    profile_dict["start_agent"] = start_agent
    profile_dict["agent_setup"] = agent_setup
    profile_dict["file_trans"] = file_trans
    profile_dict["main_exec"] = main_exec
    profile_dict["total_exec"] = total_exec

    return profile_dict


def format_var(var):

    return format(var, '.2f')


def write_to_file(string):

    with open(output_filename, 'a') as file:
        file.write(string)

def print_profile(profile_dict, agent):

    start_main = format_var(profile_dict["start_main"])
    start_agent = format_var(profile_dict["start_agent"])
    agent_setup = format_var(profile_dict["agent_setup"])
    file_trans = format_var(profile_dict["file_trans"])
    main_exec = format_var(profile_dict["main_exec"])
    total_exec = format_var(profile_dict["total_exec"])

    
    write_to_file(f"{agent}\t\t\t{start_main}\t\t{start_agent}\t\t{agent_setup}\t\t{file_trans}\t\t{main_exec}\t\t{total_exec}\n")


emptyAgentPath = ["empty-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-empty-perm-agent.jar"]
filePermAgentPath = ["no-fr-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-file-perm-agent.jar"]
noTransAgentPath = ["no-trans-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-no-trans-agent.jar"]
permAgentPath = ["all-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-perm-agent.jar"]
noAgentPath = ["no-agent".ljust(18), ""]

agents = [noAgentPath, permAgentPath, noTransAgentPath, emptyAgentPath, noAgentPath, filePermAgentPath, permAgentPath]
java = "/usr/local/buildtools/java/jdk/bin/java"
file_encoding = "-Dfile.encoding=UTF-8"
agent_classpath = "-classpath /usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/classes:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm/9.4/asm-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-util/9.4/asm-util-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-tree/9.4/asm-tree-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-analysis/9.4/asm-analysis-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-commons/9.4/asm-commons-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.15.1/jackson-databind-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-annotations/2.15.1/jackson-annotations-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-core/2.15.1/jackson-core-2.15.1.jar"
app_classpath = f"{agent_classpath}:/usr/local/google/home/pamusuo/Research/dacapobench/benchmarks/dacapo-evaluation-git-334f6fcd.jar"
# app_name = "com.ampaschal.google.apps.AllPermissionsApp"
app_name = "Harness"
app_args_list = ["avrora", "batik", "biojava", "eclipse", "fop", "graphchi", "h2", "jme", "jython", "kafka", "luindex", "lusearch", "pmd", "spring", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan", "zxing"]
app_args_list = ["sunflow", "xalan", "zxing"]

write_to_file(f"{'Agent'.ljust(18)}\t\t\tstart-main\tstart-agent\tagent-setup\tfile-trans\tmain-exec\ttotal-exec\n\n")

num_args = len(app_args_list)
count = 0

for app_args in app_args_list:

    count += 1

    print(f"Running {app_args} ({count}/{num_args})")

    write_to_file(f"\nRunning {app_args}:\n")

    try:

        ag_count = 0

        for agent in agents:

            ag_count += 1

            command = f"{java} {agent[1]} {file_encoding} {app_classpath} {app_name} {app_args}"
            
            profiles = []

            for _ in range(3):
                profile = run_shell_command(command)
                processed_profile = process_profile(profile)
                profiles.append(processed_profile)

            # Discard the first 2 agent runs
            if ag_count > 2:
                average_profile = calculate_average_profile(profiles)
                print_profile(average_profile, agent[0])

    except Exception as e:
        print("An error occurred", str(e))
        write_to_file(f"An error occurred. {str(e)}")


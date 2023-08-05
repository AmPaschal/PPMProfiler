import subprocess
import time

# Specify the Java program and its arguments
java_program = "YourJavaProgram"
java_program_args = ["arg1", "arg2"]

java = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
file_encoding = "-Dfile.encoding=UTF-8"
app_classpath = "-classpath /usr/local/google/home/pamusuo/Research/PermissionsMicroBenchmarks/target/classes:/usr/local/google/home/pamusuo/.m2/repository/org/openjdk/jmh/jmh-core/1.35/jmh-core-1.35.jar:/usr/local/google/home/pamusuo/.m2/repository/net/sf/jopt-simple/jopt-simple/5.0.4/jopt-simple-5.0.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/apache/commons/commons-math3/3.2/commons-math3-3.2.jar:/usr/local/google/home/pamusuo/.m2/repository/org/openjdk/jmh/jmh-generator-annprocess/1.35/jmh-generator-annprocess-1.35.jar:/usr/local/google/home/pamusuo/.m2/repository/com/ampaschal/google/PackagePermissionsManager/1.0-SNAPSHOT/PackagePermissionsManager-1.0-SNAPSHOT.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm/9.4/asm-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-util/9.4/asm-util-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-tree/9.4/asm-tree-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-analysis/9.4/asm-analysis-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/org/ow2/asm/asm-commons/9.4/asm-commons-9.4.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-databind/2.15.1/jackson-databind-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-annotations/2.15.1/jackson-annotations-2.15.1.jar:/usr/local/google/home/pamusuo/.m2/repository/com/fasterxml/jackson/core/jackson-core/2.15.1/jackson-core-2.15.1.jar"
app_name = "com.ampaschal.google.ManualBenchmarkRunner"

# Specify the agents
emptyAgentPath = ["empty-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-empty-perm-agent.jar"]
filePermAgentPath = ["no-fr-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-file-perm-agent.jar"]
noTransAgentPath = ["no-trans-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-no-trans-agent.jar"]
permAgentPath = ["all-perm-agent".ljust(18), "-javaagent:/usr/local/google/home/pamusuo/Research/PackagePermissionsManager/target/PackagePermissionsManager-1.0-SNAPSHOT-perm-agent.jar"]
noAgentPath = ["no-agent".ljust(18), ""]

agents = [noAgentPath, noTransAgentPath, emptyAgentPath, filePermAgentPath, permAgentPath]
agents = [noAgentPath]

# Execute the Java program with each agent and process the output
results = {}
for agent in agents:
    agent_name = agent[0]
    agent_path = agent[1]
    print(f"Microbenchmarking with agent {agent_name}")
    command = f"{java} {agent_path} {file_encoding} {app_classpath} {app_name}"
            
            
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    print("Output")
    print(output)
    decoded = output.decode().strip()
    lines = decoded.split("\n")

    agent_result = {}
    for line in lines:

        if line.startswith("[BENCHMARK]"):
            components = line.split()
            method_name = components[1]
            average = components[2]
            agent_result[method_name] = average
            
    results[agent_name] = agent_result

# Write the results to a file
timestamp = int(time.time())
output_filename = "microbenchmark_setup_check_perm_" + str(timestamp) + ".txt"

with open(output_filename, "w") as file:
    agent_names = results.keys()
    method_names = results[next(iter(results))].keys()

    name_length = max(len(name) for name in method_names)

    file.write(f"{'Method name'.ljust(name_length)}\t")
    for agent in agents:
        file.write(agent[0] + "\t")
    file.write("\n")

    for method_name in method_names:

        file.write(str(method_name).ljust(name_length) + "\t")

        for agent in agent_names:
            agent_result = results[agent]
            method_value = agent_result[method_name]
            file.write(method_value.ljust(18) + "\t")

        file.write("\n")

print("Results written to", output_filename)

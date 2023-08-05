
def generate_java_list_code(py_list):
    java_code = "Set<Object> set = new HashSet<>();\n"
    for element in py_list:
        if isinstance(element, str):
            java_code += f'set.add("{element}");\n'
        else:
            java_code += f'set.add({element});\n'
    return java_code


default_paths = [
    "com.ampaschal.google",
    "org.apache.tomcat",
    "org.apache.commons"
]

count = 100

generated_paths = []

for path in default_paths:

    generated_path = f"{path}.TestClass"
    generated_paths.append(generated_path)

    for i in range(count - 1):
        generated_path = f"{path}_{i}.TestClass"
        generated_paths.append(generated_path)


java_string = generate_java_list_code(py_list=generated_paths)





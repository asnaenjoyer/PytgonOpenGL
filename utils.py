
def load_shader(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
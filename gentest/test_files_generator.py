import os
import ast
from jinja2 import Environment, FileSystemLoader

class TestFilesGenerator:
    def __init__(self):
        if not os.path.exists("tests"):
            os.mkdir("tests")
        
        env = Environment(loader=FileSystemLoader('.'))
        self.template = env.get_template('template.jinja')

    def generate_test_file(self, file_path):
        with open(file_path, "r") as f:
            file_content = f.read()

        parsed = ast.parse(file_content)
        stmts = parsed.body
        classes = [stmt for stmt in stmts if isinstance(stmt, ast.ClassDef)]
        obj_names_of_classes = [self.__get_cls_obj_name(i.name) for i in classes]
        module_import_name = ".".join(file_path.replace("/", ".").replace("\\", ".").split(".")[:-1])
        gen_file = self.template.render(cls_objs_names=obj_names_of_classes, classes=classes, module_import_name=module_import_name, func_instance = ast.FunctionDef)
        file_name = os.path.basename(file_path)
        with open(f"./tests/test_{file_name}", "w") as f:
            f.write(gen_file)


    def __get_cls_obj_name(self, cls_name):
        if len(cls_name) == 1:
            return cls_name[0].lower()
        
        obj_name = cls_name[0].lower()
        last_case = self.__get_case(cls_name[1])
        one_change_done = False
        for char in cls_name[1:]:
            if self.__get_case(char) != last_case:
                if one_change_done:
                    obj_name += char.lower()
                    one_change_done = False
                else:
                    obj_name += "_" + char.lower()
                if not one_change_done:
                    one_change_done = True
            else:
                obj_name += char.lower()
            last_case = self.__get_case(char)
        
        return obj_name

    def __get_case(self, s):
        if s.islower():
            return "lower"
        return "upper"
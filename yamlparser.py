import yaml
import re

class YamlParser:



    def GetDeployments(template, path):

      first_line = True
        # Write on a test file
      template.pop(0)
      with open(path + "\\"+ "file_appoggio.yaml", "w") as f:
        for line in template:
          line = line.replace("{", "\"")
          line = line.replace("}", "\"")
          f.write(line + "\n")
        f.close


      with open(path + "\\"+ "file_appoggio.yaml", 'r+') as stream:
        try:
          
          parsed_yaml=yaml.safe_load(stream)
          print(parsed_yaml)
          print("### KIND PRINT ####")
          print(parsed_yaml["kind"])
          print("### LABELS ####")
          print(parsed_yaml["spec"]["template"]["metadata"]["labels"])
          print("### CONTAINERS ###")
          print(parsed_yaml["spec"]["template"]["spec"]["containers"])

          for element in parsed_yaml["spec"]["template"]["spec"]["containers"]:
            print("### NAME ###")
            print(element["name"])

        except yaml.YAMLError as exc:
          print(exc)




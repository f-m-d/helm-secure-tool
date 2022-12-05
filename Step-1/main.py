import json
import pprint
import yaml


####################################
def GetTemplateType(path):
  # Open the file
  yaml_file = open(r'C:\Users\King Crimson\Desktop\Test_HelmChart\demo\templates\service.yaml')
  lines = yaml_file.readlines()

  count=0
  for line in lines:

    # Check for Helm Strings: starting with "{{" and ending with "}}"
    if line.find("kind") != -1:
      print("Line{}: {}".format(count, line.strip()))
    count += 1

######################################
def GetHelmLines(path):
  # Open the file
  yaml_file = open(r'C:\Users\King Crimson\Desktop\Test_HelmChart\demo\templates\service.yaml')
  lines = yaml_file.readlines()

  count=0
  for line in lines:

    # Check for Helm Strings: starting with "{{" and ending with "}}"
    if line.find("{{") != -1:
      print("Line{}: {}".format(count, line.strip()))
    count += 1


#####################################
def ReplaceHelmLines(path):
  # Open the file
  yaml_file = open(r'C:\Users\King Crimson\Desktop\Test_HelmChart\demo\templates\service.yaml')
  lines = yaml_file.readlines()



############ MAIN #######################

if __name__ == "__main__":
  GetTemplateType("a")
  GetHelmLines("a")
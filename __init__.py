import json
import pprint
import yaml
from os import listdir
from os.path import isfile, isdir, join
from graph import Graph

######################################
def AddElementToGraph(graph_handler):
  


  pass







#######################################
def FolderCheck(path, graph_handler):
      # Open a folder 
  #dirpath = r"C:\Users\King Crimson\Desktop\Test_HelmChart\test-chart\templates"
  dirpath = path
  # List all files in a directory, directories included
  # allfiles = [f for f in listdir(dirpath)]
  # print("### ALL FILES ###")
  # print(allfiles)

  # List only files, no directories 
  onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
  onlydirs = [f for f in listdir(dirpath) if isdir(join(dirpath, f))]
  print("### FILES ONLY, NO DIRS ###")
  print(onlyfiles)

  # Print only
  for file in onlyfiles:
    if file.find(".yaml") != -1 or file.find(".yml") != -1:
      #print("FILE PATH: " + path + "\\" + file)
      helm_type_list = GetTemplateType(path+"\\"+file)
      print("####################################")
      # Add edge to the graph
      for helm_type in helm_type_list:
        graph_handler.add_edge(helm_type, "")
  
  for dir in onlydirs:
    #print("##### SEARCHING IN FOLDER: " + path+"\\"+dir )
    FolderCheck(path+"\\"+dir, graph_handler)

  # List only directories
  # onlydirs = [f for f in listdir(dirpath) if isdir(join(dirpath, f))]
  # print("### OLY DIRS ###")
  # print(onlydirs)
  # pass

####################################
def GetTemplateType(path):
    # Open the file
    yaml_file = open(path)
    lines = yaml_file.readlines()

    helm_type_list = []
    count=0
    for line in lines:

        # Check for Helm Strings: starting with "{{" and ending with "}}"
        if line.find("kind") != -1:
            #print("Line{}: {}".format(count, line.strip()))
            print("{}".format(line.strip()))

            #Add the string to return
            a = line.strip().split()
            helm_type = a[1]
            print("---- HELM TYPE PRINT ----")
            print(helm_type)
            helm_type_list.append(helm_type)
        count += 1
    return helm_type_list

######################################
def GetHelmLines(path):
# Open the file
    yaml_file = open(path)
    lines = yaml_file.readlines()

    count=0
    for line in lines:

        # Check for Helm Strings: starting with "{{" and ending with "}}"
        if line.find("{{") != -1:
            print("Line{}: {}".format(count, line.strip()))
        count += 1


#####################################
def CheckDefaultHelmObjects(path):
# Open the file
    yaml_file = open(path)
    lines = yaml_file.readlines()

    count=0
    for line in lines:

        # Check for Helm Strings: starting with "{{" and ending with "}}"
        if line.find("{{") != -1:
            print("Line{}: {}".format(count, line.strip()))
        count += 1


############ MAIN #######################

if __name__ == "__main__":

  #path = r"C:\Users\King Crimson\Desktop\Test_HelmChart\demo\templates\configmap.yaml"
  #GetTemplateType(path)
  #GetHelmLines(path)
  graph_handler = Graph(0)
  FolderCheck(r"C:\Users\King Crimson\Desktop\Test_HelmChart\test-chart\templates", graph_handler)

  #Instantiate an empty graph


  # Add nodes to list
  graph_handler.print_edge_list()

  pass

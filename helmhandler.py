from fileinput import close
import itertools as IT


class HelmHandler:

    ## SIMPLE PRINT OF PATH + KINDS FOUND IN THE FILE FROM PATH ##
    def PrintPathAndKinds(paths, kinds):
      for path, kind in zip(paths,kinds):
        print("-----------------------------------")
        print("###### PATH #####")
        print(path)
        print("###### KINDS ####")
        print(kind)
        print("-----------------------------------")


    ## FROM PATH, GET ALL THE KINDS INSIDE THE FILE FROM PATH ##
    def GetHelmTemplateKind(path):
      yaml_file = open(path)
      lines = yaml_file.readlines()
      yaml_file.close()

      helm_type_list = []
      count=0
      for line in lines:

        # Check for Helm Strings: starting with "{{" and ending with "}}"
        if line.find("kind") != -1:
            #print("Line{}: {}".format(count, line.strip()))
            #print("{}".format(line.strip()))

            #Add the string to return
            a = line.strip().split()
            helm_type = a[1]
            helm_type_list.append(helm_type)
        count += 1
      return helm_type_list


    ## FROM FILE WITH KIND "Pod", ADD IT TO GRAPTH WITH FORMAT
    ## FOR THE POD: Add_To_Graph("Pod::[POD-NAME]", "Container::[CONTAINER-NAME]::[Image:1.0.0]",1)
    ## FOR THE NAMESPACE: Add_To_Graph("Namespace", "Pod::[POD-NAME]", 1)
    def AddPodToGraph(path):
        pass
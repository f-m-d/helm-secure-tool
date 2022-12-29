from fileinput import close
from graph import Graph
import itertools as IT
import re


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
    def GetPodAndContainerName(path):

      pod_name = "Pod::"
      container_name = "Container::"

      # Read the file
      yaml_file = open(path)
      lines = yaml_file.readlines()
      yaml_file.close()

      for line in lines:
        if "  name: " in line:
          # Strip the POD name
          #print("### POD NAME ###")
          #print(line)
          #print("File path: "+path)
          pod_name = pod_name + re.sub("  name: ", "", line)
        
          
        if "    - name: " in line:
          # Strip the Container name
          #print("### CONTAINER NAME ###")
          #print(line)
          container_name = container_name + re.sub("    - name: ", "", line)
      return pod_name, container_name




  

    # FROM FILE WITH KIND "Deployment", ADD IT TO GRAPH WITH FORMAT
    # FOR THE DEPLOYMENT AND POD: Add_To_Graph("Deployment::[DP-NAME]", "Pod::[POD-NAME or label]",1)
    # FOR THE NAMESPACE: Add_To_Graph("Namespace", "Deployment::[DP-NAME]", 1)
    def GetDeploymentAndPodName(path):
      pod_name = "Pod::"
      deployment_name = "Deployment::"

      # Read the file
      yaml_file = open(path)
      lines = yaml_file.readlines()
      yaml_file.close()

      for line in lines:
        if "  name: " in line:
          # Strip the POD name
          #print("### POD NAME ###")
          #print(line)
          #print("File path: "+path)
          deployment_name = deployment_name + re.sub("  name: ", "", line)
          pod_name = pod_name + re.sub("  name: ", "", line)
      return deployment_name, pod_name
    

    ## FROM FILE WITH KIND "Service", ADD IT TO GRAPTH WITH FORMAT
    ## FOR THE SERVICE AND POD: Add_To_Graph("Service::[SVC-NAME]", "Pod::[POD-NAME or label]",1)
    ## FOR THE NAMESPACE: Add_To_Graph("Namespace", "Service::[SVC-NAME]", 1)
    def GetServiceAndPodName(path):
      pass


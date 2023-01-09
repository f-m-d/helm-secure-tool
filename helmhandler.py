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


    # ## FROM PATH, GET ALL THE KINDS INSIDE THE FILE FROM PATH ##
    # def GetHelmTemplateKind(path):
    #   yaml_file = open(path)
    #   lines = yaml_file.readlines()
    #   yaml_file.close()

    #   helm_type_list = []
    #   count=0
    #   for line in lines:

    #     # Check for Helm Strings: starting with "{{" and ending with "}}"
    #     if line.find("kind") != -1:
    #         #print("Line{}: {}".format(count, line.strip()))
    #         #print("{}".format(line.strip()))

    #         #Add the string to return
    #         a = line.strip().split()
    #         helm_type = a[1]
    #         helm_type_list.append(helm_type)
    #     count += 1
    #   return helm_type_list


    ## FROM FILE WITH KIND "Pod", ADD IT TO GRAPTH WITH FORMAT
    ## FOR THE POD: Add_To_Graph("Pod::[POD-NAME]", "Container::[CONTAINER-NAME]::[Image:1.0.0]",1)
    ## FOR THE NAMESPACE: Add_To_Graph("Namespace", "Pod::[POD-NAME]", 1)
    def GetPodAndContainerName(template):
      pod_name_found = False
      pod_name = "Pod::"
      container_name = "Container::"
      container_list = []

      # Read the file
      # yaml_file = open(path)
      # lines = yaml_file.readlines()
      # yaml_file.close()

      for line in template:
        if "  name: " in line and not pod_name_found:
          # Strip the POD name
          #print("### POD NAME ###")
          #print(line)
          #print("File path: "+path)
          pod_name = pod_name + re.sub("  name: ", "", line)
          pod_name_found = True
        
          
        if "    - name: " in line:
          # Strip the Container name
          #print("### CONTAINER NAME ###")
          #print(line)
          container_name_stub = container_name + re.sub("    - name: ", "", line)
          container_list.append(container_name_stub)
      return pod_name, container_list




  

    # FROM FILE WITH KIND "Deployment", ADD IT TO GRAPH WITH FORMAT
    # FOR THE DEPLOYMENT AND POD: Add_To_Graph("Deployment::[DP-NAME]", "Pod::[POD-NAME or label]",1)
    # FOR THE NAMESPACE: Add_To_Graph("Namespace", "Deployment::[DP-NAME]", 1)
    def GetDeploymentAndPodName(template):
      pod_name_found = False
      deployment_name_found = False
      pod_name = "Pod::"
      deployment_name = "Deployment::"

      # Read the file
      # yaml_file = open(path)
      # lines = yaml_file.readlines()
      # yaml_file.close()

      for line in template:
        if "  name: " in line and not deployment_name_found:
          # Strip the POD name
          #print("### POD NAME ###")
          #print(line)
          #print("File path: "+path)
          deployment_name = deployment_name + re.sub("  name: ", "", line)
          pod_name = pod_name + re.sub("  name: ", "", line)
          deployment_name_found = True

      return deployment_name, pod_name
    

    ## FROM FILE WITH KIND "Service", ADD IT TO GRAPTH WITH FORMAT
    ## FOR THE SERVICE AND POD: Add_To_Graph("Service::[SVC-NAME]", "Pod::[POD-NAME or label]",1)
    ## FOR THE NAMESPACE: Add_To_Graph("Namespace", "Service::[SVC-NAME]", 1)
    ## NB: THE PODS ARE GENERETED BY DEPLOYMENT/REPLICASETS/DAEMONSETS ETC.
    ## SO THE SERVICES 
    def GetServiceAndPodLabels(template):
      service_name_found = False
      selector_tag_found = False
      service_name = "Service::"
      pod_label = "Pod::Label::"
      pod_label_list = []

      # yaml_file = open(path)
      # lines = yaml_file.readlines()
      # yaml_file.close()    


      for line in template:
        if "  name: " in line and not service_name_found:
          # Strip service Name
          service_name = service_name + re.sub("  name: ", "", line)
          service_name_found = True

          # If you find the "  selector:" tag,
          # take all the successi
        if "  selector:" in line and not selector_tag_found:
          selector_tag_found = True  

        
        if "    " in line and selector_tag_found:
          stub_pod_label = pod_label + re.sub("    ", "", line)
          pod_label_list.append(stub_pod_label)
        

      return service_name, pod_label_list


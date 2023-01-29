import yaml
import re

class YamlParser:

    def CreateTemplateYamlFile(template, path):
      # Stub file name
      STUB_YAML_FILE_NAME = "stub_yaml_file.yaml"

      # Remove first line (Comment by Helm)
      template.pop(0)

      # Create stub file
      yaml_file_name = path + "\\"+ STUB_YAML_FILE_NAME

      # Write YAML Helm Template in YAML stub file
      with open(yaml_file_name, "w") as f:
        for line in template:
          # Remove "{ }" chars
          line = line.replace("{", "\"")
          line = line.replace("}", "\"")
          f.write(line + "\n")
        f.close
      return yaml_file_name


    def GetDeploymentAndContainers(template, path):
      deployment_name = "Deployment::"
      container_name = "Container::"
      container_list = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)
          #print(parsed_yaml)

          # Get Deployment name
          deployment_name = deployment_name + parsed_yaml["metadata"]["name"]

          # Get container names
          for element in parsed_yaml["spec"]["template"]["spec"]["containers"]:
            container_list.append(container_name + "" + element["name"])
          
          return deployment_name, container_list

        except yaml.YAMLError as exc:
          print(exc)

    

    def GetPodAndContainers(template, path):
      pod_name = "Pod::"
      container_name = "Container::"
      container_list = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get Deployment name
          pod_name = pod_name + parsed_yaml["metadata"]["name"]

          # Get container names
          for element in parsed_yaml["spec"]["containers"]:
            #print(element["name"])
            container_list.append(container_name + "" + element["name"])
          
          return pod_name, container_list

        except yaml.YAMLError as exc:
          print(exc)



    def GetServiceAndPodLabels(template, path):
      svc_name = "Service::"
      pod_label = "Pod::Label::"
      pod_label_list = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get Deployment name
          svc_name = svc_name + parsed_yaml["metadata"]["name"]

          # Get Labels
          # Labers are in form of "key": "value"
          # So you have to iter both of them
          # . item -> (key,value) for each item
          for item in parsed_yaml["spec"]["selector"].items():
            #print(item)
            pod_label_list.append(pod_label + "" + item[0] + " " + item[1])
          
          return svc_name, pod_label_list

        except yaml.YAMLError as exc:
          print(exc)




    def GetPersistentVolumeName(template, path):
      pv_name = "PersistentVolume::"

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get PV name
          pv_name = pv_name + parsed_yaml["metadata"]["name"]
          
          return pv_name

        except yaml.YAMLError as exc:
          print(exc)



    
    def GetPvcNameAndPvName(template, path):
      pvc_name = "PersistentVolumeClaim::"
      pv_name = "PersistentVolume::"


      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get PVC and PV name
          pvc_name = pvc_name + parsed_yaml["metadata"]["name"]

          if "volumeName:" in template:
            pv_name = pv_name + parsed_yaml["metadata"]["volumeName"]

          if "volumeName" not in template:
            pv_name = pv_name + "Generic::" + parsed_yaml["spec"]["resources"]["requests"]["storage"]
      
          
          return pvc_name, pv_name

        except yaml.YAMLError as exc:
          print(exc)


    # 1) Resoure RoleBinding to namespace
    # 2) Add_To_Graph(Role, User::Name,1)
    def GetRoleBindingNameRoleNameAndUsers(template, path):
      rb_name = "RoleBinding::"
      role_name = "Role::"
      users = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get RoleBinding, Role and Users
          rb_name = rb_name + parsed_yaml["metadata"]["name"]
          role_name = role_name + parsed_yaml["roleRef"]["name"]
          
          for item in parsed_yaml["subjects"]:
            users.append(item["kind"] + "::" + item["name"])
      
          return rb_name, role_name, users

        except yaml.YAMLError as exc:
          print(exc)

      pass



    def GetClusterRoleBindingNameClusterRoleNameAndUsers(template, path):
      rb_name = "ClusterRoleBinding::"
      role_name = "ClusterRole::"
      users = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get RoleBinding, Role and Users
          rb_name = rb_name + parsed_yaml["metadata"]["name"]
          role_name = role_name + parsed_yaml["roleRef"]["name"]
          
          for item in parsed_yaml["subjects"]:
            users.append(item["kind"] + "::" + item["name"])
      
          return rb_name, role_name, users

        except yaml.YAMLError as exc:
          print(exc)

      pass


    def GetNetworkPolicyNameAndAssociations(template, path):
      np_name = "NetworkPolicy::"
      pod_label = "Pod::Label::"
      ingress_name = "Ingress::"
      egress_name = "Egress::"
      pod_label_list = []
      ingress_list = []
      egress_list = []

      # Write on a test file
      yaml_stub_path = YamlParser.CreateTemplateYamlFile(template,path)

      # Open test file
      with open(yaml_stub_path, 'r+') as stream:
        try:
          parsed_yaml=yaml.safe_load(stream)

          # Get Network Policy name
          np_name = np_name + parsed_yaml["metadata"]["name"]

          # Get Labels
          # Labers are in form of "key": "value"
          # So you have to iter both of them
          # . item -> (key,value) for each item
          for item in parsed_yaml["spec"]["podSelector"]["matchLabels"].items():
            #print(item)
            pod_label_list.append(pod_label + "" + item[0] + ": " + item[1])

          # Get Ingress rules first
          if "  ingress:" in template:
            from_list = parsed_yaml["spec"]["ingress"]
            for element in from_list:
              for from_element in element["from"]:

                # Handle CIDR and exceptions
                if "ipBlock" in from_element:
                  if "cird" in from_element["ipBlock"]:
                    ingress_list.append(ingress_name + "cidr::" + from_element["ipBlock"]["cidr"])

                  if "except" in from_element["ipBlock"]:
                    #print(from_element["ipBlock"]["except"])
                    for exception in from_element["ipBlock"]["except"]:
                      ingress_list.append(ingress_name + "except::" + exception)

                  
                # Handle
                if "namespaceSelector" in from_element:
                  namespaces_labels = from_element["namespaceSelector"]["matchLabels"].items()
                  for label in namespaces_labels:
                    ingress_list.append(ingress_name + "namespaceSelector::" + label[0] + ": " + label[1])

                if "podSelector" in from_element:
                  pod_labels = from_element["podSelector"]["matchLabels"].items()
                  for label in pod_labels:
                    ingress_list.append(ingress_name + "podSelector::" + label[0] + ": " + label[1])


          if "  egress:" in template:
            from_list = parsed_yaml["spec"]["egress"]
            for element in from_list:
              for from_element in element["to"]:

                # Handle CIDR and exceptions
                if "ipBlock" in from_element:
                  if "cidr" in from_element["ipBlock"]:
                    egress_list.append(egress_name + "cidr::" + from_element["ipBlock"]["cidr"])

                  if "except" in from_element["ipBlock"]:
                    #print(from_element["ipBlock"]["except"])
                    for exception in from_element["ipBlock"]["except"]:
                      egress_list.append(egress_name + "except::" + exception)

                  
                # Handle
                if "namespaceSelector" in from_element:
                  namespaces_labels = from_element["namespaceSelector"]["matchLabels"].items()
                  for label in namespaces_labels:
                    egress_list.append(egress_name + "namespaceSelector::" + label[0] + ": " + label[1])

                if "podSelector" in from_element:
                  pod_labels = from_element["podSelector"]["matchLabels"].items()
                  for label in pod_labels:
                    egress_list.append(egress_name + "podSelector::" + label[0] + ": " + label[1])     
              #print("### INGRESS POLICY FOUND ###")



          # if "  egress:" in template:
          #   to_list = parsed_yaml["spec"]["egress"]
          #   for element in to_list:
          #     for to_element in element["to"]:
          #       print(to_element)
          #     print("### EGRESS POLICY FOUND ###")

          
          print(ingress_list)
          print(egress_list)
          return np_name, pod_label_list, ingress_list, egress_list

        except yaml.YAMLError as exc:
          print(exc)
        





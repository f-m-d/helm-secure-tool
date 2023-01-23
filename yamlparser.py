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
        





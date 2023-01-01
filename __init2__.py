from sys import argv
from os import listdir
from os.path import isfile, isdir, join
from graph import Graph
from helmhandler import HelmHandler

####################################################################
# GET THE KIND, REPLACE "XXXX" AS UTILITIES IN A DIFFERENT FILE!! ##
# ONLY STEPS ALLOWED HERE!!!!                                     ##
####################################################################
def Step1_ReturnHelmTemplatesList(path):

  file_list = []  
  dirpath = path
  
  # Return all YAML files (potential Helm template) in the path folder
  # if a folder is found, recursively search in it for YAML files 
  onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
  onlydirs = [f for f in listdir(dirpath) if isdir(join(dirpath, f))]

  for file in onlyfiles:
    file_list.append(path+'\\' +file)


  #file_list = onlyfiles
  for dir in onlydirs:
    files_from_dir = Step1_ReturnHelmTemplatesList(path+"\\"+dir)

    for file in files_from_dir:
        file_list.append(file)

  for file in file_list:
    if file.find(".yaml") == -1:
      file_list.remove(file)
  return file_list




###############################################################################
###############################################################################
###############################################################################

if __name__ == "__main__":
    # Declare an empty graph
      #path = r"C:\Users\King Crimson\Desktop\Test_HelmChart\test-chart\templates"
      path = argv[1]
      graph_handler = Graph(0)

      # Step1: return all files YAML from the Helm Chart main dir (recursively)
      path_file_list = Step1_ReturnHelmTemplatesList(path)
      #print(path_file_list)

      # Get Helm Kinds
      helm_kind_list = []
      for path in path_file_list:
        helm_kind_list.append(HelmHandler.GetHelmTemplateKind(path))
      
      HelmHandler.PrintPathAndKinds(path_file_list, helm_kind_list)

      # Adding POD to graph
      for path, helm_kind in zip(path_file_list, helm_kind_list):
        if "Deployment" in helm_kind:
          deployment_name, pod_name = HelmHandler.GetDeploymentAndPodName(path)
          graph_handler.add_edge("Namespace::Test_Namespace", deployment_name, 1)
          graph_handler.add_edge("Namespace::Test_Namespace", pod_name, 1)
          graph_handler.add_edge(deployment_name, pod_name, 1)

        if "Pod" in helm_kind:
          pod_name, container_name = HelmHandler.GetPodAndContainerName(path)
          graph_handler.add_edge("Namespace::Test_Namespace", pod_name, 1)
          graph_handler.add_edge(pod_name, container_name, 1)
        
        if "Service" in helm_kind:
          service_name, pod_label = HelmHandler.GetServiceAndPodLabels(path)
          graph_handler.add_edge("Namespace::Test_Namespace", service_name,1)
          graph_handler.add_edge(service_name,pod_label,1)

      graph_handler.print_edge_list()

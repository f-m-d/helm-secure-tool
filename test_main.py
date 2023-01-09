from test import Helm
from sys import argv
from graph import Graph
from helmhandler import HelmHandler

if __name__ == "__main__":

  graph_handler = Graph(0)

  path = argv[1]

  # Test an "helm template [path]" 
  helm_template_output_file = Helm.GetHelmTemplateCommandOutputFile(path)

  # Open the file and starting from the bot, strip the various file
  # "expanded from template" using the Helm GO parser

  # Print gile path
  print("--- FILE PATH ---")
  print(helm_template_output_file)

  template_list = Helm.GetHelmTemplateListFromFile(helm_template_output_file)
  #print("### PRINTING FILE LIST")
  #print(template_list)

  for template in template_list:
    print("#########################################")
    print("############# PRINTING FILE #############")
    print("#########################################")
    for line in template:
      print(line)


# For each template, create a grap link
  for template in template_list:
    if "kind: Deployment" in template:
      deployment_name, pod_name = HelmHandler.GetDeploymentAndPodName(template)
      graph_handler.add_edge("Namespace::Test_Namespace", deployment_name, 1)
      graph_handler.add_edge("Namespace::Test_Namespace", pod_name, 1)
      graph_handler.add_edge(deployment_name, pod_name, 1)
    
    if "kind: Pod" in template:
      pod_name, container_list = HelmHandler.GetPodAndContainerName(template)
      graph_handler.add_edge("Namespace::Test_Namespace", pod_name, 1)

      for container_name in container_list:
        graph_handler.add_edge("Namespace::Test_Namespace", container_name, 1)
        graph_handler.add_edge(pod_name, container_name, 1)
        
    if "kind: Service" in template:
      service_name, pod_label_list = HelmHandler.GetServiceAndPodLabels(template)
      graph_handler.add_edge("Namespace::Test_Namespace", service_name,1)

      for pod_label in pod_label_list:
        graph_handler.add_edge(service_name,pod_label,1)
 
  # Print Edge
  print("#########################################")
  print("############# GRAPH STATUS ##############")
  print("#########################################")
graph_handler.print_edge_list()

  
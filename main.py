from helm_handler import Helm
from sys import argv
from graph import Graph
from yaml_parser import YamlParser
import re

if __name__ == "__main__":

  pod_count = 0
  deployment_count = 0
  service_count = 0
  pvc_count = 0
  pv_count = 0
  rb_count = 0
  crb_count = 0
  psp_count = 0
  np_count = 0



  # Initialize a Graph
  graph_handler = Graph(0)

  

  # Indicate a namespace
  path = argv[1]
  namespace = "Namespace::"+argv[2]

  # Test an "helm template [path] command" 
  helm_template_output_file = Helm.GetHelmTemplateCommandOutputFile(path)

  # Open the file and starting from the bot, strip the templates
  # "expanded from template" using the Helm GO parser

  # Print gile path
  print("--- FILE PATH ---")
  print(helm_template_output_file)

  template_list = Helm.GetHelmTemplateListFromFile(helm_template_output_file)
  #print("### PRINTING FILE LIST")
  #print(template_list)

  # for template in template_list:
  #   print("#########################################")
  #   print("############# PRINTING FILE #############")
  #   print("#########################################")
  #   for line in template:
  #     print(line)


# For each template, create a grap link
  for template in template_list:

    # Find the kind from file
    # NB: The kind from the template can vary in section,
    # so better search in the whole file
    kind = ""
    for line in template:
        m = re.search("kind: .+", line)
        if m.__class__.__name__ == "Match":
          #print(m.group())
          kind = m.group()
          #print(kind)
          break



    
    #######################
    ##### DEPLOYMENT ######
    #######################
    if kind == "kind: Deployment":
      deployment_count = deployment_count +1
      deployment_name, containers, vm_list, containers_with_vm_list = YamlParser.GetDeploymentAndContainers(template, path)
      print("### DEPLOYMENT ###")
      graph_handler.add_edge(namespace, deployment_name, 1)
      for container in containers:
        graph_handler.add_edge(namespace, container, 1)
        graph_handler.add_edge(deployment_name, container, 1)

      for container, volume_mount in zip(containers_with_vm_list, vm_list):
        graph_handler.add_edge(container, volume_mount,1)
      
    


    #######################
    ######### POD #########
    #######################
    if kind == "kind: Pod":
      pod_name, containers = YamlParser.GetPodAndContainers(template, path)
      print("### POD ###")
      graph_handler.add_edge(namespace, pod_name, 1)
      for container in containers:
        graph_handler.add_edge(namespace, container, 1)
        graph_handler.add_edge(pod_name, container, 1)
        



    #######################
    ###### SERVICE ########
    #######################    
    if kind == "kind: Service":
      service_count = service_count + 1
      svc_name, pod_label_list = YamlParser.GetServiceAndPodLabels(template, path)
      print("### SERVICE ###")
      graph_handler.add_edge(namespace, svc_name,1)
      for pod_label in pod_label_list:
        graph_handler.add_edge(svc_name, pod_label, 1)




    ##########################
    ### PERSISTENT VOLUME ####
    ##########################
    if kind == "kind: PersistentVolume":
      pv_count = pv_count +1
      pv_name = YamlParser.GetPersistentVolumeName(template, path)
      print("### PERSISTENT VOLUME ####")
      graph_handler.add_edge(namespace, pv_name, 1)



    ################################
    ### PERSISTENT VOLUME CLAIM ####
    ################################
    if kind == "kind: PersistentVolumeClaim":
      pvc_count = pvc_count +1
      pvc_name, pv_name = YamlParser.GetPvcNameAndPvName(template,path)
      print("### PERSISTENT VOLUME CLAIM ###")
      graph_handler.add_edge(namespace, pvc_name,1)
      graph_handler.add_edge(pvc_name, pv_name, 1)





    #######################
    #### ROLE BINDING #####
    #######################
    if kind == "kind: RoleBinding":
      rb_count = rb_count +1
      rb_name, role_name, users = YamlParser.GetRoleBindingNameRoleNameAndUsers(template,path)
      print("### ROLE BINDING, ROLE AND USERS ###")
      graph_handler.add_edge(namespace, rb_name,1)
      for user in users:
        graph_handler.add_edge(role_name, user,1)




    #############################
    ### CLUSTER ROLE BINDING ####
    #############################
    if kind == "kind: ClusterRoleBinding":
      crb_count = crb_count +1
      crb_name, crole_name, users = YamlParser.GetClusterRoleBindingNameClusterRoleNameAndUsers(template,path)
      print("### CLUSTER ROLE BINDING, CLUSTER ROLE AND USERS ###")
      graph_handler.add_edge(namespace, crb_name,1)
      for user in users:
        graph_handler.add_edge(crole_name, user,1)




    ############################
    ### POD SECURITY POLICY ####
    ############################
    if kind == "kind: PodSecurityPolicy":
      psp_count = psp_count +1
      psp_name = YamlParser.GetPodSecurityPolicyName(template, path)
      # IT IS A CLUSTER RESOURCE, so in theory it should not be added to namespace...
      print("### POD SECURITY POLICY ###")
      graph_handler.add_edge(namespace, psp_name, 1)




    #######################
    ### NETWORK POLICY ####
    #######################
    if kind == "kind: NetworkPolicy":
      np_count = np_count +1
      np_name, pod_label_list, ingress_list, egress_list = YamlParser.GetNetworkPolicyNameAndAssociations(template, path)
      print("### NETWORK POLICY ###")
      graph_handler.add_edge(namespace, np_name,1)
      graph_handler.add_edge(np_name,1 )
      
      for pod_label in pod_label_list:
        graph_handler.add_edge(np_name, pod_label,1)

        for ingress_rule in ingress_list:
          graph_handler.add_edge(pod_label, ingress_rule,1)   

        for egress_rule in egress_list:
          graph_handler.add_edge(pod_label, egress_rule,1)
      
      for pod_label in pod_label_list:
        print(pod_label)


 
  # Print the Graph status
  print("#########################################")
  print("############# GRAPH STATUS ##############")
  print("#########################################")
  graph_handler.print_edge_list()

  print("#########################################")
  print("################ COUNT ##################")
  print("#########################################")
  print("kind: Pod: " + str(pod_count))
  print("kind: Deployment: " + str(deployment_count))
  print("kind: Service: " + str(service_count))
  print("kind: PersistentVolumeClaim: " + str(pvc_count))
  print("kind: RoleBinding: " + str(rb_count))
  print("kind: ClusterRoleBinding: " + str(crb_count))
  print("kind: PodSecurityPolicy: " + str(psp_count))
  print("kind: NetworkPolicy: " + str(np_count))
  print("kind: PersistentVolume: " + str(pv_count))

  
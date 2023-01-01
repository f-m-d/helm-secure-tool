from test import Helm
from sys import argv

if __name__ == "__main__":

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

  
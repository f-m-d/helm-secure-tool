import subprocess


class Helm:

    def GetHelmTemplateCommandOutputFile(path):
      # Get the command output to a file
      results = subprocess.run(["helm", "template", path], stdout=subprocess.PIPE)
      output_to_write = results.stdout.decode('utf-8')
      #print(results.stdout)

      # Write output to a file
      f = open(path + "\\"+ "demo-file.txt", "w")
      f.write(output_to_write)
      f.close

      return (path + "\\"+ "demo-file.txt")

    
    # Path to the temporary file "demo-file.txt"
    # NB: start reading from the bottom
    # NBB: use read().splitlines() to avoid "\n" chars
    def GetHelmTemplateListFromFile(path):
      f = open(path)
      lines = f.read().splitlines()
      f.close()


      # Base: Nothing to the first "---" found, starting from the latest line
      # General Case: from "---" to the next "---" is a kind
      # Last case: from "---" to first line

      base_case = True
      latest_three_signs = 0
      file_list = []


    # Index of the last element in a list: a.index(a[-1])

      # Base case
      for index, line in reversed(list(enumerate(lines))):

        # General case
        if line == "---" and base_case == False:
          #print(index, line)
          file_template = lines[index+1:latest_three_signs]
          file_list.append(file_template)
          latest_three_signs = index


        if line == "---" and base_case == True:
          #print(index, line)
          base_case = False
          latest_three_signs = index
          file_template = lines[index+1:lines.index(lines[-1])]
          file_list.append(file_template)

      return file_list


      
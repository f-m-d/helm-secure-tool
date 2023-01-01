import subprocess


class Helm:

    def GetHelmTemplateCommandOutputFile(path):
      # Get the command output to a file
      results = subprocess.run(["helm", "template", path], stdout=subprocess.PIPE)
      output_to_write = results.stdout.decode('utf-8')
      #print(results.stdout)

      # Write output to a file
      f = open(path + "\\"+ "demo-file.txt", "a")
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

      # From the end
      for index, line in reversed(list(enumerate(lines))):
        #print(line)
        if line == "---":
          print(index, line)
      
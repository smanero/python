import os

class File:
   def __init__(self, name : str, path : str):
      self.file = None
      self.name = name
      self.path = path

   def open(self):
      """ 
      r - Read - Default value. Opens a file for reading, error if the file does not exist
      a - Append - Opens a file for appending, creates the file if it does not exist
      w - Write - Opens a file for writing, creates the file if it does not exist
      x - Create - Creates the specified file, returns an error if the file exists
      In addition you can specify if the file should be handled as binary or text mode
      t - Text - Default value. Text mode
      b - Binary - Binary mode (e.g. images)
      """
      if os.path.exists(self.path):
         self.file = open(self.path, 'rt')
      else:
         self.file = open(self.path, 'wt')

   def read(self):
      line : str
      line = self.file.readline()
      print(line)

   def write(self, lines : str):
      self.file.writelines(lines)

   def delete(self):
      if os.path.exists(self.path):
         os.remove(self.path) 
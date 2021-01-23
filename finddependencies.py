import re
state =False
filename = "build.gradle"
pattern_depend_beging = re.compile(r"dependencies {", re.IGNORECASE)
pattern_extend_beging = re.compile(r"ext.deps", re.IGNORECASE)
pattern_depend_end =re.compile(r"}", re.IGNORECASE)
pattern_extend_end =re.compile(r"]", re.IGNORECASE)

with open(filename, "rt") as in_file:
 for line in in_file:
  if pattern_depend_beging.search(line) != None:
      state = True
    #   print(line, end='')
  if pattern_depend_end.search(line) !=None:
      state = False
  if pattern_depend_beging.search(line) == None:
     if(state):
        print(line)
     



##  if ( (state)) :
#     print(line, end='')
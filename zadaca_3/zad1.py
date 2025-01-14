class Parser:
    def _parseLine(self, line, n):
        l = line.split("//")[0].split()
        if len(l) == 0 or len(l[0]) == 0:
            return ""
    
        if l[0] == "push":
            if len(l) == 3:
                return "//" + " ".join(l) + "\n" + self._push(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined command");
                return ""
    
        elif l[0] == "pop":
            if len(l) == 3:
                return "//" + " ".join(l) + "\n" + self._pop(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined command");
                return ""
        # ZADATAK 1
        elif line[0] == "@" and line[1] in "0123456789": 
            if int(line[1:]) > 32768 or int(line[1:]) < 0:
                self._flag = False
                Parser._error("Parser", n, "Invalid memory location.")
                return ""
            
        elif len(l) == 1:
            return "//" + " ".join(l) + "\n" + self._comm(l[0], n)
    
        return ""
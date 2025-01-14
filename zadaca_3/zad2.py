import re
class Parser:
    def _parseLine(self, line, n): 
        l = line.split("//")[0].strip()  
        if not l:
            return ""

        if l.startswith("$"):  
            try:
                if l.startswith("$MV"):
                    A, B = self._extractArgs(l, 2)
                    return self._mv(A, B)
                elif l.startswith("$SWP"):
                    A, B = self._extractArgs(l, 2)
                    return self._swp(A, B)
                elif l.startswith("$ADD"):
                    A, B, D = self._extractArgs(l, 3)
                    return self._add(A, B, D)
                elif l.startswith("$WHILE"):
                    A = self._extractArgs(l, 1)
                    return self._while(A)
                elif l == "$END":
                    return self._end()
                else:
                    self._flag = False
                    self._error("Parser", n, f"Nepoznat macro: {l}")
                    return ""
            except ValueError as e:
                self._flag = False
                self._error("Parser", n, str(e))
                return ""


    def _mv(self, A, B):
        return (f"@{A}\nD=M\n@{B}\nM=D\n")

    def _swp(self, A, B):
        return (f"@{A}\nD=M\n@TEMP\nM=D\n"
                f"@{B}\nD=M\n@{A}\nM=D\n"
                f"@TEMP\nD=M\n@{B}\nM=D\n")

    def _add(self, A, B, D):
        return (f"@{A}\nD=M\n@{B}\nD=D+M\n"
                f"@{D}\nM=D\n")


    def _while(self, A):
        self._nest += 1
        label = f"WHILE{self._nest}"
        end_label = f"END{self._nest}"
    
        lines = [
            f"({label})",
            f"@{A}",
            "D=M",
            f"@{end_label}",
            "D;JEQ"
        ]
        return "\n".join(lines) + "\n"


    def _end(self):
        if self._lab == 0:
            self._flag = False
            raise ValueError("Postoji $END bez $WHILE")
        label = f"WHILE_{self._lab - 1}"
        return (f"@{label}\n0;JMP\n"
                f"(END_{label})\n")
    
    def _extractArgs(self, command, num_args):
        # regex za naredbe koje pocinju s $
        match = re.match(r"\$\w+\(([^)]+)\)", command)
        if not match:
            raise ValueError("Nepravila sintaksa. Naredba treba izgledati: $COMMAND(A, B, ...)")
        
        args = [arg.strip() for arg in match.group(1).split(",")]
        
        if len(args) != num_args:
            raise ValueError(f"Ocekivano {num_args} argumenata, dobiveno {len(args)}.")
        
        return args


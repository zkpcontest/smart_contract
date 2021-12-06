import subprocess
import platform

class zkp:

    def __init__(self,folder="bin"):
        self.folder = folder

    def get_bin(self):
        return f"""cli_{platform.system().lower()}_{platform.machine().lower()}{".exe" if platform.system().lower() == "windows" else ""}"""

    def vote(self,num):
        # with open("p_key","wb") as f:
        #     f.write(bytes.fromhex(proof_key + "01"))
        result = subprocess.check_output([f'./{self.folder}/{self.get_bin()}', '--proof','--ballot_number',str(num)])

        r = result.decode("utf-8")
        ballout = int(r.split("Ballot_open:")[1].split("\nMarshalling types filled.")[0])

        with open("proof","rb") as f:
            pro = f.read().hex()
        
        # with open("viout","rb") as f:
        #     pro = f.read().hex()
        return pro, ballout
    
    def create(self):
        result = subprocess.call([f'./{self.folder}/{self.get_bin()}', '--setup','--ballot_number',str(1)])
        with open("v_key","rb") as f:
            ver_key = (f.read().hex())
        with open("p_key","rb") as f:
            proof_key = (f.read().hex())
        return ver_key,proof_key
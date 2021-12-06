import rsa
import freeton, zkp
from random import randint
import time
import os,binascii

def fun(a):
    return a * a * a + a

fr = freeton.wrapper()
zkp = zkp.zkp()
def generate_values():
    v = randint(1,1290)
    print(f"Private: {v}\nPublic: {fun(v)}") # NOT READY FOR PRODUCTION
    # BAD DOCUMENTATION

def new_vote():
    
    input_ballot = []
    # q = bool(input("Test? (0/1): "))
    t = int(input(f"What time in seconds will the vote be valid? (Now is {int(time.time())}, 1 week {int(time.time()) + 60 * 60 * 24 * 7}): "))
    while True:
        count = int(input("How many voters?: "))
        if count < 0 or count > 100:
            print("Try again")
        else:
            break
    print("Write down answers by the line")
    for i in range(count):
        input_ballot.append(int(input()))
    count_answers = int(input("How many votes?: "))
    print("Write down answers by the line")
    answers = []
    for i in range(count_answers):
        answers.append(input().encode("utf-8").hex())
    print("Creating new key")
    ver_key,proof_key = zkp.create()
    (pubkey, privkey) = rsa.newkeys(512)
    print("Save key")
    with open("pubkey.pem","wb") as f:
        f.write(pubkey.save_pkcs1(format="PEM"))
    with open("privkey.pem","wb") as f:
        f.write(privkey.save_pkcs1(format="PEM"))
    
    data = fr.tvm_hash(privkey.save_pkcs1(format="DER"))
    print(data)
    result, adr = fr.create_vote(pubkey.save_pkcs1(format="DER"),data,input_ballot,t,ver_key,proof_key,answers)
    op = fr.get_open_key(adr)
    o_t = rsa.key.PublicKey.load_pkcs1(op, "DER")
    if o_t != pubkey:
        print("Something go wrong. Write to developer pls")
        return None

    print("""
    All is ok""")

    print("After ending of time you need Finish vote")
    print(f"Here an address: {adr}")
    print("\nSAVE A p_key AND privkey.pem")
    print("SEND p_key to voters")
    print("privkey.pem WILL BE USED FOR DECRYPTION VOTES")


def finish_vote():
    print("Upload private key to blockchain")
    adr = input("Address of vote: ")
    with open("privkey.pem","rb") as f:
        priv = rsa.key.PrivateKey.load_pkcs1(f.read(), "PEM")
    # data = fr.tvm_hash(priv.save_pkcs1(format="DER"))
    # print(data)
    fr.finish_vote(adr,priv.save_pkcs1(format="DER"))


def vote():
    print("Lets vote")
    input("Copy p_key to this folder")
    adr = input("Address of vote: ")
    v = input("Vote: ")
    ballot_number = input("Ballot number: ")
    op = fr.get_open_key(adr)
    o_t = rsa.key.PublicKey.load_pkcs1(op, "DER")
    salt1 = binascii.b2a_hex(os.urandom(3)).decode("utf-8")
    salt2 = binascii.b2a_hex(os.urandom(3)).decode("utf-8")
    message = rsa.encrypt(f"{salt1}{v}{salt2}".encode("utf-8"), o_t)
    pro, ballout = zkp.vote(ballot_number)
    fr.vote(adr,pro,ballot_number,message)

def check_votes():
    print("Good news")
    print("Lets decrypt votes")
    adr = input("Address of vote: ")
    priv = rsa.key.PrivateKey.load_pkcs1(fr.get_private_key(adr), "DER")
    answers = fr.get_answers(adr)
    answers_str = []
    for i in answers:
        answers_str.append(bytes.fromhex(i).decode("utf-8"))
    good = 0
    bad = 0
    result = {}
    for i in fr.get_votes(adr):
        try:
            a = rsa.decrypt(bytes.fromhex(i), priv)
            
            r = a[6:-6].decode("utf-8")
            for i in r.split("|"):
                if not i in answers_str:
                    raise Exception("Bad vote") 
            for i in r.split("|"):
                try:
                    result[i] += 1
                except:
                    result[i] = 1 
            good += 1
        except:
            bad += 1
    print(f"\nResult: {result}")
    print(f"\nGood: {good} {'votes' if good > 1 else 'vote'}\nBad: {bad} {'votes' if bad > 1 else 'vote'}\n")

    
    


def main():
    while True:
        print("""Hello there

        Lets start a new vote
        0. Create public value
        1. Create new vote
        2. Vote
        3. Finish vote
        4. Check results
        5. Exit
        """)
        i = input("Choose: ")
        if i == "0":
            generate_values()
        elif i == "1":
            new_vote()
        elif i == "2":
            vote()
        elif i == "3":
            finish_vote()
        elif i == "4":
            check_votes()
        elif i == "5":
            break

        else:
            print("Something go wrong")

if __name__ == "__main__":
    main()
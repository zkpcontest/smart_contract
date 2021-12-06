import tonos_ts4.ts4 as ts4
import unittest
import time

EXCHANGER_COMMISSION = 3

class key:
    secret: str
    public: str
class TestPair(unittest.TestCase):
    secret = "bc891ad1f7dc0705db795a81761cf7ea0b74c9c2a93cbf9ac1bad8bd30c9b3b75a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    public = "0x5a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    def test_exchanger(self):
        ts4.reset_all() # reset all data
        ts4.init('./', verbose = True)
        key1 = ts4.make_keypair()
        self.public1 = key1[1]
        self.secret1 = key1[0]
        # Prepare controllers 
        main = ts4.BaseContract('main',dict(),pubkey=self.public,private_key=self.secret,balance=150_000_000_000,nickname="Controller0")
        main.call_method("vote",dict(proof=ts4.Bytes("9834cc78fc6cd92e937c42d339b55a710367ed1a2cd23270c76dd32497a95780ad0ed19d33136dc79a601c4421874ae3b881392299a201eab4f7784f6ca221aec16570a98a4747cb8a450c2eedc87a0b2c8db32b508c0a015dcad64d76387181126fbdd4956329982b464aa017022c7144e01441ab63be7eb98e98e8c8663b9c82b1b28640d2911252aaeefaeebf601e8c5358c202373b678bb6eb0616a56621a3be176aa47f810d1ca62383d53f6d72a76077214e151480e454431f35ce8125%"),
        ballot_number=2147441945))


if __name__ == '__main__':
    unittest.main()

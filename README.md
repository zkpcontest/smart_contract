# smart_contract
https://vimeo.com/653723583
@Blackjack_and_code

Before voting (by voter)

    •  Generate voter’s secret key (sk) on voter’s side
    
    •  Generate voter’s public key (pk) on voter’s side, e.g. pk = H(sk), where H - some irreversible function


Create voting (by administrator)

    •  Generate RSA keypair for encrypt/decrypt vote results
    
    •  Generate ZKP proof and verify keys
    
    •  Collect in some way public keys (pk) from all voters
    
    •  Prepare available answers and voting end time
    
    •  Deploy voting contract with arguments:
    
        ✓  _open: RSA public key for encrypting answer
        
        ✓  _hash_private: RSA private key hash
        
        ✓  _ballot_numbers: List of voters’ public keys
        
        ✓  _time_limit: Unixtime the voting is active for
        
        ✓  _m_vkey: ZKP verifying key
        
        ✓  _m_pkey: ZKP proof key
        
        ✓  _available_choose: Available answers to choose


Voting (by voter)

     •  Request proof key (p_key) from vote creator (administrator)
     
     •  Generate ZKP proof from requested p_key and voters's secret key (sk)
     
     •  Encrypt chosen answer with RSA public key (can be read from vote contract)
     
     •  Send message to vote contract with arguments:
     
         ✓  proof: Generated proof data
         
         ✓  ballot_number: Voter’s secret key (sk)
         
         ✓  vote: RSA encrypted answer


Finishing the vote (by administrator)
    •  Call vote contract finish method and pass RSA secret key to allow answers decryption

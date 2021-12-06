
pragma ton-solidity >= 0.35.0;
pragma AbiHeader expire;

// This is class that describes you smart contract.
contract main {
    // Contract can have an instance variables.
    // In this example instance variable `timestamp` is used to store the time of `constructor` or `touch`
    // function call
    bytes public m_vkey;
    bytes public m_pkey;
    // uint32 constant PI_SIZE = 13;
    enum state {doesntExist, NotVote, Voted}
    // uint32 public timestamp;
        // You should change/add/remove arguments according to your circuit.
    uint32 constant PI_SIZE = 1; //change that
    uint8 constant field_element_bytes = 32;
    uint256 public hash_private;
    bytes public private_key;
    bytes public open;
    bool public status;
    uint64 public time_limit;
    mapping(uint256=>state) public ballot_numbers_state;
    bytes[] public votes;
    bytes[] public available_choose;
    // uint32[] public ballot_numbers;
    // Contract can have a `constructor` – function that will be called when contract will be deployed to the blockchain.
    // In this example constructor adds current time to the instance variable.
    // All contracts need call tvm.accept(); for succeeded deploy
    constructor(bytes _open,uint256 _hash_private, uint256[] _ballot_numbers, uint64 _time_limit, bytes _m_vkey, bytes _m_pkey, bytes[] _available_choose) public {
        // Check that contract's public key is set
        require(tvm.pubkey() != 0, 101);
        require(_time_limit > now, 103,"time too small");
        // Check that message has signature (msg.pubkey() is not zero) and
        // message is signed with the owner's private key
        require(msg.pubkey() == tvm.pubkey(), 102);
        // The current smart contract agrees to buy some gas to finish the
        // current transaction. This actions required to process external
        // messages, which bring no value (henceno gas) with themselves.
        tvm.accept();
        status = true;
        hash_private = _hash_private;
        open = _open;
        for (uint256 i = 0; i < _ballot_numbers.length; i++) {
            ballot_numbers_state[_ballot_numbers[i]] = state.NotVote;
        }
        time_limit = _time_limit;
        m_vkey = _m_vkey;
        m_pkey = _m_pkey;
        available_choose = _available_choose;

    }

    function finish_vote(bytes _private) public {
        require(time_limit > now,103,"too early");
        require(status,105,"you already share private");
        require(tvm.hash(_private) == hash_private,104,"bad private");
        tvm.accept();
        status = false;
        private_key = _private;
    }


    function r(uint256 num) private returns (uint256 result) {
        return num * num * num + num;
    }

    function vote(bytes proof,
                    uint256 ballot_number, bytes vote) public{
        require(time_limit > now,103,"time is over");
        require(ballot_numbers_state[r(ballot_number)] == state.NotVote,106,"you already vote");
        require(proof.length == 192, 109, "not valid proof");
        tvm.accept(); // beacause tvm vergrth16 too big to run it in gas credit
        proof.append(serialize_primary_input(ballot_number));
        proof.append(m_vkey);
        require(tvm.vergrth16(proof));
        ballot_numbers_state[r(ballot_number)] = state.Voted;
        votes.push(vote);
        //return r(ballot_number);
        // return proof;
        
    }

    function serialize_primary_input(uint256 some_number) internal inline view returns(bytes) {
        string blob_str=uint32_to_bytes(1);
        blob_str.append(uint256_to_bytes(some_number));
        return blob_str;
    }

    function encode_little_endian(uint256 number, uint32 bytes_size) internal pure returns (bytes){
        TvmBuilder ref_builder;
        for(uint32 i=0; i<bytes_size; ++i) {
            ref_builder.store(byte(uint8(number & 0xFF)));
            number>>=8;
        }
        TvmBuilder builder;
        builder.storeRef(ref_builder.toCell());
        return builder.toSlice().decode(bytes);
    }

    function uint256_to_bytes(uint256 number) internal pure returns (bytes){
        TvmBuilder ref_builder;
        ref_builder.store(bytes32(number));
        TvmBuilder builder;
        builder.storeRef(ref_builder.toCell());
        return builder.toSlice().decode(bytes);
    }
    function uint32_to_bytes(uint64 number) internal pure returns (bytes){
        TvmBuilder ref_builder;
        ref_builder.store(bytes8(number));
        TvmBuilder builder;
        builder.storeRef(ref_builder.toCell());
        return builder.toSlice().decode(bytes);
    }
}
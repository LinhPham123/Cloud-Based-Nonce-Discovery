import hashlib
import pickle
import timeit
import sys


def main(start_nonce, number_of_VMs, difficulty_level):
    #Set up, convert to byte and hash
    difficulty = setUpDifficulty(difficulty_level)

    start_time = timeit.default_timer()
    golden_nonce, digest = mining(start_nonce, difficulty, number_of_VMs)
    elapsed = timeit.default_timer() - start_time

    print('Time taken: %.5f and Golden_nonce is: %d' % (elapsed, golden_nonce))
    print('Digest is: %s' % str(digest))
    

def setUpDifficulty(difficulty_level):
    default = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    return (default >> difficulty_level * 4)


def mining(start_nonce, difficulty, jump_distance):
    block = {
        'data': 'COMSM0010cloud',
        'nonce': start_nonce
    }
    block_byte = pickle.dumps(block)
    digest = hashlib.sha256(block_byte).hexdigest()
    while int(digest, 16) >= difficulty:      
        block['nonce'] = block['nonce'] + jump_distance
        digest = hashlib.sha256(pickle.dumps(block)).hexdigest()
    
    return block['nonce'], digest


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
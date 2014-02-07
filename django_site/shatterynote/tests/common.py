


def flip_bits(a):
    """Flip all bits in the given byte string"""
    return b''.join([int.to_bytes(x^255, 1, 'big') for x in a])

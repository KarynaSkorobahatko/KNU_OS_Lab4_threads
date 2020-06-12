import numpy as np
from numpy.testing import assert_array_equal
import threading
from time import time
from multiprocessing import Process


def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    n, m = h // nrows, w // ncols
    return arr.reshape(nrows, n, ncols, m).swapaxes(1, 2)


def do_dot(a, b, out):
    import time
    import random
    time.sleep(random.randint(0, 2))
    out[:] = np.dot(a, b)
    print(out[0][0])


def pardot(a, b, nblocks, mblocks, dot_func=do_dot):
    n_jobs = nblocks * mblocks
    print('running {} jobs in parallel'.format(n_jobs))

    out = np.empty((a.shape[0], b.shape[1]), dtype=a.dtype)

    out_blocks = blockshaped(out, nblocks, mblocks)
    a_blocks = blockshaped(a, nblocks, 1)
    b_blocks = blockshaped(b, 1, mblocks)

    threads = []
    for i in range(nblocks):
        for j in range(mblocks):
            th = threading.Thread(target=dot_func,
                                  args=(a_blocks[i, 0, :, :],
                                        b_blocks[0, j, :, :],
                                        out_blocks[i, j, :, :]))
            th.start()
            threads.append(th)

    for th in threads:
        th.join()

    return out


if __name__ == '__main__':
    a = np.random.randn(10, 10).astype(int)
    # a = np.array([[1,1,1],[1,1,1],[1,1,1]])
    print(a)
    print(pardot(a, a, 10, 10))
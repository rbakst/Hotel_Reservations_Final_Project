# I didn't test out this code

from concurrent.futures import ProcessPoolExecutor
import functools


def map_reduce(object, num_processes, mapper, reducer, *map_args):
    chunks = chunk(object, num_processes)
    processes = []
    with ProcessPoolExecutor() as exe:
        for chunk in chunks:
            processes = [exe.submit(mapper, chunk, *map_args) for chunk in chunks]

    results = [process.result() for process in processes]
    return functools.reduce(results, reducer)


def chunk(object, num_chunks):
    num_rows = len(object)
    return [object[i:i + num_chunks] for i in range(0, num_rows, num_chunks)]

    # Alternative solution
    # num_rows = len(object)
    # num_chunks = math.ceil(num_rows / num_chunks)

    # chunks = []
    # for i in range(0, num_rows, num_chunks):
    #     chunk = object[i:i + num_chunks]
    #     chunks.append(chunk)
    
    # return chunks
from lambda_multiprocessing import Pool

def work(x):
    return x*x

with Pool() as p:
    results = p.map(work, range(5))
assert results == [x*x for x in range(5)]
import multiprocessing

def write_pipe(pipe):
    print("write pipe started")
    p, _ = pipe
    for i in range(20):
        print("sending ", i)
        p.send(i)
    p.close()


def read_pipe(pipe):
    out, p = pipe
    out.close()
    try:
        while True:
            item = p.recv()
            print("recieved ", item)
    except EOFError:
        p.close()

if __name__ == '__main__':
    pipe = multiprocessing.Pipe(True)

    p1 = multiprocessing.Process(target=write_pipe, args=(pipe,))
    p2 = multiprocessing.Process(target=read_pipe, args=(pipe,))

    p1.start()
    p2.start()

    pipe[0].close()

    p1.join()
    p2.join()
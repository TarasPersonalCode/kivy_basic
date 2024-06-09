
class NetworkFileReceiver:
    def __init__(self, network_manager, filename, batch_size):
        self.nm         = network_manager
        self.filename   = filename
        self.batch_size = batch_size
        open(filename, 'wb').close()
        self.filesize = None
        self.num_receptions = 0

    def receive_batch(self):
        if self.filesize is None:
            self.filesize = self.nm.recv()
        batch_ctr = self.batch_size
        while self.filesize > 0 and batch_ctr > 0:
            with open(self.filename, 'ab') as f:
                chunk = self.nm.sock.recv(self.nm.buff_size)
                f.write(chunk)
                self.filesize -= len(chunk)
                if self.num_receptions % 20 == 0:
                    print(f'{self.filesize=}')
            batch_ctr -= 1 
        self.num_receptions += 1
        return self.filesize != 0

    def receive_all(self):
        if self.filesize is None:
            self.receive_batch()
        while self.filesize > 0:
            self.receive_batch()

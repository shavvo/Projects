from swiftly.client.directclient import DirectClient


import json
from Queue import Queue
from threading import Thread
import time


"""
10k objects:
Time to run: ~40 seconds
File sizes: X2 as there are two files
Total size: ~855K each
Memory: ~67368kb

1 Million:
Time: 1.2 Hours
Size: 83.5M
Memory: ~6.73 gb

10 Million:
Time: 11.1 Hours
Size: 0.82G
Memory: ~67.36 gb

100 Million:
Time: 4.62 Days
Size: 8.15G
Memory: ~673.68 gb
"""

acc_file = '/home/aballens/random/accounts'
q = Queue(maxsize=0)

class SwiftResponse(object):
    def __init__(self, response):
        self.status = int(response[0])
        self.reason = str(response[1]).lower()
        self.headers = response[2]
        self.contents = response[3]

    def content_list(self):
        temp_contents = []
        for item in self.contents:
            if item.get('name') not in temp_contents:
                temp_contents.append(item.get('name'))

        return temp_contents

    def get_header_key(self, key):
        return self.headers.get(key)


def connect_to_swift(account):
    return DirectClient(swift_proxy_storage_path=account)


def get_account_containers(client, account):
    print "in get containers"
    total_containers = None
    containers = []
    marker = None
    exit = False
    while exit is False:
        if marker is None:
            response = SwiftResponse(client.get_account())
        else:
            response = SwiftResponse(client.get_account(marker=marker))

        if total_containers is None:
            total_containers = response.get_header_key(
                'x-account-container-count'
            )

        if response.status == 200:
            containers += response.content_list()

        if len(containers) < int(total_containers):
            print('Gathering more containers...')
            marker = containers[-1]
        else:
            exit = True

    return containers


def get_container_objects(client, container):
    total_objects = None
    objects = []
    marker = None
    exit = False
    while exit is False:
        if marker is None:
            response = SwiftResponse(client.get_container(container))
        else:
            response = SwiftResponse(
                client.get_container(
                    container,
                    marker=marker
                )
            )

        if total_objects is None:
            total_objects = response.get_header_key(
                'x-container-object-count'
            )

        if response.status == 200:
            objects += response.content_list()

        if len(objects) < int(total_objects):
            print('Gathering more objects...')
            marker = objects[-1]
        else:
            exit = True

    return objects


def check_object(client, container, cont_object):
    response = SwiftResponse(client.head_object(container, cont_object))
    if response.status == 200:
        return True

    return False


def account_queue(acct_file):
    with open(acct_file) as f:
        for line in f:
            line = line.strip().strip('"')
           # print line
            q.put(line)
        #print q.qsize()

def processQueue(q):
    #accounts = []
    #jd_acc_file = raw_input('File: ')
    client = None
    # Edit to allow for multiple accounts. -Shavvo
    #with open('/home/aballens/jungle_heads/jd_processes/{0}'.format(jd_acc_file)) as f:
    #    for item in f:
    #        accounts.append('/v1/{0}'.format(item.strip().strip('"')))


    with open('object_failures.txt', 'a+') as f:
        while True:
            try:
                print q.qsize()
                account = '/v1/{0}'.format(q.get())
                print account
                print('Initializing variables for account {0}'.format(account))
                containers = []
                container_objects = []

                if client is not None:
                    client.reset()

                print('Connecting to swift')
                client = connect_to_swift(account)

                print('Getting account containers')
                containers = get_account_containers(client, account)
                print "printing stuff {0}".format(containers)
                for container in containers:
                    print('Gathering objects for {0}'.format(container))
                    container_objects = get_container_objects(client, container)

                    print('Checking objects for availability')
                    for item in container_objects:
                        success = check_object(client, container, item)
                        if not success:
                            f.write(
                                '{0},{1},{2}\n'.format(
                                    account,
                                    container,
                                    item
                                )
                            )
                        # Edit to log successes -Shavvo
                        else:
                            try:
                                with open('success.log', 'a+') as g:
                                    g.write('{0} - {1} - {2} - {3} \n'.format(account,
                                                                              container,
                                                                              item,
                                                                              success))
                            except UnicodeEncodeError:
                                pass

                    print('Completed object checks')
                    q.task_done()
            except TypeError as e:
                print e
                q.task_done()
                continue


    if client is not None:
        client.reset()


def main():
    account_queue(acc_file)

    thread_num = 10

    for i in range(thread_num):
        worker = Thread(target=processQueue, args=(q,))
        worker.setDaemon(True)
        worker.start()
    q.join()


if __name__ == '__main__':
    main()

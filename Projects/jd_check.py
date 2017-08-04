from swiftly.client.directclient import DirectClient


import json
from Queue import Queue
from threading import Thread
import time
import logging
import os


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

acc_file = '/home/aballens/jungle_heads/jd_accounts'
res_dir = '/home/aballens/jungle_heads/position'
logfile = '/home/aballens/jungle_heads/logs/jungle.log'
q = Queue(maxsize=0)
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')



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
                'x-account-container-count')

        if response.status == 200:
            containers += response.content_list()

        if len(containers) < int(total_containers):
            print('Gathering more containers...')
            marker = containers[-1]
        else:
            exit = True

    return containers


#def get_container_objects(client, container): #marker
#    total_objects = None
#    objects = []
#    marker = None # remove
#    exit = False
#    while exit is False:
#        if marker is None:
#            response = SwiftResponse(client.get_container(container))
#        else:
#            response = SwiftResponse(
#                client.get_container(
#                    container,
#                    marker=marker
#                )
#            )
#
#        if total_objects is None:
#            total_objects = response.get_header_key(
#                'x-container-object-count'
#            )
#
#        if response.status == 200:
#            #objects += response.content_list()
#            for obj in response.content_list():
#                yield obj
#
#        if len(objects) < int(total_objects):
#            print('Gathering more objects...{0} - {1}'.format(container, len(objects)))
#            marker = objects[-1]
#        else:
#            exit = True
#
#    return objects


def get_container_objects(client, container):
    marker = None
    while True:
        response = SwiftResponse(client.get_container(container,
                                                      marker=marker))

        if response.status == 200:
            done = True
            for obj in response.content_list():
                done = False
                marker = obj
                yield obj
            if done:
                break
        else:
            print 'Invalid response {0}'.format(response_status)
            break


def check_object(client, container, cont_object):
    response = SwiftResponse(client.head_object(container, cont_object))
    if response.status == 200:
        return True

    return False


def account_queue(acct_file):
    with open(acct_file) as f:
        for line in f:
            line = line.strip().strip('"')
            q.put(line)


def resume_queue():
    resume_list = []
    if os.listdir(res_dir):
       for elem in os.listdir(res_dir):
           with open('{0}/{1}'.format(res_dir, elem)) as f:
               data = json.load(f)
               resume_list.append(data)
    return resume_list

def processQueue(q):
    client = None
    pos = {'Account': '', 'Container': '', 'Object':''}
    count = 0
    while True:
        try:
            account = q.get()
            print('Initializing variables for account {0}'.format(account))
            containers = []
            container_objects = []

            if client is not None:
                client.reset()

            print('Connecting to swift')
            client = connect_to_swift('/v1/{0}'.format(account))

            print('Getting account containers')
            containers = get_account_containers(client, account)
            print 'Containers list {0}'.format(containers)
            for container in containers:
                fname = '/home/aballens/jungle_heads/position/{0}_{1}'.format(account,container)
                #print('Gathering objects for {0}'.format(container))
                #container_objects = get_container_objects(client, container)
                #with open('/home/aballens/jungle_heads{0}_{1}'.format(account, container), 'w+') as f:

                print('Checking objects for availability {0}'.format(container))
                #for item in container_objects:
                succ = 0
                fail = 0
                for item in get_container_objects(client, container):
                    success = check_object(client, container, item)
                    if not success:
                        fail += 1
                        logging.warning('{0} - {1} - {2} - {3}'.format(account,
                                                                       container,
                                                                       item,
                                                                       success))
                    else:
                        try:
                            succ += 1
                            logging.info('{0} - {1} - {2} - {3}'.format(account,
                                                                        container,
                                                                        item,
                                                                        success))
                        except UnicodeEncodeError:
                            pass
                    count += 1
                    if count % 1000 == 0:
                        print count
                        pos['Account'] = account
                        pos['Container'] = container
                        pos['Object'] = item
                        pos['Success'] = succ
                        pos['Failures'] = fail
                        with open(fname, 'w') as f:
                            json.dump(pos, f)
                print('Completed object checks {0}'.format(container))
            q.task_done()
        except TypeError as e:
            print e
            q.task_done()
            continue


    if client is not None:
        client.reset()


def main():
    account_queue(acc_file)

    thread_num = 20

    for i in range(thread_num):
        worker = Thread(target=processQueue, args=(q,))
        worker.setDaemon(True)
        worker.start()
    q.join()


if __name__ == '__main__':
    main()

#/usr/bin/python

from swiftly.client.directclient import DirectClient
import json

available_commands = ['get_container', 'get_account','head_container',
                     'head_account', 'head_object']


def head_obj(account, container, c_object):
    client = DirectClient(swift_proxy_storage_path=account)
    data = client.head_object(container, c_object)
    for key, value in data[2].iteritems():
        print (key, value)

    print (data[0], data[1])


def head_contain(account, container):
    client = DirectClient(swift_proxy_storage_path=account)
    data = client.head_container(container)
    for key, value in data[2].iteritems():
        print (key, value)

    print (data[0], data[1])


def head_acct(account):
    client = DirectClient(swift_proxy_storage_path=account)
    data = client.head_account()
    for key, value in data[2].iteritems():
        print (key, value)

    print (data[0], data[1])


def get_contain(account, container):
    output = raw_input('File to put results in: ')
    client = DirectClient(swift_proxy_storage_path=account)
    data = client.get_container(container)
    with open(output, 'w') as f:
        for line in data:
            json.dump(data, f, indent = 4)
    print "results should be in {0}".format(output)


def get_acct(account):
    output = raw_input('File to put results in: ')
    client = DirectClient(swift_proxy_storage_path=account)
    data = client.get_account()
    with open(output, 'w') as f:
        for line in data:
            json.dump(data, f, indent = 4)
    print 'results should be in {0}'.format(output)


def main():
    account = raw_input("Account? \"example /v1/MossoCloudFS_1234\": ")
    container = raw_input("Container?: ")
    c_object = raw_input("Object?: ")
    command = raw_input("What would you like to do? {0}:  ".format(available_commands))
    if command not in available_commands:
        print "Invalid command, use {0}".format(available_commands)
    if command == 'head_object':
        head_obj(account, container, c_object)
    if command == 'head_container':
        head_contain(account, container)
    if command == 'head_account':
        head_acct(account)
    if command == 'get_container':
        get_contain(account, container)
    if command == 'get_account':
        get_acct(account)



if __name__ == '__main__':
    main()

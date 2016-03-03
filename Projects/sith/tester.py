from hat import Cat
import mock

def fake_talk(*args):
    print 'mocked out'

def fake_talk_2(*args):
    print 'switched by me'

def main():
    c = Cat()
    c.talk()

    with mock.patch('hat.Cat.talk', fake_talk):
        #print "blah"
        c.talk()


    # this is what that is basically doing:
    #c.talk() # back to orig `talk`

    #was_talk_func = c.talk # keep track of `talk`

    #c.talk = fake_talk_2 # switch it out

    #c.talk() # call that object's `talk` method which is really calling fake_talk_2

    #c.talk = was_talk_func # put it back the way it was

    c.talk()


if __name__ == '__main__':
    main()

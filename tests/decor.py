__author__ = 'oshmuel'

def true_func():
    return True

def false_func():
    return False

def test_post_cond(test_func, action_func):
    # verify all *args are callable objects

    #if not all(map(lambda arg: hasattr(arg, '__call__'), args)):
    #    raise Exception("not all arguments *args are callable")

    def decorator(func):
        def test_conditions_and_execute(*args):
            func(*args)
            if test_func():
                action_func()

        return test_conditions_and_execute

    return decorator

def finalizeOnLastEvent():
    print "finalize"

release_if_last_event = test_post_cond(false_func, finalizeOnLastEvent)

@release_if_last_event
def OnResponse(a):
    if a == 'bla bla': print "AAAAAAAAAAA", a

if __name__ == '__main__':
    str = "bla bla"

    print
    print

    dir(OnResponse)

    OnResponse(str)

#    black_knight('1', '2')
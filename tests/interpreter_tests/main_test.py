__author__ = 'oshmuel'

import classes_test



def main():
    if not hasattr(classes_test, '__dict__'):
        print "error"
        exit(1)

    classes_test_dict = getattr(classes_test, '__dict__')

    http_attack_object = getattr(classes_test, "HttpAttack")
    if not http_attack_object:
        print "error"
        exit(1)

    for k, v in classes_test_dict.iteritems():
        #print "checking " + str(classes_test_dict[k])
        try:
            if issubclass(classes_test_dict[k], http_attack_object):
                print "true"
            else:
                print "false"
        except:
            pass




    print "OK"



if __name__ == '__main__':
    main()
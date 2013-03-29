import datetime
import requests


def add_event(ns):
    start = datetime.datetime.combine(ns.start_date, ns.start_time)
    end = datetime.datetime.combine(ns.end_date, ns.end_time)
    payload = {'tag': ns.tag,
               'author': ns.author,
               'start': str(start),
               'end': str(end),
               'description': ns.description}
    print requests.post("http://localhost:5000/add", data=payload)


def rm_event(event):
    print "Not implemented"


def mkdate(datestring):
    return datetime.datetime.strptime(datestring, '%Y-%m-%d').date()


def mktime(timestring):
    return datetime.datetime.strptime(timestring, '%H:%M:%S').time()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ThatWas client.')

    subparsers = parser.add_subparsers()

    now = datetime.datetime.utcnow()
    now = now.replace(second=0, microsecond=0)
    dait = str(now.date())
    tyme = str(now.time())
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('tag')
    parser_add.add_argument('--start_date', default=dait, type=mkdate,
                            help='YYYY-MM-DD (%s)' % dait)
    parser_add.add_argument('--start_time', default=tyme, type=mktime,
                            help='HH:MM:SS (%s)' % tyme)
    parser_add.add_argument('--end_date', default=dait, type=mkdate,
                            help='YYYY-MM-DD (%s)' % dait)
    parser_add.add_argument('--end_time', default=tyme, type=mktime,
                            help='HH:MM:SS (%s)' % tyme)
    parser_add.add_argument('description')
    parser_add.add_argument('author')
    parser_add.set_defaults(func=add_event)

    parser_rm = subparsers.add_parser('rm')
    parser_rm.add_argument('tag')
    parser_rm.set_defaults(func=rm_event)

    args = parser.parse_args()
    args.func(args)

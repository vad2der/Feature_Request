from models import RequestTicket, ClientName, ProductArea, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from datetime import datetime

# db config
engine = create_engine('sqlite:///request_tickets.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()


def create_tables():
    # table drop and creation
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_all():
    # get the
    return s.query(RequestTicket).all()


def insert_new(title, description, client, client_priority, target_date, url_root, product_area):
    ind = 0
    try:
        ind = int(s.query(func.max(RequestTicket.id)).scalar()) +1

    except Exception as e:
        ind += 1

    # instantiate a new object from mapped class
    rt = RequestTicket(ind=int(ind), title=str(title), description=str(description), client=client,
                       client_priority=int(client_priority), target_date=datetime.strptime(target_date, "%Y %m %d"),
                       ticket_url=url_root+'/request/'+str(ind), product_area=product_area)

    try:
        s.add(rt)
        s.commit()
    except Exception as e:
        s.rollback()


    # update the entry with ticket URL = "/ticket/" + entry.id


def check_priorities_EL(priority):
    """
    checks if there are any entries with equal of less priotiry
    :param priority:
    :return: list of id of the entries with equal or less priority
    """
    check = []
    for row in s.query(RequestTicket).filter(RequestTicket.client_priority >= priority).all():
        check.append(row.id)
    return check


def downgrade_priorities(entry_ids):
    """
    function requests entries with priorities and updating them assigning priotiries +1
    :param entry_ids:
    :return:
    """
    try:
        for idx in entry_ids:
            # got an entry by id
            entry = s.query(RequestTicket).filter(RequestTicket.id == idx).first()
            # assign entry's client_priority property
            p = int(entry.client_priority)
            # update the entry with incremented clients_priority
            s.query(RequestTicket).filter(RequestTicket.id == idx).update({"client_priority": p+1})
        s.commit()
    except Exception as e:
        s.rollback()

def get_possible_priorities():
    """
    :return: gathers all existing priorities and adds one more at the end
    """
    priority_list = []
    for p, in s.query(RequestTicket.client_priority).all():
        priority_list.append(p)
    # and the next one
    priority_list.append(priority_list[-1]+1)
    return priority_list

def get_gaps():
    """
    :return: a list with gaps in priorities
    """
    priority_list = []
    check_p = 1
    for p, in s.query(RequestTicket.client_priority).all():
        priority_list.append(p)
    priority_gap_list = []
    for check_p in range(1, priority_list[-1]):
        if check_p not in priority_list:
            priority_gap_list.append(check_p)
    return priority_gap_list

def eleminate_gaps(gap_list):
    """
    TODO: develop function to eleminate all gaps by updating priorities for existing entries
    :param gap_list:
    :return:
    """
    try:
        for g in gap_list:
            pass
        s.commit()
    except Exception as e:
        s.rollback()

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


def insert_new(title, description, client, client_priority, target_date, product_area):
    ind = 0
    try:
        ind = int(s.query(func.max(RequestTicket.id)).scalar()) +1

    except Exception as e:
        ind += 1

    # instantiate a new object from mapped class
    rt = RequestTicket(ind=int(ind), title=str(title), description=str(description), client=client,
                       client_priority=int(client_priority), target_date=datetime.strptime(target_date, "%Y %m %d"),
                       product_area=product_area)

    try:
        #TODO: develop check and priorities update
        # check if there are other priorities
        check = s.query(RequestTicket).filter(RequestTicket.client_priority >= rt.client_priority).all()
        if (check):
            downgrade_priorities(rt.client_priority)
        s.add(rt)
        s.commit()
    except Exception as e:
        s.rollback()

    # get id of the newly inserted entry
    # update the entry with ticket URL = "/ticket/" + entry.id


def downgrade_priorities(priority):
    #TODO: priorities update for the number of entries
    """
    function requests entries with priorities and updating them assigning priotiries +1
    :param priority:
    :return:
    """
    pass

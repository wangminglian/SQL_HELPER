# from .model import db, SQL_arg, Project_detail
from .model import db,SQL_arg,Project_detail

if __name__ == '__main__':
    db.connect()
    db.create_tables([SQL_arg,Project_detail])

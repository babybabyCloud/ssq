# encoding: utf-8

import os.path
from Spider.dboperator import new_session
from Spider .dboperator.model import *
from . import exporterfactory


def main(db_file, before, after, limit, table, out):
    tablecls = tablemapping[table]
    path = outpath(out, tablecls.__tablename__)
    ext = extension(path)
    session = new_session('sqlite:///%s' %db_file)
    try:
        query = session.query(tablecls).order_by(tablecls.id)
        # TODO: Fix filtering output
        data = [row.columns() for row in query.all()]
        exporterfactory[ext](path, tablecls.headers, data).export()
    finally:
        session.close()


def extension(path):
    _, ext = os.path.splitext(path)
    return ext


def outpath(out, table):
    ext = extension(out)
    if not ext:
        return os.path.join(os.path.abspath(out), '%s.csv') %table
    return out
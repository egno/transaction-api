from db_common import transaction, entry

with db.DBTransaction() as tr:
    transaction
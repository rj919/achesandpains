__author__ = 'jeffreyhall'
__created__ = '2017.04'

if __name__ == '__main__':
    import os
    from server.nlp.nlp_engine import nlp_engine, engine

    # Check to see that database file is written if needed
    # assert os.path.isfile(nlp.database_file)

    n1 = nlp_engine()
    print(n1.slurp("janedoe", [["My","leg","hurts"],["I","took","an","aspirin"]]))
    # The journal entry is now in the SQL database.

    print(n1.extract("janedoe"))
    pass
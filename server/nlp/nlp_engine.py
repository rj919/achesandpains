from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from os import environ, path
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from time import gmtime, strftime
import sqlite3
from server.nlp import ontology_terms

############
# Abandoning trying to use Cliner
# Need the install directory for genia, ack.
# environ["CLINER_DIR"] = path.join( path.dirname(path.abspath(__file__)), "CliNER-master" )
# import genia_dir.interface_genia
# genia_path = path.join( environ["CLINER_DIR"], "cliner", "features_dir", "geniatagger-3.0.1", "geniatagger.exe" )
# genia_dir.interface_genia.genia(genia_path, [["Hi", "mom"]])

# to make the database file go to an absolute path, use:
# sqlite:////absolute/path/to/healthjournal.db
database_file = "./nlp/healthjournal.db"
engine = create_engine('sqlite:///' + database_file, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


class nlp_engine(object):

    def slurp(self, username,s):
        """Convert English text in a list of list of words s to discrete data, then store in database."""

        # TODO:  use ISO times in strings, store as Date in SQL
        time_string = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        nlpannotated, nlpcodes = self.annotate(s)
        entry = JournalEntry(username=username,
                             messagetext=nlpannotated,
                             ontology_code_string="\n".join(nlpcodes),
                             timestamp=time_string)
        session.add(entry)
        session.commit()

    def annotate(self, s):
        # s.lower()
        # quick-and-dirty for hackathon, abandoning use of Cliner
        # s.replace("hurt", "pain")
        # s.replace("ache", "pain")
        # s.replace("hurts", "pain")
        # s.replace("aches", "pain")
        # s.replace("ached", "pain")
        # s.replace("took", "administration of substance via oral route")
        # s.replace("take", "administration of substance via oral route")

        # uri = """http://data.bioontology.org/annotator?""" + urlencode({"text": s}) + \
        #       """&longest_only=false&exclude_numbers=false&whole_word_only=true&exclude_synonyms=false"""
        #
        # # TODO: use a real API key here
        # nlp_response = urlopen(uri)
        # nlp_out = nlp_response.read()
        # nlp_json = json.loads(nlp_out)
        # return nlp_json

        # Extract useful codes
        out_string = ""
        code_set = set([])
        for line in s:
            for word in line:
                out_string += (" " + word)
                if word in ontology_terms.term_dict:
                    code_set.add(ontology_terms.term_dict[word][0] + ": " + ontology_terms.term_dict[word][1])
            out_string += ".\n"
        return(out_string, list(code_set))

    def extract(self,username):
        # TODO:  Running short of time!  This extracts ALL journal entries (so we can only have one user for the demo)
        conn = engine.connect()
        out = "HIPAA Notice:  this is a report from a demo app.\n" + \
              "   DO NOT USE this app for clinical data or PHI of any sort.\n\n\n\nHealth journal for: " + \
              str(username) + "\n"
        code_list_string = ""
        entries = list(conn.execute(select([JournalEntry])))
        for entry_result in entries:
            entry = list(entry_result)
            this_text = entry[2]
            this_text = this_text.replace("\n", "  ") + "\n"
            out += "    " + entry[4] + "\t" + this_text
            if entry[3]:
                code_list_string += entry[3] + "\n"
        out += "\n\n\n\n\n\n\nONTOLOGY TERMS:\n\t"
        code_list = list(set(code_list_string.split("\n")))
        out += "\n\t".join(code_list)
        return out

class JournalEntry(Base):
    __tablename__ = 'journalentry'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    messagetext = Column(String)
    ontology_code_string = Column(String)
    timestamp = Column(String)

Base.metadata.create_all(engine)


import ulid2
import pathlib
import json
import gzip
import datetime

TEMPLATE = "/{base}/{logname}/{dt:%Y-%m-%d}/{dt:%H}/{dt:%Y%m%d%H%M%S}_{unique}"


class GithubEvent(object):

    def __init__(self, doc):
        self.doc = doc
    
    def data(self):
        return json.load(gzip.open(self.doc, 'rb')) 


def get_filename():
    ulid2.generate_ulid_as_base32()
    base = "/tmp"
    logname = "foo"
    unique = ulid2.generate_ulid_as_base32()
    import datetime
    dt = datetime.datetime()
    dt = datetime.datetime.now()
    return TEMPLATE.format(**locals())


def read_gh_events(base='.hooks', glob='*.gz'):
    
    doc_paths = pathlib.Path(base).glob(glob)

    docs = []

    for doc in doc_paths:
        try:
            json.load(gzip.open(doc, 'rb'))
        except json.JSONDecodeError:
            continue

        docs.append(GithubEvent(doc))
    
    return docs

import sys
import argparse
import os
import re
import gzip
from collections import defaultdict

"""
Reconstruct CoNLL files for HLTCOE NER/IR Collection with actual tokens, given encoded version and original text files

2020-08-31
James Mayfield
Run with -h flag for usage information.
"""

os_dir_char = os.path.join("a", "b")[1]

collections = {
    'russian': {
        'SOURCE_ENCODING': 'UTF-8',
        'SOURCE_FILENAME_SUFFIX': ".xml.gz",
        'SOURCE_SPLIT_PATTERN': r"</DOC>\s+<DOC>",
        'SOURCE_DOCID_PATTERN': r"<DOCNO>\s*(.*?)\s*</DOCNO>",
        'SOURCE_TEXT_PATTERN': r"<TEXT>\s*(.*?)\s*</TEXT>",
        'NER_FILENAME_PATTERN': f"([^{os_dir_char}]+)_conf.conll$",
    },
    'chinese': {
        'SOURCE_ENCODING': 'gb2312',
        'SOURCE_FILENAME_SUFFIX': ".tkn_sgm",
        'SOURCE_SPLIT_PATTERN': r"</DOC>\s+<DOC>",
        'SOURCE_DOCID_PATTERN': r"<DOCNO>\s*(.*?)\s*</DOCNO>",
        'SOURCE_TEXT_PATTERN': r"<TEXT>\s*(.*?)\s*</TEXT>",
        'NER_FILENAME_PATTERN': f"([^{os_dir_char}]+).txt_input_text.sentences.txt.conll_conf.conll$",
    },
}
   
class SourceReconstructor:

    def __init__(self, spec, ner_dir, output_dir, tokencol, transduce_fn):
        """
        Create a SourceReconstructor capable of either encoding or decoding a CoNLL file given the corresponding Source text files
        """
        self.spec = spec
        self.ner_dir = ner_dir
        self.tokencol = tokencol
        self.transduce_fn = transduce_fn
        self.index_ner_dir(ner_dir, output_dir)

    def index_ner_dir(self, ner_dir, output_dir):
        """
        Build an index mapping from a docid to the corresponding NER file
        """
        self.index = {}
        for root, dirs, files in os.walk(ner_dir):
            for file in files:
                match = re.search(self.spec['NER_FILENAME_PATTERN'], file)
                if not match:
                    continue
                docid = match.group(1)
                self.index[docid] = {'docid': docid, 'input': os.path.join(root, file), 'output': os.path.join(output_dir, file)}

    def encode(self, term, crypt_keys):
        """
        Encode a single term by adding its characters' code points to the correct sequence of values from the source document
        """
        
        return(":".join([str(ord(c) + ord(crypt_keys.pop(0))) for c in term]))

    def decode(self, code, crypt_keys):
        """
        Decode a single encoded term by subtracting the correct sequence of values in the source document from the list of ints in the encoded token
        """
        codenums = code.split(':')
        return("".join([chr(int(x) - ord(crypt_keys.pop(0))) for x in codenums]))

    def transduce_ner_file(self, input_filename, output_filename, crypt_keys):
        with open(output_filename, 'wt') as outfile:
            with open(input_filename, 'rt') as infile:
                for line_num, line in enumerate(infile):
                    line = line.rstrip()
                    if len(line) == 0:
                        outfile.write('\n')
                        continue
                    entries = line.split('\t')
                    entry = entries[self.tokencol]
                    replacement = self.transduce_fn(self, entry, crypt_keys)
                    entries[self.tokencol] = replacement
                    outfile.write("\t".join(entries) + "\n")

    def transduce_doc(self, doc):
        match = re.search(self.spec['SOURCE_DOCID_PATTERN'], doc)
        if not match:
            return
        docid = match.group(1)
        if docid not in self.index:
            return
        ner_filename = self.index[docid]['input']
        output_filename = self.index[docid]['output']
        match = re.search(self.spec['SOURCE_TEXT_PATTERN'], doc, re.S)
        if not match:
            return
        crypt_keys = [x for x in match.group(1)]
        self.transduce_ner_file(ner_filename, output_filename, crypt_keys)

    def transduce_docs(self, filename):
        openfn = gzip.open if filename.lower().endswith('.gz') else open
        with openfn(filename, 'rb') as infile:
            docs = infile.read().decode(encoding=self.spec['SOURCE_ENCODING'])
            for doc in re.split(self.spec['SOURCE_SPLIT_PATTERN'], docs, flags=re.S):
                self.transduce_doc(doc)
   
    def transduce_dir(self, source_dir):
        for root, dirs, files in os.walk(source_dir):
            for file in filter(lambda x: x.lower().endswith(self.spec['SOURCE_FILENAME_SUFFIX']), files):
                self.transduce_docs(os.path.join(root, file))

def main():
    parser = argparse.ArgumentParser(description='Reconstruct text files from source')
    parser.add_argument('--encode', dest='transduce_fn', action='store_const',
                        const=SourceReconstructor.encode, default=SourceReconstructor.decode,
                        help='encode the data')
    parser.add_argument('--tokencol', default=0, type=int, metavar="colum_num", help=argparse.SUPPRESS)
    parser.add_argument('collection', choices=collections.keys(), metavar='collection_name', help=f"Name of collection to be processed (one of {list(collections.keys())})")
    parser.add_argument('source_dir', help="Base of tree containing document source files (you must have this already)")
    parser.add_argument('ner_dir', help="Base of tree containing NER files (distributed with this collection)")
    parser.add_argument('output_dir', help='Directory into which output files will be placed')
    args = parser.parse_args()

    spec = collections[args.collection]
    output_dir = os.path.realpath(args.output_dir)
    ner_dir = os.path.realpath(args.ner_dir)
    if (output_dir == ner_dir):
        print("output_dir must not be the same as ner_dir", file=sys.stderr)
        sys.exit(-1)
    os.makedirs(output_dir, exist_ok=True)
    reconstructor = SourceReconstructor(spec, ner_dir, output_dir, args.tokencol, args.transduce_fn)
    reconstructor.transduce_dir(args.source_dir)

if __name__ == '__main__':
    main()

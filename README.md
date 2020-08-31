# ner-for-ir-collection
Collection for exploring the uses of named entity recognition in information retrieval

## Introduction

Studying the effects of semantic analysis on retrieval effectiveness can be difficult using standard test collections because both queries and documents typically lack semantic markup. This collection is designed to support study of the utility of named entity annotation. It is derived from two underlying collections: CLEF 2003/2004 Russian and TDT-3 Chinese.  We defined a new set of topic aspects for topics in those test collections that are expected to benefit from named entity markup, with two queries for each aspect.  One of these queries uses named entities as a bag-of-words query term or as a semantic constraint on a free-text query term; the other is a bag-of-words baseline query without named entity markup. We performed exhaustive judgment of the documents annotated by CLEF or TDT as relevant to each corresponding topic, resulting in relevance judgments for 133 Russian and 33 Chinese topic aspects that each have at least one relevant document. To facilitate calibration to baseline scores, we also automatically generated named entity tags for the documents in both collections.

## Contents

The collection includes the following components:

* ```README.md```: This file
* ```full_collections```: The full qrels and queries obtained during annotation
* ```expt_collections```: The qrels and queries for topic aspects for which there is at least one relevant document (this is the set used in our experiments)
* ```collection-reconstructor.py```: A python script to reconstruct the named entity annotations from source documents
* ```russian.tar.bz2```: A tarred, compressed directory of encoded named entity files

In both ```full_collections``` and ```expt_collections``, the qrels files are in standard TREC format. The queries files are ***FIXME: JAKE, PLEASE DESCRIBE***

## Recreating Named Entity Files

Because we are not allowed to distribute the documents themselves, the named entity files must be decrypted using the version of the document collection you have gained legally through other means. 

The Russian collection is available from the Linguistic Data Consortium (https://www.ldc.upenn.edu/) as collection LDC2001T58. To recreate the Russian named entity files, do the following:

* Extract the encoded files using ```tar xfj russian.bz2```. This will create a directory called `russian` that contains the encrypted files.
* Locate your version of the LDC source collection. Suppose this is in a directory called ```LDC2001T58```.
* Identify where you want the unencrypted NER files to go; suppose this is a directory called 'russian-ner'.
* Run the decoding software:

```
python collection-reconstructor.py russian LDC2001T58 russian russian-ner
```
The resulting files in the ```russian_ner directory are in tab-separated format, with one token per line, and blank lines between sentences. The first column contains the token; the second column contains the named entity tag; and the third column contains the system's confidence value for this tag assignment.

The Chinese named entity annotations are not yet available. Please contact ```jamesmayfield@gmail.com``` if you are interested in obtaining them.

## Citation

If you use this collection, please cite:

Jacob Bremerman, Dawn Lawrie, James Mayfield and Douglas W. Oard, 2020. 'Two test collections for retrieval using named entity markup.' In *Proceedings of the 29th ACM International Conference on Information and Knowledge Management (CIKM '20)*. October 19-23, 2020, Virtual Event, Ireland. ACM, New York, NY, USA. 4 pages. <https://doi.org/10.1145/3340531.3417452>.

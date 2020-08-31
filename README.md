# ner-for-ir-collection
Collection for exploring the uses of named entity recognition in information retrieval
## Introduction

Studying the effects of semantic analysis on retrieval effectiveness can be difficult using standard test collections because both queries and documents typically lack semantic markup. This collection is designed to support study of the utility of named entity annotation. It is derived from two underlying collections: CLEF 2003/2004 Russian and TDT-3 Chinese.  We defined a new set of topic aspects for topics in those test collections that are expected to benefit from named entity markup, with two queries for each aspect.  One of these queries uses named entities as a bag-of-words query term or as a semantic constraint on a free-text query term; the other is a bag-of-words baseline query without named entity markup. We performed exhaustive judgment of the documents annotated by CLEF or TDT as relevant to each corresponding topic, resulting in relevance judgments for 133 Russian and 33 Chinese topic aspects that each have at least one relevant document. To facilitate calibration to baseline scores, we also automatically generated named entity tags for the documents in both collections.

## Contents

The collection includes the following components:

full_collections contains the full qrels and queries obtained during the annotation process

expt_collections contains the qrels and queries for topic aspects for which there is at least 1 relevant document (used in our experiments)

## Citation

If you use this collection, please cite:

Jacob Bremerman, Dawn Lawrie, James Mayfield and Douglas W. Oard, 2020. 'Two test collections for retrieval using named entity markup.' In *Proceedings of the 29th ACM International Conference on Information and Knowledge Management (CIKM '20)*. October 19-23, 2020, Virtual Event, Ireland. ACM, New York, NY, USA. 4 pages. <https://doi.org/10.1145/3340531.3417452>.

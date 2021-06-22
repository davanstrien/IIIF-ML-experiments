# IIIF + Machine Learning Experiments 

# tl;dr
This repository contains code for a work in progress project to explore whether computer vision models can be used in conjunction with IIIF to transfer metadata across GLAM (Galleries, Libraries, Archives and Museums) collections. 


## Overview
This repository is where we organise some in progress work exploring whether we can use computer vision to help enrich metadata of image collections held by GLAM institutions. At the moment we're focusing on photographs. In particular, we're interested in generating metadata that is relevant for GLAM institutions. We could, for example, use a model trained on the COCO dataset on an image collection. However, this might not produce metadata that is particularly useful for a GLAM institution. We are therefore starting our exploration of this topic by focusing on the [Thesaurus for Graphic Materials](https://www.loc.gov/rr/print/tgm1/) (TGM) and photographs.  

As part of this, we are also particularly interested in using IIIF  to enable this type of work. We are currently gathering data (trying to leverage existing metadata as training labels) and creating some basic baseline computer vision models. 

This is all very much work in progress. 

## Repository contents 

- [loc_harvester](loc_harvester) contains code for getting data from the Library of congress 

- [data/europeana/example_data/data/edm/](data/europeana/example_data/data/edm/) cotains example European data

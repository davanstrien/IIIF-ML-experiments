# Code to harvest images from LOC Pictures Website
https://www.loc.gov/pictures/

## Scripts

The main scripts is `downloadStats.py` this will download the first page of the search results for all terms listed in `tgm1-2021-05-07.xml`. It will download all search results to the `data` directory. If you are downloading this from Github unzip `data.zip` to get a copy of all of the search results to safe downloading them again from the LOC. 

Once the search results have been downloaded it will print the following summaries:

 * Top 20 list of formats in a form which can be pasted into a GitHub issue and will create a table
 * Top 20 list of subjects in a GitHub Table form

If you supply `downloadStats.py` with a parameter `csv` it will create a CSV of image links which relate to the top 20 categories and formats. A generated version is available in:

 * Top 20 Format example images: `image_by_formats.csv`
 * Top 20 Subject example images: `image_by_subject.csv`

The downloadStats.py will default to retrieving the first 20 pages of results for each category. To extend this add another parameter as so:

```
time ./downloadStats.py csv 50 | tee download.log
```

This will print out:
 * The length of time it takes to run,
 * limit the number of pages to maximum of 50 
 * and store the output in download.log as well as printing it to the screen.

10 pages take about 7mins, 30 pages take about 10mins. There are 20 images per page but not all of them are accessible.   

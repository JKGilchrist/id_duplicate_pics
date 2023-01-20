# id_duplicate_pics
 
A set of python scripts, to find duplicate images (jpgs) within a directory and its sub-directories.

## How to use
After having the prequisite libraries available, as listed in environment.yml or requirements.txt, you can execute the following
`python main.py`
And the program will run and identify any and all duplicate jpg/jpeg files within the /Photos directory. Alternatively, you can give your own absolute path to a directory as an argument. For example:

`python main.py "C:/Users/JKGilchrist/My Photos"`

It prints out regular updates as it executes, and prints out tuples of the absolute paths to duplicate images into the terminal. More useful, however, is that it will create a `Photos/duplicate_pics.txt` or that same-titled .txt file in the directory provided, listing all the pairs. For each pair it also lists a Windows file explorer's search query to pull up both photos with their absolute paths, and a Windows file explorer's search query to pull up both photos using their relative paths (from the same folder the .txt file is in.)

## How it identifies duplicates
It first identifies all photos within the directory and its sub-directories and then creates a smaller version of each, 10% the size of the original. This size reductions allows for the comparisons of each photo to all the others to run **much** faster than it would otherwise. Although intuitively, it gives up some accuracy in order to speed this up, I've had it run through 1000s of consecutive frames taken from videos without it giving any false positives. So, for it to give a false positive, it would need to be a pair of photos where one photo is intentionally only a few pixels different from the other. 

***

Example photos in /Photos by [CIRA/.CA](https://www.cira.ca/stock-images)
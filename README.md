# 3-grams Python

## Description

Use Python to produce a CSV file with top five word 3-grams ([n-grams](https://en.wikipedia.org/wiki/N-gram)).

Use lowercase and remove punctuation in the commit messages for each author name.

Use event type “PushEvent” within the attached file 10K.github.jsonl.bz2

## Short summary

Basically this app has one entry point main.py.

There we are running ``` app() ``` without parameters.

That means that this procedure is using default parameters for its argument.

In case you want to use some special parameters you can do it like here:
```
app('data.jsonl.bz2', 'demo.csv')
```
In this example we use file data.jsonl.bz2 as input and demo.csv as output.

If demo.csv doesn't exist it will be created.

## Lets take a look on functions and procedures we have in this app

- Functions
- [ ] parse
- [ ] remove_punctuation
- [ ] analyze
- [ ] generate_3_grams
- [ ] generate_result
- [ ] normalize

- Procedures
- [ ] export_to_csv
- [ ] app

## parse

This function take one required argument and one optional

filename - required argument, string - filename of file with input data
type_filter - value that we will use for filtering initial data. By default, this argument take value stored in constant TYPE_FILTER.

!!! It can work only with files with extension *.jsonl.bz2 !!!

It reads our input file and generate list that contains all commits from file filtered by type_filter.

## remove_punctuation

This function take one mandatory argument

text - string to be processed

It returns string sanitized from all punctuation characters.

## analize

This function take one required argument

data - list we get after parsing input file.

It is parsing that list and generate resulted dictionary that contain next information:
- The key we use in our dictionary is name of commit author
- Value of our dictionary is set that contain commit messages divided into 3-grams(this part will be described in next topic) that where created by this author
We filter from dataset author where we couldn't find at least 5 3-grams.

## generate_3_grams

This function takes one required argument

text - string with text in which we want to find 3-grams

It is generating list of 3-grams that are in text we have provided

## generate_result

This function takes one required argument

data - dictionary with information to proces

It is generating list with results information.
We expect multidimensional list where ich row contain 6 strings.
Where first is name of commits autor.
Next five are top 5 3-grams found for this author.
Top of 3-grams we search by calculation occurrence of 3-grams
beatween all commits.

## normalize

This function takes one required argument

text - string with text we want to normalize

it removes extra spaces from string

## export_to_csv

This function takes two arguments

data - List with data prepared to export
filename - File where we want to export our data

It is exporting data into CSV file

## app

This function takes two arguments

file_to_read - file where is data we want to process
file_to_write - file where we wil export our results

This method prepare and run our application

This is entry point of our app

## Installation

No additional installation is required

## Usage

In main.py update this code:
```app()```
We can provide two arguments to overwrite default behaviour. 
We can provide to parameters:
- file_to_read - it should be filename of file with extension *.jsonl.bz2 
- file_to_write - it should be filename of file with extension *.csv. If it doesn't exist it will be created.
```app(file_to_read, file_to_write)```
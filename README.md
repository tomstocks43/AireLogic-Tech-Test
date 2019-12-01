# AireLogic Tech Test

## Description
This is a Python CLI that uses MusicBrainz and Lyrics.ovh to retrieve the average number of words in an 
artist's songs. The only non-standard library required is matplotlib and NumPy for plotting the histograms.

## How to use

This file is a CLI app coded in python. T
To use the app, make sure python 3 is installed and run the file through the follwing command
"python word_count.py example_input.txt -num n" where;
example_input.txt is a path to a text file containing names of the artists to be compared, not case sensitive.
n is the number of sets of songs to retrieve where 1 set is 20 songs.

After terating through all artists, histograms are plotted for each artist showing the Mean, Min, Max and 
standard Deviation od the number of words in each song.

### Inputs

The input text file is not case sensitive but each artist must be seperated by a new line.
The -num argument must be an integer.

### Outputs

Matplotlib should show a histogram for every artist if any lyric data was found on lyrics.ovh

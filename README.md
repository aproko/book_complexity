# book_complexity
This project lets you analyze texts from Project Gutenberg - currently by generating the vocabulary counts and plotting them using Plotly. In the future, I will hopefully support different analysis modes. In order to use the graphing option, you must have installed Plotly and gotten credentials for their API. (For a how-to, go here: https://plot.ly/python/getting-started/). If you don't have Plotly, you can still generate the raw data in the format of <b>(Title, Word Count, Tf-Idf)</b> by selecting the 'print' option.

<br>
<b><font size="25">How to Download Project Gutenberg Files</size></b>

You can run get_files.py to download texts with the following options:

<b>python get_files.py <i>maxcount</i> <i>urlfile</i></b>

<i>Maxcount</i>: the total number of documents you want to process. If you decide to harvest all English language books from http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en, you might want to cap it off at a reasonable number. Unfortunately, it doesn't seem like they are alphabetically sorted, so you'd be getting a somewhat random sample of <i>maxcount</i> number of books.

<i>Urlfile</i>: the path to the file in which you store the list of URL's you want to download from. It can be a single URL such as the one above to download books for a specific language (although right now there are some issues dealing with foreign language titles that contain funny characters); or it can be a list of URL's for specific books.

<b>Example</b>: python get_files.py 100 urls.md

There is also a commented out function that would let you download the files one by one, extract the .txt file, convert it to a word counts file and then delete the .zip and the original .txt file. This is for those cases when you are processing very large amounts of texts and don't want to clog up your directory with thousands of files.
<br><br><br>
<b><font size="25">How to Generate Tf-Idf Scores</size></b>

Once you have the .txt files, you can run tfidf.py to generate the tf-idf scores of each file. <b>Tf-idf</b> is a measure of how important a word is to a document: it is a ratio of <i>term frequency</i> (how often a word appears in a given document) and <i>inverse document frequency</i>, which helps discount words that appear very frequently in all documents (eg. <i>the</i>).

<b>python tfidf.py <i>input_directory</i> <i>mode</i> <i>display_option</i></b>

<i>Input_directory</i>: self-explanatory; the directory in which your .txt files are stored

<i>Mode</i>: genCounts or tfidf or all
  genCounts generates the _counts.txt files from your raw .txt files; tfidf assumes you had already generated _counts.txt files at some    previous point and now want to rerun the tfidf calculation directly from those; all means you want to both generate _counts.txt files    AND calcualte the tf-idf score

<i>Display_options</i>: graph or print
  graph lets you create a plotly graph from your tf-idf scores. For now, the x-axis, y-axis and graph name are hardcoded in, but in the    future, I'll be amending it so that you can provide it from the command line.
  print displays the results in the format (Title, word count, tf-idf) to stdout

<b>Example<b>: python tfidf.py . tfidf print

<b>Output</b>:

dyn-160-39-232-27:book aproko$ python tfidf.py . tfidf print
<br>A Tale of Two Cities , 138836 , 15.7567355513
<br>Adventures of Huckleberry Finn, Complete , 114235 , 19.5314337493
<br>Alice's Adventures in Wonderland , 29380 , 10.26989638
<br>American Fairy Tales , 34825 , 9.49115199991
<br>Andersen's Fairy Tales , 58388 , 11.8724278255
<br>Anne Of Green Gables , 105521 , 15.969358708

Plotting tf-idf versus length of book gives you the following graph:
<div>
    <a href="https://plot.ly/~aproko/12/" target="_blank" title="Tf-Idf of Vocabulary versus Word Count" style="display: block; text-align: center;"><img src="https://plot.ly/~aproko/12.png" alt="Tf-Idf of Vocabulary versus Word Count" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="aproko:12"  src="https://plot.ly/embed.js" async></script>
</div>

I used augmented frequency in my calculation of term frequency: 
<p>
<img src="https://upload.wikimedia.org/math/3/e/4/3e45cb19588aa065134d86c91df6755e.png"></p>

This should have taken care of the bias towards longer documents, but it seems like it doesn't get rid of it completely, given that our graph seems to show a definite correlation between average tf-idf and length of the text.

Another option is to look at tf-idf versus number of unique words used:

<div>
    <a href="https://plot.ly/~aproko/14/" target="_blank" title="Tf-Idf of Vocabulary versus Unique Word Count" style="display: block; text-align: center;"><img src="https://plot.ly/~aproko/14.png" alt="Tf-Idf of Vocabulary versus Unique Word Count" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="aproko:14"  src="https://plot.ly/embed.js" async></script>
</div>

Some interesting changes occur: where the "Count of Monte Cristo" is some 200k words longer than "Moby Dick", the two actually have the same number of unique words. If we plot the number of unique words versus total number of words, we see that "Moby Dick" really stands out for using the more varied vocabulary:

<div>
    <a href="https://plot.ly/~aproko/16/" target="_blank" title="Number of Unique Words versus Total Word Count" style="display: block; text-align: center;"><img src="https://plot.ly/~aproko/16/number-of-unique-words-versus-total-word-count.jpeg" alt="Number of Unique Words versus Total Word Count" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="aproko:16"  src="https://plot.ly/embed.js" async></script>
</div>

Once the vocabulary counts are generated, you can pretty much do any sort of calculation you want: look at word length versus number of words, calculate scores like the Flesch–Kincaid readability score, or do more complex vocabulary analysis. More functions to be added in the future!


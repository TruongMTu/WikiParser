Ever need some information from Wikipedia but don't feel like copying and pasting them manually? I've written a ruby Wikipedia parser that uses Ruby's regular expressions to extract information from the Wikipedia.html. Not only that, it posts the extracted data into a .doc file for you.
To use, run this with any Ruby interpreter that you have.
You can run this parser with the following command:
-	ruby wiki_parser_full.rb NAME_OF_FILE.EXTENSION
After you've ran the previous command, just type in what information you would like. For example:
batman, robin, batman_and_robin, etc. (Just make sure to use "_" for spaces.)
If you don't provide NAME_OF_FILE.EXTENSION, it will be stored into temp.doc
When you're done trying to get information, just type "DONE".
That's it!

Note: You're free to modify the code anyway you would like.

P.S. If you're only interested in two paragraphs instead of the full wiki page, just use the wiki_parser_part.rb file instead.

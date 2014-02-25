#coded by Tu Truong
#encoding: utf-8

# Function creates a paragraph from string p
# and writes them out to file f
def paragraph(p,f)
	
	# Replaces everything that has <b>, </b>, etc.
	value = p.gsub(/<b>|<\/b>|<a>|<\/a>/, "")
 	value.gsub!(/[\[\]]/, "")
 	arr = value.split(/</)

 	# Gets rid of anything else from .* to > 
 	# and fixes spaces between numbers
	arr.each {|x| x.gsub!(/.*>\d*/, "");
		x.gsub!(/\&\#\d*\;/, " ");}
 	
	# Prints out array of broken up strings to put them back together
 	arr.each {|x|
 		if x == arr[0] && x != ""
 			f.write("\t" + x)
	 	elsif x != ""
	 		f.write(x)
 		end
 	}
 	f.write("\n")
end

# Function opens url and extracts data from it
def get_info(w)
	require 'open-uri'
	arr = []
	contents = open('http://en.wikipedia.org/wiki/' + w)
	contents = contents.read

	# If a file name was passed in to be stored somewhere
	# Otherwise, Temp.doc will be created and modified
	if(ARGV[0] != nil)
		file = File.open(ARGV[0], 'a')
	else
		file = File.open("Temp.doc", 'a')
	end

	# Writes to file what is being searched for
	file.write(w.upcase + ":\n")

	# Uses regular expression to grab first two paragraph
	if contents =~ /<p>(.*)<\/p>\n<p>(.*)<\/p>/
		paragraph($1,file)
		paragraph($2,file)
	end
	
	file.write("\n")
	file.close
end

# This function keeps loop going until "DONE" is seen
# Otherwise, function get_info will be called to use
# To extract first two paragraphs from Wikipedia
def get_info_loop file
   loop do
       line = file.gets
       if line == nil then break end
       words = line.scan(/\S+/)
       words.each{ |word|
           case word
               when /DONE/
                   return
               else
                   get_info(word)
           end
        }
   end
end

# file input
file = STDIN

# Start the code
get_info_loop file
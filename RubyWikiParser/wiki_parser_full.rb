#coded by Tu Truong
#encoding: utf-8

# Function creates a paragraph from string p
# and writes them out to file f
def paragraph(p,f)
	
	# Replaces everything that has <b>, </b>, etc.
	value = p.gsub(/<b>|<\/b>|<a>|<\/a>/, "")
 	arr = value.split(/</)

 	# Gets rid of anything else from .* to > 
 	# and fixes spaces between numbers
	arr.each {|x| x.gsub!(/.*>\d*/, ""); 
		x.gsub!(/\&\#\d*\;/, " "); }
 	
 	arr.each {|x|
 		if x == arr[0] && x != ""
 			f.write("\t" + x)
	 	elsif x != "" && x != "[" && x != "]"
	 		f.write(x)
 		end
 	}
 	f.write("\n")
end

# Function opens url and extracts data from it
def get_info(w)
	require 'open-uri'
	paragraph = []
	contents = open('http://en.wikipedia.org/wiki/' + w) {|f| 
		f.readlines.each {|x| 
			if x =~ /<p>(.*)<\/p>/
			paragraph.push($1)
			end
	}}

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
	paragraph.each {|p| paragraph(p,file)}
	
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
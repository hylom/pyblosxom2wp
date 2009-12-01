
 pyblosxom2wp.py - import blog story from Pyblosxom to Wordpress
 by hylom <hylomm@gmail.com>, 2009.

= usage =

 1. edit some variables in pyblosxom2wp.py
     - title -> your blog's title
     - link -> your blog's link url 
     - baseurl -> your blog's baseurl

 2. run pyblosxom2wp.py and get standard output
     - usage: ./pyblosxom2wp.py <pyblosxom's_story_directory> > output.xml

 3. check output and import to Wordpress

= Files and those origins = 

  * pyblosxom2wp.py: main script file. written by hylom.

  * BeautifulSoup.py: HTML/XML Parser.
    http://www.crummy.com/software/BeautifulSoup/

  * wordpress.py: Wordpress's WXL generator, part of google-blog-converters-appengine. 
    http://code.google.com/p/google-blog-converters-appengine/


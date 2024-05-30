Problem: When Summit Learning is uploading some of its courses, its running into issues with properly rendering iFrame for links that have a drive.google domain. Rather than rendering the content, the user will see a "You need access" error message, but if the user clicks on the link, they will be able to successfully see the content 

Solution: We will replace these iFrames with a simple link "Click here to access this resource", so user will not see an access error message and can route to the content easily. 

Function: fix_iframes_for_course(course_id)
Description: Iterates through all the pages for the course, checking for any iFrames that need to be replaced with a link, and replaces those iFrames. Records the pages that have been changed. 
1. right click in the folder and open bash
2. git init
3. git add .    or git add filename   ### to add all files for commint
4. git commit -m "remarks"
5. git push -u origin main     #for main branch


change branch (new branch):

1. git fetch origin    	        	# fetch the latest from repo (optional) 
2. git checkout -b new_branch_name     # for new branch
3. git push -u origin new-branch-name	# push the new branch in the github (only for the 1st time used) later git push
4. git branch 				# check the current branch

push in the branch:
1. git status
2. git add .     or    git add file_name1, file_name2..    ## add the files for commit
3. git commit -m "message"	
4. git push -u origin branch-name     or     git push     ## to push to site


Merging the Main-Branch
1. git checkout main     ## switch to main
2. git pull origin main    ## to pull latest changes from main  (if someone else has done changes)
3. git merge your-branch-name    ## merge the main with your branch
4. git push origin main   	## push the changes of main to github







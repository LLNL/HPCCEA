# Further Development 

## Style
- Generally need to change `if (not) (x in y)` to `if (x not in y)`

## Nodeattr Options that Haven't Been Implemented Yet
- h run automatically
Help wil run with you right -h but not if there is not arugments given at all
- q logic
    - -q &&
    - -q ||
    - -q ~
    - -q -- 
- -Q [node] query=[attr]
   - most -Q options are implemented, except where the user enters an attribute to check against
- -l [list of nodes]
   - -l with no nodes / 1 node is implemented, but we haven't added functionality for a list of nodes 

## Ideas for the Future 
- Automatic updates whenever a change to a genders file is made
   - gitlab continuous integration
- create different levels of access to the database (inserting, viewing, etc.)
- create configuration file to handle password management 
- make the `description` filed of the GENDER table mandatory, and record the user who created each gender, so later users can ask for help 

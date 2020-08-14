# Further Development 

## Nodeattr Options that Haven't Been Implemented Yet

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

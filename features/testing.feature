Feature: Validate end to end processing of input files
  Scenario: validate invalid datatype for EMPLOYEE_ID
    Given file is placed in source folder for "incorrect record length||"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate invalid datatype for EMPLOYEE_ID
    Given file is placed in source folder for "invalid datatype|EMPLOYEE_ID|int"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate invalid datatype for FIRST_NAME
    Given file is placed in source folder for "invalid datatype|FIRST_NAME|str"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate end to end processing of valid input file
    Given file is placed in source folder for "invalid datatype|EMPLOYEE_ID|int"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate end to end processing of valid input file
    Given file is placed in source folder for "invalid datatype|DEPARTMENT_ID|int"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate end to end processing of invalid input file
    Given file is placed in source folder for "invalid datatype|LAST_NAME|str"
    When Dev code is executed
    Then file exists in "Error" folder
    And "Source" folder is empty
    And "Target" folder is empty

  Scenario: validate end to end processing of valid input file
    Given file is placed in source folder for "valid datatype|SALARY|int"
    When Dev code is executed
    Then file is moved to target folder
    And "source" folder is empty
    And file exists in "target" folder
    And file name is correct
    And data is correct and matching with the input file

#
#  Scenario: def1
#    Given ghi "1"
#    When jkl "2"
#    Then mno "3"
#    And pqr "4"
#
#  Scenario: def1
#    Given ghi "1"
#    When jkl "2"
#    Then mno "3"
#    And pqr "4"
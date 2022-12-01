Feature: Validate end to end processing of input files
  Scenario: validate end to end processing of valid input file
    Given file is placed in source folder for "valid datatype|SALARY|int"
    When Dev4_initial code is executed
    Then Validate if "valid" data is moved to "Validation" folder
    And validate if transformed data file is created in "Target" folder
    And Validate if "invalid" data is moved to "error" folder

  Scenario: validate incorrect record length
    Given file is placed in source folder for "incorrect record length||"
    When Dev4_initial code is executed
    Then Validate if "valid" data is moved to "Validation" folder
    And Validate if "invalid" data is moved to "error" folder

  Scenario: validate invalid datatype for EMPLOYEE_ID
    Given file is placed in source folder for "invalid datatype|EMPLOYEE_ID|int"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate invalid datatype for FIRST_NAME
    Given file is placed in source folder for "invalid datatype|FIRST_NAME|str"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate invalid datatype for LAST_NAME
    Given file is placed in source folder for "invalid datatype|LAST_NAME|str"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate invalid datatype for EMAIL
    Given file is placed in source folder for "invalid datatype|EMAIL|str"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate invalid datatype for SALARY
    Given file is placed in source folder for "invalid datatype|SALARY|int"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate invalid datatype for MANAGER_ID
    Given file is placed in source folder for "invalid datatype|MANAGER_ID|int"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder

  Scenario: validate null check for EMPLOYEE_ID
    Given file is placed in source folder for "null check|EMPLOYEE_ID|int"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder


  Scenario: validate duplicate records
    Given file is placed in source folder for "duplicate||"
    When Dev4_initial code is executed
    Then Validate if "invalid" data is moved to "error" folder
    And Validate if "valid" data is moved to "Validation" folder


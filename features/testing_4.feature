Feature: Validate end to end processing of input files
  Scenario: validate end to end processing of valid input file with pandas for Initial Load
    Given file is placed in source folder for "valid datatype|SALARY|int" with pandas
    When "code4_initial.py" code is executed with pandas
    Then Validate if "valid" data is moved to "Validation" folder with pandas
    And validate if transformed data file is created in "Target" folder with pandas
    And Validate if "invalid" data is moved to "error" folder with pandas
    And validate if processed data file is created in "Processed" folder with pandas


  Scenario: validate end to end processing of valid input file with pandas for Delta1 Load
    Given file is placed in source folder for "new delta|SALARY|int" with pandas
    When "code4_delta.py" code is executed with pandas
    Then Validate if "valid" data is moved to "Validation" folder with pandas
    And validate if transformed data file is created in "Target" folder with pandas
    And Validate if "invalid" data is moved to "error" folder with pandas
    And validate if processed data file is created in "Processed" folder with pandas

  Scenario: validate end to end processing of valid input file with pandas for Delta2 Load
    Given file is placed in source folder for "update delta|SALARY|int" with pandas
    When "code4_delta.py" code is executed with pandas
    Then Validate if "valid" data is moved to "Validation" folder with pandas
    And validate if transformed data file is created in "Target" folder with pandas
    And Validate if "invalid" data is moved to "error" folder with pandas
    And validate if processed data file is created in "Processed" folder with pandas

  Scenario: validate end to end processing of valid input file with pandas for Delta3 Load
    Given file is placed in source folder for "delete delta|SALARY|int" with pandas
    When "code4_delta.py" code is executed with pandas
    Then Validate if "valid" data is moved to "Validation" folder with pandas
    And validate if transformed data file is created in "Target" folder with pandas
    And Validate if "invalid" data is moved to "error" folder with pandas
    And validate if processed data file is created in "Processed" folder with pandas


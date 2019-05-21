class ATM():
    """
    ... Develop our code ...
    """

    def process_request(self, input):
        """
        ... Develop our code ...
        """
        return None


if __name__ == "__main__":

    import json

    # Loads the test file
    input_file = open("caixa_eletronico_amostras_teste.json")
    test_samples = json.load(input_file)

    # Instance proposed class
    atm = ATM()

    # Loops every test sample
    count_success, count_fail = 0, 0
    for idx, sample in enumerate(test_samples):
        input    = sample.get("input")
        correct_output = sample.get("output")

        processed_output = atm.process_request(inupt)

        # Checks if the result is correct
        if processed_output == correct_output:
            count_success += 1
            print("Sample # {} - Success".format(idx))
        else
            print("Sample # {} - Error".format(idx))
            count_fail += 1
    
    print("You got {} right answers and {} wrong answers".format(count_success, count_fail))
        


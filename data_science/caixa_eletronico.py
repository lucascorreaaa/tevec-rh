class ATM():
    import numpy as np
    import json

    def process_request(self, input):

        # Calculating minimum required quantity
        amount = input['request']['request']
        user_id = input['request']['userID']
        n_50,rem_50 = np.divmod(amount,50)
        n_20,rem_20 = np.divmod(rem_50,20)
        
        # Returning output SUCCESS message
        if rem_20 == 0:
            return self.output_message(user_id, amount, n_20, n_50)

        # Returning output SUCCESS message after adjust the number of notes (case of 80 and 60 decimals)
        elif rem_20 == 10:
            n_50 -= 1
            n_20_incrementer = 3 if n_20 == 0 else 4
            n_20 += n_20_incrementer
            return self.output_message(user_id, amount, n_20, n_50)
        # Returning output FAIL message 
        else:
            return self.output_message(user_id, amount, fail=True)

    def output_message(self,user_id, requested_amount, n_20, n_50, fail=False):
        if fail:
            message = {
                        'requester': {
                            'userID': user_id,
                            'requested': requested_amount
                        },
                        'response': {
                            'error': 'Nao e possivel sacar a quantia solicitada porque nao ha notas compatives. As notas disponiveis sao de R$ 20 e R$ 50, por favor insira um valor compativel.'
                        }
                    }
            return message
        message = {
                    'requester': {
                        'userID': user_id,
                        'requested': requested_amount
                    },
                    'response': {
                        '20': n_20.item(),
                        '50': n_50.item()
                    }
                }
        return message
    


if __name__ == "__main__":

    import json
    import numpy as np 

    # Loads the test file
    input_file = open("caixa_eletronico_amostras_teste.json")
    test_samples = json.load(input_file)

    # Instance proposed class
    atm = ATM()

    # Loops every test sample
    count_success, count_fail = 0, 0
    for idx, sample in enumerate(test_samples):
        input = sample.get("input")
        correct_output = sample.get("output")

        processed_output = atm.process_request(input)

        # Checks if the result is correct
        if processed_output == correct_output:
            count_success += 1
            print("Sample # {} - Success".format(idx))
        else:
            print("Sample # {} - Error".format(idx))
            count_fail += 1
    
    print("You got {} right answers and {} wrong answers".format(count_success, count_fail))
        


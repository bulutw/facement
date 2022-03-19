import requests
import hashlib

def encrypt(arg):
    md = hashlib.md5(arg.encode())
    md = hashlib.sha256(md.hexdigest().encode())
    return(md.hexdigest())

def add_a_card(card_number, client_id):
    url = f"http://localhost:1000/add-card/{encrypt(card_number)}/{client_id}"
    print("THIS IS THE URL ::: " + url)
    get = requests.get(url, headers={'Authorization': 'Token ff259428e57d2ee6a02645da8d7fa652b34c877a'})
    get = get.json()

    add_a_card.already_exists = None
    add_a_card.client_doesnt_exists = None
    add_a_card.err = None

    if get.get('detail') == None:
        response_Response = get.get('Response')
        if response_Response == "ALREADY_EXISTS":
            add_a_card.already_exists = True
            add_a_card.response_for_text = "The card is already signed the system."
        elif response_Response == "CLIENT_DOESNT_EXISTS":
            add_a_card.client_doesnt_exists = True
            add_a_card.response_for_text = "Client ID doesn't exists."
        elif response_Response == "SUCCESS":
            add_a_card.response_for_text = "Card signed successfully."
            return True
    else:
        add_a_card.err = True
        add_a_card.err_text = "ERR:SYSTEM_TOKEN_ERROR"

    # Using
    
    # add_card = add_a_card( credit_card_number, client_id )
    
    # -
    # # Handle "card added successfully" =>
    # if add_card:
    #   return HttpResponse(f'<p> {add_card.response_for_text} </p>')
    # -
    # -
    # # Handle "card is already exists" =>
    # if add_card.already_exists:
    #   return HttpResponse(f'<p> {add_card.response_for_text} </p>')
    # -
    # # Handle "client id doesn't exists" =>
    # if add_card.client_doesnt_exists:
    #   return HttpResponse(f'<p> {add_card.response_for_text} </p>')
    # -
    # # Handle errors. =>
    # if add_card.err:
    #   return HttpResponse(f'<p> {add_card.response_for_text} </p>') # Print the error
    #   # OR #
    #   return HttpResponse(' <p> An error occurred </p> ')
    # -

def check_card(cc_num):
    response = requests.get(f'http://localhost:1000/check-card/{encrypt(cc_num)}', headers={'Authorization': 'Token ff259428e57d2ee6a02645da8d7fa652b34c877a'})
    response = response.json()

    check_card.exists = None
    check_card.failure = None

    if response.get('detail') == None:
        resp_Response = response.get('Response')
        if resp_Response == 'EXISTS':
            check_card.exists = True
        elif resp_Response == 'DOESNT_EXISTS':
            check_card.exists = False
        return True
    else:
        check_card.failure = True


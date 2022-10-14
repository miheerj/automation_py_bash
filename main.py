def doc(para):
    before_number = doc_string[:doc_string.index("Number")]
    print(before_number)

    first_number = doc_string.split("Number")[1].split()[0]
    value = dict_num[first_number]

    result = re.search('Number(.+?)number next', doc_string).group(1).lstrip()
    sent_after_number = result.split(' ', 1)[1]
    print(str(value) + "." + sent_after_number)

    commands = re.split('number next', doc_string)
    for i in range(len(commands)-1):
        number_val = value+i+1
        print(str(number_val)+ "." + str(commands[i+1].lstrip()).capitalize())




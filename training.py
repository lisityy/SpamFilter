def dictionaries(truth_dict, emails_dict, spam_dict, ham_dict, all_s_words, all_h_words):
    """
    - Fill the dictionaries (spam_dict and ham_dict) with words
    from the text of the email and the number of times they are repeated
    - Return the number of spam/ham emails and total number of words in spam/ham emails
    """
    n_spam = 0  # number of spam/ham emails
    n_ham = 0
    for name, text in emails_dict.items():
        for word in text:
            if word not in spam_dict:
                spam_dict[word] = 1
            if word not in ham_dict:
                ham_dict[word] = 1
            if truth_dict[name] == 'SPAM':
                spam_dict[word] += 1
                n_spam += 1
            if truth_dict[name] == 'OK':
                ham_dict[word] += 1
                n_ham += 1
 
    for v in spam_dict.values():
        all_s_words += v
    for v in ham_dict.values():
        all_h_words += v
    return n_spam, n_ham, all_s_words, all_h_words
 
 
def get_one_sender(words):
    for i in range(len(words)):
        if words[i] == "From:":
            j = 0
            while '@' not in words[i + j]:
                j += 1
                if i + j < len(words):
                    break
            words[i + j] = words[i + j].replace('<', '')
            words[i + j] = words[i + j].replace('>', '')
            return words[i + j]
 
 
def emails_from(emails_dict, truth_dict, senders):
    """
    The function fills the dictionary with the email
    that sent the spam, and the number of his spam emails.
    """
    for name, email in emails_dict.items():
        man = get_one_sender(email)
        if truth_dict[name] == "SPAM":
            senders[man] = senders.get(man, 0) + 1
    return senders
 
 
def probability(spam_dict, ham_dict, all_s_words, all_h_words):
    """
    Calculate the probability/frequency with which a word occurs in spam/ham emails
    relative to the total number of spam/ham words
    (multiplication by K to make sure that the number does not fall below the minimum allowed in python)
    """
    K = 1000  # factor for calculating the probability
    for word, value in spam_dict.items():
        spam_dict[word] = (value / all_s_words) * K
    for word, value in ham_dict.items():
        ham_dict[word] = (value / all_h_words) * K
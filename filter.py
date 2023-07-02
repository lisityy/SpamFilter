import os
from corpus import Corpus
import utils
import training
 
 
class MyFilter:
    """
    Spam filter with machine learning by Pimenova Olga and Poludina Sofia
    """
    def __init__(self):
        self.all_spam_words = 0  # the total number of words contained in spam/ham emails
        self.all_ham_words = 0
 
        self.n_spam_emails = 0  # number of spam/ham emails
        self.n_ham_emails = 0
 
        # dictionary with the name of the word and its frequency which it appears in all spam/ham training emails
        self.spam_dict = {}
        self.ham_dict = {}
 
        # the proportion of the number of spam\ham emails to the total number of emails from the training data
        self.spam_probability = 0
        self.ham_probability = 0
 
        self.spam_senders = {}  # array with the names of spam senders
 
    def train(self, direction):
        """
        Training of the data needed to simplify email classification, based on the received data.
        """
        # Create a dictionary with file names and a text message (as an array with the words)
        train_corpus = Corpus(direction)
        emails_dict = {}
        for fname, text in train_corpus.emails():
            emails_dict[fname] = text.split()
 
        # Create a dictionary with file names and their classification (OK or SPAM)
        truth_dict = utils.read_classification_from_file(os.path.join(direction, '!truth.txt'))
 
        self.spam_senders = training.emails_from(emails_dict, truth_dict, self.spam_senders)
 
        # Edit the text of the email to make it easier to work with
        emails_dict = Corpus.reformat_text(emails_dict)
 
        # Fill spam_dict and ham_dict dictionaries + get number of spam/ham emails and number of total spam/ham words
        self.n_spam_emails, self.n_ham_emails, self.all_spam_words, self.all_ham_words \
            = training.dictionaries(truth_dict, emails_dict, self.spam_dict, self.ham_dict, self.all_spam_words,
                                    self.all_ham_words)
 
        self.spam_probability = self.n_spam_emails / (self.n_ham_emails + self.n_spam_emails)
        self.ham_probability = self.n_ham_emails / (self.n_ham_emails + self.n_spam_emails)
 
        training.probability(self.spam_dict, self.ham_dict, self.all_spam_words, self.all_ham_words)
 
    def test(self, direction):
        """
        The function classifies emails into spam and non-spam.
        """
        corpus = Corpus(direction)
        emails_dict = {}
        for fname, text in corpus.emails():
            emails_dict[fname] = text.split()
 
        sender = {}
        for fname in emails_dict:
            sender[fname] = training.get_one_sender(emails_dict[fname])
 
        emails_dict = Corpus.reformat_text(emails_dict)
 
        f = open(os.path.join(direction, "!prediction.txt"), 'w', encoding="utf-8")
        for fname in emails_dict:
            # If the sender of the email has already been encountered in the training files as a spam sender
            if sender[fname] in self.spam_senders:
                f.write(fname + " SPAM\n")
            else:
                prob_spam, prob_ham = self.total_email_probability(emails_dict[fname], self.spam_probability,
                                                                   self.ham_probability)
                if prob_spam > prob_ham:
                    f.write(fname + " SPAM\n")
                else:
                    f.write(fname + " OK\n")
        f.close()
 
    def total_email_probability(self, email_text, p_spam, p_ham):
        """
        The function calculates the probability that the received email is spam/ham.
        The calculation is based on the frequency with which the word occurred
        in the spam/ham emails in the training files.
        """
        for word in email_text:
            if word in self.spam_dict:
                tmp = p_spam * self.spam_dict[word]   # None of the numbers is 0 and the number after multiplication
                if tmp != 0 and tmp < float('inf'):     # does not become too large to process
                    p_spam = tmp
            if word in self.ham_dict:
                tmp = p_ham * self.ham_dict[word]
                if tmp != 0 and tmp < float('inf'):
                    p_ham = tmp
        return p_spam, p_ham
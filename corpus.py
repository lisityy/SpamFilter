import os
 
 
class Corpus:
    def __init__(self, email_directory):
        self.email_directory = email_directory
 
    def emails(self):
        """
        The function reads files and returns their names and email messages.
        """
        email_names = os.listdir(self.email_directory)
        for fname in email_names:
            if not fname[0] == '!':  # the file isn't classification
                with open(os.path.join(self.email_directory, fname), 'r', encoding="utf-8") as f:
                    yield fname, f.read()
 
    @staticmethod
    def reformat_text(dictionary):
        """
        The function edits words, removes punctuation and digits
        from the email text message and returns the dictionary
        with the new formatted words.
        """
        # The 100 most popular words
        stop_words = ['a', 'about', 'all', 'also', 'and', 'as', 'at', 'be', 'because', 'but', 'by', 'can', 'come',
                      'could', 'day', 'do', 'even', 'find', 'first', 'for', 'from', 'get', 'give', 'go', 'have', 'he',
                      'her', 'here', 'him', 'his', 'how', 'I', 'if', 'in', 'into', 'it', 'its', 'just', 'know', 'like',
                      'look', 'make', 'man', 'many', 'me', 'more', 'my', 'new', 'no', 'not', 'now', 'of', 'on', 'one',
                      'only', 'or', 'other', 'our', 'out', 'people', 'say', 'see', 'she', 'so', 'some', 'take', 'tell',
                      'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thing', 'think',
                      'this', 'those', 'time', 'to', 'two', 'up', 'use', 'very', 'want', 'way', 'we', 'well', 'what',
                      'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']
        digits = "1234567890"
        punctuation = "><-*|&'()!;:~,/.+[]={}?_#$^"
        remove_str = punctuation + digits
        new_dict = {}
        for name in dictionary:
            new_dict[name] = []
            for i, word in enumerate(dictionary[name]):
                word = word.lower()  # Change the word to lowercase
                word = word.strip(remove_str)  # Remove punctuation and digits from the beginning and end of the word
                # Add a word to the new dictionary, if it is not too short/long and does not contain signs
                if 3 < len(word) <= 40 and word.isalpha() and word not in stop_words:
                    if len(new_dict[name]) >= 1000:  # Read only the first 1000 words to save memory and time
                        break
                    new_dict[name].append(word)
        return new_dict
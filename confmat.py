class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def as_dict(self):
        """
        The function returns the binary confusion matrix as a dictionary.
        """
        bcm_dict = {'tp': self.tp, 'tn': self.tn, 'fp': self.fp, 'fn': self.fn}
        return bcm_dict

    def update(self, truth, prediction):
        """
        Update data in the binary confusion matrix.
        """
        if truth != self.pos_tag and truth != self.neg_tag:
            raise ValueError
        if prediction != self.pos_tag and prediction != self.neg_tag:
            raise ValueError

        if truth == prediction:
            if truth == self.pos_tag:  # true positive
                self.tp += 1
            elif truth == self.neg_tag:  # true negative
                self.tn += 1
        else:
            if truth == self.pos_tag:
                self.fn += 1
            elif truth == self.neg_tag:
                self.fp += 1

    def compute_from_dicts(self, truth_dict, pred_dict):
        """
        Calculate the binary confusion matrix based on the values stored in the dictionaries.
        """
        for i, j in truth_dict.items():
            if i in pred_dict:
                self.update(j, pred_dict[i])
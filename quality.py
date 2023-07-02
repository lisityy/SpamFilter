import utils
import os
import confmat


def quality_score(tp, tn, fp, fn):
    """
    The function returns the quality score from the passed values
    of the binary confusion matrix.
    """
    return (tp + tn) / (tp + tn + 10 * fp + fn)


def compute_quality_for_corpus(corpus_dir):
    """
    The function that evaluates the quality of predictions based on the data
    in the !truth.txt and !prediction.txt files of the specified corpus.
    """
    truth_dict = utils.read_classification_from_file(os.path.join(corpus_dir, '!truth.txt'))
    prediction_dict = utils.read_classification_from_file(os.path.join(corpus_dir, '!prediction.txt'))

    matrix = confmat.BinaryConfusionMatrix("SPAM", "OK")
    matrix.compute_from_dicts(truth_dict, prediction_dict)

    bcm_dictionary = matrix.as_dict()
    quality = quality_score(bcm_dictionary['tp'], bcm_dictionary['tn'], bcm_dictionary['fp'], bcm_dictionary['fn'])

    return quality
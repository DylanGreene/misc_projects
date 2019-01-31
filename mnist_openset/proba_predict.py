# Improved Open Set Recognition Using Classification Probabilities
# Dylan Greene

import argparse

def proba_predict(test_file, proba_file, output_file):
    # read in each line of each file
    with open(test_file, 'r') as f:
        test_lines = f.readlines()
    # only keep the actual class (don't need the actual image info)
    test_lines = [line.strip().split()[0] for line in test_lines]

    with open(proba_file, 'r') as f:
        proba_lines = f.readlines()
    proba_lines = [line.strip().split() for line in proba_lines][1:]

    # iterate over and compare predicted probabilities to a threshold
    count_correct = 0
    predictions = []
    for x in zip(test_lines, proba_lines):
        actual = int(x[0])
        highest_proba_index = int(x[1][0])
        highest_proba = float(x[1][highest_proba_index+1])
        # highest class probability is less than 0.95, likely in openset so predict -1
        if highest_proba < 0.95 and actual == -1:
            predictions.append(-1)
            count_correct += 1
        elif highest_proba >= 0.95 and actual == highest_proba_index:
            predictions.append(highest_proba_index)
            count_correct += 1
    print('Accuracy = {}% ({}/{}) (open set classification)'.format(count_correct/len(test_lines)*100, count_correct, len(test_lines)))

    # write the new predicitons to the output file
    with open(output_file, 'w') as f:
        for prediction in predictions:
            f.write('{}\n'.format(prediction))

    return

if __name__ == '__main__':
    # Set the argument parser to get the necessary files
    parser = argparse.ArgumentParser(description='Probability based classification')
    parser.add_argument('test_file', metavar='test_file', type=str, help='Path to the testing set')
    parser.add_argument('proba_file', metavar='proba_file', type=str, help='Path to the probability file from svm-predict')
    parser.add_argument('output_file', metavar='output_file', type=str, help='Path to the output file')
    args = parser.parse_args()

    proba_predict(args.test_file, args.proba_file, args.output_file)

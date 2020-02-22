from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt


root = "/home/peter/Documents/hash_code"
FILE_NAME = "f_libraries_of_the_world.txt"


def extractFile(file_name):
    B = 0
    L = 0
    D = 0
    book_scores = []
    libraries_specs_B_D_S = []
    libraries_book_IDs = []

    with open(file_name) as file:
        lines = file.readlines()
        library_specs_line = True
        for i, line in enumerate(lines):
            if line == '\n':
                continue
            line = [ int(x) for x in line.split(' ') ]
            if i == 0:
                B = line[0]
                L = line[1]
                D = line[2]
            elif i == 1:
                book_scores = line
            else:
                if library_specs_line:
                    libraries_specs_B_D_S.append(line)
                else:
                    libraries_book_IDs.append(line)
                library_specs_line = not library_specs_line
    
    return B, L, D, book_scores, libraries_specs_B_D_S, libraries_book_IDs


def libraryScoreMeanSTD(libraries_book_IDs, book_scores, print_bool=False):
    library_score_sum = []
    for i, library_book_IDs in enumerate(libraries_book_IDs):
        score_sum = 0
        for j, book_ID in enumerate(library_book_IDs):
            score_sum += book_scores[book_ID]
        library_score_sum.append(score_sum)
    library_score_sum = np.array(library_score_sum)
    score_mean = np.mean(library_score_sum)
    score_std = np.std(library_score_sum)
    if print_bool:
        print(
            "Library score mean:    ", score_mean,
            "\nLibrary score STD:     ", score_std)
        print(
            "Relation:", score_std / score_mean)
        print()
    return score_mean


def signupMeanSTD(libraries_specs_B_D_S, print_bool=False):
    all_signup_days = []
    for i, library_B_D_S in enumerate(libraries_specs_B_D_S):
        all_signup_days.append(library_B_D_S[1])
    signup_mean = np.mean(np.array(all_signup_days))
    signup_std = np.std(np.array(all_signup_days))
    if print_bool:
        print(
            "Sign_up mean:", signup_mean,
            "\nSign_up STD: ", signup_std,
            "\nRelation:", signup_std / signup_mean)
        print()
    return signup_mean


def speedMeanSTD(libraries_specs_B_D_S, print_bool=False):
    all_speeds = []
    for i, library_B_D_S in enumerate(libraries_specs_B_D_S):
        all_speeds.append(library_B_D_S[2])
    speed_mean = np.mean(np.array(all_speeds))
    speed_std = np.std(np.array(all_speeds))
    if print_bool:
        print(
            "Speed mean:", speed_mean,
            "\nSpeed STD: ", speed_std,
            "\nRelation:", speed_std / speed_mean)
        print()
    return speed_mean


def totalscore(book_scores, print_bool=False):
    total_score = np.sum(book_scores)
    book_mean = np.mean(book_scores)
    if print_bool:
        print(
            "Total score:", total_score,
            "\nMean score of a book: ", book_mean)
    return total_score


def totalNumberOfBooks(libraries_specs_B_D_S):
    books_sum = 0
    for i, library_specs_B_D_S in enumerate(libraries_specs_B_D_S):
        books_sum += library_specs_B_D_S[0]
    return books_sum


def main():
    txt_files = sorted([f for f in listdir(root) if isfile(join(root, f))][:-1])

    total_score_means = []
    signup_means = []
    speed_means = []
    names = []
    days = []
    library_score_means = []
    book_copy_ratios = []

    for txt_file in txt_files:
        name = txt_file[0]

        # Read data
        B, L, D, book_scores, libraries_specs_B_D_S, libraries_book_IDs = \
            extractFile(txt_file)

        # Data analysis
        library_score_mean = libraryScoreMeanSTD(libraries_book_IDs, book_scores)
        signup_mean = signupMeanSTD(libraries_specs_B_D_S)
        speed_mean = speedMeanSTD(libraries_specs_B_D_S)
        total_score_mean = totalscore(book_scores)
        book_copy_ratio = totalNumberOfBooks(libraries_specs_B_D_S) / B

        # Gather data
        total_score_means.append(total_score_mean)
        names.append(name)
        signup_means.append(signup_mean)
        speed_means.append(speed_mean)
        days.append(D)
        library_score_means.append(library_score_mean)
        book_copy_ratios.append(book_copy_ratio)

    print(total_score_means, names)
    #print(list(range(len(total_score_means))))
    plt.subplot(331)
    plt.plot(names, total_score_means)
    plt.title("Total scores")

    plt.subplot(332)
    plt.plot(names, signup_means)
    plt.title("Sign up means")

    plt.subplot(333)
    plt.plot(names, speed_means)
    plt.title("Speed means")

    plt.subplot(334)
    plt.plot(names, days)
    plt.title("Days")

    plt.subplot(335)
    plt.plot(names, np.array(signup_means) / np.array(days))
    plt.title("Sign up means / days")

    plt.subplot(336)
    plt.plot(names, np.array(speed_means) / np.array(days))
    plt.title("Speed means / days")

    plt.subplot(337)
    plt.plot(names, np.array(library_score_means) / np.array(days))
    plt.title("Library score means / days")

    plt.subplot(338)
    plt.plot(names, book_copy_ratios)
    plt.title("Book copy ratio")
    plt.show()

main()


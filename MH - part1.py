"""
This script demonstrates how to design the simplest recommender system based of
Collaborative Filtering. In order to make these predictions, we must first measure
similarity of users or items from the rows and columns of the Utility Matrix.
We will use the Pearson Correlation Similarity Measure to find similar users.
"""
#!/bin/python
from numpy import *
from sklearn.metrics import mean_squared_error
import operator

# User class stores the names and average rating for each user
class User:
    def __init__(self, name):
        self.name = name
        self.avg_r = 0.0

# Item class stores the name of each item
class Item:
    def __init__(self, name):
        self.name = name

# Rating class is used to assign ratings
class Rating:
    def __init__(self, user_id, item_id, rating):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating

# We store users in an array. The index of the array marks the id of that user
user = []
user.append(User("Ann"))
user.append(User("Bob"))
user.append(User("Carl"))
user.append(User("Doug"))

# Items are also stored in an array. The index of the array marks the id of that item.
item = []
item.append(Item("HP1"))
item.append(Item("HP2"))
item.append(Item("HP3"))
item.append(Item("SW1"))
item.append(Item("SW2"))
item.append(Item("SW3"))

rating = []
rating.append(Rating(1, 1, 4))
rating.append(Rating(1, 4, 1))
rating.append(Rating(2, 1, 5))
rating.append(Rating(2, 2, 5))
rating.append(Rating(2, 3, 4))
rating.append(Rating(3, 4, 4))
rating.append(Rating(3, 5, 5))
rating.append(Rating(4, 2, 3))
rating.append(Rating(4, 6, 3))

#print(rating)

n_users = len(user)
n_items = len(item)
n_ratings = len(rating)

# The utility matrix stores the rating for each user-item pair in the matrix form.
utility = zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

"""
Definition of the pcs(x, y) and guess (u, i, top_n) functions.
Complete these after reading the project description.
"""

# Finds the Pearson Correlation Similarity Measure between two users
def pcs(x, y):

    global item, user, utility, n_users, n_items
    # I is the set of all items that the two users have rated
    I = []
    for i in item:

        if (utility[x-1][item.index(i)-1] != 0) and (utility[y-1][item.index(i)-1] != 0):
            I.append(i)
    # I_x is the set of all items that user x has rated
    I_x = []
    for i in item:
        if utility[x-1][item.index(i)-1] != 0:
            I_x.append(i)

    # I_y is the set of all items that user y has rated
    I_y = []
    for i in item:
        if utility[y-1][item.index(i)-1] != 0:
            I_y.append(i)

    # I is the set of all items that the two users have rated
    # Alternate way of calculating I
    # I = [i for i in I_x if i in I_y]

    # R_x is the set of ratings that user x has given to all items in I_x
    R_x = [utility[x-1][item.index(i)-1] for i in I_x]


    # R_y is the set of ratings that user y has given to all items in I_y
    R_y = [utility[y-1][item.index(i)-1] for i in I_y]

    # r_x is the average rating that user x has given to all items in I_x
    r_x = sum(R_x) / len(R_x)
    # r_y is the average rating that user y has given to all items in I_y
    r_y = sum(R_y) / len(R_y)




    # Numerator of the pcs formula given in the notes
    numerator = 0
    for i in I:
        numerator += (utility[x-1][item.index(i)-1] - r_x) * (utility[y-1][item.index(i)-1] - r_y)

    # Denominator of the pcs formula given in the notes
    denominator = 0
    for i in I:
        denominator += ((utility[x-1][item.index(i)-1] - r_x) ** 2) * ((utility[y-1][item.index(i)-1] - r_y) ** 2)
    if denominator != 0:

        return float(numerator) / float(denominator)
    else:
        return 1000

# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this. Use top_n as 3 in this example.
def guess(user_id, i_id, top_n):

    # First find the three most similar users to this user

    # D is a dictionary of all the distances to other users
    D = {}
    for u in range(1, n_users):
        if u != user_id:
            D[u] = pcs(user_id, u)

    # sort D by its values (distances)
    sorted_D = sorted(D.items(), key=operator.itemgetter(1))


    # get the smallest n items from sorted_D
    top = sorted_D[:top_n]

    # return the average rating for item i for those of the top three most similar,
    # (counting only those of the three who have rated i)

    # remove any users who have not rated the item
    for t in top:
        if utility[t[0]-1][i_id-1] == 0:
            top.remove(t)

    SUM = 0
    for t in top:
        SUM += utility[t[0]-1][i_id-1]
    if len(top) != 0:
        return SUM / len(top)

    # if none of the top three similar users have rated i,
    else:
        return 2.5

"""
Displays utility matrix and mean squared error.
This is for answering Q1,2 of Part 1.
"""

# Display the utility matrix as given in Part 1 of your project description
set_printoptions(precision=3)
print utility

'''
# Finds the average rating for each user and stores it in the user's object
for i in range(0, n_users):
    user[i].avg_r = mean(utility[i])

'''
n = 3 # Assume top_n users

# Finds all the missing values of the utility matrix
utility_copy = copy(utility)
for i in range(1, n_users):
    for j in range(1, n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i, j, n)

print utility_copy

# Finds the utility values of the particular users in the test set. Refer to Q2
print "Ann's rating for SW2 should be " + str(guess(1, 5, n))
print "Carl's rating for HP1 should be " + str(guess(3, 1, n))
print "Carl's rating for HP2 should be " + str(guess(3, 2, n))
print "Doug's rating for SW1 should be " + str(guess(4, 4, n))
print "Doug's rating for SW2 should be " + str(guess(4, 5, n))

guess = array([guess(1, 5, n), guess(3, 1, n), guess(3, 2, n), guess(4, 4, n), guess(4, 5, n)])

### Ratings from the test set
# Ann rates SW2 with 2 stars
# Carl rates HP1 with 2 stars
# Carl rates HP2 with 2 stars
# Doug rates SW1 with 4 stars
# Doug rates SW 2 with 3 stars

test = array([2, 2, 2, 4, 3])

# Finds the mean squared error of the ratings with respect to the test set
print "Mean Squared Error is " + str(mean_squared_error(guess, test))

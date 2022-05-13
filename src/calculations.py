import numpy as np
import pandas as pd


class BasicFunctions:

    @staticmethod
    def product(users, activities):
        return users.dot(activities)

    @staticmethod
    def distance(users, activities):

        nb_users, _ = users.shape
        _, nb_activities = activities.shape

        recommendations = np.zeros((nb_users, nb_activities))
        for i in range(nb_users):
            for j in range(nb_activities):
                recommendations[i, j] = np.linalg.norm(activities[:, j] - users[i, :])

        return recommendations

    @staticmethod
    def time(users, activities):

        users = users.flatten()
        activities = activities.flatten()

        nb_users = len(users)
        nb_activities = len(activities)
        recommendations = np.zeros((nb_users, nb_activities))
        for i in range(nb_users):
            for j in range(nb_activities):
                if activities[j] > users[i]:
                    recommendations[i, j] = 0
                else:
                    recommendations[i, j] = 1 - (users[i] - activities[j]) / users[i]

        return recommendations


basic_functions = {"Product": BasicFunctions.product, "Distance": BasicFunctions.distance, "Time": BasicFunctions.time}

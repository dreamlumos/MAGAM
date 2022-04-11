from multiprocessing import freeze_support

from pyBKT.models import Model


if __name__ == '__main__':
    freeze_support()
    # Initialize the model with an optional seed
    model = Model(seed = 42, num_fits = 1)

    # Fetch Assistments and CognitiveTutor data (optional - if you have your own dataset, that's fine too!)
    # model.fetch_dataset('https://raw.githubusercontent.com/CAHLR/pyBKT-examples/master/data/as.csv', '.')
    model.fetch_dataset('https://raw.githubusercontent.com/CAHLR/pyBKT-examples/master/data/ct.csv', '../data/bkt_data')

    # Train a simple BKT model on all skills in the CT dataset
    model.fit(data_path = 'ct.csv')
    # model.fit(data_path = '../data/bkt_data/ct.csv')

    # # Train a simple BKT model on one skill in the CT dataset
    # # Note that calling fit deletes any previous trained BKT model!
    # model.fit(data_path = 'ct.csv', skills = "Plot imperfect radical")

    # # Train a simple BKT model on multiple skills in the CT dataset
    # model.fit(data_path = 'ct.csv', skills = ["Plot imperfect radical",
    #                                           "Plot pi"])

    # # Train a multiguess and slip BKT model on multiple skills in the
    # # CT dataset. Note: if you are not using CognitiveTutor or Assistments
    # # data, you may need to provide a column mapping for the guess/slip
    # # classes to use (i.e. if the column name is gsclasses, you would
    # # specify multigs = 'gsclasses' or specify a defaults dictionary
    # # defaults = {'multigs': 'gsclasses'}).
    # model.fit(data_path = 'ct.csv', skills = ["Plot imperfect radical",
    #                                           "Plot pi"],
    #                                 multigs = True)

    # # We can combine multiple model variants.
    # model.fit(data_path = 'ct.csv', skills = ["Plot imperfect radical",
    #                                           "Plot pi"],
    #                                 multigs = True, forgets = True,
    #                                 multilearn = True)

    # # We can use a different column to specify the different learn and 
    # # forget classes. In this case, we use student ID.
    # model.fit(data_path = 'ct.csv', skills = ["Plot imperfect radical",
    #                                           "Plot pi"],
    #                                 multigs = True, forgets = True,
    #                                 multilearn = 'Anon Student Id')

    # View the trained parameters!
    print(model.params())


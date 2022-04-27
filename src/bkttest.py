from multiprocessing import freeze_support

from pyBKT.models import Model

from models.BKTData import *


if __name__ == '__main__':
    # freeze_support()
    
    defaults = {'user_id': 'User', 'skill_name': 'KC', 'correct': 'IsCorrect'}   
    # model.fit(data_path = '../data/eedi_data/quizzing-policy-main/neurips_challenge/train_task_3_4_with_concept.csv', defaults=defaults)

    #d = BKTData('../data/eedi_data/quizzing-policy-main/neurips_challenge/train_task_3_4_with_concept.csv', model_defaults=defaults)
    d = BKTData('../data/bkt_input_2.csv', model_defaults=defaults)
    d.save_preds_to_csv()
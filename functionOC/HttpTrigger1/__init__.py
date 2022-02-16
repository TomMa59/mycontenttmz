import azure.functions as func
import pickle
import numpy as np
import random
from numpyencoder import NumpyEncoder
from operator import itemgetter
import pandas as pd
import json
from io import BytesIO

def main(req: func.HttpRequest, clickuser, cossim) -> func.HttpResponse:
    requete = req.get_json()
    user_id = requete['userId']

    emb_matrix_to_read = BytesIO(cossim.read())
    emb_matrix = pickle.load(emb_matrix_to_read)
    df_click_user = pd.read_csv(BytesIO(clickuser.read()))
    articles_read = df_click_user.loc[user_id]['articles_id_read']
    articles_read = list(map(int,articles_read.replace('[', '').replace(']', '').replace(',', '').split()))
    chosen_article = random.choice(articles_read)
    score = []
    for i in range(0, len(emb_matrix)):
        if(chosen_article != i):
            cos_sim = np.dot(emb_matrix[chosen_article], emb_matrix[i])/(np.linalg.norm(emb_matrix[chosen_article])*np.linalg.norm(emb_matrix[i]))
            score.append(cos_sim)          
    indexed = enumerate(score)
    sorted_scores = sorted(indexed, key=itemgetter(1), reverse=True)
    recommendation = [d[0] for d in sorted_scores[:5]]
    return json.dumps(recommendation, cls=NumpyEncoder)
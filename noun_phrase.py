import numpy as np
import vecs
import sklearn.linear_model


def get_coefficient(vecs, adjective):
    x = []
    y = []
    adj_vec = vecs_dict[adjective]
    for label, vec in vecs.items():
        if label.startswith('{}_'.format(adjective)):
            noun = label.split('_')[1]
            if noun in vecs_dict.keys():
                noun_vec = vecs_dict[noun]
                #x += [np.array([adj_vec, noun_vec])]
                x += [adj_vec * noun_vec]
                y += [vec]
    x = np.array(x)
    print(x.shape)
    y = np.array(y)
    coefs = []
    scores = []
    print('fiting linear models')
    for i in range(300):
        lm = sklearn.linear_model.LinearRegression()
        #lm.fit(x[:, :, i], y[:, i])
        lm.fit(x[:, i].reshape(-1, 1), y[:, i])
        coef = lm.coef_
        #score = lm.score(x[:, :, i], y[:, i])
        score = lm.score(x[:, i].reshape(-1, 1), y[:, i])
        scores.append(score)
        coefs.append(coef)
        #print(i)
        #print(coef)
        #print(score)
    return coefs, scores

if __name__ == '__main__':
    fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.linked.vec'
    vecs_dict = vecs.load_vecs(fname, n=1e6)
    adjectives = ['red',
                  'green',
                  'blue',
                  'yellow']
    for adjective in adjectives:
        coefs, scores = get_coefficient(vecs_dict, adjective)
        print(adjective)
        #print('coefs')
        #print(coefs)
        print('coefs mean and sd')
        print(np.mean(coefs, axis=0))
        print(np.std(coefs, axis=0))
        #print('r squared')
        #print(scores)
        print('r squared mean and sd')
        print(np.mean(scores, axis=0))
        print(np.std(scores, axis=0))

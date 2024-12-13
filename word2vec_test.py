from gensim.models import Word2Vec


if __name__ == '__main__':
    WORD2VEC_MODEL_DIR = './zhwikienergypolicy.word2vec.model'

    word2vec_model = Word2Vec.load(WORD2VEC_MODEL_DIR)

    # 查看词向量
    vec = word2vec_model.wv['光伏']
    print('光伏：', vec)

    # 查看相似词
    sim_words = word2vec_model.wv.most_similar('光伏')
    print('The most similar words: ')
    for w in sim_words:
        print(w)


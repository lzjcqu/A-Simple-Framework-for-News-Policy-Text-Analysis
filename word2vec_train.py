import os, sys
import logging
import multiprocessing
from argparse import ArgumentParser
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def word2vec_train(infile, outmodel, outvector, size, window, min_count):
    '''train the word vectors by word2vec'''
    # train model
    model = Word2Vec(
        sentences=LineSentence(infile),
        vector_size=size,
        window=window,
        min_count=min_count,
        workers=multiprocessing.cpu_count()
    )
    # save model
    model.save(outmodel)
    model.wv.save_word2vec_format(outvector, binary=False)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(program)
    logger.info('running ' + program)

    # parse the parameters
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        dest='infile',
        default='corpus.zhwiki.segwithb.txt',
        help='zhwiki corpus'
    )
    parser.add_argument(
        '-m', '--outmodel',
        dest='wv_model',
        default='zhwiki.word2vec.model',
        help='word2vec model'
    )
    parser.add_argument(
        '-v', '--outvec',
        dest='wv_vectors',
        default='zhwiki.word2vec.vectors',
        help='word2vec vectors'
    )
    parser.add_argument(
        '-s', '--size',
        type=int,
        dest='size',
        default=512,
        help='word vector size'
    )
    parser.add_argument(
        '-w', '--window',
        type=int,
        dest='window',
        default=5,
        help='window size'
    )
    parser.add_argument(
        '-n', '--min_count',
        type=int,
        dest='min_count',
        default=5,
        help='min word frequency'
    )

    options = parser.parse_args()
    infile = options.infile
    outmodel = options.wv_model
    outvec = options.wv_vectors
    vec_size = options.size
    window = options.window
    min_count = options.min_count

    try:
        word2vec_train(infile, outmodel, outvec, vec_size, window, min_count)
        logger.info('word2vec model training finished')
    except Exception as err:
        logger.error(err)
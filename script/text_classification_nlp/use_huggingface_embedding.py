from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def get_sentence_similitay(ori_sentence,contrast_list):
    """得到指定句子之间的相似度"""
    #Compute embedding for both lists
    print('原始的句子')
    print(ori_sentence)
    for sample in contrast_list:
        embedding_1= model.encode(ori_sentence, convert_to_tensor=True)
        embedding_2 = model.encode(sample, convert_to_tensor=True)
        sentence_similitay = util.pytorch_cos_sim(embedding_1, embedding_2).item()
        print(sample)
        print(sentence_similitay)


def get_list():
    question_txt = '/cloud/cloud_disk/users/huh/nlp/smart_home/script/emdbedding/huhao.txt'
    with open(question_txt,'r') as fp:
        contents = fp.readlines()
    contrast_list = []
    for sample in contents:
        contrast_list.append(sample[:-2])
    return contrast_list


def get_top10(ori_sentence,contrast_list):
    sentences_to_similitary = {}
    sentence_similitay_list = []
    for sample in tqdm(contrast_list):
        embedding_1 = model.encode(ori_sentence, convert_to_tensor=True)
        embedding_2 = model.encode(sample, convert_to_tensor=True)
        sentence_similitay = abs(float(round(util.pytorch_cos_sim(embedding_1, embedding_2).item(),8)))
        sentences_to_similitary[sentence_similitay] = sample
        sentence_similitay_list.append(sentence_similitay)
    sentence_similitay_list.sort(reverse=True)
    for count in sentence_similitay_list[:100]:
        print('相似度为')
        print(count)
        print('对应的句子为')
        print(sentences_to_similitary[count])



def get_all_samples(contrast_list):
    xls_list = []
    index = 0
    for sample in tqdm(contrast_list):
        sentences_to_similitary = {}
        sentence_similitay_list = []
        index+=1
        for tmp_sample in contrast_list:
            embedding_1 = model.encode(sample, convert_to_tensor=True)
            embedding_2 = model.encode(tmp_sample, convert_to_tensor=True)
            sentence_similitay = abs(float(round(util.pytorch_cos_sim(embedding_1, embedding_2).item(),8)))
            sentences_to_similitary[sentence_similitay] = tmp_sample
            sentence_similitay_list.append(sentence_similitay)
        sentence_similitay_list.sort(reverse=True)
        xls_list.append('原句子：,{}\n'.format(sample))
        for count in sentence_similitay_list[1:11]:
            xls_list.append(" ,{},{}\n".format(sentences_to_similitary[count],count))
        xls_list.append("\n")
        
        
    with open('embedding.csv','w') as fp:
        fp.writelines(xls_list)



    
if __name__ == '__main__':
    ori_sentence = 'Has anyone found a good way to remove stains on this cat tree? '
    contrast_list = ['Will the cat tower basket fit an adult cat of 18 lbs? ','How big of a cat will this structure hold? One of my cats weight 21 pounds. ','Can these shelves be installed onto concrete walls?','Does the chestnut/natural set in nclude everything in the picture including the planters??']
    #get_sentence_similitay(ori_sentence,contrast_list)
    contrast_list = get_list()
    
    #get_top10(ori_sentence,contrast_list)
    get_all_samples(contrast_list)




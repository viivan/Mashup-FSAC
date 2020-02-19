#输入：服务功能名词集合数组noun_list、服务标签数组tag_list
#输出：存放服务功能语义权重字典的数组noun_list2
def FN(noun_list, tag_list):
    sim_dict={}#名词平均相似度词典
    sim_list=[]#存放各描述文本名词平均相似度的数组
    noun_list2 = []#存放服务功能语义权重字典的数组
    for (temp_set,tag) in zip(noun_list,tag_list):
          for i in temp_set:
              # 初始化初始相似度
              simi=0
              tsim=0
              tagi=tag.split(",")
              for t in tagi:
                  try:
                      t = wordnet_lemmatizer.lemmatize(t.strip().lower(), pos=wordnet.NOUN)
                      senst = wordnet.synset(t + '.n.1')
                      sensi = wordnet.synset(i + '.n.1')
                      sens_path=sensi.path_similarity(senst)
                      if(tsim<sens_path):
                              tsim=sens_path
                  except:
                      continue
              for j in temp_set:
                  if i==j:
                      continue
                  try:
                      sensi=wordnet.synset(i+'.n.1')
                      sensj=wordnet.synset(j+'.n.1')
                      simi += sensi.path_similarity(sensj)/(len(temp_set)-1)
                  except :
                      continue
              if (len(temp_set)==noun_set_len):
                    w=0.5
              else:
                    w=0.5/(abs(len(temp_set)-noun_set_len))
              sim_dict[i]=simi*w+tsim*(1-w)
          temp_list = sorted(sim_dict.items(), key=lambda item: item[1], reverse=True)
          noun_set2 = set() #存放需最终计算的功能名词
          sim_dict ={}
          if len(temp_list)<=noun_set_len:
              for l in temp_list:
                  sim_dict[l[0]] = l[1]
                  noun_set2.add(l[0])
          else:
              index=0
              while(index<noun_set_len): 
                  sim_dict[temp_list[index][0]] = temp_list[index][1]
                  noun_set2.add(temp_list[index][0])
                  index=index+1
          sim_list.append(sim_dict)
          noun_list2.append(noun_set2)
          sim_dict={}
    return noun_list2
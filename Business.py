__author__ = 'shuchenwu'
import json
import random
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt


# "attributes": {"Alcohol": "full_bar", "Noise Level": "average", "Has TV": true, "Attire": "casual", "Ambience": {"romantic": false, "intimate": false, "classy": false, "hipster": false, "divey": false, "touristy": false, "trendy": false, "upscale": false, "casual": false}, "Good for Kids": true, "Price Range": 1, "Good For Dancing": false, "Delivery": false, "Coat Check": false, "Smoking": "no", "Accepts Credit Cards": true, "Take-out": true, "Happy Hour": false, "Outdoor Seating": false, "Takes Reservations": false, "Waiter Service": true, "Wi-Fi": "no", "Caters": true, "Good For": {"dessert": false, "latenight": false, "lunch": false, "dinner": false, "breakfast": false, "brunch": false}, "Parking": {"garage": false, "street": false, "validated": false, "lot": false, "valet": false}, "Music": {"dj": false}, "Good For Groups": true}, "type": "business"}
# Infer what type of restaurant based on atomsphere

class Business:
    def __init__(self,Busin_json):
        self.city = Busin_json['city']
        self.latitude = Busin_json['latitude']
        self.longitude = Busin_json['longitude']
        self.stars = Busin_json['stars']
        self.categories = Busin_json['categories']
        self.open = Busin_json['open']
        attributes = Busin_json['attributes']
        tag = []
        if "attire" in attributes:
            tag.append(attributes['attire'])
        if "Ambience" in attributes:
            for key in attributes['Ambience']:
                if attributes['Ambience'][key] == 'true':
                    tag.append(key)
        self.tag = tag

        goodfor = []
        if "Good For" in attributes:
            for key in attributes['Good For']:
                if attributes['Good For'][key] == 'true':
                    goodfor.append(key)
        self.goodfor = goodfor
        if "Delivery" in attributes:
            self.delivery = attributes['Delivery']
        if "Take-out" in attributes:
            self.take_out = attributes['Take-out']

        if 'Price Range' in attributes:
            self.priceRange = attributes['Price Range']

        if 'hours' in Busin_json:
            sum_time = 0
            for item in Busin_json['hours']:
                close_hour =Busin_json['hours'][item]['close'].split(':')
                open_hour = Busin_json['hours'][item]['open'].split(':') #length 2 integer
                time = int(close_hour[0]) - int(open_hour[0])
                sum_time=sum_time+ time# in hours


def dividebag(business_dict, feature):  #feature needs to be a string, where datadict needs to be a dictionary of datasets
    # divide into training set and test set
    #Shuffle keys
    Shuffle = []
    for key in business_dict:
        Shuffle.append(key)
    random.shuffle(Shuffle)

    count_45 = 0

    business = []
    rating = []
    for item in Shuffle:
        if 'Restaurants' in business_dict[item].categories:
            if (business_dict[item].stars in feature):
                count_45 = count_45+1
                # if business_dict[item].stars == 4.5:
                #     print(4.5)
                # if business_dict[item].stars == 4.5:
                #     print(4.0)
                #,business_dict[item].priceRange
                list = [''.join(business_dict[item].categories),
                        ''.join(business_dict[item].goodfor),''.join(business_dict[item].tag),''.join(business_dict[item].categories)]
                String = ''.join(list)

                try:
                    if business_dict[item].take_out == 'true':
                        String = ''.join([String, 'takeout'])
                except AttributeError:{}
                try:
                    if business_dict[item].delivery == 'true':
                        String = ''.join([String, 'delivery'])
                except AttributeError:{}


                business.append(String)
                rating.append(int(10*business_dict[item].stars))
    length = int(len(business)*0.8)
    train_business = business[0:length]
    train_rating = rating[0:length]
    test_business = business[length+1:len(business)]
    test_rating = rating[length+1:len(rating)]

    #training data
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(train_business)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    # Rating_train_tfidf = tfidf_transformer.fit_transform(Rating_train)
    X_train_tfidf.shape
    clf = MultinomialNB().fit(X_train_tfidf, train_rating)




    # test data
    X_new_counts = count_vect.transform(test_business)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    true = test_rating

    # plot confusion matrix
    cm = confusion_matrix(true, predicted)
    print(cm)
    print('accuracy is:')
    print(np.mean(predicted == true))
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    # normalized confusion matrix
    print('Normalized confusion matrix')
    print(cm_normalized)
    print(metrics.classification_report(true, predicted))

    cm = confusion_matrix(true, predicted)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    plt.figure()
    plot_confusion_matrix(cm, feature)

    plt.show()

    return count_45


def plot_confusion_matrix(cm,feature, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, feature, rotation=45)
    plt.yticks(tick_marks, feature)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

business = dict()

file_business=open("/Users/shuchenwu/Documents/PycharmProjects/yelp/yelp_academic_dataset_business.json","r")
lines=file_business.readlines()
for line in lines:
    info=json.loads(line)
    if info['review_count']>5:
        business[info['business_id']]= Business(info)

file_business.close()

# dividebag(business, [4.5,5])
# dividebag(business, [4,4.5])
dividebag(business, [2,3,4,5])
# dividebag(business, [3,3.5])
# dividebag(business, [2.5,3])
# dividebag(business, [2,2.5])

# mine association rule based on type of restaurent



print("done")
# use bag of words to do classification:

# use svm, random forest and naive bayes and plot



import tensorflow as tf
import json
import operator
import pandas as pd
# from google.colab import drive


bestestProducts = []
bestProducts = []
tupleProducts = []


def model(scrapedData):
    tupleProducts.clear()
    bestestProducts.clear()
    try:
        CSV_COLUMN_NAMES = ['price', 'ratings', 'reviews', 'recommend']
        OUTPUTS = ['Recommended', 'Not Recommended']
        train = pd.read_csv('ptest.csv',
                            names=CSV_COLUMN_NAMES, header=0)
        test = pd.read_csv('etest.csv',
                           names=CSV_COLUMN_NAMES, header=0)
        train_y = train.pop('recommend')
        test_y = test.pop('recommend')
    except:
        print("some problem in getting dataset ")

    def input_fn(features, labels, training=True, batch_size=256):
        """An input function for training or evaluating"""
        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
        # Shuffle and repeat if you are in training mode.
        if training:
            dataset = dataset.shuffle(1000).repeat()
        return dataset.batch(batch_size)

    # Feature columns describe how to use the input.
    try:
        my_feature_columns = []
        for key in train.keys():
            my_feature_columns.append(
                tf.feature_column.numeric_column(key=key))
    except:
        print("features columns me masti")

    try:
        # Build a DNN with 2 hidden layers with 30 and 10 hidden nodes each.
        classifier = tf.estimator.DNNClassifier(
            feature_columns=my_feature_columns,
            # Two hidden layers of 30 and 10 nodes respectively.
            hidden_units=[30, 10],
            # The model must choose between 3 classes.
            n_classes=2)
    except:
        print("model bnane me masti")

    try:
        # Train the Model.
        classifier.train(
            input_fn=lambda: input_fn(train, train_y, training=True),
            steps=5000)
    except:
        print("training model me masti")

    try:
        eval_result = classifier.evaluate(
            input_fn=lambda: input_fn(test, test_y, training=False))
    except:
        print("evaluation me masti ")

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # Generate predictions from the model
    expected = ['Recommended', 'Not Recommended']

    # with open('dataset/products.json') as data:
    #     dbmaal = json.load(data)

    try:
        print(len(scrapedData))

        def modelWorker(scrapedData):
            dbmaal = scrapedData
            print(len(dbmaal))
            result = {}
            for i in range(0, len(dbmaal)):
                predict_x = {
                    'price': [dbmaal[i]['price']],
                    'ratings': [dbmaal[i]['ratings']],
                    'reviews': [dbmaal[i]['reviews']],
                }

                def input_fn(features, batch_size=256):
                    """An input function for prediction."""
                    # Convert the inputs to a Dataset without labels.
                    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

                predictions = classifier.predict(
                    input_fn=lambda: input_fn(predict_x))
                for pred_dict, expec in zip(predictions, expected):
                    class_id = pred_dict['class_ids'][0]
                    probability = pred_dict['probabilities'][class_id]
                    print("---------------------------------THIS IS FOR PRODUCT NUMBER", +
                          i+1, "------------------------")
                    print(100 * probability,
                          dbmaal[i]['ASIN'], OUTPUTS[class_id])
                    if(expec == "Recommended" and dbmaal[i]['price'] != 0.0 and dbmaal[i]['ratings'] >= 4.3 or dbmaal[i]['price'] >= 50 or dbmaal[i]['amazonChoice'] == "true" or dbmaal[i]['bestSeller'] == "true"):
                        result[dbmaal[i]['ASIN']] = 100 * probability
                        result.update(result)
                    # print('Prediction is "{}" ({:.1f}%), expected "{}"'.format(
                    #     OUTPUTS[class_id], 100 * probability, expec), dbmaal[i]['ASIN'])

            print(len(result))
            try:
                def recommendedProducts():
                    sort = sorted(result.items(),
                                  key=operator.itemgetter(1), reverse=True)
                    if(len(result) < 3 and len(result) > 0):
                        print("less than 3 wala")
                        if(len(result) == 2):
                            for i in range(0, 2):
                                tupleProducts.append(sort[i])
                                bestProducts = dict(tupleProducts)
                                bestProducts.update(bestProducts)
                            bestestProducts.append(bestProducts.copy())
                            bestProducts.clear()
                        elif(len(result) == 1):
                            bestProducts = dict(result)
                            bestestProducts.append(bestProducts.copy())
                            bestProducts.clear()
                    elif(len(result) >= 3):
                        for i in range(0, 3):
                            tupleProducts.append(sort[i])
                            bestProducts = dict(tupleProducts)
                            bestProducts.update(bestProducts)
                        bestestProducts.append(bestProducts.copy())
                        bestProducts.clear()
                        # return(bestProducts)
                    else:
                        bestProducts = dict(result)
                        bestestProducts.append(bestProducts.copy())
                        bestProducts.clear()
                        # return(bestestProducts)
                recommendedProducts()
            except:
                print("sorting me masti")
        modelWorker(scrapedData)
    except:
        print("real time processing me masti")
    return(bestestProducts)


# model( [{
#     "_id": {
#         "$oid": "622c7bd0cc776bea085092a3"
#     },
#     "title": "Logitech Brio 4K Webcam, Ultra 4K HD Video Calling, Noise-Canceling mic, HD Auto Light Correction, Wide Field of View, Works with Microsoft Teams, Zoom, Google Voice, PC/Mac/Laptop/Macbook/Tablet",
#     "price": 0,
#     "amazonChoice": "true",
#     "bestSeller": "false",
#     "ratings": 10060,
#     "reviews": 4.6,
#     "image": "https://m.media-amazon.com/images/I/61OQP2+yqML._AC_SY450_.jpg",
#     "sellersStore": "https://www.amazon.com/stores/Logitech/page/01EFDE77-7D1A-41D7-9EEA-7C2FA22AB12F?ref_=ast_bln",
#     "pageUrl": "https://www.amazon.com/Logitech-Calling-Noise-Canceling-Correction-Microsoft/dp/B01N5UOYC4/ref=sr_1_1?qid=1647081706&rnid=172456&s=computers-intl-ship&sr=1-1",
#     "ASIN": "B01N5UOYC4",
#     "Customer Reviews": "10,060 ratings\n4.6 out of 5 stars",
#     "Best Sellers Rank": "1",
#     "Wireless Type": "Radio Frequency"
# }, {
#     "_id": {
#         "$oid": "622c7bd0cc776bea085092a4"
#     },
#     "title": "Logitech H390 Wired Headset, Stereo Headphones with Noise-Cancelling Microphone, USB, In-Line Controls, PC/Mac/Laptop - Black",
#     "ASIN": "B000UXZQ42",
#     "price": 0,
#     "amazonChoice": "false",
#     "bestSeller": "true",
#     "ratings": 36361,
#     "reviews": 4.4,
#     "image": "https://m.media-amazon.com/images/I/61CqYq+xwNL._AC_SY355_.jpg",
#     "sellersStore": "https://www.amazon.com/stores/Logitech/page/01EFDE77-7D1A-41D7-9EEA-7C2FA22AB12F?ref_=ast_bln",
#     "pageUrl": "https://www.amazon.com/Logitech-Headset-H390-Noise-Cancelling/dp/B000UXZQ42/ref=sr_1_2?qid=1647081706&rnid=172456&s=computers-intl-ship&sr=1-2",
#     "Product Dimensions": "3.23 x 8.35 x 10.24",
#     "Item Weight": "7",
#     "Item model number": "981-000014",
#     "Batteries": "1 Lithium ion batteries required.",
#     "Customer Reviews": "36,361 ratings\n4.4 out of 5 stars",
#     "Best Sellers Rank": "1",
#     "Is Discontinued By Manufacturer": "No",
#     "Date First Available": "August 9, 2007",
#     "Department": "Mobile-Cordless-Office Headsets",
#     "Manufacturer": "Logitech",
#     "Language": "English"
# }, {
#     "_id": {
#         "$oid": "622c7bd1cc776bea085092a5"
#     },
#     "title": "HyperX QuadCast - USB Condenser Gaming Microphone, for PC, PS4, PS5 and Mac, Anti-Vibration Shock Mount, Four Polar Patterns, Pop Filter, Gain Control, Podcasts, Twitch, YouTube, Discord, Red LED",
#     "ASIN": "B07NZZZ746",
#     "price": 89.99,
#     "amazonChoice": "true",
#     "bestSeller": "false",
#     "ratings": 18136,
#     "reviews": 4.8,
#     "image": "https://m.media-amazon.com/images/I/71nozlRTz3L._AC_SY450_.jpg",
#     "sellersStore": "https://www.amazon.com/stores/HyperX/page/C3BFE396-3717-4B59-A6EA-0A070E7654D1?ref_=ast_bln",
#     "pageUrl": "https://www.amazon.com/HyperX-QuadCast-Condenser-Microphone-Anti-Vibration/dp/B07NZZZ746/ref=sr_1_3?qid=1647081706&rnid=172456&s=computers-intl-ship&sr=1-3",
#     "Customer Reviews": "18,136 ratings\n4.8 out of 5 stars",
#     "Best Sellers Rank": "1"
# }, {
#     "_id": {
#         "$oid": "622c7bd1cc776bea085092a6"
#     },
#     "title": "Logitech C270 HD Webcam, HD 720p, Widescreen HD Video Calling, HD Light Correction, Noise-Reducing Mic, For Skype, FaceTime, Hangouts, WebEx, PC/Mac/Laptop/Macbook/Tablet - Black",
#     "ASIN": "B004FHO5Y6",
#     "price": 21.99,
#     "amazonChoice": "true",
#     "bestSeller": "false",
#     "ratings": 12928,
#     "reviews": 4.5,
#     "image": "https://m.media-amazon.com/images/I/61yo4swj-PL._AC_SY355_.jpg",
#     "sellersStore": "https://www.amazon.com/stores/Logitech/page/01EFDE77-7D1A-41D7-9EEA-7C2FA22AB12F?ref_=ast_bln",
#     "pageUrl": "https://www.amazon.com/Logitech-Desktop-Widescreen-Calling-Recording/dp/B004FHO5Y6/ref=sr_1_4?qid=1647081706&rnid=172456&s=computers-intl-ship&sr=1-4",
#     "Product Dimensions": "9.85 x 4.94 x 6.45",
#     "Item Weight": "4.6",
#     "Manufacturer": "Logitech",
#     "Item model number": "960-000694",
#     "Batteries": "1 Lithium ion batteries required.",
#     "Customer Reviews": "12,928 ratings\n4.5 out of 5 stars",
#     "Best Sellers Rank": "4",
#     "Is Discontinued By Manufacturer": "No",
#     "Date First Available": "December 26, 2010"
# }]
# )

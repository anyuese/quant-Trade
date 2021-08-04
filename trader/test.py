# stacking
% load_ext
nb_black


def rf_reg(x_train, y_train, x_valid, kf, label_split=None):
    randomforest = RandomForestRegressor(n_estimators=600,
                                         max_depth=20,
                                         n_jobs=-1,
                                         random_state=2017,
                                         max_features='auto',
                                         verbose=1)
    rf_train, rf_test = stacking_reg(randomforest,
                                     x_train,
                                     y_train,
                                     x_valid,
                                     'rf',
                                     kf,
                                     label_split=label_split)
    return rf_train, rf_test, 'rf_reg'


def ada_reg(x_train, y_train, x_valid, kf, label_split=None):
    adaboost = AdaBoostRegressor(n_estimators=30,
                                 random_state=2017,
                                 learning_rate=0.01)
    aba_train, ada_test = stacking_reg(adaboost,
                                       x_train,
                                       y_train,
                                       x_valid,
                                       'ada',
                                       kf,
                                       label_split=label_split)
    return ada_train, ada_test, 'ada_reg'


def gb_reg(x_train, y_train, x_valid, kf, label_split=None):
    gbdt = GradientBoostingRegressor(n_estimators=100,
                                     random_state=2017,
                                     subsample=0.8,
                                     learning_rate=0.04,
                                     max_depth=5,
                                     verbose=1)
    gbdt_train, gbdt_test = stacking_reg(adaboost,
                                         x_train,
                                         y_train,
                                         x_valid,
                                         'gb',
                                         kf,
                                         label_split=label_split)
    return gbdt_train, gbdt_test, 'gbdt_reg'


def et_reg(x_train, y_train, x_valid, kf, label_split=None):
    extratree = ExtraTreesRegressor(n_estimators=600,
                                    random_state=2017,
                                    max_features='auto',
                                    max_depth=35,
                                    learning_rate=0.04,
                                    n_jobs=-1,
                                    verbose=1)
    et_train, et_test = stacking_reg(adaboost,
                                     x_train,
                                     y_train,
                                     x_valid,
                                     'et',
                                     kf,
                                     label_split=label_split)
    return et_train, et_test, 'et_reg'


def lr_reg(x_train, y_train, x_valid, kf, label_split=None):
    lr_reg = LinearRegression(n_jobs=-1)
    lr_train, lr_test = stacking_reg(adaboost,
                                     x_train,
                                     y_train,
                                     x_valid,
                                     'lr',
                                     kf,
                                     label_split=label_split)
    return lr_train, lr_test, 'et_reg'


def xgb_reg(x_train, y_train, x_valid, kf, label_split=None):
    xgb_train, xgb_test = stacking_reg(xgboost,
                                       x_train,
                                       y_train,
                                       x_valid,
                                       'lr',
                                       kf,
                                       label_split=label_split)
    return xgb_train, xgb_test, 'xgb_reg'


def lgb_reg(x_train, y_train, x_valid, kf, label_split=None):
    lgb_train, lgb_test = stacking_reg(xgboost,
                                       x_train,
                                       y_train,
                                       x_valid,
                                       'lr',
                                       kf,
                                       label_split=label_split)
    return xgb_train, xgb_test, 'xgb_reg'


def stacking_pred(x_train, y_train,
                  x_valid, kf,
                  clf_list, label_split=None,
                  clf_fin='lgb',
                  if_concat_origin=True
                  ):
    for k, clf_list in enumerate(clf_list):
        clf_list = [clf_list]
        column_list = []
        train_data_list = []
        test_data_list = []
        for clf in clf_list:
            train_data, test_data, clf_name = clf(
                x_train,
                y_train,
                x_valid,
                kf,
                label_split=label_split
            )
            train_data_list.append(train_data)
            test_data_list.append(test_data)
            column_list.append('clf_%s' % (clf_name))
        train = np.concatenate(train_data_list, axis=1)
        test = np.concatenate(test_data_list, axis=1)

        if if_concat_origin:
            train = np.concatenate([x_train, train], axis=1)
            test = np.concatenate([x_valid, test], axis=1)
        print(x_train.shape)
        print(train.shape)
        print(clf_name)

        if clf_fin in ['rf', 'ada', 'gb', 'et', 'lr', 'lsvc', 'knn']:
            if clf_fin in ['rf']:
                clf = RandomForestRegressor(n_estimators=600,
                                            max_depth=20,
                                            n_jobs=-1,
                                            random_state=2017,
                                            max_features='auto',
                                            verbose=1)
            elif clf_fin in ['ada']:
                clf = AdaBoostRegressor(n_estimators=30,
                                        random_state=2017,
                                        learning_rate=0.01)

            elif clf_fin in ['gb']:
                clf = GradientBoostingRegressor(n_estimators=100,
                                                random_state=2017,
                                                subsample=0.8,
                                                learning_rate=0.04,
                                                max_depth=5,
                                                verbose=1)
            elif clf_fin in ['et']:
                clf = ExtraTreesRegressor(n_estimators=600,
                                          random_state=2017,
                                          max_features='auto',
                                          max_depth=35,
                                          learning_rate=0.04,
                                          n_jobs=-1,
                                          verbose=1)
            elif clf_fin in ['lr']:
                clf = LinearRegression(n_jobs=-1)
            clf.fit(train, y_train)
            pre = clf.predict(test).reshape(-1, 1)
            return pre
        elif clf_fin in ['xgb']:
            train_matrix = clf.DMatrix(train, label=y_train)
            test_matrix = clf.DMatrix(train, label=y_train)

            params = {
                'booster': 'gbtree',
                'eval_metric': 'rmse',
                'gama': 1,
                'min_child_weight': 1.5,
                'max_depth': 5,
                'lambda': 10,
                'subsample': 0.7,
                'colsample_bytree': 0.7,
                'colsample_bylevel': 0.7,
                'eta': 0.03,
                'tree_method': 'exact',
                'seed': 2017,
                'nthread': 12

            }
            num_round = 10000
            early_stopping_rounds = 100
            watchlist = [(train_matrix, 'train'), (test_matrixa, 'test')]
            model = clf.train(
                params,
                train_matrix,
                num_boost_round=num_round,
                evals=watchlist,
                early_stopping_rounds=early_stopping_rounds)
            pre = model.predict(test,
                                ntree_limit=model.best_ntree_limit).reshape(-1, 1)
            return pre
        elif clf_fin in ['lgb']:
            print(clf_name)
            clf = lightgbm
            model = clf.train(
                params,
                train_matrix,
                num_boost_round=num_round,
                evals=watchlist,
                early_stopping_rounds=early_stopping_rounds)
            print('pred')
            pre = model.predict(test,
                                ntree_limit=model.best_ntree_limit).reshape(-1, 1)
            print(pre)
            return pre

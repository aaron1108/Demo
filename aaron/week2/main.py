from test_class import test_process


if __name__ == '__main__':

    try:

        test = test_process()

        test.login('https://hall.vir999.net/?tpl=bb-in', "繁體", 'bbin', 'hk4g4504')

        test.switch_page('局查詢')

        test.search_by_round('BB電子', '注單編號', '520000897873')

    except Exception as e:

        print(e)

    finally:

        test.finsh()
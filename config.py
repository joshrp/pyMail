settings = {
    'services':
        {
            'smtp':
                {
                    'on': True,
                    'welcome': 'Hai Guyz!',
                    'port': 25, #default = 25
                    'events':{
                        'beforeDelivery':[],
                        'afterDelivery':[],
                        'beforeLocalDelivery':[],
                        'afterLocalDelivery':[],
                        'beforeRemoteDelivery':[],
                        'afterRemoteDelivery':[],
                        'onHelo':[],
                        'afterHelo':[],
                        'onMail':[],
                        'afterMail':[],
                        'onRcpt':[],
                        'afterRcpt':[],
                    }
                },
            'smtps':
                {
                    'on': False
                },
            'imap':
                {
                    'on': True,
                    'port': 143
                },
        },
    'db':
        {
            'module': 'pyMongo',
            'dsn': '',
            'user': '',
            'pass': '',
        }
}
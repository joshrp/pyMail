settings = {
    'services':
        {
            'smtp':
                {
                    'on': True,
                    'welcome': 'Hai Guyz!',
                    'port': 25 #default = 25
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
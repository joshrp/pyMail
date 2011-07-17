domains:[
    name: 'dev.com',
    transport: 'DB',
    active: 1,
    aliases: ['dev.co.uk', 'dev.net'],
    signing:{
        cert: 'path/to/cert',
        additionalHeaders:[]
    },
    options:{
        userLimit: 50,
        sizeLimit: '1'
    },
    users:[{
        name: 'test',
        password: '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8',
        sizeLimit: '50',
        options:[],
        groups: [2], 
        mailboxes: [1,2,3,4]
    }],
    groups:[{
        _id: 1,
        name: 'Test Group',
        address: 'testgroup',
        options:[] 
    }]
]

mailboxes:[
    {
        id: '1',
        name: 'Inbox',
        ancestry: [],
        messages:[
            {
                id: '123',
                flags: [] ,
                tags: [] 
            }
        ]       
    },
    {
        id: '2',
        name: 'Trash',
        ancestry: ['Inbox'],
        messages:[
            {
                id: '456',
                flags: [] ,
                tags: []
            }
        ]       
    },
    {
        id: '3',
        name: 'Custom',
        ancestry: ['Inbox'],
        messages:[
            {
                id: '789',
                flags: [] ,
                tags: [] 
            }
        ]       
    },
]

mail:[
    {
        _id: '123', 
        headers: [{
            key: 'To',
            value: 'Fred',
        }],
        rawHeaders: 'To: Fred',
        body: [{
            code: 'asdfasdfasdfasdfasd',
            headers: '',
            content: 'Hai'  
        }],
        rawBody: '' 
    },
    {
        _id: '456', 
        headers: [{
            key: 'To',
            value: 'Bob',
        }],
        rawHeaders: 'To: Bob',
        body: [{
            code: 'asdfasdfasdfasdfasd',
            headers: '',
            content: 'Hai2' 
        }],
        rawBody: '' 
    },
    {
        _id: '789' ,
        headers: [{
            key: 'To',
            value: 'George',
        }],
        rawHeaders: 'To: George',
        body: [{
            code: 'asdfasdfasdfasdfasd',
            headers: '',
            content: 'Hai3' 
        }],
        rawBody: '' 
    },
]
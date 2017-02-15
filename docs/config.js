self.$config = {
    title: 'XiaoKai Bot 文档',
    home: 'https://raw.githubusercontent.com/CCZU-DEV/xiaokai-bot/master/README.md',
    repo: 'CCZU-DEV/xiaokai-bot',
    url: 'https://cczu-dev.github.io/xiaokai-bot',
    nav: {
        default: [
            {
                title: '首页', path: '/'
            },
            {
                title: '消息源列表', path: '/Message_Sources'
            },
            {
                title: '开发', type: 'dropdown',
                items: [
                    {
                        title: '统一消息上下文', path: '/Context'
                    },
                    {
                        title: '编写消息源适配器', path: '/Write_Adapter'
                    },
                    {
                        title: '编写过滤器', path: '/Write_Filter'
                    },
                    {
                        title: '编写命令', path: '/Write_Command'
                    },
                    {
                        title: '编写自然语言处理器', path: '/Write_NLProcessor'
                    }
                ]
            }
        ]
    },
    plugins: []
};

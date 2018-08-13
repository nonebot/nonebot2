module.exports = {
    title: 'NoneBot',
    description: '基于酷 Q 的 Python 异步 QQ 机器人框架',
    themeConfig: {
        repo: 'richardchien/none-bot',
        docsDir: 'docs',
        editLinks: true,
        editLinkText: '编辑页面',
        lastUpdated: '上次更新',
        nav: [
            { text: '指南', link: '/guide/' },
        ],
        sidebar: {
            '/guide/': [
                '',
                'installation',
                'getting-started',
            ]
        },
    }
}

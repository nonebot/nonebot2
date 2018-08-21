module.exports = {
    title: 'NoneBot',
    description: '基于酷 Q 的 Python 异步 QQ 机器人框架',
    // serviceWorker: true,
    markdown: {
        lineNumbers: true
    },
    themeConfig: {
        repo: 'richardchien/none-bot',
        docsDir: 'docs',
        editLinks: true,
        editLinkText: '在 GitHub 上编辑此页',
        lastUpdated: '上次更新',
        activeHeaderLinks: false,
        nav: [
            { text: '指南', link: '/guide/' },
            { text: '进阶', link: '/advanced/' },
            { text: '配置', link: '/configurations.md' },
            { text: '术语表', link: '/glossary.md' },
        ],
        sidebar: {
            '/guide/': [
                {
                    title: '指南',
                    collapsable: false,
                    children: [
                        '',
                        'installation',
                        'getting-started',
                        'whats-happened',
                        'basic-configurations',
                        'writing-commands',
                        'writing-nl-processors',
                        'tuling',
                        'handling-notices-and-requests',
                        'whats-next',
                    ]
                }
            ],
            '/advanced/': [
                {
                    title: '进阶',
                    collapsable: false,
                    children: [
                        '',
                    ]
                }
            ],
        },
    }
}

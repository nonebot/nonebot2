self.$config = {
  title: 'XiaoKai Bot 文档',
  home: 'https://raw.githubusercontent.com/CCZU-DEV/xiaokai-bot/master/README.md',
  repo: 'CCZU-DEV/xiaokai-bot',
  url: 'https://cczu-dev.github.io/xiaokai-bot',
  'edit-link': 'https://github.com/CCZU-DEV/xiaokai-bot/blob/master/docs',
  nav: {
    default: [
      {
        title: '首页', path: '/'
      },
      {
        title: '编写插件', type: 'dropdown',
        items: [
          {
            title: '过滤器', path: '/Write_Filter'
          },
          {
            title: '命令', path: '/Write_Command'
          }
        ]
      }
    ]
  },
  plugins: []
}

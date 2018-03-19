import Index from './Main.vue'

export const loginRouter = {
  path: '/login',
  name: 'login',
  meta: {
    title: 'Login - 登录'
  },
  component: resolve => {
    require(['./Login.vue'], resolve);
  }
};
export const locking = {
  path: '/locking',
  name: 'locking',
  component: resolve => {
    require(['./main_components/locking-page.vue'], resolve)
  }
}

export const page404 = {
  path: '/*',
  name: 'error_404',
  meta: {
    title: '404-页面不存在'
  },
  component: resolve => {
    require(['./components/Error/404.vue'], resolve);
  }
};

export const page401 = {
  path: '/401',
  meta: {
    title: '401-权限不足'
  },
  name: 'error_401',
  component: resolve => {
    require(['./components/Error/401.vue'], resolve);
  }
};

export const page500 = {
  path: '/500',
  meta: {
    title: '500-服务端错误'
  },
  name: 'error_500',
  component: resolve => {
    require(['./components/Error/500.vue'], resolve);
  }
};

export const appRouter = [
  {
    path: '/',
    icon: 'home',
    name: 'main',
    title: '首页',
    component: Index,
    redirect: '/home',
    children: [
      {
        path: 'home',
        title: '首页',
        name: 'home_index',
        component: resolve => {
          require(['./components/home/home.vue'], resolve);
        }
      }, {
        path: 'ownspace',
        title: '个人中心',
        name: 'ownspace_index',
        component: resolve => {
          require(['./components/Myself/own-space.vue'], resolve);
        }
      }, {
        path: 'message',
        title: '消息中心',
        name: 'message_index',
        component: resolve => {
          require(['./components/Myself/message.vue'], resolve);
        }
      }
    ]
  }, {
    path: '/order',
    icon: 'folder',
    name: 'order',
    title: '数据库工单',
    component: Index,
    children: [
      {
        path: 'myorder',
        name: 'myorder',
        title: '我的工单',
        'icon': 'person',
        component: resolve => {
          require(['./components/Order/MyOrder.vue'], resolve)
        }
      }, {
        path: 'dmledit',
        name: 'dmledit',
        title: '发起工单',
        'icon': 'code',
        component: resolve => {
          require(['./components/Order/SQLsyntax.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/management',
    icon: 'social-buffer',
    name: 'sql-approver',
    title: '数据库管理',
    access: 2,
    component: Index,
    children: [
      {
        path: 'management-audit',
        name: 'management-audit-approver',
        title: '审核',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Management/AuditSql.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/management',
    icon: 'social-buffer',
    name: 'sql-executer',
    title: '数据库管理',
    access: 3,
    component: Index,
    children: [
      {
        path: 'management-execute',
        name: 'management-execute-man',
        title: '执行',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Management/ExecuteSql.vue'], resolve)
        }
      }, {
        path: 'management-record',
        name: 'management-record-1',
        title: '执行记录',
        'icon': 'android-drafts',
        component: resolve => {
          require(['./components/Management/Record.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/management',
    icon: 'social-buffer',
    name: 'management',
    title: '数据库管理',
    access: 0,
    component: Index,
    children: [
      {
        path: 'management-user',
        name: 'management-user',
        title: '用户',
        'icon': 'person-stalker',
        component: resolve => {
          require(['./components/Management/UserInfo.vue'], resolve)
        }
      }, {
        path: 'management-database',
        name: 'management-database',
        title: '数据库',
        'icon': 'social-buffer',
        component: resolve => {
          require(['./components/Management/MamagementBase.vue'], resolve)
        }
      }, {
        path: 'management-audit',
        name: 'management-audit',
        title: '审核',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Management/AuditSql.vue'], resolve)
        }
      }, {
        path: 'management-execute',
        name: 'management-execute',
        title: '执行',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Management/ExecuteSql.vue'], resolve)
        }
      }, {
        path: 'management-record',
        name: 'management-record',
        title: '执行记录',
        'icon': 'android-drafts',
        component: resolve => {
          require(['./components/Management/Record.vue'], resolve)
        }
      }, {
        path: 'ddledit',
        name: 'ddledit',
        title: '表结构修改',
        'icon': 'compose',
        component: resolve => {
          require(['./components/Order/GenSQL.vue'], resolve)
        }
      }, {
        path: 'indexedit',
        name: 'indexedit',
        title: '索引修改',
        'icon': 'share',
        component: resolve => {
          require(['./components/Order/GenIndex.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/view',
    icon: 'search',
    name: 'view',
    title: '数据库查看',
    access: 0,
    component: Index,
    children: [
      {
        path: 'view-dml',
        name: 'view-dml',
        title: '数据库字典',
        'icon': 'ios-book',
        component: resolve => {
          require(['./components/Search/DataBaseDic.vue'], resolve)
        }
      },
      {
        path: 'serach-sql',
        name: 'serach-sql',
        title: 'SQL查询',
        'icon': 'qr-scanner',
        component: resolve => {
          require(['./components/Search/SearchSQL.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/logger',
    icon: 'social-buffer',
    name: 'logger',
    title: '日志服务',
    component: Index,
    children: [
      {
        path: 'logger-view',
        name: 'logger-mywork',
        title: '日志工单',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Logger/MyLogOrder.vue'], resolve)
        }
      },
      {
        path: 'logger-view',
        name: 'logger-view',
        title: '实时日志显示',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Logger/LoggerView.vue'], resolve)
        }
      },
      {
        path: 'logger-view',
        name: 'logger-view-full',
        title: '查看文件内容',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Logger/LoggerViewFull.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/logger',
    icon: 'social-buffer',
    name: 'logger-manager',
    title: '日志管理',
    access: 0,
    component: Index,
    children: [
      {
        path: 'logger-manager',
        name: 'logger-manager',
        title: '日志配置',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Logger/LoggerManager.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/mycommand',
    icon: 'social-buffer',
    name: 'my-command',
    title: '检查命令',
    access: 0,
    component: Index,
    children: [
      {
        path: 'my-command',
        name: 'my-command-index',
        title: '服务器检查',
        'icon': 'edit',
        component: resolve => {
          require(['./components/MyCommand/MyCommand.vue'], resolve)
        }
      }
    ]
  }, {
    path: '/asset',
    icon: 'social-buffer',
    name: 'asset-manager',
    title: '资产管理',
    access: 0,
    component: Index,
    children: [
        {
        path: 'asset-manage',
        name: 'asset-manage-add',
        title: '添加资产',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Asset/AssetManager.vue'], resolve)
          }
        },
        {
        path: 'asset-list',
        name: 'asset-manage-list',
        title: '资产清单',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Asset/AssetList.vue'], resolve)
          }
        },
        {
        path: 'host-manage',
        name: 'host-manage-add',
        title: '添加主机',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Asset/HostManager.vue'], resolve)
          }
        },
        {
        path: 'host-list',
        name: 'host-manage-list',
        title: '主机清单',
        'icon': 'edit',
        component: resolve => {
          require(['./components/Asset/HostList.vue'], resolve)
          }
        }
    ]
  }
]

export const orderList = {
  path: '/',
  icon: 'home',
  name: 'main',
  title: '首页',
  component: Index,
  redirect: '/home',
  children: [
    {
      path: 'orderlist',
      title: '工单详情',
      name: 'orderlist',
      component: resolve => {
        require(['./components/Order/MyorderList.vue'], resolve)
      }
    }
  ]
};
export const MainRoute = [
  loginRouter,
  locking,
  ...appRouter,
  orderList,
  page404,
  page401,
  page500
]

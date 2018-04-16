<style lang="less">
  @import '../../styles/common.less';
  @import '../Order/components/table.less';
</style>
<template>
  <div>
    <Row>
      <Card>
        <p slot="title">
          <Icon type="person"></Icon>
          我的文件清单(含日志)
          <Button type="ghost" shape="circle" style="margin-left: 80%" @click="_Refresh_log">刷新</Button>
        </p>

        <Row>
          <Col span="24">
          <Table border :columns="columns6" :data="applytable" stripe size="small"></Table>
          </Col>
        </Row>
        <br>
        <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="20"></Page>
      </Card>
    </Row>


    <Modal v-model="show_increamt_flag" :width="1100"  :mask-closable="false" @on-ok="" @on-cancel="show_confirm">
      <!--<Modal v-model="show_increamt_flag" width="78%">-->
       <div class="row">
        <div class="col-lg-10 test-cl">
          <Input type="textarea" ref="textAreaTest" disabled v-model="data_websocket_server" :rows="36" style="width: 100%;height:750px;font-size:20px;"></Input>
        </div>
      </div>
    </Modal>
     <Modal v-model="show_full_flag" :width="1100"  :mask-closable="false" @on-ok="" @on-cancel="show_confirm_full">
       <div class="row">
        <div class="col-lg-10" >
              <Input type="textarea" disabled v-model="data_websocket_server_full" :rows="36" style="width: 100%;height:750px;font-size:20px;color: red;background-color:#0c0c0c;overflow:scroll;"></Input>
        </div>
      </div>
    </Modal>


     <Modal
        v-model="confirm_close_log_show"
        title="关闭实时日志显示"
        @on-ok="close_socket"
        @on-cancel="rebase_model">
        <p>您确认要关闭此实时日志？ </p>
    </Modal>


  </div>
</template>
<script>
  import Cookies from 'js-cookie'
  import axios from 'axios'
  import util from '../../libs/util'

  export default {
    name: 'logger-view',
    data () {
      return {
        textAreaObj: null,
        columns6: [
          {
            title: '日志说明',
            key: 'file_title',
            width: 150
          },
          {
            title: '日志路径',
            key: 'file_path',
            width: 200
          },
          {
            title: '类型',
            key: 'file_type',
            width: 80
          },
          {
            title: '关键字',
            key: 'keyword',
            width: 120
          },
          {
            title: '访问用户',
            key: 'visit_user',
            width: 120
          },
          {
            title: '公网IP',
            key: 'public_server_ip',
            width: 120
          },
          {
            title: '内网IP',
            key: 'private_server_ip',
            width: 120
          },
          {
            title: '主机名',
            key: 'server_hostname',
            width: 120
          },
          {
            title: '查看小组',
            key: 'file_owner',
            width: 100
          },
          {
            title: '查看日志',
            key: 'action',
            align: 'left',
            fixed: 'right',
            width: 220,
            render: (h, params) => {
              if (params.row.full_file_status === 'true') {
                return h('div', [
                  h('Button', {
                    style: {
                      marginLeft: '5px'
                    },
                    props: {
                      size: 'small',
                      type: 'primary'
                    },
                    on: {
                      click: () => {
                        this.show_tailf(0)
                      }
                    }
                  }, '增量内容'),
                  h('Button', {
                    style: {
                      marginLeft: '10px'
                    },
                    props: {
                      type: 'default',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.show_tailf(1)
                      }
                    }
                  }, '全量内容'),
                  h('Button', {
                    style: {
                      marginLeft: '10px'
                    },
                    props: {
                      type: 'default',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.download_file(params.index)
                      }
                    }
                  }, '下载')
                ])
              } else {
                return h('div', [
                  h('Button', {
                    props: {
                      size: 'small',
                      type: 'primary'
                    },
                    on: {
                      click: () => {
                        this.show_increment(params.index)
                      }
                    }
                  }, '增量内容'),
                  h('Button', {
                    style: {
                      marginLeft: '10px'
                    },
                    props: {
                      type: 'default',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.download_file(params.index)
                      }
                    }
                  }, '下载')
                ])
              }
            }
          },
          {
            title: '配置',
            key: 'key_word',
            align: 'left',
            width: 240,
            fixed: 'right',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  style: {
                    marginLeft: '2px'
                  },
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.edit_keyword(params.index)
                    }
                  }
                }, '关键字'),
                h('Button', {
                  style: {
                    marginLeft: '10px'
                  },
                  props: {
                    type: 'default',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.edit_keyword(params.index)
                    }
                  }
                }, '内网访问'),
                h('Button', {
                  style: {
                    marginLeft: '10px'
                  },
                  props: {
                    type: 'default',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.edit_keyword(params.index)
                    }
                  }
                }, '访问用户')
              ])
            }
          },
          {
            title: '统计分析',
            key: 'key_word',
            align: 'left',
            width: 150,
            fixed: 'right',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  style: {
                    marginLeft: '2px'
                  },
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.edit_keyword(params.index)
                    }
                  }
                }, '统计'),
                h('Button', {
                  style: {
                    marginLeft: '10px'
                  },
                  props: {
                    type: 'default',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.edit_keyword(params.index)
                    }
                  }
                }, '分析')
              ])
            }
          }
        ],
        sql: [],
        full_file_status: 0,
        pagenumber: 1,
        data_websocket_server: '',
        confirm_close_log_show: false,
        websock: null,
        computer_room: util.computer_room,
        applytable: [],
        openswitch: false,
        show_increamt_flag: false,
        show_full_file_flag: false,
        modaltext: {},
        websocket_server: '127.0.0.1',
        editsql: '',
        myip: '',
        mypath: '',
        mykeyword: '',
        mycnum: ''
      }
    },
    watch: {
      data_websocket_server () {
        console.log(this.textAreaObj);
        this.textAreaObj.scrollTop = this.textAreaObj.scrollHeight + 20;
      }
    },
    methods: {
      show_confirm () {
        this.confirm_close_log_show = true
      },
      rebase_model () {
        this.show_increamt_flag = true
      },
      close_socket () {
        this.threadPoxi('quit')
        // this.show_increamt_flag = false
      },
      closeAreaText () {
        this.show_increamt_flag = false
      },
      show_tailf (type) {
        // alert(type)
        this.show_increamt_flag = true
        const myip = '43.241.232.104'
        // const mypath = '/var/log/nginx/access.log.1'
        const mypath = '/mnt/java/laimi-wms/logs/app.log'
        const mykeyword = ''
        const mycnum = '10'
        // const type = 0
        // this.websocket()
        this.initWebSocket()
        const agentData = 'myip:' + myip + ';mypath:' + mypath + ';mykeyword:' + mykeyword + ';mycnum:' + mycnum + ';type:' + type
        this.threadPoxi(agentData)  // 0-- 增量文件  1--全量文件
      },
      threadPoxi (agentData) {  // 实际调用的方法
        // 参数
        // 若是ws开启状态
          if (this.websock.readyState === this.websock.OPEN) {
            // alert('OPEN')
            this.websocketsend(agentData)
          } else if (this.websock.readyState === this.websock.CONNECTING) {  // 若是 正在开启状态，则等待300毫秒
            // alert('READING')
            let that = this; // 保存当前对象this
            setTimeout(function () {
              that.websocketsend(agentData)
            }, 300);
          } else { // 若未开启 ，则等待500毫秒
            // alert('NOT OPEN')
            this.initWebSocket();
            let that = this; // 保存当前对象this
            setTimeout(function () {
              that.websocketsend(agentData)
            }, 500);
          }
      },
      initWebSocket () { // 初始化weosocket
        // ws地址
        // const wsuri = process.env.WS_API + "/websocket/threadsocket";
        const wsuri = 'ws://127.0.0.1:3310/';
        this.websock = new WebSocket(wsuri);
        // var _this = this;
        // this.websock.onmessage = function (event) {
        //        // _this.test();
        //       alert(this.websocketonmessage)
        //    }
        this.websock.onmessage = this.websocketonmessage;
        // this.data_websocket_server = this.websocketonmessage;
        // alert(this.websocketonmessage)
        console.log(this.websock, 'jj')
        this.websock.onclose = this.websocketclose;
      },
      websocketonmessage (e) { // 数据接收
        // alert('receive')
        console.log(e, 'msg');
        // const redata = JSON.parse(e.data);
        const redata = e.data;
        this.data_websocket_server = this.data_websocket_server + redata

        // console.log(redata.value, '...receive');
        console.log(redata, '........receive');
      },
      websocketsend (agentData) { // 数据发送
        this.websock.send(agentData);
      },
      websocketclose (e) {  // 关闭
        console.log('connection closed (' + e.code + ')');
      },
      edit_keyword () {
        this.ClearForm
      },
      currentpage (vl) {
        axios.get(`${util.url}/workorder/?user=${Cookies.get('user')}&page=${vl}`)
          .then(res => {
            this.applytable = res.data.data
            this.pagenumber = parseInt(res.data.page.alter_number)
          })
          .catch(error => {
            util.ajanxerrorcode(this, error)
          })
      },
      websocket () {
          let ws = new WebSocket('ws://localhost:3310/')
          ws.onopen = () => {
            // Web Socket 已连接上，使用 send() 方法发送数据
              ws.send('Oops')
              console.log('数据发送中...')
          }
          ws.onmessage = evt => {
            console.log('数据已接收...')
          }
          ws.onclose = function () {
            // 关闭 websocket
            console.log('连接已关闭...')
          }
          // 路由跳转时结束websocket链接
          this.$router.afterEach(function () {
            ws.close()
          })
      }
    },
    mounted () {
      this.textAreaObj = this.$refs.textAreaTest.$el.getElementsByTagName('textarea')[0];
      axios.get(`${util.url}/filemanager?user=${Cookies.get('user')}&page=1`)
        .then(res => {
          this.applytable = res.data.data
          // this.full_file_status = res.
          console.log(res.data, 'hello')
          // this.pagenumber = res.data.page.alter_number
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    }
  }
</script>

<style>
  .test-cl textarea {
    background-color: green !important;
    color: yellow !important;
  }
</style>


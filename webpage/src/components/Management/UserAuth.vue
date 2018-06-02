<style lang="less">
@import '../../styles/common.less';
@import '../Order/components/table.less';
</style>
<template>
<div>
  <!--<Col span="9">-->
  <!--<Card>-->
    <!---->
    <!---->
    <!--<p slot="title">-->
      <!--<Icon type="load-b"></Icon>-->
      <!--新增模块-->
    <!--</p>-->
    <!--<div class="edittable-testauto-con">-->
      <!--<Form :model="usermodule" :label-width="80" ref="usermoduleva" :rules="userinfoValidate">-->
        <!--<FormItem label="编号" prop="modulenum">-->
          <!--<Input v-model="usermodule.code" placeholder="请输入"></Input>-->
        <!--</FormItem>-->
        <!--<FormItem label="名称" prop="modulename">-->
          <!--<Input v-model="usermodule.name" placeholder="请输入" type="password"></Input>-->
        <!--</FormItem>-->
        <!--<FormItem label="类型" prop="moduletype">-->
          <!--<Input v-model="usermodule.type" placeholder="请输入" type="password"></Input>-->
        <!--</FormItem>-->
        <!--<FormItem label="备注" prop="moduleremark">-->
          <!--<Input v-model="usermodule.remark" placeholder="请输入" type="password"></Input>-->
        <!--</FormItem>-->
        <!--<FormItem label="启用状态" prop="modulestatus">-->
          <!--<Input v-model="usermodule.status" placeholder="请输入"></Input>-->
        <!--</FormItem>-->
        <!--&lt;!&ndash;<FormItem label="电子邮箱:" prop="email">&ndash;&gt;-->
          <!--&lt;!&ndash;<Input v-model="usermodule.email" placeholder="请输入"></Input>&ndash;&gt;-->
        <!--&lt;!&ndash;</FormItem>&ndash;&gt;-->
        <!--&lt;!&ndash;<FormItem label="平台模块:" prop="module">&ndash;&gt;-->
        <!--&lt;!&ndash;<Transfer&ndash;&gt;-->
          <!--&lt;!&ndash;:data="module_list"&ndash;&gt;-->
          <!--&lt;!&ndash;:target-keys="targetKeys"&ndash;&gt;-->
          <!--&lt;!&ndash;:render-format="myrender"&ndash;&gt;-->
          <!--&lt;!&ndash;@on-change="handleChange">&ndash;&gt;-->
          <!--&lt;!&ndash;&lt;!&ndash;:filter-method="filterMethod"&ndash;&gt;&ndash;&gt;-->
        <!--&lt;!&ndash;</Transfer>&ndash;&gt;-->
          <!--&lt;!&ndash;</FormItem>&ndash;&gt;-->
        <!--<br><br>-->
        <!--<Button type="primary" @click.native="Registered" style="margin-left: 35%">注册</Button>-->
      <!--</Form>-->
    <!--</div>-->
  <!--</Card>-->
  <!--</Col>-->
  <Col span="24" class="padding-left-10">
  <Card>
    <p style="height: 29px;"  slot="title">
      <Icon size="20" type="ios-crop-strong"></Icon>
      模块清单
          <Button  type="primary" shape="circle" style="margin-left: 80%" @click="showAddModule">新增模块</Button>

    </p>
    <div class="edittable-con-1">
      <Table border :columns="columns_module" :data="data_module" stripe height="550"></Table>
    </div>
    <br>
    <Page :total="pagenumber" show-elevator @on-change="splicpage" :page-size="10"></Page>
    <br><br>
    <Button type="primary" @click.native="Registered" style="margin-left: 35%">注册</Button>

  </Card>
  </Col>


  <Modal v-model="addModule" :closable='false' :mask-closable=false :width="500">
    <h3 slot="header" style="color:#2D8CF0">添加新的平台模块</h3>
    <Form :label-width="100" label-position="right">
      <FormItem label="E-mail">
        <Input v-model="email"></Input>
      </FormItem>
    </Form>
    <div slot="footer">
      <Button type="text" @click="addModule=false">取消</Button>
      <Button type="warning" @click="putemail">更改</Button>
    </div>
  </Modal>
</div>
</template>
<script>
import axios from 'axios'
import '../../assets/tablesmargintop.css'
import util from '../../libs/util'
export default {
  name: 'user-auth',
  data () {
    const valideRePassword = (rule, value, callback) => { // eslint-disable-line no-unused-vars
      if (value !== this.editPasswordForm.newPass) {
        callback(new Error('两次输入密码不一致'));
      } else {
        callback();
      }
    };
    const valideuserinfoPassword = (rule, value, callback) => {
      if (value !== this.userinfo.password) {
        callback(new Error('两次输入密码不一致'));
      } else {
        callback();
      }
    };
    return {
      module_list: [],
      targetKeys: [],
      usermodule: {
        code: '',
        name: '',
        type: '',
        remark: '',
        status: ''
      },
      columns_module: [
        {
          title: '模块名称',
          key: 'name',
          width: 180
        },
        {
          title: '第一审核人',
          key: 'first_approve_man',
          width: 120,
          render: (h, params) => {
             return h('Dropdown', {
                      props: {
                        style: 'margin-left: 20px',
                        placement: 'bottom-end'
                      },
                    }, [
                        h('a', {
                            on: {
                          click: () => {
                             javascript:void(0)
                          }
                      }, },
                            [h('Icon',{
                              props: {
                                style: 'arrow-down-b'
                             }
                            })],
                             '更多'),
                        h('DropdownMenu',{
                            props:{
                               slot:'list'
                            }
                        },[
                            h('DropdownItem','1'),
                            h('DropdownItem','2')
                          ]
                         )
                    ])
          }
        },
        {
          title: '备用审核人',
          key: 'second_approve_man',
          width: 120,
        },
        {
          title: '第一执行人',
          key: 'first_execute_man',
          width: 120,
        },
        {
          title: '备用执行人',
          key: 'second_execute_man',
          width: 120,
        }
      ],
      data_module: [],

      pagenumber: 1,
      addModule: false,
      // 新建用户
      email: '',
      // 用户名
      username: '',
      confirmuser: '',
      deluserModal: false
    }
  },
  methods: {
    showAddModule () {
      this.addModule = true
    },
    myrender (item) {
                return item.name;
            },
    handleChange (newTargetKeys, direction, moveKeys) {
                console.log(newTargetKeys);
                console.log(direction);
                console.log(moveKeys);
                this.targetKeys = newTargetKeys;
            },

    edituser (index) {
      this.editPasswordModal = true
      this.username = this.data5[index].username
    },
    editgroup (index) {
      this.editInfodModal = true
      this.username = this.data5[index].username
      this.editInfodForm.department = this.data5[index].department
      this.editInfodForm.group = this.data5[index].group
    },
    deleteUser (index) {
      this.deluserModal = true
      this.username = this.data5[index].username
    },
    editEmail (index) {
      this.editemail = true
      this.username = this.data5[index].username
      this.email = this.data5[index].email
    },
    putemail () {
      axios.put(`${util.url}/userinfo/changemail`, {
        'username': this.username,
        'mail': this.email
      })
        .then(res => {
          this.$Notice.success({
            title: res.data
          })
          this.editemail = false
          this.refreshuser()
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    Registered () {
      this.$refs['userinfova'].validate((valid) => {
        if (valid) {
          axios.post(util.url + '/userinfo/', {
              'username': this.userinfo.username,
              'password': this.userinfo.password,
              'group': this.userinfo.group,
              'department': this.userinfo.department,
              'email': this.userinfo.email,
              'module_list': this.targetKeys,
            })
            .then(res => {
              this.$Notice.success({
                title: res.data
              })
              this.refreshuser()
              this.userinfo = {}
            })
            .catch(() => {
              this.$Notice.error({
                title: '警告',
                desc: '用户名已注册过,请更换其他用户名注册！'
              })
            })
        }
      })
    },
    refreshModule (type = 1, flow = 1) {
      // axios.get(`${util.url}/config?type=${type}&flow=${flow}&page=${vl}`)
      axios.get(`${util.url}/config?type=${type}&flow=${flow}`)
        .then(res => {
          // res.data.forEach(item => {
          //   item.key = item.id + ''
          // })
          this.data_module = res.data
        })
        .catch(error => {
          util.ajanxerrorcode(this, error)
        })
    },
    splicpage (page) {
      this.refreshuser(page)
    }
  },
  mounted () {
    this.refreshModule()

  }
}
</script>
<!-- reder put request  render_group put request  remove delete request-->

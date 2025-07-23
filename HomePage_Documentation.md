# HomePage.vue 代码文档

## 文件概述
**文件路径**: `c:\Users\89172\Desktop\ecnu_smarteredu\src\views\HomePage.vue`

该文件是上海市高等学校计算机基础教学资源平台的首页组件，使用Vue 3的`<script setup>`语法编写，包含页面布局、用户登录/注册功能、资源搜索和导航菜单等核心功能。

## 导入依赖

### 第三方库
```javascript
import { Search } from "@element-plus/icons-vue"          // Element Plus搜索图标组件
import { defineAsyncComponent, reactive, ref, watch } from "vue"  // Vue3组合式API
import axios from "@/https"                                 // 自定义封装的axios实例
import { toRaw } from "@vue/reactivity"                   // Vue响应式转换工具
import { useRoute, useRouter } from "vue-router"           // Vue Router组合式API
```

### 自定义组件和数据
```javascript
import { navigationMenu } from "../components/HomeTitleData.vue"  // 导航菜单数据配置
import { someLinks } from "../components/Links.vue"                 // 链接数据配置
import { schoolOptions } from "@/components/schoolOptions.vue"    // 学校选项数据
import TopMenu from "@/components/menus/topMenu.vue"               // 顶部菜单组件

// 异步组件加载
const GetSecondaryMenu = defineAsyncComponent(() => import("@/components/menus/GetSecondaryMenu.vue"))
const getList = defineAsyncComponent(() => import("@/components/getInfo/getList.vue"))
```

## 响应式数据变量

### 基础状态变量
| 变量名 | 类型 | 初始值 | 描述 |
|--------|------|--------|------|
| `search_query` | `ref` | `""` | 搜索框输入内容绑定 |
| `isAuth` | `ref` | `localStorage.getItem("isAuth")` | 用户认证状态 |
| `loginState` | `let` | `isAuth.value === "true"` | 登录状态布尔值 |
| `adminFormCheck` | `ref` | `""` | 管理员登录表单ref引用 |
| `userFormCheck` | `ref` | `""` | 用户登录表单ref引用 |

### 页面控制变量
| 变量名 | 类型 | 初始值 | 描述 |
|--------|------|--------|------|
| `zindex0` | `ref` | `1` | 控制页面层级显示 |
| `seen` | `ref` | `false` | 控制内容区域显示状态 |
| `isComputer` | `ref` | `true` | 设备类型判断(电脑/手机) |
| `geturl` | `ref` | `""` | 当前请求的API地址 |
| `navigation_title` | `ref` | `"新闻公告"` | 当前页面标题 |
| `formLabelWidth` | `const` | `"150px"` | 表单标签宽度 |

### 表单数据
| 变量名 | 类型 | 描述 |
|--------|------|------|
| `adminForm` | `reactive` | 管理员登录表单数据{email, password} |
| `form` | `reactive` | 用户登录/注册表单数据，包含完整用户信息 |

### 对话框控制变量
| 变量名 | 类型 | 描述 |
|--------|------|------|
| `dialogFormVisibleUser` | `ref` | 用户登录对话框显示控制 |
| `dialogFormVisibleAdmin` | `ref` | 管理员登录对话框显示控制 |
| `dialogFormVisibleUserRegister` | `ref` | 用户注册对话框显示控制 |

## 表单验证规则

### Rules对象
包含所有表单项的验证规则，使用Element Plus的表单验证语法：

| 字段名 | 验证规则 |
|--------|----------|
| `password` | 必填，提示"请输入密码！" |
| `email` | 必填，提示"请输入用户名！" |
| `passwordConfirm` | 必填，提示"请再次输入密码！" |
| `captcha` | 必填，提示"请输入验证码！" |
| `gender` | 必填，提示"请选择性别！" |
| `grade` | 必填，提示"请选择年级！" |
| `school_name` | 必填，提示"请选择学校！" |
| `name` | 必填，提示"请输入姓名！" |

## 年级选项生成

### grade_options数组
动态生成年级选项，包含：
- 研究生/00级
- 本科生/xx级（根据当前年份动态生成4个年级）
- 教师/00级

生成逻辑：
```javascript
let myDate = new Date()
let tYear = myDate.getFullYear()
let tMonth = myDate.getMonth() + 1
// 根据当前月份决定起始年级
```

## 核心函数说明

### 1. 登录相关函数

#### `PostAdmin()`
- **作用**: 管理员登录验证
- **流程**: 
  1. 验证表单
  2. 发送POST请求到`/api/admin/login`
  3. 处理响应：成功则跳转管理员页面，失败显示错误信息

#### `PostUser()`
- **作用**: 用户登录验证
- **流程**:
  1. 验证表单
  2. 发送POST请求到`/api/login`
  3. 存储用户信息到localStorage
  4. 更新登录状态

#### `login_submit()`
- **作用**: 新版本的登录函数
- **流程**:
  1. 表单验证
  2. 发送POST请求到`/auth/login`
  3. 获取token并存储
  4. 调用`init_profile()`获取用户详细信息

### 2. 注册相关函数

#### `signup_submit()`
- **作用**: 用户注册
- **流程**:
  1. 表单验证
  2. 发送POST请求到`/auth/register`
  3. 处理注册结果

#### `RegisterUser()`
- **作用**: 旧版本用户注册（使用`/api/register`接口）
- **注意**: 此函数可能已被`signup_submit()`替代

### 3. 验证码相关函数

#### `verify_captcha(f)`
- **作用**: 发送注册验证码
- **参数**: `f` - 包含邮箱地址的表单对象
- **流程**: GET请求到`/auth/register/captcha`

#### `verify_captcha_fp(f)`
- **作用**: 发送忘记密码验证码
- **参数**: `f` - 包含邮箱地址的表单对象
- **流程**: GET请求到`/auth/password/captcha`

### 4. 验证工具函数

#### `jud_email(f)`
- **作用**: 邮箱格式验证
- **返回值**: 布尔值，true表示格式不正确

#### `jud_pwd(f)`
- **作用**: 密码强度验证
- **规则**: 必须包含大小写字母和数字，长度8-20位
- **返回值**: 布尔值，true表示格式不正确

#### `check_email(f)` / `check_password(f)` / `check_again(f)`
- **作用**: 实时表单验证反馈
- **功能**: 更新对应的错误提示信息

### 5. 用户管理函数

#### `UserLogOut()`
- **作用**: 用户退出登录
- **流程**:
  1. 清除localStorage中的认证信息
  2. 重置登录状态
  3. 跳转回首页
  4. 页面刷新

#### `init_profile()`
- **作用**: 获取用户详细信息
- **流程**: 使用token请求`/users/profile`接口，存储用户信息到localStorage

### 6. 页面交互函数

#### `changeZindex(val)`
- **作用**: 控制页面层级
- **参数**: `val` - 布尔值，决定层级值

#### `changeurl(val)`
- **作用**: 更新请求URL
- **参数**: `val` - 菜单ID值

#### `resource_retrieval_user()`
- **作用**: 跳转到资源检索页面
- **流程**: 使用router跳转到`resource_retrieval`路由，携带搜索参数

## 监听与响应

### watch监听
监听`geturl`变化：
- 根据URL长度判断显示模式
- 更新页面标题
- 检查用户权限（需要登录才能访问某些内容）
- 动态调整标题显示宽度

## 模板结构

### 页面布局
使用Element Plus的`el-container`布局：
- `el-header`: 顶部标题栏，包含搜索框
- `el-dialog`: 多个对话框组件用于登录/注册
- 动态组件渲染区域

### 关键组件
1. **搜索区域**: 包含输入框和搜索按钮
2. **登录对话框**: 分为管理员登录和用户登录两种
3. **注册对话框**: 完整的用户注册表单
4. **验证码功能**: 集成邮箱验证码发送

## 数据存储

### localStorage键值
| 键名 | 描述 |
|------|------|
| `isAuth` | 用户认证状态 |
| `token` | JWT认证令牌 |
| `permission` | 用户权限等级 |
| `email` | 用户邮箱 |
| `user_id` | 用户ID |
| `userId` | 用户ID（备用） |
| `username` | 用户名 |

## 接口调用

### 认证相关接口
- `POST /api/admin/login` - 管理员登录
- `POST /api/login` - 用户登录（旧版）
- `POST /auth/login` - 用户登录（新版）
- `POST /auth/register` - 用户注册
- `GET /auth/register/captcha` - 获取注册验证码
- `GET /auth/password/captcha` - 获取忘记密码验证码
- `GET /users/profile` - 获取用户详细信息

### 内容相关接口
- `GET /api/menu/info/{id}/{title}` - 获取菜单内容
- 动态URL格式，支持不同内容类型
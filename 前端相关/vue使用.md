### 1. 使用vue-router

> 引入路由

```javascript
import Vue from 'vue'
import VueRouter from 'vue-router'
import Zhang from '../demo/Zhang.vue'
import Chu from '../demo/Chu.vue'

//配置路由
const routes = [
  { path: '/index/link1', component: Zhang },
  { path: '/index/link2', component: Chu }
]

//注册router组件
Vue.use(VueRouter)

//创建路由实例并挂载路由
export default new VueRouter({
	//地址栏显示当前页面的path
	mode: 'history',
	//每次路由变化视图重新滚到顶部
	scrollBehavior: () => ({ y: 0 }),
	routes
})
```

> 挂载

```javascript
import Vue from 'vue'
import App from './App.vue'
import router from './router/routerConfig.js'

//将路由实例注册到 根vue 实例上
Vue.use(router)

new Vue({
  //挂载
  router,
  render: h => h(App),
}).$mount('#app')
```

### 2.使用vuex

> 引入vuex

```javascript
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state:{
		count: 0
	},
	mutations:{
		add(state){
			state.count++
		}
	}
})
```

> 挂载

```javascript
import Vue from 'vue'
import App from './App.vue'
import store from './store/storeConfig.js'

Vue.use(store)

new Vue({
  //挂载
  store,
  render: h => h(App),
}).$mount('#app')
```

> 相应式的显示vuex中state中的实例值 -> 使用computed方法

```javascript
computed: {
    count () {
        return store.state.count
    }
}
```

> 当一个组件需要获取多个状态的时候，将这些状态都声明为计算属性会有些重复和冗余。为了解决这个问题，我们可以使用 `mapState` 辅助函数帮助我们生成计算属性，让你少按几次键：

```javascript
import { mapState } from 'vuex'

export default {
  // ...
  computed: mapState({
    // 箭头函数可使代码更简练
    count: state => state.count,

    // 传字符串参数 'count' 等同于 `state => state.count`
    countAlias: 'count',

    // 为了能够使用 `this` 获取局部状态，必须使用常规函数
    countPlusLocalState (state) {
      return state.count + this.localCount
    }
  })
}
```

> 简化一：当映射的计算属性的名称与 state 的子节点名称相同时，我们也可以给 `mapState` 传一个字符串数组。

```javascript
computed: mapState([
  // 映射 this.count 为 store.state.count
  'count'
])
```

> 简化二： 对象展开运算符

```javascript
computed: {
  localComputed () { /* ... */ },
  // 使用对象展开运算符将此对象混入到外部对象中
  ...mapState({
    // ...
  })
}
```

#### 2.1 Getter

```javascript
const store = new Vuex.Store({
  state: {
    users: [
      { id: 1, text: '...', boy: true },
      { id: 2, text: '...', boy: false }
    ]
  },
  getters: {
    doSomething: state => {
      return state.users.filter(user => user.done)
    },
    doSomethingToo: (state) => (id) =>{
      return state.users.filter(user => user.id === id)
    }
  }
})
```

```javascript
//外部调用
let fUsers = this.$store.doSomething
let oneUsers = this.$store.doSomethingToo(12)
```

> `mapGetters` 辅助函数仅仅是将 store 中的 getter 映射到局部计算属性：

```javascript
import { mapGetters } from 'vuex'

export default {
  // ...
  computed: {
  // 使用对象展开运算符将 getter 混入 computed 对象中
    ...mapGetters([
      'doSomething',
      'doSomethingToo',
      // ...
    ])
  }
}

```

#### 2.2 Mutation

```javascript
const store = new Vuex.Store({
  state: {
    count: 1
  },
  mutations: {
    increment (state) {
      // 变更状态
      state.count++
    }
  }
})
store.commit('increment')
```

> 你可以向 `store.commit` 传入额外的参数，即 mutation 的 **载荷（payload）**：

```javascript
mutations: {
  increment (state, n) {
    state.count += n
  }
}
store.commit('increment', 10)
```

##### 2.2.1 警告

> ##### Mutation 需遵守 Vue 的响应规则
>
> Vuex 的 store 中的状态是响应式的，那么当我们变更状态时，监视状态的 Vue 组件也会自动更新。这也意味着 Vuex 中的 mutation 也需要与使用 Vue 一样遵守一些注意事项：
>
> 1. 最好提前在你的 store 中初始化好所有所需属性。
> 2. 当需要在对象上添加新属性时，你应该
>
> - 使用 `Vue.set(obj, 'newProp', 123)`, 或者
> - 以新对象替换老对象。例如，利用[对象展开运算符](https://github.com/tc39/proposal-object-rest-spread)
>
> [ ](https://github.com/tc39/proposal-object-rest-spread)我们可以这样写：
>
> ```
> state.obj = { ...state.obj, newProp: 123 }
> ```
>
> ##### Mutation 必须是同步函数
>
> 在 mutation 中混合异步调用会导致你的程序很难调试。例如，当你调用了两个包含异步回调的 mutation 来改变状态，你怎么知道什么时候回调和哪个先回调呢？这就是为什么我们要区分这两个概念。在 Vuex 中，**mutation 都是同步事务**

#### 2.3 Action

> Action 类似于 mutation，不同在于：
>
> - Action 提交的是 mutation，而不是直接变更状态。
> - Action 可以包含任意异步操作。

```javascript
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment (state) {
      state.count++
    }
  },
  actions: {
    increment (context) {
      context.commit('increment')
    }
  }
})
store.dispatch('increment')
```

> 异步栗子

```javascript
actions: {
  checkout ({ commit, state }, products) {
    // 把当前购物车的物品备份起来
    const savedCartItems = [...state.cart.added]
    // 发出结账请求，然后乐观地清空购物车
    commit(types.CHECKOUT_REQUEST)
    // 购物 API 接受一个成功回调和一个失败回调
    shop.buyProducts(
      products,
      // 成功操作
      () => commit(types.CHECKOUT_SUCCESS),
      // 失败操作
      () => commit(types.CHECKOUT_FAILURE, savedCartItems)
    )
  }
}
```

> 辅助函数

```javascript
import { mapActions } from 'vuex'

export default {
  // ...
  methods: {
    ...mapActions([
      'increment', // 将 `this.increment()` 映射为 `this.$store.dispatch('increment')`

      // `mapActions` 也支持载荷：
      'incrementBy' // 将 `this.incrementBy(amount)` 映射为 `this.$store.dispatch('incrementBy', amount)`
    ]),
    ...mapActions({
      add: 'increment' // 将 `this.add()` 映射为 `this.$store.dispatch('increment')`
    })
  }
}

```


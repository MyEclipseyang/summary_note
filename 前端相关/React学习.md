### React学习

#### 1.父传子

> 父组件通过key = {value}将值传递给子组件

> 父

```react
//多个方块组成一个棋盘
class Board extends React.Component {
  renderSquare(i) {
      //给子组件传key为number, value为i的属性
    return <Square number={i} />;
  }

  render() {
    const status = 'Next player: X';

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}
```

> 子

```react
//一个方块
class Square extends React.Component {
    
  render() {
    return (
      <button className="square" onClick={()=>{alert('click Square:'+this.props.number)}}>
            {/*
              *获取父类传的属性值
              */}
        { this.props.number }
      </button>
    );
  }
}
```

#### 2.子传父

> 子组件通过调用父组件传递给子组件的方法，向父组件传递或更新数据

> 父

```react
renderSquare(i) {
    return (
		<Square
			number={this.state.squares[i]}
			onClick={ ()=> this.handlerClick(i) }
		/>
	)
  }
  
  handlerClick(i){
	  const squares = this.state.squares.slice();
	  squares[i] = 'X';
	  this.setState({ squares: squares });
  }
```

> 子

```react
class Square extends React.Component {
	constructor(props) {
	    super(props);
		this.state = {
			number: null
		};
	}

  render() {
    return (
      <button 
		className="square" 
		onClick={()=>{ this.props.onClick() }}
	   >
        { this.props.number }
      </button>
    );
  }
}
```


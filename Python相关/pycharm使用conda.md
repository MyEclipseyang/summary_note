### pycharm使用conda

#### 1.如果新建项目包net_error

> 进入”**C:\Users\Administrator**“，打开“**.condarc“**，你将会看到以下代码：
>
> ```
> 
> channels:
>   - httpn://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
> ```
>
> 需要改为（根据系统而定）
>
> ```
> channels:
>   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/win-64
> ```

#### 2.CondaError:

> 如果提示Downloaded bytes did not match Content-Length
>
> conda config --set remote_read_timeout_secs 1000.0
# ExpOven

<center><img src="https://github.com/user-attachments/assets/c478b73c-4f7b-4b7d-bd26-28522892fb98"></center>

ExpOven is a notifier application mainly designed for AI researchers. It provides a simple and efficient way to monitor the status of experiments opportunely.

You execute your experiments or commands on the server. When the command is completed or encounters an issue, you will receive a notification in your messaging apps (such as DingTalk, email, Slack, etc.). Additionally, you can use this tool to track the progress of the experiments.

## Installation

### Step 0. Third Party Setup

- [DingTalk](./docs/third_party_setup/dingtalk.md)
- [Feishu(Lark)](./docs/third_party_setup/feishu.md)

### Step 1. Install Package

You can clone the repo and install the package with:

```shell
git clone https://github.com/IsshikiHugh/ExpOven.git
cd ExpOven
pip install .  # Make sure you are in the (virtual) environment that you want to install ExpOven.
```

Or simply install with:

```shell
pip install git+https://github.com/IsshikiHugh/ExpOven
```

### Step 2. Edit Configuration

After finishing installation, you need to edit the configuration file. The default configuration file is located at `~/.config/oven/cfg.yaml`. You can also specify the configuration file by setting the environment variable `OVEN_HOME`. If the environment variable is set, the configuration file will be located at `$OVEN_HOME/cfg.yaml`.

The template of the config file is given at [docs/cfg.yaml.temp](./docs/cfg.yaml.temp).

The things to be filled can be found in **[Step 0](#step-0-third-party-setup)**.

## Quick Start

Check [docs/examples.py](./docs/examples.py) for runnable examples.

### As CLI

```shell
ding [LOGGING MESSAGE]
# eg:
ding 'Hello World!'
mv from to ; ding 'Data moved.'  # Similar to `bake mv from to`.
```

Tips: When you have already started the experiment, you can still print type `ding 'Exp xxx stopped.'` and press Enter. Although it seems you don't send the command correctly, it's actually put into the queue. When the experiment is over, the command will still be executed.

<center><img src="docs/eg_ding_dingtalk.png" width="50%"></center>

```shell
bake [RUNNABLE COMMAND]
# eg:
bake echo 'Hello World!'
bake pip install -r requirements.txt
bake bash scripts/download_data.sh
bake CUDA_VISIBLE_DEVICES='0,1' python train.py
```

<center><img src="docs/eg_bake_dingtalk.png" width="50%"></center>

### As Package

As a single function, it notifies the message. The two forms are equivalent.

```py
oven.notify('Hello World!')
oven.ding('Hello World!')

# eg:

def compute_loss(gt, pd):
    loss = (gt - pd).abs().mean()  # (,)
    if torch.isnan(loss).any():
        oven.notify('Loss contains NaN.')  # 👈
        ipdb.set_trace()
    return loss

def main():
    model = Model()
    train(model)
    metric = evaluate(model)
    oven.notify(f'Train over with metric: {metric}')  # 👈
```

As function wrapper, the notifier will be called both before and after the function is executed. The two forms are equivalent.

```py
@oven.monitor
def foo() -> None:
    print('Hello World!')

@oven.bake
def bar() -> None:
    print('Hello World!')

# eg:

@oven.monitor  # 👈
def train() -> None:
    for epoch in range(10):
        train_before_epoch()
        train_epoch()
        train_after_epoch()
```


## Contribution

Thank you for contributing!

**Before contributing, you are suggested to check this [issue#14](https://github.com/IsshikiHugh/ExpOven/issues/14) first**. In addition, I leave some design details at [docs/docs.md](./docs/docs.md). The implementation of [DingTalk backend](./oven/backends/dingtalk/__init__.py) should be a good example.

According to [this](https://stackoverflow.com/questions/35278957/can-i-modify-someone-elses-pull-request-and-push-it-back-in-its-branch/49854013#49854013), I *recommend* you to check "Allow edits from maintainers." when you open the pull request.

Any suggestions (as well as new feature requests) and contributions are welcome!
<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import { Title, Content, } from '@smui/dialog';
    import {login} from "../../services/userService";
    import {RESPONSE_STATUS_SUCCESS} from "../../../constants";
    import {showToast} from "../../utils/toast";


    let username: string = $state('test');
    let usernameDirty = $state(false);
    let usernameInvalid = $state(false);
    let password: string = $state('test');
    let passwordDirty = $state(false);
    let passwordInvalid = $state(false);
    let passwordInvalidMessage = $state('');

    const { onSwitch, onLoginSuccess } = $props();

    function handlerUsernameChange() {
        // 验证输入是否符合要求
        if (username) {
            // 正则表达式：只允许下划线、数字和字母
            usernameInvalid = !/^\w+$/.test(username);
        } else {
            usernameInvalid = true;
        }
        console.log('handlerUsernameChange======', username, usernameInvalid)
    }

    function handlerPasswordChange() {
        // 验证输入是否符合要求
        if (!password || !password.trim()) {
            passwordInvalidMessage = '密码不能为空';
            passwordInvalid = true;
        } else if (!/^\S+$/.test(password)) {
            passwordInvalidMessage = '密码不能包含空白字符';
            passwordInvalid = true;
        } else {
            passwordInvalidMessage = '';
            passwordInvalid = false;
        }
        console.log('handlerPasswordChange======', password, passwordInvalidMessage)
    }


    async function handleUserConfirm() {
        try {
            const response = await login({
                username,
                password,
            })

            if (response.status === RESPONSE_STATUS_SUCCESS) {
                showToast(response.message);
                onLoginSuccess(response.data);
            }
        } catch (error) {
            console.log(error);
        }

    }
</script>

<div class="user-register">
    <Title class="simple-title">登录账号</Title>
    <Content id="simple-content">
        <Textfield
                type="text"
                bind:value={username}
                bind:invalid={usernameInvalid}
                bind:dirty={usernameDirty}
                autofocus
                label="账号"
                style="width: 100%;"
                oninput={handlerUsernameChange}
        >
            {#snippet helper()}
                <HelperText validationMsg={usernameInvalid && usernameDirty}>
                    {usernameInvalid && usernameDirty ? '账号只能包含字母、数字和下划线' : ''}
                </HelperText>
            {/snippet}
        </Textfield>
        <Textfield
                type="password"
                bind:value={password}
                bind:invalid={passwordInvalid}
                bind:dirty={passwordDirty}
                label="密码"
                style="width: 100%;"
                oninput={handlerPasswordChange}
        >
            {#snippet helper()}
                <HelperText validationMsg={!!passwordInvalid && passwordDirty}>
                    {passwordInvalid && passwordDirty ? passwordInvalidMessage : ''}
                </HelperText>
            {/snippet}
        </Textfield>
    </Content>
    <div class="buttons">
        <Button class="confirm" variant="raised"  disabled={
            !username || usernameInvalid ||
            !password || passwordInvalid
        } onclick={handleUserConfirm}>
            <Label>确定</Label>
        </Button>
        <Button class="text" onclick={onSwitch}>
            <Label>立即注册</Label>
        </Button>
    </div>
</div>

<style lang="scss">
  .user-register{
    width: 500px;

    :global(.simple-title){
      text-align: center;
    }

    .buttons{
      display:flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 20px 24px 20px 24px;

      :global(.confirm){
        width: 100%;
      }
      :global(.text){
        font-size: 12px;
        margin-top: 10px;
      }
    }
  }

  @media screen and (max-width: 768px) {
      .user-register {
          width: 300px;
      }
  }

  @media screen and (min-width: 768px) and (max-width: 1024px) {
      .user-register {
          width: 400px;
      }
  }



</style>
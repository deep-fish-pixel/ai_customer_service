<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import { Title, Content, } from '@smui/dialog';
    import {login} from "../../services/userService";
    import {RESPONSE_STATUS_SUCCESS} from "../../../constants";
    import {showToast} from "../../utils/toast";


    let username: string = $state('');
    let usernameDirty = $state(false);
    let usernameInvalid = $state(false);
    let password: string = $state('');
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
    <Title class="simple-title">注册账号</Title>
    <Content id="simple-content">
        <Textfield
                type="text"
                bind:value={username}
                bind:invalid={usernameInvalid}
                bind:dirty={usernameDirty}
                label="账号"
                style="min-width: 450px;"
                oninput={handlerUsernameChange}
        >
            {#snippet helper()}
                <HelperText validationMsg={usernameInvalid && usernameDirty}>
                    {usernameInvalid && usernameDirty ? '账号只能包含字母、数字和下划线' : ''}
                </HelperText>
            {/snippet}
        </Textfield>
        <Textfield
                type="text"
                bind:value={password}
                bind:invalid={passwordInvalid}
                bind:dirty={passwordDirty}
                label="密码"
                style="min-width: 450px;"
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
    :global(.simple-title){
      text-align: center;
    }

    .buttons{
      display:flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin-bottom: 10px;

      :global(.confirm){
        width: 70%;
      }
      :global(.text){
        font-size: 12px;
        margin-top: 10px;
      }
    }
  }



</style>
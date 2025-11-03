<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import { navigate, useRouter, useLocation, useHistory } from "svelte5-router";
    import Dialog, { Title, Content, Actions } from '@smui/dialog';


    let username: string | null = $state(null);
    let usernameDirty = $state(false);
    let usernameInvalid = $state(false);
    let password: string | null = $state(null);
    let passwordDirty = $state(false);
    let passwordInvalid = $state(false);
    let passwordInvalidMessage = $state('');
    let nickname: string | null = $state(null);
    let nicknameDirty = $state(false);
    let nicknameInvalid = $state(false);
    const router = useRouter();
    const location = useLocation();
    const history = useHistory();

    let isSpace = $derived(history.location.pathname.match(/^\/space\/\w+$/));
    let visible = $state(!isSpace);

    // $effect(() => {
    //     if (!history.location.pathname.match(/^\/user\/\w+$/)) {
    //         visible = true;
    //     }
    // });

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

    function handlerNicknameChange() {
        if (!nickname || !nickname.trim()) {
            nicknameInvalid = true;
        } else {
            nicknameInvalid = false;
        }
        console.log('handlerNicknameChange======', nickname, nicknameInvalid)
    }

    const confirm = async () => {
        navigate(`/space/${username}`);
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
        <Textfield
                type="text"
                bind:value={nickname}
                bind:invalid={nicknameInvalid}
                bind:dirty={nicknameDirty}
                label="昵称"
                style="min-width: 450px;"
                oninput={handlerNicknameChange}
        >
            {#snippet helper()}
                <HelperText validationMsg={nicknameInvalid && nicknameDirty}>
                    {nicknameInvalid && nicknameDirty ? '昵称不能为空' : ''}
                </HelperText>
            {/snippet}
        </Textfield>
    </Content>
    <div class="buttons">
        <Button class="confirm" variant="raised"  disabled={
            !username || usernameInvalid ||
            !password || passwordInvalid ||
            !nickname || nicknameInvalid
        } onclick={confirm}>
            <Label>确定</Label>
        </Button>
        <Button class="text" onclick={() => clicked++}>
            <Label>返回登录</Label>
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
      }
    }
  }



</style>
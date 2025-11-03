<script lang="ts">
    import Dialog from '@smui/dialog';
    import UserLogin from './UserLogin.svelte';
    import UserRegister from './UserRegister.svelte';
    import type {User} from "../../types/user";
    import {setUser} from "../../utils/getUser";

    const { visible: propVisible, onclose } = $props();
    let visible = $state(false);
    let isLogin = $state(true);

    $effect(() => {
        visible = propVisible
    });

    function handleToRegister(){
        isLogin = false;
    }
    function handleToLogin(){
        isLogin = true;
    }
    async function handleLoginSuccess(user: User){
        setUser(user);
        visible = false;
        onclose();
    }
</script>

<Dialog
        bind:open={visible}
        aria-labelledby="simple-title"
        aria-describedby="simple-content"
        scrimClickAction=""
        escapeKeyAction=""
>
    {#if isLogin}
        <UserLogin onSwitch={handleToRegister} onLoginSuccess={handleLoginSuccess}></UserLogin>
    {:else}
        <UserRegister onSwitch={handleToLogin}></UserRegister>
    {/if}
</Dialog>

<style lang="scss">
  :global(.MuiListItem-root) {
    border-radius: 8px;
    margin-bottom: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  }

  .document-tab{
    :global(.material-icons){
      color: #ff3e00;
      cursor: pointer;
      font-size: 12px;
    }
  }
</style>
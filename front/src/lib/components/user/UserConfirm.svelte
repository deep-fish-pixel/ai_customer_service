<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import { navigate, useRouter, useLocation, useHistory } from "svelte5-router";
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
    import UserLogin from './UserLogin.svelte';
    import UserRegister from './UserRegister.svelte';


    let focused = $state(false);
    let username: string | null = $state(null);
    let usernameDirty = $state(false);
    let usernameInvalid = $state(false);
    let password: string | null = $state(null);
    let passwordDirty = $state(false);
    let passwordInvalid = $state(false);
    const router = useRouter();
    const location = useLocation();
    const history = useHistory();

    let visible = $state(true);
</script>

<Dialog
        bind:open={visible}
        aria-labelledby="simple-title"
        aria-describedby="simple-content"
        onclick={(e) => {
          // 禁止关闭
          setTimeout(() => {
            visible = true;
          }, 80)
        }}
>
    <UserLogin></UserLogin>
    <UserRegister></UserRegister>
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
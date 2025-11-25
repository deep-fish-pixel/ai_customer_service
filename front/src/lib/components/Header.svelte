<script lang="ts">
  import Menu from '@smui/menu';
  import userIcon from "../../assets/user.svg";
  import List, { Item, Text } from '@smui/list';
  import {resetUser} from "../state/userState.svelte";
  import type {User} from "../types/user";


  const { userinfo, onLoginVisible }: {
    userinfo: User,
    onLoginVisible: (visible: boolean) => void
  } = $props();

  let menu: Menu;

  const handleUserClick = () => {
    if (userinfo.nickname) {
      menu.setOpen(true)
    } else {
      onLoginVisible(true);
    }
  }

  const userLogoutHandle = () => {
    resetUser();
    window.location.reload();
  }
</script>

<header class="header">
  <p>AI智能客服</p>
  <div>
    <div class="user-icon" onclick={handleUserClick}>
      <img src={userIcon} width="30" height="30" alt="user"/>
    </div>
    <Menu bind:this={menu}>
      <List>
        <Item onSMUIAction={userLogoutHandle}>
          <Text>退出登录</Text>
        </Item>
      </List>
    </Menu>
  </div>
  <span class="user-nickname">{userinfo.nickname}</span>
</header>

<style lang="scss">
  .header {
    color: #fff;
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: 24px;
    padding: 14px 20px 10px;
    gap: 12px;
    display: flex;

    p {
      flex: 1;
      margin: 0;
      padding: 0;
    }

    .user-icon {
      color: #fff;
      width: 30px;
      height: 30px;
      cursor: pointer;
    }

    .user-nickname {
      font-size: 14px;
    }
  }
</style>
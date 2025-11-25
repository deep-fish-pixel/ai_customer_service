<script lang="ts">
  import {type Component, onMount,} from 'svelte';
  import SettingsPanel from '../components/settings/SettingsPanel.svelte';
  import ChatArea from '../components/chat/chatArea/Index.svelte';
  import ChatInput from '../components/chat/chatInput/Index.svelte';
  import type {FileItem, ToolConfig} from "../types";
  import type {Message,} from "../types/chat";
  import Toast from "../components/Toast.svelte";
  import UserConfirm from "../components/user/UserConfirm.svelte";
  import {getUserinfo} from "../services/userService";
  import { chatMessageState }  from "../state/chatMessages.svelte"
  import {
    RESPONSE_STATUS_FAILED,
    RESPONSE_STATUS_FAILED_TOKEN_INVALID,
    RobotPrologue
  } from "../../constants";
  import {getTokenAuthorization} from "../utils/authorization";
  import Header from "../components/Header.svelte";
  import {getUser, resetUser, setUser} from "../state/userState.svelte";

  let loginVisible = $state(false);
  let userinfo = $state(getUser());
  let chatAreaContainer: any;
  let chatInputContainer: any;

  // 初始化示例消息
  onMount(async () => {
    chatMessageState.messages = [
      {
        id: '1',
        content: RobotPrologue,
        sender: 'bot',
        timestamp: new Date()
      }
    ];

    try {
      // 检测token是否有效
      if (getTokenAuthorization().Authorization) {
        const response = await getUserinfoLocal();

        if (response.status === RESPONSE_STATUS_FAILED || response.status === RESPONSE_STATUS_FAILED_TOKEN_INVALID) {
          showLogin();
        }
      } else {
        showLogin();
      }

    } catch (e) {
      console.error(e)
    }
  });

  function showLogin() {
    loginVisible = true;
    resetUser();
    userinfo = getUser();
  }

  // 获取用户信息并更新本地数据
  const getUserinfoLocal = async () => {
    const response = await getUserinfo();

    if (response && response.data) {
      setUser(response.data);
      userinfo = getUser();
    }

    return response;
  }

  const handleClose = () => {
    loginVisible = false;
    window.location.reload();
  }

  const handleToolOperation = (message?: string) => {
    if (message) {
      chatInputContainer.sendMessage(message);
    }
  }

  const loginVisibleHandle = (visible: boolean) => {
    loginVisible = visible;
  }

  const scrollToBottomHandle = () => {
    console.log(chatAreaContainer)
    chatAreaContainer.scrollToBottom();
  }
</script>

<div class="app-container">
  <Toast></Toast>
  <Header userinfo={userinfo} onLoginVisible={loginVisibleHandle}/>
  <div class="content">
    <div class="chat-container">
      <div class="chat-inner-container">
        <ChatArea bind:this={chatAreaContainer}/>
        <ChatInput
            bind:this={chatInputContainer}
            onScrollToBottom={scrollToBottomHandle}
            onGetUserinfoLocal={getUserinfoLocal}
        />
      </div>
    </div>
    <!-- 右侧设置区域 -->
    <SettingsPanel
        onToolOperate={handleToolOperation}
    />
  </div>
  <UserConfirm visible={loginVisible} onclose={handleClose}></UserConfirm>
</div>

<style lang="scss">
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #f5f5f5;
  }

  .app-container {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .content {
    display: flex;
    flex-direction: row;
    flex: 1;
  }

  .chat-container {
    height: 100%;
    width: 100%;
    display: flex;
    background-color: #ffffff;
    flex: 1;
    justify-content: center;
  }

  .chat-inner-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    max-width: 1000px;
    padding: 0;
  }


  /* 滚动条样式 */
  ::-webkit-scrollbar {
    width: 6px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  ::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }

  /* 确保Textfield正确显示多行 */
  :global(.MuiOutlinedInput-root) {
    min-height: 48px;
    max-height: 120px;
  }

  :global(.MuiOutlinedInput-inputMultiline) {
    min-height: 48px;
    max-height: 120px;
    overflow-y: auto;
    padding: 10px 14px;
  }

  .hide-scrollbar::-webkit-scrollbar {
    display: none; /* Chrome/Safari/Opera */
    width: 0;
  }

</style>

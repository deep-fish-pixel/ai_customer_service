<script lang="ts">
  import {onMount, tick} from 'svelte';
  import SettingsPanel from '../components/settings/SettingsPanel.svelte';
  import ChatMessage from '../components/ChatMessage.svelte';
  import Textfield from '@smui/textfield';
  import Button, {Label} from '@smui/button';
  import Paper from '@smui/paper';
  import type {FileItem, ToolConfig} from "../types";
  import type {Message,} from "../types/chat";
  import SendIcon from "../icons/SendIcon.svelte";
  import userIcon from "../../assets/user.svg";
  import {sendChatMessageStream} from '../services/chatService';
  import Toast from "../components/Toast.svelte";
  import UserConfirm from "../components/user/UserConfirm.svelte";
  import {getUserId, setUser, getUser, resetUser,} from "../utils/getUser";
  import {getUserinfo} from "../services/userService";
  import {
    JsonSeperatorRegex,
    RESPONSE_STATUS_FAILED,
    RESPONSE_STATUS_FAILED_TOKEN_INVALID,
    RobotPrologue
  } from "../../constants";
  import {getTokenAuthorization} from "../utils/authorization";
  import { getRecentMessages, } from "../utils/handleMessages";
  import StopIcon from "../icons/StopIcon.svelte";

  // 状态管理
  let inputContainer: HTMLElement;
  let messageContainer: HTMLElement;
  let messages: Message[] = $state([]);
  let task_type = '';
  let inputMessage = $state('');
  let files: FileItem[] = $state([]);
  let tools: ToolConfig[] = $state([]);
  let height = $state(500);
  let focus = $state(false);
  let loginVisible = $state(false);
  let disabled = $derived(!inputMessage || !getUserId());
  let userinfo = $state(getUser());
  let receiving = $state(false);
  // 停止接收消息流句柄
  let abortStream: () => void;

  // 初始化示例消息
  onMount(async () => {
    messages = [
      {
        id: '1',
        content: RobotPrologue,
        sender: 'bot',
        timestamp: new Date()
      }
    ];

    resize();

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

    function showLogin() {
      loginVisible = true;
      resetUser();
      userinfo = getUser();
    }

  });

  // 获取用户信息并更新本地数据
  const getUserinfoLocal = async () => {
    const response = await getUserinfo();

    if (response && response.data) {
      setUser(response.data);
      userinfo = getUser();
    }

    return response;
  }

  // 发送消息
  const sendMessage = async () => {
    if (!inputMessage.trim() || receiving) return;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage.trim(),
      sender: 'user',
      task_status: -1,
      timestamp: new Date(),
    };

    // 最近4条消息
    const history = getRecentMessages(messages, 20);

    messages = [...messages, userMessage];

    console.log('send========', messages);

    // 创建临时机器人消息
    const botMessageId = (Date.now() + 1).toString();
    const botMessage: Message = {
      id: botMessageId,
      content: '',
      sender: 'bot',
      task_status: -1,
      timestamp: new Date(),
    };
    messages = [...messages, botMessage];

    // 清空输入框
    inputMessage = '';

    // 滚动到底部
    await tick();
    scrollToBottom();

    // 接收消息
    receiving = true;

    try {
      // 使用流式请求
      abortStream = sendChatMessageStream(
        userMessage.content,
        history,
        task_type,
        (chunk) => {
          // 更新机器人消息内容
          // 任务类型
          if (chunk && chunk.match(/\{'extract_info':/)) {
            return;
          }

          if (chunk && chunk.match(/\{'(task_status|collect_info|collect_origin)':/)) {
            chunk = chunk.replace(/: None/g, ': null');
            const response = new Function('return ' + chunk)();

            if (!response || response.task_status === 0) {
              return;
            }

            response.query = response.query.replace(JsonSeperatorRegex.CALL_GET_USER_INFO, () => {
              // 触发调用接口
              getUserinfoLocal();
              return '';
            })

            const task_status = response.task_status;
            // 任务完成后结束任务类型
            if (task_status === 2) {
              task_type = '';
            } else {
              task_type = response.task_type;
            }

            messages = messages.map((msg, index) => {
              if (msg.id === botMessageId) {
                if(task_status >= 0) {
                  const lastMessage = messages[index -1];

                  if (lastMessage && !Number.isInteger(lastMessage.task_status)) {
                    lastMessage.task_status = 0;
                  }
                }
                return {
                  ...msg,
                  content: msg.content + response.query,
                  task_status: task_status,
                }
              }

              return msg;
            });

            console.log('receive===========1', messages);
          } else {
              messages = messages.map(msg =>
                  msg.id === botMessageId ? {...msg, content: msg.content + chunk} : msg
              );
            console.log('receive===========2', messages);
          }


          scrollToBottom();
        },
        () => {
          // 流结束
          scrollToBottom();
          receiving = false;
        },
        (error) => {
          // 处理错误
          messages = messages.map(msg =>
            msg.id === botMessageId ? {
              ...msg,
              content: msg.content + (error.message.match(/aborted/) ? ' 该请求被取消' : ` 请求错误: ${error.message}`),
              sender: 'bot'
            } : msg
          );
          scrollToBottom();

          receiving = false;
        }
      );
    } catch (error) {
      messages = messages.map(msg =>
        msg.id === botMessageId ? {
          ...msg,
          content: '连接服务器失败，请稍后重试',
          sender: 'bot'
        } : msg
      );
      scrollToBottom();

      receiving = false;
    }

    // 提供取消功能
    return () => abortStream && abortStream();
  };

  const stopReceiveMessage = async () => {
    receiving = false;
    abortStream();
  }

  // 处理输入框回车事件
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !disabled) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 滚动到底部
  const scrollToBottom = () => {
    if (messageContainer) {
      messageContainer.scrollTop = messageContainer.scrollHeight;
    }
  };

  // 文件上传处理
  const handleFileUpload = (file: File) => {
    const newFile: FileItem = {
      id: Date.now().toString(),
      name: file.name,
      uploadTime: new Date().toLocaleString('zh-CN'),
      size: file.size
    };
    files = [...files, newFile];

    // 模拟上传成功消息
    const uploadMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: `文件 "${file.name}" 上传成功！`,
      sender: 'bot',
      timestamp: new Date()
    };
    messages = [...messages, uploadMessage];
  };

  // 文件删除处理
  const handleFileDelete = (fileId: string) => {
    files = files.filter(file => file.id !== fileId);
  };

  // 文件查看处理
  const handleFileView = (fileId: string) => {
    const file = files.find(f => f.id === fileId);
    if (file) {
      // 模拟查看文件操作
      console.log('查看文件:', file.name);
    }
  };

  // 工具切换处理
  const handleFocus = (focused: boolean) => {
    focus = focused;
    tick().then(() => resize());
  };

  const resize = () => {
    height = window.innerHeight - 80 - (inputContainer ? inputContainer.clientHeight + 48 : 0);

    // fix Textfield bug
    inputContainer.querySelector('textarea')?.setAttribute('placeholder', '请输入您的问题...');
  };

  window.addEventListener('resize', resize)

  const handleClose = () => {
    loginVisible = false;
    window.location.reload();
  }

  const handleUserClick = () => {
    if (!userinfo.nickname) {
      loginVisible = true;
    }
  }

  const handleToolOperation = (message?: string) => {
    if (message) {
      inputMessage = message;
      sendMessage();
    }
  }
</script>

<div class="app-container">
  <Toast></Toast>
  <header class="header">
    <p>AI超级智能客服</p>
    <div class="user-icon" onclick={handleUserClick}>
      <img src={userIcon} width="30" height="30" alt="user"/>
    </div>
    <span class="user-nickname">{userinfo.nickname}</span>
  </header>
  <div class="content">
    <div class="chat-container">
      <div class="chat-inner-container">
        <!-- 消息列表 -->
        <div class="messages-container hide-scrollbar" style={"height:" + height + "px;"}
             bind:this={messageContainer}>
          <div class="messagess">
            {#each messages as message}
              <ChatMessage message={message}/>
            {/each}
          </div>
        </div>

        <!-- 输入区域 -->
        <Paper elevation={2} class="input-container">
          <div class="input-wrapper" bind:this={inputContainer}>
            <Textfield
                class={focus ? 'input-focus' : 'input-focusout'}
                textarea={true}
                variant="outlined"
                value={inputMessage}
                oninput={(e) => inputMessage = (e.target as HTMLInputElement)?.value}
                onkeydown={handleKeyPress}
                onfocus={() => handleFocus(true)}
                onfocusout={() => handleFocus(false)}
                placeholder="请输入您的问题..."
            />
            {#if receiving}
              <Button
                  class="send-button"
                  color="primary"
                  onclick={stopReceiveMessage}
                  title="取消接收消息"
              >
                <StopIcon></StopIcon>
              </Button>
            {:else}
              <Button
                  class="send-button"
                  color="primary"
                  onclick={sendMessage}
                  disabled={disabled}
                  title="发送消息"
              >
                <SendIcon></SendIcon>
              </Button>
            {/if}

          </div>
        </Paper>
      </div>
    </div>

    <!-- 右侧设置区域 -->
    <div class="settings-container">
      <SettingsPanel
          onToolOperate={handleToolOperation}
      />
    </div>
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

  .header {
    width: 100%;
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
    padding: 10px 0 0 0;
  }

  .messages-container {
    padding: 16px;
    overflow-y: scroll;
    background-color: #eee;
  }

  .messagess {
    display: flex;
    flex-direction: column;
  }

  .input-container {
    padding: 16px;
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
  }

  .input-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    position: relative;

    :global(.input-focusout) {
      width: 100%;
      height: 56px;

      :global(textarea) {
        resize: none;
      }
    }

    :global(.input-focus) {
      width: 100%;
      height: 100px;

      :global(textarea) {
        resize: none;
        width: 100%;
      }
    }

    :global(.mdc-text-field__resizer) {
      width: 100%;
      resize: none;
    }

    :global(.mdc-notched-outline__leading) {
      border-width: 1px;
    }

    :global(.mdc-notched-outline__trailing) {
      border-width: 1px;
    }

    :global(.send-button) {
      min-width: 44px;
      overflow: hidden;
      padding: 0;
      margin: 0;
      outline: none;
      border: none;
      position: absolute;
      right: 0;
      bottom: 8px;
    }
  }


  .settings-container {
    height: 100%;
    background-color: #ffffff;
    border-left: 1px solid var(--boxBorderColor);
    width: 350px;
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

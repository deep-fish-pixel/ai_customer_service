<script lang="ts">
  import { onMount, tick } from 'svelte';
  import SettingsPanel from './lib/components/settings/SettingsPanel.svelte';
  import ChatMessage from './lib/components/ChatMessage.svelte';
  import Textfield from '@smui/textfield';
  import Button from '@smui/button';
  import Paper from '@smui/paper';
  import type {FileItem, ToolConfig} from "./lib/types";
  import type { Message, } from "./lib/types/chat";
  import SendIcon from "./lib/icons/SendIcon.svelte";
  import { sendChatMessage, sendChatMessageStream } from './lib/services/chatService';


  // 状态管理
  let inputContainer: HTMLElement;
  let messageContainer: HTMLElement;
  let messages: Message[] = [];
  let inputMessage: string = '';
  let files: FileItem[] = [];
  let tools: ToolConfig[] = [];
  let height = 500;
  let focus = false;

  $: disabled = !inputMessage;

  // 初始化示例消息
  onMount(() => {
    messages = [
      {
        id: '1',
        content: '您好！我是小智，是你的智能客服助手，有什么可以帮助您的吗？',
        sender: 'bot',
        timestamp: new Date()
      }
    ];

    resize();

  });

  // 发送消息
  const sendMessage = async () => {
    if (!inputMessage.trim() ) return;
    
    let abortStream: () => void;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    // 最近4条消息
    const history = messages.slice(Math.max(0, messages.length - 10), messages.length);

    messages = [...messages, userMessage];
    
    // 创建临时机器人消息
    const botMessageId = (Date.now() + 1).toString();
    const botMessage: Message = {
      id: botMessageId,
      content: '',
      sender: 'bot',
      timestamp: new Date()
    };
    messages = [...messages, botMessage];
    
    // 清空输入框
    inputMessage = '';
    
    // 滚动到底部
    await tick();
    scrollToBottom();
    
    try {
      // 使用流式请求
      abortStream = sendChatMessageStream(
        userMessage.content,
        history,
        (chunk) => {
          // 更新机器人消息内容
          messages = messages.map(msg => 
            msg.id === botMessageId ? { ...msg, content: msg.content + chunk } : msg
          );
          scrollToBottom();
        },
        () => {
          // 流结束
          scrollToBottom();
        },
        (error) => {
          // 处理错误
          messages = messages.map(msg => 
            msg.id === botMessageId ? {
              ...msg,
              content: `请求错误: ${error.message}`,
              sender: 'bot'
            } : msg
          );
          scrollToBottom();
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
    }

    // 提供取消功能
    return () => abortStream && abortStream();
  };

  // 处理输入框回车事件
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
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
  const handleToolToggle = (toolId: string, enabled: boolean) => {
    tools = tools.map(tool =>
            tool.id === toolId ? { ...tool, enabled } : tool
    );
  };

  // 工具切换处理
  const handleFocus = (focused: boolean) => {
    focus = focused;
    tick().then(() => resize());
  };

  const resize = () =>  {
    height = window.innerHeight - 80 - (inputContainer ? inputContainer.clientHeight + 48 : 0);

    // fix Textfield bug
    inputContainer.querySelector('textarea')?.setAttribute('placeholder', '请输入您的问题...');
  };

  window.addEventListener('resize', resize)
</script>

<div class="app-container">
  <header class="header">
    AI智能客服
  </header>
  <div class="content">
    <div class="chat-container">
      <div class="chat-inner-container">
        <!-- 消息列表 -->
        <div class="messages-container hide-scrollbar" style={"height:" + height + "px;"} bind:this={messageContainer}>
          <div class="messagess">
            {#each messages as message}
              <ChatMessage message={message} />
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
                    oninput={(e) => inputMessage = (e.target as HTMLTextAreaElement)?.value}
                    onkeydown={handleKeyPress}
                    onfocus={() => handleFocus(true)}
                    onfocusout={() => handleFocus(false)}
                    placeholder="请输入您的问题..."
            />
            <Button
                    class="send-button"
                    color="primary"
                    onclick={sendMessage}
                    disabled={disabled}
            >
              <SendIcon></SendIcon>
            </Button>
          </div>
        </Paper>
      </div>
    </div>

    <!-- 右侧设置区域 -->
    <div class="settings-container">
      <SettingsPanel
              {files}
              {tools}
              onFileUpload={handleFileUpload}
              onFileDelete={handleFileDelete}
              onFileView={handleFileView}
              onToolToggle={handleToolToggle}
      />
    </div>
  </div>
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

  .header{
    width: 100%;
    color: var(--mainTextColor);
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: 24px;
    padding: 14px 20px;
    gap: 12px;
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

  .chat-inner-container{
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

    :global(.input-focusout){
      width: 100%;
      height: 56px;
      :global(textarea) {
        resize: none;
      }
    }
    :global(.input-focus){
      width: 100%;
      height: 100px;
      :global(textarea) {
        resize: none;
        width: 100%;
      }
    }
    :global(.mdc-text-field__resizer){
      width: 100%;
      resize: none;
    }
    :global(.mdc-notched-outline__leading){
      border-width: 1px;
    }
    :global(.mdc-notched-outline__trailing){
      border-width: 1px;
    }
    :global(.send-button){
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

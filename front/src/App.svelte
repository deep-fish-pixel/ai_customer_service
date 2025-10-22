<script lang="ts">
  import { onMount, tick } from 'svelte';
  import ResizableSplitPanel from './lib/components/ResizableSplitPanel.svelte';
  import SettingsPanel from './lib/components/settings/SettingsPanel.svelte';
  import ChatMessage from './lib/components/ChatMessage.svelte';
  import Textfield from '@smui/textfield';
  import Button from '@smui/button';
  import Paper from '@smui/paper';
  import type {FileItem, Message, ToolConfig} from "./types";

  // 状态管理
  let messages: Message[] = [];
  let inputMessage: string = '';
  let messageContainer: HTMLElement;
  let files: FileItem[] = [];
  let tools: ToolConfig[] = [];

  // 初始化示例消息
  onMount(() => {
    messages = [
      {
        id: '1',
        content: '您好！我是智能客服助手，有什么可以帮助您的吗？',
        sender: 'bot',
        timestamp: new Date()
      }
    ];
  });

  // 发送消息
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date()
    };
    messages = [...messages, userMessage];
    
    // 清空输入框
    inputMessage = '';
    
    // 滚动到底部
    await tick();
    scrollToBottom();

    // 模拟机器人回复
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `您刚刚说："${userMessage.content}"\n\n这是一条模拟回复。在实际应用中，这里会显示AI生成的回复。`,
        sender: 'bot',
        timestamp: new Date()
      };
      messages = [...messages, botMessage];
      
      tick().then(() => scrollToBottom());
    }, 1000);
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
    
    tick().then(() => scrollToBottom());
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
</script>

<div class="app-container">
  <ResizableSplitPanel>
    <!-- 左侧聊天区域 -->
    <div slot="left" class="chat-container">
      <!-- 消息列表 -->
      <div class="messages-container" bind:this={messageContainer}>
        {#each messages as message}
          <ChatMessage {message} />
        {/each}
      </div>

      <!-- 输入区域 -->
      <Paper elevation={2} class="input-container">
        <div class="input-wrapper">
          <Textfield
            variant="outlined"
            value={inputMessage}
            oninput={(e) => inputMessage = e.target && e.target.value}
            onkeydown={handleKeyPress}
            placeholder="请输入您的问题..."
          />
          <Button
            color="primary"
            onclick={sendMessage}
            style="marginLeft: '8px';minWidth: '64px';"
          >
            发送
          </Button>
        </div>
      </Paper>
    </div>

    <!-- 右侧设置区域 -->
    <div slot="right" class="settings-container">
      <SettingsPanel
        {files}
        {tools}
        onFileUpload={handleFileUpload}
        onFileDelete={handleFileDelete}
        onFileView={handleFileView}
        onToolToggle={handleToolToggle}
      />
    </div>
  </ResizableSplitPanel>
</div>

<style lang="scss">
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html, body, #app {
    height: 100%;
    width: 100%;
    overflow: hidden;
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

  .chat-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
  }

  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px 0;
    background-color: #fafafa;
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
  }

  .settings-container {
    height: 100%;
    background-color: #ffffff;
    border-left: 1px solid #e0e0e0;
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
</style>
